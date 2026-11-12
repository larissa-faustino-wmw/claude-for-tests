# executar-testes

Skill do Claude que **executa os casos de teste do Squash**, no **App** e na **Web**, e registra o resultado na execução do Squash. Vale para os momentos de execução do tester: a atividade (com o reteste), a sprint, a Delivery da versão e a homologação de cliente.

## Para que serve

- **Lê o que executar no Squash:** os casos da atividade (requirement na sprint), uma iteração, a campanha da versão ou a da homologação.
- **Escolhe o modo de cada caso:**

  | Modo | Quando |
  |---|---|
  | Automatizado | o caso já tem teste no `totaluitest` (App) ou no `webuitest` (Web): a skill roda e lê o resultado |
  | Assistido no App | pelo **agente tcui**: a skill sobe o app, clica, preenche, lê valores e tira print |
  | Assistido na Web | pelo **Claude in Chrome**, no Tomcat de dev ou no ambiente que você indicar |
  | Manual guiado | o que a skill não faz sozinha (aparelho, impressora, ERP): ela mostra um passo por vez e você diz o que viu |

- **Confere cada passo com o valor** e guarda a evidência (print, valor, log).
- **Registra no Squash:** status por passo, comentário com ambiente e modo, e a evidência anexada.
- **Prepara o Defect de cada falha** para a `criar-task-jira`, e põe a chave na execução.

## Quando usar

- "executa os testes da VENDAS-25526";
- "roda a iteração SHIELD - VENDAS-21089 da campanha da Rivatti";
- "reteste da VENDAS-24543 depois da correção";
- "executa a regressão da 9.070".

Para chamar direto: `/executar-testes`.

## O que você precisa ter

- **Claude in Chrome**, logado no Squash (ler o plano e registrar) e na Web quando o caso for Web.
- **App assistido:** o `totaluitest` na branch **`tcui-split-tc5`** (onde está o agente tcui) e o `workspace.properties` com o app e a base. A janela do simulador abre na sua tela.
- **Web:** o Tomcat de dev de pé, ou o endereço do ambiente.
- **Automatizado:** JDK 8 (App) ou JDK 17 (Web) e Maven.

## Como usar

1. Peça a execução (atividade, iteração, campanha ou versão).
2. Confira a **lista de casos com o modo** proposto para cada um, e dê o ok.
3. Acompanhe: na primeira execução, a skill mostra o que vai registrar no Squash antes de gravar.
4. No fim, você recebe o resumo por status, os Defects para abrir (ou abertos, com a sua aprovação) e o que ficou pendente.

## Bom saber

- **Sem evidência, não é "passou".**
- A skill **faz backup da base do App** antes de usar o agente, porque o app grava nela.
- Ela **não sobe nem derruba o Tomcat ou o agente, e não troca de branch**, sem perguntar.
- **Senha:** nos logins de Squash, Jira e ambientes de homologação, quem entra é você. Só no Tomcat local, e se você pedir, ela usa o usuário de teste do arquivo de configuração.
- Ela olha os pontos que escondem defeito em todo caso que grava ou sincroniza: erro só no log, o que se perde na sincronização, o parâmetro desligado, os idiomas e dado de outro teste.
- Falha de teste automatizado não é, por si, defeito do produto: ela confere antes se o problema é o teste (para isso, a `analise-logs-jenkins`).

## Onde entra no fluxo do tester

| Fluxo | Antes | Depois |
|---|---|---|
| Atividade | `gerador-de-testcases` | `criar-task-jira` (Defects), reteste, `liberar-atividade` |
| Delivery | `analise-impacto-delivery` | `criar-task-jira` (Defects), `relatorio-qualidade` |
| Homologação | `roteiro-homologacao` | `criar-task-jira` (Defects) |

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `SKILL.md` | o fluxo: o que executar, modo, ambiente, execução, registro, Defects e encerramento |
| `references/modo-app.md` | App: teste do `totaluitest` e execução assistida pelo agente tcui |
| `references/modo-web.md` | Web: teste do `webuitest` e execução assistida pelo Chrome |
| `references/squash-execucao.md` | ler o plano pela API e registrar a execução pela tela |
| `references/pontos-de-defeito.md` | onde os defeitos se escondem |

## Instalação

Copie a pasta `executar-testes/` inteira, com `references/`, em `~/.claude/skills/` ou em `.claude/skills/` do workspace. Precisa do Claude Code (Chrome, agente tcui e repositórios).
