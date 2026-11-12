# Estrutura do webuitest

Conferida no repositório (branch `main`, commit `50553af`) em 10/11/2026. Playwright 1.55.0, JUnit 5.12.2, JDK 17, Maven 3.8.5. Releia as classes antes de usar: a infraestrutura vai crescer.

## Pacotes

| Pacote | Classe | O que faz |
|---|---|---|
| `config` (main) | `ConfiguracaoTeste` | lê `webuitest.properties` ou, no workspace, `workspace.properties` da raiz; `get`, `getBoolean`, `getInt`, `getCaminho`, `getObrigatorio` |
| `tomcat` (main) | `ServerXml` | a porta do Tomcat, lida do `conf/server.xml` |
| | `TomcatLocal` | a URL base (`montaUrlBase(contexto)`) |
| | `LogErroTomcat` | o que o `error.log` da aplicação ganhou desde um ponto |
| `banco` (main) | `BancoTeste` | conexão JDBC com a base `web` ou `app` do Tomcat do dev (`BancoTeste.de(configuracao, BancoTeste.BASE_WEB).abreConexao()`); senha só do arquivo de configuração |
| | `CatalogoMenu`, `AcaoMenu` | o comando (`NMCOMANDOACAO`) de cada item de menu |
| `web` (main) | `SessaoWeb` | navegador logado: `abre(configuracao, urlBase)`, `entra(usuario, senha)`, `listaItensMenu()`, `abre(ItemMenu)` → `ResultadoAbertura`, `salvaImagem(Path)`, `getPagina()` |
| | `ItemMenu` | um item do menu: `contexto()`, `url()`, `getChaveMenu()` (`cdSistema,cdMenu`) |
| | `ResultadoAbertura` | status, URL, mensagens de erro JSF visíveis, respostas 5xx, erros de JavaScript e diálogos da abertura |
| (test) | `AmbienteLocal` | `carregaOuPula()`, `abreSessaoLogada()`, `getUrlBase()`, `getLogErro()`, `getPastaSaida()` |
| (test) | `SmokeTelasTest` | abre cada tela do menu e reprova por 4xx/5xx, erro JSF visível ou linha nova no `error.log` |

## Abrir a tela do cenário

```java
ItemMenu item = sessao.listaItensMenu().stream()
	.filter(i -> i.getChaveMenu().orElse("").equals("<cdSistema>,<cdMenu>"))
	.findFirst()
	.orElseThrow(() -> new IllegalStateException("O usuario de teste nao tem a tela <cdSistema>,<cdMenu> no menu"));
ResultadoAbertura abertura = sessao.abre(item);
// conferir abertura: status < 400, sem mensagem de erro JSF, sem 5xx
FrameLocator tela = sessao.getPagina().frameLocator("#contentFrame");
```

- Identifique a tela pela **chave `cdSistema,cdMenu`**, nunca pela posição no menu (menu e ordem mudam por ambiente).
- A chave sai do banco web (tabelas de menu, ver `CatalogoMenu`) ou do `target/webuitest/smoke/menu.tsv` gerado pelo smoke.
- Abrir o item **executa o comando** dele. Abra só a tela do cenário; comando que não seja `showList`/`open` merece conferência do dev antes.

## Conferir erro depois de uma ação

Os mesmos critérios do smoke:

- mensagem de erro do JSF **visível**: `frame.locator(".wmw-errorMessage >> visible=true")` deve ter `hasCount(0)`;
- resposta 5xx: registre com `pagina.onResponse` (a `SessaoWeb` já registra durante a abertura);
- `error.log`: `LogErroTomcat` antes e depois da ação.

Se mais de um teste precisar disso, o lugar é um método na `SessaoWeb` ou um utilitário novo, combinado com o tester (é a primeira infraestrutura de negócio).

## Dados e limpeza

O banco de dev **não tem reset**.

- O teste cria os próprios registros (por JDBC com `BancoTeste` ou pela própria tela) com um **marcador único** no texto (ex.: `"WEBUITEST " + System.currentTimeMillis()`), para achar e apagar.
- Apaga em `@AfterEach` ou `finally`, inclusive quando falha, por chave ou pelo marcador. Nunca `DELETE` sem `WHERE`.
- Não conte com dado que outro teste deixou, nem com a ordem dos testes.
- Colunas e tabelas: a fonte é a classe de domain do `lavenderecore` (`@TableName`), não o `docs/modelo-er/`. Os três SGBDs (SQL Server, PostgreSQL, Oracle) precisam aceitar o SQL: prefira SQL simples e parâmetros (`PreparedStatement`).
- Parâmetro de configuração que o teste muda: guarde o valor original e restaure no `@AfterEach`.

## Rodar

```bash
mvn test -Dtest=AmbienteLocalTest                         # diagnóstico do ambiente
mvn test -Dtest=<Classe>Test                              # o teste
mvn test -Dtest=<Classe>Test -Dnavegador.headless=false   # vendo a janela
```

- Precisa do Tomcat de dev de pé com o wmwvendas publicado. Subir e refazer o build: scripts `dev/dev-*` da raiz do workspace (`dev/README.md`). Antes de subir, veja se a porta do `server.xml` já responde: o dev pode estar com o Tomcat dele aberto. **Pergunte antes** de subir ou derrubar.
- Suba destacado (`Start-Process "<workspace>\dev\dev-run.bat" -WindowStyle Minimized`), não por tarefa em segundo plano, que mata o Tomcat quando expira.
- Saídas em `target/webuitest/` (imagens, `menu.tsv`).

## Regras do repositório (CLAUDE.md do webuitest)

- Nada da máquina do dev em código ou arquivo versionado; chave nova de configuração entra também no `webuitest.properties.example`, comentada.
- Não leia nem grave a senha.
- Porta do `server.xml`, nunca constante.
- `.java` ISO-8859-1 + CRLF; fontes em ASCII puro.
