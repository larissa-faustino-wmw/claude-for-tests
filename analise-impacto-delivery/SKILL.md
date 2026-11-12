---
name: analise-impacto-delivery
description: Analisa os riscos da versão do Lavendere na semana de Delivery para o facilitador e o time de QA — compara a release com a main nos repositórios (lavenderepda, lavendereweb, lavenderecore), cruza com o fixVersion do Jira e aponta o que a análise por atividade não alcança: atividades que mexem nos mesmos arquivos (testadas sozinhas, nunca juntas), commits sem atividade, correções feitas durante a Delivery e atividades que mudaram depois de testadas. Também calibra a regressão fixa da Delivery (pastas de Testes de Regressão App e Web no Squash) contra os bugs reais. Use SEMPRE que o usuário pedir riscos ou impacto da versão 9.xxx, o que aprofundar no teste da Delivery, o que entrou na release, commits sem atividade, conflito entre atividades da versão, ou revisão/calibração da regressão fixa — mesmo que diga só "analisa a release". Para o impacto de uma atividade só, use a skill analise-impacto. Somente leitura.
---

# Análise de impacto da Delivery

Na Delivery, cada atividade da versão já foi testada na sua branch, e a regressão fixa (pastas `00. Testes de Regressão App` e `Web` no Squash) cobre os fluxos largos. Esta skill procura o que **nenhuma das duas camadas vê**: o que só existe com todas as atividades juntas na `release`.

Ela tem dois modos:

| Modo | Quando | Quem usa |
|---|---|---|
| **Versão** | na semana de Delivery, depois que o facilitador incrementa a `develop` na `release`, e de novo antes de liberar | facilitador e testers da Delivery |
| **Calibração** | de tempos em tempos, para revisar a regressão fixa | time de QA |

Somente leitura: código, Jira, Confluence e Squash. Casos novos seguem para a `gerador-de-testcases`; o impacto detalhado de uma atividade, para a `analise-impacto`.

## O fluxo das branches

| Branch | O que tem |
|---|---|
| `main` | a última versão liberada. **Sempre a base do comparativo** |
| `release` | a versão em teste: a `develop` incrementada pelo facilitador, mais as correções da Delivery |
| `develop` | as atividades liberadas pelo QA; durante a Delivery já recebe a sprint seguinte |

Ciclo: `develop` → `release` (início da Delivery) → testes → `release` → `main` → versão liberada → `main` → `develop`.

Sempre `git -C projetos/<repo>` com referências `origin/...`, depois de `git fetch --quiet origin`. Nunca `checkout`, `pull` ou qualquer comando que mexa no branch de trabalho do tester. Repositórios: `lavenderepda`, `lavendereweb`, `lavenderecore` (e `framework-*` se tiverem commits na `release`).

## Modo versão

### 1. O que entrou na versão

Escopo: **`origin/main..origin/release`**. Antes de o facilitador incrementar a `develop` na `release`, use `origin/main..origin/develop`, conferindo o fixVersion de cada chave, porque a `develop` pode já ter atividades da sprint seguinte.

```
git -C projetos/<repo> log origin/main..origin/release --no-merges --name-only --format="@%h %ci %s"
```

Para cada repositório: os commits, as chaves `VENDAS-` das mensagens e os arquivos de cada um.

### 2. Conferir com o Jira

`search_jira_jql`: `project = VENDAS AND fixVersion = "<versão>"` (subtasks contam pela principal). `jira_release_impact` dá o resumo.

- **Chave no código que não está no fixVersion:** entrou na versão sem estar planejada.
- **Atividade do fixVersion sem commit:** ou não tem código (configuração, documentação), ou o código não entrou.

Cite as duas listas; não são erro por si, mas o facilitador precisa saber.

### 3. Atividades que mexem nos mesmos arquivos

Arquivos alterados por mais de uma atividade. Para os arquivos de regra (service, domain, DAO, cálculo, sync), desça ao método: as duas mudaram o mesmo método? Uma muda o que a outra lê?

Cada sobreposição é um candidato: as duas atividades foram testadas sozinhas, cada uma na sua branch, e nunca juntas. Com `references/rastreio-impacto.md`, diga que fluxo do usuário passa pelos dois códigos.

### 4. Commits sem atividade

Commits da lista 1 cuja mensagem não traz `VENDAS-`. Descarte os de versão e build (`pom.xml`, `maven-release-plugin`, "Versão 9.xxx-n"). O resto ninguém testou de propósito: leia o que alteram e diga se toca regra ou tela.

### 5. Correções durante a Delivery

Commits que entraram na `release` depois do incremento (`--since=<data do incremento>`; a data é a do primeiro commit de merge da `develop` na `release`, ou o facilitador informa). Em geral são correções de Defects da Delivery. Cada uma merece um impacto rápido, porque será testada só pelo reteste do Defect, com a regressão já em andamento.

### 6. Mudou depois de testada

Atividade com commits depois da data em que o QA a liberou (a Testing fechada, ou o último comentário do QA): ajuste de code review, conflito resolvido no merge, correção feita direto. Se o commit tocou regra, cite para reteste.

### 7. Risco e entrega

Dê o risco de cada achado com `references/riscos.md`. Formato em `references/modelo-saida.md`: resumo da versão, divergências com o fixVersion e a tabela de riscos (sobreposições, commits sem atividade, correções da Delivery, atividades a retestar), cada um com evidência e a sugestão de onde o teste da versão deve aprofundar além da regressão fixa.

Os cenários que valerem a pena entram no Test de Delivery. Ofereça gerar os casos com a `gerador-de-testcases`.

## Modo calibração

Compara onde os bugs acontecem com o que a regressão fixa cobre. Detalhes em `references/calibracao.md`. Em resumo:

1. Onde dá problema: `jira_feature_hotspots` e `jira_problem_causes` no período (padrão: 12 meses), com destaque para bugs de produção.
2. O que a regressão cobre: os casos das pastas 7 (App) e 17 (Web), lidos pela API do Squash.
3. Cruzar por assunto: área com bug e sem caso → caso novo; área com bug e caso amplo demais → detalhar; caso sem bug na área há muito tempo → enxugar ou automatizar.
4. Qualidade dos casos: sem resultado esperado, sem requirement, em Work in progress.

Entrega: uma lista curta de mudanças sugeridas na regressão fixa, cada uma com os bugs que a justificam. A decisão e a edição no Squash são do time.

## Armadilhas

- **Status no JQL vão em inglês:** "Aberto" = `Open`, "Em Andamento" = `In Progress`, "Fechado" = `Closed`. Com o nome em português, o Jira recusa a consulta.
- **Durante a Delivery a develop já tem a próxima sprint.** O escopo é `main..release`; `main..develop` só antes do incremento, conferindo o fixVersion de cada chave.
- **A mesma atividade pode estar em várias versões** (backport de hotfix: fixVersion `9.050-18` e `9.068`). Não conte duas vezes nem estranhe.
- **Commit de versão não é "sem atividade":** `pom.xml`, `maven-release-plugin` e "Versão 9.xxx-n" saem da lista.
- **A release pode ter mais chaves que o fixVersion** (em 10/11/2026, 74 atividades entre `main` e `release` no lavenderepda): é divergência a reportar, não erro da análise.
- **Versão afetada diz onde o cliente viu**, não onde o bug nasceu.

## Cuidados

- **Evidência sempre:** commit, arquivo e método. Sem isso, vira pergunta ao dev ou ao facilitador.
- Não refaça a análise de cada atividade: isso é da `analise-impacto`. Aqui, só o que aparece com a versão inteira.
- Poucos riscos bem fundamentados: o teste da Delivery tem prazo.
- Os `.java` são ISO-8859-1: acento torto no diff não é erro.
