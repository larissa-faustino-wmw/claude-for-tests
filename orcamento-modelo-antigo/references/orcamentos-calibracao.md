# Orçamentos já feitos (régua de calibração)

Os primeiros orçamentos do comparativo modelo antigo × modelo com IA (VENDAS-20462 a VENDAS-20912, 2026). Use-os para manter a régua coerente: um cenário parecido com um destes deve ter um orçamento parecido, ou uma justificativa para a diferença.

Horas reais = Σ Time Spent no Jira (atividade + subtasks), conferido em 01/10/2026.

| # | Atividade | Cenário | Análise e config. | Codificação | Orçado | Reais (Σ Jira) | % Redução | Bug achado |
|---|---|---|---|---|---|---|---|---|
| 1 | VENDAS-20462 | CT011-T027 Tributação Personalizada CBS | 12 | 12 | 24 h | 4:02 | 83,19% | — |
| 2 | VENDAS-20473 | CT025-T037 Bloqueio de bonificação quando venda+bonif excede estoque | 16 | 24 | 40 h | 4:15 | 89,38% | VENDAS-19974 |
| 3 | VENDAS-20474 | CT025-T038 Item bonificado dentro do limite de estoque | 12 | 12 | 24 h | 2:31 | 89,51% | — |
| 4 | VENDAS-20475 | CT025-T039 Bloqueio na edição de item bonificado extrapolando estoque | 12 | 12 | 24 h | 4:19 | 82,01% | — |
| 5 | VENDAS-20507 | CT025-T040 Estoque na replicação de pedido com item bonificado | 12 | 12 | 24 h | 0:41 | 97,15% | — |
| 6 | VENDAS-20519 | CT025-T041 Baixa de estoque após venda e bonificação do carrinho | 12 | 12 | 24 h | 3:12 | 86,67% | VENDAS-20511 |
| 7 | VENDAS-20527 | CT001-T001 Login com credenciais válidas (Refatoração) | 6 | 16 | 22 h | 6:18 | 71,36% | — |
| 8 | VENDAS-20542 | CT001-T002 Bloqueio de login com credenciais inválidas (Refatoração) | 4 | 4 | 8 h | 1:27 | 81,88% | — |
| 9 | VENDAS-20841 | CT006-T001 Fluxo básico do módulo de pagamentos | 2 | 6 | 8 h | — | — | — |
| 10 | VENDAS-20911 | CT006-T002 Múltiplos pagamentos com tipos diferentes | 2 | 6 | 8 h | — | — | VENDAS-20949 |
| 11 | VENDAS-20912 | CT006-T003 Pagamento vinculado a título financeiro | 4 | 12 | 16 h | — | — | VENDAS-20914, VENDAS-20933, VENDAS-20938 |

## Observações para manter a régua coerente

- Pedido com uma regra de estoque, bonificação ou tributo foi orçado em **24 h (12 + 12)**, porte M alto. Histórico 2024 de Estoque Padrão: mediana 19,8 h. Coerente.
- O caso mais complexo de estoque (T037, soma venda + bonificação) foi orçado em **40 h**, porte G.
- **Ponto de atenção:** CT001-T001 (login válido) foi orçado em 22 h, mas no Jira os logins antigos levaram 1,5 h (VENDAS-4647) e 4,8 h (VENDAS-4649). Um orçamento assim só se sustenta com o escopo maior escrito na justificativa.
- Pagamentos (CT006) não tem análogo no histórico: os dois primeiros foram orçados como porte P e o terceiro como M baixo.
- Bugs encontrados durante a construção com IA são um ganho à parte. Vale citá-los, mas não entram na conta de horas.
- VENDAS-20507 tem só 10 min lançados na própria atividade; confira se faltou lançamento antes de usá-la como exemplo de redução.

## Orçamentos mais novos

Os orçamentos feitos depois desta tabela estão no próprio Jira, no Original Estimate das Test Automated do modelo com IA. Para calibrar com eles:

```
project = VENDAS AND issuetype = "Test Automated" AND created >= 2026-03-01 AND originalEstimate is not EMPTY ORDER BY created DESC
```

Leia o Original Estimate (`estimate_h`) e o comentário de orçamento de cada uma (com a divisão análise × codificação e o porte).
