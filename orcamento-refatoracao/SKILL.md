---
name: orcamento-refatoracao
description: Orça quantas horas a REFATORAÇÃO de um teste automatizado legado para o novo padrão TotalUiTest (cenário do Confluence migrado para o Squash TM, massa .sql migrada para @InvokeInit com ParametrosTestUtil/TabelasTestUtil, nomenclatura, JavaDoc e comentários de passo) levaria no MODELO ANTIGO, sem IA, a partir de uma auditoria do cenário antigo, e registra o orçamento no Original Estimate da atividade Test Automated no Jira — criando a atividade se ela ainda não existir. Calcula também o % de redução contra as horas reais. Use SEMPRE que o usuário pedir orçamento, estimativa ou comparativo de horas de uma refatoração, migração de cenário para o novo padrão, atividade com Test Case Type "Refatoração", cenário com link de cenário anterior CT-LVP no Jira, ou perguntar quanto custaria refatorar ou migrar um teste antes da IA — mesmo que diga só "orça essa refatoração". Para cenário novo, use a skill orcamento-modelo-antigo.
---

# Orçamento de refatoração no modelo antigo

Esta skill orça a refatoração de um teste que **já existia**: o cenário legado do Confluence (CT-LVP-x-y) vira um caso no Squash TM e o código é migrado para o novo padrão. O número é o custo de fazer **essa mesma refatoração à mão**, não o de criar o cenário do zero. Orçar refatoração como criação infla o ganho e é o primeiro número que alguém contesta olhando o Jira.

Refatorações são analisadas **separadas** das criações: os percentuais de redução são diferentes e misturar os dois distorce a média.

O orçamento termina **registrado no Jira**: Original Estimate da Test Automated com o total, e um comentário com a auditoria, a divisão e a justificativa.

## 1. Reunir o material

Com a chave da atividade, leia pelo MCP interno (`get_jira_issue`): descrição (Cenário, Teste, **Cenário anterior**, Link do Squash), Feature, Test Case Type, Original Estimate atual e Σ Time Spent.

Depois busque o cenário legado:

| Material | Onde |
|---|---|
| Documento do cenário antigo (CT-LVP-x-y) | link "Cenário anterior" da atividade; leia com `get_confluence_page` (o id está na URL) ou ache com `search_knowledge_base` pelo código CT-LVP |
| `.java` e `.sql` legados | no repositório `totaluitest`, se estiver disponível: a classe atual, ou a versão antes da refatoração no histórico do git (`git log --follow`). Senão, peça ao tester |
| Utils que montam massa | as classes que o `.java` legado chama (ex.: `UtilAgenda.populaAgendaVisita`) |
| Caso novo no Squash | o link do Squash da atividade, se já existir |

Se o tester mandar uma lista de pontos de ajuste, use-a como ponto de partida e faça a sua auditoria mesmo assim.

## 2. Classificar o tipo

| Tipo | Quando | Como orçar |
|---|---|---|
| **R1 — Migração de padrão** | Mesmos passos, mesma regra, mesma massa. Muda a forma: Confluence → Squash, .sql → `@InvokeInit`, nomes, JavaDoc, comentários, mensagens dos asserts | componentes desta skill |
| **R2 — Migração com correção** | Durante a migração apareceu problema no cenário: validação faltando ou errada, massa inconsistente, passo que não testava o que dizia, regra que mudou. Parte do cenário precisa ser reconfigurada e revalidada | R1 + componentes R2 (seção 5) |
| **R3 — Reescrita** | O cenário muda de verdade: passos novos, outra regra, massa refeita | **não use esta skill**: use `orcamento-modelo-antigo`, como automação nova (configuração nunca é reaproveitada) |
| **Ajuste** | Troca de link, nome, mensagem, um assert | não orce individualmente; agrupe numa atividade de ajuste em lote |

A classificação sai da auditoria: qualquer erro além da forma (nomes, JavaDoc, comentários, mensagens) faz a refatoração ser **R2**. Só pergunte "o cenário mudou alguma coisa além do padrão?" quando não houver código nem cenário legado para auditar.

## 3. Auditar o cenário antigo (obrigatório)

Leia o cenário legado inteiro (`.java`, `.sql`, utils de massa e documento) e liste **todos** os erros. Parta do princípio de que **todos precisam ser corrigidos na refatoração**: o orçamento é o custo de entregar o cenário migrado e correto, não só migrado.

| Categoria | O que procurar |
|---|---|
| Falso positivo | `return`, `if` ou `try/catch` que deixa o teste verde sem testar (ex.: fim de semana); assert que compara uma variável com ela mesma ou reaproveita um valor lido em passo anterior; `assertNotNull`/`assertTrue` onde cabe `assertEquals` com o valor esperado; `startsWith`/`contains` no lugar da string completa; Resultado Esperado que repete o anterior; passo sem validação; contagem que não garante qual item foi validado |
| Massa | divergência entre o SQL e o cenário (parâmetro com valor diferente, parâmetro sem finalidade documentada); parâmetro JSON gravado com replace inteiro (o util faz patch: precisa do Map com todas as chaves); data fixa; massa vinda de util compartilhado que precisa ser trazida para a classe; colunas de auditoria que o padrão não usa |
| Sincronização | `waitOpening` faltando depois de ação que abre tela, combo ou mensagem; `waitOpening` redundante; espera no lugar errado (início do passo seguinte) |
| Asserções | mensagem de falha que não corresponde ao campo validado, duplicada ou escrita como afirmação; acentuação |
| Pages e código | método chamado na Page errada; login fora da `LoginPage`; método que não existe na Page certa; variáveis mortas, fora do escopo ou que deveriam ser `final`; import errado; nome de classe e método fora do padrão |
| Documentação | JavaDoc fora do padrão (link do Confluence, "Versão 1.0", prefixo CT-LVP); comentários de passo de uma linha; passo sem Resultado Esperado correspondente; numeração fora de sequência |

Classifique cada erro:

- **simples**: mensagem, wait, variável, nome, comentário. Troca local, sem revalidar o fluxo.
- **de correção**: falso positivo, validação nova, divergência de massa. Exige reconfigurar ou executar de novo para saber o valor esperado. São estes que tornam a refatoração R2.

## 4. Medir o tamanho

Use o script em vez de contar a olho:

```
python scripts/medir_refatoracao.py Teste.sql TesteAntigo.java [TesteNovo.java]
```

Ele conta no `.sql`: INSERT, UPDATE, DELETE, parâmetros (`TBLVPVALORPARAMETRO`), parâmetros JSON e expressões de data do SQLite. No `.java`: passos, Resultados Esperados, asserts, `waitOpening`, `TabelasTestUtil`, `setParametro` e datas.

Os DELETE do legado são descartados na migração: não custam conversão, mas exigem conferir se a massa continua íntegra. Sem arquivos, estime pelos passos do cenário e pela lista de pré-condições do documento.

## 5. Montar o orçamento por componente

No processo antigo, a refatoração também passava por duas pessoas, code review, validação e merge.

**Análise e configuração (QA 1)**

| Componente | Referência |
|---|---|
| Ler o teste antigo, o .sql e o documento; entender o cenário | 0,5–2 h |
| Baixar o SQLite, subir o ambiente e executar o cenário legado para confirmar o comportamento atual | 1–2 h |
| Migrar o documento do Confluence para o Squash (pré-condições, passos, resultados esperados, rastreabilidade) | ~15 min por passo, mínimo 1 h |
| **Só R2:** reconfigurar na mão a parte afetada, debugar, atualizar o SQL e revalidar | 2–6 h; como régua, ~30 min por erro de correção |

**Codificação (QA 2, review, validação, merge)**

| Componente | Referência |
|---|---|
| Converter a massa à mão para `ParametrosTestUtil`/`TabelasTestUtil` | 0,5 h + ~5 min por INSERT/UPDATE + ~10 min por parâmetro JSON ou expressão de data |
| Renomear classe e método, JavaDoc com link do Squash, comentários de Passo/Resultado Esperado, mensagens dos asserts | ~10 min por passo, mínimo 1 h |
| Ajustar Page/ids se o código antigo agrupava ações no Page ou usava métodos que mudaram | 0–3 h |
| **Só R2:** codificar as correções da auditoria (asserts novos ou reescritos, remoção de falso positivo, waits que faltavam) | ~15–20 min por erro de correção (os simples já estão na linha de renomeação e mensagens) |
| Executar, depurar diferenças da massa migrada, estabilizar | 1–3 h |
| Sonar, Checkstyle, commit | 0,5 h |
| Code review + ajustes | 0,5–1,5 h |
| Validação do cenário (QA 1 ou PO) | 0,5 h |
| Merge na develop | 0,5 h |

Some, arredonde cada coluna para hora cheia e confira a faixa:

| Tipo | Faixa |
|---|---|
| R1 pequena (login, até 4 passos, massa curta) | 6–9 h |
| R1 média (pedido, 6–10 passos, 10–25 inserts) | 10–14 h |
| R1 grande (muitos passos, massa extensa, vários parâmetros JSON) | 15–20 h |
| R2 | R1 + 2–8 h |

R1 acima de 20 h provavelmente é R2 ou R3: revise a classificação. Uma R2 pode passar de R1 + 8 h quando a auditoria encontra muitos erros de correção; aí a justificativa precisa citar a lista.

## 6. Conferir contra o histórico

Veja `references/historico-refatoracao.md`. O histórico do modelo antigo é pequeno e misturado com refatorações de framework, então a régua vem principalmente dos componentes. Os casos comparáveis ficaram entre 6 h e 10 h. Compare também com as refatorações recentes do Jira (JQL no fim do arquivo): mesma massa e mesmo tipo devem dar orçamento parecido.

## 7. Calcular a redução (quando houver horas reais)

Horas reais = **Σ Time Spent** da atividade no Jira (`time_spent_h`, inclui subtasks e lançamentos posteriores, como merge). Se o tester informar outro valor, use o dele e avise quando divergir.

```
python scripts/calcular_reducao.py --analise 4 --codificacao 4 --reais 1:27
```

(8 h e 1:27 → restante 6:33:00 → 81,88%.) Sem horas reais, deixe reais, restante e % em branco.

## 8. Apresentar e pedir aprovação

Mostre o orçamento (formato abaixo) e pergunte:

> Posso registrar no Jira? Original Estimate `<total>h` na `<VENDAS-xxxxx>` e o comentário com a auditoria e a justificativa.

## 9. Registrar no Jira

Pelo Chrome, seguindo `references/registro-jira.md`:

- **A atividade existe:** Original Estimate = total; comentário com tipo, erros da auditoria, divisão e premissas. Original Estimate já preenchido com outro valor: mostre os dois e pergunte antes de trocar.
- **A atividade não existe:** crie a Test Automated (Test Case Type `Refatoração`, com o link do cenário anterior) com a skill `criar-task-jira`, já com o Original Estimate, e depois comente. Sem a `criar-task-jira`, crie pelo Chrome conforme `references/registro-jira.md`.

Sem Chrome: entregue o valor do Original Estimate e o texto do comentário prontos para colar. Termine com o link `https://jira2.wmw.com.br/browse/<CHAVE>`.

## Formato da resposta

1. A linha do orçamento:

| Atividade | Cenário | Tipo | Análise e configuração | Codificação | Total (Original Estimate) | Horas reais (Σ Jira) | Restante | % Redução |
|---|---|---|---|---|---|---|---|---|

Horas em `hh:mm:ss`, % com vírgula.

2. **Erros encontrados no cenário antigo**, agrupados pelas categorias da seção 3, cada um marcado como simples ou de correção, indicando o que veio da lista do tester e o que a auditoria acrescentou. Todos entram no orçamento.
3. **Justificativa** curta: tipo (R1/R2) e por quê, medidas (passos, inserts, parâmetros, erros de correção), premissas.
4. **Detalhamento por componente**.
5. Alerta de uma frase quando algo for frágil (por exemplo, refatoração acima de 20 h sem correção de cenário documentada).
6. A pergunta de aprovação.

## Armadilhas

- **Refatoração não é criação.** Orçar como cenário novo infla o ganho e é o primeiro número contestado.
- **A classe pode ter mudado de nome.** Para achar a versão legada, use `git log --follow` no arquivo atual.
- **Encoding do legado.** Os `.java` são ISO-8859-1: o script de medição lê com substituição, então acento torto não afeta a contagem.
- **DELETE do legado não custa conversão**, mas exige conferir se a massa continua íntegra.
- **`resolution = Concluída` não funciona no JQL**; use `resolution is not EMPTY`. E `time_spent_h` é o Σ com as subtasks.
- **Link curto do Confluence** (`wiki.wmw.com.br/confluence/x/<código>`): o código é o id da página em base64 (little-endian), com `-` → `/` e `_` → `+`.

## Cuidados

- Nada vai para o Jira sem aprovação.
- Não sobrescreva Original Estimate preenchido sem perguntar, nem apague comentários.
- O Original Estimate é o **total**; divisão e auditoria vão no comentário.
- A skill só lê o código: a auditoria aponta os erros, não os corrige.
- Na tela de login do Jira, peça para o tester entrar. Nunca digite senha.
