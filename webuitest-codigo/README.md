# webuitest-codigo

Skill do Claude que **escreve testes automatizados de tela do Lavendere Web** no repositório `webuitest`: Playwright Java + JUnit 5, rodando contra o wmwvendas no Tomcat local de dev. É o par Web da `totaluitest-codigo`.

As regras de Playwright vêm das instruções oficiais de geração de testes (TypeScript, Python e .NET, no repositório github/awesome-copilot), adaptadas para Java, para as telas JSF do `framework-web` e para a infraestrutura que o `webuitest` já tem.

## Para que serve

- **Automatizar um cenário LVW** do Squash ou de uma Test Automated.
- **Criar a base da automação Web:** as primeiras Pages, a abertura de tela pela chave de menu, a conferência de erro e a limpeza da massa.
- **Entregar quatro coisas**, como no App: o cenário (ou a conferência com o caso do Squash), o código, o worklog e a lista de classes alteradas.

## Quando usar

- "automatiza esse cenário na web";
- "escreve o teste da COMERCIAL-LVW-012";
- "cria a Page da tela de aprovação de desconto promocional".

Para chamar direto: `/webuitest-codigo`. Para o App, use a `totaluitest-codigo`.

## O que você precisa ter

- **Claude Code com o workspace**, com o `webuitest` e o `lavendereweb` em `projetos/`. A skill lê o `.xhtml` da tela para achar os ids.
- **O Tomcat de dev** com o wmwvendas publicado, e o `workspace.properties` (ou `webuitest.properties`) preenchido, para rodar. A skill não sobe nem derruba o Tomcat sem perguntar.
- **JDK 17** e Maven.
- **MCP interno da WMW**, para ler a Test Automated e os links.

## As regras principais

| Assunto | Regra |
|---|---|
| Onde está a tela | no iframe `#contentFrame`, aberta pela `SessaoWeb` com a chave `cdSistema,cdMenu` |
| Localizadores | papel ou rótulo acessível quando houver; senão o **id do `.xhtml` pelo sufixo** (`[id$=':btnSalvar']`). Nunca `j_idt`, posição ou XPath |
| Asserções | as do Playwright, que esperam sozinhas (`assertThat(locator).hasText(...)`); nada de `innerText()` com `assertEquals` |
| Esperas | nenhuma espera fixa e nenhum timeout aumentado |
| Erro da tela | depois de cada ação, sem mensagem de erro visível, sem resposta 5xx e sem linha nova no `error.log` |
| Dados | o banco não tem reset: o teste cria a massa e apaga em `@AfterEach`/`finally` |
| Comentários | `/* Passo N: */` e `/* Resultado Esperado N: */`, como no TotalUiTest |
| Encoding | ISO-8859-1, CRLF, **ASCII puro** (acento por `\uXXXX`) |

## Bom saber

- A automação Web **está começando**. Antes de criar a primeira Page ou o primeiro utilitário de uma área, a skill mostra a estrutura proposta e espera o seu ok, porque os próximos testes vão copiar.
- **Abrir um item de menu executa o comando dele.** A skill abre só a tela do cenário.
- A skill roda o teste duas ou três vezes antes de dar como pronto, e não diz que passou sem ter rodado.
- Ela não altera o `lavendereweb`. Se um componente não tiver id estável, ela pede ao dev para pôr o id.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `SKILL.md` | o fluxo, as regras essenciais e as armadilhas |
| `references/regras-playwright.md` | localizadores, asserções, esperas, estrutura do teste, Page e checklist, em Java |
| `references/estrutura-webuitest.md` | a infraestrutura do repositório, como abrir a tela, conferir erro, limpar dados e rodar |
| `references/entregas.md` | o formato do cenário, do worklog e da lista de classes |

## Instalação

Copie a pasta `webuitest-codigo/` inteira, com `references/`, em `~/.claude/skills/` ou em `.claude/skills/` do workspace. Precisa do Claude Code.
