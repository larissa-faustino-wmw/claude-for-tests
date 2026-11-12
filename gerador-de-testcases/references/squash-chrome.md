# Squash TM pelo Chrome

O Squash da WMW (`https://squash.wmw.com.br/squash`) não tem MCP: consulta e cadastro são feitos pela extensão Claude in Chrome, na sessão do tester.

As telas mudam entre versões do Squash. Os nomes abaixo são os mais comuns; **leia a tela** (`read_page` / `find`) antes de cada ação e, se algo não bater, descreva o que viu e pergunte em vez de improvisar.

## Preparação

1. Carregue as ferramentas numa chamada só:
   `ToolSearch select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__find,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__form_input,mcp__claude-in-chrome__get_page_text`
2. `tabs_context_mcp`, depois abra uma **aba nova** (não use as abas do tester).
3. Navegue para `https://squash.wmw.com.br/squash/test-case-workspace`.
4. Caiu na tela de login? Peça para o tester entrar e avisar. **Nunca digite usuário ou senha.**

## Leitura pela API REST (preferida)

Com o tester logado, a API REST do Squash responde na mesma sessão do Chrome: basta navegar até a URL e ler com `get_page_text`. É JSON, mais rápido e confiável que ler a árvore da tela. **Use a API só para leitura (GET)**; cadastro e edição continuam pela tela.

| O quê | URL |
|---|---|
| Conteúdo de uma pasta (casos com `name` e `reference`) | `https://squash.wmw.com.br/squash/api/rest/latest/test-case-folders/<id>/content?size=500` |
| Um caso (passos, prerequisite, campos, requisitos verificados) | `https://squash.wmw.com.br/squash/api/rest/latest/test-cases/<id>` |

O projeto VENDAS é o id `6`. A label `DEV_TESTS` fica no campo personalizado de código `labels` do caso (`custom_fields`).

## Consultar (numeração e duplicidade)

1. Na árvore da biblioteca, abra o projeto **VENDAS** e localize a pasta do prefixo.
2. Leia as References dos casos da pasta (a lista da pasta, ou a pesquisa de casos de teste filtrando por Reference `<PREFIXO>-LVP-`). Use `get_page_text` para ler a lista inteira em vez de rolar e olhar.
3. Anote o **maior número** de LVP e de LVW.
4. Leia os nomes dos casos da pasta e procure algum que já cubra o mesmo comportamento do cenário novo. Encontrou? Mostre ao tester (Reference, nome, link) e proponha reaproveitar ou atualizar.
5. Pasta não encontrada: procure por nome na árvore e na pesquisa. Se não existir, leve isso para a rodada de dúvidas (proposta de pasta nova).

## Cadastrar (só depois do "pode cadastrar")

Para cada caso aprovado, um de cada vez:

1. **Reconfira a numeração** na pasta (alguém pode ter cadastrado no meio tempo).
2. Selecione a pasta na árvore e use o botão de criar (**+** / **Create** → **Test case** / **Novo caso de teste**).
3. No diálogo: **Name** (sem a Reference), **Reference**, **Description**. Confirme com **Add** / **Adicionar**.
4. Abra o caso criado. Na aba de informações, preencha **Importance/Weight**, **Nature**, **Type** e, se existir, o campo de label/tag com `DEV_TESTS` (só quando a atividade tiver a label). Valor que não existe na lista: escolha o mais próximo e anote para avisar.
5. **Prerequisite**, se a tela tiver o campo: os pré-requisitos.
6. Aba **Steps / Passos**: adicione um passo por linha (Action, Expected result). Para o PERSISTENCIA-001, use **Call a test case / Chamar um caso de teste** e escolha o caso 3463.
7. Confira o caso salvo contra a versão aprovada (Reference, nome, campos, número e ordem dos passos). Diferença: corrija antes de seguir para o próximo.
8. Guarde o id da URL (`/test-case/<id>/`) para o link.

## Vincular ao requirement e à sprint (depois de todos os casos)

**Requirement** (espaço de requisitos):

1. Procure o requirement cuja **Reference** é a chave da atividade (`VENDAS-xxxxx`).
2. Não encontrou: pare e pergunte ao tester. Não crie requirement sem ele pedir.
3. Na cobertura do requirement (**Verified by / Coberto por** test cases), adicione todos os casos criados. Confira se aparecem na lista; caso já vinculado não se adiciona de novo.

**Sprint** (aba **Executions**):

1. Abra a lista de sprints e identifique a **próxima** (a que ainda não começou, a seguir da atual). É a mesma mostrada na aprovação; se a tela mostrar outra situação (duas candidatas, nenhuma futura), pare e pergunte.
2. Adicione o requirement `VENDAS-xxxxx` à sprint. Os casos vinculados a ele entram junto.
3. Confira que o requirement aparece na sprint. Se ele já estava lá, só confira que os casos novos apareceram.

## Regras

- Um clique em salvar por vez. Se aparecer erro ou a tela travar, **confira se o caso foi criado** (procure pela Reference) antes de tentar de novo, para não duplicar.
- Não edite, mova, renumere nem apague casos existentes sem o tester pedir.
- Pasta nova só com aprovação, com o nome aprovado.
- Não dispare diálogos de confirmação do navegador (excluir, sair sem salvar). Se um aparecer, pare e peça ao tester para fechar.
- Se a extensão não responder depois de 2 ou 3 tentativas, pare e devolva os cenários prontos para cadastro manual, dizendo o que ficou pendente.

## Sem Chrome

Entregue a matriz e os cenários no formato de `references/modelo-saida.md`, com a Reference `<PREFIXO>-LVP-???`, e diga ao tester que a numeração e o cadastro precisam ser feitos à mão.
