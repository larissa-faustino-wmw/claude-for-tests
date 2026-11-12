# Como fazer cada conferência

## Jira (MCP interno)

| O quê | Consulta |
|---|---|
| Subtasks da atividade | `parent = VENDAS-xxxxx` (Testing e Defects, com status e resolução) |
| Defects abertos | `parent = VENDAS-xxxxx AND issuetype = Defect AND resolution is EMPTY` |
| Bugs causados pela atividade | `project = VENDAS AND "Issue Cause" ~ "VENDAS-xxxxx"` |
| Testing em andamento do time (para conferir o padrão) | `project = VENDAS AND issuetype = Testing AND status = "In Progress"` |

Status no JQL em inglês: `Open` (Aberto), `In Progress` (Em Andamento), `Closed` (Fechado). Resolução no JQL: use `resolution is EMPTY` / `is not EMPTY` (o valor "Concluída" não funciona).

## Squash (API REST, só leitura)

1. Ache o requirement da atividade (Reference = `VENDAS-xxxxx`) e os casos ligados a ele.
2. No plano da sprint (Executions) ou da iteração: `https://squash.wmw.com.br/squash/api/rest/latest/iterations/<id>/test-plan?size=200`. Para cada item dos casos da atividade, o `execution_status` e as `executions` (quem, quando).
3. Execução sem comentário nem anexo: abra a execução (`…/api/rest/latest/executions/<id>`) para conferir a evidência.

Se não achar a iteração ou sprint da atividade, pergunte ao tester onde os casos foram executados.

## Git (reteste)

O que foi testado é o que vai para a `develop`? Compare a data do último commit da atividade com a data da última execução no Squash:

```
git -C projetos/<repo> log origin/main..origin/<branch da atividade> --no-merges --format="%h %ci %s" --grep="VENDAS-xxxxx" -1
```

A branch tem a chave no nome (`*VENDAS-xxxxx*`); repositórios: `lavenderepda`, `lavendereweb`, `lavenderecore` (os citados no comentário de branch do dev). Commit mais novo que a última execução: o reteste está desatualizado; diga o que o commit mudou (`git show --stat`) para o tester decidir se reexecuta.

Sem os repositórios clonados, marque a conferência como "não verificada" e diga por quê.
