# Regras de Playwright (Java) para o webuitest

Adaptadas das instruções oficiais de geração de testes Playwright (TypeScript, Python e .NET) do repositório github/awesome-copilot e do agent "Playwright Tester Mode", para Java e para as telas JSF do `framework-web`. As instruções originais não têm versão Java nem falam de Page Object, dados ou JSF: essas partes são do time.

## Localizadores

Ordem de preferência:

1. **Papel acessível com nome** — `frame.getByRole(AriaRole.BUTTON, new FrameLocator.GetByRoleOptions().setName("Salvar"))`, quando o botão tem texto visível ou `title`.
2. **Rótulo** — `getByLabel("Cliente")`, quando o campo está num `layout:formGrid` (é ele que desenha o `<label>`). Confira no HTML que o `<label>` está ligado ao campo; se não estiver, `getByLabel` não acha.
3. **Id do `.xhtml` pelo sufixo** — `frame.locator("[id$=':btnSalvar']")`. O JSF prefixa o id do formulário (`cadPedidoForm:btnSalvar`); o sufixo sobrevive a mudança de formulário. É a opção mais comum nas telas do Lavendere, porque muitos componentes não expõem papel ou rótulo.
4. **Texto** — `getByText(...)`, para conferir conteúdo, não para achar campo.

Nunca: ids gerados (`j_idt123`), posição (`nth`, `:nth-child`), XPath de layout, classes de estilo (`.col-md-4`). Localizador ambíguo (o strict mode do Playwright reclama de mais de um elemento): refine, não use `.first()` para calar o erro. Exceção conhecida: o menu é desenhado duas vezes (desktop e mobile), e a `SessaoWeb` já trata isso.

Componente sem papel, rótulo nem id estável: peça ao dev do web para pôr `id` na tag. Não mexa no `lavendereweb`.

## Asserções

Use as asserções do Playwright, que esperam e repetem até o timeout (web-first):

```java
import static com.microsoft.playwright.assertions.PlaywrightAssertions.assertThat;

assertThat(frame.locator("[id$=':vlTotalPedido']")).hasText("R$ 1.250,00");      // texto exato
assertThat(frame.locator("[id$=':dsMensagem']")).containsText("gravado");          // parcial
assertThat(frame.locator("[id$=':nuQuantidade']")).hasValue("10");                 // valor de campo
assertThat(frame.locator("[id$=':itensTable'] tbody tr")).hasCount(3);             // quantidade
assertThat(pagina).hasURL(Pattern.compile(".*cadPedido.*"));                       // URL depois da ação
```

- **Não** leia `innerText()`/`inputValue()` para comparar com `assertEquals`: não espera, e o valor pode ainda não ter chegado. `assertEquals` fica para o que não é tela (resultado de consulta ao banco).
- `isVisible()` só quando o teste é sobre algo aparecer ou sumir; para conferir valor, use a asserção do valor.
- Estrutura de um componente (uma grade, um painel): `matchesAriaSnapshot(...)` existe na versão do repositório (1.55), útil para conferir a forma de uma tabela de totais.
- As asserções do Playwright em Java não aceitam mensagem própria: a falha mostra o localizador e o valor. Por isso o localizador tem de dizer o que é (constante da Page com nome do campo), e o Resultado Esperado do passo explica a regra.

## Esperas

- Confie no auto-waiting do Playwright: `click`, `fill` e as asserções já esperam o elemento.
- **Proibido:** `Thread.sleep`, `page.waitForTimeout`, aumentar `navegador.timeoutMs` para fazer passar.
- Ação que dispara requisição e você precisa da resposta: `pagina.waitForResponse(predicado, () -> acao)`, como a `SessaoWeb.abre`.
- Tela com polling nunca fica com a rede ociosa: não dependa de `NETWORKIDLE` (a `SessaoWeb` já tolera).

## Estrutura do teste

```java
/**
 * <Título do cenário>
 *
 * @author <tester>
 * @version <versão>
 * @see <a href="<link do Squash>">Squash TM</a>
 * @see <a href="https://jira2.wmw.com.br/browse/<CHAVE>">Atividade Jira</a>
 */
class <Verbo><Assunto>Test {

	private static AmbienteLocal ambiente;
	private SessaoWeb sessao;

	@BeforeAll
	static void carregaAmbiente() {
		ambiente = AmbienteLocal.carregaOuPula();
	}

	@BeforeEach
	void entra() {
		sessao = ambiente.abreSessaoLogada();
	}

	@AfterEach
	void limpaESai() throws Exception {
		try {
			// apaga a massa criada pelo teste (ver estrutura-webuitest.md)
		} finally {
			if (sessao != null) {
				sessao.close();
			}
		}
	}

	@Test
	void deve<ComportamentoEsperado>() {
		/*
		 * Passo 1:
		 * Abrir a tela de <tela> pelo menu.
		 */
		...
		/*
		 * Resultado Esperado 1:
		 * A tela abre sem mensagem de erro.
		 */
		...
	}
}
```

- Um arquivo de teste por cenário do Squash (é como o time rastreia), agrupado por área no pacote.
- Nome da classe com verbo e o comportamento, terminando em `Test`; método `deve…`.
- Comentários de passo no padrão do TotalUiTest (`/* Passo N: */` multilinha, nunca `//`, nunca `/**` dentro do método), um Resultado Esperado por passo.
- Comentário além dos passos só para lógica não óbvia.
- Teste de integração sempre por `AmbienteLocal.carregaOuPula()`: sem configuração local, ele é pulado, não falha. Teste unitário (sem Tomcat, banco nem navegador) não usa o `AmbienteLocal`.

## Page

As instruções oficiais não falam de Page Object; o time usa no TotalUiTest e vale para a Web:

- Uma Page por tela (`<Tela>Page`), recebendo o `Frame`/`FrameLocator` do `#contentFrame` (ou a `SessaoWeb`).
- Métodos com verbo e o componente (`clicaSalvar()`, `preencheQuantidade(String)`, `valorTotal()` devolvendo o `Locator` para a asserção).
- Os seletores ficam na Page, como constantes (`private static final String BOTAO_SALVAR = "[id$=':btnSalvar']";`); o teste não conhece seletor.
- A Page não faz asserção de negócio: devolve o `Locator`, e o teste decide o que esperar.

## Antes de entregar (checklist)

- [ ] Localizadores por papel, rótulo ou id do `.xhtml`; nenhum `j_idt`, posição ou XPath; nenhum `.first()` para fugir do strict mode.
- [ ] Asserções web-first (`assertThat(locator)…`); nenhum `innerText()` comparado com `assertEquals`.
- [ ] Nenhum `sleep`/`waitForTimeout`; timeout padrão intacto.
- [ ] Conferência de erro (mensagem visível, 5xx, `error.log`) depois das ações que vão ao servidor.
- [ ] Massa criada pelo teste e apagada em `@AfterEach`/`finally`.
- [ ] JavaDoc com Squash e Jira; passos e resultados esperados numerados.
- [ ] ASCII puro (acento por `\uXXXX`), ISO-8859-1, CRLF.
- [ ] Rodou duas ou três vezes seguidas e passou em todas.
