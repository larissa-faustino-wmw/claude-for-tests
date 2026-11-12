# Métricas

Conferidas com os dados da 9.068 em 10/11/2026.

## A versão em números

De `jira_release_impact(version="9.068", project="VENDAS")` (patches inclusos), campo `totals`:

| Métrica | Campo | 9.068 |
|---|---|---|
| Data de liberação | `release_date` | 20/10/2026 |
| Entregas | `deliveries` (horas: `hours_deliveries`) | 16 (367,1 h) |
| Correções | `fixes_shipped` (horas: `hours_fixes`) | 66 (541,9 h) |
| Defects internos (pegos no teste) | `internal_defects` | 44 |
| Patches | `patches_released`, `patches` | 1 (9.068-1, 27/10) |

## Contenção (os dois números)

Quanto do que deu errado foi pego **antes** do cliente.

| Número | Fórmula | 9.068 |
|---|---|---|
| **Pela causa confirmada** | `internal_defects ÷ (internal_defects + problems_caused_confirmed)` | 44 ÷ (44 + 2) = **95,7%** |
| **Pela versão afetada** | `internal_defects ÷ (internal_defects + (problems − problems_legacy))` | 44 ÷ (44 + 3) = **93,6%** |

- **Causa confirmada:** bugs cujo Issue Cause cita uma entrega ou correção desta versão. É o mais preciso, mas só conta o que o time registrou. Mostre ao lado a cobertura: `problems_with_cause_pct` (9.068: 66,7%).
- **Versão afetada:** bugs com a versão afetada nesta versão, sem os marcados como Legado. Pega mais casos, mas "versão afetada" diz onde o cliente viu, não onde nasceu.
- `defects_caused_confirmed` (Defects em outras atividades causados por esta versão) **não** entram no denominador: foram pegos no teste.
- Explique os dois em uma linha cada na página. Se divergirem muito (mais de 10 pontos), diga por quê (Issue Cause pouco preenchido, bugs antigos vistos só agora).

## O que escapou

`items_that_caused_problems` (o que causou, quantos problemas e horas, exemplos com Root Cause) e os problemas com versão afetada (`search_jira_jql`: `project = VENDAS AND issuetype = Bug AND affectedVersion in ("<versão>", "<patches>")`). Para cada escape: chave, resumo, feature, prioridade, causa e Root Cause em uma frase.

## Esforço da Delivery

A Test de Delivery da versão: `project = VENDAS AND issuetype = Test AND fixVersion = "<versão>" AND summary ~ "Versão"` (título `Versão <versão> de <data>`). Da descrição, as métricas no formato `[Chave:valor]`:

| Métrica | 9.068 (VENDAS-24892) |
|---|---|
| Planejado | `DiasEstimados` 4,5 × `NrTesters` 5 × `HorasDiariasTesters` 7 = 157,5 h |
| Dias realizados | `DiasRealizados` 4,5 |
| Horas lançadas | `time_spent_h` 169,4 h (158 h na própria atividade) |
| Clientes testados | `ClientesTestados` Rasip |

Desvio = lançadas ÷ planejado − 1 (9.068: +7,6%).

## Onde doeu

- `features` do `jira_release_impact`: as com `regression_confirmed` ou `regression_suspect`, com `internal_defects`, `problems`, `hours_problems` e `worst_problems`.
- `jira_problem_causes(days=<desde a liberação anterior>)`: parcela legado × mudança recente.
- `jira_feature_hotspots(days=180)`: as features da versão que estão subindo.

## Automação

| Métrica | Como |
|---|---|
| Concluídas no período (da liberação anterior à desta) | `project = VENDAS AND issuetype = "Test Automated" AND resolved >= "<data anterior>" AND resolved <= "<data desta>"` |
| **Automação de verdade × limpeza** | é limpeza quando o Test Case Type é `Descontinuação`, ou quando não há horas lançadas e a atividade tem mais de 1 ano. Em 07/2026 fecharam 17 com idade média de 699 dias: parece limpeza, não 17 automações |
| Fila aberta | `... AND resolution is EMPTY` (10/11/2026: 314) |
| Horas orçadas × reais | Original Estimate (`estimate_h`) × `time_spent_h` das concluídas de verdade; a redução = 1 − reais ÷ orçadas |
| Bugs achados pela automação | label `QA_BUG_FOUND` nas concluídas do período |

## Execução no Squash

Campanhas na pasta VERSÕES (id 137) pela API: `https://squash.wmw.com.br/squash/api/rest/latest/campaign-folders/137/content?size=200`; a campanha da versão pelo nome; cada iteração em `iterations/<id>/test-plan`. Some os `execution_status`: SUCCESS, FAILURE, BLOCKED, UNTESTABLE, READY (não executado), RUNNING. Sem login no Squash: "sem dado".

## Tendência

As 4 versões anteriores (`jira_release_ranking`), com as mesmas contas: os dois números de contenção, Defects internos, escapes, horas de problema e desvio da Delivery. `jira_rework(days=180)`: `rework_pct`. Recalcule sempre: as versões antigas amadurecem (bugs chegam depois).
