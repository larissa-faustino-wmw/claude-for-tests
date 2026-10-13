# Refatoracao -- modulo `sugestao`

> Gerado por `massa.py plano`. O estado e deduzido do repositorio
> (presenca de `.sql` e de `@InvokeInit`), entao nao envelhece.
> Regenere depois de cada teste migrado. Anotacoes manuais no fim do
> arquivo sao preservadas.

| | |
|---|---|
| Classes de teste | 9 |
| Arquivos `.sql` restantes | 10 |
| Statements | 105 |
| Convertiveis automaticamente | 105 (100%) |
| Exigem decisao humana | 0 |
| Migrados / em fase A | 0 / 0 |

## Ordem sugerida

Menor esforco primeiro. `bloq` = statements que exigem decisao.

| # | Estado | Teste | stmts | auto | bloq | enc |
|---|---|---|---|---|---|---|
| 1 | NAO INICIADO | `EmitirPedidoComProdutoCriticoAutorizarWebTest_Retorno` | 1 | 1 | 0 | ok |
| 2 | NAO INICIADO | `EmitirPedidoComKitAbertoTest` | 9 | 9 | 0 | ok |
| 3 | NAO INICIADO | `EmitirPedidoKitFechadoTest` | 9 | 9 | 0 | ok |
| 4 | NAO INICIADO | `EmitirPedidoKitFechadoTresQuantidadeValoresDefinidosTest` | 10 | 10 | 0 | ok |
| 5 | NAO INICIADO | `ExcluirItemKitInseridoPedidoTest` | 10 | 10 | 0 | ok |
| 6 | NAO INICIADO | `EmitirPedidoKitFechadoTresQuantidadeValoresDefinidosClienteTest` | 11 | 11 | 0 | ok |
| 7 | NAO INICIADO | `EmitirPedidoSemProdutoCriticoTest` | 13 | 13 | 0 | ok |
| 8 | NAO INICIADO | `EmitirPedidoComProdutoCriticoAutorizarWebTest` | 13 | 13 | 0 | ok |
| 9 | NAO INICIADO | `EmitirPedidoKitFechadoTresQuantidadeValoresDefinidosTest` | 13 | 13 | 0 | ok |
| 10 | NAO INICIADO | `EmitirPedidoKitFechadoUnidadeAlternativaTest` | 16 | 16 | 0 | ok |

## Como migrar

```
/migrar-teste <NomeDaClasseTest>   # um teste (comece pelo nº 1)
/migrar-modulo sugestao            # a fila inteira, um por vez
```

Regras que valem sempre: ISO-8859-1, validacao em fase A e fase B, um
teste por vez. Detalhe em `../../skills/migracao-massa-teste/SKILL.md`.

<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->

## Anotacoes

Decisoes tomadas, duvidas para o time, defeitos encontrados no `.sql`
original. Este bloco sobrevive a regeneracao.
