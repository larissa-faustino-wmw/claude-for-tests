# totaluitest-codigo

Skill do Claude que **escreve e refatora testes automatizados do app Lavendere no framework TotalUiTest** (repositório `totaluitest`), no padrão novo do time: massa de dados em `@InvokeInit` com `ParametrosTestUtil`/`TabelasTestUtil`, JavaDoc com os links do Squash e do Jira, e comentários de Passo/Resultado Esperado. Junto com o código, entrega o cenário, o worklog e a lista de classes alteradas.

## Para que serve

- **Automatiza um cenário** do Squash ou do Confluence (CTxxx-Txxx, CT-LVP-x-y).
- **Refatora um teste legado**: migra o `.sql` para `@InvokeInit`, renomeia, documenta e corrige asserts e waits.
- **Monta massa de dados** de teste (parâmetros simples e JSON, inserts e updates).
- **Entrega quatro artefatos:** cenário (ou a conferência com o caso do Squash), código, texto do worklog em primeira pessoa e a lista de classes alteradas (que também serve para o Component/s da Test Automated).

## Quando usar

- "automatiza o cenário CT011-T030";
- "refatora o EmitirPedidoTributacaoPersonalizadaFecopTipoQuatroTest para o padrão novo";
- "monta a massa desse cenário";
- "escreve o teste da VENDAS-25597".

Para chamar direto: `/totaluitest-codigo`.

## O que você precisa ter

- **Claude Code com o repositório `totaluitest`** aberto ou ao lado. A skill lê as Pages e os utils para usar só métodos que existem, e acha um teste parecido para usar de molde. No claude.ai, sem o repositório, anexe a Page e um teste parecido.
- **MCP interno da WMW**: lê a Test Automated (links do Squash e do cenário anterior) e o documento CT-LVP no Confluence.
- **Opcional:** Claude in Chrome, para ler os passos do caso no Squash; Maven + JDK 8, para compilar.

## Como usar

1. **Peça o teste** com a chave da Test Automated, o link do caso no Squash ou os passos colados.
2. Se faltar o link do Squash ou da atividade, **a skill pergunta**: as duas linhas são obrigatórias no JavaDoc.
3. **Revise** o código, o cenário e as classes alteradas.
4. **Rode o teste** na sua máquina ou no Jenkins. Se algo falhar, mande o log: a skill corrige e reemite o worklog e a lista.
5. **Lance o worklog** e preencha o Component/s com a lista de classes.

## Regras que a skill segue

| Assunto | Regra |
|---|---|
| Login | `logar()` sem parâmetros no sucesso; `logar("SENHA", false)` + `waitOpening(WmwMessageBox.class)` nas exceções |
| Esperas | `waitOpening` depois de todo click que muda a tela; `waitValue(esperado, "id")` para valor que vem do banco; nada de `sleep` |
| Asserts | `assertEquals` com o valor concreto e mensagem do campo; string de item completa; `getMessage()` para mensagens do app |
| Comentários | `/* Passo N: */` e `/* Resultado Esperado N: */` multilinha, numerados em par |
| JavaDoc | título, `@author`, `@version`, Squash e Jira obrigatórios; Confluence quando houver cenário anterior |
| Datas | `DatasTestUtil` (`hoje()`, `hojeUi()`, `hojeMais(n)`), nunca data fixa |
| Parâmetro JSON | só funciona se o código estiver em `PARAMETROS_JSON` do `ParametrosTestUtil`; a skill confere e acrescenta |
| Código do app | nunca alterado para a automação; componente sem id → pedir `setID` ao dev |
| Encoding | `.java` em ISO-8859-1 com CRLF, conferido com `file -b` |

## Bom saber

- **Parâmetro JSON fora de `PARAMETROS_JSON`** é a armadilha mais silenciosa: com `Map`, nada é gravado; com `String`, o JSON inteiro é trocado e o app não lê o parâmetro (componentes somem e o teste cai em `TimeoutException`).
- A skill **não diz que o teste passou** sem ter rodado. A execução de UI é no seu ambiente.
- Para criar os casos no Squash, use a `gerador-de-testcases`; para orçar, a `orcamento-modelo-antigo` ou a `orcamento-refatoracao`; para entender uma falha, a `analise-logs-jenkins`.
- A skill não commita nem faz push sem você pedir.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `SKILL.md` | o fluxo: ler, mapear análogo, conferir métodos, escrever, encoding, compilar, entregar |
| `references/regras-codigo.md` | estrutura da classe, JavaDoc, comentários, waits, asserts, variáveis, métodos conferidos do `PedidoPage` |
| `references/massa-de-dados.md` | `@InvokeInit`, `ParametrosTestUtil`, `TabelasTestUtil`, `DatasTestUtil` e os erros comuns de massa |
| `references/entregas.md` | formato do cenário, do código, do worklog e da lista de classes |
| `references/contexto-sistema.md` | o que saber do Lavendere para testar (stacks, persistência, dependências externas) |

As assinaturas dos utils e das Pages foram conferidas no `totaluitest` (branch develop) em 10/11/2026.

## Instalação

Copie a pasta `totaluitest-codigo/` inteira, com a subpasta `references/`:

- **Claude Code**: em `~/.claude/skills/`, ou em `.claude/skills/` do projeto;
- **claude.ai**: suba a pasta como skill nas configurações de Skills.
