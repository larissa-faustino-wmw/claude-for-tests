# fechar-test-automated

Skill do Claude que faz o **fechamento de uma Test Automated**: confere que o teste está pronto de verdade e preenche no Jira e no Squash tudo o que o fechamento exige. Esse fechamento alimenta o comparativo de horas, o relatório de qualidade e a fila de automação, então campo esquecido aqui vira número errado lá.

## O que ela confere

| Conferência | Para fechar |
|---|---|
| Revisão | parecer da `revisar-teste-automatizado` aprovado, sem crítico nem alto. Se não houver revisão, ela oferece rodar o revisor antes |
| Código na develop | os commits da atividade estão na `develop` do `totaluitest` ou do `webuitest` |
| Passa | três rodadas seguidas e, se já está na execução noturna, sem falha no Jenkins |
| Squash × código | o caso descreve o que o teste faz |
| Horas | Σ Time Spent lançado |
| Defeitos | os Defects e Bugs achados pela automação estão vinculados |

## O que ela preenche (GUIA-JIRA-003)

- **Component/s:** as classes criadas ou alteradas, com o nome da classe, como nas atividades fechadas.
- **Fix Version/s:** a versão em que o teste foi liberado.
- **Descrição:** a classe em "Teste:" e o link do caso em "Link do Squash:".
- **Labels:** `QA_BUILD_AI` ou `QA_BUILD_TESTER`, `QA_REVIEW_AI` quando couber e `QA_BUG_FOUND` quando a automação achou defeito.
- **Linked Issues:** os defeitos achados.
- **Comentário de fechamento:** horas orçadas, reais e a **redução**, a revisão e os defeitos.
- **Squash:** o caso marcado como aprovado e automatizado. Na primeira vez, ela confirma com você quais campos o time usa.

Depois de tudo aprovado por você, ela fecha a atividade com a resolução "Concluída".

## Quando usar

- "fecha a VENDAS-25597";
- "o que falta para fechar essa Test Automated?";
- ao fim do fluxo de automação, depois da revisão.

Para chamar direto: `/fechar-test-automated`.

## O que você precisa ter

- **MCP interno da WMW** (a atividade).
- **Claude in Chrome** logado no Jira e no Squash.
- **Os repositórios** `totaluitest`/`webuitest` em `projetos/` (conferir a develop).
- As skills `revisar-teste-automatizado` e `orcamento-modelo-antigo` (revisão e cálculo da redução).

## Bom saber

- **Não fecha com pendência que bloqueia:** revisão pedindo mudanças, código fora da develop ou teste falhando.
- **Não lança horas.** Se faltar, ela oferece o texto do worklog.
- **Component/s só aceita componente que já existe no Jira.** Se a classe nova não tiver componente, ela para e avisa, porque criar componente é de quem administra o projeto.
- Atividade que **não vai ser automatizada** (obsoleta, duplicada) não se fecha por aqui, e sim pela `prioriza-automacao` no modo revisar a fila.

## Onde entra no fluxo de automação

`prioriza-automacao` → orçamento → `gerador-de-testcases` → `totaluitest-codigo` / `webuitest-codigo` → `revisar-teste-automatizado` → `analise-logs-jenkins` → **`fechar-test-automated`**

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `SKILL.md` | o fluxo: ler, conferir, montar, aprovar e aplicar |
| `references/campos-fechamento.md` | os campos do Jira e do Squash, o modelo de descrição e do comentário |

## Instalação

Copie a pasta `fechar-test-automated/` inteira, com `references/`, em `~/.claude/skills/` ou em `.claude/skills/` do workspace.
