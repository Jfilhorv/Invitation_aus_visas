# Metodologia e limites de comparabilidade

Auditoria atualizada em 12 de agosto de 2026.

## Escopo

O conjunto registra resultados de convites publicados por órgãos oficiais australianos. Ele não é uma lista de elegibilidade migratória atual e não deve ser interpretado como previsão de convite.

## Identidade ocupacional

- Códigos publicados diretamente pela fonte recebem `codigo_status=source`.
- Títulos sem código só recebem um código quando há correspondência textual exata e não ambígua no índice oficial ANZSCO 2022 do Australian Bureau of Statistics; esses casos recebem `codigo_status=abs_exact_title`.
- Correspondências aproximadas não são usadas. Casos não resolvidos permanecem com `codigo_status=missing`.
- `identidade_ocupacional` separa a classificação e o código. Registros sem classificação recebem identidade própria baseada no título publicado.
- `nivel_ocupacional` distingue major group, sub-major group, minor group, unit group e occupation. Níveis diferentes não devem ser tratados como a mesma série.

## Métricas

As métricas são mantidas separadas no dashboard:

- `pontos_minimos`: menor pontuação convidada em rodada SkillSelect;
- `matrix_score`: pontuação Canberra Matrix;
- `ultimo_eoi_pontos`: pontuação do último EOI convidado;
- `convites_emitidos`: convites efetivamente publicados para uma rodada ou período; totais por categoria só são somados quando as categorias são mutuamente exclusivas;
- `nomeacoes_recebidas`: nomeações efetivamente recebidas pelo Department of Home Affairs, por estado, visto e período de corte publicado;
- `alocacao_nomeacoes`: limite anual de nomeações disponibilizado a cada estado, por visto e ano-programa; não representa convites, pessoas ou vistos concedidos;
- contagens e totais agregados não entram nos gráficos de pontuação.

Médias, mínimos, máximos e frequências não combinam métricas diferentes.

## Dimensões preservadas

As séries do gráfico são separadas por jurisdição, subclasse de visto, métrica e qualificadores publicados em `unidade_extra`, incluindo onshore/offshore. Para o eixo horizontal, a distância representa o intervalo cronológico real entre as datas.

## Classificações

ANZSCO 2022 é usada como referência de normalização porque continua aparecendo em listas e instrumentos migratórios. OSCA 2024 substituiu ANZSCO como classificação estatística australiana geral, mas isso não converte automaticamente instrumentos migratórios ou resultados históricos para OSCA.

## Proveniência e validação

Cada linha mantém URL oficial, arquivo arquivado e SHA-256. O manifesto inclui as planilhas oficiais do ABS usadas na normalização. `validado=true` significa que o registro foi extraído de um arquivo oficial arquivado e reconciliado com o manifesto; não significa elegibilidade migratória atual.

Somente fontes hospedadas em domínios oficiais do governo australiano (`.gov.au`) podem alimentar o conjunto. Blogs, agentes, agregadores, redes sociais, cópias em arquivos externos e estimativas são rejeitados, mesmo quando parecem reproduzir uma tabela oficial.

Os totais federais consolidados de 2025–26 são empilhados em duas métricas independentes. A tabela de nomeações recebidas usa o corte oficial de 30 de junho de 2026; a tabela de alocações usa o ano-programa `2025-26`. Valores iguais entre elas não são somados e não permitem inferir quantidade de convites ou concessões de visto.

Na rodada ACT de 11 de junho de 2026, os totais de convites são a soma das categorias oficiais mutuamente exclusivas (Doctorate Streamlined, Small Business Owners e Critical Skill Occupations), separados por subclass 190/491. Em Tasmania, a declaração de que a alocação foi integralmente nomeada não é classificada como `convites_emitidos`.

Fontes de referência:

- https://immi.homeaffairs.gov.au/visas/working-in-australia/skillselect/invitation-rounds
- https://immi.homeaffairs.gov.au/visas/working-in-australia/skillselect/previous-rounds
- https://immi.homeaffairs.gov.au/what-we-do/state-and-territory-nomination-allocations
- https://www.abs.gov.au/statistics/classifications/anzsco-australian-and-new-zealand-standard-classification-occupations/2022
- https://www.abs.gov.au/statistics/classifications/osca-occupation-standard-classification-australia/latest-release
