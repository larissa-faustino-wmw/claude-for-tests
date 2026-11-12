# Regras de código

## Estrutura da classe

Molde (padrão novo, ex.: `test/tributacao/ivaDual/ValidarIbsCbsPedidoMistoComESemIcmsStTest.java`):

```java
package br.com.wmw.lavenderepda.presentation.ui.test.<area>;

import static org.junit.jupiter.api.Assertions.assertEquals;
// imports da Page, das telas usadas no waitOpening, dos utils e do InvokeInit

/**
 * <Título do cenário>
 *
 * @author <tester que está criando o cenário>
 * @version <versão, ex.: 9.068>
 * @see <a href="<link do caso no Squash>">Squash TM</a>
 * @see <a href="https://jira2.wmw.com.br/browse/<CHAVE>">Atividade Jira</a>
 * @see <a href="https://confluence.wmw.com.br/confluence/pages/viewpage.action?pageId=<id>"><CT-LVP-x-y-Título></a>
 */
@PDATotalUITest
public class <Verbo><Assunto>Test {

	@InvokeInit
	public void prepararMassaDeDados() throws Exception { ... }

	@Test
	public void deve<ComportamentoEsperado>() { ... }
}
```

- **Squash e Jira são obrigatórias** no JavaDoc, em toda criação e refatoração. Os links estão na descrição da Test Automated. Sem eles, pergunte ao tester; nunca omita.
- **Confluence é adicional**: entra quando há documento do cenário anterior (CT-LVP-x-y). Use o link com `pageId`, não o curto (`wiki.wmw.com.br/confluence/x/...`). Sem documento, omita só essa linha.
- Nome da classe com verbo e o comportamento (`Validar…`, `Emitir…`, `Bloquear…`) terminando em `Test`; método `deve…`.

## Comentários de passo

Cada passo e cada resultado esperado em bloco **multilinha com `/*`** (um asterisco), rótulo na primeira linha e descrição nas seguintes:

```java
/*
 * Passo 1:
 * Efetuar login no App, acessar Pedidos e iniciar um novo pedido.
 */

/*
 * Resultado Esperado 1:
 * A capa do pedido abre com o cliente "CLIENTE PJ".
 */
```

- Nunca `//` nem comentário de uma linha para passo.
- Nunca `/**` dentro do método (a IDE acusa "Dangling Javadoc comment").
- Todo passo tem um Resultado Esperado com o mesmo número, em sequência.
- O primeiro passo sempre começa pelo login.

## Sincronização

- Depois de **todo** click que abre tela, janela, combo ou mensagem: `waitOpening(<Classe>.class)` dessa tela. Ex.: `pedidoPage.waitOpening(CadPedidoForm.class)`, `pedidoPage.waitOpening(WmwMessageBox.class)`.
- Menu de opções (burger): `clickBmOpcoes()` e `waitOpening(ButtonOptions.getClassWindowOptions())`.
- Valor que o app carrega do banco: `waitValue(esperado, "idDoComponente")`. Ele faz polling até o valor real substituir o placeholder, então o `assertEquals` fica confiável mesmo com a latência do SQLite.
- Espera no lugar certo: logo depois da ação, não no começo do passo seguinte. Sem `waitOpening` redundante.
- Sem `Thread.sleep`.

## Validações

- `assertEquals(esperado, obtido, "mensagem")` com o valor esperado concreto. Evite `assertTrue`/`assertNotNull` onde cabe `assertEquals`, e `contains`/`startsWith` onde cabe a string completa.
- Mensagem do assert descreve a falha do campo validado ("Total do pedido incorreto."), sem duplicar entre asserts.
- Mensagens do app: `assertEquals("<texto exato>", page.getMessage(), "Mensagem de confirmação incorreta.")` (`getMessage()` está na `BasePage`).
- String de item na lista: valide a string completa concatenada, `[Código] - [Descrição] [Quantidade] [Unidade] - [Preço Unitário] [Preço Total]` (ex.: `"10 - AGUA MINERAL COM GAS 1,55,00 itens - R$3,70R$ 18,50"`).
- Getter usado uma vez vai direto no `assertEquals`, sem variável intermediária.
- Sem `return`, `if` ou `try/catch` que deixe o teste verde sem testar.

## Variáveis

- Declare só quando o valor é reutilizado (ex.: número do pedido para rowkeys), como `final`, o mais perto possível do primeiro uso (no máximo 3 linhas antes).
- Número do pedido: `getValueLbNuPedidoInCaditemPedidoForm()` logo no início da inserção de itens.

## Métodos úteis do `PedidoPage` (conferidos)

| Método | Uso |
|---|---|
| `logar()` | login de sucesso (também há `logar()` em outras Pages do fluxo) |
| `clickEdFiltro()` | antes de buscar ou selecionar cliente |
| `clickBmOpcoes()` | abre o menu de opções |
| `clickTabDinamicaDetalhes()` | aba de detalhes (status, datas) que não aparecem na capa |
| `selectcbStatusPedido("Fechado2")` | filtro de status na lista de pedidos |
| `clickBtExcluirPedido()` | encerra fluxos de erro limpando a base local |
| `getValueLbNuPedidoInCaditemPedidoForm()` | número do pedido na inserção de itens |

`LoginPage`: `logar()`, `logar(senha)`, `logar(senha, esperaTelaPosLogin)`, `logar(id, value, senha[, esperaTelaPosLogin])`. Nos cenários de exceção de login: `logar("SENHA", false)` + `waitOpening(WmwMessageBox.class)`.

Antes de usar qualquer outro método, confira que existe na Page.

## Constantes

- Valores fixos de negócio (códigos de tela, de domínio, cores) não ficam soltos no teste: viram `public static final` na Page da automação, nunca no código do app.
- Domínio compartilhado por vários testes: um `enum` no pacote de utilitários da automação (crie se não existir e liste em Classes alteradas).

## Código de produção

Nunca altere o `lavenderepda` para atender a automação (getter novo, visibilidade). Componente sem id: peça ao dev do app o `setID("nomeDoId")` e use `waitValue`/`find` por esse id.
