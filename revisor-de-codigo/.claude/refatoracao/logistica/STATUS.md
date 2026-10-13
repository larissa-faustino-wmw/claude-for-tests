# Refatoracao -- modulo `logistica`

> Gerado por `massa.py plano`. O estado e deduzido do repositorio
> (presenca de `.sql` e de `@InvokeInit`), entao nao envelhece.
> Regenere depois de cada teste migrado. Anotacoes manuais no fim do
> arquivo sao preservadas.

| | |
|---|---|
| Classes de teste | 10 |
| Arquivos `.sql` restantes | 10 |
| Statements | 193 |
| Convertiveis automaticamente | 193 (100%) |
| Exigem decisao humana | 0 |
| Migrados / em fase A | 0 / 0 |

## Ordem sugerida

Menor esforco primeiro. `bloq` = statements que exigem decisao.

| # | Estado | Teste | stmts | auto | bloq | enc |
|---|---|---|---|---|---|---|
| 1 | NAO INICIADO | `ValidarSelecaoTransportadoraFechamentoPedidoPorRegiaoEDataTest` | 13 | 13 | 0 | ok |
| 2 | NAO INICIADO | `ValidarSelecaoTransportadoraInicioPedidoPorCepTest` | 15 | 15 | 0 | ok |
| 3 | NAO INICIADO | `ValidarSelecaoTransportadoraQualquerMomentoNoPedidoPorCepTest` | 15 | 15 | 0 | ok |
| 4 | NAO INICIADO | `ValidarSelecaoTransportadoraQualquerMomentoPedidoObservacaoTest` | 19 | 19 | 0 | ok |
| 5 | NAO INICIADO | `ValidarTransportadoraMultiploEnderecoFreteMinimoTest` | 19 | 19 | 0 | ok |
| 6 | NAO INICIADO | `ValidarFreteClienteJaCalculandoRateioFreteTransportadoraTest` | 21 | 21 | 0 | ok |
| 7 | NAO INICIADO | `ValidarTransportadoraQualquerMomentoPedidoMultiplosEnderecosTest` | 22 | 22 | 0 | ok |
| 8 | NAO INICIADO | `ValidarBloqueioPedidoSelecionaTransportadoraQualquerMomentoTest` | 23 | 23 | 0 | ok |
| 9 | NAO INICIADO | `ValidarDataEntregaTransportadoraRelacionadaTipoFreteTest` | 23 | 23 | 0 | ok |
| 10 | NAO INICIADO | `ValidarPedidoSemSelecaoTransportadoraComSomaFreteNoValorTotalTest` | 23 | 23 | 0 | ok |

## Como migrar

```
/migrar-teste <NomeDaClasseTest>   # um teste (comece pelo nº 1)
/migrar-modulo logistica           # a fila inteira, um por vez
```

Regras que valem sempre: ISO-8859-1, validacao em fase A e fase B, um
teste por vez. Detalhe em `../../skills/migracao-massa-teste/SKILL.md`.

<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->

## Anotacoes

Decisoes tomadas, duvidas para o time, defeitos encontrados no `.sql`
original. Este bloco sobrevive a regeneracao.
