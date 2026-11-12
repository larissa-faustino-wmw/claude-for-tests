# orcamento-refatoracao

Skill do Claude que **orça quantas horas a refatoração de um teste automatizado legado** para o novo padrão TotalUiTest levaria no modelo antigo (sem IA) e **registra o orçamento no Jira**, no Original Estimate da Test Automated. Se a atividade ainda não existe, ela é criada. O orçamento parte de uma **auditoria do cenário antigo**: todos os erros encontrados entram na conta.

Refatoração aqui é: o cenário do Confluence (CT-LVP-x-y) migrado para o Squash, a massa `.sql` migrada para `@InvokeInit` com `ParametrosTestUtil`/`TabelasTestUtil`, e nomes, JavaDoc, comentários de passo e mensagens dos asserts no padrão novo.

## Para que serve

- **Audita o cenário antigo:** falsos positivos, massa divergente, waits faltando, asserts fracos, Pages erradas, documentação fora do padrão. Cada erro é marcado como simples ou de correção.
- **Classifica a refatoração:** R1 (só migração de padrão), R2 (migração com correção) ou R3 (reescrita, que é orçada como cenário novo pela `orcamento-modelo-antigo`).
- **Mede o tamanho com script:** INSERT/UPDATE, parâmetros, JSON, datas, passos e asserts.
- **Orça por componente**, com faixas de conferência, e registra no Jira com um comentário que mostra a auditoria e a conta.
- **Calcula a redução** com o Σ Time Spent da atividade.

## Quando usar

- "orça essa refatoração";
- "quanto custaria refatorar o EmitirPedidoTributacaoPersonalizadaFecopTipoQuatroTest no modelo antigo?";
- "preenche o Original Estimate da VENDAS-24958";
- qualquer Test Automated com Test Case Type "Refatoração" ou com link de cenário anterior CT-LVP.

Para chamar direto: `/orcamento-refatoracao`. Cenário **novo** é com a `orcamento-modelo-antigo`.

## O que você precisa ter

- **MCP interno da WMW**: lê a atividade, o documento CT-LVP no Confluence e as horas reais.
- **O código legado**: o repositório `totaluitest` na máquina (a skill acha a versão antiga no histórico do git) ou os arquivos `.java` e `.sql` colados no chat.
- **Claude in Chrome** conectado e você **logado no Jira**, para gravar. A skill nunca digita senha.
- **Opcional:** a skill `criar-task-jira`, que cria a Test Automated quando ela não existe.

## Como usar

1. **Peça o orçamento** com a chave da atividade ou o nome da classe. Se você já tem uma lista de pontos de ajuste, mande junto: a skill parte dela e acrescenta o que encontrar.
2. **Revise a auditoria**: os erros listados são o que justifica o número.
3. **Revise o orçamento**: tipo, total, divisão e alertas.
4. **Aprove o registro.** A skill grava o Original Estimate e o comentário (ou cria a atividade) e devolve o link.

## Faixas de conferência

| Tipo | Faixa |
|---|---|
| R1 pequena (até 4 passos, massa curta) | 6–9 h |
| R1 média (6–10 passos, 10–25 inserts) | 10–14 h |
| R1 grande (muitos passos, massa extensa, JSON) | 15–20 h |
| R2 | R1 + 2–8 h |

R1 acima de 20 h é sinal de que a classificação está errada. As poucas refatorações comparáveis do modelo antigo ficaram entre 6 h e 10 h.

## Bom saber

- **Todos os erros da auditoria entram no orçamento**: o custo é entregar o cenário migrado *e correto*.
- A skill **só lê** o código: aponta os erros, não corrige.
- Refatorações são analisadas **separadas** das criações, porque os percentuais de redução são diferentes.
- O **Original Estimate é o total**; a divisão e a auditoria ficam no comentário.
- Original Estimate já preenchido com outro valor: a skill pergunta antes de trocar.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `SKILL.md` | o fluxo: material, tipo, auditoria, medição, componentes, conferência, redução, aprovação e registro |
| `references/historico-refatoracao.md` | refatorações do modelo antigo e do modelo com IA, e a consulta das mais novas no Jira |
| `references/registro-jira.md` | como gravar o Original Estimate, criar a Test Automated e o modelo do comentário |
| `scripts/medir_refatoracao.py` | conta INSERT/UPDATE/DELETE, parâmetros, JSON e datas no `.sql`; passos, asserts e waits no `.java` |
| `scripts/calcular_reducao.py` | conta de total, restante e % de redução em hh:mm:ss |

## Instalação

Copie a pasta `orcamento-refatoracao/` inteira, com `references/` e `scripts/`:

- **Claude Code**: em `~/.claude/skills/`, ou em `.claude/skills/` do projeto;
- **claude.ai**: suba a pasta como skill nas configurações de Skills.
