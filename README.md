# Australia invitation visas

Live dashboard: https://jfilhorv.github.io/Invitation_aus_visas/

Sources: **official `.gov.au` sites only**.  
One current document per government; extra files only when the government published a new version (round / program year changed).

## Analysis page

Open `analise/index.html` in a browser (loads `analise/data.js` generated from JSON).

Filters: state, visa, category, occupation, metric. Stacked table: date · state · visa · occupation · score.

## Aggregated dataset

- `dados/agregado/vistos-de-convites.csv`
- `dados/agregado/vistos-de-convites.json`
- `analise/data.js` (same content for the page)

Category: `visto_de_convite`. Each row has `fonte_url`, `sha256_fonte`, and `validado`.

Occupation identity is normalized conservatively against the official ABS ANZSCO 2022 structure and index. The dashboard keeps occupation levels, metrics and onshore/offshore series separate. See `dados/agregado/metodologia.md`.

## Validation

`dados/fontes/manifesto-validacao.csv`

Criteria: HTTP 200, final host `.gov.au`, PDF starts with `%PDF` (or official HTML), SHA256.

Inventory: `dados/fontes/inventario-oficial.md`

## What governments publish today

| Government | Current document | By occupation? | History on official site |
|---|---|---|---|
| Federal (Home Affairs) | HTML SkillSelect invitation rounds | Yes (189 / 491 family) | `previous-rounds` (2020–2026) |
| ACT | 1 PDF: 2025-26 Invitation round rankings | Yes (ANZSCO unit group) | Current program year only |
| WA | 1 PDF: last invited EOI (May 2026) | Yes (current trades) | HTML totals 2023-24 and 2024-25 |
| SA | HTML “Invitations issued” | By ANZSCO sub-major group | Dec 2025–May 2026 in index |
| NSW, VIC, QLD, NT | Do not publish results | No | — |
| TAS | 190/491 totals only | No | — |

No blogs, migration agents, archive.org, or non-`.gov.au` sites were used.
