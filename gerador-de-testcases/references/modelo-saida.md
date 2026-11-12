# Modelo da entrega para aprovação

A resposta segue esta ordem. Alertas (Story sem critérios, Squash sem acesso, numeração pendente) vão **no topo**, antes do Contexto.

## 1. Contexto

Duas a quatro frases: o que a atividade muda, a plataforma (LVP/LVW), os parâmetros envolvidos e as páginas do Confluence consultadas.

## 2. Matriz de cenários

| Reference | Nome do cenário | Descrição funcional | Origem |
|---|---|---|---|
| COMISSAO-LVP-015 | Comissão por grupo com desconto no item | valida o percentual de comissão recalculado ao aplicar desconto | Critério 2 |
| COMISSAO-LVP-016 | Alterar a tabela de preço com itens já inseridos | usuário troca a tabela depois de inserir itens; comissão deve recalcular | Erro comum: voltar e alterar |

A coluna **Origem** diz de onde veio o cenário: o critério de aceite, o bug, o Defect da subtask, ou o erro comum (`references/erros-comuns.md`). Ela só aparece no chat; não vai para o Squash.

## 3. Cenários

Para cada cenário:

### COMISSAO-LVP-015 – Comissão por grupo com desconto no item

| Campo | Valor |
|---|---|
| Reference | COMISSAO-LVP-015 |
| Pasta no Squash | VENDAS / Comissão |
| Label | DEV_TESTS *(só se a atividade tiver a label; senão, omita a linha)* |
| Weight | High |
| Nature | Regra de Negócio |
| Type | Aceitação |

**Pré-requisitos**
- Parâmetros: `PRM-XXXX` = "S"; …
- Massa: cliente "Cliente Teste Comissão", produto "Produto Grupo A" com preço "100,00"…
- Estresse do cálculo, quando houver: valor com arredondamento, valor zero, limite.

**Observações e riscos**
- Divergência entre Confluence e Jira (com as URLs) para o QA confirmar.
- Dependências (outra funcionalidade, sincronização, carga).
- Páginas do Confluence usadas.

**Clientes conhecidos que usam a funcionalidade**
- Customer da atividade do Jira. Se vazio: "Não informado na atividade".

**Passos**

| # | Ação | Resultado esperado |
|---|---|---|
| 1 | Acessar o menu Pedidos e tocar em "Novo pedido" | O sistema abre a seleção de cliente |
| 2 | Selecionar o cliente "Cliente Teste Comissão" | O sistema abre a capa do pedido com a tabela "Tabela 01" |
| 3 | Inserir o item "Produto Grupo A" com quantidade "10" e desconto "5%" | O sistema exibe o total do item de R$ 950,00 (10 × 100,00 − 5%) e a comissão de R$ 28,50 (3% de 950,00) |
| 4 | Chamar o caso PERSISTENCIA-001 | Pedido gravado no App, sincronizado e igual na Web |

## 4. Fechamento

> Pasta no Squash: `VENDAS / Comissão`. Posso cadastrar estes N casos no Squash?

## Como cada parte vai para o Squash

| Na entrega | No Squash |
|---|---|
| Título sem a Reference | Name |
| Reference | Reference |
| Weight, Nature, Type | campos da aba de informações |
| Label | o campo de label/tag do caso, se existir na tela |
| Pré-requisitos | Prerequisite (se a tela tiver) ou o início da Description |
| Contexto, Observações e riscos, Clientes | Description |
| Passos | Steps: um passo por linha, Action e Expected result |
| "Chamar o caso PERSISTENCIA-001" | passo do tipo Call test case apontando para o 3463 |
