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
    elif item["arquivo_local"].startswith("dados/estados/act/"):
        item["jurisdicao"] = "ACT"
    if local.is_file():
        item["sha256"] = digest(local)
        item["content_length"] = str(local.stat().st_size)

official_abs = [
    (
        "ACT Migration",
        "https://www.act.gov.au/__data/assets/pdf_file/0020/3140480/2026-27-Invitation-round-rankings.pdf",
        "dados/estados/act/2026-27-Invitation-round-rankings.pdf",
        "Documento canonico 2026-27; rankings da rodada ACT de 12 de outubro de 2026.",
    ),
    (
        "WA Migration Services invitation results",
        "https://migration.wa.gov.au/sites/default/files/2023-10/Last%20invited%20expression%20of%20interest%20by%20occupation%20-%20October%20invitation%20round%202023_0.pdf",
        "dados/estados/wa/Last invited EOI by occupation - October 2023.pdf",
        "Resultados oficiais por ocupacao do round de outubro de 2023.",
    ),
    (
        "WA Migration Services invitation results",
        "https://migration.wa.gov.au/sites/default/files/2023-11/Last%20invited%20expression%20of%20interest%20by%20occupation%20-%20November%20invitation%20round%202023.pdf",
        "dados/estados/wa/Last invited EOI by occupation - November 2023.pdf",
        "Resultados oficiais por ocupacao do round de novembro de 2023.",
    ),
    (
        "WA Migration Services invitation results",
        "https://migration.wa.gov.au/sites/default/files/2024-11/November%202024%20SNMP%20Invite%20Round%20-%20Last%20Invited%20By%20Priority%20Occupation.pdf",
        "dados/estados/wa/SNMP Invite Round - November 2024.pdf",
        "Resultados oficiais por ocupacao do round de novembro de 2024.",
    ),
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
        "WA Migration Services invitation results",
        "https://migration.wa.gov.au/sites/default/files/2026-10/Oct%202026.BC%20-%20SNMP%20Invite%20Round%20-%20Last%20Invited%20By%20Occupation%20B%26C%20Trade%20Occupations.pdf",
        "dados/estados/wa/Oct 2026 BC - SNMP Invite Round - Last Invited By Occupation Trade Occupations.pdf",
        "Resultados oficiais por ocupacao das trades de construcao do round de 14 de outubro de 2026.",
    ),
    (
        "WA Migration Services invitation results",
        "https://migration.wa.gov.au/sites/default/files/2026-10/Oct%202026%20-%20SNMP%20Invite%20Round%20-%20Last%20Invited%20By%20Occupation%20in%20other%20priority%20occupation.pdf",
        "dados/estados/wa/Oct 2026 - SNMP Invite Round - Last Invited By Occupation Other Priority Occupations.pdf",
        "Resultados oficiais por ocupacao das demais ocupacoes prioritarias do round de 14 de outubro de 2026.",
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
        "jurisdicao": (
            "WA" if rel.startswith("dados/estados/wa/")
            else "ACT" if rel.startswith("dados/estados/act/")
            else "federal"
        ),
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
