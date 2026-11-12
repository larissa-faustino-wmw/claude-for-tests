# Campos do fechamento

Pelo [GUIA-JIRA-003](https://confluence.wmw.com.br/confluence/x/GwDdQQ) (v1) e pela [PQA-JIRA-000](https://confluence.wmw.com.br/confluence/pages/viewpage.action?pageId=1099595800) (labels), conferidos em 10/11/2026.

## Jira

| Campo | Na criação | No fechamento |
|---|---|---|
| Component/s | em branco | todas as classes criadas ou alteradas, incluindo o cenário |
| Fix Version/s | em branco | a versão em que foi liberado |
| Description | `Teste:` e `Link do Squash:` podem estar "a definir" | preenchidos |
| Labels | origem (`QA_ORIGIN_*`) | + construção (`QA_BUILD_AI` / `QA_BUILD_TESTER`), `QA_REVIEW_AI` quando houve revisão ou refatoração pela IA, `QA_BUG_FOUND` quando a automação encontrou defeito real |
| Original Estimate | o orçamento | não muda |
| Linked Issues | a atividade de origem | + Defects e Bugs achados |

Exemplo fechado: VENDAS-25282 — Component/s `ValidarAvisoVisitaAndamentoSugestaoSaidaTodasSituacoesTest`, Fix Version `9.068`, labels `QA_BUILD_AI` e `QA_ORIGIN_ISSUE`, descrição com o Teste e os dois links do Squash.

### Descrição (como fica)

```
Cenário: <nome do cenário>
Teste: <NomeDaClasseTest>
Cenário anterior: <link CT-LVP do Confluence ou N/A>
Baseado na atividade: <VENDAS-xxxxx ou N/A>
Baseado no cenário: <link do Squash ou N/A>
Link do Squash: <link do caso>
```

### Comentário de fechamento (modo Text)

```
h2. Fechamento da automação

||Item||Valor||
|Teste|{{<NomeDaClasseTest>}}|
|Caso no Squash|[<Reference>|<link>]|
|Revisão|<APROVADO / APROVADO COM OBSERVAÇÕES> — 3 rodadas passando|
|Horas orçadas (modelo antigo)|<n>h|
|Horas reais (Σ)|<hh:mm>|
|Redução|<nn,nn%>|
|Defeitos encontrados|[VENDAS-aaaaa|https://jira2.wmw.com.br/browse/VENDAS-aaaaa] ou nenhum|

*Classes:* {{<Classe1>}}, {{<Classe2>}}
```

A redução: `python scripts/calcular_reducao.py --analise <h> --codificacao <h> --reais <hh:mm>` da `orcamento-modelo-antigo` (a divisão análise/codificação está no comentário de orçamento; sem ela, passe o total em `--analise` e `0` em `--codificacao`). Sem Original Estimate: diga que a redução não pode ser calculada.

## Squash

O caso tem os campos de automação na API (`automated_test`, `automated_test_technology`, `automated_test_reference`, `scm_repository_url`) e o `status` (`WORK_IN_PROGRESS`, `UNDER_REVIEW`, `APPROVED`, `OBSOLETE`, `TO_BE_UPDATED`). O padrão do time para o fechamento ainda não está escrito; na primeira vez, proponha e confirme com o tester:

- **Status:** `APPROVED` (o caso corresponde ao teste revisado).
- **Nature / Type:** `Automatizado` / `TotalUiTest` (App), se o time usa esses valores para caso automatizado.
- **Referência do teste automatizado:** a classe (e o repositório), se o time usa o campo.

Registre a decisão confirmada aqui, para as próximas vezes.

## Conferir depois

Pelo MCP: `get_jira_issue` deve mostrar `components`, `fix_versions`, `labels`, status "Fechado" e resolução "Concluída". Pela API do Squash: o `status` do caso.
