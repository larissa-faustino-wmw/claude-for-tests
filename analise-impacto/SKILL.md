---
name: analise-impacto
description: Analisa o impacto (side effects) de uma alteração do Lavendere para o QA — lê o diff da branch da atividade nos repositórios (lavenderepda, lavendereweb, lavenderecore), descobre quem mais usa o código alterado (telas, services, sincronização, as duas stacks), confere o que já está coberto (casos da atividade no Squash, testes do totaluitest, regressão fixa da Delivery) e devolve a lista de side effects com risco e a recomendação de virar caso de teste, automatizar ou deixar com a regressão. Use SEMPRE que o usuário pedir análise de impacto, side effect, "o que mais essa alteração pode quebrar", "o que regredir", impacto de uma correção (bug voltou para reteste) ou riscos de uma atividade VENDAS-xxxxx — mesmo que diga só "analisa o impacto da VENDAS-25526". Para os riscos da versão inteira na Delivery ou a calibração da regressão fixa, use a skill analise-impacto-delivery. Somente leitura: não cria casos nem altera código.
---

# Análise de impacto (side effects)

A regressão fixa da Delivery (pastas `00. Testes de Regressão App` e `Web` no Squash) é ampla e exploratória: diz onde olhar, não o que mudou. O reteste das atividades cobre o que cada uma prometeu. O **side effect** fica no meio: uma área que a atividade não pretendia mexer, que a regressão fixa não detalha, e que usa o código alterado. Esta skill encontra esse meio **durante o desenvolvimento**, quando o QA pega a atividade, para que o side effect vire caso de teste (e, quando vale, automação) antes da Delivery.

A skill **só lê**: código, Jira, Confluence e Squash. Os casos aprovados seguem para a `gerador-de-testcases`; a automação, para a `totaluitest-codigo`.

**Quando:** o QA pega uma Story ou um Bug pronto na branch (o padrão é a branch já estar pronta; se o dev ainda estiver commitando, avise que a análise precisa ser refeita no fim), ou um Bug volta para reteste. **Entrada:** a chave `VENDAS-xxxxx`.

Na semana de Delivery, o que só aparece com a versão inteira (atividades que mexem nos mesmos arquivos, commits sem atividade, correções da Delivery) é da skill `analise-impacto-delivery`.

## Fluxo

### 1. Ler a atividade

Pelo MCP interno (`get_jira_issue`, com comentários): tipo, descrição, critérios de aceite, Feature, Environment, subtasks (Defects já achados), Issue Cause e Root Cause (em Bug), links. Se for subtask, use a chave da atividade principal para achar o código.

### 2. Levantar o que mudou

Detalhes e comandos em `references/coleta-diff.md`. Em resumo:

1. Em cada repositório de `projetos/` (`lavenderepda`, `lavendereweb`, `lavenderecore`, e os `framework-*` se aparecerem), `git fetch` e procure a branch com a chave no nome (`*VENDAS-xxxxx*`).
2. A base do comparativo é sempre a **`main`** (a última versão liberada). Dentro de `origin/main..origin/<branch>`, pegue os commits **com a chave na mensagem** (`git log --grep`) e os arquivos que eles alteraram. Sem o filtro pela chave, o diff traz também o que a branch herdou da `develop` e ainda não foi liberado.
3. Branch não encontrada: procure os commits pela chave em `origin/main..origin/develop` (já liberada pelo QA e incrementada) e, na semana de Delivery, em `origin/main..origin/release`. Nada em lugar nenhum: pergunte ao tester qual é a branch.
4. Liste os arquivos alterados por repositório e o tipo de cada um (domain, DAO, service, tela, sync, `Messages`, parâmetro, script de banco, sqlmap, managed bean, xhtml).

Diff muito grande (refatoração, centenas de arquivos): foque nas classes de regra (service, domain, DAO, cálculo) e avise que a análise é parcial.

### 3. Rastrear até onde a mudança vai

Para cada alteração relevante, siga `references/rastreio-impacto.md`:

- **quem chama** o método ou a classe alterada (`Grep` no repositório), até chegar às telas e aos fluxos do usuário;
- **a outra stack**: a mesma entidade no app (`TBLVP<X>`) e no web (`TBLVW<X>`), e a sincronização entre elas (`docs/ia/comum/30-correspondencia-app-web.md`);
- **parâmetros**: parâmetro novo ou com uso alterado — todos os pontos que leem o mesmo parâmetro;
- **área de negócio** de cada classe (`docs/ia/comum/areas.tsv`, mapas em `docs/ia/pda/20-mapa-modulos.md` e `docs/ia/web/20-mapa-modulos.md`).

Não leia o repositório inteiro: parta do diff. Use a KB (`docs/ia/INDEX.md`) antes de varrer código.

Cada achado vira um **candidato a side effect**: "a alteração em X afeta Y (tela/fluxo), porque Y chama X em Z". Sempre com a evidência (arquivo e método).

### 4. Conferir o que já está coberto

Para cada candidato:

- **Casos da atividade**: os casos ligados ao requirement `VENDAS-xxxxx` no Squash. Se o critério de aceite da atividade já cobre o candidato, ele não é side effect.
- **Testes automatizados**: testes do `totaluitest` que passam pelo fluxo (`Grep` pelas Pages e telas envolvidas em `src/test/java/.../test/`). Coberto por teste automatizado que valida o valor afetado = coberto.
- **Regressão fixa**: os casos das pastas `00. Testes de Regressão App` (id 7) e `Web` (id 17). Leia pela API do Squash (`references/rastreio-impacto.md` §Squash). Ela conta como cobertura **só para o fluxo largo**: o caso "Tributação" cobre "abrir pedido e olhar impostos", não "FECOP tipo 2 com ST".

### 5. Dar o risco

Com `references/riscos.md`: probabilidade (quão direto é o uso do código alterado) × impacto (cálculo, financeiro, sincronização, fluxo de uso diário), ajustado pelo histórico da feature no Jira (`jira_feature_hotspots`, `jira_rework`, `jira_problem_causes`) e por outras atividades abertas que mexem nas mesmas classes.

Para cada side effect, a recomendação:

| Recomendação | Quando |
|---|---|
| **Automatizar** | risco alto e passa no critério de automação (`references/riscos.md`) |
| **Virar caso** (manual) | risco médio ou alto, sem critério de automação |
| **Regressão fixa basta** | risco baixo e o fluxo largo está na regressão |
| **Só observar** | risco baixo, sem cobertura, citado para o tester olhar de passagem |

### 6. Entregar

Formato em `references/modelo-saida.md`: resumo da mudança, mapa de impacto, tabela de side effects (risco, evidência, cobertura atual, recomendação) e as perguntas ao dev quando o código não deixa claro.

Feche oferecendo o próximo passo:

> Quer que eu gere os casos dos side effects aprovados com a `gerador-de-testcases`? Eles entram no requirement VENDAS-xxxxx e na sprint junto com os da atividade.

Os marcados para automatizar seguem depois para `orcamento-modelo-antigo` e `totaluitest-codigo`.

**Bug em reteste:** além do impacto da correção, verifique se o Root Cause aponta uma causa que pode existir em outros pontos (o mesmo padrão em outra tela) e se é reincidência (Issue Cause apontando outra atividade).

## Armadilhas

- **Não use o `merge-base` como escopo.** As branches nem sempre saem da develop atual; o diff traz commits de outras atividades (na VENDAS-25440, 27 arquivos contra os 5 da atividade). Base `main` + filtro pela chave.
- **O nome da branch varia** (`VENDAS-25440`, `Angel-VENDAS-10781`, `Branch_VENDAS-18185`): procure por `*VENDAS-xxxxx*`.
- **Commit já na `main`:** a atividade foi liberada; a análise vira de reteste (o código a olhar é o da correção nova).
- **A regressão fixa é ampla.** O caso "Tributação" cobre abrir pedido e olhar impostos, não uma regra específica: não conte como cobertura de regra.
- **Os mapas de módulo da KB são rascunho.** Use como guia para achar área e telas, não como verdade.
- **O MCP não traz o Environment:** plataforma deduzida tem de ser marcada como deduzida.

## Cuidados

- **Evidência sempre.** Side effect sem arquivo e método que o sustente vira "pergunta ao dev", não achado.
- Não invente regra de negócio: o que o código faz está no código; o que deveria fazer, no Jira e no Confluence.
- Não sugira caso para o que a atividade já cobre, nem repita a regressão fixa.
- Prefira poucos side effects bem fundamentados a uma lista longa: o tester precisa conseguir testar.
- Somente leitura: não faça checkout que mude o branch de trabalho do tester (use `origin/<branch>` nos comandos), não commite, não altere arquivos.
- Os `.java` são ISO-8859-1: acento torto no diff não é erro da alteração.
