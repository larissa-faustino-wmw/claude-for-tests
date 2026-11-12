# relatorio-qualidade

Skill do Claude que gera o **relatório de qualidade de uma versão** como **página web**, para o time de QA e a gerência. O topo, de uma tela, responde à gerência: a versão foi bem? estamos melhorando? o que fazer? O detalhe embaixo serve ao QA.

## O que a página mostra

**Para a gerência:**

- **Placar:** os dois números de contenção, os escapes e o desvio do esforço da Delivery, cada um com a variação contra a versão anterior.
- **Tendência:** a contenção e os escapes nas últimas 5 versões.
- **Recomendações:** de 3 a 5, cada uma com a evidência e a ação.

**Para o QA:** a versão em números, o que escapou (com o Root Cause), onde doeu (regressões e features), o esforço da Delivery, a automação, a execução no Squash e um "como ler" com as definições e as fontes.

## Os dois números de contenção

Contenção é a parte do que deu errado que o teste pegou antes do cliente. A página mostra sempre os dois:

| Número | O que conta | 9.068 |
|---|---|---|
| **Pela causa confirmada** | bugs cujo Issue Cause cita uma atividade da versão | 95,7% (44 Defects ÷ 44 + 2 escapes) |
| **Pela versão afetada** | bugs com versão afetada na versão, sem os de legado | 93,6% (44 ÷ 44 + 3) |

O primeiro é mais preciso, mas depende de o Issue Cause estar preenchido (na 9.068, 66,7% dos problemas tinham causa registrada). O segundo pega mais casos, mas a versão afetada diz onde o cliente viu o bug, não onde ele nasceu.

## Quando usar

- "relatório da 9.068";
- "como foi a última versão?";
- "monta o balanço de qualidade para a gerência".

Sem versão no pedido, a skill pergunta qual. O melhor momento é **logo depois de liberar a versão**. Como bugs continuam chegando depois disso, a tendência recalcula as versões anteriores a cada relatório, e a página avisa quando a versão tem menos de 30 dias.

Para chamar direto: `/relatorio-qualidade`.

## O que você precisa ter

- **MCP interno da WMW** (todas as contas do Jira).
- **Claude in Chrome** logado no Squash, para a seção de execução. Sem ele, a seção aparece como "sem dado".
- **Claude Code com Artifacts**, para publicar a página e receber o link. Sem isso, a skill grava o `.html` e diz onde está.

## Bom saber

- **Automação de verdade × limpeza da fila:** fechar atividades antigas sem horas não é automatizar. A skill separa os dois; em 07/2026, 17 Test Automated foram fechadas com idade média de 699 dias.
- O relatório é da versão e do processo, **não compara pessoas**.
- Número que não deu para obter aparece como "sem dado", com o motivo. A skill nunca estima calado.
- As métricas do esforço vêm do Test de Delivery (`[DiasEstimados]`, `[NrTesters]`…). Por isso é importante manter esse formato na descrição, como a `criar-task-jira` já faz.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `SKILL.md` | o fluxo: versão e corte, dados, recomendações, página e publicação |
| `references/metricas.md` | as definições, fórmulas e consultas, com os números da 9.068 como exemplo |
| `references/pagina.md` | a ordem das seções e as regras de conteúdo e forma |

## Instalação

Copie a pasta `relatorio-qualidade/` inteira, com `references/`, em `~/.claude/skills/` ou em `.claude/skills/` do workspace.
