# Refatoracao -- modulo `cliente`

> Gerado por `massa.py plano`. O estado e deduzido do repositorio
> (presenca de `.sql` e de `@InvokeInit`), entao nao envelhece.
> Regenere depois de cada teste migrado. Anotacoes manuais no fim do
> arquivo sao preservadas.

| | |
|---|---|
| Classes de teste | 14 |
| Arquivos `.sql` restantes | 15 |
| Statements | 118 |
| Convertiveis automaticamente | 115 (97%) |
| Exigem decisao humana | 3 |
| Migrados / em fase A | 0 / 15 |

## Ordem sugerida

Menor esforco primeiro. `bloq` = statements que exigem decisao.

| # | Estado | Teste | stmts | auto | bloq | enc |
|---|---|---|---|---|---|---|
| 1 | FASE A | `CadastrarProspectAprovadoDuasEtapasTest` | 0 | 0 | 0 | !! UTF-8 |
| 2 | FASE A | `CadastrarProspectAprovadoDuasEtapasTest_Retorno` | 0 | 0 | 0 | ok |
| 3 | FASE A | `ExcluirCadastroNovoClienteTest` | 0 | 0 | 0 | ok |
| 4 | FASE A | `CadastrarNovoClienteTest` | 0 | 0 | 0 | ok |
| 5 | FASE A | `BuscarDadosPorCNPJNovoClienteTest` | 0 | 0 | 0 | ok |
| 6 | FASE A | `CadastrarNovoClienteComCamposDinamicosTest` | 0 | 0 | 0 | ok |
| 7 | FASE A | `ValidarListagemDeNovosClientesExclusaoDeRegistrosTest` | 0 | 0 | 0 | ok |
| 8 | FASE A | `ValidarCadastroMultiplosEnderecosClienteTest` | 17 | 17 | 0 | ok |
| 9 | FASE A | `ValidarEnderecoEntregaClientePedidoTest` | 19 | 19 | 0 | ok |
| 10 | FASE A | `ValidarCadastroEAtualizacaoDeContatosDoClienteTest` | 21 | 21 | 0 | !! UTF-8 |
| 11 | FASE A | `ValidarAtualizacaoEnderecosClienteComSupervisorTest` | 27 | 27 | 0 | ok |
| 12 | FASE A | `ValidarAtualizacaoClienteTest` | 30 | 30 | 0 | !! UTF-8 |
| 13 | FASE A | `CadastrarMultiplosEnderecosNovosClienteTest` | 1 | 0 | 1 | ok |
| 14 | FASE A | `ValidarQuantidadeMinimaEnderecosCadastroNovosClientesTest` | 1 | 0 | 1 | ok |
| 15 | FASE A | `BuscarEnderecoPorCEPNoCadastroDeNovoClienteTest` | 2 | 1 | 1 | !! UTF-8 |

## Bloqueios por causa raiz

| Causa | Qtd | Resolvivel na util? |
|---|---|---|
| DDL -- permanece no .sql (correto) | 2 | nao |
| analise caso a caso | 1 | nao |

<details><summary>Detalhe dos bloqueios</summary>

- **2x** DDL nao pertence a massa de dados. Manter em .ddl/.sql ou DatabasePrepareTestUtil.executeUpdate(...).
- **1x** Nao foi possivel identificar o CDPARAMETRO no WHERE

</details>

## Como migrar

```
/migrar-teste <NomeDaClasseTest>   # um teste (comece pelo nº 1)
/migrar-modulo cliente             # a fila inteira, um por vez
```

Regras que valem sempre: ISO-8859-1, validacao em fase A e fase B, um
teste por vez. Detalhe em `../../skills/migracao-massa-teste/SKILL.md`.

<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->

## Anotacoes

Decisoes tomadas, duvidas para o time, defeitos encontrados no `.sql`
original. Este bloco sobrevive a regeneracao.

### 2026-08-06 -- migracao do modulo inteiro (fases A e B NAO executadas)

Os 15 `.sql` do modulo foram processados, um por vez, via subagente
`migrador-massa`. **Maven nao existe nesta maquina (`mvn not found`) e `db/`
esta vazio: nenhuma das duas fases rodou.** O codigo esta migrado e revisado,
mas nao executado. **Ninguem apague `.sql` algum antes da fase B.**

**Quatro `.sql` NAO podem ser apagados nunca -- eles guardam DDL.** Foram
reduzidos so ao `ALTER TABLE`, com cabecalho comentado explicando, e a classe
correspondente tem `// TODO MIGRACAO`. Sao eles:
`ExcluirCadastroNovoClienteTest`, `CadastrarMultiplosEnderecosNovosClienteTest`,
`ValidarQuantidadeMinimaEnderecosCadastroNovosClientesTest` (1 ALTER cada, a
coluna `AD_CONTATOCLIENTE`) e `CadastrarNovoClienteComCamposDinamicosTest`
(10 ALTER). Para esses quatro, a fase B se limita a confirmar que o teste passa
com o `.sql` ja reduzido -- renomear para `.bak` faz a coluna sumir e o teste
quebra por motivo alheio a migracao.

**O plano superestimava os bloqueios.** Dos 16 statements marcados como
"exigem decisao humana", 13 eram DDL de verdade e 3 eram
`CDPARAMETRO IN ('941','389')` -- que nao e bloqueio, e uma chamada
`setParametro` por codigo. Ocorreu em `BuscarEnderecoPorCEPNoCadastroDeNovoClienteTest`,
`ValidarListagemDeNovosClientesExclusaoDeRegistrosTest` e
`BuscarDadosPorCNPJNovoClienteTest`, os tres migrados por completo. Vale
ensinar o padrao ao `massa.py` em vez de continuar caindo nele.

**`_Retorno.sql` confirmou o precedente de autorizacaoNegociacao:** vai para o
corpo do teste, nunca para `prepararMassaDeDados()`. Detalhe na anotacao
especifica de `CadastrarProspectAprovadoDuasEtapasTest`, abaixo.

**Defeito real encontrado -- os dois `.sql` em UTF-8 gravavam mojibake no
banco.** `DatabasePrepareTestUtil.execAbsoluteFileSQL` le o arquivo com
`new String(Files.readAllBytes(path))`, ou seja, o charset default da JVM, que
o surefire fixa em ISO-8859-1. Em `ValidarCadastroEAtualizacaoDeContatosDoClienteTest`
e `ValidarAtualizacaoClienteTest` os bytes UTF-8 dos acentos eram lidos um a
um como ISO-8859-1 e entravam no banco duplicados (o classico mojibake: "Tubarao"
com til virando dois caracteres, e assim em `DSCIDADE`, `DSBAIRRO` e tres
`DSLABEL` de `TBLVPCAMPO`). A migracao
corrige (os valores passam a entrar acentuados corretamente) -- **isso e
mudanca de comportamento real**, ainda que nenhum desses valores seja lido por
assertiva nos dois testes. Os outros dois `.sql` UTF-8 do projeto
(`estoque` e `verba/grupoProduto`) continuam com o mesmo defeito latente.

**Mudanca de comportamento que vale para quase todo o modulo:** os parametros
JSON (27, 280, 1049, 1054, 1056, 1371, 1463, 1828) passaram de substituicao do
objeto inteiro para patch chave a chave (`json_set`). Todas as chaves que cada
`.sql` declarava foram declaradas explicitamente, entao o cenario pretendido e
identico; a diferenca e que chaves extras vindas do banco base agora sobrevivem
em vez de sumir. Alem disso `ParametrosTestUtil` filtra so por `CDPARAMETRO`,
enquanto varios `.sql` filtravam tambem por `NMENTIDADE = 'TBWMWSISTEMA'` e
`VLCHAVE = '[1]'`: se houver mais de uma linha para o mesmo parametro no banco
base, todas passam a ser atualizadas.

**Sujeira herdada, reportada e NAO corrigida:** varios `.sql` usam aspas duplas
em literal de WHERE (`CDCLIENTE = "1"`, `CDUSUARIO = "WMWROBOT"`). So funciona
pelo fallback do SQLite de "identificador inexistente vira string" e quebraria
com `SQLITE_DQS` desligado. Preservado como estava em todos os testes, exceto
em `ValidarCadastroEAtualizacaoDeContatosDoClienteTest`, onde virou aspas
simples -- equivalente em SQLite, mas e uma divergencia entre os arquivos.

**Pendencias para o time:**

- `CadastrarProspectAprovadoDuasEtapasTest`: `CDNOVOCLIENTE` divergente entre
  `TBLVPNOVOCLIENTE` ('3') e `TBLVPNOVOCLIENTEANA` ('461613026'). Confirmar com
  quem conhece o CT-LVP de prospect em duas etapas.
- `ValidarAtualizacaoClienteTest` esta em pasta duplicada
  (`cliente/atualizacao/ValidarAtualizacaoClienteTest/ValidarAtualizacaoClienteTest/`),
  com o package acompanhando a duplicacao. Compila e o `.sql` e achado por
  convencao, mas foge do padrao dos vizinhos. Corrigir exige renomear package e
  mover arquivos -- fora do escopo da massa.

### 2026-08-06 -- CadastrarProspectAprovadoDuasEtapasTest (fases A e B NAO executadas)

Maven indisponivel neste ambiente; validacao delegada ao lote. **Nao apagar os
dois `.sql` antes da fase B.**

Dois arquivos migrados na mesma passada:

- `CadastrarProspectAprovadoDuasEtapasTest.sql` (12 statements) ->
  `prepararMassaDeDados()`, primeiro metodo da classe.
- `CadastrarProspectAprovadoDuasEtapasTest_Retorno.sql` (3 inserts) -> corpo do
  teste, no passo 7, no lugar de `DatabasePrepareTestUtil.execSqlRetornoWeb`,
  seguindo o precedente do modulo autorizacaoNegociacao. Os inserts so podem
  rodar depois que o prospect e criado pela UI no passo 3.

Ajustes no `.java` fora da massa, todos consequencia direta da troca do passo 7:
assinatura de `deveTestarProspectAprovadoDuasEtapas()` passou de
`throws SQLException` para `throws Exception` (`TabelasTestUtil.insert` declara
`Exception`), e os imports de `DatabasePrepareTestUtil` e `java.sql.SQLException`
sairam por terem ficado sem uso. Nenhum passo, assertiva ou Page Object mudou.

**Parametros 27 e 1828:** substituicao total do JSON virou patch chave a chave.
Todas as chaves do `.sql` foram declaradas; so difere se o banco base trouxer
chave extra, que agora sobrevive em vez de sumir. O 1371 nao e JSON e seguiu
como update simples.

**`DATE('now','localtime')`** em `TBLVPRELNOVIDADENOVOCLI.DTGERACAO` virou
`DatasTestUtil.hoje()`.

**Defeito no `_Retorno.sql` original (ja reportado, NAO corrigido):**
`CDNOVOCLIENTE` diverge entre `TBLVPNOVOCLIENTE` ('3') e `TBLVPNOVOCLIENTEANA`
('461613026'). A analise aprovada nao referencia o novo cliente inserido. A
migracao reproduz os dois valores como estao.

**Suspeita menor, tambem nao corrigida:** no `.sql` de preparacao, o segundo
`TBLVPCAMPO` tem `NMENTIDADE = 'TBLVWPROSPECT'` mas `rowkey =
'1;TBLVWNOVOCLIENTE;NUFONE;'`. Reproduzido fielmente.

**Risco conhecido na fase A:** com os `.sql` no lugar, os inserts de
`TBLVPAUTORIZACAO`, `TBLVPCAMPO`, `TBLVPSTATUSANALISECLIENTE`,
`TBLVPTIPOANALISECLIENTE` e os tres do retorno rodam duas vezes. Se houver
unique/PK em `rowkey`, o segundo estoura `InvokeInitException` -- artefato da
convivencia SQL+Java, nao erro da migracao. Nesse caso va direto para a fase B.
