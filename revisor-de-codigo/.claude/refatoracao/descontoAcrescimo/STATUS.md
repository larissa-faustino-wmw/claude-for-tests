# Refatoracao -- modulo `descontoAcrescimo`

> Gerado por `massa.py plano`. O estado e deduzido do repositorio
> (presenca de `.sql` e de `@InvokeInit`), entao nao envelhece.
> Regenere depois de cada teste migrado. Anotacoes manuais no fim do
> arquivo sao preservadas.

| | |
|---|---|
| Classes de teste | 10 |
| Arquivos `.sql` restantes | 8 |
| Statements | 36 |
| Convertiveis automaticamente | 36 (100%) |
| Exigem decisao humana | 0 |
| Migrados / em fase A | 0 / 8 |

## Ordem sugerida

Menor esforco primeiro. `bloq` = statements que exigem decisao.

| # | Estado | Teste | stmts | auto | bloq | enc |
|---|---|---|---|---|---|---|
| 1 | FASE A | `ValidarAdicaoDescontoManualItemDescontoQuantidadeAplicadoTest` | 0 | 0 | 0 | !! UTF-8 |
| 2 | FASE A | `EmitirPedidoDescontoPromocionalValorTest` | 0 | 0 | 0 | !! UTF-8 |
| 3 | FASE A | `EmitirPedidoDescontoQuantidadePromocionalIgnorandoDescontoTest` | 0 | 0 | 0 | !! UTF-8 |
| 4 | FASE A | `EmitirPedidoDescontoPromocionalPercentualTest` | 0 | 0 | 0 | !! UTF-8 |
| 5 | FASE A | `EmitirPedidoDescontoQuantidadePromocionalTest` | 0 | 0 | 0 | !! UTF-8 |
| 6 | FASE A | `ValidarPedidoVendaExtrapolandoDescontoMaximoTest` | 0 | 0 | 0 | !! UTF-8 |
| 7 | FASE A | `EmitirPedidoDescontoQuantidadeUnidadeAlternativaTest` | 17 | 17 | 0 | !! UTF-8 |
| 8 | FASE A | `EmitirPedidoDescontoQuantidadeAgrupadorSimilaridadeTest` | 19 | 19 | 0 | ok |

## Como migrar

```
/migrar-teste <NomeDaClasseTest>   # um teste (comece pelo nº 1)
/migrar-modulo descontoAcrescimo   # a fila inteira, um por vez
```

Regras que valem sempre: ISO-8859-1, validacao em fase A e fase B, um
teste por vez. Detalhe em `../../skills/migracao-massa-teste/SKILL.md`.

<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->

## Anotacoes

Decisoes tomadas, duvidas para o time, defeitos encontrados no `.sql`
original. Este bloco sobrevive a regeneracao.

### 2026-08-06 -- migracao do modulo (8 testes, `/migrar-modulo`)

Os 8 `.sql` do modulo foram migrados para `@InvokeInit prepararMassaDeDados()`,
116 statements, nenhum bloqueio. Os `.sql` continuam no lugar: a fase B ainda
nao pode ser feita.

**Validacao nao executada.** `db/` esta vazio (so `.donotdelete`), sem banco
base nao ha como rodar o Maven. Fase A e fase B ficam pendentes de execucao
humana:

```
mvn compile exec:exec@db -Denv.test=develop
# FASE A -- com os .sql no lugar
mvn test -Dtest=EmitirPedidoDescontoPromocionalValorTest+EmitirPedidoDescontoPromocionalPercentualTest+EmitirPedidoDescontoQuantidadePromocionalIgnorandoDescontoTest+EmitirPedidoDescontoQuantidadePromocionalTest+ValidarPedidoVendaExtrapolandoDescontoMaximoTest+ValidarAdicaoDescontoManualItemDescontoQuantidadeAplicadoTest+EmitirPedidoDescontoQuantidadeAgrupadorSimilaridadeTest+EmitirPedidoDescontoQuantidadeUnidadeAlternativaTest -Denv.test=develop -Duser.language.format=pt -Dfile.encoding=ISO-8859-1
# FASE B -- renomear cada .sql para .sql.bak e repetir
```
Atencao a "Flakes" na saida (`rerunFailingTestsCount=3`): flake conta como
falha aqui.

**Mudancas de comportamento aceitas em todo o modulo**

1. Parametros JSON (43, 80, 428, 908, 970, 1012) passaram de substituicao do
   objeto inteiro para patch por chave (`json_set`). Todas as chaves que o
   `.sql` declarava seguem declaradas; chaves extras do banco base deixam de
   ser removidas. Todos ja constam do whitelist `PARAMETROS_JSON`.
2. Os `UPDATE` de parametro filtravam tambem `NMENTIDADE='TBWMWSISTEMA'` e
   `VLCHAVE='[1]'` (as vezes `CDSISTEMA=1`); `ParametrosTestUtil` filtra so por
   `CDPARAMETRO`. Se houver mais de uma linha do parametro no banco base, todas
   passam a ser atualizadas. Atinge 38, 43, 79, 80, 220, 254, 428, 608, 721,
   776, 970, 1284, 1756.
3. `DATE('now','localtime')` / `DATE('now','+2 day','localtime')` viraram
   `DatasTestUtil.hoje()` / `hojeMais(2)`.

**Defeitos encontrados nos `.sql` originais (reportados, nao corrigidos)**

- `EmitirPedidoDescontoQuantidadePromocionalTest`: primeira linha de
  `TBLVPDESCPROMOCIONAL` tem `QTITEM = 3` mas rowkey com a posicao da
  quantidade zerada; as demais linhas sao coerentes.
- `EmitirPedidoDescontoQuantidadeAgrupadorSimilaridadeTest` e
  `EmitirPedidoDescontoQuantidadeUnidadeAlternativaTest`: as faixas de
  `TBLVPDESCQUANTIDADE` da tabela de preco 2 / produto 10 terminam o rowkey em
  `;8` e `;10` para `QTITEM` 10 e 25 -- fora do padrao das outras oito. No
  segundo teste as assertivas do passo 9 comparam esses rowkeys literalmente,
  entao corrigir exige mexer no caso de teste.
- `ValidarPedidoVendaExtrapolandoDescontoMaximoTest`: `UPDATE` de
  `TBLVPPRODUTO` repete `CDTRIBUTACAOPRODUTO` e `FLUTILIZAVERBA` com o mesmo
  valor (colapsa no `LinkedHashMap` de `TabelasTestUtil`, sem efeito); `UPDATE`
  sem `WHERE` em `TBLVPITEMTABELAPRECO` mantido sem `WHERE`.
- Varios testes: `TBLVPESTOQUE` grava `CDLOCALESTOQUE = '1'` com rowkey
  trazendo `0` nessa posicao. `ValidarAdicaoDescontoManualItemDescontoQuantidadeAplicadoTest`
  tem um bloco `ALTER TABLE` inteiramente comentado (codigo morto, nao migrado).
- `EmitirPedidoDescontoQuantidadeUnidadeAlternativaTest`: parametro 608
  configurado duas vezes com o mesmo valor. Duplicata reproduzida.

**Pendencias para decisao humana** (nao bloqueiam o merge da massa)

- Confirmar com quem mantem os casos se o escopo `NMENTIDADE`/`VLCHAVE` dos
  `UPDATE` de parametro e mesmo irrelevante neste banco base (item 2 acima).
- Decidir se os rowkeys fora de padrao das faixas do produto 10 devem ser
  corrigidos -- no `EmitirPedidoDescontoQuantidadeUnidadeAlternativaTest` isso
  implica alterar as assertivas, entao seria outro ticket.
