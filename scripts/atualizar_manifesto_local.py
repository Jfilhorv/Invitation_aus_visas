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
    if item["arquivo_local"].startswith("dados/estados/wa/"):
        item["jurisdicao"] = "WA"
    if local.is_file():
        item["sha256"] = digest(local)
        item["content_length"] = str(local.stat().st_size)

official_abs = [
    (
        "WA Migration Services invitation results",
        "https://migration.wa.gov.au/sites/default/files/2025-05/SNMP%20Invite%20Round%20-%20Last%20Invited%20By%20Occupation%20May%202025.pdf",
        "dados/estados/wa/SNMP Invite Round - Last Invited By Occupation May 2025.pdf",
        "Resultados oficiais por ocupacao do round de maio de 2025.",
    ),
    (
        "WA Migration Services invitation results",
        "https://migration.wa.gov.au/sites/default/files/2025-10/SNMP%20-%20Priority%20Invite%20Round%20-%20October%202025.pdf",
        "dados/estados/wa/SNMP - Priority Invite Round - October 2025.pdf",
        "Resultados oficiais por ocupacao do round de outubro de 2025.",
    ),
    (
        "WA Migration Services invitation results",
        "https://migration.wa.gov.au/sites/default/files/2025-12/SNMP%20Invite%20Round%20-%20December%202025.pdf",
        "dados/estados/wa/SNMP Invite Round - December 2025.pdf",
        "Resultados oficiais por ocupacao do round de dezembro de 2025.",
    ),
    (
        "WA Migration Services invitation results",
        "https://migration.wa.gov.au/sites/default/files/2026-01/SNMP%20Invite%20Round%20-%20January%202026.pdf",
        "dados/estados/wa/SNMP Invite Round - January 2026.pdf",
        "Resultados oficiais por ocupacao do round de janeiro de 2026.",
    ),
    (
        "WA Migration Services invitation results",
        "https://migration.wa.gov.au/sites/default/files/2026-03/TRADE%20-%20SNMP%20Invite%20Round%20-%20Last%20Invited%20By%20Occupation%20-%20March%202026.pdf",
        "dados/estados/wa/TRADE - SNMP Invite Round - Last Invited By Occupation - March 2026.pdf",
        "Resultados oficiais de trades prioritarias do round de marco de 2026; arquivo preservado no dominio oficial embora nao esteja ligado na pagina atual do programa.",
    ),
    (
        "WA Migration Services invitation results",
        "https://migration.wa.gov.au/sites/default/files/2026-03/v.1OTHER%20priority%20occupations%20-%20SNMP%20Invite%20round%20-%20March%202026.pdf",
        "dados/estados/wa/v.1OTHER priority occupations - SNMP Invite round - March 2026.pdf",
        "Resultados oficiais de outras ocupacoes prioritarias do round de marco de 2026.",
    ),
    (
        "Home Affairs state nomination allocations",
        "https://immi.homeaffairs.gov.au/what-we-do/state-and-territory-nomination-allocations",
        "dados/federal/state-and-territory-nomination-allocations.html",
        "Alocacoes oficiais 190/491 por estado; limites anuais, nao vistos concedidos.",
    ),
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
        "jurisdicao": "WA" if rel.startswith("dados/estados/wa/") else "federal",
        "url": url,
        "arquivo_local": rel,
        "status_http": "200",
        "content_type": "text/html; charset=utf-8" if rel.endswith(".html") else "application/pdf" if rel.endswith(".pdf") else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
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
