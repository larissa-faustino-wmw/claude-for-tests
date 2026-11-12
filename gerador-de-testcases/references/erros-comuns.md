# Erros que o desenvolvedor esquece

O dev implementa o que está escrito e testa a lógica que imaginou. O usuário real faz outras coisas: volta tela, sai no meio, digita do jeito dele, perde a conexão, repete o clique. Para cada critério de aceite, passe por esta lista e transforme em cenário (ou em passo de um cenário existente) o que se aplica à funcionalidade. Não force: item que não tem relação com a tela fica de fora.

Cenário que vem desta lista entra na matriz com o motivo na Descrição Funcional ("usuário volta da tela de itens sem salvar").

## Ordem e caminho

- Fazer os passos em **outra ordem** da que a história descreve (informar o desconto antes do item, trocar a condição de pagamento depois de inserir itens).
- **Voltar** para uma tela anterior e alterar algo que já foi usado no cálculo (trocar o cliente, a tabela de preço ou o tipo de pedido com itens já inseridos).
- **Sair sem salvar** (botão voltar do aparelho, fechar a aba, trocar de menu) e entrar de novo: o que ficou gravado? aparece mensagem?
- Entrar na funcionalidade por **outro caminho** (pelo menu, pela lista, pelo atalho, pela agenda, pela consulta de cliente).
- **Reabrir** o registro salvo e editar: o valor recalcula? o que era padrão sobrescreve o que o usuário digitou?
- **Duplicar, copiar ou replicar** (replicação de pedido, pedido a partir de orçamento): a regra nova vem junto?

## Entrada de dados

- Campo **vazio**, só **espaços**, **zero**, **negativo**, valor **muito alto**.
- **Casas decimais** além do permitido, vírgula x ponto, colar texto com máscara (CNPJ com pontos, telefone com parênteses).
- Texto **longo** (limite do campo, quebra no relatório ou no PDF), acentos e caracteres especiais (`'`, `"`, `&`, `%`).
- Mudar um valor e **não sair do campo** antes de salvar.
- Valores no **limite exato** da regra (igual ao mínimo, igual ao máximo, um centavo acima).

## Repetição e concorrência

- **Clique duplo** em Salvar, Enviar, Aplicar, Fechar pedido: grava duas vezes? aplica duas vezes?
- Aplicar, **remover e aplicar de novo** (cupom, desconto, bonificação, política).
- O mesmo registro alterado no App e na Web antes da sincronização.
- Dois itens iguais no mesmo pedido.

## Estado do sistema e do aparelho

- **Sem conexão** no meio da operação; conexão volta depois.
- **Sincronizar** no meio do fluxo (pedido aberto, item em edição).
- Aplicativo **fechado à força** ou aparelho **reiniciado** antes de salvar e depois de salvar.
- **Data e hora**: virada do dia, fim do mês, horário de verão, data do aparelho diferente da do servidor.
- Usuário com **outro perfil** (supervisor x representante, sem permissão da tela).
- **Mais de uma empresa** ou representante na base: a regra respeita a empresa selecionada?
- Carga **grande** (muitos itens, muitos clientes): a tela continua utilizável?

## Configuração

- O mesmo fluxo com o **parâmetro desligado**: a funcionalidade some de verdade? nada quebra?
- Parâmetro com **valor vazio** ou fora do esperado.
- Combinação com **outras funcionalidades** que mexem no mesmo valor (desconto + bonificação + cashback + política comercial; tributação + frete).
- **Cliente** com cadastro incompleto, bloqueado, novo cliente, prospect.
- **Produto** sem preço, sem estoque, bloqueado, com unidade alternativa, com grade.

## Saída e efeitos colaterais

- O valor da tela é o mesmo do **PDF, impressão, e-mail, relatório e totalizadores**?
- O que a tela mostra é o que **vai para o ERP / Web** depois da sincronização?
- **Mensagens**: o texto da mensagem ajuda o usuário a resolver? aparece uma vez só? some depois de corrigido?
- Depois de **cancelar** a operação, o sistema volta ao estado anterior por inteiro?
