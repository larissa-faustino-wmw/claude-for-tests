# Padrões de falha do TotalUiTest

Referência para classificar falhas. Os fatos abaixo vêm do código do framework (`projetos/totaluitest`, pacote `br.com.wmw.totalcross.test.api`); se o framework mudar, confira no fonte antes de afirmar.

## Como o framework espera

- Toda espera passa por `DriverWait.until(...)`: uma thread testa a condição a cada 75 ms até dar verdadeiro ou estourar o tempo.
- O tempo limite é o `TIME_WAIT` de `src/test/resources/configTests/`: **20 s no Windows** (`configSpeed.properties`) e **30 s no Linux** (`configSpeedLinux.properties`, o do Jenkins). Uma falha de espera no Jenkins significa que a condição ficou falsa por 30 s seguidos — não é "lentidão de um segundo".
- No timeout o framework lança `DriverWaitException` envolvendo um `java.util.concurrent.TimeoutException` com a mensagem `TimeoutException : <último By>, element timeout has expired` seguida do `toString()` da condição. **É o `toString()` da condição que diz o que se esperava** — leia sempre as linhas logo abaixo do `TimeoutException`.

## Failure x Error no TotalUiTest

A regra geral (Failure = assert deu diferente; Error = não chegou ao assert) **tem uma exceção importante aqui**: o `waitValue` é, na prática, um assert de valor, mas quando o valor não bate ele termina em timeout e aparece como **Error** (`DriverWaitException`), não como Failure. Portanto:

- `AssertionFailedError` (Failure) → o teste comparou com `assertEquals`/`assertTrue` e deu diferente.
- `DriverWaitException` com `Expected : … / Actual : …` (Error) → também é divergência de valor. Trate como Failure para o diagnóstico (olhe produto ou massa), não como problema de espera.

## Catálogo de assinaturas

| Assinatura no log | O que significa | Categoria mais provável |
|---|---|---|
| `DriverWaitException: Erro ao esperar a tela <X> abrir.` | `waitOpening(<X>.class)` não viu a tela. **A causa original é descartada** pelo framework (a exceção é recriada sem `cause`), então o motivo está em outro lugar: stack trace solta logo antes, print da falha, ou passo anterior. | Depende: app quebrou (bug), clique anterior não navegou (teste), apareceu um `WmwMessageBox` no lugar da tela (massa/parâmetro ou bug), ambiente lento |
| `TimeoutException : <By>, element timeout has expired` + `Expected Condition: Checks whether the '<By>' object is different from null` | O elemento com aquele id/caminho não existe na tela atual. | Id renomeado no produto (confira `git log` do `lavenderepda`), tela diferente da esperada, ou teste esperando antes da hora |
| `TimeoutException …` + `Expected : <a>` / `Actual  : <b>` | `waitValue`: o campo nunca chegou ao valor esperado. `Actual : null` → o campo não foi achado (tela/id). `Actual` com outro valor → o app calculou/mostrou outra coisa. | Valor diferente: produto ou massa. `null`: teste ou tela errada |
| `… checks whether the result of '<By> : <classe>' is an instance of '<X>'` | Abriu outra tela (classe `<classe>`) no lugar de `<X>`. | Navegação mudou no produto, ou um diálogo inesperado ficou por cima |
| `DriverClickException: O componente de ID:<id> Não está visivel na tela.` | O componente existe, mas não está visível para o clique (fora da área, atrás de outro, scroll). | Teste (scroll/ordem dos passos) ou mudança de layout no produto |
| `DriverClickException: <texto de mensagem do app>` | O `checkInError` achou um `WmwMessageBox` do tipo **ERROR**; o texto da exceção é a mensagem que o app mostrou ao usuário. **Leia a mensagem: ela costuma dizer a causa.** | Massa/parâmetro incompleto (teste) ou regra do produto que mudou (provável bug) |
| `InvokeInitException` | Um método `@InvokeInit` falhou — a massa não foi montada e o app nem abriu. Costuma vir com `SQLException`: coluna ou tabela inexistente, constraint, sintaxe. | Teste (SQL errado) ou banco base desatualizado em relação ao app (ambiente). Coluna inexistente: a fonte da verdade é a classe de domain do `lavenderepda` |
| `org.opentest4j.AssertionFailedError: expected: <a> but was: <b>` | Failure real de `assertEquals`. | Produto ou massa |
| `DBException`, falha no `exec:exec@db`, `DatabaseManager`, banco não encontrado em `./db/<versão>/` | O banco base não foi baixado ou está incompleto/de outra versão. | Ambiente |
| `The forked VM terminated without properly saying goodbye`, `OutOfMemoryError`, `There was a timeout in the fork` | O fork do Surefire morreu. Os testes daquele fork aparecem sem resultado ou como erro. | Ambiente (memória do agente, timeout do pipeline) |
| Stack trace solta com `totalcross.*` ou `br.com.wmw.*` (fora do bloco de um teste) | Exceção no app enquanto algum teste rodava. Cruze o horário/fork com a falha seguinte. | Provável bug se o frame de topo for `br.com.wmw.*` e se repetir |

## Configuração do Surefire (pom do `totaluitest`)

Esses valores mudam como ler os totais do build — confira no `pom.xml` do branch, pois podem ser sobrescritos no Jenkins com `-D…`:

- `forkCount=${execs}` (padrão **4**), `reuseForks=false`, `parallel=classes`: até 4 JVMs rodando classes diferentes ao mesmo tempo. Linhas de testes diferentes se intercalam no console.
- `skipAfterFailureCount=1`: depois da primeira falha o Surefire **pula os testes que ainda não começaram**. Uma contagem alta de *Skipped* é consequência da primeira falha, não N problemas novos. Com vários forks o corte é aproximado — alguns testes ainda terminam.
- `rerunFailingTestsCount=0`: não há rerun por padrão, logo **não existe bloco `Flakes:`** a menos que o pipeline passe `-Dsurefire.rerunFailingTestsCount=<n>`. Sem rerun, flaky só se prova comparando builds.
- `disable.system.out=true` (padrão): o `System.out` do app é silenciado; o `System.err` (e `printStackTrace`) continua aparecendo. Para investigar localmente com a saída do app, rode com `-Ddisable.system.out=false`.
- Execução padrão: `clean test -Denv.test=<develop|release> -Duser.language.format=pt -Dfile.encoding=ISO-8859-1`. Sem esses dois últimos, datas, valores e acentos saem diferentes — falha de formatação em massa costuma ser isso.

## Evidências que o framework deixa

- **Print da tela na falha**: `dadosTest/<Classe>/imagens/<metodo>/` (gerado pelo `WatcherTotalUITest.testFailed`). Mostra a tela que estava aberta quando a espera estourou — resolve a maioria dos "Erro ao esperar a tela abrir".
- **Banco do teste**: com `downloadDatabase`, cada classe usa uma cópia em `dadosTest/<Classe>/dbs`. Em sucesso a pasta é apagada; **em falha o banco fica**. Dá para abrir o `.sqlite3` e conferir se a massa do `@InvokeInit` entrou como esperado.
- No Jenkins essas pastas só existem se o job arquivar `dadosTest/**`. Se o usuário não tiver os prints, peça para arquivar ou para rodar a classe localmente.

## Decidindo a categoria

1. Há exceção do app (`br.com.wmw.*`) no mesmo fork, segundos antes? → a falha de espera é sintoma; investigue a exceção (provável bug, ou massa que leva o app a um estado inválido).
2. A mensagem é `Expected/Actual` ou `AssertionFailedError`? → divergência de valor: compare com a massa do teste; se a massa está certa e outros testes do mesmo cálculo também falham, provável bug.
3. `DriverClickException` com mensagem do app? → leia a mensagem; quase sempre aponta parâmetro/cadastro.
4. Elemento/tela não encontrado, sem exceção do app? → veja o print; confira se id ou navegação mudaram no `lavenderepda` (`git log`); se nada mudou e o teste passa em outros builds, suspeito de flaky.
5. Fork morto, banco ausente, muitos testes sem relação falhando juntos no mesmo horário? → ambiente.
