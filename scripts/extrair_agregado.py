# -*- coding: utf-8 -*-
"""Parse already-downloaded official .gov.au invitation sources into one aggregated dataset."""
from __future__ import annotations

import csv
import hashlib
import html as htmlmod
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup
try:
    from pypdf import PdfReader
except ImportError:  # compatibility with the existing local extraction runtime
    from PyPDF2 import PdfReader
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "dados" / "agregado"
MANIFESTO = ROOT / "dados" / "fontes" / "manifesto-validacao.csv"
ANZSCO_STRUCTURE = ROOT / "dados" / "fontes" / "anzsco-2022-structure.xlsx"
ANZSCO_INDEX = ROOT / "dados" / "fontes" / "anzsco-2022-index.xlsx"

FIELDS = [
    "categoria",
    "nivel",
    "jurisdicao",
    "visto",
    "data_round",
    "ocupacao",
    "anzsco",
    "ocupacao_canonica",
    "classificacao",
    "classificacao_versao",
    "nivel_ocupacional",
    "codigo_status",
    "identidade_ocupacional",
    "metrica",
    "valor",
    "unidade_extra",
    "fonte_url",
    "arquivo_local",
    "sha256_fonte",
    "validado",
]

MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
}
MONTH_HEADERS = ["jul", "aug", "sep", "sept", "oct", "nov", "dec", "jan", "feb", "mar", "apr", "may", "jun"]

LOG = []
ERRORS = []
COUNTS = defaultdict(int)


def log(msg: str) -> None:
    LOG.append(msg)


def err(msg: str) -> None:
    ERRORS.append(msg)
    LOG.append("ERRO: " + msg)


def norm(s) -> str:
    return re.sub(r"\s+", " ", (s or "").replace("\xa0", " ").replace("\u200b", "")).strip()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifesto() -> dict:
    out = {}
    with MANIFESTO.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            key = (row.get("arquivo_local") or "").replace("\\", "/").strip()
            if key:
                out[key] = row
    return out


def source_meta(manifesto: dict, rel: str) -> tuple[str, str, str]:
    rel = rel.replace("\\", "/")
    path = ROOT / rel
    digest = sha256_file(path) if path.exists() else ""
    rec = manifesto.get(rel, {})
    url = rec.get("url") or ""
    man_sha = (rec.get("sha256") or "").strip()
    if man_sha and digest and man_sha.lower() != digest.lower():
        err(f"SHA256 diverge do manifesto para {rel}: arquivo={digest} manifesto={man_sha}")
    return url, rel, digest or man_sha


def row(
    *,
    nivel: str,
    jurisdicao: str,
    visto: str,
    data_round: str,
    ocupacao: str,
    anzsco: str,
    metrica: str,
    valor: str,
    unidade_extra: str,
    fonte_url: str,
    arquivo_local: str,
    sha256_fonte: str,
    validado: bool = True,
) -> dict:
    return {
        "categoria": "visto_de_convite",
        "nivel": nivel,
        "jurisdicao": jurisdicao,
        "visto": visto or "n/a",
        "data_round": data_round or "",
        "ocupacao": ocupacao or "",
        "anzsco": anzsco or "",
        "metrica": metrica,
        "valor": "" if valor is None else str(valor),
        "unidade_extra": unidade_extra or "",
        "fonte_url": fonte_url,
        "arquivo_local": arquivo_local,
        "sha256_fonte": sha256_fonte,
        "validado": "true" if validado else "false",
    }


def clean_value(raw: str) -> str | None:
    s = norm(raw).replace(",", "")
    if not s or s in {"-", "–", "—", "."}:
        return None
    low = s.lower().replace("*", "").replace("**", "")
    if low in {"n/a", "na", "not invited", "not applicable"}:
        return "N/A"
    s = re.sub(r"[*]+$", "", s).strip()
    return s


def match_key(value: str) -> str:
    """Conservative title key: formatting only, never fuzzy similarity."""
    return re.sub(r"[^a-z0-9]+", " ", norm(value).casefold()).strip()


def anzsco_level(code: str) -> str:
    return {
        1: "major_group",
        2: "sub_major_group",
        3: "minor_group",
        4: "unit_group",
        6: "occupation",
    }.get(len(code or ""), "unclassified")


def load_anzsco_reference() -> tuple[dict, dict]:
    """Load official ABS ANZSCO 2022 titles/aliases; retain only unambiguous matches."""
    if not ANZSCO_STRUCTURE.exists() or not ANZSCO_INDEX.exists():
        raise FileNotFoundError("Official ABS ANZSCO 2022 reference workbooks are missing")

    canonical: dict[str, str] = {}
    wb = load_workbook(ANZSCO_STRUCTURE, read_only=True, data_only=True)
    for code, title, *_ in wb["Table 6"].iter_rows(min_row=7, values_only=True):
        code = str(code or "").strip()
        if re.fullmatch(r"\d{6}", code) and title:
            canonical[code] = norm(str(title))

    candidates: dict[str, set[str]] = defaultdict(set)
    wb = load_workbook(ANZSCO_INDEX, read_only=True, data_only=True)
    for code, title, *_ in wb["Table 1"].iter_rows(min_row=7, values_only=True):
        code = str(code or "").strip()
        if re.fullmatch(r"\d{6}", code) and title:
            candidates[match_key(str(title))].add(code)
    title_to_code = {k: next(iter(v)) for k, v in candidates.items() if len(v) == 1}
    return canonical, title_to_code


def enrich_occupations(rows: list[dict]) -> dict[str, int]:
    canonical, title_to_code = load_anzsco_reference()
    stats = defaultdict(int)
    for r in rows:
        published = norm(r.get("ocupacao", ""))
        source_code = re.sub(r"\D", "", r.get("anzsco", "") or "")
        code = source_code
        status = "source" if code else "missing"

        # Aggregates/publication sentinels are intentionally not occupations.
        if not code and published and published.casefold() != "agregado" and r.get("metrica") != "publicacao":
            inferred = title_to_code.get(match_key(published), "")
            if inferred:
                code = inferred
                status = "abs_exact_title"

        level = anzsco_level(code)
        canonical_title = canonical.get(code, "") if len(code) == 6 else ""
        if not canonical_title:
            canonical_title = published

        r["anzsco"] = code
        r["ocupacao_canonica"] = canonical_title
        r["classificacao"] = "ANZSCO" if code else ""
        r["classificacao_versao"] = "2022" if code else ""
        r["nivel_ocupacional"] = level
        r["codigo_status"] = status
        r["identidade_ocupacional"] = (
            f"ANZSCO-2022:{code}" if code else f"UNCLASSIFIED:{match_key(published)}"
        )
        stats[status] += 1
    return dict(stats)


def parse_english_date(text: str) -> str:
    t = norm(htmlmod.unescape(text or ""))
    t = t.replace(",", " ")
    m = re.search(
        r"\b(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(20\d{2})\b",
        t,
        re.I,
    )
    if m:
        return f"{int(m.group(3)):04d}-{MONTHS[m.group(2).lower()]:02d}-{int(m.group(1)):02d}"
    m = re.search(
        r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(20\d{2})\b",
        t,
        re.I,
    )
    if m:
        return f"{int(m.group(2)):04d}-{MONTHS[m.group(1).lower()]:02d}"
    m = re.search(r"\b(20\d{2})-(\d{2})-(\d{2})\b", t)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    m = re.search(r"\b(20\d{2})-(\d{2})\b", t)
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    m = re.search(r"\b(20\d{2})[–-](\d{2})\b", t)
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    return ""


def parse_numeric_date(text: str) -> str:
    t = norm(text)
    m = re.search(r"\b(\d{1,2})/(\d{1,2})/(20\d{2})\b", t)
    if m:
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if 1 <= mo <= 12 and 1 <= d <= 31:
            return f"{y:04d}-{mo:02d}-{d:02d}"
    m = re.search(r"\b(\d{1,2})/(20\d{2})\b", t)
    if m:
        mo, y = int(m.group(1)), int(m.group(2))
        if 1 <= mo <= 12:
            return f"{y:04d}-{mo:02d}"
    m = re.search(r"\b(\d{1,2})/(\d{4})\b", t)
    if m and int(m.group(1)) <= 12:
        return f"{int(m.group(2)):04d}-{int(m.group(1)):02d}"
    return parse_english_date(t)


def program_year_month(label: str, program_year: str) -> str:
    key = norm(label).lower().rstrip(".")
    if key not in MONTHS:
        return ""
    mo = MONTHS[key]
    m = re.match(r"(20\d{2})\s*[–-]\s*(\d{2})", program_year or "")
    if not m:
        return ""
    start_y = int(m.group(1))
    year = start_y if mo >= 7 else start_y + 1
    return f"{year:04d}-{mo:02d}"


def visa_from_text(text: str, *, federal: bool = False) -> str:
    t = norm(text).lower()
    has189 = "189" in t
    has190 = "190" in t
    has491 = "491" in t
    if has189 and not has190 and not has491:
        return "189"
    if has190 and not has189 and not has491:
        return "190"
    if has491 and not has189 and not has190:
        if federal or "family" in t or "fsr" in t or "sponsored" in t:
            return "491-family" if federal or "family" in t or "fsr" in t else "491"
        return "491"
    if has189 and has491:
        return "n/a"
    return "n/a"


def extra_join(*parts: str) -> str:
    items = []
    for p in parts:
        p = norm(p)
        if p and p not in items:
            items.append(p)
    return ";".join(items)


def soup_file(path: Path) -> BeautifulSoup:
    raw = path.read_text(encoding="utf-8", errors="replace")
    return BeautifulSoup(raw, "lxml")


def hidden_json(soup: BeautifulSoup) -> dict | None:
    inp = soup.select_one("#ctl00_PlaceHolderMain_PageSchemaHiddenField_Input")
    if not inp or not inp.get("value"):
        return None
    try:
        return json.loads(inp["value"])
    except json.JSONDecodeError as e:
        err(f"JSON do campo oculto invalido: {e}")
        return None


def expand_row(tr) -> list[str]:
    cells = []
    for c in tr.find_all(["th", "td"], recursive=False):
        text = norm(c.get_text(" ", strip=True))
        try:
            span = max(1, int(c.get("colspan") or 1))
        except ValueError:
            span = 1
        for _ in range(span):
            cells.append(text)
    if not cells:
        for c in tr.find_all(["th", "td"]):
            cells.append(norm(c.get_text(" ", strip=True)))
    return cells


def table_rows(table) -> list[list[str]]:
    return [expand_row(tr) for tr in table.find_all("tr") if expand_row(tr)]


def looks_like_month_header(cells: list[str]) -> bool:
    joined = " ".join(c.lower() for c in cells)
    return ("jul" in joined and "aug" in joined and "jun" in joined) or (
        sum(1 for c in cells if norm(c).lower().rstrip(".") in MONTHS) >= 8
    )


# ---------------------------------------------------------------------------
# FEDERAL
# ---------------------------------------------------------------------------

def parse_federal_html_fragment(html: str) -> list:
    html = htmlmod.unescape(html or "")
    return BeautifulSoup(html, "lxml")


def infer_program_year(round_iso: str) -> str:
    if not round_iso or len(round_iso) < 7:
        return ""
    y, m = int(round_iso[:4]), int(round_iso[5:7])
    start = y if m >= 7 else y - 1
    return f"{start}-{str(start + 1)[2:]}"


def parse_federal_occupation_table(table, round_date: str, meta, federal=True) -> list[dict]:
    rows_out = []
    raw = table_rows(table)
    if len(raw) < 2:
        return rows_out
    # Build column roles from up to 2 header rows
    header0 = raw[0]
    header1 = raw[1] if len(raw) > 1 and not _is_data_occ_row(raw[1]) else None
    start = 2 if header1 is not None else 1
    # If first data-looking row was treated as header1 incorrectly
    if header1 is None:
        start = 1

    n_cols = max(len(r) for r in raw)
    col_visa = ["n/a"] * n_cols
    col_loc = [""] * n_cols

    def assign_visa_from_header(cells):
        for i, c in enumerate(cells):
            cl = c.lower()
            if "189" in cl:
                col_visa[i] = "189"
            elif "491" in cl:
                col_visa[i] = "491-family" if federal else "491"
            elif "190" in cl:
                col_visa[i] = "190"

    assign_visa_from_header(header0)
    if header1 is not None:
        assign_visa_from_header(header1)
        for i, c in enumerate(header1):
            cl = c.lower()
            if "offshore" in cl:
                col_loc[i] = "offshore"
            elif "onshore" in cl:
                col_loc[i] = "onshore"

    # If only occupation + one score column with no visa in header, assume 189
    numeric_cols = [i for i in range(1, n_cols) if i < len(header0) or True]
    visa_set = {v for v in col_visa[1:] if v != "n/a"}
    if not visa_set:
        for i in range(1, n_cols):
            col_visa[i] = "189"

    data_rows = raw[start:]
    # If header1 was actually first occupation (Occupation* / 189 / 491 is header, ok)
    # Detect: header1 looks like occupation data if first cell is not a header word
    if header1 is not None and _is_data_occ_row(header1):
        data_rows = [header1] + raw[1:]
        # wait raw[1:] already includes header1; use raw[1:]
        data_rows = raw[1:]

    for cells in data_rows:
        if not cells:
            continue
        occ = cells[0]
        if not occ or occ.lower() in {"occupation", "occupation*", ""}:
            continue
        if occ.lower().startswith("visa subclass"):
            continue
        anzsco = ""
        mcode = re.match(r"^(\d{4,6})\b\s*(.*)$", occ)
        if mcode:
            anzsco = mcode.group(1)
            occ = mcode.group(2) or occ
        for i, val in enumerate(cells[1:], start=1):
            cleaned = clean_value(val)
            if cleaned is None:
                continue
            loc = col_loc[i] if i < len(col_loc) else ""
            visto = col_visa[i] if i < len(col_visa) else "189"
            rows_out.append(
                row(
                    nivel="federal",
                    jurisdicao="FEDERAL",
                    visto=visto,
                    data_round=round_date,
                    ocupacao=occ,
                    anzsco=anzsco,
                    metrica="pontos_minimos",
                    valor=cleaned,
                    unidade_extra=extra_join(f"location={loc}" if loc else ""),
                    **_meta_kw(meta),
                )
            )
    return rows_out


def _is_data_occ_row(cells: list[str]) -> bool:
    if not cells:
        return False
    first = cells[0].lower().strip("*")
    if first in {"occupation", "occupation*", "", "visa subclass", "subclass"}:
        return False
    if any(k in first for k in ("lowest points", "offshore", "onshore", "minimum points")):
        return False
    return True


def _meta_kw(meta) -> dict:
    url, rel, digest = meta
    return {"fonte_url": url, "arquivo_local": rel, "sha256_fonte": digest}


def parse_federal_totals_table(table, round_date: str, meta, kind_hint: str = "") -> list[dict]:
    rows_out = []
    raw = table_rows(table)
    if len(raw) < 2:
        return rows_out
    header = [c.lower() for c in raw[0]]
    header_join = " ".join(header)
    if "act" in header_join and "nsw" in header_join:
        return rows_out  # state nomination allocations, not invitation results
    if looks_like_month_header(raw[0]):
        return rows_out  # handled separately
    is_cutoff = "minimum points" in header_join or "minimum points score" in header_join
    for cells in raw[1:]:
        if not cells or "visa subclass" in cells[0].lower():
            continue
        visto = visa_from_text(cells[0], federal=True)
        extras = []
        if "family" in cells[0].lower():
            visto = "491-family"
        # values
        for i, val in enumerate(cells[1:], start=1):
            h = header[i] if i < len(header) else ""
            cleaned = clean_value(val)
            if cleaned is None:
                continue
            if "tie" in h or "date of effect" in h or "month and year" in h:
                iso = parse_numeric_date(val) or parse_english_date(val)
                extras.append(f"tiebreak={iso or norm(val)}")
                continue
            if is_cutoff and ("point" in h or i == 1):
                rows_out.append(
                    row(
                        nivel="federal",
                        jurisdicao="FEDERAL",
                        visto=visto,
                        data_round=round_date,
                        ocupacao="agregado",
                        anzsco="",
                        metrica="pontos_minimos",
                        valor=cleaned,
                        unidade_extra=extra_join(*extras),
                        **_meta_kw(meta),
                    )
                )
            elif "number" in h or "eoi" in h or "total" in h or (not is_cutoff and i == 1):
                rows_out.append(
                    row(
                        nivel="federal",
                        jurisdicao="FEDERAL",
                        visto=visto,
                        data_round=round_date,
                        ocupacao="agregado",
                        anzsco="",
                        metrica="eois_convidados",
                        valor=cleaned,
                        unidade_extra=extra_join(*extras),
                        **_meta_kw(meta),
                    )
                )
        # if cutoff table has date-of-effect as last col already handled
    return rows_out


def parse_federal_monthly_table(table, round_date: str, meta, program_year: str) -> list[dict]:
    rows_out = []
    raw = table_rows(table)
    if len(raw) < 2 or not looks_like_month_header(raw[0]):
        return rows_out
    headers = raw[0]
    for cells in raw[1:]:
        label = cells[0] if cells else ""
        if not label or label.lower() in {"total", "total to date"}:
            continue
        visto = visa_from_text(label, federal=True)
        if "family" in label.lower() or (visto == "n/a" and "491" in label):
            visto = "491-family"
        for i, val in enumerate(cells[1:], start=1):
            h = headers[i] if i < len(headers) else ""
            hl = norm(h).lower().rstrip(".")
            if hl in {"total", "total to date"}:
                continue
            cleaned = clean_value(val)
            if cleaned is None or cleaned in {"0", "N/A"}:
                continue
            month_iso = program_year_month(h, program_year)
            if not month_iso:
                continue
            rows_out.append(
                row(
                    nivel="federal",
                    jurisdicao="FEDERAL",
                    visto=visto,
                    data_round=month_iso,
                    ocupacao="agregado",
                    anzsco="",
                    metrica="eois_convidados",
                    valor=cleaned,
                    unidade_extra=extra_join(
                        f"programa={program_year}" if program_year else "",
                        "agregado_mensal=true",
                    ),
                    **_meta_kw(meta),
                )
            )
    return rows_out


def parse_federal_prorata_table(table, round_date: str, meta) -> list[dict]:
    rows_out = []
    raw = table_rows(table)
    if len(raw) < 2:
        return rows_out
    header = [c.lower() for c in raw[0]]
    if "occupation id" not in " ".join(header):
        return rows_out
    for cells in raw[1:]:
        if len(cells) < 4:
            continue
        subclass, occ_id, desc = cells[0], cells[1], cells[2]
        score = clean_value(cells[3] if len(cells) > 3 else "")
        tie = cells[4] if len(cells) > 4 else ""
        visto = "n/a"
        if "189" in subclass and "491" in subclass:
            visto = "n/a"
            extra_v = "visto_publicado=189/491"
        elif "189" in subclass:
            visto = "189"
            extra_v = ""
        elif "491" in subclass:
            visto = "491-family"
            extra_v = ""
        else:
            extra_v = ""
        extras = [extra_v]
        iso = parse_numeric_date(tie)
        if iso:
            extras.append(f"tiebreak={iso}")
        elif clean_value(tie) and clean_value(tie) != "N/A":
            extras.append(f"tiebreak={norm(tie)}")
        if score is None:
            continue
        rows_out.append(
            row(
                nivel="federal",
                jurisdicao="FEDERAL",
                visto=visto,
                data_round=round_date,
                ocupacao=desc,
                anzsco=re.sub(r"\D", "", occ_id),
                metrica="pontos_minimos",
                valor=score,
                unidade_extra=extra_join(*extras, "pro_rata=true"),
                **_meta_kw(meta),
            )
        )
    return rows_out


def classify_and_parse_federal_tables(tables, round_date: str, meta, program_year: str, include_monthly: bool) -> list[dict]:
    out = []
    for table in tables:
        raw = table_rows(table)
        if not raw:
            continue
        header_join = " ".join(raw[0]).lower()
        if "occupation id" in header_join and "subclass" in header_join:
            out.extend(parse_federal_prorata_table(table, round_date, meta))
        elif looks_like_month_header(raw[0]):
            if include_monthly:
                out.extend(parse_federal_monthly_table(table, round_date, meta, program_year))
        elif "visa subclass" in header_join:
            out.extend(parse_federal_totals_table(table, round_date, meta))
        elif "occupation" in header_join or (len(raw) > 2 and _is_data_occ_row(raw[1] if len(raw) > 1 else [])):
            out.extend(parse_federal_occupation_table(table, round_date, meta))
        elif any("occupation" in " ".join(r).lower() for r in raw[:2]):
            out.extend(parse_federal_occupation_table(table, round_date, meta))
        else:
            # try occupation anyway if many 2-col numeric rows
            nums = 0
            for r in raw[1:6]:
                if len(r) >= 2 and re.fullmatch(r"\d{2,3}", (clean_value(r[1]) or "").replace("N/A", "65") or ""):
                    nums += 1
            if nums >= 3:
                out.extend(parse_federal_occupation_table(table, round_date, meta))
    return out


def extract_round_date_from_html(inner: BeautifulSoup, fallback_title: str) -> str:
    for h in inner.find_all(["h2", "h3", "h4"]):
        t = h.get_text(" ", strip=True)
        if re.search(r"invitations issued on", t, re.I):
            d = parse_english_date(t)
            if d:
                return d
    return parse_english_date(fallback_title)


def split_html_on_other_rounds(inner: BeautifulSoup, this_date_text: str):
    """Drop tables that belong to a later 'Invitations issued on <other date>' section."""
    tables = list(inner.find_all("table"))
    headings = []
    for h in inner.find_all(["h2", "h3", "h4"]):
        t = norm(h.get_text(" ", strip=True))
        if re.search(r"invitations issued on", t, re.I):
            headings.append((h, t, parse_english_date(t)))
    if len(headings) <= 1:
        return tables
    this_iso = parse_english_date(this_date_text)
    keep = []
    for table in tables:
        # find nearest preceding invitations-issued heading
        prev = None
        for h, t, iso in headings:
            if table.sourceline and h.sourceline and h.sourceline <= (table.sourceline or 0):
                prev = iso
            elif prev is None:
                # fallback: use document order
                pass
        # BeautifulSoup sourceline may be missing; use occurrence order
        keep.append(table)
    # Safer: cut at the HTML string index of the second matching heading that differs
    html = str(inner)
    matches = list(re.finditer(r"Invitations issued on [^<]+", html, re.I))
    cut = None
    for m in matches[1:]:
        other = parse_english_date(m.group(0))
        if other and other != this_iso:
            cut = m.start()
            break
    if cut is None:
        return tables
    truncated = BeautifulSoup(html[:cut], "lxml")
    return truncated.find_all("table")


def parse_federal(manifesto: dict) -> list[dict]:
    out = []
    # current page
    rel = "dados/federal/invitation-rounds.html"
    meta = source_meta(manifesto, rel)
    soup = soup_file(ROOT / rel)
    data = hidden_json(soup)
    if not data or "content" not in data:
        err("invitation-rounds.html: campo JSON 'content' ausente")
    else:
        monthly_done = False
        for block in data["content"]:
            title = block.get("text") or ""
            inner = parse_federal_html_fragment(block.get("block") or "")
            tables = inner.find_all("table")
            if not tables:
                continue
            round_date = extract_round_date_from_html(inner, title) or "2026-06-04"
            py = infer_program_year(round_date)
            include_monthly = (not monthly_done) and any(looks_like_month_header(table_rows(t)[0]) for t in tables if table_rows(t))
            rows = classify_and_parse_federal_tables(tables, round_date, meta, py, include_monthly=True)
            if any(r["metrica"] == "eois_convidados" and "agregado_mensal=true" in (r["unidade_extra"] or "") for r in rows):
                monthly_done = True
            out.extend(rows)
            log(f"FEDERAL current '{title}': {len(rows)} linhas (data_round={round_date})")

    # previous rounds
    rel = "dados/federal/previous-rounds.html"
    meta = source_meta(manifesto, rel)
    soup = soup_file(ROOT / rel)
    data = hidden_json(soup)
    seen_monthly_years = set()
    if not data or "criteria" not in data:
        err("previous-rounds.html: campo JSON 'criteria' ausente")
        return out
    # current page already captured 2025-26 monthly
    seen_monthly_years.add("2025-26")
    for item in data["criteria"]:
        title = item.get("title") or ""
        inner = parse_federal_html_fragment(item.get("description") or "")
        round_date = extract_round_date_from_html(inner, title)
        if not round_date:
            round_date = parse_english_date(title)
        py = infer_program_year(round_date)
        tables = split_html_on_other_rounds(inner, title)
        include_monthly = py not in seen_monthly_years
        rows = classify_and_parse_federal_tables(tables, round_date, meta, py, include_monthly=include_monthly)
        if include_monthly and any("agregado_mensal=true" in (r["unidade_extra"] or "") for r in rows):
            seen_monthly_years.add(py)
        out.extend(rows)
        log(f"FEDERAL previous '{title}': {len(rows)} linhas (data_round={round_date})")
    return out


def parse_federal_state_totals(manifesto: dict) -> list[dict]:
    """Official federal cross-state nomination totals and annual allocations."""
    out = []
    state_map = {"ACT":"ACT", "NSW":"NSW", "NT":"NT", "QLD":"QLD", "Qld":"QLD",
                 "SA":"SA", "TAS":"TAS", "Tas":"TAS", "VIC":"VIC", "Vic":"VIC", "WA":"WA"}

    rel = "dados/federal/invitation-rounds.html"
    meta = source_meta(manifesto, rel)
    soup = soup_file(ROOT / rel)
    data = hidden_json(soup) or {}
    for block in data.get("content", []):
        if norm(block.get("text", "")).casefold() != "state and territory nominations":
            continue
        inner = parse_federal_html_fragment(block.get("block") or "")
        date_text = inner.get_text(" ", strip=True)
        date_tokens = re.findall(
            r"\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+20\d{2}\b",
            date_text, re.I,
        )
        cutoff = parse_english_date(date_tokens[-1]) if date_tokens else "2026-06-30"
        for table in inner.find_all("table"):
            rows = table_rows(table)
            if len(rows) < 3 or len(rows[0]) < 9:
                continue
            states = [state_map.get(norm(x), norm(x).upper()) for x in rows[0][1:]]
            for values in rows[1:]:
                visa = "190" if "190" in values[0] else "491" if "491" in values[0] else ""
                if not visa:
                    continue
                for state, value in zip(states, values[1:]):
                    cleaned = clean_value(value)
                    if cleaned is None:
                        continue
                    out.append(row(nivel="estadual", jurisdicao=state, visto=visa,
                        data_round=cutoff, ocupacao="agregado", anzsco="",
                        metrica="nomeacoes_recebidas", valor=cleaned,
                        unidade_extra="program_year=2025-26;cutoff=2026-06-30;federal_consolidated=true",
                        fonte_url=meta[0], arquivo_local=meta[1], sha256_fonte=meta[2]))

    rel = "dados/federal/state-and-territory-nomination-allocations.html"
    meta = source_meta(manifesto, rel)
    soup = soup_file(ROOT / rel)
    for table in soup.find_all("table"):
        rows = table_rows(table)
        if len(rows) < 9 or not any(norm(r[0]) == "ACT" for r in rows[1:] if r):
            continue
        for values in rows[1:]:
            state = state_map.get(norm(values[0]))
            if not state or len(values) < 3:
                continue
            for visa, value in (("190", values[1]), ("491", values[2])):
                cleaned = clean_value(value)
                if cleaned is None:
                    continue
                out.append(row(nivel="estadual", jurisdicao=state, visto=visa,
                    data_round="2025-26", ocupacao="agregado", anzsco="",
                    metrica="alocacao_nomeacoes", valor=cleaned,
                    unidade_extra="program_year=2025-26;federal_consolidated=true;allocation_not_grant=true",
                    fonte_url=meta[0], arquivo_local=meta[1], sha256_fonte=meta[2]))
        break
    log(f"FEDERAL state totals: {len(out)} linhas")
    return out

# ---------------------------------------------------------------------------
# ACT PDF
# ---------------------------------------------------------------------------

SCORE_RE = re.compile(r"^(N/A|NA|\d{2,3})$", re.I)
DATE_FRAG_RE = re.compile(r"^[\d()/]+$")


def pdf_words(page) -> list[tuple[float, float, str]]:
    words = []

    def visitor(text, cm, tm, fontDict, fontSize):
        t = (text or "").strip()
        if not t:
            return
        words.append((float(tm[5]), float(tm[4]), t))

    page.extract_text(visitor_text=visitor)
    return words


def parse_act_date_tokens(tokens: list[str]) -> str:
    blob = "".join(tokens)
    blob = blob.replace(" ", "")
    m = re.search(r"(\d{1,2})/(\d{1,2})/(20\d{2})", blob)
    if m:
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if 1 <= mo <= 12 and 1 <= d <= 31:
            return f"{y:04d}-{mo:02d}-{d:02d}"
    m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{2})", blob)
    if m:
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        y += 2000
        if 1 <= mo <= 12 and 1 <= d <= 31:
            return f"{y:04d}-{mo:02d}-{d:02d}"
    return ""


def merge_tokens_on_lines(words, y_tol=2.5, x_gap=14.0):
    """Group words into visual lines, then concatenate horizontally close fragments."""
    if not words:
        return []
    ordered = sorted(words, key=lambda w: (-w[0], w[1]))
    lines = []
    for y, x, t in ordered:
        if lines and abs(lines[-1][0] - y) <= y_tol:
            lines[-1][1].append((x, t))
        else:
            lines.append((y, [(x, t)]))
    merged = []
    for y, items in lines:
        items.sort()
        buf_x, buf = items[0][0], items[0][1]
        last_x = items[0][0]
        for x, t in items[1:]:
            if x - last_x <= x_gap:
                buf += t
                last_x = x
            else:
                merged.append((y, buf_x, buf))
                buf_x, buf, last_x = x, t, x
        merged.append((y, buf_x, buf))
    return merged


def parse_act(manifesto: dict) -> list[dict]:
    rel = "dados/estados/act/2025-26-Invitation-round-rankings.pdf"
    meta = source_meta(manifesto, rel)
    path = ROOT / rel
    reader = PdfReader(str(path))
    all_words = []
    for pi, page in enumerate(reader.pages):
        for y, x, t in pdf_words(page):
            all_words.append((pi, y, x, t))

    rounds = []
    for pi, y, x, t in all_words:
        if t.upper().startswith("ACT INVITATION ROUND"):
            same = [(x2, t2) for p2, y2, x2, t2 in all_words if p2 == pi and abs(y2 - y) < 4]
            same.sort()
            blob = " ".join(t2 for _, t2 in same)
            iso = parse_english_date(blob)
            rounds.append({"page": pi, "y": y, "iso": iso, "label": blob})
    rounds.sort(key=lambda r: (r["page"], -r["y"]))
    if not rounds:
        err("ACT PDF: nenhum ACT INVITATION ROUND encontrado")
        return []

    def round_index_for(pi, y):
        idx = 0
        for i, r in enumerate(rounds):
            if (pi, -y) >= (r["page"], -r["y"]):
                idx = i
        return idx

    col_xs = [None] * len(rounds)
    for i, r in enumerate(rounds):
        xs = []
        for pi, y, x, t in all_words:
            if round_index_for(pi, y) != i:
                continue
            if t in {"491", "190"} and x > 250 and r["page"] == pi and r["y"] >= y >= r["y"] - 130:
                xs.append(x)
        clustered = []
        for x in sorted(xs):
            if not clustered or abs(x - clustered[-1]) > 20:
                clustered.append(x)
        if len(clustered) >= 4:
            col_xs[i] = clustered[:4]
        else:
            col_xs[i] = [325.0, 381.0, 437.0, 493.0]
            err("ACT PDF: colunas do round %s instaveis; usando fallback" % r["label"])

    COL_META = [
        ("491", "applicant=canberra_resident"),
        ("190", "applicant=canberra_resident"),
        ("491", "applicant=overseas"),
        ("190", "applicant=overseas"),
    ]

    anchors = []
    for pi, y, x, t in all_words:
        if x < 130 and re.fullmatch(r"\d{4}", t) and t not in {"2025", "2026", "2024", "2023", "2027"}:
            ri = round_index_for(pi, y)
            anchors.append((ri, pi, y, x, t))

    windows = {}
    by_page = defaultdict(list)
    for a in anchors:
        by_page[a[1]].append(a)
    for pi, lst in by_page.items():
        lst.sort(key=lambda a: -a[2])
        for i, a in enumerate(lst):
            y = a[2]
            y_hi = (lst[i - 1][2] + y) / 2 if i else y + 22
            y_lo = (y + lst[i + 1][2]) / 2 if i + 1 < len(lst) else y - 22
            windows[(pi, y, a[4])] = (y_lo, y_hi)

    out = []
    per_round = defaultdict(int)
    header_noise = {
        "ANZSCO", "UNIT", "GROUP", "TITLE", "UNIT GROUP TITLE", "Canberra",
        "resident", "Overseas", "applicant", "Minimum", "Matrix", "score", "ranked",
    }

    for ri, pi, y, x, code in anchors:
        cols = col_xs[ri]
        y_lo, y_hi = windows.get((pi, y, code), (y - 16, y + 16))
        nearby_raw = [
            (y2, x2, t2)
            for p2, y2, x2, t2 in all_words
            if p2 == pi and y_lo < y2 < y_hi and round_index_for(p2, y2) == ri
        ]
        nearby = merge_tokens_on_lines(nearby_raw)

        def nearest_col(xv):
            dists = [(abs(xv - cx), j) for j, cx in enumerate(cols)]
            dists.sort()
            if dists[0][0] <= 50:
                return dists[0][1]
            return None

        title_parts = []
        col_scores = [[] for _ in cols]
        col_dates = [[] for _ in cols]
        score_left = min(cols) - 18

        for y2, x2, t2 in sorted(nearby, key=lambda z: (-z[0], z[1])):
            if x2 < 130 and re.fullmatch(r"\d{4}", t2):
                continue
            if t2 in header_noise:
                continue
            if x2 >= score_left:
                j = nearest_col(x2)
                if j is None:
                    continue
                compact = t2.replace(" ", "")
                if SCORE_RE.match(compact) or re.fullmatch(r"\d{2,3}", compact):
                    col_scores[j].append("N/A" if compact.upper() in {"N/A", "NA"} else compact)
                    continue
                if re.search(r"\d{1,2}/", compact) or DATE_FRAG_RE.match(compact) or "(" in compact or ")" in compact:
                    col_dates[j].append(compact)
                    continue
                continue
            if DATE_FRAG_RE.match(t2) or re.search(r"\d{1,2}/", t2):
                continue
            if SCORE_RE.match(t2):
                continue
            title_parts.append((y2, x2, t2))

        title_parts.sort(key=lambda z: (-z[0], z[1]))
        seen_t = []
        for _, _, t2 in title_parts:
            t2 = t2.strip()
            if not t2 or t2 in seen_t:
                continue
            if DATE_FRAG_RE.match(t2) or re.fullmatch(r"\d{1,2}/?", t2):
                continue
            up = t2.upper()
            if any(k in up for k in ("INVITATION ROUND", "MINIMUM MATRIX", "PLEASE NOTE", "SUBMISSIONS WERE", "UNIT GROUP")):
                continue
            if t2 in {"ACT", "Please", "note:", "note", "N/A", "considered.", "considered", "ranked"}:
                continue
            seen_t.append(t2)
        ocupacao = norm(" ".join(seen_t))
        ocupacao = re.sub(r"\s*-\s*", "-", ocupacao)
        ocupacao = re.sub(r"ACT INVITATION ROUND.*", "", ocupacao, flags=re.I).strip()
        ocupacao = re.sub(r"Please note:.*", "", ocupacao, flags=re.I).strip()
        ocupacao = re.sub(r"Minimum Matrix score ranked", "", ocupacao, flags=re.I).strip()
        ocupacao = re.sub(r"N/A = Matrix submissions were not considered\.?", "", ocupacao, flags=re.I).strip()
        ocupacao = re.sub(r"\bUnit group\b", "", ocupacao, flags=re.I).strip()
        ocupacao = re.sub(r"\s+\(\d{0,2}/?\s*$", "", ocupacao).strip()
        round_iso = rounds[ri]["iso"]
        for j, (visto, applicant) in enumerate(COL_META):
            if j >= len(col_scores):
                continue
            scores = col_scores[j]
            if not scores:
                continue
            valor = scores[0]
            tie = parse_act_date_tokens(col_dates[j]) if col_dates[j] else ""
            extras = [applicant]
            if tie:
                extras.append("tiebreak=%s" % tie)
            extras.append("unit_group=true")
            out.append(
                row(
                    nivel="estadual",
                    jurisdicao="ACT",
                    visto=visto,
                    data_round=round_iso,
                    ocupacao=ocupacao,
                    anzsco=code,
                    metrica="matrix_score",
                    valor=valor,
                    unidade_extra=extra_join(*extras),
                    **_meta_kw(meta),
                )
            )
            per_round[round_iso or rounds[ri]["label"]] += 1

    for k, n in per_round.items():
        log("ACT round %s: %s linhas matrix_score" % (k, n))

    # The official round page publishes aggregate invitations by pathway.
    # Sum the mutually exclusive pathway counts, keeping them separate from scores.
    summary_rel = "dados/estados/act/canberra-matrix-invitation-round.html"
    summary_meta = source_meta(manifesto, summary_rel)
    summary_text = norm(soup_file(ROOT / summary_rel).get_text(" ", strip=True))
    section = summary_text.split("2025-2026 Allocation", 1)[0]
    round_match = re.search(r"Canberra Matrix Invitation Round:\s*([^\.]+?20\d{2})", section, re.I)
    summary_date = parse_english_date(round_match.group(1)) if round_match else ""
    for visa in ("190", "491"):
        counts = [int(x) for x in re.findall(rf"{visa}\s+nominations:\s*(\d+)\s+invitation", section, re.I)]
        if summary_date and counts:
            out.append(row(
                nivel="estadual", jurisdicao="ACT", visto=visa,
                data_round=summary_date, ocupacao="agregado", anzsco="",
                metrica="convites_emitidos", valor=str(sum(counts)),
                unidade_extra=extra_join("round_total=true", "pathways_summed=true"),
                **_meta_kw(summary_meta),
            ))
            log(f"ACT round {summary_date}: {sum(counts)} convites subclass {visa}")
    return out


def parse_wa_pdf(manifesto: dict) -> list[dict]:
    sources = [
        ("dados/estados/wa/Last invited EOI by occupation - May 2023.pdf", "2023-05", "priority=published_round"),
        ("dados/estados/wa/Last invited EOI by occupation - August 2023.pdf", "2023-08", "priority=published_round"),
        ("dados/estados/wa/SNMP Invite Round - August 2024.pdf", "2024-08", "priority=published_round"),
        ("dados/estados/wa/SNMP Invite Round - September 2024.pdf", "2024-09", "priority=published_round"),
        ("dados/estados/wa/SNMP Invite Round - October 2024.pdf", "2024-10", "priority=published_round"),
        ("dados/estados/wa/SNMP Invite Round - December 2024.pdf", "2024-12", "priority=published_round"),
        ("dados/estados/wa/SNMP Invite Round - February 2025.pdf", "2025-02", "priority=published_round"),
        ("dados/estados/wa/SNMP Invite Round - March 2025 Non Priority.pdf", "2025-03", "priority=non_priority"),
        ("dados/estados/wa/SNMP Invite Round - Last Invited By Occupation May 2025.pdf", "2025-05", "priority=published_round"),
        ("dados/estados/wa/SNMP Invite Round - June 2025.pdf", "2025-06", "priority=published_round"),
        ("dados/estados/wa/SNMP - Priority Invite Round - October 2025.pdf", "2025-10", "priority=trades"),
        ("dados/estados/wa/SNMP Invite Round - December 2025.pdf", "2025-12", "priority=all_published"),
        ("dados/estados/wa/SNMP Invite Round - January 2026.pdf", "2026-01", "priority=trades"),
        ("dados/estados/wa/TRADE - SNMP Invite Round - Last Invited By Occupation - March 2026.pdf", "2026-03", "priority=trades"),
        ("dados/estados/wa/v.1OTHER priority occupations - SNMP Invite round - March 2026.pdf", "2026-03", "priority=other"),
        ("dados/estados/wa/Last invited expression of interest - Priority trade occupations - May 2026.pdf", "2026-05-20", "priority=trades"),
    ]
    # This PDF's text layer emits its Schedule 2 table before the Schedule 2
    # heading. Keep the historical Schedule 1 fallback for every other source.
    prefix_stream_overrides = {
        "dados/estados/wa/TRADE - SNMP Invite Round - Last Invited By Occupation - March 2026.pdf": "WASMOL2",
    }
    markers = [
        (r"General stream\s*[-–—]\s*WASMOL Schedule 1", "WASMOL1"),
        (r"General stream\s*[-–—]\s*WASMOL Schedule 2", "WASMOL2"),
        (r"Graduate stream\s*[-–—]\s*Higher Education", "graduate_he"),
        (r"Graduate stream\s*[-–—]\s*Vocational Education and Training", "graduate_vet"),
    ]
    out = []
    occ_re = re.compile(
        r"([A-Za-z][A-Za-z0-9 &'()/.,\-]+?)\s*\((\d{6})\)\s+"
        r"(WA|Western Australia|Overseas|Another Australian State or Territory)\s+"
        r"(\d{2,3})\s+(\d{1,2}/\d{1,2}/20\d{2})",
        re.I,
    )
    seen = set()
    for rel, round_date, priority in sources:
        meta = source_meta(manifesto, rel)
        reader = PdfReader(str(ROOT / rel))
        blob = "\n".join(page.extract_text() or "" for page in reader.pages)
        flat = re.sub(r"\s+", " ", blob)
        spans = []
        for pat, name in markers:
            spans.extend((m.start(), name) for m in re.finditer(pat, flat, re.I))
        spans.sort()
        if not spans:
            spans = [(0, "published_stream")]
        elif spans[0][0] > 0:
            # Some WA PDFs render the first WASMOL table before its heading in extracted text.
            # A verified per-document override handles the March 2026 PDF whose
            # prefix is Schedule 2; older documents retain the Schedule 1 rule.
            spans.insert(0, (0, prefix_stream_overrides.get(rel, "WASMOL1")))
        source_count = 0
        for i, (start, stream) in enumerate(spans):
            end = spans[i + 1][0] if i + 1 < len(spans) else len(flat)
            section = flat[start:end]
            for m in occ_re.finditer(section):
                occ, code, resid, pts, sub = m.group(1), m.group(2), norm(m.group(3)), m.group(4), m.group(5)
                # Headers and prose can precede the first occupation; retain only the final title fragment.
                occ = re.split(r"(?:Date|completed\.|round)\s+", occ, flags=re.I)[-1]
                occ = norm(occ)
                key = (round_date, stream, code, resid.lower(), pts, sub)
                if key in seen:
                    continue
                seen.add(key)
                resid_n = resid.replace("Western Australia", "WA")
                if resid_n.upper() in {"WA", "WESTERN AUSTRALIA"}:
                    resid_n = "WA"
                sub_iso = parse_numeric_date(sub)
                out.append(
                    row(
                        nivel="estadual", jurisdicao="WA", visto="n/a",
                        data_round=round_date, ocupacao=occ, anzsco=code,
                        metrica="ultimo_eoi_pontos", valor=pts,
                        unidade_extra=extra_join(
                            f"residence={resid_n}", f"stream={stream}",
                            f"eoi_submission_date={sub_iso or sub}", priority,
                        ),
                        **_meta_kw(meta),
                    )
                )
                source_count += 1
        log(f"WA PDF {Path(rel).name}: {source_count} linhas ultimo_eoi_pontos")
    log("WA PDFs last-invited: %s linhas" % len(out))
    log("WA PDFs: stream, residencia e data de submissao preservados; totais mensais permanecem em metrica separada.")
    if len(out) == 0:
        err("WA PDF: nenhuma ocupacao extraida")
    return out


def wa_stream_from_label(label: str) -> str:
    t = norm(label).lower()
    if "schedule 1" in t or "wasmol schedule 1" in t:
        return "WASMOL1"
    if "schedule 2" in t or "wasmol schedule 2" in t:
        return "WASMOL2"
    if "higher" in t:
        return "graduate_he"
    if "vocational" in t or "v ocational" in t or re.search(r"\bvet\b", t):
        return "graduate_vet"
    return ""


def parse_wa_html(manifesto: dict) -> list[dict]:
    rel = "dados/estados/wa/state-nominated-migration-program.html"
    meta = source_meta(manifesto, rel)
    soup = soup_file(ROOT / rel)
    tables = soup.find_all("table")
    out = []

    # Current May 2026 totals — table whose header has WASMOL schedule and visa subclass
    for table in tables:
        raw = table_rows(table)
        if len(raw) < 3:
            continue
        head = " ".join(raw[0]).lower()
        if "intending visa subclass" in head and "wasmol" in head:
            streams = []
            for c in raw[0][1:]:
                streams.append(wa_stream_from_label(c) or norm(c))
            for cells in raw[1:]:
                label = cells[0].lower()
                if "total" in label:
                    continue
                visto = visa_from_text(cells[0], federal=False)
                if visto == "n/a":
                    continue
                for i, val in enumerate(cells[1:], start=0):
                    cleaned = clean_value(val)
                    if cleaned is None:
                        continue
                    stream = streams[i] if i < len(streams) else ""
                    out.append(
                        row(
                            nivel="estadual",
                            jurisdicao="WA",
                            visto=visto,
                            data_round="2026-05-20",
                            ocupacao="agregado",
                            anzsco="",
                            metrica="convites_emitidos",
                            valor=cleaned,
                            unidade_extra=extra_join(
                                f"stream={stream}" if stream else "",
                                "round=current_may_2026_priority_trades",
                            ),
                            **_meta_kw(meta),
                        )
                    )

        # last invited profile tables (aggregate, not by occupation)
        if "eoi points" in head or (len(raw) > 1 and "eoi points" in " ".join(raw[1]).lower()):
            hdr = raw[1] if len(raw) > 1 and "visa subclass" in " ".join(raw[1]).lower() else raw[0]
            # identify columns
            hdr_l = [c.lower() for c in hdr]
            for cells in raw:
                if len(cells) < 4:
                    continue
                first = cells[0].lower()
                if "stream" in first and "visa" not in first:
                    continue
                if "trade occupations" in first or "occupations in" in first:
                    continue
                visto = None
                stream = wa_stream_from_label(cells[0])
                # find visa col
                for i, c in enumerate(cells):
                    if c.strip() in {"190", "491"}:
                        visto = c.strip()
                        rest_start = i + 1
                        break
                if not visto:
                    continue
                # remaining: residence, maybe qualification, points, date
                rest = cells[rest_start:] if "rest_start" in dir() else cells[2:]
                # skip dashes
                if all((clean_value(c) is None) for c in rest):
                    continue
                pts = None
                resid = ""
                sub = ""
                qual = ""
                for c in rest:
                    if re.fullmatch(r"\d{2,3}", (clean_value(c) or "")):
                        pts = clean_value(c)
                    elif re.search(r"\d{1,2}/\d{1,2}/20\d{2}", c):
                        sub = parse_numeric_date(c)
                    elif clean_value(c) and not re.fullmatch(r"\d+", clean_value(c) or ""):
                        if "australia" in c.lower() or c.upper() == "WA":
                            resid = "WA" if "western" in c.lower() or c.upper() == "WA" else norm(c)
                        elif c not in {"-", "–"}:
                            if not resid:
                                # qualification or residence
                                if any(q in c.lower() for q in ("bachelor", "certificate", "diploma", "phd", "master", "honours", "aqf")):
                                    qual = norm(c)
                                else:
                                    resid = norm(c)
                if pts is None:
                    continue
                out.append(
                    row(
                        nivel="estadual",
                        jurisdicao="WA",
                        visto=visto,
                        data_round="2026-05-20",
                        ocupacao="agregado",
                        anzsco="",
                        metrica="ultimo_eoi_pontos",
                        valor=pts,
                        unidade_extra=extra_join(
                            f"stream={stream}" if stream else "",
                            f"residence={resid}" if resid else "",
                            f"eoi_submission_date={sub}" if sub else "",
                            f"qualification={qual}" if qual else "",
                            "perfil_agregado=true",
                        ),
                        **_meta_kw(meta),
                    )
                )

        # program-year monthly invitation tables
        prev = table.find_previous(["h2", "h3", "h4", "h5", "p", "strong"])
        prev_t = prev.get_text(" ", strip=True) if prev else ""
        if looks_like_month_header(raw[0]) and (
            "invitation" in (prev_t + " ".join(raw[0])).lower()
            or re.search(r"20\d{2}\s*[\u2013\u2014-]\s*\d{2}", prev_t)
        ):
            py = ""
            mpy = re.search(r"(20\d{2})\s*[\u2013\u2014-]\s*(\d{2})", prev_t)
            if mpy:
                py = f"{mpy.group(1)}-{mpy.group(2)}"
            elif "2025" in prev_t and "26" in prev_t:
                py = "2025-26"
            elif "2024" in prev_t and "25" in prev_t:
                py = "2024-25"
            elif "2023" in prev_t and "24" in prev_t:
                py = "2023-24"
            headers = raw[0]
            current_stream = ""
            for cells in raw[1:]:
                label = cells[0]
                sl = wa_stream_from_label(label)
                if sl and not re.fullmatch(r"190|491", label.strip()):
                    current_stream = sl
                    continue
                if label.lower().startswith("total"):
                    continue
                visto = visa_from_text(label, federal=False)
                if visto not in {"190", "491"}:
                    continue
                for i, val in enumerate(cells[1:], start=1):
                    h = headers[i] if i < len(headers) else ""
                    if "total" in h.lower():
                        continue
                    cleaned = clean_value(val)
                    if cleaned is None or cleaned == "0":
                        continue
                    month_iso = program_year_month(h, py)
                    if not month_iso:
                        continue
                    out.append(
                        row(
                            nivel="estadual",
                            jurisdicao="WA",
                            visto=visto,
                            data_round=month_iso,
                            ocupacao="agregado",
                            anzsco="",
                            metrica="convites_emitidos",
                            valor=cleaned,
                            unidade_extra=extra_join(
                                f"stream={current_stream}" if current_stream else "",
                                f"programa={py}" if py else "",
                                "agregado_mensal=true",
                            ),
                            **_meta_kw(meta),
                        )
                    )
    log(f"WA HTML: {len(out)} linhas")
    return out

# ---------------------------------------------------------------------------
# SA
# ---------------------------------------------------------------------------

SA_FILES = [
    ("dados/estados/sa/invitations-issued-late-may-2026.html", "2026-05-21"),
    ("dados/estados/sa/invitations-issued-may-2026.html", "2026-05"),
    ("dados/estados/sa/invitations-issued-april-2026.html", "2026-04"),
    ("dados/estados/sa/invitations-issued-march-2026.html", "2026-03"),
    ("dados/estados/sa/invitations-issued-feb-2026.html", "2026-02"),
    ("dados/estados/sa/invitations-issued-jan-2026.html", "2026-01"),
    ("dados/estados/sa/invitations-issued-dec-2025.html", "2025-12"),
]


def parse_sa_group_name(label: str) -> tuple[str, str]:
    m = re.match(r"^(\d{2})\s+(.*)$", norm(label))
    if m:
        return m.group(2), m.group(1)
    if norm(label).lower() == "total":
        return "agregado", ""
    return norm(label), ""


def parse_sa(manifesto: dict) -> list[dict]:
    out = []
    for rel, default_date in SA_FILES:
        meta = source_meta(manifesto, rel)
        soup = soup_file(ROOT / rel)
        tables = soup.find_all("table")
        if not tables:
            err(f"SA {rel}: nenhuma tabela")
            continue
        table = tables[0]
        raw = table_rows(table)
        if len(raw) < 3:
            err(f"SA {rel}: tabela curta ({len(raw)} linhas)")
            continue
        # row 0: group labels spanning 3 cols each (plus leading empty)
        # row 1: ANZSCO / 190 / 491 / Total / 190 / 491 / Total
        top = raw[0]
        # Determine column groups from top header. Each non-empty top cell covers 3 metric cols.
        # After expand_row, colspan is already expanded so top may be like
        # ['', 'Invitations in April 2026', 'Invitations in April 2026', 'Invitations in April 2026',
        #  '2025-26 invitations issued (to date)', ...]
        groups = []  # (start_idx, label, iso_date, is_ytd)
        i = 1
        while i < len(top):
            label = top[i]
            if not label:
                i += 1
                continue
            # span length
            j = i
            while j < len(top) and top[j] == label:
                j += 1
            is_ytd = "to date" in label.lower() or "2025-26 invitations issued" in label.lower()
            is_interim = "interim" in label.lower()
            iso = parse_english_date(label) or ""
            if not iso:
                if "december 2025" in label.lower() or "in december" in label.lower():
                    iso = "2025-12"
                elif is_interim and "november 2025" in label.lower():
                    iso = "2025-11-01"
                else:
                    iso = default_date if not is_ytd else "2025-26"
            groups.append((i, label, iso, is_ytd, is_interim, j - i))
            i = j

        header1 = raw[1]
        n_added = 0
        for cells in raw[2:]:
            if not cells:
                continue
            occ, anzsco = parse_sa_group_name(cells[0])
            for start, glabel, iso, is_ytd, is_interim, width in groups:
                # skip YTD except we only want monthly/round counts
                if is_ytd:
                    continue
                # map 190 / 491 within the group using header1
                for k in range(width):
                    idx = start + k
                    if idx >= len(cells) or idx >= len(header1):
                        continue
                    h = header1[idx].lower()
                    if "190" in h:
                        visto = "190"
                    elif "491" in h:
                        visto = "491"
                    else:
                        continue  # skip group Total column
                    cleaned = clean_value(cells[idx])
                    if cleaned is None:
                        continue
                    extras = ["anzsco_submajor=true"]
                    if is_interim:
                        extras.append("periodo=interim_to_1_nov_2025")
                    extras.append(f"coluna={norm(glabel)}")
                    out.append(
                        row(
                            nivel="estadual",
                            jurisdicao="SA",
                            visto=visto,
                            data_round=iso,
                            ocupacao=occ,
                            anzsco=anzsco,
                            metrica="convites_emitidos",
                            valor=cleaned,
                            unidade_extra=extra_join(*extras),
                            **_meta_kw(meta),
                        )
                    )
                    n_added += 1
        log(f"SA {Path(rel).name}: {n_added} linhas")
    return out


# ---------------------------------------------------------------------------
# NSW / VIC / QLD / TAS / NT
# ---------------------------------------------------------------------------

GAP_PAGES = [
    (
        "NSW",
        "dados/estados/nsw/skilled-nominated-visa-subclass-190.html",
        "n/a",
        True,
        [],
    ),
    (
        "VIC",
        "dados/estados/vic/registration-of-interest.html",
        "n/a",
        True,
        [],
    ),
    (
        "QLD",
        "dados/estados/qld/registering-your-interest.html",
        "n/a",
        True,
        [],
    ),
    (
        "NT",
        "dados/estados/nt/overseas-workers-and-your-business.html",
        "n/a",
        True,
        [],
    ),
]


def parse_gaps_and_tas(manifesto: dict) -> list[dict]:
    out = []
    for juris, rel, visto, published_ok, _ in GAP_PAGES:
        meta = source_meta(manifesto, rel)
        out.append(
            row(
                nivel="estadual",
                jurisdicao=juris,
                visto=visto,
                data_round="",
                ocupacao="",
                anzsco="",
                metrica="publicacao",
                valor="NOT_PUBLISHED",
                unidade_extra="invitation_by_occupation=not_published",
                validado=published_ok,
                **_meta_kw(meta),
            )
        )
        log(f"{juris}: 1 linha publicacao=NOT_PUBLISHED")

    # TAS: gap + official totals
    rel = "dados/estados/tas/processing-times-and-allocation-usage.html"
    meta = source_meta(manifesto, rel)
    out.append(
        row(
            nivel="estadual",
            jurisdicao="TAS",
            visto="n/a",
            data_round="2025-26",
            ocupacao="",
            anzsco="",
            metrica="publicacao",
            valor="NOT_PUBLISHED",
            unidade_extra="invitation_by_occupation=not_published",
            **_meta_kw(meta),
        )
    )
    soup = soup_file(ROOT / rel)
    text = soup.get_text(" ", strip=True)
    # Do not classify Tasmania's fully delivered nominations as invitations.
    # The same 2025-26 nomination totals are already present in the federal table.

    log("TAS: 1 NOT_PUBLISHED; totais 2025-26 nao duplicados como convites")
    return out


# ---------------------------------------------------------------------------
# assemble / write
# ---------------------------------------------------------------------------

def dedupe_key(r: dict) -> tuple:
    return (
        r["jurisdicao"],
        r["visto"],
        r["data_round"],
        r["ocupacao"],
        r["anzsco"],
        r["metrica"],
        r["valor"],
        r["unidade_extra"],
        r["arquivo_local"],
    )


def write_outputs(rows: list[dict]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUT_DIR / "vistos-de-convites.csv"
    json_path = OUT_DIR / "vistos-de-convites.json"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
        f.write("\n")
    data_js = ROOT / "analise" / "data.js"
    data_js.write_text(
        "window.CONVITES_DATA = " + json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    log(f"CSV escrito: {csv_path} ({len(rows)} linhas)")
    log(f"JSON escrito: {json_path}")
    log(f"Dashboard escrito: {data_js}")


def write_log(n_by_j: dict, n_total: int) -> None:
    lines = []
    lines.append("# Log de extracao - vistos de convite")
    lines.append("")
    lines.append(f"Gerado em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")
    lines.append("")
    lines.append("Somente fontes oficiais `.gov.au` ja baixadas em `dados/` foram usadas.")
    lines.append("Nenhum download de sites nao-governamentais. Nenhum numero extraoficial.")
    lines.append("")
    lines.append("## Linhas por jurisdicao")
    lines.append("")
    lines.append("| Jurisdicao | Linhas |")
    lines.append("|---|---|")
    for j in ["FEDERAL", "ACT", "WA", "SA", "NSW", "VIC", "QLD", "TAS", "NT"]:
        lines.append(f"| {j} | {n_by_j.get(j, 0)} |")
    lines.append(f"| **Total** | **{n_total}** |")
    lines.append("")
    lines.append("## Notas de parse")
    lines.append("")
    for msg in LOG:
        lines.append(f"- {msg}")
    lines.append("")
    lines.append("## Erros / avisos")
    lines.append("")
    if ERRORS:
        for msg in ERRORS:
            lines.append(f"- {msg}")
    else:
        lines.append("- Nenhum erro de parse bloqueante.")
    lines.append("")
    lines.append("## Regras aplicadas")
    lines.append("")
    lines.append("- Federal: JSON oculto `#ctl00_PlaceHolderMain_PageSchemaHiddenField_Input` em invitation-rounds e previous-rounds.")
    lines.append("- ACT: PDF 2025-26 Invitation round rankings (scores de matrix por unit group ANZSCO).")
    lines.append("- WA: PDFs oficiais de last-invited por ocupacao entre maio de 2025 e maio de 2026; subclass 190/491 permanece `n/a` quando o PDF nao a identifica. Totais SNMP continuam em metricas separadas.")
    lines.append("- SA: HTML invitations-issued por mes (contagens por sub-major group 190/491). Colunas year-to-date nao foram repetidas.")
    lines.append("- NSW/VIC/QLD/NT: `metrica=publicacao`, `valor=NOT_PUBLISHED` (pagina oficial existe, sem resultados por ocupacao).")
    lines.append("- TAS: NOT_PUBLISHED por ocupacao; nominações entregues nao sao classificadas como convites.")
    lines.append("- Celulas vazias / '-' foram omitidas; `N/A` e `Not invited` gravados como `N/A`.")
    (OUT_DIR / "extracao-log.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    manifesto = load_manifesto()
    rows: list[dict] = []
    rows.extend(parse_federal(manifesto))
    rows.extend(parse_federal_state_totals(manifesto))
    rows.extend(parse_act(manifesto))
    rows.extend(parse_wa_pdf(manifesto))
    rows.extend(parse_wa_html(manifesto))
    rows.extend(parse_sa(manifesto))
    rows.extend(parse_gaps_and_tas(manifesto))

    enrichment = enrich_occupations(rows)
    log(
        "Normalizacao ANZSCO 2022 (ABS): "
        + ", ".join(f"{k}={v}" for k, v in sorted(enrichment.items()))
    )

    # light dedupe of exact duplicates
    seen = set()
    unique = []
    n_dup = 0
    for r in rows:
        k = dedupe_key(r)
        if k in seen:
            n_dup += 1
            continue
        seen.add(k)
        unique.append(r)
    if n_dup:
        log(f"Duplicatas exatas removidas: {n_dup}")
    rows = unique

    n_by_j = defaultdict(int)
    for r in rows:
        n_by_j[r["jurisdicao"]] += 1
        COUNTS[r["jurisdicao"]] += 1

    write_outputs(rows)
    write_log(n_by_j, len(rows))

    print("=== LINHAS POR JURISDICAO ===")
    for j in ["FEDERAL", "ACT", "WA", "SA", "NSW", "VIC", "QLD", "TAS", "NT"]:
        print(f"{j}: {n_by_j.get(j, 0)}")
    print(f"TOTAL: {len(rows)}")
    if ERRORS:
        print("=== ERROS ===")
        for e in ERRORS:
            print(e)


if __name__ == "__main__":
    main()
