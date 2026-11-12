---
name: prioriza-automacao
description: Sugere o que automatizar a seguir no Lavendere a partir de uma versão (padrão) — analisa todas as atividades da versão (entregas e correções), os Defects encontrados, os bugs que elas causaram e o histórico de bugs das features, confere o que já está automatizado (Test Automated, totaluitest no App, webuitest na Web) e devolve a lista priorizada de cenários de automação, App e Web, cada um com os bugs que o justificam. O QA avalia a lista e, só depois da aprovação, os escolhidos viram atividades Test Automated no board de automação do Jira. Também revisa a fila (o board de Test Automated abertas): o que puxar a seguir, o que fechar por já estar automatizado, duplicado ou obsoleto, o que juntar e os dados a corrigir. Use SEMPRE que o usuário pedir para revisar, limpar ou ordenar a fila ou o board de automação, ou que o usuário pedir o que automatizar, prioridade ou fila de automação, backlog de testes automatizados, onde a automação falta, sugestões de cenários automatizados de uma versão 9.xxx, ou cobertura de automação por feature — mesmo que diga só "o que vale automatizar da 9.070?".
---

# Priorização de automação

O objetivo é colocar a automação onde o bug está. Os dados mostram que o esforço histórico nem sempre acompanhou a dor: em 11/2026, Estoque Padrão tinha 45 automações e não estava entre as áreas com mais bugs, enquanto Pedidos Pendentes, Desconto Diversos, Orçamentos, Títulos Financeiros e Condição de Pagamento tinham zero automação e bugs subindo. Cada sugestão desta skill precisa vir com os bugs que ela teria pegado.

## Regras que não se negociam

1. **O escopo padrão é uma versão.** Se o usuário não disser a versão, pergunte qual (sugira a última liberada e a em Delivery, com `jira_release_ranking`). Período em dias ou uma atividade específica só quando o usuário pedir explicitamente.
2. **Nada é criado no Jira antes de o QA avaliar a lista completa.** Primeiro todas as sugestões, numeradas; o QA aprova, descarta ou ajusta; só então as aprovadas viram Test Automated.
3. **Toda sugestão tem evidência:** a atividade da versão, o Defect ou o bug (chave), e o Root Cause quando houver.
4. **App e Web.** O App automatiza com o TotalUiTest; a Web, com o `webuitest` (Playwright). A Web ainda está começando: sugira cenários Web normalmente, marcando a plataforma e o que o `webuitest` ainda não tem (`references/automacao-web.md`).
5. **Somente leitura até a aprovação.**

## Modos

| Modo | Pedido | Onde |
|---|---|---|
| **Sugerir** (padrão) | "o que automatizar da 9.070?" | o fluxo abaixo |
| **Revisar a fila** | "revisa a fila de automação", "limpa o board" | `references/revisao-fila.md` |

Na revisão da fila, as mesmas regras valem: evidência para cada decisão, a lista completa para o QA avaliar e nada alterado no Jira antes da aprovação.

## Fluxo (modo sugerir)

### 1. Definir o escopo

| Pedido | Escopo |
|---|---|
| versão (padrão) | todas as atividades com fixVersion na versão (patches inclusos), mais os bugs com versão afetada nela |
| período (só se pedido) | bugs e Defects criados no período e as entregas resolvidas nele |
| atividade (só se pedido) | a atividade, seus Defects, o que ela causou e a feature dela |

### 2. Levantar os dados

Detalhes e consultas em `references/fontes-dados.md`. Para uma versão:

1. **Resumo da versão:** `jira_release_impact` (entregas, correções, Defects internos, o que causou problema confirmado, features suspeitas de regressão).
2. **As atividades:** `search_jira_jql` com `project = VENDAS AND fixVersion in (<versão e patches>) AND issuetype in (Story, Bug)`. Para cada uma: Feature, plataforma, critérios de aceite e os Defects (subtasks) encontrados no teste.
3. **O que quebrou:** bugs cujo Issue Cause cita uma atividade da versão, e bugs com versão afetada na versão (Root Cause de cada um).
4. **Histórico das features da versão:** bugs dos últimos 180 dias por feature e tendência (`jira_feature_hotspots`), retrabalho (`jira_rework`).
5. **O que já está automatizado:** Test Automated por feature (`jira_aggregate`), testes do `totaluitest` por pasta de área, testes do `webuitest`, e Test Automated ainda abertas (o board) para não sugerir de novo o que já está na fila.

### 3. Gerar os candidatos

Para cada atividade da versão e para cada bug relevante, pergunte: **que teste automatizado teria pegado isso, ou vai impedir que volte?**

- **Atividade entregue (Story):** o fluxo principal do critério de aceite, se for regra ou cálculo; mais os side effects já registrados (Defects da atividade, análise da `analise-impacto`).
- **Correção (Bug):** o cenário que reproduz o bug corrigido, mais a variação próxima que o Root Cause indica (o mesmo erro em outro tipo de pedido, outro parâmetro).
- **Defect interno:** se o Defect apareceu no teste manual de uma regra, o cenário que o pegaria automaticamente.
- **Bug causado por uma atividade da versão:** prioridade alta — é regressão confirmada.

Agrupe candidatos que testam a mesma regra num cenário só.

### 4. Pontuar e filtrar

Com `references/pontuacao.md`: **dor** (bugs e Defects ligados, horas, produção, regressão confirmada, tendência da feature) × **automatizável** (regra e cálculo sim; visual, lentidão, integração externa, dado de cliente não) × **lacuna** (a feature tem pouca automação para a dor que tem).

Descarte, citando o motivo numa linha no fim da lista: o que já está automatizado, o que já está na fila, o que não é automatizável (lentidão, layout, ERP, serviço externo).

### 5. Apresentar a lista para avaliação

Formato em `references/modelo-saida.md`: o resumo da versão, a cobertura por feature (dor × automação) e **todas as sugestões numeradas**, em ordem de pontuação, cada uma com plataforma, cenário em uma frase, evidência, pontuação explicada e uma estimativa de porte (P/M/G/GG da `orcamento-modelo-antigo`).

Feche com:

> Avalie a lista: diga quais números aprovar, descartar ou ajustar. As aprovadas viram Test Automated no board de automação. Quer o orçamento das aprovadas antes de criar?

Ajustes voltam a este passo. Não crie nada antes da resposta.

### 6. Criar as aprovadas no Jira

Para cada aprovada, uma **Test Automated** pela skill `criar-task-jira` (tipo Test Automated, GUIA-JIRA-003), que faz a busca por duplicidade e mostra o formulário antes de criar. Valores desta skill:

| Campo | Valor |
|---|---|
| Summary | o cenário, sem texto genérico; Web com o prefixo `Web - ` |
| Test Case Type | `Automação` |
| Feature | a feature do cenário |
| Labels | `QA_ORIGIN_AI` (sugerida pela IA); `QA_ORIGIN_ISSUE` quando o cenário nasceu de um bug ou Defect específico |
| Linked Issues | a atividade da versão e os bugs/Defects que justificam o cenário |
| Description | modelo do GUIA-JIRA-003 (Cenário, Teste "a definir", Baseado na atividade, links do Squash "a definir") e uma linha "Justificativa:" com a evidência |
| Original Estimate | o orçamento, se o QA pediu; senão, perguntar na criação (é obrigatório no guia) |
| Affects Version/s | a versão analisada |

A atividade criada entra no board de automação (status inicial de backlog). Devolva a tabela com número da sugestão → chave criada → link.

## Armadilhas

- **Status no JQL vão em inglês:** "Aberto" = `Open`, "Em Andamento" = `In Progress`, "Fechado" = `Closed`. Com o nome em português, o Jira recusa a consulta.
- **O MCP não traz o Environment** e o filtro por ele no JQL não retorna nada: a plataforma é deduzida e marcada como deduzida.
- **`resolution = Concluída` não funciona no JQL**; use `resolution is not EMPTY`.
- **A cobertura por feature subestima.** Várias Test Automated não têm Feature preenchida (ex.: VENDAS-25597): confira pelo Summary e pela classe antes de dizer que a feature não tem automação.
- **Limpeza de fila infla o "concluído".** Fechamentos em massa de atividades antigas sem horas não são automação.
- **fixVersion inclui backports:** uma atividade pode aparecer em mais de uma versão.
- **A fila tem sujeira** (status Fechado sem resolução, horas lançadas em Options, `NOT_IS_TEST_CASE`): não use a fila bruta como cobertura.

## Cuidados

- Não sugira o que a análise não sustenta: sem bug, Defect ou regra de cálculo que justifique, não entra.
- Prefira 10 a 20 sugestões bem fundamentadas a uma lista enorme; agrupe as fracas numa linha.
- Não confunda "a feature tem muitos bugs" com "todo bug dela é automatizável": lentidão, layout e integração com ERP ficam de fora, com o motivo.
- Plataforma deduzida (o MCP não traz o campo Environment) é marcada como deduzida; na dúvida, pergunte na avaliação.
- Nada é criado sem aprovação; uma sugestão por Test Automated.
