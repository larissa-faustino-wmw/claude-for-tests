# Registro do orçamento no Jira

O MCP interno só lê. A gravação é pelo Claude in Chrome, na sessão do tester, em `https://jira2.wmw.com.br`.

## Preparação

1. Carregue as ferramentas numa chamada só:
   `ToolSearch select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__find,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__form_input`
2. `tabs_context_mcp` e abra uma **aba nova**.
3. Caiu na tela de login: peça para o tester entrar. **Nunca digite senha.**

## Atividade existente

1. Abra `https://jira2.wmw.com.br/browse/<CHAVE>`.
2. **Edit** → campo **Original Estimate** (seção Time Tracking). Formato do Jira: `24h`, `18h 30m`.
   - Se o campo já tem valor diferente, pare e pergunte antes de trocar (o tester já aprovou o orçamento, mas não a troca de um valor existente).
   - Não mexa em Remaining Estimate, Time Spent nem nos outros campos.
3. **Update** e confira na tela que o Original Estimate mostra o valor novo.
4. **Comment** com o texto abaixo (modo Text) e **Add**.

## Atividade nova

Prefira a skill `criar-task-jira` (tipo Test Automated): ela faz a busca por duplicidade, a rodada de dúvidas e a aprovação. Passe para ela o cenário, a Feature, o Test Case Type e o Original Estimate orçado.

Sem a `criar-task-jira`, crie pelo Chrome seguindo o [GUIA-JIRA-003](https://confluence.wmw.com.br/confluence/x/GwDdQQ):

1. Antes, procure se já existe (`project = VENDAS AND issuetype = "Test Automated" AND text ~ "<palavras do cenário>"`). Existindo, use a existente.
2. **Create** → Project `Vendas` → Issue Type `Test Automated`.
3. Campos obrigatórios: Priority (`Medium`), Summary (resumo do cenário, sem texto genérico), Features Involved (tags das funcionalidades), Test Case Type, Description (modelo abaixo), Feature, Customer (`WMW`), **Original Estimate** (o total orçado), Affects Version/s (versão em que foi sugerido), Labels (conforme a PQA-JIRA-000). Component/s, Due date, Remaining Estimate e Fix Version/s ficam em branco.
4. Mostre o formulário preenchido ao tester antes de clicar **Create**, uma vez só. Depois, comente o orçamento.

Description da Test Automated:

```
Cenário: <nome do cenário>
Teste: <classe do teste ou "a definir">
Cenário anterior: N/A
Baseado na atividade: <VENDAS-xxxxx ou N/A>
Baseado no cenário: <link do Squash ou N/A>
Link do Squash: <link do caso de teste ou "a definir">
```

Campo obrigatório que a skill não sabe preencher (versão, labels, tags): pergunte em vez de chutar.

## Comentário do orçamento

Modo Text do Jira:

```
h2. Orçamento no modelo antigo

||Coluna||Horas||
|Análise e configuração|<n>h|
|Codificação|<n>h|
|*Total (Original Estimate)*|*<n>h*|

*Porte:* <P/M/G/GG> — <motivo em uma frase>

*Análogos do histórico:* <VENDAS-xxxx (n h)>, <VENDAS-xxxx (n h)>

*Premissas:* <o que foi assumido>

*Detalhamento:* <etapa n h; etapa n h; ...>
```

Com horas reais já lançadas, acrescente: `*Horas reais (Σ Jira):* hh:mm — *Redução:* nn,nn%`.

## Depois

Devolva o link `https://jira2.wmw.com.br/browse/<CHAVE>` e diga o que foi gravado (Original Estimate e comentário). Se aparecer erro ao salvar, confira se a alteração entrou antes de repetir.
