# Risco e recomendação

## Probabilidade (o side effect acontecer)

| Nível | Quando |
|---|---|
| Alta | o fluxo chama diretamente o código alterado, sem condição que o isole |
| Média | chama por um caminho condicional (parâmetro, tipo de pedido, perfil) que existe em clientes |
| Baixa | caminho raro, atrás de configuração pouco usada, ou dependência indireta de vários níveis |

## Impacto (se acontecer)

| Nível | Quando |
|---|---|
| Alto | valor financeiro ou fiscal errado (preço, desconto, imposto, comissão, cashback, saldo, verba), pedido que não fecha ou não sincroniza, perda de dado, divergência App × Web |
| Médio | fluxo de uso diário bloqueado com contorno, relatório ou PDF errado, mensagem errada que confunde o usuário |
| Baixo | visual, layout, texto secundário |

## Risco

| | Impacto alto | Impacto médio | Impacto baixo |
|---|---|---|---|
| **Prob. alta** | Alto | Alto | Médio |
| **Prob. média** | Alto | Médio | Baixo |
| **Prob. baixa** | Médio | Baixo | Baixo |

Sobe um nível quando:

- a feature está entre as que mais deram Defect ou bug em produção (`jira_feature_hotspots`);
- a área tem correção que voltou (`jira_rework`) ou causa repetida (`jira_problem_causes`);
- outra atividade aberta mexe nas mesmas classes;
- só um lado (App ou Web) foi alterado numa regra que existe nos dois.

## Critério de automação

Um side effect de risco alto vai para **automatizar** quando atende a pelo menos um:

- cálculo ou valor que se confere por número (tributação, desconto, comissão, cashback, estoque, totalizadores);
- sincronização App ↔ Web de dado de negócio;
- área com histórico de Defect ou reincidência;
- fluxo de uso diário que uma regressão manual não detalharia.

E **fica manual** quando:

- é visual ou de layout;
- o fluxo é raro ou depende de integração externa (CNPJ, mapas, e-mail);
- a área está prevista para mudar de novo em breve;
- o TotalUiTest não suporta o componente (custaria suporte novo no framework; cite, e deixe o tester decidir).

## Candidato à regressão fixa

Um side effect que protege um fluxo largo e de uso diário (o cálculo do pedido, a sincronização do pedido) é candidato a **detalhar o caso da regressão fixa** correspondente. Cite isso na entrega; a decisão é do time.
