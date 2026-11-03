# Atualização dos dados

Este documento define quando procurar novas publicações oficiais e como incorporá-las ao projeto sem perder histórico, escopo ou rastreabilidade.

## Quando podem surgir novos dados

Não existe um calendário nacional único. Cada fonte deve ser monitorada separadamente.

| Fonte | Próxima atualização conhecida | Frequência prática | O que pode mudar |
|---|---|---|---|
| Home Affairs — SkillSelect | Última rodada publicada em **15 de outubro de 2026**; nenhuma próxima data oficial registrada nesta atualização. | Periódica durante o program year | Total de EOIs, tie-break, ocupações e scores mínimos publicados |
| Home Affairs — allocations | Quando forem divulgadas ou revisadas as alocações do program year | Normalmente por program year, com possíveis revisões | Alocações 190 e 491 por estado e território |
| ACT | Próximas semanas provisórias: **25 Jan, 22 Mar e 24 May 2027** | Rodadas regulares quando o programa está ativo | Matrix scores, rankings e resultados por unit group |
| WA | Rodadas mensais previstas; última publicada em **14 Oct 2026** | Verificar a página do SNMP e novos PDFs de rounds | Last invited EOI, critérios por ocupação e totais 190/491 |
| SA | Sem calendário fixo garantido | Verificar o índice oficial de “Invitations issued” | Convites 190/491 por sub-major group ANZSCO |
| TAS | Última rodada publicada em **29 Oct 2026** | Página corrente é sobrescrita regularmente | Convites, score ROI mínimo, fila e vagas por subclass |
| NSW, VIC, QLD e NT | Conforme cada governo publicar | Revisão periódica das páginas oficiais | Totais, allocations, regras e eventual surgimento de detalhe ocupacional |

“Sem nova publicação” não significa que não houve convites. Significa apenas que não existe um novo resultado oficial compatível com o modelo do projeto.

## Busca obrigatória para WA

Em toda atualização, verificar nesta ordem:

1. a aba **Current invitation round** da [página oficial do SNMP](https://migration.wa.gov.au/our-services-support/state-nominated-migration-program);
2. a tabela do program year, comparando todos os meses e os totais 190/491 com o último snapshot local;
3. todos os links cujo texto ou arquivo contenha **last invited EOI**, **last invited by occupation** ou equivalente;
4. a pasta mensal oficial indicada pelos links (`/sites/default/files/YYYY-MM/`), sem adivinhar URLs;
5. a página de [notícias do Migration WA](https://migration.wa.gov.au/news), usada para localizar anúncios, mas não para substituir os resultados tabulares;
6. redes sociais e páginas de agentes apenas como alerta de investigação — nunca como fonte incorporada.

O extrator executa uma auditoria de frescor e cobertura histórica de WA. Ele registra o mês mais recente dos totais e dos PDFs ocupacionais, emite `WA FRESHNESS` quando a página oficial possui um mês mais novo ou um PDF ligado ainda não arquivado, e lista `WA HISTORY GAP` quando existe total mensal sem fonte ocupacional preservada. Fevereiro, abril e setembro de 2026 são lacunas já investigadas e documentadas; qualquer outro mês sem cobertura ocupacional é erro bloqueante. A atualização não deve ser commitada enquanto um novo aviso não for investigado.

## Auditoria obrigatória de todas as jurisdições

O extrator também confronta automaticamente:

| Fonte | Verificação de frescor |
|---|---|
| Federal | Data da rodada corrente na página versus data federal mais recente do dataset |
| ACT | Data da Canberra Matrix round e todos os PDFs anuais de rankings ligados na biblioteca |
| WA | Último mês dos totais, último PDF ocupacional, todos os PDFs ligados na página corrente e meses históricos com total sem fonte ocupacional |
| SA | Todos os artigos `invitations-issued` ligados pelo índice oficial versus o manifesto |
| TAS | Data da rodada ROI na página corrente versus data mais recente extraída |
| NSW, VIC, QLD e NT | Integridade e conteúdo mínimo dos snapshots oficiais monitorados; detalhe ocupacional permanece `NOT_PUBLISHED` enquanto não surgir uma tabela oficial |
| Todas | Existência local e SHA-256 de cada fonte marcada como válida no manifesto |

Qualquer divergência gera um aviso com o nome da jurisdição seguido de `FRESHNESS`. Não fazer commit nem publicar o dashboard enquanto houver aviso sem explicação no log.

## Regra de inclusão

Uma atualização só entra no dataset quando:

1. a fonte é oficial e termina em `.gov.au`;
2. o conteúdo original foi salvo localmente;
3. jurisdição, visto, período, métrica e nível ocupacional estão identificados;
4. o valor pode ser lido sem estimativa;
5. a URL e o SHA-256 da fonte ficam registrados;
6. totais agregados não são atribuídos artificialmente a profissões ou grupos.

Blogs, agentes, redes sociais e resumos comerciais não são fontes de dados do projeto.

## Definição canônica de rodada e data

Toda análise temporal deve partir de um evento oficial identificável. Uma rodada
comparável é identificada por jurisdição, visto, métrica, nível ocupacional,
stream/residência quando publicados e data oficial. Várias linhas ocupacionais na
mesma combinação pertencem à mesma rodada; não são várias rodadas.

- `YYYY-MM-DD` representa o dia oficial quando a fonte o informa;
- `YYYY-MM` representa o período oficial quando a fonte publica somente o mês;
- tabelas mensais de resumo federal não criam uma segunda rodada quando já existe
  a data exata correspondente;
- acumulados do program year, allocations, nominations recebidas e atualizações
  administrativas não entram no eixo de score nem no IAS;
- ausência de uma profissão só pode ser interpretada como ausência naquela rodada
  quando a fonte publica um universo ocupacional comparável; nos demais casos é
  `não conhecido`, nunca zero;
- resultados por Sub-major Group ou Unit Group não devem ser atribuídos
  automaticamente a todas as profissões descendentes.

Essa mesma identidade de rodada deve alimentar eixo temporal, Date Range, KPIs,
histórico, contagem de rodadas e IAS. Não criar uma regra de datas exclusiva para
um gráfico ou cartão.

## Como adicionar uma nova publicação

### 1. Arquivar a fonte

Salvar o HTML, PDF ou XLSX original na pasta da jurisdição correspondente em `dados/`. Não substituir silenciosamente uma publicação histórica por uma versão mais nova. Quando o endereço oficial reutilizar o mesmo nome, preservar uma cópia datada.

### 2. Atualizar o inventário e o manifesto

Adicionar a publicação a `dados/fontes/inventario-oficial.md` e a `dados/fontes/manifesto-validacao.csv`, registrando pelo menos:

- fonte e jurisdição;
- URL oficial;
- caminho do arquivo local;
- tipo e tamanho do conteúdo;
- status de validação;
- observação sobre o que a fonte publica.

Executar:

```powershell
python scripts/atualizar_manifesto_local.py
```

Esse passo reconcilia tamanho e SHA-256 com os bytes arquivados. Ele não substitui a validação humana da fonte.

### 3. Registrar a fonte no extrator

Atualizar `scripts/extrair_agregado.py` quando a nova publicação exigir um arquivo, tabela ou formato ainda não conhecido. Fontes recorrentes podem ter listas explícitas, como os arquivos da SA e os PDFs da WA.

Não adaptar silenciosamente uma tabela nova a uma regra antiga se as colunas ou o significado tiverem mudado.

### 4. Normalizar datas corretamente

Usar somente estas representações no dataset:

- `YYYY-MM-DD` para uma rodada com dia oficial;
- `YYYY-MM` quando a fonte publica apenas o mês;
- `YYYY-YY` para um total de program year.

Não converter program year em uma data inventada. Não deixar datas como números seriais do Excel. Quando uma tabela tiver datas em colunas, transformá-las em registros — uma linha por combinação de data, jurisdição, visto, ocupação/grupo e métrica.

### 5. Preservar notas e escopo

Notas de rodapé, stream, residência, applicant location, priority group e observações de coluna devem ser preservadas em `unidade_extra` ou em campos próprios. Elas não devem ser concatenadas ao valor numérico nem descartadas quando alteram o significado do resultado.

### 6. Gerar as saídas

Executar:

```powershell
python scripts/extrair_agregado.py
```

O processo deve atualizar em conjunto:

- `dados/agregado/vistos-de-convites.csv`;
- `dados/agregado/vistos-de-convites.json`;
- `analise/data.js`;
- `dados/agregado/extracao-log.md`.

Nunca editar apenas `analise/data.js`, pois isso faria o dashboard divergir dos downloads e do log.

### 7. Atualizar a hierarquia ANZSCO e os skill levels

O filtro global de hierarquia usa a referência oficial armazenada em
`dados/fontes/anzsco-2022-structure.xlsx`. Ela contém Major, Sub-major, Minor,
Unit group, profissões de seis dígitos e os respectivos skill levels.

Depois de substituir essa planilha por uma nova versão oficial validada, executar:

```powershell
python scripts/build_anzsco_hierarchy.py
```

Isso regenera `analise/anzsco-hierarchy.js`. O arquivo é derivado: não deve ser
editado manualmente. Conferir a versão da classificação antes de misturar códigos
novos com séries históricas. Resultados agregados ou sem código permanecem como
`Aggregate / not attributable`; não devem ser distribuídos artificialmente entre
grupos ou profissões.

## Verificações obrigatórias

Antes de publicar:

1. confirmar que não houve erro bloqueante no log;
2. comparar os totais principais com a tabela oficial;
3. conferir pelo menos uma profissão/grupo, uma data e um score de cada fonte nova;
4. confirmar que 189/491-family federais não foram misturados com 190/491 estaduais;
5. confirmar que allocation, nomination, invitation e visa grant continuam métricas separadas;
6. confirmar que totais federais não foram distribuídos entre profissões;
7. verificar duplicatas exatas e sobreposição entre total mensal, round datado e year-to-date;
8. abrir o dashboard local e testar filtros, Date Range, INV, OCC, IAS e links oficiais;
9. atualizar a data/descrição de cobertura no README quando necessário.

## Política para mudanças de formato ou regra

Se um governo alterar a página, a planilha, a classificação ANZSCO ou o significado de uma coluna:

- manter o arquivo antigo arquivado;
- criar uma nova regra de extração identificável;
- documentar a mudança no log;
- não reescrever resultados históricos sem justificativa;
- registrar qual versão de classificação foi usada;
- mostrar `Not published` ou `Not comparable` quando uma conversão segura não for possível.

## Fontes que devem ser monitoradas

- Home Affairs — SkillSelect invitation rounds: https://immi.homeaffairs.gov.au/visas/working-in-australia/skillselect/invitation-rounds
- Home Affairs — previous rounds: https://immi.homeaffairs.gov.au/visas/working-in-australia/skillselect/previous-rounds
- Home Affairs — state and territory nomination allocations: https://immi.homeaffairs.gov.au/what-we-do/state-and-territory-nomination-allocations
- ACT Migration: https://www.act.gov.au/migration/home
- WA Migration Services: https://migration.wa.gov.au/our-services-support/state-nominated-migration-program
- SA invitations-issued index: https://migration.sa.gov.au/news?category=invitations-issued

As datas e expectativas devem ser verificadas novamente no momento de cada atualização.
