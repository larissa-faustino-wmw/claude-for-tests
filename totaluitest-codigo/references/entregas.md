# Formato das entregas

## 1. Cenário de teste

Tabela com um passo por linha, na mesma numeração dos comentários do código:

| # | Passo | Resultado esperado |
|---|---|---|
| 1 | Efetuar login no App, acessar Pedidos, iniciar um novo pedido e selecionar o cliente "CLIENTE PJ" | A capa do pedido abre com o cliente "CLIENTE PJ" e a tabela de preço "TABELA 01" |
| 2 | Inserir o item "10" com quantidade "5" | O item aparece na lista como "10 - AGUA MINERAL COM GAS 1,55,00 itens - R$3,70R$ 18,50" |

Pré-requisitos (parâmetros e massa) antes da tabela, em lista. O cenário segue o que o código faz: se o código valida um campo, o resultado esperado cita o campo e o valor.

**Caso já existe no Squash**: em vez de reescrever, liste as diferenças entre o caso e o código (passo que o código não cobre, validação a mais, valor diferente) para o tester ajustar um ou outro. Para criar ou atualizar casos no Squash, use a skill `gerador-de-testcases`.

## 2. Código

A classe completa, pronta para gravar, mais os trechos de outras classes alteradas (método novo na Page, parâmetro acrescentado no `ParametrosTestUtil`). Método novo em Page tem um comentário `//` dizendo por que foi criado.

## 3. Worklog do Jira

Texto para o tester lançar no worklog da atividade:

- **primeira pessoa**, na voz do tester (pode citar o apoio do Claude: "com apoio do Claude");
- o que foi feito na criação ou refatoração, com as justificativas (ex.: a regra do app que embasou um assert, o motivo de um wait);
- correções feitas depois (erro na execução, encoding, formato de comentário), com o motivo;
- frases diretas, rótulos com dois-pontos, sem emoji. Se a skill de estilo de escrita do tester estiver instalada, siga-a.

Exemplo:

```
Criação do cenário CT011-T030 com apoio do Claude.
Massa: parâmetros 970 e 924 configurados no @InvokeInit, tributação dos produtos 10 e 2 inseridas na classe.
Validações: IBS e CBS por item e total do pedido, conforme o cálculo do TributacaoService (base sem IPI).
Ajuste: incluído o parâmetro 1795 na lista PARAMETROS_JSON, que não estava cadastrado.
```

## 4. Classes alteradas

Um arquivo por linha, caminho a partir de `src/test/java` e a ação entre parênteses:

```
- br/com/wmw/lavenderepda/presentation/ui/test/cliente/atualizacao/ValidarAtualizacaoClienteTest.java (alterada: cenário reescrito e massa no @InvokeInit)
- br/com/wmw/lavenderepda/presentation/ui/page/core/MenuPrincipalPage.java (alterada: métodos novos clickBtTrocarEmpresaRep e trocarRepresentante)
- br/com/wmw/lavenderepda/presentation/ui/base/ParametrosTestUtil.java (alterada: parâmetro 1795 em PARAMETROS_JSON)
- br/com/wmw/lavenderepda/presentation/ui/test/cliente/atualizacao/AtualizacaoDeClienteTest.sql (removida)
```

Inclua testes, Pages, utils, `.sql`/`.ddl` e os legados (`_old`) afetados. Essa lista também serve para o campo Component/s da Test Automated (as classes criadas ou alteradas).
