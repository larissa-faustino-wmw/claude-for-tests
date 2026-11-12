# prioriza-automacao

Skill do Claude que **sugere o que automatizar a seguir**, a partir de uma versão: analisa todas as atividades dela, os Defects encontrados, os bugs que ela causou e o histórico das features, confere o que já está automatizado e devolve uma lista priorizada de cenários (App e Web), cada um com os bugs que o justificam. Você avalia a lista; só as aprovadas viram Test Automated no board de automação do Jira.

## Por que existe

A automação precisa estar onde o bug está, e os números mostram que nem sempre está. Em 11/2026, Estoque Padrão tinha 45 automações e não estava entre as áreas com mais bugs, enquanto Pedidos Pendentes (42 bugs em 180 dias, subindo), Desconto Diversos, Orçamentos, Títulos Financeiros e Condição de Pagamento tinham zero. Já Tributação Personalizada, com 19 automações, viu os bugs caírem de 30 para 13.

## Quando usar

- "o que vale automatizar da 9.070?";
- "monta a fila de automação da última versão";
- "onde está faltando automação?".

Sem versão no pedido, a skill **pergunta qual versão** analisar. Período em dias ("últimos 6 meses") ou uma atividade específica só quando você pedir explicitamente.

Para chamar direto: `/prioriza-automacao`.

## O que você recebe

1. O resumo da versão (entregas, correções, Defects, regressões confirmadas).
2. A cobertura das features da versão: bugs × automação existente × o que já está na fila.
3. **Todas as sugestões numeradas**, em ordem de pontuação, com plataforma (App ou Web), o cenário, a evidência (bugs e Defects), a pontuação explicada e o porte provável.
4. Os descartados, com o motivo (já automatizado, já na fila, não automatizável).
5. Um parágrafo **"Para começar a Web"**: os primeiros cenários Web e a infraestrutura que eles exigem no `webuitest`.

Você responde quais números aprovar, descartar ou ajustar. Depois, a skill cria uma Test Automated por aprovada (pela `criar-task-jira`), com Test Case Type Automação, label `QA_ORIGIN_AI` (ou `QA_ORIGIN_ISSUE`), os bugs vinculados e a justificativa na descrição. Ela pode orçar antes com a `orcamento-modelo-antigo`.

## Modo revisar a fila

O board de automação tinha **314 Test Automated abertas** em 10/11/2026, muito mais do que o time automatiza num ciclo. Peça "revisa a fila de automação" e a skill lê o board inteiro e devolve:

- **Puxar a seguir:** as 10 a 15 de maior pontuação, com a dor atual da feature.
- **Fechar:** já automatizadas (Test Automated concluída ou teste existente no repositório), duplicadas na fila, obsoletas ou sem valor, cada uma com a evidência. Ela não fecha nada só por ser antiga.
- **Juntar:** atividades da mesma regra com variações pequenas.
- **Corrigir dados:** status final sem resolução, horas lançadas em Options, `NOT_IS_TEST_CASE`, sem Feature, sem label de origem.
- **Revisar com o time:** o que ela não conseguiu decidir.

Você aprova seção por seção. Só então ela aplica no Jira pelo Chrome, com um comentário explicando cada fechamento. Antes, pergunta qual transição e resolução o time usa para descartar. A ordem do board ela não mexe.

## Como pontua

**Dor** (regressão confirmada, bugs de produção, Defects, prioridade, tendência, retrabalho, cálculo financeiro ou fiscal) × **automatizável** (regra e cálculo sim; Web e suporte novo no framework pesam menos; lentidão, layout, ERP e serviço externo ficam de fora) × **lacuna** (feature com pouca automação para a dor que tem sobe). A conta aparece em cada sugestão.

## O que você precisa ter

- **MCP interno da WMW** (versões, bugs, histórico).
- **Os repositórios** `totaluitest` e `webuitest` em `projetos/`, para conferir o que já está automatizado.
- **Claude in Chrome** logado no Jira, para criar as Test Automated aprovadas.
- A skill `criar-task-jira` instalada (faz a criação).

## Bom saber

- **Nada é criado antes de você avaliar a lista inteira.**
- A plataforma é deduzida do texto e do Root Cause dos bugs (o MCP não traz o campo Environment) e vem marcada como deduzida.
- A **Web** ainda não é automatizada: o `webuitest` hoje abre telas e verifica que não quebram. Os primeiros cenários Web vão construir a base (Pages, massa, limpeza do banco), por isso pesam mais no porte.
- 10 a 20 sugestões boas valem mais que uma lista enorme.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `SKILL.md` | o fluxo: escopo, dados, candidatos, pontuação, avaliação e criação |
| `references/fontes-dados.md` | as consultas no Jira e nos repositórios, e como deduzir App ou Web |
| `references/pontuacao.md` | a conta de dor × automatizável × lacuna |
| `references/automacao-web.md` | o que o `webuitest` já tem e como começar a Web |
| `references/modelo-saida.md` | o formato da lista e da criação |
| `references/revisao-fila.md` | o modo revisar a fila: leitura do board, critérios de fechar, juntar e corrigir, aplicação após aprovação |

## Instalação

Copie a pasta `prioriza-automacao/` inteira, com `references/`, em `~/.claude/skills/` ou em `.claude/skills/` do workspace. Precisa do Claude Code para conferir os repositórios de teste.
