# Criar a atividade pelo Claude in Chrome

Procedimento do Passo 5. Só comece depois da aprovação do tester.

## Antes de começar

- Leia a skill `chrome-browser` se ainda não leu nesta conversa, e carregue as ferramentas do Claude in Chrome **numa única** chamada do ToolSearch: `tabs_context_mcp`, `tabs_create_mcp`, `navigate`, `computer`, `read_page`, `find`, `form_input`, `get_page_text`, `file_upload` (este último só se houver anexo no computador).
- Chame `tabs_context_mcp` e abra **uma aba nova**; não use as abas do tester.
- Não clique em nada que abra alerta ou confirmação do navegador (excluir, descartar). Se aparecer, peça ao tester para fechar.
- Se uma ação falhar 2 ou 3 vezes, pare e conte ao tester o que tentou; não fique repetindo.

## 1. Entrar no Jira

1. Navegue para `https://jira2.wmw.com.br`.
2. Se aparecer a tela de login, peça ao tester para entrar e avisar. **Nunca digite usuário nem senha.**
3. Descubra o usuário logado (menu do avatar no canto superior direito, ou o campo Reporter preenchido na tela de criação). Ele é o Reporter padrão e o Assignee da Testing.

## 2. Abrir a tela de criação

**Atividade solta** (Bug, Suggestion, Test Automated, outros):

1. Clique no botão **Create** da barra superior.
2. No diálogo, escolha **Project** e **Issue Type** conforme a referência do tipo.
3. Trocar o Issue Type recarrega o formulário: leia a página de novo (`read_page`/`find`) antes de preencher qualquer campo.
4. Se houver o botão **Configure Fields**, deixe em **All**, para todos os campos aparecerem.

**Subtask** (Defect, Testing):

1. Navegue para `https://jira2.wmw.com.br/browse/<CHAVE-DA-PAI>`.
2. Clique em **More → Create sub-task**. Se a atividade já tem subtasks, também dá pelo botão **+** / **Add** da lista de subtasks.
3. Escolha o Issue Type (`Defect` ou `Testing`) e leia a página de novo.

## 3. Preencher

- **Summary**: o título aprovado, exatamente.
- **Selects e listas** (Priority, Phase, SDLC phase, Test Case Type, Feature, Customer): use `form_input` quando for um `<select>`. Campos com busca (Customer, Feature, Features Involved, Labels, Assignee) aceitam digitação: digite o valor, espere a lista de sugestões e clique na opção exata. Não deixe texto digitado sem escolher a opção — o Jira descarta ou cria um valor errado.
- **Environment**: é múltipla escolha (Web, App, Other); marque todas as aprovadas.
- **Description**: clique na aba **Text** do campo, apague o conteúdo e digite a marcação aprovada (`references/formatacao-jira.md`). Depois clique em **Visual** e tire uma captura para conferir a formatação. Se o texto não entrou pelo `form_input`, clique dentro do campo e digite com `computer` (ação de digitação).
- **Anexos**: se o arquivo está no computador, use `file_upload` no campo Attachment. Prints que só vieram colados no chat não são arquivos: liste-os para o tester anexar depois da criação.
- **Campos que a referência manda deixar em branco**: não toque.

## 4. Conferir e criar

1. Role o formulário inteiro e confira cada campo contra a versão aprovada (captura de tela).
2. Diferença em relação ao aprovado (campo obrigatório que você não previu, valor que não existe na lista): **pare e pergunte** ao tester antes de criar.
3. Clique em **Create** uma vez só.
4. Se o diálogo continuar aberto com erro em vermelho, leia o erro, corrija (ou pergunte, se a correção mudar o conteúdo) e tente de novo.

## 5. Depois de criar

1. O Jira mostra a mensagem "Issue <CHAVE> - <título> has been successfully created" com link. Pegue a chave.
2. Abra `https://jira2.wmw.com.br/browse/<CHAVE>` e confira título, descrição (formatação) e campos.
3. Faça os passos pós-criação do tipo (Testing: atribuir ao QA logado e mover para Em Andamento).
4. Devolva o link ao tester.

## Se algo der errado no meio

- Antes de tentar criar de novo, verifique se a atividade não foi criada: busque pelo título no Jira (ou pela lista de subtasks da pai). Duas atividades iguais geram retrabalho para o time.
- Se o Chrome não responder ou a extensão não estiver conectada, entregue ao tester o título, a descrição (a marcação para colar no modo Text) e a tabela de campos, para criar manualmente.
