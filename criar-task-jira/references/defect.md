# Defect — subtask de bug

**Guia:** [GUIA-JIRA-002 - Como criar subtask de defect no Jira](https://confluence.wmw.com.br/confluence/x/AgA-QQ) (conferido na versão 12, em 10/11/2026). Se o guia mudar, atualize este arquivo.

Bug encontrado ao testar uma atividade (Story ou Bug). É criado como **subtask da atividade pai**: na pai, **More → Create sub-task**, Issue Type `Defect`.

## Verificações antes de abrir (do guia)

1. Parâmetros relacionados ao problema e se houve alteração recente nos valores.
2. Documentação do processo, funcionalidade ou parâmetro.
3. Se o mesmo problema ocorre na `develop`.
4. Se não é uma melhoria não prevista em documento (aí não é Defect: conversar com o líder sobre Story ou Suggestion).

## O que já existe (antes de perguntar)

Além da busca por palavras-chave do `SKILL.md` (que pega o mesmo problema em outra atividade pai ou num Bug solto), leia as subtasks da pai (`parent = <CHAVE>`): o Summary de todas e a Description das que parecerem próximas. Problema já reportado, mesmo com outras palavras ou em outra tela com a mesma causa: não crie, sugira comentar na existente.

## O que perguntar (só o que faltar)

- **Develop**: se foi verificado e o resultado. **Exceção:** na homologação de uma versão nova, cuja funcionalidade ainda não chegou na develop, não pergunte; registre na Descrição que a funcionalidade ainda não existe na develop. Na dúvida se é esse o caso, pergunte isso.
- **Parâmetros e documentação**: quando o bug parecer depender de regra, cálculo ou parâmetro (PRM-XXXX).
- **Phase**: `Manual testing` ou `Automated testing`. Nunca assuma.
- **Environment**: `Web`, `App` e/ou `Other`. Se os prints indicarem, proponha.
- **Referências abertas**: expressões que um dev fora da conversa não entenderia ("a regra que falamos", "aquele cliente").
- **Massa de dados**, só quando o bug depende dela: empresa (quando há mais de uma na base) e representante; conforme o bug, itens, tabela de preços, frete, condição de pagamento, tipo de pedido.
- **Resultado esperado**, se não veio. Se o tester não souber, escreva uma proposta "(sugestão do QA, validar com PO)".
- **Evidências**: em erro ou travamento sem log, se existe log ou vídeo.

## Campos

| # | Campo | Valor | Perguntar? |
|---|---|---|---|
| 1 | Issue Type | `Defect` | não |
| 2 | Summary | título no padrão `Tela - descrição curta` | não |
| 3 | Reporter | o QA logado (já vem preenchido) | não |
| 4 | Assignee | `Automatic`; o dev, só se o tester disser que alinhou com ele | não |
| 5 | Priority | `Medium`. Subir (sugestão) se bloqueia o fluxo, perde dados ou afeta saldo/financeiro — ofereça na rodada | não |
| 6 | Original/Remaining Estimate | em branco | não |
| 7 | Phase | `Manual testing` / `Automated testing` | **sim, se não veio** |
| 8 | SDLC phase | `Development` (testando a demanda antes de ir para a develop ou para versão/hotfix), `Delivery` (no processo de delivery da versão), `Homologation` (homologação do sistema/funcionalidade), `Production` (cliente usando a versão). Deduza do contexto da pai; pergunte só se não der | só se não der para deduzir |
| 9 | Environment | `Web` / `App` / `Other` (múltipla) | **sim, se não veio** |
| 10 | Description | modelo abaixo | — |
| 11 | Issue Cause | só quando a causa já é conhecida. Hipótese não vai aqui | não |
| 12 | Labels | (sugestão) `BUG_LEGADO` quando o comportamento já existia antes da pai e o tester confirmar | ofereça na rodada |
| 13 | Attachment | prints, logs, vídeo | — |
| 14 | Linked Issues | atividades relacionadas que surgiram no contexto | não |

**Phase x SDLC phase** são campos diferentes: Phase é *como* achou (manual ou automatizado); SDLC phase é *em que etapa*.

## Modelo de descrição

Cinco seções, cada título em Heading 2, nesta ordem:

```
h2. Descrição

<impacto em uma frase; depois o detalhe. Mensagem de erro literal em Paragraph quote. Parâmetros e referência da regra. Hipótese marcada como "Observação para análise (hipótese do QA, não confirmada no código)".>

h2. Passos para reproduzir

<empresa e representante, quando aplicável, e o contexto (massa)>

# <passo no imperativo> (anexo 01)
# <passo>

h2. Resultado atual

<só o fato observado. Em bug de valores, tabela reportado x esperado x diferença.>

h2. Resultado esperado

<o que o tester informou, ou a proposta marcada como sugestão>

h2. Backup/Carga disponível

< anexar carga >
```

**Backup/Carga:** bug só no Web → `< anexar dados de conexão da base >`; no App/PDA → `< anexar carga >`; nos dois → os dois. Não pergunte sobre a carga; lembre o tester de trocar o espaço reservado na entrega.

## Exemplo

Relato: "Os totalizadores não batem após a aplicação do cashback. Valor do pedido: 4800,00. Cupom com 7777,77 (só dá para aplicar 4799,99 por causa da regra que falamos). Cashback total: 138304,73. Depois: pedido 0,01, cashback aplicado 4799,99, total 135326,95, que é 138304,73 - 2977,78. O correto não seria 138304,73 - 4799,99 = 133504,74?" + 4 prints do App, atividade pai informada.

Rodada de esclarecimento:

> Antes de montar a atividade, preciso de alguns pontos:
> 1. Foi verificado na develop? O problema também ocorre lá?
> 2. Phase: teste manual ou automatizado?
> 3. Environment: pelos prints é App, confirma?
> 4. Qual é "a regra que falamos" do limite do cashback, e qual a referência (story, documento ou parâmetro)?
> 5. Empresa e representante do pedido, e os itens e a tabela de preços do pedido de R$ 4.800,00?
>
> Sugestões antes de montar: testar o cashback com um valor dentro do limite (sem ajuste) para ver se o total bate; e, se o Cashback total alimenta o saldo real do cliente, avaliar subir a Priority.

Título: `Cashback do pedido - Cashback total incorreto após ajuste automático do valor aplicado`

Descrição (modo Text):

```
h2. Descrição

Na aba Cashback do Pedido (App), ao aplicar um cupom com valor acima do permitido, o sistema ajusta o valor e exibe a mensagem:

bq. O valor do cashback foi ajustado para R$4.799,99, o maior valor que pode ser distribuído entre os itens do pedido.

Após o ajuste, Valor do pedido e Cashback aplicado ficam corretos, mas o Cashback total é reduzido em R$ 2.977,78 em vez de R$ 4.799,99. Também ocorre na develop.

Observação para análise (hipótese do QA, não confirmada no código): 2.977,78 = 7.777,77 - 4.799,99, ou seja, o total parece ser reduzido pelo valor informado e devolvido pelo valor aplicado, quando deveria ser reduzido apenas pelo valor aplicado.

h2. Passos para reproduzir

Empresa 01, representante 100. Pedido de R$ 4.800,00. Cashback total inicial: R$ 138.304,73.

# Abrir o pedido e acessar a aba Cashback (anexo 01)
# Selecionar o cupom T23873.06, com valor disponível R$ 7.777,77 (anexo 02)
# Tocar em "Aplicar Cashback"
# Ler a mensagem de ajuste e tocar em OK (anexo 03)
# Conferir os totalizadores no rodapé (anexo 04)

h2. Resultado atual

||Campo||Atual||Esperado||Diferença||
|Valor do pedido|0,01|0,01|0,00|
|Cashback aplicado|4.799,99|4.799,99|0,00|
|Cashback total|135.326,95|133.504,74|1.822,21|

h2. Resultado esperado

Cashback total de R$ 133.504,74 (138.304,73 - 4.799,99), reduzido pelo valor efetivamente aplicado.

h2. Backup/Carga disponível

< anexar carga >
```

Campos: Defect · Assignee Automatic · Priority Medium · Phase Manual testing · SDLC phase Development · Environment App · Issue Cause, Labels e Linked Issues em branco · anexos `01-cashback-antes-de-aplicar.png`, `02-cupom-selecionado.png`, `03-mensagem-de-ajuste.png`, `04-totalizadores-apos-ajuste.png`.
