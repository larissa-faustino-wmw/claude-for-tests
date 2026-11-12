# Registro do orçamento no Jira

O MCP interno só lê. A gravação é pelo Claude in Chrome, na sessão do tester, em `https://jira2.wmw.com.br`.

## Preparação

1. Carregue as ferramentas numa chamada só:
   `ToolSearch select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__find,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__form_input`
2. `tabs_context_mcp` e abra uma **aba nova**.
3. Caiu na tela de login: peça para o tester entrar. **Nunca digite senha.**

## Atividade existente

1. Abra `https://jira2.wmw.com.br/browse/<CHAVE>`.
2. **Edit** → campo **Original Estimate** (seção Time Tracking). Formato do Jira: `8h`, `12h 30m`.
   - Campo já com valor diferente: pare e pergunte antes de trocar.
   - Não mexa em Remaining Estimate, Time Spent nem nos outros campos.
3. **Update** e confira na tela que o Original Estimate mostra o valor novo.
4. **Comment** com o texto abaixo (modo Text) e **Add**.

## Atividade nova

Prefira a skill `criar-task-jira` (tipo Test Automated): ela busca duplicidade, tira as dúvidas e pede aprovação. Passe o cenário, a Feature, o Test Case Type `Refatoração`, o link do cenário anterior e o Original Estimate orçado.

Sem a `criar-task-jira`, crie pelo Chrome seguindo o [GUIA-JIRA-003](https://confluence.wmw.com.br/confluence/x/GwDdQQ):

1. Antes, procure se já existe: `project = VENDAS AND issuetype = "Test Automated" AND text ~ "<nome da classe ou CT-LVP-x-y>"`. Existindo, use a existente.
2. **Create** → Project `Vendas` → Issue Type `Test Automated`.
3. Campos obrigatórios: Priority (`Medium`), Summary (ex.: `Refatorar <Classe>Test: massa e padrão`), Features Involved, Test Case Type `Refatoração`, Description (modelo abaixo), Feature, Customer (`WMW`), **Original Estimate**, Affects Version/s, Labels (conforme a PQA-JIRA-000). Component/s, Due date, Remaining Estimate e Fix Version/s ficam em branco.
4. Mostre o formulário preenchido ao tester antes de clicar **Create**, uma vez só. Depois, comente o orçamento.

Description:

```
Cenário: <nome do cenário>
Teste: <classe do teste>
Cenário anterior: <link do CT-LVP-x-y no Confluence>
Baseado na atividade: <VENDAS-xxxxx ou N/A>
Baseado no cenário: N/A
Link do Squash: <link do caso de teste ou "a definir">
```

Campo obrigatório que a skill não sabe preencher (versão, labels, tags): pergunte em vez de chutar.

## Comentário do orçamento

Modo Text do Jira:

```
h2. Orçamento da refatoração no modelo antigo

||Coluna||Horas||
|Análise e configuração|<n>h|
|Codificação|<n>h|
|*Total (Original Estimate)*|*<n>h*|

*Tipo:* <R1/R2> — <motivo em uma frase>

*Tamanho:* <n> passos, <n> INSERT/UPDATE, <n> parâmetros (<n> JSON), <n> expressões de data

h2. Erros do cenário antigo

# <erro> (correção)
# <erro> (simples)

*Premissas:* <o que foi assumido>

*Detalhamento:* <componente n h; componente n h; ...>
```

Com horas reais já lançadas, acrescente: `*Horas reais (Σ Jira):* hh:mm — *Redução:* nn,nn%`.

Nomes de classe e trechos de código no comentário vão entre `{{` e `}}` (monoespaçado), para `_` e `*` não virarem formatação.

## Depois

Devolva o link `https://jira2.wmw.com.br/browse/<CHAVE>` e diga o que foi gravado. Se aparecer erro ao salvar, confira se a alteração entrou antes de repetir.
