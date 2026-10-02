# Refatoracao -- modulo `estoque`

> Gerado por `massa.py plano`. O estado e deduzido do repositorio
> (presenca de `.sql` e de `@InvokeInit`), entao nao envelhece.
> Regenere depois de cada teste migrado. Anotacoes manuais no fim do
> arquivo sao preservadas.

| | |
|---|---|
| Classes de teste | 36 |
| Arquivos `.sql` restantes | 35 |
| Statements | 342 |
| Convertiveis automaticamente | 339 (99%) |
| Exigem decisao humana | 3 |
| Migrados / em fase A | 0 / 35 |

## Ordem sugerida

Menor esforco primeiro. `bloq` = statements que exigem decisao.

| # | Estado | Teste | stmts | auto | bloq | enc |
|---|---|---|---|---|---|---|
| 1 | FASE A | `ValidarBloqueioReservaCorrenteSemEstoquePrevistoTest` | 1 | 1 | 0 | ok |
| 2 | FASE A | `ValidarBloqueioProdutoSemEstoqueListaItensRegistroProdutoFaltaTest` | 7 | 7 | 0 | ok |
| 3 | FASE A | `ValidarRecalculoManualEstoqueNoMenuProdutoTest` | 7 | 7 | 0 | ok |
| 4 | FASE A | `ValidarPopUpApenasComRegistroFaltaEstoqueTest` | 8 | 8 | 0 | ok |
| 5 | FASE A | `ValidarRegistroFaltaPopUpNaoCarregaNenhumaOpcaoPadraoTest` | 8 | 8 | 0 | ok |
| 6 | FASE A | `ValidarProdutoFaltaQuandoIgnoraControleEstoqueTipoPedidoTest` | 8 | 8 | 0 | ok |
| 7 | FASE A | `ValidarRegistroProdutoFaltaComAjusteDeQuantidadeDeVendaTest` | 8 | 8 | 0 | ok |
| 8 | FASE A | `ValidarMensagemParaRegistroProdutoFaltaTest` | 8 | 8 | 0 | ok |
| 9 | FASE A | `ValidarPopUpRegistroFaltaAjusteQuantidadeDisponivelRegistroFaltaTest` | 8 | 8 | 0 | ok |
| 10 | FASE A | `ValidarRecalculoManualEstoqueAdicionarItemPedidoTest` | 8 | 8 | 0 | ok |
| 11 | FASE A | `ValidarBloqueioProdutoEstoquePedidoNormalTest` | 8 | 8 | 0 | ok |
| 12 | FASE A | `ValidarVendaItemSemEstoqueTest` | 8 | 8 | 0 | ok |
| 13 | FASE A | `ValidarEstoquePedidoInsercaoExclusaoDeItensTest` | 8 | 8 | 0 | !! UTF-8 |
| 14 | FASE A | `ValidarBloqueioVendaProdutoSemEstoqueEDestaqueCorTest` | 8 | 8 | 0 | ok |
| 15 | FASE A | `EmitirAvisoFaltaAdicionarProdutoSemEstoqueComRegistroProdutoFaltaTest` | 9 | 9 | 0 | ok |
| 16 | FASE A | `ValidacaoBloqueioFechamentoPedidoProdutoSemEstoqueTest` | 9 | 9 | 0 | ok |
| 17 | FASE A | `ValidarAvisoVendaItemSemEstoquePrevistoTest` | 9 | 9 | 0 | ok |
| 18 | FASE A | `EmitirPedidoValidandoEstoqueMaximoLoteProdudoTest` | 9 | 9 | 0 | ok |
| 19 | FASE A | `ExcluirItemPedidoComLoteDeEstoqueTest` | 9 | 9 | 0 | ok |
| 20 | FASE A | `EmitirPedidoProdutoComLoteEstoqueTest` | 9 | 9 | 0 | ok |
| 21 | FASE A | `ValidarAvisoVendaItemSemEstoqueTest` | 10 | 10 | 0 | ok |
| 22 | FASE A | `ValidarBloqueioFechamentoPedidoProdutoSemEstoqueComAvisoTest` | 11 | 11 | 0 | ok |
| 23 | FASE A | `ValidarBloqueioFechamentoPedidoComProdutoSemEstoquePevistoTest` | 11 | 11 | 0 | ok |
| 24 | FASE A | `ValidarLiberacaoVendaItemSemEstoqueComSenhaTest` | 11 | 11 | 0 | ok |
| 25 | FASE A | `ValidarAvisoProdutoSemEstoqueListaItensRegistroFaltaUnidadeAltTest` | 12 | 12 | 0 | ok |
| 26 | FASE A | `ValidarVendaItemSemEstoqueMensagemEstoqueInsuficienteTest` | 12 | 12 | 0 | ok |
| 27 | FASE A | `ValidarVendaItemSemEstoqueMensagemDetalhesEstoquePrevistoTest` | 12 | 12 | 0 | ok |
| 28 | FASE A | `ValidarRegistroFaltaMesmoProdutoUnidadeAlternativaDiferentePedidoTest` | 13 | 13 | 0 | ok |
| 29 | FASE A | `ValidarBloqueioFechamentoPedidoProdutoSemEstoqueRevalidacaoTipoPedidoTest` | 13 | 13 | 0 | ok |
| 30 | FASE A | `ValidarEmissaoPedidoInclusaoProdutoFaltaUnidadeDiferenteTest` | 14 | 14 | 0 | ok |
| 31 | FASE A | `ValidarPedidoComProdutoSemEstoqueTest` | 16 | 16 | 0 | ok |
| 32 | FASE A | `ValidarBloqueioFechamentoPedidoComProdutoSemEstoqueLocalEstoqueTest` | 18 | 18 | 0 | ok |
| 33 | FASE A | `ValidarBonificacaoReplicacaoEstoqueInsuficienteTest` | 6 | 5 | 1 | ok |
| 34 | FASE A | `ValidarItemBonificadoDentroLimiteEstoqueTest` | 7 | 6 | 1 | ok |
| 35 | FASE A | `ValidarBloqueioProdutoSemEstoqueUnidadeAlternativaGridFaltaTest` | 19 | 18 | 1 | ok |

## Bloqueios por causa raiz

| Causa | Qtd | Resolvivel na util? |
|---|---|---|
| delete() em TabelasTestUtil | 2 | sim |
| analise caso a caso | 1 | nao |

**2 dos 3 bloqueios deste modulo somem** com as melhorias em
`../../skills/migracao-massa-teste/referencias/proposta-melhorias-utils.md`.
Considere resolver a util antes de migrar este modulo -- e uma
mudanca contra 2 ocorrencias.

<details><summary>Detalhe dos bloqueios</summary>

- **2x** DELETE nao tem equivalente em TabelasTestUtil. Use DatabasePrepareTestUtil.executeUpdate(...) ou crie TabelasTestUtil.delete().
- **1x** UPDATE em TBLVPVALORPARAMETRO altera colunas alem de VLPARAMETRO -- converter a mao.

</details>

## Como migrar

```
/migrar-teste <NomeDaClasseTest>   # um teste (comece pelo nº 1)
/migrar-modulo estoque             # a fila inteira, um por vez
```

Regras que valem sempre: ISO-8859-1, validacao em fase A e fase B, um
teste por vez. Detalhe em `../../skills/migracao-massa-teste/SKILL.md`.

<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->

## Anotacoes

Decisoes tomadas, duvidas para o time, defeitos encontrados no `.sql`
original. Este bloco sobrevive a regeneracao.

### 2026-08-07 -- migracao do modulo (35 testes, `/migrar-modulo`)

Os 35 `.sql` do modulo foram migrados para `@InvokeInit prepararMassaDeDados()`.
340 dos 342 statements convertidos; 2 ficaram pendentes de decisao humana (ver
abaixo). Os `.sql` continuam no lugar -- a fase B ainda nao pode ser feita.

**Onda 0 executada antes de migrar.** `TabelasTestUtil` ganhou
`executeDelete()` (builder) e `delete(String tabela, String where)` (estatico,
delegando ao builder), seguindo o par `executeX()`/`X()` que a classe ja usava.
Isso zerou os 2 bloqueios de DELETE do modulo -- usados em
`ValidarBonificacaoReplicacaoEstoqueInsuficienteTest` e
`ValidarItemBonificadoDentroLimiteEstoqueTest`. Decisao do usuario, tomada antes
da fila comecar.

**Validacao nao executada.** `db/` esta vazio (so `.donotdelete`), sem banco base
nao ha como rodar o Maven. Fases A e B pendentes de execucao humana:

```
mvn compile exec:exec@db -Denv.test=develop
mvn test -Dtest='Validar*Estoque*+Emitir*Estoque*+...' -Denv.test=develop -Duser.language.format=pt -Dfile.encoding=ISO-8859-1
```
Atencao a "Flakes" na saida (`rerunFailingTestsCount=3`): flake conta como falha.

**Ponto estrutural para a fase A.** `TabelasTestUtil.executeInsert()` emite
`INSERT` puro, sem `OR REPLACE`. Enquanto o `.sql` estiver no lugar, cada INSERT
roda duas vezes (SQL e depois Java). Se `TBLVPESTOQUE` tiver PK/unique em
`rowkey`, varios testes vao falhar na fase A por constraint sem que a massa
esteja errada -- a fase B e o sinal confiavel. Nao foi possivel conferir o
schema: nao ha `.ddl` no repositorio nem banco em `db/`.

**Defeitos encontrados nos `.sql` originais (reportados, nao corrigidos)**

1. `ValidarBloqueioProdutoSemEstoqueUnidadeAlternativaGridFaltaTest` -- statement
   do parametro 220 **corrompido**: o trecho `EMA=1 AN` foi deslocado de
   `CDSISTEMA=1 AND` (WHERE) para dentro de `VLPARAMETRO` (SET), produzindo
   `SET VLPARAMEEMA=1 ANTRO=...` e `WHERE CDSISTD CDPARAMETRO=220`. Statement
   invalido: o parametro 220 nunca foi aplicado neste teste, e as assertivas de
   grade dos passos 4/5/9 foram calibradas contra o valor do banco base. Era o
   unico bloqueio do modulo que nao sumia com mudanca de util -- e o "UPDATE
   altera colunas alem de VLPARAMETRO" do plano e exatamente este defeito.
2. `ValidarBonificacaoReplicacaoEstoqueInsuficienteTest` -- o `.sql` ao lado da
   classe **nao e a massa desta classe**. Foi renomeado no commit `167a95a7`
   (`ValidacaoReplicacaoBonificacaoComEstoqueInsuficienteTest.sql` ->
   `ValidarBonificacaoReplicacaoEstoqueInsuficienteTest.sql`) e passou a ser
   carregado por convencao. Configura estoque do produto 4; o teste exercita o
   produto 10. Grava `permiteBonificarApenasProdutosInseridosNoPedido = "N"` no
   parametro 413, contradizendo o `"S"` da massa Java -- hoje o teste so passa
   porque o Java roda depois e sobrescreve. A massa legitima era
   `ct032/t041/ValidacaoBonificacaoReplicacaoEstoqueInsuficienteTest.sql`,
   apagada em `3bb53428`.
3. `ValidarBloqueioFechamentoPedidoProdutoSemEstoqueRevalidacaoTipoPedidoTest` --
   parametro 87 gravado como valor simples `'S'` sobre coluna que hoje e JSON,
   destruindo o objeto. Os testes vizinhos gravam o objeto completo.
4. **TAB literal antes do `{`** no valor do parametro 87, em 7 arquivos
   (`ValidacaoBloqueioFechamentoPedidoProdutoSemEstoque`,
   `ValidarAvisoVendaItemSemEstoquePrevisto`,
   `ValidarBloqueioFechamentoPedidoProdutoSemEstoqueComAviso`,
   `ValidarBloqueioFechamentoPedidoComProdutoSemEstoquePevisto`,
   `ValidarLiberacaoVendaItemSemEstoqueComSenha`,
   `ValidarVendaItemSemEstoqueMensagemDetalhesEstoquePrevisto`,
   `ValidarBloqueioFechamentoPedidoComProdutoSemEstoqueLocalEstoque`). O valor
   gravado nao comeca com `{`, entao nunca casou com o `LIKE '{%'` de
   `patchJsonDb` -- na pratica o parametro nunca foi JSON valido nesses testes.
   **Consequencia para a ferramenta:** com o TAB, `massa.py` classifica o
   statement como valor simples e gera `setParametro(87, "usa", "<json
   inteiro>")`, que gravaria o objeto dentro da chave `usa`. Essa saida foi
   descartada e as chaves escritas a mao nos 7 casos. Vale corrigir o gerador.
5. `ValidarPedidoComProdutoSemEstoqueTest` -- os dois INSERT em
   `TBLVPVERBASALDO` usam a mesma rowkey `1;0;0;E;`: o primeiro grava saldo 3000,
   o segundo ("cenario 1.4") grava 100. Ou o segundo falha por chave duplicada,
   ou existem duas linhas concorrentes.
6. Recorrentes, cosmeticos: `TBLVPESTOQUE` com `CDLOCALESTOQUE = '1'` e rowkey
   trazendo `0` nessa posicao (aparece em quase todo o modulo); `QTESTOQUE`
   escrito como `.0000000` sem zero a esquerda, e como `0000000` inteiro em um
   caso; massa morta que nenhum passo exercita (produto 3 em
   `ValidarAvisoVendaItemSemEstoque`, produto 4 em
   `ValidarRegistroFaltaMesmoProdutoUnidadeAlternativaDiferentePedido`).

**Mudancas de comportamento aceitas**

- Parametros JSON (43, 80, 87, 238, 413, 804, 957, 970, 1642, 1891) passaram de
  substituicao do objeto inteiro para patch por chave (`json_set`). Todas as
  chaves que o `.sql` declarava seguem declaradas; chaves extras do banco base
  deixam de ser removidas. Nos 7 casos do TAB isso tem efeito colateral
  positivo: o valor gravado passa a ser JSON valido de fato.
- `ParametrosTestUtil` filtra so por `CDPARAMETRO`, entao os filtros
  `CDSISTEMA=1`, `NMENTIDADE='TBWMWSISTEMA'` e `VLCHAVE='[1]'` deixaram de
  existir. Atinge 38, 43, 79, 80, 87, 220, 238, 254, 409, 413, 535, 608, 721,
  800, 804, 957, 970, 1063, 1064, 1284, 1642, 1669, 1736, 1756, 1891.
- Datas `DATE('now', ...)` viraram `DatasTestUtil.hoje()` / `hojeMais(2)`. Em
  `EmitirPedidoProdutoComLoteEstoqueTest` as datas fixas de 2021 foram mantidas
  de proposito: a assertiva le `"23/04/2021"` literal.

**Pendencias que precisam de decisao humana**

- **Parametro 220 do `ValidarBloqueioProdutoSemEstoqueUnidadeAlternativaGridFaltaTest`**
  (CT-LVP-25-12, autor Lucas Rosa): deveria valer `'1;3;168;11;6;7;4;41;13;'`?
  Se sim, e correcao de caso de teste com reavaliacao das assertivas de grade,
  em commit proprio -- nao migracao de massa. Nao convertido; `// TODO MIGRACAO`
  no codigo com o SQL original citado.
- **`.sql` do `ValidarBonificacaoReplicacaoEstoqueInsuficienteTest`**
  (CT032-T041, autora Larissa): o arquivo renomeado deve ser apagado (hipotese
  mais provavel, ja que a massa correta esta em Java) ou o produto 4 faz parte
  do cenario? Ate isso ser respondido a fase B nao pode concluir a remocao do
  arquivo com seguranca. Os 2 statements do produto 4 nao foram migrados.
- **Parametro 1891 do `ValidarBloqueioReservaCorrenteSemEstoquePrevistoTest`**
  (CT-LVP-25-36, autor Guilherme Frasson): o JSON do `.sql` esta malformado
  (`;` no lugar de `,` apos `"usa":"2"`), o que faz `json_set` abortar com
  "malformed JSON". Com o `.sql` presente, a fase A tende a falhar de forma
  determinista -- nao e regressao da migracao. Confirmar se as 7 chaves valem no
  cenario: se o teste passava justamente porque o JSON invalido era descartado,
  a massa corrigida muda o resultado.
- **Parametro 87 do
  `ValidarBloqueioFechamentoPedidoProdutoSemEstoqueRevalidacaoTipoPedidoTest`**
  (CT-LVP-25-28): fica so com `"usa":"S"` (fiel ao `.sql`) ou tambem com
  `"ocultaRecalculaEstoque":"N"`, como os vizinhos? `// REVISAR` no codigo.

**Fora do escopo, registrado durante o lote.** 28 arquivos `.sql` de outros
modulos (agenda 9, cliente 8, descontoAcrescimo 8, autorizacaoNegociacao 2,
boleto 1) aparecem modificados na arvore: todos tiveram statements comentados
com `/* */` e 17 perderam os acentos no processo (`-- Parametros` virou
`-- Par<U+FFFD>metros`). Nao foi feito por esta migracao -- os migradores so
editam `.java`. Bytes originais no commit `93851304`. O usuario optou por deixar
como esta e tratar depois.
