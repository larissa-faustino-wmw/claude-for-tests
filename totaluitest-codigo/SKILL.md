---
name: totaluitest-codigo
description: Escreve ou refatora testes automatizados do app Lavendere no framework TotalUiTest da WMW (repositório totaluitest, JUnit 5, @PDATotalUITest), com a massa de dados embutida em @InvokeInit via ParametrosTestUtil/TabelasTestUtil, JavaDoc com Squash e Jira, comentários de Passo/Resultado Esperado, e entrega também o cenário para o Squash, o texto do worklog e a lista de classes alteradas. Use SEMPRE que o usuário pedir para escrever, gerar, automatizar, codificar ou refatorar um teste automatizado ou um cenário do Squash/Confluence (CTxxx-Txxx, CT-LVP-x-y), migrar massa .sql para @InvokeInit, montar massa de dados de teste, ou mencionar TotalUiTest, TBLVP, @PDATotalUITest, waitOpening, waitValue, ParametrosTestUtil, TabelasTestUtil, DatasTestUtil ou Pages do framework — mesmo que diga só "automatiza esse cenário".
---

# Código de teste TotalUiTest

Você é um especialista sênior em automação de testes no framework TotalUiTest da WMW. Escreve testes do app (lavenderepda) que seguem o padrão novo do time, usando só o que existe no repositório `totaluitest`.

## Entregas

Toda criação ou refatoração entrega quatro coisas (formatos em `references/entregas.md`):

1. **Cenário de teste** (passos e resultados esperados), fiel ao código. Se o caso já existe no Squash, a entrega é a conferência: o que o código cobre a mais ou a menos que o caso.
2. **Código** da classe de teste, com a massa em `@InvokeInit`.
3. **Worklog do Jira**: texto pronto para o tester lançar, em primeira pessoa.
4. **Classes alteradas**: todos os arquivos criados, alterados, renomeados ou removidos.

Não há mais `.sql` solto como entrega: a massa roda em Java dentro da classe. Só gere o SQL equivalente se o tester pedir.

Se algo mudar depois (erro na execução, encoding, formato), reemita o worklog e a lista atualizados.

## Fluxo

### 1. Ler a atividade e o cenário

- **Atividade do Jira** pelo MCP interno (`get_jira_issue`): a descrição da Test Automated traz Cenário, Teste (classe), Cenário anterior (CT-LVP no Confluence), Baseado na atividade e Link do Squash. Esses links vão no JavaDoc.
- **Caso do Squash**: se o tester colar os passos, use-os. Se só houver o link e o Chrome estiver conectado, leia a aba de passos do caso. Senão, peça os passos.
- **Cenário anterior** (refatoração): o documento CT-LVP pelo `get_confluence_page` e a classe e o `.sql` legados no repositório.
- **Regra de negócio**: na dúvida sobre o que o app faz, leia o código do `lavenderepda` (a tela, o service) em vez de supor. Cite a regra no worklog quando ela embasar um assert.

Falta o link do Squash ou a atividade: pergunte ao tester antes de entregar. Nunca omita as linhas do Squash e do Jira no JavaDoc.

### 2. Mapear um teste análogo

Antes de escrever, ache no repositório um teste do padrão novo da mesma área (pasta `src/test/java/br/com/wmw/lavenderepda/presentation/ui/test/<área>/`) e use como molde: os testes novos têm `@InvokeInit` e o link do Squash no JavaDoc (`Grep "squash.wmw.com.br"`). Os antigos (JavaDoc com CT-LVP, `// passo 1`) **não** são molde.

### 3. Conferir cada método antes de usar

Todo método de Page, util ou formulário que você chamar precisa existir: confira com `Grep` na Page (`src/test/java/.../presentation/ui/page/`) e na `BasePage` (`src/main/java/br/com/wmw/totalcross/test/api/base/BasePage.java`). Método novo numa Page só quando não houver equivalente, marcado com comentário `//` explicando, e listado em Classes alteradas.

### 4. Escrever

Seguindo `references/regras-codigo.md` (estrutura, waits, asserts, documentação) e `references/massa-de-dados.md` (utils de massa, parâmetros JSON, datas).

### 5. Gravar com o encoding certo

Os `.java` do `totaluitest` são **ISO-8859-1 com CRLF**. As ferramentas Read/Edit/Write gravam UTF-8 e trocam acentos por `�` sem avisar.

- Arquivo novo: escreva num temporário e converta para ISO-8859-1 + CRLF com um script Python (`open(..., encoding="latin-1", newline="\r\n")`).
- Arquivo existente com acento: edite por script que lê e grava `latin-1` preservando o CRLF.
- Confira depois com `file -b`: tem de dizer `ISO-8859` (ou `ASCII`) `with CRLF line terminators`.
- Procure `EF BF BD` / `ï¿½` no arquivo antes de entregar.

### 6. Compilar, se possível

Se o ambiente tiver Maven e o JDK 8 (`JAVA8_HOME`), rode a compilação dos testes no repositório para pegar import e método errado. O teste de UI em si roda no ambiente do tester (Jenkins ou máquina dele); não diga que passou sem ter rodado.

## Regras essenciais

As completas estão nas referências. As que mais quebram teste:

- **Login:** `pedidoPage.logar()` (ou o `logar()` da Page do fluxo) sem parâmetros nos cenários de sucesso. Exceção (senha inválida, expirada, usuário inativo): `loginPage.logar("SENHA", false)` e `loginPage.waitOpening(WmwMessageBox.class)`.
- **Depois de todo click que muda a tela, `waitOpening(...)`** da tela, janela ou mensagem que abre.
- **Valor carregado do banco: `waitValue(esperado, "id")`**, nunca leitura direta logo depois de abrir a tela.
- **Filtro de cliente:** `clickEdFiltro()` antes de buscar ou selecionar cliente.
- **Sem ação dentro de Resultado Esperado**: mova para o passo seguinte.
- **Nunca alterar código de produção do app** para a automação. Componente sem id: o dev do app expõe com `setID("nomeDoId")`.
- **Parâmetro JSON precisa estar em `PARAMETROS_JSON`** do `ParametrosTestUtil`; senão o `Map` é ignorado em silêncio (ver `references/massa-de-dados.md`).

## Armadilhas

- **Parâmetro JSON fora de `PARAMETROS_JSON`:** com `Map`, nada é gravado e não há erro; com `String`, o JSON inteiro é trocado e o teste termina em `TimeoutException`.
- **Encoding.** `.java` em ISO-8859-1 com CRLF; Read/Edit/Write gravam UTF-8 e trocam acento por `�` sem avisar.
- **Teste antigo não é molde.** JavaDoc com CT-LVP e `// passo 1` são do padrão velho; o molde tem `@InvokeInit` e link do Squash.
- **`TabelasTestUtil.delete` com WHERE vazio apaga a tabela inteira.**
- **`/**` dentro do método** gera "Dangling Javadoc comment": passos usam `/*`.
- **`ETelas` não existe.** Os exemplos antigos citavam; só crie o enum se precisar.
- **Há vários `logar()`** (LoginPage, PedidoPage, ClientePage, AgendaPage…): use o da Page do fluxo.

## Cuidados

- Não use classe ou método que você não conferiu no repositório.
- Não refatore Pages ou testes fora do escopo pedido; limpeza pequena no arquivo que você já mexe, sim.
- Não commite nem faça push sem o tester pedir. Commit leva só o código da atividade (`VENDAS-xxxxx`).
- Sem dados reais (CPF, CNPJ, e-mail, senha) na massa.
