---
name: fechar-test-automated
description: Faz o fechamento de uma atividade Test Automated do Lavendere — confere que a revisão do teste foi aprovada, que o código está na develop do totaluitest ou do webuitest, que o teste passa (rodadas e Jenkins) e que o caso do Squash bate com o código; preenche no Jira os campos do GUIA-JIRA-003 para o fim (Component/s com as classes, Fix Version/s, descrição com a classe e o link do Squash, labels QA_BUILD_* e QA_BUG_FOUND, Linked Issues dos defeitos achados), registra as horas reais e a redução contra o orçamento, atualiza o caso no Squash e fecha a atividade. Use SEMPRE que o usuário pedir para fechar, finalizar ou concluir uma Test Automated, uma automação ou um cenário automatizado, ou perguntar o que falta para fechar — mesmo que diga só "fecha a VENDAS-25597".
---

# Fechar a Test Automated

O último passo do fluxo de automação: o teste existe, foi revisado, roda, e a atividade no Jira conta isso direito. É o fechamento que alimenta o comparativo de horas, o relatório de qualidade e a fila de automação; campo esquecido aqui vira número errado lá.

Nada é alterado no Jira nem no Squash antes da aprovação.

## 1. Ler

- **A Test Automated** (`get_jira_issue`, com comentários): descrição (Cenário, Teste, Cenário anterior, Baseado na atividade, Baseado no cenário, Link do Squash), Test Case Type, Feature, labels, Component/s, Fix Version/s, Affects Version/s, Original Estimate, Σ horas (`time_spent_h`), links e o comentário de orçamento.
- **O teste:** a classe e o que foi criado ou alterado junto (Pages, utils, `ParametrosTestUtil`, infraestrutura do `webuitest`), pelo git da branch (`*VENDAS-xxxxx*`) ou pelos commits com a chave.
- **O parecer da revisão:** `projetos/<repo>/target/revisao-teste/<Classe>-review.md` ou o comentário de revisão na atividade.
- **O caso do Squash** (link da descrição): status, passos, campos de automação.

## 2. Conferir

| Conferência | Para fechar | Como |
|---|---|---|
| **Revisão** | parecer APROVADO ou APROVADO COM OBSERVAÇÕES, sem CRÍTICO nem ALTO aberto | o parecer da `revisar-teste-automatizado`. Sem revisão: ofereça rodar o agente `revisor-teste-automatizado` antes |
| **Código na develop** | os commits da atividade estão na `origin/develop` do repositório de teste | `git -C projetos/<repo> log origin/develop --no-merges --oneline --grep="VENDAS-xxxxx"` |
| **Passa** | três rodadas seguidas passando (da revisão) e, se já entrou na execução noturna, a última execução do Jenkins sem falha deste teste | o parecer; o log do Jenkins pela `analise-logs-jenkins`, se o tester trouxer |
| **Squash × código** | o caso descreve o que o teste faz (mesmos passos e resultados esperados) | comparar; diferença: ajustar o caso (`gerador-de-testcases`) ou o teste antes de fechar |
| **Horas** | Σ Time Spent lançado (atividade + subtasks) | o Jira. Sem horas: o tester lança; a skill não lança |
| **Defeitos achados** | todo Defect ou Bug aberto por causa da automação está vinculado | links da atividade e Bugs/Defects que citam a atividade ou a classe |

Cada uma: **ok**, **pendente** (com o que falta) ou **não se aplica**. Pendência que bloqueia (revisão com ALTO, código fora da develop, teste falhando): não feche; diga o que falta.

## 3. Montar o fechamento

Campos do GUIA-JIRA-003 que se preenchem no fim (`references/campos-fechamento.md`):

| Campo | Valor |
|---|---|
| **Component/s** | todas as classes criadas ou alteradas, incluindo o teste: o **nome da classe**, sem caminho (ex.: `ValidarAvisoVisitaAndamentoSugestaoSaidaTodasSituacoesTest`) |
| **Fix Version/s** | a versão em que o teste foi liberado: a que vai receber a `develop` com o commit (pergunte se não for óbvio) |
| **Description** | `Teste:` com a classe; `Link do Squash:` com o link do caso; as outras linhas como já estão |
| **Labels** | mantém as de origem (`QA_ORIGIN_*`); acrescenta a de construção (`QA_BUILD_AI` com IA, `QA_BUILD_TESTER` sem); `QA_REVIEW_AI` em refatoração ou revisão feita pela IA; `QA_BUG_FOUND` se a automação achou defeito real |
| **Linked Issues** | os Defects e Bugs achados durante a automação |

**Horas e redução:** com o Original Estimate e o Σ Time Spent, calcule a redução com o script da `orcamento-modelo-antigo` (`scripts/calcular_reducao.py`) e monte o comentário de fechamento (`references/campos-fechamento.md`): horas orçadas, reais, redução, defeitos achados, rodadas e o link do parecer.

**Squash:** o caso do Squash marcado como automatizado e aprovado conforme o padrão do time (`references/campos-fechamento.md` §Squash). Na primeira vez, leia os campos na tela e confirme com o tester quais preencher.

Mostre tudo e pergunte:

> Posso atualizar a VENDAS-xxxxx (Component/s, Fix Version, labels, links, descrição), comentar o fechamento, atualizar o caso no Squash e fechar a atividade?

## 4. Aplicar (pelo Chrome, depois do ok)

1. **Edit** da Test Automated: Component/s, Fix Version/s, labels, descrição. Mude só esses campos.
2. **Link** dos Defects e Bugs (`relates to`).
3. **Comentário** de fechamento.
4. **Squash:** os campos aprovados do caso.
5. **Fechar:** a transição de fechamento com resolução "Concluída". Na primeira vez, leia as transições na tela e confirme qual é.
6. Confira na tela (ou pelo MCP) que os campos e o status ficaram certos; devolva o link.

## Armadilhas

- **Component/s só aceita componente que já existe no projeto.** Classe nova pode não ter componente ainda: se o campo não oferecer o nome, pare e diga ao tester (criar componente é de quem administra o projeto), em vez de pôr outro nome.
- **O nome no Component/s é o da classe, sem pacote nem `.java`**, como nas atividades fechadas.
- **Status no JQL vão em inglês** (`Closed`, `In Progress`); resolução no JQL, `is EMPTY`/`is not EMPTY`.
- **"Fechado" sem resolução existe:** confira que a resolução ficou "Concluída".
- **Σ Time Spent inclui as subtasks** (`time_spent_h`); `time_spent_own_h` é só da atividade. A redução usa o Σ.
- **Fix Version não é a Affects Version:** Affects é a versão em que foi sugerido; Fix é a versão em que foi liberado.
- **Fechar não é limpar a fila:** atividade que não vai ser automatizada (obsoleta, duplicada) não se fecha por aqui, e sim pela `prioriza-automacao` no modo revisar a fila, com o motivo.

## Cuidados

- Nada é alterado sem aprovação; só os campos do fechamento.
- Não lance horas (ofereça o texto do worklog, se faltar).
- Não feche com revisão em MUDANÇAS SOLICITADAS, código fora da develop ou teste falhando.
- Na tela de login do Jira ou do Squash, peça para o tester entrar.
