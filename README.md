# Vistos de convites (Austrália)

Fonte: **somente sites oficiais `.gov.au`**.  
Um documento vigente por governo; arquivo extra só quando o próprio governo publicou uma versão nova (round / ano-programa mudou).

## Página de análise

Abra `analise/index.html` no navegador (carrega `analise/data.js` gerado do JSON).

Filtros: estado, visto, categoria, ocupação, métrica. Tabela empilhada: data · estado · visto · ocupação · pontuação.

## Arquivo único agregado

- `dados/agregado/vistos-de-convites.csv`
- `dados/agregado/vistos-de-convites.json`
- `analise/data.js` (mesmo conteúdo para a página)

Categoria: `visto_de_convite`. Cada linha tem `fonte_url`, `sha256_fonte` e `validado`.

## Validação

`dados/fontes/manifesto-validacao.csv`

Critérios: HTTP 200, host final `.gov.au`, PDF começa com `%PDF` (ou HTML oficial), SHA256.

Inventário: `dados/fontes/inventario-oficial.md`

## O que o governo publica hoje

| Governo | Documento vigente | Por profissão? | Histórico no site oficial |
|---|---|---|---|
| Federal (Home Affairs) | HTML SkillSelect invitation rounds | Sim (189 / 491 family) | `previous-rounds` (2020–2026) |
| ACT | 1 PDF: 2025-26 Invitation round rankings | Sim (grupo ANZSCO) | Só o ano vigente |
| WA | 1 PDF: last invited EOI (May 2026) | Sim (trades atuais) | Totais HTML 2023-24 e 2024-25 |
| SA | HTML “Invitations issued” | Por grupo ANZSCO | Dec 2025–May 2026 no índice |
| NSW, VIC, QLD, NT | Não publicam resultados | Não | — |
| TAS | Totais 190/491 | Não | — |

Não foram usados blogs, agentes, archive.org nem sites fora de `.gov.au`.
