# Refatoracao -- modulo `verba`

> Gerado por `massa.py plano`. O estado e deduzido do repositorio
> (presenca de `.sql` e de `@InvokeInit`), entao nao envelhece.
> Regenere depois de cada teste migrado. Anotacoes manuais no fim do
> arquivo sao preservadas.

| | |
|---|---|
| Classes de teste | 19 |
| Arquivos `.sql` restantes | 19 |
| Statements | 131 |
| Convertiveis automaticamente | 131 (100%) |
| Exigem decisao humana | 0 |
| Migrados / em fase A | 0 / 0 |

## Ordem sugerida

Menor esforco primeiro. `bloq` = statements que exigem decisao.

| # | Estado | Teste | stmts | auto | bloq | enc |
|---|---|---|---|---|---|---|
| 1 | NAO INICIADO | `EmitirPedidoUtilizandoVerbaFlexRepresentanteExtrapolandoSaldoTest` | 4 | 4 | 0 | ok |
| 2 | NAO INICIADO | `EmitirPedidoTresItensConsumindoVerbaRecalculandoValoresRelatorioTest` | 4 | 4 | 0 | ok |
| 3 | NAO INICIADO | `EmitirPedidoAlterandoItemMantendoDescontoAlterandoConsumoVerbaTest` | 4 | 4 | 0 | ok |
| 4 | NAO INICIADO | `EmitirPedidoUtilizandoVerbaFlexPorRepresentanteTest` | 4 | 4 | 0 | ok |
| 5 | NAO INICIADO | `EmitirPedidoVerbaFlexFornecedorExtrapolandoSaldoTest` | 6 | 6 | 0 | ok |
| 6 | NAO INICIADO | `EmitirPedidoVerbaFlexFornecedorAlterandoDescontoInseridoItemTest` | 6 | 6 | 0 | ok |
| 7 | NAO INICIADO | `EmitirPedidoUtilizandoVerbaFlexFornecedorTest` | 6 | 6 | 0 | ok |
| 8 | NAO INICIADO | `EmitirPedidoVerbaFlexClienteExtrapolandoSaldoTest` | 7 | 7 | 0 | ok |
| 9 | NAO INICIADO | `EmitirPedidoUtilizandoVerbaFlexporClienteTest` | 7 | 7 | 0 | ok |
| 10 | NAO INICIADO | `EmitirPedidoGerandoVerbaPedidoCorrenteConsumindoVerbaGeradaTest` | 7 | 7 | 0 | ok |
| 11 | NAO INICIADO | `EmitirPedidoGerandoVerbaPedidoCorrenteConsumindoVerbaGeradaParcialTest` | 7 | 7 | 0 | ok |
| 12 | NAO INICIADO | `EmitirPedidoVerbaCorrenteConsumindoVerbaExtrapolandoSaldoTest` | 7 | 7 | 0 | ok |
| 13 | NAO INICIADO | `EmitirPedidoGerandoVerbaPedidoCorrenteAcumuladaTest` | 7 | 7 | 0 | ok |
| 14 | NAO INICIADO | `EmitirPedidoGerandoVerbaPedidoCorrenteTest` | 7 | 7 | 0 | ok |
| 15 | NAO INICIADO | `EmitirPedidoBonificacaoConsumindoVerbaRepresentanteTest` | 8 | 8 | 0 | ok |
| 16 | NAO INICIADO | `EmitirPedidoUtilizandoVerbaFlexGrupoProdutoExtrapolandoSaldoTest` | 8 | 8 | 0 | ok |
| 17 | NAO INICIADO | `EmitirPedidoUtilizandoVerbaFlexPorGrupoProdutoTest` | 8 | 8 | 0 | ok |
| 18 | NAO INICIADO | `ValidarConsumoVerbaGrupoSaldoPersonalizadoTest` | 9 | 9 | 0 | !! UTF-8 |
| 19 | NAO INICIADO | `saldoZero` | 15 | 15 | 0 | ok |

## Como migrar

```
/migrar-teste <NomeDaClasseTest>   # um teste (comece pelo nº 1)
/migrar-modulo verba               # a fila inteira, um por vez
```

Regras que valem sempre: ISO-8859-1, validacao em fase A e fase B, um
teste por vez. Detalhe em `../../skills/migracao-massa-teste/SKILL.md`.

<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->

## Anotacoes

Decisoes tomadas, duvidas para o time, defeitos encontrados no `.sql`
original. Este bloco sobrevive a regeneracao.
