# Levantamento

## Jira (MCP interno)

| O quê | Consulta |
|---|---|
| A agrupadora | `get_jira_issue(<chave>)`, com comentários (branch, projetos, scripts costumam estar neles) |
| Itens da agrupadora | `search_jira_jql`: `parent = <chave>` (Codings e Defects) e os links da agrupadora |
| Test do cliente (abertas e anteriores) | `project = VENDAS AND issuetype = Test AND Customer = "<cliente>" ORDER BY created DESC` |
| Bugs do cliente | `project = VENDAS AND issuetype in (Bug, Defect) AND Customer = "<cliente>" AND created >= -180d` |
| Features em que o cliente mais tem problema | `jira_aggregate` com o JQL acima e `group_by="feature"` |
| Bugs do cliente corrigidos recentemente | `... AND resolved >= -90d` |

O campo Customer vem como `Nome [código]` no MCP, e o JQL aceita o valor assim: `Customer = "Contabilista [2593]"` (conferido: 10 Test da Contabilista). Sem o código, procure o cliente com `text ~ "<nome>"` e copie o Customer do resultado.

Exemplos reais (10/11/2026):

- **Agrupadora de projeto:** VENDAS-25439 "Agrupadora Contabilista - Projeto Final Go Live (Prioridades)", com 6 subtasks (5 Codings e 1 Defect); rodadas anteriores VENDAS-22738 (9.062), VENDAS-23248 (9.066), VENDAS-24047 e VENDAS-25094 (bugs prioritários).
- **Agrupadora com branch própria:** VENDAS-22610 "Verba Politriz Junho 2026": branch `politriz_9.053`, projetos lavenderecore, lavenderedados, lavendereweb e lavenderepda, "POSSUI SCRIPT", e a dica de que a VENDAS-22616 tem scripts que facilitam os cenários. A descrição lista o que foi feito e o que **não** tem suporte — este último vai para "fora do escopo".
- **Funcionalidade para um cliente:** VENDAS-22573 "VENDAS-19174 REQ-Braile-…", VENDAS-22561 "VENDAS-19244 Homologar impressoras PMB".

## Squash (API REST, só leitura)

Com o tester logado no Chrome, navegar até a URL e ler com `get_page_text`.

| O quê | URL |
|---|---|
| Pasta HOMOLOGAÇÕES (campanhas e subpastas) | `https://squash.wmw.com.br/squash/api/rest/latest/campaign-folders/107/content?size=200` |
| Uma campanha (iterações) | `…/api/rest/latest/campaigns/<id>` |
| Plano de teste de uma iteração (casos e status de execução) | `…/api/rest/latest/iterations/<id>/test-plan?size=200` |
| Casos de uma pasta da biblioteca | `…/api/rest/latest/test-case-folders/<id>/content?size=500` |

Campanha anterior do cliente: procure pelo nome do cliente nas campanhas e subpastas da HOMOLOGAÇÕES. Itens com status `FAILURE`, `BLOCKED`, `UNTESTABLE` ou `READY` (não executado) nas homologações anteriores são candidatos a reconferir.

## Base do cliente

A homologação roda na base do próprio cliente (as bases de teste ficam no servidor Docker 10.1.1.69). A skill **não guarda nem digita senha** e **só executa SELECT**.

Como acessar, em ordem:

1. Se o workspace já tem uma conexão configurada para a base do cliente (arquivo de configuração local do tester), use-a, só leitura.
2. Senão, entregue as consultas ao tester e peça que cole o resultado.

Consultas úteis:

```sql
-- App: parâmetros ligados que tocam o escopo (troque a lista pelos códigos das atividades)
SELECT CDPARAMETRO, VLPARAMETRO FROM TBLVPVALORPARAMETRO WHERE CDPARAMETRO IN (<códigos>);
```

- Web: o parâmetro mora na tabela do domain `ConfigParametro` do `lavenderecore` (`@TableName("TBLVWCONFIGPARAMETRO")`); confira as colunas na classe antes de montar a consulta.
- Os códigos dos parâmetros saem das atividades (PRM-XXXX citado), do código alterado (`LavenderePdaConfig`, `ConfigParametro`) e dos CSUs do Confluence.
- Para a massa: consultas de contagem (empresas, representantes, tipos de pedido, tabelas de preço, clientes na condição exigida) — o suficiente para escolher a massa dos cenários, sem trazer dados pessoais para o chat.

**Dados do cliente não vão para o Squash.** Nos casos, use descrições e códigos internos ("empresa 1, representante 100, cliente com limite estourado"), nunca CNPJ, nome de pessoa ou contato.
