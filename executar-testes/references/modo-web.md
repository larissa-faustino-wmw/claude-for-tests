# Web (wmwvendas)

## Automatizado (o caso já tem teste no webuitest)

Quando houver: `mvn test -Dtest=<Classe>` no `projetos/webuitest`, com JDK 17 e o Tomcat de dev de pé (diagnóstico antes: `mvn test -Dtest=AmbienteLocalTest`). Saídas e prints em `target/webuitest/`. Escrever esses testes é com a skill `webuitest-codigo`.

## Assistido (pelo Claude in Chrome)

Enquanto não há teste automatizado, a execução assistida na Web é pelo Chrome do tester.

### Antes

1. Carregue as ferramentas do Chrome numa chamada só (`tabs_context_mcp`, `tabs_create_mcp`, `navigate`, `read_page`, `find`, `computer`, `form_input`, `get_page_text`) e abra uma **aba nova**.
2. **Ambiente:** o Tomcat de dev (`http://localhost:<porta>/wmwvendas/`, porta do `server.xml`) ou o ambiente que o tester indicar. Tomcat parado: pergunte antes de subir (`dev/dev-*` da raiz do workspace).
3. **Login:** peça ao tester para entrar. Só no Tomcat local, e se o tester pedir, use o usuário de teste do arquivo de configuração do workspace; em homologação ou base de cliente, sempre o tester.
4. Depois do login, a Web abre popups em cadeia (recados, novidades, aniversariantes): feche-os antes de seguir.
5. Pré-requisitos do caso (parâmetros, massa): pela própria tela, quando for assim que o caso manda; senão, peça ao tester ou faça pelo banco de dev com aprovação. Anote o que mudou, para restaurar.

### Durante

- A tela abre no **iframe `#contentFrame`**: leia o conteúdo dele (`read_page`, `get_page_text`).
- Ache os campos pelo rótulo visível ou pelo id do componente (no `.xhtml` da tela, em `projetos/lavendereweb/webapp/views/`).
- Depois de cada ação que vai ao servidor, confira:
  - mensagem de erro do JSF **visível** (`.wmw-errorMessage`; há mensagens escondidas que não contam);
  - o log do Tomcat (`logs/localhost.<data>.log` e o `error.log` da aplicação, `log/vendas/error.log`): erro de JSF às vezes só aparece ali.
- **Evidência:** screenshot de cada resultado esperado e o valor lido.
- Não dispare diálogos de confirmação do navegador (excluir, sair sem salvar) sem avisar: eles travam a extensão.
- Botões de ação irreversível (excluir, enviar ao ERP, aprovar): só quando o caso manda e no ambiente de teste.

### Depois

- Restaure o que alterou e feche a aba que a skill abriu.
- Registros criados pelo caso: liste no resumo (o banco de dev não tem reset).
