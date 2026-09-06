<p align="center">
  <a href="https://jfilhorv.github.io/Invitation_aus_visas/analise/">
    <img src="analise/logo-ias.png" width="240" alt="Invitation Activity Score — Australian skilled migration dashboard">
  </a>
</p>

<h1 align="center"><a href="https://jfilhorv.github.io/Invitation_aus_visas/analise/">Invitations · occupation history</a></h1>

<p align="center">
  A visual history of Australian skilled-migration invitation rounds, occupation scores and state nomination data.<br>
  Built exclusively from official Australian government publications.
</p>

<p align="center">
  <a href="https://jfilhorv.github.io/Invitation_aus_visas/analise/"><strong>Open the interactive dashboard →</strong></a>
</p>

<p align="center">
  <a href="https://jfilhorv.github.io/Invitation_aus_visas/analise/">
    <img alt="Dashboard online" src="https://img.shields.io/badge/DASHBOARD-OPEN-00A691?style=for-the-badge">
  </a>
  <a href="https://github.com/Jfilhorv/Invitation_aus_visas">
    <img alt="GitHub repository" src="https://img.shields.io/badge/GITHUB-REPOSITORY-E23084?style=for-the-badge&logo=github&logoColor=white">
  </a>
  <img alt="Official sources only" src="https://img.shields.io/badge/SOURCES-OFFICIAL%20.GOV.AU-00A691?style=for-the-badge">
</p>

<p align="center">
  <strong>7,910 normalized records · 488 occupational identities · 9 jurisdictions · 33 official source URLs · January 2021–June 2026 score history</strong>
</p>

> [!IMPORTANT]
> This is a historical evidence and exploration tool. It does not predict invitations, determine visa eligibility or replace professional migration advice.

## Explore the project

| | |
|---|---|
| **[Open the dashboard](https://jfilhorv.github.io/Invitation_aus_visas/analise/)** | Filter by state, visa, year, ANZSCO hierarchy, skill level, metric and occupation |
| **[Open the analytical explorer](https://jfilhorv.github.io/Invitation_aus_visas/analise/analytics.html)** | Scroll through recent evidence, jurisdiction coverage, published volume, ANZSCO concentration and WA-specific lenses |
| **[Open the GitHub repository](https://github.com/Jfilhorv/Invitation_aus_visas)** | Browse the code, normalized data, archived evidence and update scripts |
| **[Understand the metrics](#reading-the-headline-figures)** | Learn what each KPI measures — and what it does not measure |
| **[See the analysis views](#analysis-views)** | Scores, invitations, occupations, states and documentation |
| **[Review the evidence standard](#sources-and-evidence-standard)** | See which official publications are represented |
| **[Open the original government sources](#original-government-sources)** | Go directly to every `.gov.au` page and file used |
| **[Understand the methodology](#data-model-and-normalization)** | Learn how incompatible government publications are combined safely |
| **[Update the dataset](dados/agregado/ATUALIZACAO-DADOS.md)** | Know when to check official sources and how to add a publication safely |
| **[Download data and sources](#downloads)** | CSV, JSON, audit files, ABS references and archived publications |
| **[Read the known limits](#known-limits)** | Understand gaps, uncertainty and differences between programs |

## What the dashboard helps explain

The dashboard brings together invitation rounds, occupational scores and state nomination information that governments publish across different pages, PDFs and levels of detail. It is intended to help answer questions such as:

- Which occupations appeared in published invitation rounds?
- What was the lowest or latest published score for an occupation?
- How has that score changed over time?
- How many occupations had published results in a round?
- How many invitations were reported for a visa or state program?
- Which information is available federally, by state, by visa and by year?

The objective is not merely to collect rows. It is to expose the relationships between dates, scores, occupations, visas and jurisdictions while keeping the limits of each source visible.

## Analysis views

### Analytical explorer

The separate scroll-based analytical page turns the archive into a guided overview while preserving the dashboard's pink-and-teal visual language. It includes a recent-evidence strip, a next-activity watchlist, evidence coverage by jurisdiction, published invitation volume, ANZSCO concentration, and WA breakdowns by residence context, nomination stream, observed EOI score band and approximate EOI queue age.

Percentages describe the records represented in the archive. They are not invitation probabilities or labour-demand estimates. Officially announced future dates are labelled **Official**; modelled monitoring horizons are labelled **Watch estimate**; missing dates remain **Awaiting**. Cross-jurisdiction volume is shown as source coverage rather than a ranking because publication periods and reporting methods differ.

### Global snapshot

The top of the dashboard answers four immediate questions using the active filters:

1. **When was the latest matching round?**
2. **How many occupations had a published result?**
3. **How many invitations were officially reported?**
4. **How did the result change from the previous comparable round?**

The comparison is dynamic. Selecting WA and subclass 190, for example, changes the latest-round context and compares the WA 190 total with the previous available WA 190 round—not with a federal 189 round.

### Occupation explorer

The occupation list combines published score evidence with the **Invitation Activity Score (IAS)**. It can be sorted by IAS, name, lowest score, number of records or historical average.

| Control | What it does |
|---|---|
| **ANZSCO** | Filters the official hierarchy from Major group to six-digit occupation |
| **Skill** | Filters official Australian ANZSCO skill levels 1–5 |
| **Search** | Finds an occupation by title or ANZSCO code |
| **IAS** | Ranks historical invitation activity using the evidence represented in this repository |

IAS is comparative within the current filtered context. It is a historical activity indicator—not labour demand, eligibility, invitation probability or a forecast.

### Occupation history

Selecting an occupation opens its historical record with:

- IAS and its evidence components;
- lowest and latest published score;
- latest invitation date represented;
- number of distinct rounds;
- bar or line presentation;
- exact official source for every table row;
- separate series where the source distinguishes visa, stream, residence or applicant location.

### Occupation groups, scores, invitations and coverage

The chart switch deliberately separates four views:

- **Occupation groups** — official ANZSCO Sub-major groups, shown initially when the dashboard opens;
- **Scores** — published points associated with occupation or program criteria;
- **Invitation events** — aggregate invitations or EOIs invited in a published round;
- **Published coverage** — number of distinct occupations with a published numeric result.

The group view can switch between **INV** (attributed invitations), **OCC** (occupations with published results) and **IAS**. INV is intentionally smaller when governments publish only aggregate totals that cannot be assigned safely to an occupation group. The views are not interchangeable and are never added together.

### States and documentation

The lower views provide program-level context and the documentary trail behind the selected analysis. They distinguish state nomination figures, allocations, occupation detail availability and direct official-source links.

## Reading the headline figures

| Measure | Meaning | Important limitation |
|---|---|---|
| **Latest round** | Most recent official date matching the active filters | State and federal rounds are separate events |
| **Occupations in latest round** | Distinct occupations with a published numeric result | This is not the number of people invited |
| **Invitations in latest round** | Published invitation total for the matching jurisdiction and visa | A total may cover all occupations; it must not be attributed to one occupation |
| **Invitation variation** | Difference from the previous comparable published round | Comparison uses the same jurisdiction and visa scope |
| **Lowest score** | Lowest numeric score in the selected occupation history | A lower score is historically more accessible, not a guarantee |
| **Latest score** | Most recent published score for the selected occupation | Different streams or applicant locations can have different scores |
| **Rounds** | Number of distinct comparable official rounds represented | Publication frequency and occupational detail vary between governments |
| **IAS** | A 0–100 historical activity signal | It is not an invitation probability, eligibility score or government measure |

The federal figure of **10,000 invitations** refers to the entire subclass **189** round of 4 June 2026. Home Affairs does not publish how those 10,000 invitations were distributed among individual occupations.

### Invitation Activity Score (IAS)

IAS makes several dimensions of the collected history easier to compare. Its displayed rule is:

| Component | Weight |
|---|---:|
| Participation across all comparable rounds | 35% |
| Recency measured in comparable rounds | 30% |
| Participation in the last eight comparable rounds | 20% |
| Recent round-by-round continuity | 10% |
| Comparable published score within the same round context | 5% |

Pink represents lower historical activity and teal higher activity. Grey indicates insufficient evidence. Context breadth remains visible in the hover as evidence quality but no longer adds points to IAS. The score is recalculated from the active context and should be read together with its hover explanation and evidence level. Recency is based on the number of comparable rounds since the last appearance, not simply elapsed calendar months. Federal, ACT and WA thresholds are compared only inside compatible jurisdiction, visa, metric and published stream contexts; aggregate invitation totals are never assigned to an individual occupation. Histories with fewer than eight comparable rounds are progressively adjusted towards the neutral midpoint of 50, preventing one recent observation from appearing as a fully established IAS 100.

## Visa and jurisdiction context

### Federal

Home Affairs publishes SkillSelect invitation results for subclass **189** and, in historical rounds, the family-sponsored regional stream represented in the data as **491-family**. These are federal results and should not be combined with state invitation rounds as though they were one event.

### State nomination

States and territories administer nomination activity for:

- **190 — Skilled Nominated**, a permanent visa;
- **491 — Skilled Work Regional (Provisional)**, a regional provisional visa.

The detail published by each jurisdiction is inconsistent. Some publish totals only, some publish occupational criteria, and some publish neither historical results nor occupation-level counts.

### Why WA can display `190 / 491*`

Western Australia publishes invitation totals separately by subclass, but its occupation-level score material does not assign every occupation row exclusively to 190 or 491. For that reason:

- the **209** shown for WA 190 is a confirmed aggregate total;
- WA occupation and score rows are useful contextual criteria;
- those rows are displayed as **190 / 491*** rather than being falsely assigned to one subclass;
- the asterisk indicates that the official occupation-level source does not separate the visa subclasses.

Filtering WA by 190 or 491 therefore keeps relevant WA occupation criteria visible while preserving this uncertainty.

## Chart methodology

The chart always retains the complete available official-result boundary, currently **January 2021 to June 2026** for numeric score data. A date enters this axis only when the collected source publishes a numeric occupational result for that event. Monthly program summaries, financial-year allocations and administrative updates do not create score-round dates.

The default **Occupation groups** view uses official ANZSCO Sub-major groups. Its Date Range control is available only in this view because it recalculates the group comparison, occupation list and supporting table over the selected historical window. `All` represents the complete available range. Other chart tabs retain stable control positions but do not display Date Range where it has no meaningful role.

Clicking a group filters the occupation list. Other groups remain visible in light grey so the user can change the selection or click the active group again to clear it. Bar and smooth-line modes use the same underlying values.

The **Scores** view uses a fixed sequence of every valid official result date in the active State, Visa, Year, Metric and Skill context. Selecting a different occupation does not rebuild or shift this date base:

- a bar or point appears only where the selected occupation has a published result;
- an empty position means no result was published for that occupation on that valid date, not zero;
- every official result date keeps a fixed axis position and a compact visible label;
- year brackets preserve chronological orientation;
- smooth lines break at missing result dates instead of implying continuous observations.

The fixed event sequence makes occupations directly comparable. Horizontal slots represent official result events rather than a uniform number of elapsed calendar days; dates remain the authoritative temporal reference.

Scores, invitations, occupation coverage and IAS remain separate measures. Bar and line modes change only the presentation, not the underlying values.

## Sources and evidence standard

Only official Australian government sources ending in **`.gov.au`** are accepted. Blogs, migration agents, commercial summaries, social media and web archives are excluded.

| Jurisdiction | Official material represented | Occupation detail |
|---|---|---|
| **Federal — Home Affairs** | Current and previous SkillSelect invitation rounds | Yes, scores by published occupation |
| **ACT** | Invitation-round rankings and published totals | ANZSCO unit-group detail where published |
| **WA** | Last-invited EOI criteria and state invitation totals | Yes, but 190/491 is not separated per occupation |
| **SA** | Invitations-issued publications | ANZSCO sub-major groups and subclass totals |
| **TAS** | Published 190/491 totals | No occupation-level result in the collected source |
| **NSW, VIC, QLD, NT** | Program information and available official totals | No equivalent published occupation-result history found |

Every collected record retains its official source URL. Source files are checked for a successful response, official final host and valid PDF or HTML content, and are fingerprinted with SHA-256.

## Data model and normalization

Government publications do not share a common schema. They can describe exact occupations, ANZSCO unit groups, sub-major groups, streams, residence categories or whole-program totals. The combined dataset keeps those levels distinct rather than forcing them into false equivalence.

Occupation identities are matched conservatively against the official **ABS ANZSCO 2022** structure and index:

- an exact code or title match is retained when supported;
- broader occupational groups remain broader groups;
- source wording is preserved;
- missing codes are not invented;
- onshore, offshore, residence and program streams remain separate series;
- aggregate totals are not duplicated across their component rows.

The global ANZSCO filter preserves the official hierarchy:

```text
Major group (1 digit)
└── Sub-major group (2 digits)
    └── Minor group (3 digits)
        └── Unit group (4 digits)
            └── Occupation (6 digits)
```

The dashboard lookup contains **1,590 official nodes**: 8 Major groups, 43 Sub-major groups, 99 Minor groups, 364 Unit groups and 1,076 occupations. Predominant skill level is a separate official attribute, not a sixth hierarchy level. Where ABS distinguishes Australian and New Zealand skill levels, the dashboard uses the Australian value.

The principal analytical fields include jurisdiction, visa, round date, occupation, ANZSCO code, occupational level, metric, numeric value, source URL, source fingerprint and validation status.

## Known limits

- Governments do not publish all states, visas and occupational detail in one national dataset.
- An invitation total usually cannot be divided reliably among occupations.
- A published score is historical evidence, not a future threshold.
- “No data” means no suitable result was found in the collected official publication; it does not mean no invitations occurred.
- State nomination, federal invitation, nomination allocation and visa grant are different measures and are not interchangeable.
- Publication formats and terminology can change between program years.

These limits are deliberately visible in the dashboard through labels such as **Not published**, **Not specified** and **190 / 491*** rather than being filled with estimates or zeroes.

## Downloads

All downloadable material used by the analysis is available below. The CSV is the easiest format for Excel, Power BI or general analysis; JSON preserves the same normalized records for code and web applications.

### Original government sources

These are the original government links from which the source material was collected. Links marked **PDF/XLSX** download or open the government file directly; links marked **HTML** open the exact official publication page used.

| Jurisdiction | Original official source | Type | What it contributed |
|---|---|---:|---|
| **Federal** | [Home Affairs — current SkillSelect invitation rounds](https://immi.homeaffairs.gov.au/visas/working-in-australia/skillselect/invitation-rounds) | HTML | Latest federal round, occupations, scores and 189 invitation total |
| **Federal** | [Home Affairs — previous SkillSelect rounds](https://immi.homeaffairs.gov.au/visas/working-in-australia/skillselect/previous-rounds) | HTML | Historical federal occupation scores and invitation totals |
| **Federal** | [Home Affairs — state and territory nomination allocations](https://immi.homeaffairs.gov.au/what-we-do/state-and-territory-nomination-allocations) | HTML | Annual 190 and 491 allocations by jurisdiction |
| **ACT** | [ACT — guidelines and invitations library](https://www.act.gov.au/migration/resources/library-guidelines-and-invitations) | HTML | Official document index |
| **ACT** | [ACT — Canberra Matrix invitation round](https://www.act.gov.au/migration/resources/canberra-matrix-invitation-round) | HTML | Round context and methodology |
| **ACT** | [ACT — 2025–26 invitation-round rankings](https://www.act.gov.au/__data/assets/pdf_file/0009/2920554/2025-26-Invitation-round-rankings.pdf) | PDF | Rankings, occupations and score criteria |
| **WA** | [WA — State Nominated Migration Program](https://migration.wa.gov.au/our-services-support/state-nominated-migration-program) | HTML | Program information, visa totals and historical round tables |
| **WA** | [WA — May 2025 occupation results](https://migration.wa.gov.au/sites/default/files/2025-05/SNMP%20Invite%20Round%20-%20Last%20Invited%20By%20Occupation%20May%202025.pdf) | PDF | Last invited EOI by occupation |
| **WA** | [WA — historical occupation rounds, May 2023–June 2025](https://migration.wa.gov.au/sites/default/files/2025-06/SNMP%20Invite%20Round%20-%20Last%20Invited%20By%20Occupation.pdf) | PDF collection | Nine additional official rounds with occupation, residence, stream, EOI score and submission date |
| **WA** | [WA — October 2025 priority round](https://migration.wa.gov.au/sites/default/files/2025-10/SNMP%20-%20Priority%20Invite%20Round%20-%20October%202025.pdf) | PDF | Occupation-level round results |
| **WA** | [WA — December 2025 invitation round](https://migration.wa.gov.au/sites/default/files/2025-12/SNMP%20Invite%20Round%20-%20December%202025.pdf) | PDF | Occupation-level round results |
| **WA** | [WA — January 2026 invitation round](https://migration.wa.gov.au/sites/default/files/2026-01/SNMP%20Invite%20Round%20-%20January%202026.pdf) | PDF | Occupation-level round results |
| **WA** | [WA — March 2026 priority-trade results](https://migration.wa.gov.au/sites/default/files/2026-03/TRADE%20-%20SNMP%20Invite%20Round%20-%20Last%20Invited%20By%20Occupation%20-%20March%202026.pdf) | PDF | Occupation-level round results |
| **WA** | [WA — March 2026 other-priority results](https://migration.wa.gov.au/sites/default/files/2026-03/v.1OTHER%20priority%20occupations%20-%20SNMP%20Invite%20round%20-%20March%202026.pdf) | PDF | Occupation-level round results |
| **WA** | [WA — May 2026 priority-trade results](https://migration.wa.gov.au/sites/default/files/2026-05/Last%20invited%20expression%20of%20interest%20-%20Priority%20trade%20occupations%20-%20May%202026.pdf) | PDF | Latest invited EOI scores by priority-trade occupation |
| **SA** | [SA — invitations-issued index](https://migration.sa.gov.au/news?category=invitations-issued) | HTML | Official index of all collected SA publications |
| **SA** | [SA — December 2025](https://migration.sa.gov.au/news/invitations-issued-dec-2025) · [January 2026](https://migration.sa.gov.au/news/invitations-issued-jan-2026) · [February 2026](https://migration.sa.gov.au/news/invitations-issued-feb-2026) · [March 2026](https://migration.sa.gov.au/news/invitations-issued-march-2026) · [April 2026](https://migration.sa.gov.au/news/invitations-issued-april-2026) · [May 2026](https://migration.sa.gov.au/news/invitations-issued-may-2026) · [Late May 2026](https://migration.sa.gov.au/news/invitations-issued-late-may-2026) | HTML | Invitation totals by ANZSCO group and visa subclass |
| **TAS** | [Tasmania — processing times and allocation usage](https://www.migration.tas.gov.au/news/processing_times_and_allocation_usage) | HTML | Published 190 and 491 program totals |
| **TAS** | [Tasmania — document library](https://www.migration.tas.gov.au/skilled_migration/document_library) | HTML | Program documentation context |
| **NSW** | [NSW — Skilled Nominated visa subclass 190](https://www.nsw.gov.au/visas-and-migration/skilled-visas/skilled-nominated-visa-subclass-190) | HTML | Official process; confirms occupation results are not published there |
| **VIC** | [Victoria — Registration of Interest](https://liveinmelbourne.vic.gov.au/migrate/skilled-migration-visas/registration-of-interest-for-victorian-state-visa-nomination) | HTML | Official process; no occupation-result table |
| **QLD** | [Queensland — registering interest](https://www.migration.qld.gov.au/visa-options/skilled-visas/registering-your-interest-in-queenslands-migration-program) | HTML | Official process; no invitation-by-occupation results |
| **NT** | [NT Government](https://nt.gov.au/) · [Overseas workers and your business](https://nt.gov.au/employ/for-employers-in-nt/employ-people-from-overseas/overseas-workers-and-your-business) | HTML | Official `.gov.au` pages; no invitation-by-occupation publication found |
| **ABS** | [ANZSCO 2022 structure](https://www.abs.gov.au/statistics/classifications/anzsco-australian-and-new-zealand-standard-classification-occupations/2022/anzsco%202022%20structure%20062023.xlsx) | XLSX | Official occupation hierarchy |
| **ABS** | [ANZSCO 2022 index of titles and specialisations](https://www.abs.gov.au/statistics/classifications/anzsco-australian-and-new-zealand-standard-classification-occupations/2022/anzsco%202022%20index%20of%20principal%20titles%2C%20alternative%20titles%20and%20specialisations%20062023.xlsx) | XLSX | Exact occupation-title matching reference |

### Analysis-ready data

| Download | Format | Contents |
|---|---:|---|
| **[Download the complete normalized dataset](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/agregado/vistos-de-convites.csv)** | CSV | All collected and normalized invitation, score, occupation and nomination records |
| **[Download the complete normalized dataset](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/agregado/vistos-de-convites.json)** | JSON | Same analytical records with their full field structure |
| **[Download the dashboard data bundle](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/analise/data.js)** | JavaScript | Browser-ready copy of the normalized dataset used by the dashboard |
| **[Download the ANZSCO hierarchy bundle](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/analise/anzsco-hierarchy.js)** | JavaScript | Browser-ready hierarchy and Australian skill-level lookup derived from the official ABS workbook |

### Methodology and audit files

| Download | Purpose |
|---|---|
| **[Download methodology](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/agregado/metodologia.md)** | Normalization, interpretation, deduplication and aggregation rules |
| **[Download state-source audit](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/agregado/auditoria-fontes-estaduais.md)** | Review of coverage and limitations by jurisdiction |
| **[Download extraction log](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/agregado/extracao-log.md)** | Record of extraction and transformation activity |
| **[Read the data-update guide](dados/agregado/ATUALIZACAO-DADOS.md)** | Update cadence, ingestion sequence, validation checklist and ANZSCO rebuild instructions |
| **[Download official-source inventory](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/fontes/inventario-oficial.md)** | Catalogue of the government publications represented |
| **[Download source validation manifest](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/fontes/manifesto-validacao.csv)** | URLs, validation state and SHA-256 source fingerprints |
| **[Download WA and ACT source notes](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/fontes/downloads-wa-act.md)** | Documentary notes for the collected WA and ACT publications |

### Official classification references

| Download | Contents |
|---|---|
| **[Download ABS ANZSCO 2022 index](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/fontes/anzsco-2022-index.xlsx)** | Official occupation-title and code reference used for conservative identity matching |
| **[Download ABS ANZSCO 2022 structure](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/fontes/anzsco-2022-structure.xlsx)** | Official hierarchy used to distinguish occupations from broader groups |

### Archived official publications

The repository retains the official HTML and PDF material used to make the analysis reproducible. Every link below points directly to the archived file.

<details>
<summary><strong>Federal — 3 downloads</strong></summary>

- [Download current invitation rounds](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/federal/invitation-rounds.html)
- [Download previous invitation rounds](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/federal/previous-rounds.html)
- [Download state and territory nomination allocations](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/federal/state-and-territory-nomination-allocations.html)

</details>

<details>
<summary><strong>ACT — 3 downloads</strong></summary>

- [Download 2025–26 invitation-round rankings PDF](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/act/2025-26-Invitation-round-rankings.pdf)
- [Download Canberra Matrix invitation-round page](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/act/canberra-matrix-invitation-round.html)
- [Download ACT guidelines and invitations page](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/act/library-guidelines-and-invitations.html)

</details>

<details>
<summary><strong>Western Australia — 9 downloads</strong></summary>

- [Download 2025–26 WA SNMP criteria](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/wa/2025-26%20WA%20SNMP%20Criteria%20-%20July%202025.pdf)
- [Download May 2023 occupation results](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/wa/Last%20invited%20EOI%20by%20occupation%20-%20May%202023.pdf)
- [Download August 2023 occupation results](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/wa/Last%20invited%20EOI%20by%20occupation%20-%20August%202023.pdf)
- [Download August 2024 invitation round](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/wa/SNMP%20Invite%20Round%20-%20August%202024.pdf)
- [Download September 2024 invitation round](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/wa/SNMP%20Invite%20Round%20-%20September%202024.pdf)
- [Download October 2024 invitation round](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/wa/SNMP%20Invite%20Round%20-%20October%202024.pdf)
- [Download December 2024 invitation round](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/wa/SNMP%20Invite%20Round%20-%20December%202024.pdf)
- [Download February 2025 invitation round](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/wa/SNMP%20Invite%20Round%20-%20February%202025.pdf)
- [Download March 2025 non-priority round](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/wa/SNMP%20Invite%20Round%20-%20March%202025%20Non%20Priority.pdf)
- [Download June 2025 invitation round](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/wa/SNMP%20Invite%20Round%20-%20June%202025.pdf)
- [Download May 2026 priority-trade results](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/wa/Last%20invited%20expression%20of%20interest%20-%20Priority%20trade%20occupations%20-%20May%202026.pdf)
- [Download October 2025 priority round](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/wa/SNMP%20-%20Priority%20Invite%20Round%20-%20October%202025.pdf)
- [Download December 2025 invitation round](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/wa/SNMP%20Invite%20Round%20-%20December%202025.pdf)
- [Download January 2026 invitation round](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/wa/SNMP%20Invite%20Round%20-%20January%202026.pdf)
- [Download May 2025 occupation results](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/wa/SNMP%20Invite%20Round%20-%20Last%20Invited%20By%20Occupation%20May%202025.pdf)
- [Download March 2026 trade results](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/wa/TRADE%20-%20SNMP%20Invite%20Round%20-%20Last%20Invited%20By%20Occupation%20-%20March%202026.pdf)
- [Download March 2026 other-priority results](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/wa/v.1OTHER%20priority%20occupations%20-%20SNMP%20Invite%20round%20-%20March%202026.pdf)
- [Download WA State Nominated Migration Program page](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/wa/state-nominated-migration-program.html)

</details>

<details>
<summary><strong>South Australia — 8 downloads</strong></summary>

- [Download December 2025 invitations](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/sa/invitations-issued-dec-2025.html)
- [Download January 2026 invitations](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/sa/invitations-issued-jan-2026.html)
- [Download February 2026 invitations](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/sa/invitations-issued-feb-2026.html)
- [Download March 2026 invitations](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/sa/invitations-issued-march-2026.html)
- [Download April 2026 invitations](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/sa/invitations-issued-april-2026.html)
- [Download May 2026 invitations](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/sa/invitations-issued-may-2026.html)
- [Download late-May 2026 invitations](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/sa/invitations-issued-late-may-2026.html)
- [Download SA invitations-issued index](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/sa/news-invitations-issued-index.html)

</details>

<details>
<summary><strong>Other states and territories — 9 downloads</strong></summary>

- [Download NSW subclass 190 page](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/nsw/skilled-nominated-visa-subclass-190.html)
- [Download NT government migration page](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/nt/nt-gov-home.html)
- [Download NT overseas-workers page](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/nt/overseas-workers-and-your-business.html)
- [Download Queensland registration-of-interest page](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/qld/registering-your-interest.html)
- [Download Tasmania document library](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/tas/document-library.html)
- [Download Migration Tasmania home page](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/tas/migration-tas-home.html)
- [Download Tasmania processing and allocation page](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/tas/processing-times-and-allocation-usage.html)
- [Download Victoria registration-of-interest page](https://raw.githubusercontent.com/Jfilhorv/Invitation_aus_visas/master/dados/estados/vic/registration-of-interest.html)

</details>

### Complete archive

**[Download the entire project and source archive as ZIP](https://github.com/Jfilhorv/Invitation_aus_visas/archive/refs/heads/master.zip)**

The archived government files are retained for traceability. For the latest policy or eligibility rules, always follow the original `.gov.au` source linked in the dashboard.

## Project links

| Resource | Link |
|---|---|
| Live GitHub Pages dashboard | [jfilhorv.github.io/Invitation_aus_visas/analise](https://jfilhorv.github.io/Invitation_aus_visas/analise/) |
| Source repository | [github.com/Jfilhorv/Invitation_aus_visas](https://github.com/Jfilhorv/Invitation_aus_visas) |
| Data and archived evidence | [Browse the repository](https://github.com/Jfilhorv/Invitation_aus_visas/tree/master/dados) |
| Data-update and validation guide | [Read ATUALIZACAO-DADOS.md](dados/agregado/ATUALIZACAO-DADOS.md) |

## Publication and responsibility

The dashboard is published as a static GitHub Pages site from this repository. It is an independent evidence project and is not affiliated with, endorsed by or operated by the Australian Government. Government source material remains subject to its original terms and attribution requirements; code and repository licensing should be checked in the repository before reuse.

## Audit trail

The supporting material is retained in the repository:

- `dados/agregado/metodologia.md` — detailed transformation and interpretation rules;
- `dados/fontes/inventario-oficial.md` — inventory of official publications;
- `dados/fontes/manifesto-validacao.csv` — validation and source fingerprints;
- `dados/agregado/vistos-de-convites.csv` and `.json` — normalized analytical records.

The governing principle is simple: **show what the official source supports, preserve its level of detail, and make uncertainty explicit.**
