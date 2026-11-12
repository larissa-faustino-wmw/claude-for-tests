# Histórico real do modelo antigo (export Jira, issue type Test Automated)

Fonte: export do Jira de 01/10/2026 com 250 atividades (abr/2022 a mar/2026).
- **Base do modelo antigo:** criadas antes de 01/03/2026, status Closed e com horas lançadas — 194 atividades.
- **Fora da base:** atividades não concluídas (Options / In Development) ou sem horas; e tudo a partir de 03/2026, que já é modelo com IA (listado no fim só para consulta).

Horas = Σ Time Spent (soma de todas as pessoas: tester que configurava e documentava, dev que codificava, revisores).

Atenção: code review e validação com PO quase nunca foram lançados separadamente. Os números são um **piso** do custo real.

2025 quase não tem automação nova concluída: o ano foi de ajustes, análises e 9 cenários de Local de Estoque/Contrato abertos e parados sem horas. Por isso a referência principal continua sendo 2024.

## Estatística por tipo e ano (base)

| Tipo | Ano | Qtd | P25 | Mediana | Média | P75 | Máx |
|---|---|---|---|---|---|---|---|
| Ajuste | 2022 | 4 | 2,5 | 3,3 | 4,1 | 8,2 | 8,2 |
| Ajuste | 2023 | 6 | 2,2 | 2,7 | 6,4 | 12,9 | 16,4 |
| Ajuste | 2024 | 5 | 2,2 | 3,3 | 3,0 | 3,8 | 5,0 |
| Ajuste | 2025 | 3 | 0,2 | 1,5 | 1,8 | 3,7 | 3,7 |
| Automação | 2022 | 41 | 2,5 | 7,9 | 9,2 | 13,1 | 31,8 |
| Automação | 2023 | 59 | 8,0 | 12,6 | 15,3 | 16,6 | 64,4 |
| Automação | 2024 | 66 | 14,5 | 19,9 | 24,2 | 29,3 | 97,6 |
| Pesquisa/Analise | 2022 | 1 | 11,5 | 11,5 | 11,5 | 11,5 | 11,5 |
| Pesquisa/Analise | 2023 | 1 | 10,8 | 10,8 | 10,8 | 10,8 | 10,8 |
| Pesquisa/Analise | 2025 | 2 | 1,5 | 6,2 | 6,2 | 11,0 | 11,0 |
| Refatoração | 2022 | 2 | 7,0 | 23,2 | 23,2 | 39,3 | 39,3 |
| Refatoração | 2023 | 1 | 19,6 | 19,6 | 19,6 | 19,6 | 19,6 |
| Refatoração | 2024 | 3 | 0,5 | 6,1 | 5,5 | 10,0 | 10,0 |

## Estatística por funcionalidade (Automação, base)

| Funcionalidade (Feature no Jira) | Qtd | Mediana | Média | Mín | Máx |
|---|---|---|---|---|---|
| — | 104 | 12,0 | 14,5 | 0,5 | 97,6 |
| Estoque -> Controle de Estoque - Estoque Padrão | 17 | 19,8 | 23,9 | 7,5 | 78,4 |
| Comercial -> Logística - Transportadora | 13 | 20,9 | 23,3 | 15,0 | 34,3 |
| Contábil/Fiscal -> Faturamento - NF-e | 3 | 21,8 | 26,1 | 18,1 | 38,3 |
| Comercial -> Emissão de Pedidos - Venda | 3 | 34,4 | 34,6 | 16,0 | 53,4 |
| Comercial -> Emissão de Pedidos - Grade | 3 | 21,4 | 26,8 | 5,2 | 53,8 |
| Inteligência de Vendas -> Pesquisa de Mercado - Execução | 3 | 2,2 | 3,7 | 2,2 | 6,6 |
| CRM -> Cliente - Atualizar Cadastro | 2 | 48,1 | 48,1 | 41,1 | 55,1 |
| Contábil/Fiscal -> Tributação - Padrão | 2 | 9,7 | 9,7 | 8,0 | 11,4 |
| Comercial -> Política de Bonificação - Aplicação das Políticas | 2 | 16,0 | 16,0 | 13,0 | 19,0 |
| Contábil/Fiscal -> Tributação - Personalizada | 2 | 7,5 | 7,5 | 4,3 | 10,7 |
| Comercial -> Logística - Frete | 1 | 18,3 | 18,3 | 18,3 | 18,3 |
| Estoque -> Controle de Estoque - Reserva Corrente | 1 | 13,0 | 13,0 | 13,0 | 13,0 |
| Financeiro -> Ficha Financeira - Rede de Clientes | 1 | 44,7 | 44,7 | 44,7 | 44,7 |
| CRM -> Contatos - Cadastro | 1 | 27,6 | 27,6 | 27,6 | 27,6 |
| CRM -> Multiplos Endereços - Endereços do Cliente | 1 | 41,8 | 41,8 | 41,8 | 41,8 |
| CRM | 1 | 31,3 | 31,3 | 31,3 | 31,3 |
| Comercial -> Produto - Produto Bloqueado | 1 | 13,6 | 13,6 | 13,6 | 13,6 |
| Comercial -> Rentabilidade - Personalizada | 1 | 3,2 | 3,2 | 3,2 | 3,2 |
| Comercial -> Liberações de Pedidos - Autorização de Negociação | 1 | 4,6 | 4,6 | 4,6 | 4,6 |
| CRM -> Novo Cliente - Cadastro | 1 | 10,0 | 10,0 | 10,0 | 10,0 |
| Inteligência de Vendas -> Sugestão de Venda - Kit | 1 | 12,5 | 12,5 | 12,5 | 12,5 |
| Estoque -> Controle de Estoque - Lote de Produto | 1 | 0,8 | 0,8 | 0,8 | 0,8 |

## Atividades da base (para buscar análogos)

Busque por palavra-chave da funcionalidade (estoque, bonificação, tributação, transportadora, cliente, NF-e, grade, desconto, verba, login, remessa...).

| Chave | Tipo | Ano | Horas | Funcionalidade | Resumo |
|---|---|---|---|---|---|
| VENDAS-1128 | Ajuste | 2022 | 4,0 | — | Ajuste: descrição do produto 10, nos testes. |
| VENDAS-2598 | Ajuste | 2022 | 2,5 | Comercial -> Gestão de Verba - Transferência de Verba | WMW - Erro ao rodar teste automatizado de verba |
| VENDAS-3410 | Ajuste | 2022 | 1,5 | Comercial -> Marcadores - Pedido | Totaluitest - Erro ao rodar ApresentarMarcadorPedidoTest |
| VENDAS-3440 | Ajuste | 2022 | 8,2 | — | Ajuste: AUD da branch PDA para encontrar os testes que estão faltando no jenkins |
| VENDAS-3616 | Ajuste | 2023 | 2,2 | — | Ajuste: Verificar diferença entre quantidade de testes finalizados e testes rodando no jenkins |
| VENDAS-4429 | Ajuste | 2023 | 3,0 | — | Ajuste: Manutenção de testes automatizados referente a atividade VENDAS-4240 |
| VENDAS-4477 | Ajuste | 2023 | 12,9 | Contábil/Fiscal -> Tributação - Personalizada | WMW - Manutenção e análise dos casos de teste automatizado com tributação FECOP |
| VENDAS-4670 | Ajuste | 2023 | 2,4 | Sistema -> Integração - Configuração | WMW - Tabela de UF inativa na WebTc no ambiente de testes automatizados |
| VENDAS-5018 | Ajuste | 2023 | 1,7 | — | Ajuste de assertEquals com mensagens erradas |
| VENDAS-5384 | Ajuste | 2023 | 16,4 | — | Ajuste: FECOP nos testes automatizados |
| VENDAS-10909 | Ajuste | 2024 | 0,5 | — | ajustar fonte |
| VENDAS-7793 | Ajuste | 2024 | 5,0 | — | Ajuste: Ajustar nos Teste |
| VENDAS-8448 | Ajuste | 2024 | 2,2 | — | Ajuste: Falha nos testes do jenkins |
| VENDAS-9752 | Ajuste | 2024 | 3,3 | — | Ajuste: Adicionar alíquota do FECOP no calculo da ST |
| VENDAS-9947 | Ajuste | 2024 | 3,8 | — | Problema com cenários de testes devido a ajuste feito |
| VENDAS-16487 | Ajuste | 2025 | 3,7 | Contábil/Fiscal -> Faturamento - NF-e | Problema no teste automatizado - Cenário 30.01 |
| VENDAS-17965 | Ajuste | 2025 | 1,5 | — | Ajuste na mensagem do cenário ConsumoDeVerbaGrupoSaldoPersonalizadoTest |
| VENDAS-18051 | Ajuste | 2025 | 0,2 | — | Ajuste de mensagem LGPD |
| VENDAS-1155 | Automação | 2022 | 14,2 | — | Emissão de um pedido utilizando dois item e gerando verba no pedido corrente acumulada. |
| VENDAS-1344 | Automação | 2022 | 8,9 | — | Emissão de um pedido utilizando um item e gerando verba no pedido corrente e um item consumindo a verba gerada |
| VENDAS-1376 | Automação | 2022 | 0,6 | — | WMW - Cadastrar um novo cliente e emitir um pedido com desconto promocional por produto e por percentual |
| VENDAS-1379 | Automação | 2022 | 1,0 | — | CT-LVP-5-1-Emitir um pedido com um produto que tenha lote de estoque |
| VENDAS-1380 | Automação | 2022 | 0,5 | — | CT-LVP-5-2-Emitir um pedido validando o estoque máximo do lote do produto |
| VENDAS-1383 | Automação | 2022 | 0,8 | Estoque -> Controle de Estoque - Lote de Produto | CT-LVP-5-3-Exclusão de item com lote de estoque |
| VENDAS-1473 | Automação | 2022 | 4,2 | — | CT-LVP-11-6-2-Emissão de pedido com Tributação Personalizada FECOP tipo 2 |
| VENDAS-1474 | Automação | 2022 | 4,1 | — | CT-LVP-11-6-3-Emissão de pedido com Tributação Personalizada FECOP tipo 3 |
| VENDAS-1526 | Automação | 2022 | 31,8 | — | Emissão de um pedido de venda aplicando um politica de bonificação de valor com item opcional |
| VENDAS-1547 | Automação | 2022 | 4,3 | Contábil/Fiscal -> Tributação - Personalizada | CT-LVP-11-7-Emissão de pedido com Tributação Personalizada para Zona Franca/Suframa |
| VENDAS-1712 | Automação | 2022 | 10,7 | Contábil/Fiscal -> Tributação - Personalizada | CT-LVP-11-8-Replicação de pedido para cliente de outro estado com Tributação Personalizada. |
| VENDAS-1720 | Automação | 2022 | 18,1 | — | WMW - Emissão de Pedido com Tributação Fixa sem FECOP |
| VENDAS-1863 | Automação | 2022 | 13,0 | Comercial -> Política de Bonificação - Aplicação das Políticas | Emissão de um pedido de venda aplicando um politica de bonificação e aplicando um brinde Opcional |
| VENDAS-1869 | Automação | 2022 | 12,5 | Inteligência de Vendas -> Sugestão de Venda - Kit | CT-LVP-9-7-Exclusão de item de kit inserido no pedido |
| VENDAS-2000 | Automação | 2022 | 12,0 | — | Emissão de pedido utilizando Verba/Flex por representante extrapolando saldo e adicionando item |
| VENDAS-2027 | Automação | 2022 | 12,7 | — | Cadastro de Múltiplos Endereços de novos cliente |
| VENDAS-2067 | Automação | 2022 | 0,5 | — | Quantidade mínima de endereços no cadastro de novos clientes |
| VENDAS-2184 | Automação | 2022 | 10,0 | CRM -> Novo Cliente - Cadastro | CT-LVP-4-5-Validar exclusão do cadastro do novo cliente |
| VENDAS-2216 | Automação | 2022 | 19,0 | Comercial -> Política de Bonificação - Aplicação das Políticas | CT13.t3.Emissão de um pedido de venda aplicando um politica de bonificação e aplicando um brinde automatico |
| VENDAS-2355 | Automação | 2022 | 14,7 | — | Emissão de um pedido de venda aplicando um politica de bonificação com base na familia e linha de produtos |
| VENDAS-2572 | Automação | 2022 | 11,3 | — | CT-LVP-14-1-Emissão de um pedido de troca com ordenação por descrição |
| VENDAS-2577 | Automação | 2022 | 7,8 | — | WMW - Emissão de Pedido com Tributação Fixa com valor Outorga sem FECOP |
| VENDAS-2717 | Automação | 2022 | 2,7 | — | WMW - Emissão de Pedido com Tributação Fixa com FECOP tipo 1 |
| VENDAS-2719 | Automação | 2022 | 5,5 | — | CT-LVP-11-12-2-Emissão de Pedido com Tributação Fixa com FECOP tipo 2 |
| VENDAS-2720 | Automação | 2022 | 4,0 | — | WMW - Emissão de Pedido com Tributação Fixa com FECOP tipo 3 |
| VENDAS-2721 | Automação | 2022 | 2,5 | — | CT-LVP-11-12-4-Emissão de Pedido com Tributação Fixa com FECOP tipo 4 |
| VENDAS-2739 | Automação | 2022 | 27,4 | — | Emissão de um pedido de venda aplicando um politica de bonificação só por produtos especificos por linha de pr |
| VENDAS-3014 | Automação | 2022 | 19,5 | — | CT-LVP-13-6-Emissão de um pedido de venda aplicando um politica de bonificação por faixa quantidade manual |
| VENDAS-3304 | Automação | 2022 | 9,8 | — | Emissão de um pedido de venda aplicando um politica de bonificação por faixa quantidade automatico |
| VENDAS-3351 | Automação | 2022 | 25,8 | — | Emissão de um pedido de venda aplicando um politica de bonificação onde o pedido pode ficar pendente por extra |
| VENDAS-3428 | Automação | 2022 | 7,9 | — | WMW - Emissão de Pedido com Tributação Fixa para Medicamentos sem FECOP e sem base de cálculo retida (R2) |
| VENDAS-3429 | Automação | 2022 | 3,1 | — | WMW - Emissão de Pedido com Tributação Fixa para Medicamentos sem FECOP com cálculo auxiliar 1 menor/igual ao  |
| VENDAS-628 | Automação | 2022 | 1,6 | — | WMW - Emissão de pedido com Tributação Personalizada ICMS. |
| VENDAS-629 | Automação | 2022 | 1,0 | — | WMW - Emissão de pedido com Tributação Personalizada PIS. |
| VENDAS-707 | Automação | 2022 | 5,5 | — | Emissão de um pedido utilizando um item e gerando verba no pedido corrente. |
| VENDAS-709 | Automação | 2022 | 14,2 | — | Emissão de um pedido utilizando dois item e gerando verba no pedido corrente e um item consumindo a verba gera |
| VENDAS-710 | Automação | 2022 | 0,6 | — | WMW - Emissão de pedido com Tributação Personalizada IPI |
| VENDAS-711 | Automação | 2022 | 0,6 | — | WMW - Emissão de pedido com Tributação Personalizada ST. |
| VENDAS-712 | Automação | 2022 | 1,9 | — | WMW - Emissão de pedido com Tributação Personalizada COFINS |
| VENDAS-718 | Automação | 2022 | 16,2 | — | WMW - Emissão de pedido com Tributação Personalizada FECOP tipo 1 |
| VENDAS-950 | Automação | 2022 | 13,1 | — | CT-LVP-11-6-4-Emissão de pedido com Tributação Personalizada FECOP tipo 4 |
| VENDAS-3644 | Automação | 2023 | 8,0 | Contábil/Fiscal -> Tributação - Padrão | WMW - Emissão de Pedido com Tributação Fixa para Medicamentos sem FECOP com cálculo auxiliar 1 menor/igual ao  |
| VENDAS-3762 | Automação | 2023 | 6,6 | Inteligência de Vendas -> Pesquisa de Mercado - Execução | Cenário 17.1: Realizar uma pesquisa de mercado sem dependência do cliente por meio do menu de Cliente |
| VENDAS-3766 | Automação | 2023 | 2,2 | Inteligência de Vendas -> Pesquisa de Mercado - Execução | Cenário 17.2: Realizar uma pesquisa de mercado sem dependência do cliente por meio do Pedido |
| VENDAS-3771 | Automação | 2023 | 2,2 | Inteligência de Vendas -> Pesquisa de Mercado - Execução | Cenário 17.3: Realizar uma pesquisa de mercado condicionando ao cliente por meio do Pedido (Fluxo Principal) |
| VENDAS-3779 | Automação | 2023 | 4,6 | Comercial -> Liberações de Pedidos - Autorização de Negociação | Cenário 18.1: Solicitação de negociação de preço e autorizar na web (Fluxo principal) |
| VENDAS-3782 | Automação | 2023 | 3,2 | Comercial -> Rentabilidade - Personalizada | WMW - Cálculo de rentabilidade com base na formula 7, considerando os produtos neutros e não neutros |
| VENDAS-3783 | Automação | 2023 | 13,6 | Comercial -> Produto - Produto Bloqueado | Cenário 20.1: Emitir um pedido com um produto crítico e autorizar na web |
| VENDAS-3792 | Automação | 2023 | 5,9 | — | CT-LVP-11-19-Emissão de Pedido com Tributação Fixa com valor de PMPF |
| VENDAS-3942 | Automação | 2023 | 8,3 | — | Caso o produto da bonificação automática já esteja incluído no pedido como bonificação, a quantidade deste ite |
| VENDAS-3959 | Automação | 2023 | 8,8 | — | Ao alterar a quantidade de venda que mude a faixa da política de bonificação para uma que não gere bonificação |
| VENDAS-3971 | Automação | 2023 | 7,6 | — | Emissão de um pedido de venda aplicando um politica de bonificação com redução e exclusão de itens que tenham  |
| VENDAS-4039 | Automação | 2023 | 3,0 | — | Emissão de um pedido de venda aplicando um politica de bonificação e consumindo a verba do supervisor |
| VENDAS-4080 | Automação | 2023 | 33,8 | — | Arredondamento do valor após a inserção do desconto e alterar o desconto da capa após a inserção do item no pe |
| VENDAS-4131 | Automação | 2023 | 10,8 | — | Inserir o desconto na capa e na tela de inserção de item tem que puxar o desconto nos próximos itens a serem i |
| VENDAS-4232 | Automação | 2023 | 11,4 | Contábil/Fiscal -> Tributação - Padrão | CT-LVP-11-17-Replicação de pedido para cliente de outro estado com Tributação Fixa. |
| VENDAS-4276 | Automação | 2023 | 12,1 | — | Alteração % e de desconto e valor do item na tela de inserção do item e atualizações no detalhe do item devem  |
| VENDAS-4300 | Automação | 2023 | 16,6 | — | Troca de tabela de preço nos itens do pedido (PRM 90) |
| VENDAS-4453 | Automação | 2023 | 12,9 | — | Exclusão de itens pela tela de detalhe deve refletir na lista de multipla inserção e Exclusão dos itens pela m |
| VENDAS-4580 | Automação | 2023 | 12,6 | — | Replicação de pedido com multipla inserção |
| VENDAS-4625 | Automação | 2023 | 14,3 | — | Inserir desconto na capa e validar os desontos na lista de itens |
| VENDAS-4643 | Automação | 2023 | 7,6 | — | CT-LVP-21-2-Emitir Pedido utilizando gôndola (Fluxo Principal) |
| VENDAS-4647 | Automação | 2023 | 1,5 | — | Validar login com credenciais válidas |
| VENDAS-4650 | Automação | 2023 | 5,1 | — | CT-LVP-4-7-Cadastro de novo cliente |
| VENDAS-4652 | Automação | 2023 | 5,2 | — | CT-LVP-23-1-Novo Recado |
| VENDAS-4654 | Automação | 2023 | 6,0 | — | CT-LVP-24-1-Emissão de pedido (padrão) |
| VENDAS-4664 | Automação | 2023 | 12,3 | — | CT-LVP-8-8-Registrar chegada, atualizar chegada e desfazer chegada |
| VENDAS-4665 | Automação | 2023 | 10,8 | — | CT-LVP-8-9-Registrar saída |
| VENDAS-4667 | Automação | 2023 | 16,0 | — | CT-LVP-4-8-Busca de endereço por CEP no cadastro de novo cliente |
| VENDAS-4706 | Automação | 2023 | 15,3 | — | Validação de valores após ultrapassar o limite de estoque |
| VENDAS-4741 | Automação | 2023 | 19,8 | — | Exclusão multipla de itens pela lista de itens inseridos no pedido deve refletir na lista de multipla inserção |
| VENDAS-5097 | Automação | 2023 | 12,7 | — | CT-LVP-1-5-Emitir pedido com unidade alternativa e troca de tabela de preço após a inserção do item |
| VENDAS-5283 | Automação | 2023 | 16,3 | — | Valor desconto deve zerar ao excluir o item na multipla inserção |
| VENDAS-5356 | Automação | 2023 | 32,1 | — | Unidade padrão na múltipla inserção |
| VENDAS-5421 | Automação | 2023 | 10,2 | — | Ao alterar quantidade de item inserido desconto é mantido e consumo de verba alterado |
| VENDAS-6279 | Automação | 2023 | 28,8 | — | Consumo de Verba Grupo Saldo Personalizado |
| VENDAS-6326 | Automação | 2023 | 39,3 | — | Adicionar o desconto manual em item com desconto quantidade aplicado |
| VENDAS-6604 | Automação | 2023 | 20,7 | — | Emissão de um pedido de venda aplicando uma politica de bonificação e removendo itens bonificados no pedido |
| VENDAS-6633 | Automação | 2023 | 15,7 | — | Emissão de um pedido de venda aplicando um politica de bonificação e removendo brindes no pedido |
| VENDAS-6649 | Automação | 2023 | 13,7 | — | Emissão de um pedido de venda com um item bonificado e um item de venda |
| VENDAS-6669 | Automação | 2023 | 20,5 | — | Emissão de Pedido bonificado com Tributação Fixa com valor de PMPF |
| VENDAS-6699 | Automação | 2023 | 8,9 | — | Emissão de pedido bonificado com Tributação Personalizada IPI |
| VENDAS-6710 | Automação | 2023 | 8,0 | — | Emissão de pedido bonificado com Tributação Personalizada ST |
| VENDAS-6758 | Automação | 2023 | 11,7 | — | Emissão de pedido bonificado com Tributação Personalizada ICMS |
| VENDAS-6780 | Automação | 2023 | 9,2 | — | Emissão de pedido bonificado com Tributação Personalizada PIS |
| VENDAS-6839 | Automação | 2023 | 10,7 | — | Emissão de pedido bonificado com Tributação Personalizada COFINS |
| VENDAS-6849 | Automação | 2023 | 13,2 | — | Emissão de pedido bonificado com Tributação Personalizada FECOP tipo 1 |
| VENDAS-6900 | Automação | 2023 | 15,7 | — | Emissão de pedido bonificado com Tributação Personalizada FECOP tipo 2 |
| VENDAS-6921 | Automação | 2023 | 15,2 | — | Emissão de pedido bonificado com Tributação Personalizada FECOP tipo 3 |
| VENDAS-6936 | Automação | 2023 | 18,2 | — | Emissão de pedido bonificado com Tributação Personalizada FECOP tipo 4 |
| VENDAS-7015 | Automação | 2023 | 33,0 | — | Cadastro de novo cliente com busca dos dados através do CNPJ |
| VENDAS-7037 | Automação | 2023 | 8,2 | — | Emissão de Pedido de bonificação com Tributação Fixa. |
| VENDAS-7070 | Automação | 2023 | 13,3 | — | Emissão de pedido com três itens consumindo Verba/Flex por representante e recalculando valores no relatório |
| VENDAS-7091 | Automação | 2023 | 14,2 | — | Listagem de novos clientes e exclusão de registros |
| VENDAS-7102 | Automação | 2023 | 2,0 | — | Emissão de pedido com um itens consumindo Verba por menu inferior da capa do pedido. |
| VENDAS-7116 | Automação | 2023 | 30,3 | — | Emitir um pedido utilizando desconto quantidade e unidade alternativa |
| VENDAS-7239 | Automação | 2023 | 64,4 | — | Cadastro de novo cliente com campos dinamicos |
| VENDAS-7342 | Automação | 2023 | 32,7 | — | Inserção de item utilizando o filtro de desconto quantidade na tela de inserção no pedido e verificação do fil |
| VENDAS-7483 | Automação | 2023 | 50,7 | — | Pedido com desconto quantidade e agrupador de similaridade |
| VENDAS-7609 | Automação | 2023 | 37,1 | — | Avisos de falta ao adicionar produtos no pedido com a configuração de produto falta |
| VENDAS-10808 | Automação | 2024 | 33,9 | Comercial -> Logística - Transportadora | 29.09-Seleção de transportadora a qualquer momento no pedido por cep e utilizando multipos endereços e validan |
| VENDAS-10905 | Automação | 2024 | 13,0 | Estoque -> Controle de Estoque - Reserva Corrente | 25.36 - Reserva de estoque Corrente - Validação de reserva de estoque sem estoque PO |
| VENDAS-10906 | Automação | 2024 | 53,4 | Comercial -> Emissão de Pedidos - Venda | 4-16- Criação de pedido sem cliente e sem carrossel de fotos |
| VENDAS-10921 | Automação | 2024 | 16,2 | Comercial -> Logística - Transportadora | 29.10-Seleção de transportadora no fechameto do pedido por região com multiplos endereço somando frete no pedi |
| VENDAS-11002 | Automação | 2024 | 18,3 | Comercial -> Logística - Frete | 29-11- Validação do total do pedido com o frete do cliente já calculando o rateio frete transportadora. |
| VENDAS-11006 | Automação | 2024 | 17,5 | Comercial -> Logística - Transportadora | 29-12-Validação de fechamento do pedido sem seleção de transportadora e com soma do frete no valor total. |
| VENDAS-11174 | Automação | 2024 | 16,0 | Comercial -> Emissão de Pedidos - Venda | 4-15- Criação de pedido sem cliente com lista de itens padrão |
| VENDAS-11384 | Automação | 2024 | 38,3 | Contábil/Fiscal -> Faturamento - NF-e | 30.01-Validação de Filtro de Pedidos e campos na aba NF-e na capa do pedido e titulo do cliente |
| VENDAS-11549 | Automação | 2024 | 21,8 | Contábil/Fiscal -> Faturamento - NF-e | 30.02 -Validar a utilização a nota fiscal eletrônica agrupando os itens por sua referência |
| VENDAS-12238 | Automação | 2024 | 15,0 | Comercial -> Logística - Transportadora | 29-14- Validação de bloqueio de fechamento do pedido com seleção de transportadora a qualquer momento do pedid |
| VENDAS-12371 | Automação | 2024 | 18,1 | Contábil/Fiscal -> Faturamento - NF-e | CT006-T008-Validação de geração da NFE no fechamento do pedido. |
| VENDAS-12539 | Automação | 2024 | 15,7 | Comercial -> Logística - Transportadora | 29.13-Seleção de transportadora a qualquer momento do pedido selecionando a transportadora antes do item |
| VENDAS-7789 | Automação | 2024 | 18,1 | — | Emissão de pedido com inclusão do mesmo produto com unidade unidade diferente |
| VENDAS-7870 | Automação | 2024 | 8,5 | — | CT-LVP-25-03-Validação da pop-up de registro de falta com ajuste de quantidade de venda para estoque disponíve |
| VENDAS-7950 | Automação | 2024 | 9,0 | — | CT-LVP-25-04-Validação da pop-up de registro de falta com ajuste de quantidade de venda para estoque disponíve |
| VENDAS-8019 | Automação | 2024 | 11,8 | — | CT-LVP-25-05-Validação da pop-up de registro de falta com ajuste de quantidade de venda. |
| VENDAS-8025 | Automação | 2024 | 11,3 | — | Validação da pop-up apenas com registro da falta de estoque. |
| VENDAS-8044 | Automação | 2024 | 11,3 | — | Validação de registro da falta onde pop-up não carrega nenhuma das opções como padrão |
| VENDAS-8054 | Automação | 2024 | 10,9 | — | Validando bloqueio de venda de produto sem estoque na lista itens do pedido com registro de produto falta. |
| VENDAS-8100 | Automação | 2024 | 20,0 | — | Bloqueio de venda de produto sem estoque na lista itens do pedido com registro de produto falta e unidade alte |
| VENDAS-8166 | Automação | 2024 | 8,1 | — | Validação de estoque ao adicionar o de unidade alternativa diferente no mesmo pedido. |
| VENDAS-8188 | Automação | 2024 | 3,5 | — | 25.11 - Estoque Padrão - Produto sem estoque na lista itens do pedido com registro de produto falta sem bloque |
| VENDAS-8217 | Automação | 2024 | 27,1 | — | Validação de bloqueio de produto sem estoque com unidade alternativa grade. |
| VENDAS-8233 | Automação | 2024 | 23,3 | — | CT-LVP-25-13-Validação de bloqueio de produto sem estoque com unidade alternativa grade e inclusão do mesmo it |
| VENDAS-8263 | Automação | 2024 | 16,7 | — | CT-LVP-25-14-Validação de bloqueio de produto sem estoque em uma unidade alternativa grade e com outra unidade |
| VENDAS-8277 | Automação | 2024 | 97,6 | — | Validação de atualização do estoque padrão no modo grade em pedido de venda. |
| VENDAS-8350 | Automação | 2024 | 20,0 | — | Validação de atualização do estoque padrão no modo grade em pedido de bonificação. |
| VENDAS-8392 | Automação | 2024 | 25,1 | Estoque -> Controle de Estoque - Estoque Padrão | CT-LVP-27-04- Validação de atualização do estoque padrão no modo grade em pedido de venda com quantidades frac |
| VENDAS-8492 | Automação | 2024 | 53,8 | Comercial -> Emissão de Pedidos - Grade | Validação de inserção de itens na grade quantidade do pedido com replicação do item |
| VENDAS-8522 | Automação | 2024 | 9,0 | — | Validação de bloqueio com produto sem estoque em pedido normal |
| VENDAS-8528 | Automação | 2024 | 14,5 | — | CT-LVP-25-16-Validação de produto falta com tipo de pedido que ignora controle de estoque. |
| VENDAS-8639 | Automação | 2024 | 14,0 | — | CT-LVP-25-17-Validação de bloqueio de venda de produto sem estoque com a cor do item em vermelho |
| VENDAS-8669 | Automação | 2024 | 5,2 | Comercial -> Emissão de Pedidos - Grade | Validação de bloqueio de vendo em pedido com grade. |
| VENDAS-8860 | Automação | 2024 | 17,2 | Estoque -> Controle de Estoque - Estoque Padrão | Validação de venda de item com estoque zerado ou negativo. |
| VENDAS-8866 | Automação | 2024 | 38,0 | Estoque -> Controle de Estoque - Estoque Padrão | 25.20 - Estoque Padrão - Validação de venda de item com estoque zerado ou negativo com mensagem que não tem es |
| VENDAS-8975 | Automação | 2024 | 21,5 | Estoque -> Controle de Estoque - Estoque Padrão | CT-LVP-25-22-Liberação de venda de item com estoque zerado ou negativo com senha Skip to end of metadata |
| VENDAS-9024 | Automação | 2024 | 19,8 | Estoque -> Controle de Estoque - Estoque Padrão | Validação de bloqueio de fechamento de pedido com produto sem estoque. |
| VENDAS-9044 | Automação | 2024 | 21,4 | Comercial -> Emissão de Pedidos - Grade | Validação de bloqueio de fechamento de pedido com grade de produto sem estoque |
| VENDAS-9066 | Automação | 2024 | 24,7 | Estoque -> Controle de Estoque - Estoque Padrão | 25.27 - Estoque Padrão - Validação de bloqueio de fechamento de pedido com produto sem estoque e local de esto |
| VENDAS-9213 | Automação | 2024 | 20,2 | Estoque -> Controle de Estoque - Estoque Padrão | 25.21 - Estoque Padrão - Validação de venda de item com estoque zerado ou negativo com mensagem de detalhes de |
| VENDAS-9214 | Automação | 2024 | 18,5 | Estoque -> Controle de Estoque - Estoque Padrão | 25.23 - Estoque Padrão - Validação de aviso de venda de item sem estoque. |
| VENDAS-9215 | Automação | 2024 | 14,2 | Estoque -> Controle de Estoque - Estoque Padrão | 25.24 - Estoque Padrão - Validação de aviso de venda de item sem estoque com detalhes de estoque previsto. |
| VENDAS-9216 | Automação | 2024 | 36,4 | Estoque -> Controle de Estoque - Estoque Padrão | 25.28 - Estoque Padrão - Validação de bloqueio de fechamento de pedido com produto sem estoque e revalidação p |
| VENDAS-9217 | Automação | 2024 | 24,4 | Estoque -> Controle de Estoque - Estoque Padrão | 25.29 - Estoque Padrão - Validação de bloqueio de fechamento de pedido com produto sem estoque e atualização d |
| VENDAS-9218 | Automação | 2024 | 11,3 | Estoque -> Controle de Estoque - Estoque Padrão | 25.30 - Estoque Padrão - Validação de bloqueio de fechamento de pedido com produto sem estoque e com aviso de  |
| VENDAS-9219 | Automação | 2024 | 19,0 | — | 25.31 - Estoque Padrão - Validação de bloqueio de fechamento de pedido com produto sem estoque e com aviso de  |
| VENDAS-9220 | Automação | 2024 | 7,5 | Estoque -> Controle de Estoque - Estoque Padrão | CT032-T017-Validação de bloqueio de venda de produto sem estoque com a cor do item em vermelho. |
| VENDAS-9294 | Automação | 2024 | 18,0 | Estoque -> Controle de Estoque - Estoque Padrão | 25.32 - Estoque Padrão - Validação de movimentação de estoque no pedido, com inserção e exclusão de itens. |
| VENDAS-9295 | Automação | 2024 | 12,3 | Estoque -> Controle de Estoque - Estoque Padrão | 25.33 - Estoque Padrão - Validação de recalculo manual do estoque ao adicionar item no pedido. |
| VENDAS-9296 | Automação | 2024 | 18,7 | Estoque -> Controle de Estoque - Estoque Padrão | 25.34 - Estoque Padrão - Validação de recalculo manual do estoque no menu produto. |
| VENDAS-9297 | Automação | 2024 | 78,4 | Estoque -> Controle de Estoque - Estoque Padrão | 25.35 - Estoque Padrão - Validação de movimentação de estoque com itens de troca recolher no pedido como desco |
| VENDAS-9438 | Automação | 2024 | 31,3 | CRM | 4.14 - Criação de novo cliente com emissão de novo pedido com tipo de frete |
| VENDAS-9439 | Automação | 2024 | 55,1 | CRM -> Cliente - Atualizar Cadastro | 28.06 - Atualização de endereços de cliente com supervisor |
| VENDAS-9544 | Automação | 2024 | 41,1 | CRM -> Cliente - Atualizar Cadastro | 28.01 - Atualização de cliente |
| VENDAS-9545 | Automação | 2024 | 41,8 | CRM -> Multiplos Endereços - Endereços do Cliente | 28.02 - Cadastro de multiplos endereços do cliente |
| VENDAS-9546 | Automação | 2024 | 34,4 | Comercial -> Emissão de Pedidos - Venda | 28.03 - Validação de endereço de entrega do cliente no pedido |
| VENDAS-9547 | Automação | 2024 | 27,6 | CRM -> Contatos - Cadastro | Cadastrar e atualizar contato do cliente |
| VENDAS-9548 | Automação | 2024 | 44,7 | Financeiro -> Ficha Financeira - Rede de Clientes | 28.05 - Validar a seleção de cliente de rede para emissão de pedido. |
| VENDAS-9887 | Automação | 2024 | 29,3 | Comercial -> Logística - Transportadora | 29.01-Seleção de transportadora no fechamento do pedido por região. |
| VENDAS-9898 | Automação | 2024 | 34,3 | Comercial -> Logística - Transportadora | 29.08-Seleção de transportadora a no fechameto do pedido por região com multiplos endereço. |
| VENDAS-9899 | Automação | 2024 | 20,5 | Comercial -> Logística - Transportadora | 29.02-Seleção de transportadora no início do pedido por CEP. |
| VENDAS-9900 | Automação | 2024 | 22,0 | Comercial -> Logística - Transportadora | 29.03-Seleção de transportadora a qualquer momento no pedido por CEP. |
| VENDAS-9901 | Automação | 2024 | 26,3 | Comercial -> Logística - Transportadora | 29.04-Seleção de transportadora por data de entrega no fechamento do pedido por região com transportadas relac |
| VENDAS-9902 | Automação | 2024 | 20,9 | Comercial -> Logística - Transportadora | 29.05-Seleção de transportadora selecionada a qualquer momento no pedido por cep e utilizando frete minimo tip |
| VENDAS-9903 | Automação | 2024 | 16,8 | Comercial -> Logística - Transportadora | 29.06-Seleção de transportadora a qualquer momento no pedido por cep e observação de transportadora |
| VENDAS-9904 | Automação | 2024 | 34,2 | Comercial -> Logística - Transportadora | 29.07-Seleção de transportadora a qualquer momento no pedido e utilizando cep por multiplos endereços. |
| VENDAS-678 | Pesquisa/Analise | 2022 | 11,5 | — | Análise: TotalUiTest Build |
| VENDAS-4062 | Pesquisa/Analise | 2023 | 10,8 | — | Análise e organização de cenários de teste automatizado antigos |
| VENDAS-13086 | Pesquisa/Analise | 2025 | 1,5 | Comercial -> Emissão de Pedidos - Venda | Validação de numeros negativos na inserção de quantidade de item |
| VENDAS-13677 | Pesquisa/Analise | 2025 | 11,0 | Sistema -> Framework - TotalCross | Analisar sobre os falsos negativos dos testes automatizados no jenkins |
| VENDAS-701 | Refatoração | 2022 | 7,0 | — | Refatoração: Diversos Rene |
| VENDAS-943 | Refatoração | 2022 | 39,3 | — | Refatoração: fonte legado |
| VENDAS-4384 | Refatoração | 2023 | 19,6 | — | Refatoração: Dar suporte ao componente de multiplas inserçao no TotalUiTest |
| VENDAS-10832 | Refatoração | 2024 | 10,0 | CRM -> Novo Cliente - Cadastro | Refatoração de cenários referente a atividade VENDAS-9140 |
| VENDAS-11461 | Refatoração | 2024 | 0,5 | Comercial -> Liberações de Pedidos - Pedidos Pendentes | Refatoração do cenário EmissaoPedVendaAplicandoUmaPoliticaBonifOndePedFicaPendentePorExtrapolarValorDoItemTest |
| VENDAS-8711 | Refatoração | 2024 | 6,1 | — | Refatoração: Melhoria nas classes de multipla inserção |

## Modelo antigo fora da base (não concluídas ou sem horas)

Não use como custo de referência — as horas estão incompletas. Servem só para saber que a funcionalidade já foi estudada.

| Chave | Tipo | Status | Ano | Horas | Funcionalidade | Resumo |
|---|---|---|---|---|---|---|
| VENDAS-1151 | Pesquisa/Analise | Closed | 2022 | 0,0 | — | atividades de auditotia de testes automatizados |
| VENDAS-11620 | Automação | Options | 2024 | 16,2 | Contábil/Fiscal -> Faturamento - NF-e | 30.03-Validação de busca de NFE no pedido e no pedido relacionado |
| VENDAS-13088 | Refatoração | Options | 2025 | 6,0 | CRM -> Novo Cliente - Cadastro | Refatoração do cenário 4.11 de atualização de dados via receitaWS e Sintegra, onde o campo deve ser  |
| VENDAS-13095 | Automação | Options | 2025 | 4,5 | CRM -> Novo Cliente - Cadastro | 4-07-Alteração do tipo de pessoa antes de salvar o novo cadastro de cliente |
| VENDAS-13199 | Automação | Options | 2025 | 19,0 | Comercial -> Logística - Transportadora | 29.15 - Validação de bloqueio nos finais de semana na seleção de transportadora a qualquer momento d |
| VENDAS-13985 | Ajuste | Options | 2025 | 2,0 | Inteligência de Vendas -> Sugestão de Venda - Kit | Ajustar cenário de inserção de kit fechado no pedido |
| VENDAS-14045 | Ajuste | Options | 2025 | 4,0 | Inteligência de Vendas -> Sugestão de Venda - Kit | Refatoração do cenário CT-LVP-9-3 |
| VENDAS-15263 | Automação | Options | 2025 | 0,0 | Estoque -> Controle de Estoque - Local de Estoque | 31.01-Pedido com itens em locais de estoque diferentes |
| VENDAS-15265 | Automação | Options | 2025 | 2,3 | Estoque -> Controle de Estoque - Local de Estoque | 31.02-Pedido com local de estoque por cliente |
| VENDAS-15266 | Automação | Options | 2025 | 0,0 | Estoque -> Controle de Estoque - Local de Estoque | 31.03- Pedido com local estoque por tabela de preço |
| VENDAS-15267 | Automação | Options | 2025 | 0,0 | Estoque -> Controle de Estoque - Local de Estoque | 31.04-Pedido com local estoque por tipo de pedido |
| VENDAS-15269 | Automação | Options | 2025 | 0,0 | Estoque -> Contrato - Aplicação | 32.01- Pedido com itens de contrato por local de estoque |
| VENDAS-15272 | Automação | Options | 2025 | 0,0 | Estoque -> Contrato - Aplicação | 32.02-Pedido de contrato com itens em local de estoque de contrato diferentes |
| VENDAS-15273 | Automação | Options | 2025 | 0,0 | Estoque -> Contrato - Aplicação | 32.03-Pedido de contrato com itens em local de estoque diferentes por dentro e fora do contrato |
| VENDAS-15274 | Automação | Options | 2025 | 0,0 | Estoque -> Contrato - Aplicação | 32.04-Pedido com contrato por local de estoque com saldo extrapolado |
| VENDAS-15278 | Automação | Options | 2025 | 0,0 | Estoque -> Contrato - Aplicação | 32.05-Pedido com contrato por local de estoque com data de vigencia extrapolado |
| VENDAS-17485 | Ajuste | Closed | 2025 | 0,0 | Contábil/Fiscal -> Tributação - Personalizada | Atualização de cenário - deveEmitirPedidoCompraValidandoEstoqueUtilizandoVerbaTributacaoDescontos |
| VENDAS-17978 | Ajuste | Closed | 2025 | 0,0 | — | Erro nos testes automatizados |
| VENDAS-19638 | Pesquisa/Analise | In Analysis | 2026 | 4,2 | Contábil/Fiscal -> Tributação - Personalizada | Refatoração dos cenários de teste automatizado |
| VENDAS-2357 | Automação | Options | 2022 | 3,6 | Comercial -> Liberações de Pedidos - Pedidos Pendentes | CT-LVP-2-2-Liberação de pedido via app |
| VENDAS-2582 | Automação | Options | 2022 | 8,5 | Comercial -> Emissão de Pedidos - Troca | WMW - Emissão de um pedido de troca com ordenação por descrição e utilizando motivo da troca por ite |
| VENDAS-2589 | Automação | Options | 2022 | 6,2 | Comercial -> Emissão de Pedidos - Troca | WMW - Emissão de um pedido de troca com ordenação por código |
| VENDAS-3373 | Automação | Options | 2022 | 14,4 | — | Emissão de um pedido de venda aplicando um politica de bonificação e removendo o brindes após perder |
| VENDAS-3744 | Automação | Options | 2023 | 3,0 | — | CT-LVP-11-16-Emissão de Pedido com Tributação Fixa para Medicamentos sem FECOP (R3) |
| VENDAS-3772 | Automação | Options | 2023 | 4,7 | — | CT-LVP-11-18-Emissão de Pedido com Tributação Fixa com Unidades Alternativas |
| VENDAS-3781 | Automação | Options | 2023 | 0,2 | — | WMW - Cadastro de prospect aprovado em duas etapas |
| VENDAS-3784 | Automação | Options | 2023 | 0,0 | — | Cenário 20.2: Emitir um pedido com um produto crítico e liberado por senha |
| VENDAS-3788 | Automação | Options | 2023 | 0,8 | — | Cenário 20.2: Emitir um pedido com um produto crítico e liberado por senha |
| VENDAS-3803 | Automação | Options | 2023 | 3,5 | — | CT-LVP-13-11-Emissão de um pedido de venda aplicando um politica de bonificação e Validar se a bonif |
| VENDAS-4642 | Automação | Options | 2023 | 8,9 | — | CT-LVP-21-1-Emitir Pedido sem a utilização de gôndola |
| VENDAS-4649 | Automação | Options | 2023 | 4,8 | — | CT-LVP-22-1-Login inválido |
| VENDAS-6185 | Pesquisa/Analise | Options | 2023 | 0,0 | — | Análise: Ajustar o desempenho no teste automatizado |
| VENDAS-626 | Automação | Closed | 2022 | 0,0 | Comercial -> Gestão de Verba - Transferência de Verba | CT-LVP-12-13-Emissão de um pedido utilizando dois itens e gerando verba no pedido corrente e um item |
| VENDAS-6316 | Automação | In Development | 2023 | 7,5 | — | CT-LVP-39-09-Emissão de um pedido de venda aplicando um politica de bonificação onde o pedido pode f |
| VENDAS-6320 | Automação | Closed | 2023 | 0,0 | — | Ao alterar quantidade de item inserido desconto é removido e consumo de verba mantido |
| VENDAS-9194 | Refatoração | Options | 2024 | 3,8 | — | Refatoração: Melhoria no total ui test |
| VENDAS-9738 | Automação | Options | 2024 | 11,0 | Comercial -> Emissão de Pedidos - Venda | 28.07 - Validação de endereço de entrega e de cobrança do cliente no pedido na carga de supervisor |

## Modelo novo com IA (a partir de 03/2026) — NÃO usar como base

Horas do Jira: Time Spent da própria atividade e Σ (inclui subtasks).

| Chave | Tipo | Status | Data | Time Spent | Σ Time Spent | Resumo |
|---|---|---|---|---|---|---|
| VENDAS-20462 | Automação | Closed | 10/03/2026 | 3:19 | 4:02 | CT011-T027-TRIBUTACAO-Emissão de pedido com Tributação Personalizada CBS |
| VENDAS-20473 | Automação | Closed | 11/03/2026 | 3:57 | 4:15 | CT032-T037-ESTOQUE-Bloqueio de bonificação quando a soma (venda e bonif) excede o estoque. |
| VENDAS-20474 | Automação | Closed | 11/03/2026 | 2:21 | 2:31 | CT032-T038-ESTOQUE-Validar a inserção de item bonificado dentro do limite de estoque disponível. |
| VENDAS-20475 | Automação | Closed | 11/03/2026 | 4:09 | 4:19 | CT032-T039-ESTOQUE - Validação de bloqueio na edição de item bonificado extrapolando estoque. |
| VENDAS-20503 | Refatoração | Closed | 12/03/2026 | 2:06 | 2:06 | REFATORAÇÃO: CT032-T031-ESTOQUE-Validação de bloqueio de fechamento de pedido com produto sem estoqu |
| VENDAS-20507 | Automação | Closed | 12/03/2026 | 0:10 | 0:41 | CT032-T040-ESTOQUE-Validação de estoque na replicação de pedido com item bonificado. |
| VENDAS-20519 | Automação | Closed | 13/03/2026 | 3:00 | 3:12 | Validar bonificação na replicação com estoque insuficiente |
| VENDAS-20525 | Pesquisa/Analise | In Development | 14/03/2026 | 42:28 | 52:53 | Estudo do teste automatizado com IA - SUB POR MODULO |
| VENDAS-20527 | Refatoração | Closed | 14/03/2026 | 6:18 | 6:18 | CT001-T001-SISTEMA-Validar login com credenciais válidas |
| VENDAS-20542 | Refatoração | Closed | 16/03/2026 | 1:27 | 1:27 | Validar bloqueio de login com credenciais inválidas |
| VENDAS-20543 | Automação | In Development | 16/03/2026 | 1:33 | 1:33 | Alterar Senha Respeitando Limite de Doze Caracteres |
| VENDAS-20588 | Ajuste | Options | 17/03/2026 | 0:40 | 0:40 | AJUSTE: cenários de desconto da capa |
| VENDAS-20598 | Ajuste | Closed | 18/03/2026 | 3:04 | 3:04 | AJUSTE: CT032-T005 - Validação da pop-up de registro de falta com ajuste de quantidade de venda. |
| VENDAS-20599 | Ajuste | Closed | 18/03/2026 | 0:55 | 0:55 | AJUSTE: CT003-003-Inserção de item utilizando o filtro de desconto quantidade na tela de inserção no |
| VENDAS-20600 | Ajuste | Closed | 18/03/2026 | 0:45 | 0:45 | AJUSTE: CT029-T003-NOVOCLIENTE - Cadastrar um novo cliente e emitir um pedido com desconto promocion |
| VENDAS-20602 | Ajuste | Closed | 18/03/2026 | 0:00 | 0:00 | AJUSTE: CT006-T008-Validação de geração da NFE no fechamento do pedido. |
| VENDAS-20632 | Pesquisa/Analise | Options | 19/03/2026 | 37:40 | 37:40 | ESTUDO: Teste automatizado Web |
| VENDAS-20761 | Ajuste | Closed | 27/03/2026 | 0:33 | 0:33 | AJUSTE: Cenários de Estoque no novo padrão |
| VENDAS-20762 | Refatoração | Closed | 27/03/2026 | 0:21 | 0:21 | CT029-T009-Busca de Endereço por CEP no Cadastro de Novo Cliente |
