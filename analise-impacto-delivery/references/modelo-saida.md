# Modelo da entrega (modo versão)

## Riscos da versão <9.xxx>

**Escopo:** `origin/main..origin/release` em <data>.

| Repositório | Commits | Atividades | Commits sem atividade |
|---|---|---|---|
| lavenderepda | 112 | 41 | 5 |
| lavenderecore | 48 | 22 | 1 |
| lavendereweb | 30 | 15 | 0 |

**Divergências com o fixVersion**
- No código e fora do fixVersion: VENDAS-xxxxx (<título>)
- No fixVersion sem commit: VENDAS-yyyyy (<título>) — sem código ou não entrou?

**Riscos**

| # | Tipo | Achado | Risco | Evidência | Onde aprofundar no teste |
|---|---|---|---|---|---|
| 1 | Sobreposição | VENDAS-111 e VENDAS-222 alteram `PedidoService.calculaTotal` | Alto | commits `a1b2c3`, `d4e5f6` | pedido com desconto de política comercial e cashback juntos |
| 2 | Sem atividade | commit "ajuste arredondamento" em `ItemPedidoService` | Médio | `9f8e7d` | totalizadores com 3 casas decimais |
| 3 | Correção da Delivery | correção do Defect VENDAS-333 em `SyncPedido` | Médio | `c0ffee` | envio de pedido com item bonificado |
| 4 | Mudou depois de testada | VENDAS-444 com commit após a liberação do QA | Baixo | `abc123` | reteste rápido da atividade |

**Perguntas ao facilitador ou ao dev**
1. <pergunta com commit e arquivo>

**Próximo passo:** os riscos aprovados viram casos do Test de Delivery com a `gerador-de-testcases`.

---

Regras:
- Ordene por risco; agrupe os baixos numa linha.
- Evidência sempre (commit e arquivo, e o método quando for regra).
- O achado em linguagem de quem testa; classes e métodos em `código`.
