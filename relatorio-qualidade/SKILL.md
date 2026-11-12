---
name: relatorio-qualidade
description: Gera o relatório de qualidade de uma versão do Lavendere como página web para o time de QA e a gerência — contenção de defeitos (pela causa confirmada e pela versão afetada), o que escapou, esforço do teste da Delivery, onde doeu (regressões e features), automação (concluídas, fila, horas orçadas x reais, bugs achados), execução no Squash, tendência das últimas versões e recomendações com evidência. Use SEMPRE que o usuário pedir relatório, indicadores, métricas, dashboard ou balanço de qualidade de uma versão 9.xxx, "como foi a versão", contenção de defeitos, bugs que escaparam, ou um resumo para a gerência — mesmo que diga só "relatório da 9.068". Sem versão no pedido, pergunte qual.
---

# Relatório de qualidade da versão

Um relatório por versão, gerado depois que ela é liberada, para **QA e gerência**. A unidade é a versão porque é como o time trabalha (sprint → develop → release → Delivery → main). O relatório também mostra a tendência das últimas versões, para responder "estamos melhorando?".

A saída é uma **página web**: a gerência lê o topo (os números, a tendência e as recomendações); o QA desce para o detalhe.

## 1. Versão e corte

- Sem versão no pedido, pergunte qual (ofereça as últimas liberadas, de `jira_release_ranking`).
- Registre a **data do corte** na página. Bugs continuam chegando depois da liberação: o número de uma versão recém-liberada ainda vai mudar. Por isso a tendência recalcula as versões anteriores a cada relatório, e a página avisa quando a versão tem menos de 30 dias.

## 2. Levantar os dados

Definições, fórmulas e consultas em `references/metricas.md`. Resumo:

| Seção | Fonte |
|---|---|
| A versão em números | `jira_release_impact(version, project="VENDAS")` |
| Contenção (os dois números) | `jira_release_impact`: Defects internos × problemas com causa confirmada × problemas com versão afetada |
| O que escapou | `items_that_caused_problems` e os problemas com versão afetada, com Root Cause |
| Esforço da Delivery | a Test de Delivery da versão: métricas da descrição (`[DiasEstimados]`, `[NrTesters]`, `[HorasDiariasTesters]`, `[ClientesTestados]`) e horas lançadas |
| Onde doeu | `features` do `jira_release_impact` (regressão confirmada ou suspeita) e `jira_problem_causes` (legado × mudança recente) |
| Automação | Test Automated resolvidas no período da versão, fila aberta, Original Estimate × horas reais, label `QA_BUG_FOUND` |
| Execução no Squash | a campanha da versão na pasta VERSÕES (API do Squash, só leitura) |
| Tendência | as mesmas contas para as 4 versões anteriores (`jira_release_ranking` para achá-las) e `jira_rework` |

Dado que não deu para obter (Squash sem login, Test de Delivery sem métricas): a seção aparece com "sem dado" e o motivo. Nunca invente nem estime um número sem dizer.

## 3. Recomendações

De 3 a 5, cada uma com a evidência e a ação, ligadas às skills do time quando couber:

- feature com regressão confirmada ou bugs subindo e pouca automação → entrar na fila (`prioriza-automacao`);
- muitos escapes de uma feature que a regressão fixa cobre só de forma ampla → detalhar a regressão (`analise-impacto-delivery`, modo calibração);
- Issue Cause pouco preenchido (a contenção pela causa fica fraca) → reforçar o preenchimento;
- Delivery acima do planejado → o que puxou o esforço (clientes, correções durante a Delivery).

Sem evidência, não recomende.

## 4. Montar a página

Layout e conteúdo em `references/pagina.md`. Antes de escrever o HTML:

- carregue a skill `artifact-design` (e a `dataviz` para os gráficos), se estiverem disponíveis;
- topo para a gerência, detalhe para o QA;
- cada número com a fonte (link da issue ou da consulta) acessível;
- em pt-BR, números no formato brasileiro (`95,7%`, `169,4 h`).

## 5. Publicar

Com a ferramenta de Artifact disponível (Claude Code com artifacts): publique a página e devolva o link; ela fica privada até o usuário compartilhar. Relatório de versão seguinte: publique como página nova (cada versão tem a sua), com o mesmo formato.

Sem a ferramenta: grave o `.html` (ex.: `relatorio-qualidade-9.068.html`) e diga onde está.

Na resposta, além do link, um resumo de 3 linhas: os dois números de contenção, o principal escape e a principal recomendação.

## Armadilhas

- **Status no JQL vão em inglês:** "Aberto" = `Open`, "Em Andamento" = `In Progress`, "Fechado" = `Closed`. Com o nome em português, o Jira recusa a consulta.
- **`defects_caused_confirmed` não é escape:** são Defects pegos no teste de outras atividades; não entram no denominador da contenção.
- **Os números amadurecem.** Bugs chegam depois da liberação: recalcule as versões anteriores a cada relatório e avise quando a versão tem menos de 30 dias.
- **`jira_release_impact` inclui os patches por padrão** (9.068 = 9.068 e 9.068-1).
- **Ache a Test de Delivery pelo título** (`Versão <versão> de <data>`); o Customer dela pode ser WMW ou vazio.
- **As métricas da Delivery usam ponto decimal** (`[DiasEstimados:4.5]`): converta para vírgula só na página.
- **Horas da Delivery:** `time_spent_h` é o Σ com as subtasks; `time_spent_own_h`, só da atividade. Diga qual está usando.
- **Limpeza de fila infla a automação concluída:** separe antes de mostrar o número.

## Cuidados

- **Os dois números de contenção sempre juntos**, com a explicação curta de cada um e a cobertura do Issue Cause.
- Não exponha dados de cliente além do nome do cliente que já está no Jira; nada de dados pessoais.
- Separe automação de verdade de fechamento de limpeza da fila (ver `metricas.md`), senão o número engana.
- Não compare pessoas: o relatório é da versão e do processo, não de quem testou.
