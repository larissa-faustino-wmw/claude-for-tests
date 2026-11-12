# Test Automated — atividade de teste automatizado

**Guia:** [GUIA-JIRA-003 - Como criar atividade de teste automatizado no Jira](https://confluence.wmw.com.br/confluence/x/GwDdQQ) (conferido na versão 1, em 10/11/2026). Labels: [PQA-JIRA-000 - Labels de Teste Automatizado](https://confluence.wmw.com.br/confluence/display/qualidade/PQA-JIRA-000-Labels+de+Teste+Automatizado) (versão 13). Se um dos dois mudar, atualize este arquivo.

Criação: botão **Create** → Project `Vendas` → Issue Type `Test Automated`.

## O que já existe (antes de perguntar)

Além da busca por palavras-chave do `SKILL.md`, busque atividades de Test Automated do mesmo cenário ou da mesma classe de teste (`project = VENDAS AND issuetype = "Test Automated" AND text ~ "<cenário ou classe>"`). Se o cenário já tem atividade aberta, avise.

## O que perguntar (só o que faltar)

- **Test Case Type**, se o relato não deixar claro.
- **Cenário**: nome do cenário e classe do teste (se já existir).
- **Origem**: cenário anterior no Confluence (CT-LVP), atividade em que se baseia (VENDAS-xxxxx), cenário do Squash em que se baseia, link do caso de teste no Squash. O que não se aplicar fica `N/A`.
- **Original Estimate**: as horas orçadas. Se o tester não tiver, (sugestão) ofereça calcular com a skill `orcamento-modelo-antigo` (cenário novo) ou `orcamento-refatoracao` (refatoração).
- **Affects Version/s**: a versão em que o cenário foi sugerido, se não der para deduzir.
- **Labels de origem e de construção** (ver abaixo), se o relato não disser.

## Campos

| # | Campo | Valor | Perguntar? |
|---|---|---|---|
| 1 | Issue Type | `Test Automated` | não |
| 2 | Priority | `Medium` | não |
| 3 | Summary | resumo do cenário, no padrão `Tela - descrição curta`. Nunca genérico | não |
| 4 | Component/s | **em branco na criação**; preenchido só depois, com as classes criadas ou alteradas | não |
| 5 | Features Involved | tags das funcionalidades validadas, já existentes no Jira. Ex.: tributação personalizada → `Pedido`, `Venda`, `Tributacao`, `TributacaoPersonalizada`. Escolha da lista; não crie tag nova sem o tester confirmar | não, salvo dúvida |
| 6 | Test Case Type | `Automação` (novo cenário), `Ajuste` (cenário existente), `Refatoração` (cenário existente), `Pesquisa/Análise` (estudo ou viabilidade), `Descontinuação` (cenário descontinuado) | se não estiver claro |
| 7 | Reporter | o QA logado | não |
| 8 | Description | modelo abaixo | — |
| 9 | Feature | a funcionalidade principal (Módulo > Funcionalidade) | não, salvo dúvida |
| 10 | Customer | sempre `WMW` | não |
| 11 | Due date | em branco | não |
| 12 | Original Estimate | horas orçadas para automatizar | **sim, se não veio** |
| 13 | Remaining Estimate | em branco | não |
| 14 | Affects Version/s | versão em que foi sugerido | se não der para deduzir |
| 15 | Fix Version/s | **em branco na criação**; preenchido ao finalizar o teste | não |
| 16 | Labels | conforme PQA-JIRA-000 (abaixo) | se não der para deduzir |
| 17 | Attachment | logs, prints, vídeo | — |

## Labels (PQA-JIRA-000)

Use uma label de **origem** e uma de **construção**, mais as de situação quando couberem:

| Grupo | Label | Quando |
|---|---|---|
| Origem | `QA_ORIGIN_AI` | atividade encontrada ou sugerida pela IA |
| Origem | `QA_ORIGIN_TESTER` | a ideia veio de alguém do time de testes |
| Origem | `QA_ORIGIN_ISSUE` | o cenário veio de uma Story, Bug ou Defect anterior — vincule a issue de origem em Linked Issues |
| Origem | `QA_ORIGIN_LEGACY` | veio de cenário antigo do Confluence, pela triagem |
| Construção | `QA_BUILD_AI` | construído com auxílio da IA; o tester dirige o fluxo e revisa |
| Construção | `QA_BUILD_TESTER` | construído manualmente por um tester |
| Situação | `QA_REVIEW_AI` | demanda refatorada ou revisada pela IA |
| Situação | `QA_STUDY_AI` | estudo de IA sobre melhoria de qualidade |
| Situação | `QA_BUG_FOUND` | o teste encontrou um defeito real e abriu um Defect (normalmente incluída depois, durante a automação) |

## Modelo de descrição

Sem seções: uma linha por informação, em Paragraph.

```
Cenário: <nome do cenário>
Teste: <classe do teste>
Cenário anterior: <link CT-LVP do Confluence ou N/A>
Baseado na atividade: <VENDAS-xxxxx ou N/A>
Baseado no cenário: <link do Squash ou N/A>
Link do Squash: <link do caso de teste>
```

No modo Text, para cada informação ficar numa linha sem virar parágrafos separados, termine as linhas com `\\` (quebra de linha do Jira) ou deixe uma linha em branco entre elas. Links podem ir como `[texto|url]` ou só a URL.
