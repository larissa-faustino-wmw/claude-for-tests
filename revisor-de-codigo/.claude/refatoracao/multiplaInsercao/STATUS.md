# Refatoracao -- modulo `multiplaInsercao`

> Gerado por `massa.py plano`. O estado e deduzido do repositorio
> (presenca de `.sql` e de `@InvokeInit`), entao nao envelhece.
> Regenere depois de cada teste migrado. Anotacoes manuais no fim do
> arquivo sao preservadas.

| | |
|---|---|
| Classes de teste | 11 |
| Arquivos `.sql` restantes | 11 |
| Statements | 57 |
| Convertiveis automaticamente | 54 (95%) |
| Exigem decisao humana | 3 |
| Migrados / em fase A | 0 / 0 |

## Ordem sugerida

Menor esforco primeiro. `bloq` = statements que exigem decisao.

| # | Estado | Teste | stmts | auto | bloq | enc |
|---|---|---|---|---|---|---|
| 1 | NAO INICIADO | `ArredondarValorInsercaoComDescontoEAlteracaoDescontoCapaTest` | 3 | 3 | 0 | ok |
| 2 | NAO INICIADO | `ExcluirItensTelaDetalhesRefleteNaListaMultiplaInsercaoTest` | 3 | 3 | 0 | ok |
| 3 | NAO INICIADO | `InserirDescontoCapaPuxaDescontoNosProximosItensInseridosTest` | 3 | 3 | 0 | ok |
| 4 | NAO INICIADO | `AlterarDescontoInsercaoItemRefleteNaMultiplaInsercaoTest` | 3 | 3 | 0 | ok |
| 5 | NAO INICIADO | `InserirDescontoCapaValidarDescontosListaDeItensTest` | 4 | 4 | 0 | ok |
| 6 | NAO INICIADO | `ExluirItemDeveRefletirNaListaDeMultiplaInsercaoTest` | 4 | 4 | 0 | ok |
| 7 | NAO INICIADO | `ExcluirItemMultiplaInsercaoZeraValorDescontoTest` | 4 | 4 | 0 | ok |
| 8 | NAO INICIADO | `ReplicacarPedidoComMultiplaInsercaoTest` | 4 | 4 | 0 | ok |
| 9 | NAO INICIADO | `ValidarValoresAposUltrapassarLimiteEstoqueTest` | 7 | 7 | 0 | ok |
| 10 | NAO INICIADO | `ValidarUnidadePadraoMultiplaInsercaoTest` | 15 | 15 | 0 | ok |
| 11 | NAO INICIADO | `TrocarTabelaPrecoItensPedidoTest` | 7 | 4 | 3 | ok |

## Bloqueios por causa raiz

| Causa | Qtd | Resolvivel na util? |
|---|---|---|
| analise caso a caso | 3 | nao |

<details><summary>Detalhe dos bloqueios</summary>

- **3x** UPDATE em TBLVPVALORPARAMETRO altera colunas alem de VLPARAMETRO -- converter a mao.

</details>

## Como migrar

```
/migrar-teste <NomeDaClasseTest>   # um teste (comece pelo nº 1)
/migrar-modulo multiplaInsercao    # a fila inteira, um por vez
```

Regras que valem sempre: ISO-8859-1, validacao em fase A e fase B, um
teste por vez. Detalhe em `../../skills/migracao-massa-teste/SKILL.md`.

<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->

## Anotacoes

Decisoes tomadas, duvidas para o time, defeitos encontrados no `.sql`
original. Este bloco sobrevive a regeneracao.
