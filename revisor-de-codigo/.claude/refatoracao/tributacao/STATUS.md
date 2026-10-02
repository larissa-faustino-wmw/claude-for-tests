# Refatoracao -- modulo `tributacao`

> Gerado por `massa.py plano`. O estado e deduzido do repositorio
> (presenca de `.sql` e de `@InvokeInit`), entao nao envelhece.
> Regenere depois de cada teste migrado. Anotacoes manuais no fim do
> arquivo sao preservadas.

| | |
|---|---|
| Classes de teste | 32 |
| Arquivos `.sql` restantes | 30 |
| Statements | 592 |
| Convertiveis automaticamente | 592 (100%) |
| Exigem decisao humana | 0 |
| Migrados / em fase A | 0 / 0 |

## Ordem sugerida

Menor esforco primeiro. `bloq` = statements que exigem decisao.

| # | Estado | Teste | stmts | auto | bloq | enc |
|---|---|---|---|---|---|---|
| 1 | NAO INICIADO | `EmitirPedidoTributacaoFixaValorOutorgaSemFecopTest` | 14 | 14 | 0 | ok |
| 2 | NAO INICIADO | `EmitirPedidoTributacaoFixaFecopTipoUmTest` | 14 | 14 | 0 | ok |
| 3 | NAO INICIADO | `EmitirPedidoTributacaoFixaFecopTest` | 14 | 14 | 0 | ok |
| 4 | NAO INICIADO | `EmitirPedidoTributacaoFixaFecopTipoTresTest` | 15 | 15 | 0 | ok |
| 5 | NAO INICIADO | `EmitirPedidoTributacaoFixaFecopTipoDoisTest` | 15 | 15 | 0 | ok |
| 6 | NAO INICIADO | `EmitirPedidoTributacaoFixaMedicamentosSemFecopCalculoAuxiliarRUmTest` | 17 | 17 | 0 | ok |
| 7 | NAO INICIADO | `ReplicarPedidoParaClienteDeOutroEstadoComTributacaoFixaTest` | 17 | 17 | 0 | ok |
| 8 | NAO INICIADO | `EmitirPedidoTributacaoFixaFecopTipoQuatroTest` | 17 | 17 | 0 | ok |
| 9 | NAO INICIADO | `EmitirPedidoTributacaoFixaMedicamentosSemFecopRTresTest` | 17 | 17 | 0 | ok |
| 10 | NAO INICIADO | `EmitirPedidoTributacaoFixaMedicamentosSemFecopCalculoAuxiliarRUMBTest` | 17 | 17 | 0 | ok |
| 11 | NAO INICIADO | `EmitirPedidoTributacaoPersonalizadaPisTest` | 17 | 17 | 0 | ok |
| 12 | NAO INICIADO | `EmitirPedidoTributacaoPersonalizadaCofinsTest` | 17 | 17 | 0 | ok |
| 13 | NAO INICIADO | `EmitirPedidoTributacaoPersonalizadaIcmsTest` | 17 | 17 | 0 | ok |
| 14 | NAO INICIADO | `EmitirPedidoTributacaoPersonalizadaIpiTest` | 17 | 17 | 0 | ok |
| 15 | NAO INICIADO | `EmitirPedidoTributacaoPersonalizadaFecopTipoTresTest` | 17 | 17 | 0 | ok |
| 16 | NAO INICIADO | `EmitirPedidoTributacaoPersonalizadaFecopTipoDoisTest` | 17 | 17 | 0 | ok |
| 17 | NAO INICIADO | `EmitirPedidoTributacaoPersonalizadaFecopTipoQuatroTest` | 17 | 17 | 0 | ok |
| 18 | NAO INICIADO | `EmitirPedidoTributacaoPersonalizadaZonaFrancaSuframaTest` | 17 | 17 | 0 | ok |
| 19 | NAO INICIADO | `EmitirPedidoTributacaoPersonalizadaStTest` | 17 | 17 | 0 | ok |
| 20 | NAO INICIADO | `ReplicarPedidoClienteOutroEstadoTributacaoPersonalizadaTest` | 18 | 18 | 0 | ok |
| 21 | NAO INICIADO | `EmitirPedidoTributacaoPersonalizadaCbsTest` | 19 | 19 | 0 | ok |
| 22 | NAO INICIADO | `EmitirPedidoBonificacaoComTributacaoFixaSemFecopTest` | 23 | 23 | 0 | ok |
| 23 | NAO INICIADO | `EmitirPedidoTributacaoPersonalizadaFecopTipoUmTest` | 23 | 23 | 0 | ok |
| 24 | NAO INICIADO | `EmitirPedidoTributacaoFixaUnidadesAlternativasTest` | 26 | 26 | 0 | ok |
| 25 | NAO INICIADO | `EmitirPedidoBonificadoComTributacaoFixaComValorDePmpfTest` | 28 | 28 | 0 | ok |
| 26 | NAO INICIADO | `EmitirPedidoBonificadoComTributacaoPersonalizadaPisTest` | 29 | 29 | 0 | ok |
| 27 | NAO INICIADO | `EmitirPedidoBonificadoComTributacaoPersonalizadaCofinsTest` | 29 | 29 | 0 | ok |
| 28 | NAO INICIADO | `EmitirPedidoBonificadoComTributacaoPersonalizadaIcmsTest` | 29 | 29 | 0 | ok |
| 29 | NAO INICIADO | `EmitirPedidoBonificadoComTributacaoPersonalizadaIpiTest` | 29 | 29 | 0 | ok |
| 30 | NAO INICIADO | `EmitirPedidoBonificacaoComTributacaoPersonalizadaStTest` | 29 | 29 | 0 | ok |

## Como migrar

```
/migrar-teste <NomeDaClasseTest>   # um teste (comece pelo nº 1)
/migrar-modulo tributacao          # a fila inteira, um por vez
```

Regras que valem sempre: ISO-8859-1, validacao em fase A e fase B, um
teste por vez. Detalhe em `../../skills/migracao-massa-teste/SKILL.md`.

<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->

## Anotacoes

Decisoes tomadas, duvidas para o time, defeitos encontrados no `.sql`
original. Este bloco sobrevive a regeneracao.
