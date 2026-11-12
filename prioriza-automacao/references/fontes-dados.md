# Fontes de dados

Consultas conferidas no Jira da WMW em 10/11/2026.

## Versão

| O quê | Como |
|---|---|
| Versões recentes (para perguntar qual) | `jira_release_ranking` |
| Resumo da versão | `jira_release_impact(version="9.068", project="VENDAS")`: `totals` (entregas, correções, Defects internos), `items_that_caused_problems` (regressão confirmada, com Root Cause), `features` (suspeita de regressão por feature). Inclui os patches por padrão. Leia o `how_to_read` |
| Atividades da versão | `search_jira_jql`: `project = VENDAS AND fixVersion in ("9.068", "9.068-1") AND issuetype in (Story, Bug)` (pagine com `start_at`) |
| Defects de uma atividade | `search_jira_jql`: `parent = VENDAS-xxxxx AND issuetype = Defect` |
| Bugs que uma atividade causou | `search_jira_jql`: `project = VENDAS AND "Issue Cause" ~ "VENDAS-xxxxx"` |
| Bugs com versão afetada | `search_jira_jql`: `project = VENDAS AND issuetype = Bug AND affectedVersion in ("9.068", "9.068-1")` |

Exemplo (9.068): 16 entregas, 66 correções, 44 Defects internos, 4 itens que causaram problema confirmado.

## Histórico da feature

| O quê | Como |
|---|---|
| Bugs por feature e tendência | `jira_feature_hotspots(days=180, project="VENDAS")` |
| Correções que voltaram | `jira_rework(days=180, project="VENDAS")` |
| Quem causou os problemas | `jira_problem_causes(days=180, project="VENDAS")` |
| Bugs de uma feature | `search_jira_jql`: `project = VENDAS AND issuetype in (Bug, Defect) AND "Feature" = "<Módulo > Funcionalidade>" AND created >= -180d` |

## Automação existente

| O quê | Como |
|---|---|
| Test Automated concluídas por feature | `jira_aggregate(jql='project = VENDAS AND issuetype = "Test Automated" AND resolution is not EMPTY', group_by="feature")` (o valor da resolução não é "Concluída" no JQL: use `is not EMPTY`) |
| Fila atual (board de automação) | `search_jira_jql`: `project = VENDAS AND issuetype = "Test Automated" AND resolution is EMPTY` |
| Testes do App | `projetos/totaluitest/src/test/java/br/com/wmw/lavenderepda/presentation/ui/test/<área>/` — conte `*Test.java` por pasta; os do padrão novo têm o link do Squash no JavaDoc |
| Testes da Web | `projetos/webuitest/src/test/java/` (ver `references/automacao-web.md`) |

Cobertura por feature em 11/2026 (para comparar): Estoque Padrão 45 automações; Tributação Personalizada 19; Novo Cliente 14; Agenda de Visitas 14; Emissão de Pedidos - Venda 5; Pedidos Pendentes, Desconto Diversos, Orçamentos, Títulos Financeiros e Condição de Pagamento 0.

## Plataforma (App ou Web)

O MCP não devolve o campo Environment e o filtro por ele no JQL não funciona. Deduza e marque como deduzida:

| Sinal | Plataforma |
|---|---|
| "aplicativo", "app", "PDA", "sincronizar", classes `…Form`, `…Window`, `TBLVP…` no Root Cause | App |
| "web", "tela de aprovação", classes `…Bean`, `.xhtml`, `TBLVW…`, "Oracle/PostgreSQL/SQL Server" | Web |
| os dois, ou cálculo que existe nas duas stacks | App e Web (dois cenários) |

Na dúvida, pergunte na avaliação. Para ler o campo de verdade, abra a atividade no Jira pelo Chrome.
