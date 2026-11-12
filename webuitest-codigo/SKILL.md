---
name: webuitest-codigo
description: Escreve testes automatizados de tela do Lavendere Web (wmwvendas) no repositório webuitest — Playwright Java + JUnit 5 contra o Tomcat local de dev — usando a infraestrutura que já existe (AmbienteLocal, SessaoWeb, BancoTeste, LogErroTomcat), localizadores estáveis para as telas JSF do framework-web, asserções web-first do Playwright, limpeza dos dados no banco sem reset, e entrega também o cenário, o worklog e a lista de classes alteradas. Use SEMPRE que o usuário pedir para escrever, gerar, automatizar ou corrigir um teste da Web, automatizar um cenário LVW do Squash, criar Page de tela web, ou mencionar webuitest, Playwright, wmwvendas, SessaoWeb ou teste de tela web — mesmo que diga só "automatiza esse cenário na web". Para o App (TotalUiTest), use a skill totaluitest-codigo.
---

# Código de teste Web (webuitest)

Você escreve testes de tela do Lavendere Web no repositório `projetos/webuitest`: **Playwright Java + JUnit 5**, contra o wmwvendas publicado no **Tomcat local** do tester. As regras de Playwright vêm das boas práticas oficiais (localizador estável, asserção que espera sozinha, nada de espera fixa) adaptadas às telas JSF do `framework-web` e à infraestrutura do repositório.

A automação Web está **começando**: hoje o repositório tem o smoke que abre as telas do menu. Os primeiros testes de negócio vão criar a base (Pages, utilitários de massa e limpeza). Faça isso com cuidado, porque os próximos vão copiar.

## Entregas

As mesmas da `totaluitest-codigo` (formatos em `references/entregas.md`):

1. **Cenário** (passos e resultados esperados) fiel ao código, ou a conferência com o caso LVW do Squash.
2. **Código**: a classe de teste e, se preciso, a Page e o utilitário de massa.
3. **Worklog** em primeira pessoa, para o tester lançar.
4. **Classes alteradas**, com o caminho a partir de `src/`.

## Fluxo

### 1. Ler o cenário e a atividade

- Test Automated pelo MCP interno (`get_jira_issue`): Cenário, Teste, Link do Squash, Baseado na atividade.
- Caso do Squash (Reference `…-LVW-nnn`): passos colados pelo tester, ou lidos pela API do Squash no Chrome.
- Regra de negócio: na dúvida, leia o código da tela (`lavendereweb/webapp/views/…xhtml`, o managed bean e o service no `lavenderecore`) em vez de supor.

### 2. Ler a infraestrutura antes de escrever

Leia o que existe (`references/estrutura-webuitest.md`): `AmbienteLocal`, `SessaoWeb`, `BancoTeste`, `LogErroTomcat`, `ItemMenu`, o `SmokeTelasTest` e as Pages que já existirem. **Reaproveite; não recrie.** Método novo na infraestrutura só quando não houver equivalente, listado em Classes alteradas.

Antes de criar a primeira Page ou o primeiro utilitário de massa de uma área, mostre ao tester a estrutura proposta (pacote, nome, métodos) e espere o ok.

### 3. Conhecer a tela

- **Leia o `.xhtml` da tela** para achar os ids dos componentes (`input:text id="..."`, `input:button id="..."`) e os rótulos (`label="#{msgs....}"`; o texto em pt-BR está nos `Messages`).
- **Explore a tela de verdade**, se o Tomcat estiver de pé: abra pela `SessaoWeb` com `navegador.headless=false` ou leia o snapshot da página (`salvaImagem`, `content()` do frame). Não escreva localizador sem ter visto o HTML renderizado.
- O catálogo de componentes do `framework-web` (`docs/ia/web/framework-web/10-catalogo-componentes.md`) diz como cada tag é desenhada.

### 4. Escrever

Seguindo `references/regras-playwright.md`. As essenciais:

- **A tela abre no iframe `#contentFrame`**, pela `SessaoWeb.abre(item)`; tudo da tela se procura dentro do frame (`frameLocator("#contentFrame")`).
- **Localizador estável:** rótulo ou papel acessível quando o HTML tiver; senão o **id que está no `.xhtml`**, pelo sufixo (`[id$=':btnSalvar']`), porque o JSF prefixa o id do formulário. **Nunca** `j_idt…`, posição, índice ou XPath de layout.
- **Asserção web-first:** `PlaywrightAssertions.assertThat(locator).hasText(...)`, `hasValue`, `hasCount`, `isVisible` só quando o teste é sobre aparecer. Ler `innerText()` e comparar com `assertEquals` não espera e dá teste instável.
- **Sem espera fixa** (`Thread.sleep`, `waitForTimeout`) e sem aumentar o timeout padrão.
- **Depois de cada ação que vai ao servidor**, confira que não há erro: mensagem `.wmw-errorMessage` visível, resposta 5xx e linha nova no `error.log` (os mesmos critérios do smoke).
- **Dados:** o banco não tem reset. O teste cria a própria massa e **apaga o que criou em `@AfterEach`/`finally`**, inclusive quando falha.
- **Comentários de passo** no padrão do time: `/* Passo N: ... */` e `/* Resultado Esperado N: ... */`, multilinha, numerados em par, como no TotalUiTest.

### 5. Gravar com o encoding certo

`.java` em ISO-8859-1 com CRLF (o `.gitattributes` garante o CRLF), e **os fontes atuais são ASCII puro**: texto com acento numa asserção vai com escape `\uXXXX` (`"Operação realizada"`). Confira com `file -b` depois de gravar. Read/Edit/Write gravam UTF-8: escreva por script quando houver acento.

### 6. Rodar, se o ambiente estiver de pé

- Primeiro `mvn test -Dtest=AmbienteLocalTest` (diz se Tomcat, banco e login estão ok); depois `mvn test -Dtest=<SeuTest>` com JDK 17.
- **Não suba nem derrube o Tomcat sem perguntar**: o dev pode estar com o dele aberto na IDE. Subir é pelos scripts `dev/dev-*` da raiz do workspace.
- Rode duas ou três vezes: teste que passa uma vez e falha na outra não está pronto.
- Não diga que passou sem ter rodado.

## Armadilhas

- **O iframe.** Localizador procurado na `Page` principal não acha nada da tela: use o frame `#contentFrame`.
- **Abrir item de menu executa o comando dele** (`NMCOMANDOACAO`). Abra só a tela do cenário, pela chave `cdSistema,cdMenu` do `ItemMenu`, e não amplie o `smoke.comandoPermitido`.
- **Popups depois do login** (recados, novidades, aniversariantes) cobrem a tela: a `SessaoWeb.entra` já fecha; não reescreva o login.
- **A senha do login** só pode ser preenchida depois que o script do `login.xhtml` limpa o campo; por isso, sempre `AmbienteLocal.abreSessaoLogada()`.
- **Id do JSF tem `:`** (`atendimentoForm:btnNovoCliente`): em CSS, `#atendimentoForm\\:btnNovoCliente` ou `[id$=':btnNovoCliente']`.
- **Mensagens escondidas.** As telas carregam `.wmw-errorMessage` invisíveis: só conta a visível (`>> visible=true`).
- **O `error.log` é do Tomcat inteiro**: outra execução ou alguém navegando ao mesmo tempo põe erro alheio no seu teste.
- **Texto depende do idioma.** A sessão abre em `pt-BR`; rótulo e mensagem vêm dos `Messages`, então copie de lá, não da memória.
- **Nada da máquina no código:** porta, banco, usuário e senha vêm do `webuitest.properties`/`workspace.properties`. Nunca leia nem grave a senha.

## Cuidados

- Não altere o código do `lavendereweb` para a automação: componente sem id estável, peça ao dev para pôr o `id` na tag.
- Não refatore a infraestrutura fora do escopo; limpeza pequena no arquivo que você já mexe, sim.
- Não commite nem faça push sem o tester pedir; commit só com o código da atividade (`VENDAS-xxxxx`).
- Sem dados reais (CPF, CNPJ, e-mail) na massa.
