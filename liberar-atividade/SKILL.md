---
name: liberar-atividade
description: Fecha o teste de uma atividade do Lavendere (Story ou Bug) pelo QA — confere se todos os casos do requirement foram executados no Squash com resultado e evidência, se os Defects da atividade estão resolvidos ou com destino decidido, e se os side effects foram cobertos; com tudo certo, comenta a liberação na atividade com o resumo, fecha a Testing e sugere os cenários candidatos à automação; com pendência, registra a devolução ao dev. Use SEMPRE que o usuário pedir para liberar, aprovar, reprovar, devolver ou fechar o teste de uma atividade VENDAS-xxxxx, fechar a Testing, ou perguntar se a atividade pode ser liberada — mesmo que diga só "libera a VENDAS-25526".
---

# Liberar a atividade

O último passo do tester numa atividade. Depois da liberação, o dev incrementa a branch na `develop`: o que for liberado com pendência escondida chega à Delivery. Por isso a skill **confere antes de liberar**, e libera só com o tester aprovando o resumo.

Nada é alterado no Jira antes da aprovação.

## 1. Ler a atividade

Pelo MCP interno:

- a atividade (`get_jira_issue`, com comentários): tipo, status, branch e projetos citados nos comentários, Fix Version;
- as subtasks (`search_jira_jql`: `parent = VENDAS-xxxxx`): a **Testing** (status, responsável, horas) e os **Defects** (status, resolução, prioridade);
- Bugs ligados (links) e Bugs abertos que citam a atividade (`project = VENDAS AND "Issue Cause" ~ "VENDAS-xxxxx"`).

Sem Testing: avise. O fluxo pede uma Testing por atividade testada (`criar-task-jira`); pergunte se cria antes de liberar.

## 2. Conferir

| Conferência | Liberar exige | Fonte |
|---|---|---|
| **Casos executados** | todos os casos do requirement `VENDAS-xxxxx` na sprint com resultado: `SUCCESS`, ou `UNTESTABLE` com motivo. Nenhum `FAILURE`, `BLOCKED`, `READY` ou `RUNNING` | Squash, API (plano da iteração/sprint; `references/conferencias.md`) |
| **Evidência** | cada caso executado tem comentário ou anexo na execução | Squash |
| **Defects** | todos resolvidos e retestados, ou com destino decidido e registrado: aceito pelo PO, virou outra atividade, é legado e virou Bug | Jira |
| **Side effects** | se houve `analise-impacto`, os side effects aprovados viraram caso e foram executados | Squash + comentário da análise |
| **Reteste** | o último commit da branch é anterior à última execução (o que foi testado é o que vai para a `develop`) | git (`references/conferencias.md`) |
| **Testing** | atribuída a quem testou e com as horas lançadas | Jira |

Cada conferência dá **ok**, **pendente** (com o que falta) ou **não se aplica** (com o motivo).

## 3. Decidir com o tester

Mostre a tabela das conferências e a proposta:

- **Liberar:** tudo ok.
- **Liberar com ressalva:** pendência que o tester ou o PO aceita (um Defect de prioridade baixa que vira outra atividade, um caso não testável no ambiente). A ressalva vai escrita no comentário, com a chave do que ficou.
- **Devolver ao dev:** caso falhando, Defect aberto sem destino, commit depois do teste.

Quem decide é o tester. Não libere com pendência que ele não aceitou explicitamente.

## 4. Montar o comentário

Modelo em `references/modelos.md`, no modo Text do Jira (mesma formatação da `criar-task-jira`): resultado (liberada, liberada com ressalva, devolvida), ambiente e base testados, casos executados com o link do Squash e o placar por status, Defects com chave e situação, side effects cobertos, ressalvas ou pendências e, na devolução, o que precisa ser feito.

Mostre o comentário e as ações e pergunte:

> Posso comentar na VENDAS-xxxxx, fechar a Testing VENDAS-yyyyy e mover a atividade para <status>?

## 5. Aplicar (pelo Chrome, depois do ok)

- **Comentário** na atividade.
- **Liberada:** fecha a Testing (transição de fechamento, resolução "Concluída"). Na atividade, a transição que o time usa depois da liberação do QA: **leia as opções na tela e pergunte na primeira vez** qual é; não assuma.
- **Devolvida:** a Testing continua aberta (Em Andamento). Na atividade, a transição de devolução ao dev, se o time usa uma; senão, só o comentário com a menção ao dev (`[~usuario]`).
- Confira na tela que os status mudaram e devolva os links.

Worklog: a skill **não lança horas**. Se a Testing estiver sem horas, ofereça o texto do worklog para o tester lançar.

## 6. Candidatos à automação

Com a atividade liberada, liste os casos executados que valem automatizar, com o critério da `prioriza-automacao` (cálculo ou regra verificável por valor, sincronização, área com histórico de bug, fluxo de uso diário; fora: visual, lentidão, integração externa). Para cada um: o caso do Squash, a plataforma (App ou Web) e o porquê em uma linha.

Ofereça criar as Test Automated aprovadas com a `criar-task-jira` (label `QA_ORIGIN_ISSUE`, vinculadas à atividade). Nada é criado sem o tester escolher.

## Armadilhas

- **Status no JQL vão em inglês:** "Aberto" = `Open`, "Em Andamento" = `In Progress`, "Fechado" = `Closed`. Com o nome em português, o Jira recusa a consulta.
- **"Fechado" sem resolução existe:** em 11/2026 havia Testing em "Fechado" com a resolução vazia. Ao fechar, confira que a resolução ficou "Concluída".
- **O título da Testing varia:** as antigas se chamam "Teste" ou "Testes"; ache pela subtask do tipo `Testing` da atividade, não pelo título.
- **Defect "Fechado" não é Defect retestado:** confira que houve execução do caso depois da correção.
- **Commit depois do teste:** ajuste de code review ou correção de Defect que entra depois da última execução muda o que vai para a `develop`. Compare as datas.
- **Atividade com várias subtasks de Testing** (reteste aberto como outra Testing): todas precisam estar fechadas.

## Cuidados

- Nada é comentado, fechado ou movido sem aprovação.
- Não lance horas nem altere campos que não sejam os da liberação.
- Não feche Defect: quem fecha é o fluxo do Defect (o dev corrige, o tester retesta).
- Na tela de login do Jira ou do Squash, peça para o tester entrar.
