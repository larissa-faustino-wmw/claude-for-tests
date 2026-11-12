# Modelo da entrega (modo atividade)

## Impacto da VENDAS-xxxxx — <título>

**Mudança em uma frase:** <o que a atividade alterou, em termos de negócio>

**Código analisado**

| Repositório | Branch | Commits | Arquivos |
|---|---|---|---|
| lavenderepda | `origin/VENDAS-xxxxx` | 4 | 9 |
| lavenderecore | — (sem branch) | — | — |

Avisos, se houver: análise parcial (diff grande), branch não encontrada num repositório, só um lado alterado.

**Mapa de impacto**

| Alteração | Onde mais é usada | Fluxo do usuário |
|---|---|---|
| `PedidoService.calculaCashback` (regra do limite) | `CadPedidoForm`, `RelPedidoPdf`, `PedidoSync` | aba Cashback, totalizadores, PDF, envio do pedido |

**Side effects**

| # | Side effect | Risco | Evidência | Cobertura atual | Recomendação |
|---|---|---|---|---|---|
| 1 | PDF do pedido mostra o cashback antigo | Alto | `RelPedidoPdf.montaTotais` lê `vlCashbackTotal` calculado antes do ajuste | regressão fixa: "Emissão de PDF" (largo) | Automatizar |
| 2 | Replicação de pedido com cashback aplicado | Médio | `ReplicaPedidoService` copia o item sem recalcular | nenhuma | Virar caso |
| 3 | Mensagem de ajuste no App × Web | Baixo | só o App foi alterado; `lavenderecore` tem a mesma regra em `CashbackService` | — | Perguntar ao dev |

**Perguntas ao dev** (quando o código não deixa claro)

1. <pergunta com o arquivo e o método>

**Candidatos à regressão fixa:** <se houver, qual caso detalhar>

**Próximo passo:** gerar os casos aprovados com a `gerador-de-testcases` (entram no requirement VENDAS-xxxxx e na sprint); os de automação seguem para `orcamento-modelo-antigo` e `totaluitest-codigo`.

---

Regras:

- Cada side effect tem evidência (arquivo e método). Sem evidência, vai para "Perguntas ao dev".
- Ordene por risco.
- Prefira até ~8 side effects. Se houver mais, agrupe os de risco baixo numa linha ("observar de passagem: …").
- Nomes de classe e método em `código`; o side effect em si, em linguagem de usuário.
