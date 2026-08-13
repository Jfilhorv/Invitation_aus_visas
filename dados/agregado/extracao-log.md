# Log de extracao - vistos de convite

Gerado em 2026-08-12 21:30:54.

Somente fontes oficiais `.gov.au` ja baixadas em `dados/` foram usadas.
Nenhum download de sites nao-governamentais. Nenhum numero extraoficial.

## Linhas por jurisdicao

| Jurisdicao | Linhas |
|---|---|
| FEDERAL | 3509 |
| ACT | 2706 |
| WA | 143 |
| SA | 272 |
| NSW | 1 |
| VIC | 1 |
| QLD | 1 |
| TAS | 3 |
| NT | 1 |
| **Total** | **6637** |

## Notas de parse

- FEDERAL current 'Current round': 146 linhas (data_round=2026-06-04)
- FEDERAL current 'State and Territory nominations': 0 linhas (data_round=2026-06-04)
- FEDERAL previous '13 November 2025': 290 linhas (data_round=2025-11-13)
- FEDERAL previous '21 August 2025': 264 linhas (data_round=2025-08-21)
- FEDERAL previous '7 November 2024': 165 linhas (data_round=2024-11-07)
- FEDERAL previous '5 September 2024': 151 linhas (data_round=2024-09-05)
- FEDERAL previous '13 June 2024': 140 linhas (data_round=2024-06-13)
- FEDERAL previous '18 December 2023': 118 linhas (data_round=2023-12-18)
- FEDERAL previous '25 May 2023': 240 linhas (data_round=2023-05-25)
- FEDERAL previous '8 December 2022': 747 linhas (data_round=2022-12-08)
- FEDERAL previous '6 October 2022': 416 linhas (data_round=2022-10-06)
- FEDERAL previous '22 August 2022': 464 linhas (data_round=2022-08-22)
- FEDERAL previous '21 April 2022': 138 linhas (data_round=2022-04-21)
- FEDERAL previous '21 January 2022': 127 linhas (data_round=2022-01-21)
- FEDERAL previous '29 October 2021': 14 linhas (data_round=2021-10-29)
- FEDERAL previous '26 July 2021': 14 linhas (data_round=2021-07-26)
- FEDERAL previous '21 April 2021': 26 linhas (data_round=2021-04-21)
- FEDERAL previous '21 January 2021': 13 linhas (data_round=2021-01-21)
- FEDERAL previous '21 October 2020': 12 linhas (data_round=2020-10-21)
- FEDERAL previous '11 September 2020': 12 linhas (data_round=2020-09-11)
- FEDERAL previous '11 August 2020': 12 linhas (data_round=2020-08-11)
- ACT round 2026-06-11: 420 linhas matrix_score
- ACT round 2026-05-06: 420 linhas matrix_score
- ACT round 2026-03-12: 420 linhas matrix_score
- ACT round 2026-01-29: 420 linhas matrix_score
- ACT round 2025-12-10: 418 linhas matrix_score
- ACT round 2025-09-15: 608 linhas matrix_score
- WA PDF last-invited: 18 linhas
- WA PDF: stream atribuido pelo cabecalho de secao do PDF (WASMOL1/2/graduate). O HTML do round 20 May 2026 publica WASMOL1=0 e convites em WASMOL2/graduate; pontos/ANZSCO/datas seguem o PDF oficial.
- WA HTML: 125 linhas
- SA invitations-issued-late-may-2026.html: 36 linhas
- SA invitations-issued-may-2026.html: 36 linhas
- SA invitations-issued-april-2026.html: 34 linhas
- SA invitations-issued-march-2026.html: 34 linhas
- SA invitations-issued-feb-2026.html: 34 linhas
- SA invitations-issued-jan-2026.html: 34 linhas
- SA invitations-issued-dec-2025.html: 64 linhas
- NSW: 1 linha publicacao=NOT_PUBLISHED
- VIC: 1 linha publicacao=NOT_PUBLISHED
- QLD: 1 linha publicacao=NOT_PUBLISHED
- NT: 1 linha publicacao=NOT_PUBLISHED
- TAS: 2 totais + 1 NOT_PUBLISHED
- Normalizacao ANZSCO 2022 (ABS): abs_exact_title=3215, missing=379, source=3043
- CSV escrito: C:\Users\efilh\Invitation_aus_visa\dados\agregado\vistos-de-convites.csv (6637 linhas)
- JSON escrito: C:\Users\efilh\Invitation_aus_visa\dados\agregado\vistos-de-convites.json
- Dashboard escrito: C:\Users\efilh\Invitation_aus_visa\analise\data.js

## Erros / avisos

- Nenhum erro de parse bloqueante.

## Regras aplicadas

- Federal: JSON oculto `#ctl00_PlaceHolderMain_PageSchemaHiddenField_Input` em invitation-rounds e previous-rounds.
- ACT: PDF 2025-26 Invitation round rankings (scores de matrix por unit group ANZSCO).
- WA: PDF last-invited May 2026 + tabelas HTML SNMP (totais do round corrente e mensais 2025-26 / 2024-25 / 2023-24).
- SA: HTML invitations-issued por mes (contagens por sub-major group 190/491). Colunas year-to-date nao foram repetidas.
- NSW/VIC/QLD/NT: `metrica=publicacao`, `valor=NOT_PUBLISHED` (pagina oficial existe, sem resultados por ocupacao).
- TAS: NOT_PUBLISHED por ocupacao + totais oficiais 190/491 do programa 2025-26.
- Celulas vazias / '-' foram omitidas; `N/A` e `Not invited` gravados como `N/A`.
