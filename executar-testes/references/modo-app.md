# App (TotalCross)

## Automatizado (o caso já tem teste no totaluitest)

A classe está no Squash (campo de teste automatizado do caso), no Component/s da Test Automated ou na descrição dela ("Teste:"). Rode só ela:

- na branch `tcui-split-tc5`: `.claude/skills/tcui-criar-teste/scripts/rodar-teste.ps1` (o script da skill `tcui-criar-teste`);
- em qualquer branch: `mvn test -Dtest=<Classe>` no `projetos/totaluitest`, com `JAVA_HOME` no JDK 8 (`JAVA8_HOME`).

Resultado: o relatório do Surefire. Falha: a evidência é o print em `dadosTest/<Classe>/imagens/<metodo>/` e o log; para entender a causa, a skill `analise-logs-jenkins` lê o mesmo formato. Falha de teste não é, por si, defeito do produto: confira se é o teste (massa, espera) antes de abrir Defect.

## Assistido (pelo agente tcui)

O agente sobe o app dentro da JVM dele e recebe ações por HTTP em `http://127.0.0.1:8099`. O manual completo é a skill `tcui-test` (`projetos/totaluitest/.claude/skills/tcui-test/SKILL.md`, na branch `tcui-split-tc5`): **leia antes de usar**. O essencial:

### Antes

1. Confira a branch do `totaluitest` (`tcui-split-tc5`). Em outra, pergunte ao tester; não troque de branch por conta própria.
2. Já há agente de pé? `curl -s -m 5 http://127.0.0.1:8099/health`. Se sim, reuse e não chame `/launch` nem `/quit` sem combinar (pode ser a sessão do tester no Eclipse).
3. **Base:** copie o `wmwvendas.sqlite3` que o agente vai usar (o `/dataPath`), confira o hash, e trabalhe na cópia. Homologação: a base do cliente, também em cópia.
4. Pré-requisitos do caso (parâmetros, massa) aplicados na cópia com Python `sqlite3`, anotando o que mudou.
5. Suba: `.\run-agent.ps1` na raiz do `totaluitest` (lê `tcui-agent.properties` ou `workspace.properties`). Sem configuração, pergunte `-AppDir` e `-AppArgs`: não chute. A janela do simulador abre na tela do tester: avise antes. Espere `[tcui] app de pe` ou `/health` com `appRunning: true`.

### Durante

- **Ache o fluxo nos page objects** (`src/test/java/br/com/wmw/lavenderepda/presentation/ui/page/`) antes de explorar: eles dizem qual controle clicar e qual tela esperar.
- **`/tree`** (ou `/find?q=...`) antes de agir; depois de trocar de tela, `/tree` de novo.
- Aja pelo `name` da árvore: `/click`, `/type`, `/key`, `/scroll`; leia com `/value` e `/window`.
- Lista que carrega em outra thread: `/waitValue` com o valor esperado (ou `not=` o anterior).
- Diálogo no topo aparece no campo `dialog` da resposta: leia a mensagem (é o resultado de muitos passos) e feche pelo botão.
- **Evidência:** `/screenshot` em cada resultado esperado, e o valor lido (`/value`) anotado com o passo.
- Login: a senha dos testes é a da base de teste do totaluitest (`WMW`); na base de cliente, peça ao tester.

### Depois

- `POST /quit` (se foi a skill que subiu o agente).
- Devolva a base original (ou descarte a cópia) e confira o hash.
- Persistência (o caso grava e sincroniza): a conferência do lado Web vai pelo modo Web (`modo-web.md`) ou pelo banco web, só leitura.
