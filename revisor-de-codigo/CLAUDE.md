# totaluitest

Testes de interface (TotalCross) do PDA Lavendere. JUnit 5 + framework proprio
`br.com.wmw.totalcross.test`.

## ISO-8859-1 -- leia antes de editar qualquer arquivo

Todo `.java`, `.sql` e `.ddl` sob `src/` esta em **ISO-8859-1**
(`pom.xml`: `project.build.sourceEncoding`; surefire: `-Dfile.encoding=ISO-8859-1`).
400 dos 494 arquivos tem bytes que **nao sao UTF-8 valido**.

- Ler: `iconv -f ISO-8859-1 -t UTF-8 <arquivo>`. Ler direto mostra `�` no lugar
  dos acentos -- e editar sobre esse texto grava a perda no disco.
- Escrever: `encoding="iso-8859-1"`. Com `Edit`, mexa so em linhas sem acento.
- Nunca use aspas curvas, travessao ou reticencias tipograficas.
- O hook `.claude/scripts/garantir_iso8859.py` reconverte UTF-8 e bloqueia
  U+FFFD. Antes de editar, guarde `cp <arquivo> <arquivo>.orig`; se bloquear,
  restaure da copia e refaca.
- Conferir tudo: `python3 .claude/skills/migracao-massa-teste/scripts/massa.py encoding`

## Estrutura

```
src/main/java/br/com/wmw/totalcross/test/   framework de teste (driver, DSL, @InvokeInit)
src/test/java/.../presentation/ui/base/     PDATotalUITest, DatabasePrepareTestUtil,
                                            ParametrosTestUtil, TabelasTestUtil
src/test/java/.../presentation/ui/page/     Page Objects por dominio
src/test/java/.../presentation/ui/test/     casos de teste, agrupados por funcionalidade
db/<versao>/wmwvendas.sqlite3               banco base (nao versionado)
```

## Massa de dados: dois modelos

**Legado** -- `<NomeDoTeste>.sql` ao lado da classe, carregado por convencao
(`DatabasePrepareTestUtil.execSqlTestClass`). SQL fixo, nao validado, quebra
quando um parametro ou coluna muda. 208 arquivos.

**Atual** -- metodo `@InvokeInit private void prepararMassaDeDados()` na classe
de teste, usando `ParametrosTestUtil` e `TabelasTestUtil`.

Ordem de execucao em `BaseTotalUITest.invokeInit()`: o `.sql` roda primeiro
(`invokeFileSql`, `order = -1000`), depois os `@InvokeInit` da classe de teste.
Logo **o Java sobrescreve o SQL** -- os dois convivem durante a migracao.

Teste novo nasce no modelo atual. Para converter um teste legado, use
`/migrar-teste` (skill `migracao-massa-teste`). Panorama: `/auditar-massa`.

O plano de refatoracao vive em `.claude/refatoracao/`: `README.md` com o painel
geral e a ordem das ondas, e uma pasta por modulo com `STATUS.md`. Sao arquivos
gerados (`massa.py plano`) cujo estado e deduzido do repositorio -- regenere
depois de migrar cada teste. As anotacoes manuais no fim de cada arquivo
sobrevivem a regeneracao.

## Comandos

```bash
# baixar o banco base
mvn compile exec:exec@db -Denv.test=develop

# rodar tudo
mvn clean test -Denv.test=develop -Duser.language.format=pt -Dfile.encoding=ISO-8859-1

# um teste
mvn test -Dtest=NomeDoTeste -Denv.test=develop -Duser.language.format=pt -Dfile.encoding=ISO-8859-1
```

Ambientes: `develop` e `release`.

## Convencoes

- Classes de teste terminam em `Test` e levam `@PDATotalUITest`.
- Javadoc da classe referencia o caso no Squash e traz autor e versao.
- Cada passo do caso de teste vira um bloco comentado (`Passo N` /
  `Resultado Esperado N`) na ordem do roteiro.
- Toda assertiva leva mensagem descrevendo o que falhou.
- Interacao com a UI passa por Page Object; nunca manipule widget direto.
- Checkstyle: `CheckstyleTotalcrossTotalUiTest.xml`. Em blocos de massa,
  `@SuppressWarnings("checkstyle:MultipleStringLiterals")` e esperado.
