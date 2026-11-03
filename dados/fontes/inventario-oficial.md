# Inventario oficial — rounds de convite (skilled migration) por ocupacao

Coleta atualizada em 3 Nov 2026. Somente fontes `.gov.au`. Sem blogs, agentes de migracao, archive.org ou sites terceiros. Um documento canonico vigente por fonte; atualizacoes de novo round / novo ano-programa mantidas como versoes distintas.

Regra de validade: HTTP 200 + host final `.gov.au` + PDF `%PDF-` ou HTML com titulo oficial + SHA256.

## Federal (Home Affairs / SkillSelect)

**Documento vigente (um):** pagina HTML oficial

- [Invitation rounds](https://immi.homeaffairs.gov.au/visas/working-in-australia/skillselect/invitation-rounds) → `dados/federal/invitation-rounds.html`
- Ultimo round publicado na pagina: **Invitations issued on 15 October 2026**, com **20.000 EOIs convidadas** para a subclass 189 e pontuacao minima publicada para **159 ocupacoes**.
- Nao ha PDF/XLSX ligado nesta pagina.

**Anos anteriores no site oficial:** sim

- [Previous rounds](https://immi.homeaffairs.gov.au/visas/working-in-australia/skillselect/previous-rounds) → `dados/federal/previous-rounds.html`
- Historico oficial de rounds anteriores (pontos minimos / ocupacoes) em HTML.

**data.gov.au:** busca CKAN `https://data.gov.au/data/api/3/action/package_search?q=skillselect` nao devolveu dataset de SkillSelect invitation rounds (unico hit irrelevante: gazette NSW). Nenhum PDF/XLSX oficial de invitation rounds encontrado em data.gov.au. **NOT_PUBLISHED** como dataset tabular separado.

## ACT

**Documentos vigentes (um por ano-programa):** PDF

- Biblioteca: [Library - guidelines and invitations](https://www.act.gov.au/migration/resources/library-guidelines-and-invitations) → `dados/estados/act/library-guidelines-and-invitations.html`
- PDF canonico atual: [2026-27 Invitation round rankings](https://www.act.gov.au/__data/assets/pdf_file/0020/3140480/2026-27-Invitation-round-rankings.pdf) → `dados/estados/act/2026-27-Invitation-round-rankings.pdf`
- PDF canonico: [2025-26 Invitation round rankings](https://www.act.gov.au/__data/assets/pdf_file/0009/2920554/2025-26-Invitation-round-rankings.pdf) → `dados/estados/act/2025-26-Invitation-round-rankings.pdf`
- Pagina [Canberra Matrix – Invitation Round](https://www.act.gov.au/migration/resources/canberra-matrix-invitation-round) → `dados/estados/act/canberra-matrix-invitation-round.html` (explica o round; rankings no PDF).
- Ultimo round: **12 October 2026**, subclass 190, com **261 convites**; a pagina registra zero convites 491 nesse round.

**Anos anteriores no site oficial:** a biblioteca lista os PDFs **2026-27** e **2025-26**. Um resultado de busca ainda referencia o antigo `2024-25-Invitation-Round-Rankings.pdf`, mas a URL oficial devolveu HTTP 404; por isso ele nao foi incorporado. Nao ha link recuperavel 2024-25 / 2023-24 de rankings. Existe DOCX equivalente do mesmo 2025-26 (nao baixado: duplicata do mesmo conteudo). Listas de ocupacao elegivel e guidelines 190/491 **nao** foram baixadas (nao sao resultados de convite).

## WA

**Documentos vigentes:** dois PDFs complementares de last invited EOI + HTML da pagina SNMP

- [State Nominated Migration Program](https://migration.wa.gov.au/our-services-support/state-nominated-migration-program) → `dados/estados/wa/state-nominated-migration-program.html`
- PDFs ligados na pagina atual: [construction trades](https://migration.wa.gov.au/sites/default/files/2026-10/Oct%202026.BC%20-%20SNMP%20Invite%20Round%20-%20Last%20Invited%20By%20Occupation%20B%26C%20Trade%20Occupations.pdf) e [other priority occupations](https://migration.wa.gov.au/sites/default/files/2026-10/Oct%202026%20-%20SNMP%20Invite%20Round%20-%20Last%20Invited%20By%20Occupation%20in%20other%20priority%20occupation.pdf).
- Round corrente na aba: **14 October 2026**, com 1.227 convites (836 subclass 190 e 391 subclass 491), 62 ocupacoes e 92 perfis ocupacao/stream.

**Anos anteriores no site oficial:** sim. Alem das tabelas HTML agregadas, foram localizados e arquivados PDFs oficiais de last-invited EOI por ocupacao:

- maio, agosto, outubro e novembro de 2023;
- agosto, setembro, outubro, novembro e dezembro de 2024;
- fevereiro, marco, maio, junho, outubro e dezembro de 2025;
- janeiro, marco, maio e outubro de 2026.

Marco de 2026 possui dois documentos complementares no dominio oficial: [trades prioritarias](https://migration.wa.gov.au/sites/default/files/2026-03/TRADE%20-%20SNMP%20Invite%20Round%20-%20Last%20Invited%20By%20Occupation%20-%20March%202026.pdf) e [outras ocupacoes prioritarias](https://migration.wa.gov.au/sites/default/files/2026-03/v.1OTHER%20priority%20occupations%20-%20SNMP%20Invite%20round%20-%20March%202026.pdf). Ambos continuam acessiveis no servidor oficial, embora nao estejam ligados na navegacao corrente.

No total, a extracao representa **21 documentos em 19 rodadas/periodos ocupacionais de WA**. Os PDFs preservam ANZSCO, stream, residencia, EOI points score e data de submissao. Eles nao publicam a quantidade de convites por profissao.

### Lacunas historicas confirmadas de WA

Os totais mensais oficiais e os resultados ocupacionais sao publicacoes diferentes. A auditoria encontrou tres meses com total de convites, mas sem linhas ocupacionais arquivadas:

| Mes | O que existe | Situacao da fonte ocupacional |
|---|---|---|
| February 2026 | 2.400 convites agregados | Dois PDFs oficiais chegaram a ser indexados, mas hoje os URLs oficiais retornam HTTP 404; nenhum dado foi reconstruido de cache ou fonte secundaria |
| April 2026 | 1 convite agregado | Nenhum PDF oficial por ocupacao foi localizado |
| September 2026 | 1.100 convites agregados | Nenhum PDF oficial por ocupacao foi localizado |

Esses meses permanecem no dataset apenas com suas metricas agregadas. O log de extracao registra `WA HISTORY GAP` para impedir que a ausencia pareca cobertura ocupacional completa.

As abas HTML tambem fornecem:

- Aba **2024-25 Invitation rounds** — totais mensais por stream/visa (nao last-invited por ocupacao).
- Aba **2023-24 Invitation rounds** — idem.
- Alguns PDFs historicos deixam de aparecer na navegacao corrente, mas continuam hospedados no dominio oficial e sao preservados no arquivo do projeto com URL e SHA-256.
- O PDF de criterios SNMP 2025-26 foi preservado como documentacao; occupation lists e payslip guidance nao foram tratados como invitation results.

## SA

**Documento vigente:** HTML (nao ha PDF unico)

- Indice: [Invitations issued](https://migration.sa.gov.au/news?category=invitations-issued) → `dados/estados/sa/news-invitations-issued-index.html` (page 1 of 1).
- Mais recente: [Invitations issued - Late May 2026](https://migration.sa.gov.au/news/invitations-issued-late-may-2026) → `dados/estados/sa/invitations-issued-late-may-2026.html`

**Atualizacoes 2025-26 listadas no indice (cada mes = versao oficial nova):**

| Pagina | Arquivo |
|---|---|
| Late May 2026 | `invitations-issued-late-may-2026.html` |
| May 2026 | `invitations-issued-may-2026.html` |
| April 2026 | `invitations-issued-april-2026.html` |
| March 2026 | `invitations-issued-march-2026.html` |
| Feb 2026 | `invitations-issued-feb-2026.html` |
| Jan 2026 | `invitations-issued-jan-2026.html` |
| Dec 2025 | `invitations-issued-dec-2025.html` |

Nenhum PDF/XLSX nestas paginas. Nao foram inventadas URLs fora do indice oficial.

## NSW — NOT_PUBLISHED

Pagina oficial salva: [Skilled Nominated visa (subclass 190)](https://www.nsw.gov.au/visas-and-migration/skilled-visas/skilled-nominated-visa-subclass-190) → `dados/estados/nsw/skilled-nominated-visa-subclass-190.html`

NSW descreve o invitation process e Skills List (elegibilidade). **Nao publica PDF nem tabela de resultados de convite por ocupacao.**

## VIC — NOT_PUBLISHED

Pagina oficial salva: [Registration of Interest for Victorian skilled visa nomination](https://liveinmelbourne.vic.gov.au/migrate/skilled-migration-visas/registration-of-interest-for-victorian-state-visa-nomination) → `dados/estados/vic/registration-of-interest.html`

VIC explica que invitation rounds ocorrem ao longo do ano, sem datas fixas. **Nao publica PDF/resultados por ocupacao.**

## QLD — NOT_PUBLISHED

Pagina oficial salva: [Registering your interest in Queensland's migration program](https://www.migration.qld.gov.au/visa-options/skilled-visas/registering-your-interest-in-queenslands-migration-program) → `dados/estados/qld/registering-your-interest.html`

QLD explica ROI/EOI e convites por e-mail. Occupation lists no site sao **elegibilidade**, nao invitation results — nao baixadas. **Nao publica PDF de invitation-by-occupation.**

## TAS — NOT_PUBLISHED (por ocupacao)

Paginas oficiais salvas:

- Home: [migration.tas.gov.au](https://www.migration.tas.gov.au/) → `dados/estados/tas/migration-tas-home.html`
- [Processing Times and Invitations Issued](https://www.migration.tas.gov.au/news/processing_times_and_allocation_usage) → `dados/estados/tas/processing-times-and-allocation-usage.html` — rodada ROI de **29 Oct 2026**: 64 convites subclass 190 e 26 subclass 491; menores scores ROI de 316 e 75, alem de fila, vagas disponiveis e media movel. A escala ROI da Tasmania nao e equivalente aos pontos SkillSelect. **Sem breakdown por ocupacao**.
- [Document library / Resources](https://www.migration.tas.gov.au/skilled_migration/document_library) → `dados/estados/tas/document-library.html` — PDFs de programa/checklist/ocupacoes elegiveis, **nao** invitation rankings.

## NT — NOT_PUBLISHED

Tentativas oficiais:

- `https://theterritory.nt.gov.au/` → **INVALID** (redirect para `australiasnorthernterritory.com.au`, fora de `.gov.au`; nao salvo).
- `https://migration.nt.gov.au/` → **INVALID** (mesmo redirect comercial; nao salvo).
- Homepage `.gov.au` salva: [nt.gov.au](https://nt.gov.au/) → `dados/estados/nt/nt-gov-home.html`
- Unica pagina `.gov.au` encontrada sobre overseas workers: [Overseas workers and your business](https://nt.gov.au/employ/for-employers-in-nt/employ-people-from-overseas/overseas-workers-and-your-business) → `dados/estados/nt/overseas-workers-and-your-business.html` — aponta nomination para `theterritory.com.au` (fora de `.gov.au`).

**Nao existe PDF/HTML oficial `.gov.au` de invitation-by-occupation para o NT.**

## Resumo do que existe vs o que nao e publicado

| Jurisdicao | Documento vigente de convite por ocupacao | Formato | Anos anteriores no site oficial |
|---|---|---|---|
| Federal | Invitation rounds (15 Oct 2026) + previous rounds | HTML | Sim (pagina previous-rounds) |
| ACT | 2026-27 e 2025-26 Invitation round rankings | PDF | Sim (2025-26 preservado) |
| WA | 21 documentos em 19 last-invited EOI rounds/periods, May 2023–Oct 2026 | PDF + HTML | Sim: PDFs ocupacionais e tabelas HTML agregadas; gaps documentados em Feb/Apr/Sep 2026 |
| SA | News "Invitations issued" (Late May 2026 + meses 2025-26) | HTML | Indice atual lista Dec 2025–Late May 2026 |
| NSW | **NOT_PUBLISHED** | — | — |
| VIC | **NOT_PUBLISHED** | — | — |
| QLD | **NOT_PUBLISHED** | — | — |
| TAS | Convites e scores ROI agregados; **NOT_PUBLISHED** por ocupacao | HTML | Pagina corrente e sobrescrita a cada atualizacao |
| NT | **NOT_PUBLISHED** (site de nomination saiu de `.gov.au`) | — | — |

Validacao detalhada: `dados/fontes/manifesto-validacao.csv`.
