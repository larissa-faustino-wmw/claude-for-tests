# Calibração da regressão fixa

A regressão fixa da Delivery fica no Squash, projeto VENDAS (id 6):

| Pasta | id | Casos (10/11/2026) |
|---|---|---|
| `/VENDAS/Delivery/00. Testes de Regressão App` | 7 | 61 |
| `/VENDAS/Delivery/00. Testes de Regressão Web` | 17 | 63 |

Os casos são um por assunto, espelhados entre App e Web (Reference `PEDIDO-03.19 - APP` / `- WEB` = Tributação), com passos amplos e, em geral, sem resultado esperado nem requirement. Exemplo, "Tributação" (PEDIDO-03.19 - APP): "Realizar novo pedido"; "Inserir um item… analisar os cálculos de tributação"; "Analisar os valores se estão calculando certo / validar com a carga antiga do cliente".

## Ler pelo Squash

Com o tester logado, a API REST responde na sessão do Chrome (navegar e ler com `get_page_text`). Só leitura.

- Pasta: `https://squash.wmw.com.br/squash/api/rest/latest/test-case-folders/<id>/content?size=500`
- Caso: `https://squash.wmw.com.br/squash/api/rest/latest/test-cases/<id>` (passos, `prerequisite`, `status`, `verified_requirements`)

## Passos

1. **Onde dá problema.** `jira_feature_hotspots` e `jira_problem_causes` no período (padrão 12 meses). Separe bugs de produção (SDLC phase `Production`) dos achados internos: produção pesa mais, porque passou pela regressão.
2. **O que a regressão cobre.** Liste os casos das duas pastas com os passos. Associe cada caso a uma ou mais Features do Jira pelo assunto (Tributação → `Contábil/Fiscal > Tributação - …`; Envio de dados Smartphone→Web → sincronização).
3. **Cruze.**

   | Situação | Sugestão |
   |---|---|
   | Feature com bugs e **sem caso** na regressão | caso novo, com os bugs como base dos passos |
   | Feature com bugs e caso **só amplo** | detalhar o caso: as verificações concretas que pegariam os bugs reais (valores, combinações de parâmetro) |
   | Bug de produção numa área que a regressão cobre | o caso não pegou: revisar os passos daquele caso |
   | Caso sem bug na área há muito tempo | enxugar, ou automatizar se for estável e repetitivo |

4. **Qualidade dos casos.** Conte casos sem resultado esperado, sem requirement e em `WORK_IN_PROGRESS` ou `UNDER_REVIEW`.

## Entrega

| # | Caso / área | Sugestão | Bugs que justificam |
|---|---|---|---|
| 1 | Tributação (PEDIDO-03.19) | detalhar: FECOP tipo 2 com ST; replicação para outro estado | VENDAS-xxxxx, VENDAS-yyyyy |

Mais o resumo da qualidade dos casos. A decisão e a edição no Squash são do time.
