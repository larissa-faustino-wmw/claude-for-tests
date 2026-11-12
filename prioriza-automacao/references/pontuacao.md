# Pontuação das sugestões

Uma conta simples e explicável. A pontuação ordena a lista; quem decide é o QA.

## Dor (0 a 10)

| Sinal | Pontos |
|---|---|
| bug causado por atividade da versão (regressão confirmada) | +4 |
| bug de produção ligado ao cenário | +3 por bug (máx. 6) |
| Defect interno ligado ao cenário | +1 por Defect (máx. 3) |
| prioridade High/Highest no bug ligado | +1 |
| feature com tendência "subindo" no `jira_feature_hotspots` | +2 |
| correção da área voltou (`jira_rework`) | +2 |
| cálculo financeiro ou fiscal envolvido (preço, desconto, imposto, comissão, cashback, verba, títulos) | +2 |

Limite em 10.

## Automatizável (multiplicador)

| Situação | Fator |
|---|---|
| regra ou cálculo verificável por valor na tela, App, framework suporta | 1,0 |
| Web (webuitest): fluxo de tela simples (abrir, filtrar, gravar, conferir valor) | 0,8 |
| precisa de suporte novo no framework (componente que o TotalUiTest não trata; na Web, qualquer coisa além de abrir tela) | 0,6 |
| depende de dado específico de cliente que precisa ser montado | 0,7 |
| lentidão, layout, integração com ERP ou serviço externo (CNPJ, mapas, e-mail) | 0 (descartar) |

## Lacuna (multiplicador)

| Automação da feature hoje | Fator |
|---|---|
| nenhuma Test Automated concluída | 1,5 |
| 1 a 5 | 1,2 |
| 6 a 15 | 1,0 |
| mais de 15 | 0,8 |

## Pontuação

`dor × automatizável × lacuna`, arredondada a uma casa. Mostre a conta na sugestão:

> **8,6** = dor 6 (bug de produção VENDAS-24455 Highest, tendência subindo, Defect interno) × 0,8 (Web) × 1,5 (feature sem automação)

## Porte

Para cada sugestão, o porte provável da `orcamento-modelo-antigo` (P 6–10 h, M 14–24 h, G 28–40 h, GG 48 h+), só como referência para o QA. O orçamento de verdade é feito depois, se o QA pedir.
