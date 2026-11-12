# gerador-de-testcases

Skill do Claude que **gera os cenários de teste de uma atividade do Jira e cadastra os casos no Squash TM**. Ela lê a Story ou o Bug, pesquisa a documentação no Confluence, monta os cenários pensando no que o usuário real faz, mostra tudo para você aprovar e cadastra no Squash pelo Chrome, devolvendo o link de cada caso.

## Para que serve

- **Cobre a atividade inteira**: todos os critérios de aceite da Story, ou o fluxo completo que o usuário fazia quando o Bug apareceu (não só a correção).
- **Pensa além do que está escrito**: inclui os erros que o desenvolvedor costuma esquecer, como voltar uma tela e alterar algo, clicar duas vezes em salvar, sair sem salvar, ficar sem conexão, valor no limite exato, parâmetro desligado, ou valor da tela diferente do PDF.
- **Usa a documentação**: pesquisa no Confluence por padrão, usa parâmetros, mensagens e regras nos passos, e aponta divergências entre Confluence e Jira.
- **Define a Reference certa**: `<PREFIXO>-LVP-nnn` (App) ou `<PREFIXO>-LVW-nnn` (Web), com o próximo número livre consultado no Squash.
- **Cadastra no Squash**, mas só depois da sua aprovação, e termina **vinculando os casos ao requirement** da atividade (Reference = chave do Jira) e **adicionando o requirement à próxima sprint** em Executions, para entrarem no reteste da versão.

## Quando usar

A skill entra sozinha quando você pede cenários ou casos de teste. Por exemplo:

- "monta os cenários da VENDAS-25526";
- "o que testar nesse bug?";
- "cria os casos de teste dessa story e cadastra no Squash";
- "revisa a cobertura dos critérios de aceite da VENDAS-25199".

Para chamar direto: `/gerador-de-testcases`.

## O que você precisa ter

- **MCP interno da WMW** (leitura de Jira e Confluence). Sem ele, cole a atividade no chat e a skill pula a pesquisa no Confluence.
- **Claude in Chrome** conectado, com `squash.wmw.com.br` liberado nas permissões de site.
- **Estar logado no Squash** nesse Chrome. A skill nunca digita senha.

Sem o Chrome, você recebe os cenários prontos com a Reference `<PREFIXO>-LVP-???`, para numerar e cadastrar à mão.

## Como usar

1. **Peça os cenários** com a chave da atividade.
2. **Responda à rodada de dúvidas** (uma só): regra ambígua, valor esperado, pasta no Squash quando o cenário foge da Feature. "Não sei" vale.
3. **Revise a entrega**: matriz (com a origem de cada cenário), e cada cenário com cabeçalho, pré-requisitos, observações e riscos, clientes e passos.
4. **Aprove**, total ou parcialmente ("cadastra só os 3 primeiros"), ou peça ajustes.
5. **Acompanhe o cadastro** no Chrome e confira pelos links que ela devolve.

## Padrões que a skill segue

| Item | Regra |
|---|---|
| Plataforma | campo **Environment** da atividade: `App` → LVP, `Web` → LVW. Com os dois, gera os dois conjuntos |
| Prefixo | o sub-módulo da **Feature**, conferido nos [Manuais de Configuração](https://confluence.wmw.com.br/confluence/pages/viewpage.action?pageId=1212592). Se a pasta no Squash já usa um prefixo, vale o da pasta |
| Feature que não descreve o cenário | a skill propõe outro prefixo ou uma pasta nova, com o motivo. Você decide |
| Numeração | maior número da pasta no Squash + 1, conferido de novo logo antes de cadastrar |
| Tela x regra | a validação do cálculo vai no mesmo passo em que a tela mostra o valor, nunca em cenário separado |
| Parâmetros | cada arranjo de parâmetros é um cenário próprio |
| Tecniquês | proibido em teste de tela; exigido em teste de backend (tabela, query, endpoint, log) |
| Persistência no App | salvar, sincronizar e conferir na Web, chamando o caso compartilhado [PERSISTENCIA-001](https://squash.wmw.com.br/squash/test-case-workspace/test-case/3463/steps) |
| Label `DEV_TESTS` | vai no caso só se a atividade tiver essa label no Jira |
| Story sem critérios de aceite | a skill para e avisa, para você cobrar o PO ou o dev |

## Bom saber

- A **coluna Origem** da matriz mostra de onde veio cada cenário (critério 2, Defect da subtask, erro comum). Ela ajuda a revisar e não vai para o Squash.
- A lista de erros comuns está em `references/erros-comuns.md`. Vale ler e completar com o que o time aprende.
- Se a skill encontrar no Squash um caso que já cobre o mesmo comportamento, ela propõe reaproveitar em vez de criar outro.
- Ela não edita, move, renumera nem apaga casos existentes sem você pedir.
- Depois do cadastro, ela pode passar um cenário para a `totaluitest-codigo` (automação) ou abrir a Test Automated com a `criar-task-jira`.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `SKILL.md` | o fluxo: ler a atividade, pesquisar, montar, perguntar, aprovar, cadastrar e devolver os links |
| `references/erros-comuns.md` | o que o usuário real faz e o dev esquece, por categoria |
| `references/nomenclatura.md` | Reference, prefixo a partir da Feature, quando usar outra pasta, numeração |
| `references/modelo-saida.md` | o formato da entrega e como cada parte vai para o Squash |
| `references/squash-chrome.md` | consulta e cadastro no Squash pelo navegador |

## Instalação

Copie a pasta `gerador-de-testcases/` inteira, com a subpasta `references/`:

- **Claude Code**: em `~/.claude/skills/`, ou em `.claude/skills/` do projeto;
- **claude.ai**: suba a pasta como skill nas configurações de Skills.
