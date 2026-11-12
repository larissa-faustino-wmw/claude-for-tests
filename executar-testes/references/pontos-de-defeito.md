# Pontos que escondem defeito

Reunidos do aceite dos devs (`executar-qa`) e da experiência do time. Passe por eles em todo caso que grava, calcula ou sincroniza, mesmo que o passo do caso não peça.

## Onde o erro se esconde

- **Erro só no log.** Erro de JSF que só aparece no `localhost.<data>.log` do Tomcat ou no `error.log` da aplicação, com a tela aparentemente certa.
- **Mensagem escondida.** A Web carrega `.wmw-errorMessage` invisíveis; o App mostra erro e aviso no mesmo `WmwMessageBox`, só distinguíveis pelo texto.
- **Valor que chega depois.** Lista ou contador que carrega em outra thread (App) ou por requisição posterior (Web): conferir cedo demais dá falso "passou" ou falso "falhou".

## Sincronização App ↔ Web

- O que se perde no caminho: aspas, quebra de linha, acentos, blob (foto, assinatura).
- Inativar e excluir: o registro some na outra ponta? fica órfão?
- Reenvio: sincronizar duas vezes duplica?
- Conferir nos dois lados, não só no que gravou.

## Configuração

- **O parâmetro desligado:** a funcionalidade some de verdade e nada mais quebra.
- **Cada nível do parâmetro:** sistema, empresa, representante, quando a funcionalidade aceita.
- **Os idiomas** (pt-BR, espanhol, inglês), quando a atividade trouxe texto novo.
- Mais de uma empresa ou representante na base: a regra respeita a selecionada.

## Dados

- Dado deixado por outro teste ou outra execução no banco de dev: o caso passa ou falha por causa dele.
- Data relativa (hoje, fim do mês, fim de semana): o mesmo caso muda de resultado conforme o dia.
- Base do cliente: a configuração real dele pode tornar um passo "não testável"; registre o motivo, não force.

## Os erros que o usuário real comete

A lista da `gerador-de-testcases` (`references/erros-comuns.md`) vale também na execução: voltar uma tela e alterar, clique duplo em salvar, sair sem salvar, sem conexão no meio, valor no limite exato. Quando o caso não cobre e for barato, experimente de passagem e registre o que viu num comentário (não como falha do caso).
