# Squash: ler o plano e registrar a execução

## Ler (API REST, só leitura)

Com o tester logado no Chrome, navegar até a URL e ler com `get_page_text`.

| O quê | URL |
|---|---|
| Plano de uma iteração (itens, caso, status, execuções) | `https://squash.wmw.com.br/squash/api/rest/latest/iterations/<id>/test-plan?size=200` |
| Um caso (passos, pré-requisito, resultado esperado) | `…/api/rest/latest/test-cases/<id>` |
| Uma campanha (iterações) | `…/api/rest/latest/campaigns/<id>` |
| Pastas de campanhas | VERSÕES `campaign-folders/137`, HOMOLOGAÇÕES `campaign-folders/107`, TESTES INTERNOS `campaign-folders/188` (`/content?size=200`) |

Status de execução que aparecem: `READY` (não executado), `RUNNING` (em andamento), `SUCCESS`, `FAILURE`, `BLOCKED`, `UNTESTABLE`.

Os casos de uma atividade: os ligados ao requirement com Reference = a chave do Jira, que a `gerador-de-testcases` coloca na próxima sprint em Executions. Se não achar o item no plano, pergunte em qual iteração ou sprint está.

Itens com `referenced_test_case: null` (caso apagado da biblioteca) aparecem no plano: cite, não execute.

## Registrar (pela tela)

A tela do Squash muda entre versões: **leia a tela** (`read_page`/`find`) antes de agir, e pergunte se algo não bater.

1. Abra a iteração (ou sprint) e o item do caso no plano de teste.
2. Inicie a execução (botão de executar / "Run"; prefira a execução passo a passo).
3. Para cada passo: o status (Passou / Falhou / Bloqueado / Não testável), o comentário com o que foi visto (valor, mensagem) e o anexo da evidência (print).
4. Comentário geral da execução: ambiente (Tomcat de dev, homologação), base, modo (automatizado, assistido, manual) e, em falha, a chave do Defect.
5. Encerre a execução e confira, pela API, o novo `execution_status` do item.

Regras:

- Um clique por vez; erro ao salvar: confira se a execução foi gravada antes de repetir.
- Não altere execuções antigas nem de outro tester; registre uma nova.
- Não mude atribuição (`assigned_to`) nem o plano (adicionar ou tirar casos) sem o tester pedir.
- Caso automatizado: registre o resultado da execução automatizada da mesma forma, citando a classe e o relatório.
