# Modelo da entrega

## Automação sugerida — versão <9.xxx>

**A versão:** <n> entregas, <n> correções, <n> Defects internos, <n> itens com regressão confirmada (`jira_release_impact`).

**Cobertura das features da versão**

| Feature | Atividades na versão | Bugs 180 dias (tendência) | Automações hoje | Na fila |
|---|---:|---|---:|---:|
| Comercial > Liberações de Pedidos - Pedidos Pendentes | 3 | 42 (subindo) | 0 | 0 |
| Comercial > Emissão de Pedidos - Venda | 5 | 62 (subindo) | 5 | 1 |

**Sugestões** (em ordem de pontuação)

| # | Plat. | Cenário | Evidência | Pontuação | Porte |
|---|---|---|---|---|---|
| 1 | App | Pedido aprovado na Web chega ao App com o status da pendência de verba atualizado | VENDAS-24455 (Highest, produção): "não está atualizando os status da pendência que foi liberada" | **9,0** = 6 × 1,0 × 1,5 | M |
| 2 | Web | Tela de aprovação de desconto promocional lista os pedidos com os filtros laterais | VENDAS-22826, VENDAS-23791 (produção, Rasip) | **8,6** = 7 × 0,8 × 1,5 | G (primeira Page Web) |
| 3 | App | Recalcular o desconto por grupo de quantidade ao excluir item do pedido | VENDAS-24543, causado por VENDAS-24408 da versão (regressão confirmada) | **7,8** = … | M |

Cada linha, se precisar de detalhe, ganha embaixo: o fluxo em 2–4 passos e o resultado verificado (o valor que o teste confere).

**Descartados** (uma linha cada)
- VENDAS-24352 lentidão na adição de itens: desempenho, não automatizável no TotalUiTest.
- VENDAS-24190 integração da nota com o ERP: depende do ERP.
- <cenário>: já automatizado em `<Classe>Test` / já na fila em VENDAS-xxxxx.

**Para começar a Web:** <os 2–3 cenários Web de maior pontuação e a infraestrutura que exigem>.

**Próximo passo:**
> Avalie a lista: diga quais números aprovar, descartar ou ajustar. As aprovadas viram Test Automated no board de automação. Quer o orçamento das aprovadas antes de criar?

---

Depois da criação:

| # | Test Automated | Link |
|---|---|---|
| 1 | VENDAS-xxxxx | https://jira2.wmw.com.br/browse/VENDAS-xxxxx |
