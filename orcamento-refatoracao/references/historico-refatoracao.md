# Histórico de refatorações (export Jira, Test Automated, Test Case Type = Refatoração)

## Modelo antigo (antes de 03/2026)

| Chave | Ano | Horas | Status | Comparável? | Resumo |
|---|---|---|---|---|---|
| VENDAS-10832 | 2024 | 10,0 | Closed | **Sim** | Refatoração de cenários por mudança de regra (VENDAS-9140): atualizar projeto e base, subir ambiente, ajustar script, validar com o dev, merge |
| VENDAS-13088 | 2025 | 6,0 | Options (não concluída) | Parcial | Refatoração do cenário 4.11 (ReceitaWS/Sintegra) após mudança de regra; horas incompletas |
| VENDAS-11461 | 2024 | 0,5 | Closed | Não (é ajuste) | Ajuste de id e valor do item após mudança de estrutura |
| VENDAS-8711 | 2024 | 6,1 | Closed | Não | Correção nas classes de múltipla inserção (framework) |
| VENDAS-9194 | 2024 | 3,8 | Options | Não | Melhoria no TotalUiTest (framework) |
| VENDAS-4384 | 2023 | 19,6 | Closed | Não | Suporte ao componente de múltipla inserção no TotalUiTest (framework) |
| VENDAS-943 | 2022 | 39,3 | Closed | Não | Refatoração do código-fonte legado (Pages) |
| VENDAS-701 | 2022 | 7,0 | Closed | Não | Atividades diversas |

Conclusão: só VENDAS-10832 (10 h) e, parcialmente, VENDAS-13088 (6 h) são refatorações de cenário. Use-as como faixa de conferência (6–10 h), não como base estatística.

## Modelo novo com IA (03/2026 em diante) — horas reais

| Chave | Cenário | Cenário anterior (Confluence) | Σ Time Spent | Orçado | Observação |
|---|---|---|---|---|---|
| VENDAS-20503 | CT032-T031 Bloqueio de fechamento com produto sem estoque | CT-LVP-25-31 | 2:06 | — | Corrigiu idPedido não utilizado (R2) |
| VENDAS-20527 | CT001-T001 Login com credenciais válidas | CT-LVP-22-1 | 6:18 | 22 h (6 + 16) | Worklog: "identificado problema no cenário" (R2) |
| VENDAS-20542 | CT001-T002 Bloqueio de login com credenciais inválidas | CT-LVP-22-2 | 1:27 | 8 h (4 + 4) | R1 |
| VENDAS-20762 | CT029-T009 Busca de endereço por CEP no novo cliente | CT-LVP-4-8 | 0:21 | — | Lançado como ajuste de cenário |

Observação sobre o CT001-T001: 22 h está acima da faixa R2 pequena desta skill (R1 pequena 6–9 h + 2–8 h = 8–17 h). Se mantido, a justificativa precisa descrever o que foi corrigido no cenário.

## Refatorações mais novas (ao vivo)

As refatorações do modelo com IA estão no Jira, com o orçamento no Original Estimate e o detalhamento no comentário de orçamento. Para calibrar com elas:

```
project = VENDAS AND issuetype = "Test Automated" AND "Test Case Type" = "Refatoração" AND created >= 2026-03-01 AND originalEstimate is not EMPTY ORDER BY created DESC
```

Uma refatoração parecida (mesmo tamanho de massa, mesmo tipo R1/R2) deve ter orçamento parecido, ou a justificativa diz por que não.
