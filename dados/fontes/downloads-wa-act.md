# WA and ACT invitation-round PDF downloads

Downloaded from official Western Australian and ACT government sites on 12 August 2026.
Each file was checked to start with `%PDF` and to be larger than 1 KB (HTML error pages were discarded).

## Western Australia (`dados/estados/wa/`)

| Filename | Bytes | Source URL | Date (from filename) |
|---|---:|---|---|
| SNMP Invite Round - December 2025.pdf | 268466 | https://migration.wa.gov.au/sites/default/files/2025-12/SNMP%20Invite%20Round%20-%20December%202025.pdf | December 2025 |
| SNMP Invite Round - January 2026.pdf | 245612 | https://migration.wa.gov.au/sites/default/files/2026-01/SNMP%20Invite%20Round%20-%20January%202026.pdf | January 2026 |
| SNMP - Priority Invite Round - October 2025.pdf | 237282 | https://migration.wa.gov.au/sites/default/files/2025-10/SNMP%20-%20Priority%20Invite%20Round%20-%20October%202025.pdf | October 2025 |
| SNMP Invite Round - Last Invited By Occupation May 2025.pdf | 165561 | https://migration.wa.gov.au/sites/default/files/2025-05/SNMP%20Invite%20Round%20-%20Last%20Invited%20By%20Occupation%20May%202025.pdf | May 2025 |
| TRADE - SNMP Invite Round - Last Invited By Occupation - March 2026.pdf | 497074 | https://migration.wa.gov.au/sites/default/files/2026-03/TRADE%20-%20SNMP%20Invite%20Round%20-%20Last%20Invited%20By%20Occupation%20-%20March%202026.pdf | March 2026 |
| v.1OTHER priority occupations - SNMP Invite round - March 2026.pdf | 528562 | https://migration.wa.gov.au/sites/default/files/2026-03/v.1OTHER%20priority%20occupations%20-%20SNMP%20Invite%20round%20-%20March%202026.pdf | March 2026 |
| Last invited expression of interest - Priority trade occupations - May 2026.pdf | 328515 | https://migration.wa.gov.au/sites/default/files/2026-05/Last%20invited%20expression%20of%20interest%20-%20Priority%20trade%20occupations%20-%20May%202026.pdf | May 2026 |
| 2025-26 WA SNMP Criteria - July 2025.pdf | 488031 | https://migration.wa.gov.au/sites/default/files/2026-05/2025-26%20WA%20SNMP%20Criteria%20-%20July%202025.pdf | July 2025 (program year 2025-26) |

## Australian Capital Territory (`dados/estados/act/`)

| Filename | Bytes | Source URL | Date (from filename) |
|---|---:|---|---|
| 2025-26-Invitation-round-rankings.pdf | 776507 | https://www.act.gov.au/__data/assets/pdf_file/0009/2920554/2025-26-Invitation-round-rankings.pdf | 2025-26 (rounds through June 2026) |

## Discovery notes

### WA pages fetched

- https://migration.wa.gov.au/our-services-support/state-nominated-migration-program (200)
- https://migration.wa.gov.au/sites/default/files/ (404 — no directory listing)
- News: December 2025 invitation round, 2025-26 invitations, 2025-26 program, 2024-25 program (200, no extra PDF hrefs)

Invite/SNMP/occupation PDFs found on the SNMP page (beyond the original five):

- `Last invited expression of interest - Priority trade occupations - May 2026.pdf` (downloaded)
- `PDF.SNMP - Decision review request_0.pdf` (form — not downloaded)
- `PDF.SNMP - payslip template.pdf` (template — not downloaded)
- `ms-payslip-template.pdf` (template — not downloaded)

Monthly URL probe (Jan–Dec 2021–2026, common Invite/TRADE/OTHER/Priority/WASMOL names): **744 candidates**, **6 live PDFs**. Extra hit not in the original list:

- January 2026 `SNMP Invite Round - January 2026.pdf` (downloaded)

Alternate 2024-25 naming (`SNMP Invite Round - Last Invited By Occupation Month YYYY.pdf`): **1 live PDF** (May 2025, downloaded). Other months 2023–2026 returned 404.

### ACT pages fetched

- https://www.act.gov.au/migration/skilled-migrants (200, no PDF hrefs)
- https://www.act.gov.au/migration (200, no PDF hrefs)
- https://www.act.gov.au/migration/resources/canberra-matrix-invitation-round (200; points to library `#invitation-ranking`)
- https://www.act.gov.au/migration/resources/library-guidelines-and-invitations (200; only **2025-26** invitation rankings PDF is published)
- https://www.act.gov.au/migration/resources and `/attachments` (200)

Historical CDN guesses for 2021-22 / 2022-23 / 2023-24 / 2024-25 invitation rankings under `/__data/assets/pdf_file/` all returned **404**. The official library currently lists only the 2025-26 rankings file.

### PDFs discovered but not downloaded (not invitation-round data)

WA:

- https://migration.wa.gov.au/sites/default/files/2026-05/PDF.SNMP%20-%20Decision%20review%20request_0.pdf
- https://migration.wa.gov.au/sites/default/files/2026-05/PDF.SNMP%20-%20payslip%20template.pdf
- https://migration.wa.gov.au/sites/default/files/2025-03/ms-payslip-template.pdf
- https://immi.homeaffairs.gov.au/form-listing/forms/956.pdf (federal form 956)

ACT (guidelines / attachments / occupation list, not invitation rankings):

- https://www.act.gov.au/__data/assets/pdf_file/0011/3105839/Document-13.2-ACT-nomination-guidelines-July-2026-Canberra-resident.pdf
- https://www.act.gov.au/__data/assets/pdf_file/0004/3105841/Document-13.4-ACT-nomination-guidelines-July-2026-Overseas-applicant.pdf
- https://www.act.gov.au/__data/assets/pdf_file/0005/2931395/ACT-Nominated-Migration-Program-Occupation-List.pdf
- https://www.act.gov.au/__data/assets/pdf_file/0005/3106229/ACT-Migration-Application-Portal-Guide-to-Account-Creation.pdf
- https://www.act.gov.au/__data/assets/pdf_file/0004/1835689/ACT-188-nomination-guidelines.pdf
- https://www.act.gov.au/__data/assets/pdf_file/0006/1769541/Attachment-A-Nomination-Obligations-to-the-Australian-Capital-Territory.pdf
- https://www.act.gov.au/__data/assets/pdf_file/0007/1769542/Attachment-B-Financial-Declaration-overseas-applicants-only.pdf
- https://www.act.gov.au/__data/assets/pdf_file/0012/1769547/Attachment-C-Summary-of-Working-Hours.pdf
- https://www.act.gov.au/__data/assets/pdf_file/0004/1769548/Attachment-D-Summary-of-ACT-Residence.pdf
- https://www.act.gov.au/__data/assets/pdf_file/0005/1769549/Attachment-E-Commonwealth-Statutory-Declaration-form.pdf
- https://www.act.gov.au/__data/assets/pdf_file/0004/3027469/Attachment-F-Employability-Statement-Template-overseas-applicants-only.pdf
- https://www.act.gov.au/__data/assets/pdf_file/0006/1769550/Declaration-of-ACT-Nomination-Obligations-Business-Innovation-Stream-subclass-188.pdf
- https://www.act.gov.au/__data/assets/pdf_file/0007/1769551/Declaration-of-ACT-Nomination-Obligations-Business-Innovation-Stream-subclass-888.pdf

### 404 / failures

- `https://migration.wa.gov.au/sites/default/files/` — 404 (no index)
- Most monthly WA pattern URLs for 2021–2026 (Invite / TRADE / OTHER / Priority / WASMOL) — 404
- Extra months probed after hits (Nov 2025, Feb/Apr/Jun/Jul 2026, TRADE/OTHER variants for Jan/Dec/May) — 404
- ACT historical rankings filenames (`2024-25`, `2023-24`, `2022-23`, `2021-22`) on known and nearby asset IDs — 404
- Unencoded space URL `.../2025-11/SNMP Invite Round - November 2025.pdf` — curl HTTP 000 (invalid request)

HEAD probe of 744 WA monthly candidates completed; last curl exit code 3 is expected (final URL was 404).
