# orcamento-modelo-antigo

Skill do Claude que **orça quantas horas um cenário novo de teste automatizado levaria no modelo antigo de QA** (antes da IA) e **registra o orçamento no Jira**, no Original Estimate da atividade Test Automated. Se a atividade ainda não existe, ela é criada. Com horas reais lançadas, a skill calcula também o % de redução do modelo com IA.

## Para que serve

- **Dá um número defensável:** cada orçamento é comparado com atividades parecidas que de fato aconteceram no Jira (histórico de 2022 a 2026), e a skill avisa quando o número destoa do histórico.
- **Mostra a conta:** divide o total em Análise e configuração e Codificação, etapa por etapa, com o porte (P, M, G, GG) e as premissas.
- **Registra no Jira:** Original Estimate com o total e um comentário com a divisão, os análogos e as premissas.
- **Calcula a redução:** usa o Σ Time Spent da atividade (inclui subtasks) como horas reais.

## Quando usar

A skill entra sozinha quando você pede orçamento ou estimativa de horas de automação. Por exemplo:

- "orça esse cenário";
- "quanto tempo a VENDAS-25438 levaria no formato antigo?";
- "preenche o Original Estimate dessa Test Automated";
- "qual a redução com IA da VENDAS-20462?".

Para chamar direto: `/orcamento-modelo-antigo`.

**Refatoração** de cenário existente é com a skill `orcamento-refatoracao`.

## O que você precisa ter

- **MCP interno da WMW** (leitura de Jira): para ler a atividade, os análogos e as horas reais.
- **Claude in Chrome** conectado e você **logado no Jira**, para gravar o Original Estimate e o comentário. A skill nunca digita senha.
- **Opcional:** a skill `criar-task-jira`, que cria a Test Automated quando ela ainda não existe.

Sem o Chrome, você recebe o valor do Original Estimate e o comentário prontos para colar.

## Como usar

1. **Peça o orçamento** com a chave da Test Automated, o cenário do Squash, a classe Java ou uma descrição.
2. **Responda à pergunta**, se houver (no máximo uma, quando falta algo que muda o porte).
3. **Revise** o total, a divisão, os análogos e os alertas.
4. **Aprove o registro.** A skill grava no Jira (ou cria a atividade) e devolve o link.

## Como a skill orça

| Porte | Total típico | Perfil |
|---|---|---|
| P | 6–10 h | fluxo curto, até 5 passos, sem cálculo |
| M | 14–24 h | pedido completo com uma regra de negócio |
| G | 28–40 h | várias regras, cálculos, vários formulários |
| GG | 48 h ou mais | grade, fluxos entre módulos, suporte novo no framework |

Regras fixas:

- **A configuração é sempre orçada do zero**: no modelo antigo, cada cenário tinha o seu banco, a sua massa e o seu SQL. Cenário parecido calibra o tamanho, não dá desconto.
- **A divisão não é 50/50:** regra pesada aumenta a Análise e configuração; muitas telas aumentam a Codificação.
- **O histórico é piso:** code review e validação quase nunca foram lançados à parte.
- Funcionalidade pouco conhecida: +30–50% na análise. Suporte novo no TotalUiTest: +4–8 h na codificação.

## Bom saber

- O **Original Estimate é o total**. A divisão entre as colunas fica no comentário.
- Se a atividade já tem Original Estimate diferente, a skill pergunta antes de trocar.
- Bugs achados durante a construção com IA podem ir no comentário, mas não entram na conta.
- Para conferir a régua com orçamentos recentes, a skill lê o Original Estimate das Test Automated criadas desde 03/2026.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `SKILL.md` | o fluxo: entender, buscar análogos, porte, divisão, conferência, redução, aprovação e registro |
| `references/historico-jira.md` | histórico do modelo antigo: estatísticas por tipo, ano e funcionalidade, e a lista de atividades para análogos |
| `references/orcamentos-calibracao.md` | os primeiros orçamentos do comparativo, com as horas reais, e como achar os mais novos no Jira |
| `references/processo-antigo.md` | o documento de teste que o QA 1 fazia no Confluence (para orçar a documentação) |
| `references/registro-jira.md` | como gravar o Original Estimate, criar a Test Automated e o modelo do comentário |
| `scripts/calcular_reducao.py` | conta de total, restante e % de redução em hh:mm:ss |

## Instalação

Copie a pasta `orcamento-modelo-antigo/` inteira, com `references/` e `scripts/`:

- **Claude Code**: em `~/.claude/skills/`, ou em `.claude/skills/` do projeto;
- **claude.ai**: suba a pasta como skill nas configurações de Skills.
