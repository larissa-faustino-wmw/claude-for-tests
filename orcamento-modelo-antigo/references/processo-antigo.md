# Como era o documento de teste no Confluence (modelo antigo)

Exemplo real: **CT-LVP-8-6 — Antecipar execução de agenda de visitas** (Confluence, Setor de Qualidade, 2023).

Estrutura que o QA 1 precisava produzir para cada cenário:

1. **Informações gerais:** objetivo, CSUs relacionados, versão do CT.
2. **Pré-condições:** parâmetros configurados na web com seus valores. No exemplo: 649 = 2, 1709 = 1 e o parâmetro JSON 140 com cinco propriedades.
3. **Local dos inserts e do backup** da base usada no cenário (pasta de rede "Automatização-testes-regressão\Scripts cenário X").
4. **Avisos** sobre dados variáveis (ex.: datas relativas ao dia de execução).
5. **Tabela de passos:** cada passo agrupa várias ações; para cada um, o resultado esperado com valores concretos (cliente, tabela de preço, condição de pagamento, total 74,80, status, origem) e **um print da tela com destaques em vermelho**.

O exemplo tem 9 passos e 9 prints. Para orçar a etapa de documentação, conte os passos do cenário: cada passo exigia executar o fluxo, capturar a tela, marcar os campos e escrever o resultado esperado.

Referência de custo de cenários da mesma área (Agenda de Visitas, 2023): VENDAS-4664 (CT-LVP-8-8, registrar/atualizar/desfazer chegada) 12,3 h e VENDAS-4665 (CT-LVP-8-9, registrar saída) 10,8 h.
