# Modo revisar a fila

A fila de automação é o board kanban das Test Automated abertas. Em 10/11/2026 tinha **314** atividades: 268 em Options, 36 em In Analysis, 8 em In Development, 1 em In Product Increment e 1 em "Fechado" sem resolução. 144 sem label nenhuma, 132 com `QA_ORIGIN_AI`. As que estavam em Options somavam 181 h lançadas.

O objetivo é deixar a fila pequena, confiável e ordenada: o que puxar a seguir, o que fechar, o que juntar e o que corrigir.

## 1. Ler a fila inteira

`search_jira_jql`, paginando de 100 em 100 com `start_at`:

```
project = VENDAS AND issuetype = "Test Automated" AND resolution is EMPTY ORDER BY created ASC
```

Para cada atividade: status, Summary, Feature, labels, criação, horas lançadas, Original Estimate, links. A descrição (Cenário, Teste, Cenário anterior, Link do Squash) só das que forem para a análise de duplicidade ou de obsolescência.

Contagem geral para o resumo: `jira_aggregate` com `group_by` = `status`, `label`, `feature` e `created_month`.

## 2. Inconsistências (corrigir dados)

| Sinal | O que sugerir |
|---|---|
| status "Fechado" (ou outro final) sem resolução | fechar direito, com a resolução certa |
| horas lançadas e status Options | trabalho começado e parado: perguntar ao responsável se retoma ou se registra o que já foi feito e fecha |
| label `NOT_IS_TEST_CASE` | não é caso de teste: converter para o tipo certo ou fechar |
| sem Feature | preencher (a feature sai do Summary ou da classe) |
| sem label de origem (`QA_ORIGIN_*`) | preencher conforme a PQA-JIRA-000 (`QA_ORIGIN_LEGACY` para as antigas vindas do Confluence) |
| sem Original Estimate | orçar quando ela for puxada (não precisa orçar a fila inteira) |
| In Development sem atualização há mais de 30 dias | perguntar se está parada |

## 3. Fechar (com o motivo)

| Motivo | Como verificar |
|---|---|
| **Já automatizado** | existe Test Automated concluída com o mesmo cenário (Summary parecido, mesma feature), ou o teste já existe no `totaluitest`/`webuitest` (`Grep` pelo nome da classe da descrição ou pelas palavras do cenário) |
| **Duplicada na fila** | outra aberta com o mesmo cenário: fica a mais completa (descrição, links, estimativa), a outra fecha apontando para ela |
| **Obsoleta** | a funcionalidade foi descontinuada ou a regra mudou de forma que o cenário não faz mais sentido (Story posterior na mesma feature que mudou a regra; parâmetro removido). Na dúvida, não feche: liste para o QA |
| **Sem valor** | cenário de layout, de lentidão ou dependente de ERP/serviço externo (não automatizável — ver `pontuacao.md`) |

Não feche por idade. Atividade antiga e sem movimento vai para "revisar com o time", não para "fechar".

## 4. Juntar

Atividades da mesma feature que testam a mesma regra com variações pequenas (um parâmetro, um tipo de pedido) podem virar uma só, com os cenários como passos ou parâmetros. Sugira o grupo, qual fica e o que entra nela. Exemplo típico: vários "FECOP tipo 1/2/3/4" separados.

## 5. Ordenar o que fica

Pontue cada atividade que fica com a mesma conta de `pontuacao.md`, usando a dor **atual** da feature (`jira_feature_hotspots` de 180 dias), os bugs ligados à atividade e a lacuna de automação da feature.

As que estão em In Analysis e In Development vêm primeiro (já começadas), salvo se forem para fechar.

## 6. Entrega

| Seção | Conteúdo |
|---|---|
| Resumo | total, por status, por label, por idade; quantas para fechar, juntar, corrigir e manter |
| **Puxar a seguir** | as 10 a 15 de maior pontuação, com a conta e a evidência |
| Fechar | chave, Summary, motivo e a evidência (a Test Automated concluída ou a classe de teste que já cobre; a duplicada que fica) |
| Juntar | os grupos: qual fica, quais entram |
| Corrigir dados | chave e o que corrigir |
| Revisar com o time | as que a skill não conseguiu decidir (antigas sem movimento, possível obsolescência) |

Feche com:

> Avalie: diga o que aprovar em cada seção. Nada é alterado no Jira antes disso.

## 7. Aplicar o que foi aprovado

Pelo Chrome, no Jira, uma atividade por vez, só o que foi aprovado:

- **Fechar:** um comentário com o motivo e a evidência, e a transição de fechamento. **Pergunte ao QA qual transição e qual resolução o time usa** para descartar uma Test Automated (não assuma); use a mesma para todas.
- **Juntar:** comentário nas que saem apontando para a que fica, link "duplicates", e o fechamento como acima. Na que fica, acrescente os cenários na descrição.
- **Corrigir dados:** Edit dos campos aprovados (Feature, labels, resolução).
- **Ordem:** a ordem do board (rank) não é alterada pela skill. Se o time quiser refletir a prioridade, use o campo Priority, com aprovação.

Devolva a tabela do que foi feito, com os links, e o que ficou pendente.
