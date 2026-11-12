---
name: orcamento-modelo-antigo
description: Orça quantas horas um cenário NOVO de teste automatizado (TotalUiTest / lavenderepda) levaria no MODELO ANTIGO de QA da WMW, antes da IA, usando o histórico real do Jira (Test Automated) como régua, e registra o orçamento no Original Estimate da atividade Test Automated no Jira — criando a atividade se ela ainda não existir. Calcula também o % de redução contra as horas reais do modelo novo. Use SEMPRE que o usuário pedir orçamento, estimativa, levantamento ou comparativo de horas, ganho ou redução com IA, "quanto tempo levaria no formato antigo", Original Estimate de uma Test Automated, ou mencionar horas orçadas / horas reais / % redução de uma atividade VENDAS-xxxxx ou de um cenário CTxxx-Txxx — mesmo que diga só "orça esse cenário". Para refatoração de cenário existente, use a skill orcamento-refatoracao.
---

# Orçamento de automação no modelo antigo

O objetivo é um número **defensável perante coordenação e gerência**: cada orçamento precisa ser explicável com atividades parecidas que de fato aconteceram no Jira. Um orçamento inflado que alguém desmonte olhando o histórico derruba a credibilidade do comparativo inteiro. Na dúvida, prefira o número conservador e justificado.

O orçamento termina **registrado no Jira**: Original Estimate da Test Automated com o total, e um comentário com a divisão e a justificativa.

## Escopo

| Test Case Type | Quem orça |
|---|---|
| Automação (cenário novo) | esta skill |
| Ajuste | esta skill (normalmente 2–5 h no total) |
| Refatoração | skill `orcamento-refatoracao`. Se ela não estiver instalada, avise e use 40–60% do custo de criar do zero, reaproveitando só o SQL e o documento do **próprio** cenário |

## O processo antigo (o que está sendo orçado)

Cada etapa era feita por uma pessoa diferente, em sequência. Detalhes do documento do Confluence que o QA 1 produzia: `references/processo-antigo.md`.

1. **QA 1, Análise e configuração:** baixa o SQLite do ambiente de teste automatizado; estuda a funcionalidade; configura **na mão** tabelas, parâmetros e dados, debugando até o fluxo funcionar; gera o SQL de configuração; executa o fluxo e cria o documento no Confluence com **um print por passo**.
2. **QA 2, Codificação:** lê o documento e o SQL, cria a branch, codifica, estabiliza, roda Sonar e Checkstyle, commit e push.
3. **QA 3 ou programador:** code review; o QA 2 ajusta.
4. **QA 1 ou PO:** valida o cenário contra o documento.
5. **QA 2:** merge na develop.

As etapas 3 a 5 entram na coluna **Codificação**.

**Configuração nunca é reaproveitada.** Mesmo com um cenário parecido já automatizado, orce a configuração inteira do zero: cada cenário tinha o seu SQLite, a sua massa e o seu SQL. Cenários parecidos calibram o tamanho, nunca descontam horas.

**A divisão entre as colunas não é 50/50.** Regra de negócio pesada, massa grande ou funcionalidade pouco conhecida → Análise e configuração maior. Muitas telas, componentes que o TotalUiTest não trata ou muitas validações de tela → Codificação maior.

## Passo a passo

### 1. Entender o cenário

Aceite qualquer entrada: chave do Jira, cenário do Squash, classe Java do modelo novo ou descrição solta. Com a chave, leia a atividade pelo MCP interno (`get_jira_issue`): resumo, descrição (cenário, classe, link do Squash), Feature, Test Case Type, Original Estimate atual e Σ Time Spent. A classe Java, se existir, é ótimo insumo: conte passos, inserts de massa, parâmetros e telas.

Levante:

- quantidade de passos e de validações;
- telas e formulários, e se o fluxo muda de módulo (pedido → estoque → sincronização);
- parâmetros (simples e JSON) e tabelas da massa;
- cálculo a conferir (tributação, frete, rateio, desconto, estoque);
- se a funcionalidade é conhecida pelo time ou exige estudo longo;
- componente de tela que exigiria suporte novo no TotalUiTest (grid específica, grade, combo multisseleção, carrossel, botões de rodapé novos);
- o Test Case Type (Automação, Ajuste, Refatoração).

Se faltar algo que muda o porte (por exemplo, não dá para saber quantos passos), pergunte uma coisa só. Para o resto, assuma e registre a premissa.

### 2. Buscar análogos

1. **Histórico do modelo antigo** (`references/historico-jira.md`): 2 a 5 atividades parecidas por funcionalidade e tipo de fluxo, buscando por palavra-chave (estoque, bonificação, tributação, transportadora, cliente, NF-e, grade, desconto, verba, login, remessa…). Use só a seção **base** (concluídas, com horas, antes de 03/2026) e priorize 2024. Não concluídas só mostram que a funcionalidade já foi estudada; as do modelo com IA nunca entram como custo.
2. **Régua dos orçamentos já feitos** (`references/orcamentos-calibracao.md`) e, ao vivo, o Original Estimate das Test Automated mais recentes da mesma Feature (JQL no fim desse arquivo). Um cenário parecido deve ter orçamento parecido.

Os números do histórico são **piso**: code review e validação com PO quase nunca foram lançados à parte.

### 3. Classificar o porte

| Porte | Total típico | Perfil |
|---|---|---|
| P — Simples | 6–10 h | 1 tela ou fluxo curto, ≤ 5 passos, massa pequena, sem cálculo, funcionalidade já automatizada antes |
| M — Médio | 14–24 h | pedido completo com uma regra de negócio (estoque, bonificação, um tributo), 6–12 passos, massa média |
| G — Complexo | 28–40 h | várias regras combinadas, cálculos a conferir, vários formulários, replicação ou edição de pedido, primeira automação de um sub-módulo |
| GG — Muito complexo | 48 h ou mais | grade, cadastros com muitas abas ou campos dinâmicos, fluxos entre módulos, suporte novo no framework, primeira automação de um módulo inteiro |

Referência 2024 (Automação concluída): P25 14,5 h · mediana 19,9 h · P75 29,3 h. 2025 não teve automação nova concluída, então 2024 continua sendo a régua.

Ajustes:

- **Funcionalidade pouco conhecida** ou sem boa documentação: +30–50% na Análise e configuração.
- **Suporte novo no TotalUiTest:** +4–8 h na Codificação.
- **Cenário parecido já existente:** não reduz nada.

### 4. Dividir nas duas colunas

Estime por etapa e some, para o número ser auditável. Faixas para porte M (escale para os outros):

**Análise e configuração (QA 1)**

| Etapa | Faixa |
|---|---|
| baixar o SQLite e subir o ambiente | 1–2 h |
| estudo da funcionalidade | 1–6 h |
| configuração manual de tabelas, parâmetros e dados + debug | 3–8 h |
| geração do SQL de configuração e teste do script | 1–2 h |
| execução do fluxo + documento no Confluence com print por passo | 2–4 h |

**Codificação (QA 2, review, validação, merge)**

| Etapa | Faixa |
|---|---|
| leitura do documento e do SQL, alinhamento, branch | 0,5–1 h |
| codificação (ids, Page, asserts) | 3–8 h |
| estabilização + Sonar/Checkstyle + commit | 1–3 h |
| code review + ajustes | 1–2 h |
| validação do cenário (QA 1 ou PO) | 0,5–1 h |
| merge na develop | 0,5 h |

Arredonde cada coluna para hora cheia.

### 5. Conferir contra o histórico

- Acima do **P75** dos análogos: a justificativa precisa dizer o que este cenário tem a mais.
- Muito abaixo: confira se não esqueceu etapa.
- Histórico daquela funcionalidade bem menor que o orçado (ex.: login levou 1,5 h e 4,8 h): **avise explicitamente**. É o ponto que um gerente questionaria.

### 6. Calcular a redução (quando houver horas reais)

Horas reais = **Σ Time Spent** da atividade no Jira (`time_spent_h` do `get_jira_issue`, que inclui subtasks e retrabalho). É o número que a gerência confere, e o mais conservador. Se o tester informar outro valor, use o dele e avise quando divergir do Jira.

Faça a conta com o script, para não errar hh:mm:

```
python scripts/calcular_reducao.py --analise 12 --codificacao 12 --reais 3:25
```

Restante = total − reais; % Redução = restante ÷ total, com duas casas e vírgula (24 h e 3:25 → 85,76%). Atividade ainda sem horas lançadas: deixe reais, restante e % em branco.

### 7. Apresentar e pedir aprovação

Mostre o orçamento (formato abaixo) e pergunte:

> Posso registrar no Jira? Original Estimate `<total>h` na `<VENDAS-xxxxx>` e o comentário com a justificativa.

### 8. Registrar no Jira

Pelo Chrome, seguindo `references/registro-jira.md`:

- **A atividade existe:** Original Estimate = total orçado; comentário com a divisão, o porte, os análogos e as premissas. Se o Original Estimate já tiver outro valor, mostre os dois e pergunte antes de trocar.
- **A atividade não existe:** crie a Test Automated com a skill `criar-task-jira` (tipo Test Automated, GUIA-JIRA-003), já com o Original Estimate orçado, e depois comente. Sem a `criar-task-jira`, crie pelo Chrome conforme `references/registro-jira.md`.

Sem Chrome: entregue o valor do Original Estimate e o texto do comentário prontos para o tester colar.

Termine com o link `https://jira2.wmw.com.br/browse/<CHAVE>`.

## Formato da resposta

1. A linha do orçamento:

| Atividade | Cenário | Análise e configuração | Codificação | Total (Original Estimate) | Horas reais (Σ Jira) | Restante | % Redução |
|---|---|---|---|---|---|---|---|

Horas em `hh:mm:ss`; % com vírgula.

2. **Justificativa** curta: porte, análogos (chave e horas), ajustes e premissas.
3. **Detalhamento por etapa** (as faixas do passo 4 com o valor escolhido).
4. Se algo for frágil frente ao histórico, um alerta de uma frase.
5. A pergunta de aprovação do passo 7.

Seja direto. Não explique o processo antigo na resposta: ele orienta a estimativa.

## Armadilhas

- **`resolution = Concluída` não funciona no JQL** (o Jira recusa o valor). Use `resolution is not EMPTY`.
- **`time_spent_h` é a soma com as subtasks** (Σ); `time_spent_own_h` é só da atividade. As horas reais do comparativo são o Σ.
- **Fechamento não é automação.** Test Automated antigas fechadas sem horas (limpeza da fila, como as 17 de 07/2026 com idade média de 699 dias) não servem de análogo nem de horas reais.
- **Atividade do modelo com IA nunca é análogo de custo** (a partir de 03/2026).
- **O histórico é piso:** code review e validação quase nunca foram lançados à parte.
- **Formato do Original Estimate na tela:** `24h`, `18h 30m`. E ele guarda só o total; a divisão vai no comentário.

## Cuidados

- Nada vai para o Jira sem aprovação.
- Não sobrescreva Original Estimate preenchido sem perguntar, nem apague comentários.
- O Original Estimate é o **total**; a divisão entre colunas vai só no comentário.
- Bugs achados na construção com IA podem ser citados no comentário, mas não entram na conta de horas.
- Na tela de login do Jira, peça para o tester entrar. Nunca digite senha.
