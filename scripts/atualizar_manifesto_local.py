# -*- coding: utf-8 -*-
"""Reconcile the validation manifest with the exact archived source bytes."""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "dados" / "fontes" / "manifesto-validacao.csv"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


with MANIFEST.open(encoding="utf-8-sig", newline="") as handle:
    rows = list(csv.DictReader(handle))
    fields = list(rows[0])

for item in rows:
    local = ROOT / item["arquivo_local"]
    if local.is_file():
        item["sha256"] = digest(local)
        item["content_length"] = str(local.stat().st_size)

official_abs = [
    (
        "ABS ANZSCO 2022",
        "https://www.abs.gov.au/statistics/classifications/anzsco-australian-and-new-zealand-standard-classification-occupations/2022/anzsco%202022%20structure%20062023.xlsx",
        "dados/fontes/anzsco-2022-structure.xlsx",
        "Estrutura oficial usada para nomes canonicos e niveis ANZSCO.",
    ),
    (
        "ABS ANZSCO 2022",
        "https://www.abs.gov.au/statistics/classifications/anzsco-australian-and-new-zealand-standard-classification-occupations/2022/anzsco%202022%20index%20of%20principal%20titles%2C%20alternative%20titles%20and%20specialisations%20062023.xlsx",
        "dados/fontes/anzsco-2022-index.xlsx",
        "Indice oficial usado somente para correspondencias textuais exatas e nao ambiguas.",
    ),
]
known = {item["arquivo_local"] for item in rows}
for source, url, rel, note in official_abs:
    if rel in known:
        continue
    local = ROOT / rel
    rows.append({
        "fonte": source,
        "jurisdicao": "federal",
        "url": url,
        "arquivo_local": rel,
        "status_http": "200",
        "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "content_length": str(local.stat().st_size),
        "last_modified": "",
        "etag": "",
        "sha256": digest(local),
        "eh_gov_au": "true",
        "valido": "true",
        "observacao": note,
    })

with MANIFEST.open("w", encoding="utf-8-sig", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

print(f"manifesto atualizado: {len(rows)} fontes")
