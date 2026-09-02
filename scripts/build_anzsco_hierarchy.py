"""Build the dashboard's ANZSCO hierarchy lookup from the official ABS workbook."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "dados" / "fontes" / "anzsco-2022-structure.xlsx"
OUTPUT = ROOT / "analise" / "anzsco-hierarchy.js"

SHEETS = {
    "Table 1": (1, "major"),
    "Table 2": (2, "sub_major"),
    "Table 3": (3, "minor"),
    "Table 4": (4, "unit"),
    "Table 5": (6, "occupation"),
}


def clean_code(value: object, length: int) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip().removesuffix(".0")
    return text if text.isdigit() and len(text) == length else ""


def clean_skill(value: object) -> list[int]:
    if pd.isna(value):
        return []
    text = str(value).strip()
    australian = re.search(r"([1-5])\s*Aus\b", text, flags=re.IGNORECASE)
    if australian:
        return [int(australian.group(1))]
    return sorted({int(level) for level in re.findall(r"[1-5]", text)})


def main() -> None:
    nodes: dict[str, dict[str, object]] = {}
    for sheet_name, (length, level) in SHEETS.items():
        frame = pd.read_excel(SOURCE, sheet_name=sheet_name, header=None)
        code_column = length - 1 if length < 6 else 4
        name_column = code_column + 1
        skill_column = frame.shape[1] - 1
        for _, row in frame.iterrows():
            code = clean_code(row.iloc[code_column], length)
            if not code:
                continue
            name = "" if pd.isna(row.iloc[name_column]) else str(row.iloc[name_column]).strip()
            if not name:
                continue
            nodes[code] = {
                "name": name,
                "level": level,
                "skills": clean_skill(row.iloc[skill_column]),
            }

    payload = {
        "version": "ANZSCO 2022 Australian Update",
        "source": "../dados/fontes/anzsco-2022-structure.xlsx",
        "nodes": dict(sorted(nodes.items(), key=lambda item: (len(item[0]), item[0]))),
    }
    OUTPUT.write_text(
        "window.ANZSCO_HIERARCHY = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(nodes):,} ANZSCO nodes to {OUTPUT}")


if __name__ == "__main__":
    main()
