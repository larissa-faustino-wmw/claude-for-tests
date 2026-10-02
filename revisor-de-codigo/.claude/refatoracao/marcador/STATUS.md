# Refatoracao -- modulo `marcador`

> Gerado por `massa.py plano`. O estado e deduzido do repositorio
> (presenca de `.sql` e de `@InvokeInit`), entao nao envelhece.
> Regenere depois de cada teste migrado. Anotacoes manuais no fim do
> arquivo sao preservadas.

| | |
|---|---|
| Classes de teste | 4 |
| Arquivos `.sql` restantes | 4 |
| Statements | 15 |
| Convertiveis automaticamente | 11 (73%) |
| Exigem decisao humana | 4 |
| Migrados / em fase A | 0 / 0 |

## Ordem sugerida

Menor esforco primeiro. `bloq` = statements que exigem decisao.

| # | Estado | Teste | stmts | auto | bloq | enc |
|---|---|---|---|---|---|---|
| 1 | NAO INICIADO | `ApresentarMarcadorClienteTest` | 3 | 2 | 1 | ok |
| 2 | NAO INICIADO | `ApresentarMarcadorProdutoporClienteTest` | 3 | 2 | 1 | ok |
| 3 | NAO INICIADO | `ApresentarMarcadorProdutoTest` | 3 | 2 | 1 | ok |
| 4 | NAO INICIADO | `ApresentarMarcadorPedidoTest` | 6 | 5 | 1 | ok |

## Bloqueios por causa raiz

| Causa | Qtd | Resolvivel na util? |
|---|---|---|
| blob hexadecimal | 2 | nao |
| analise caso a caso | 2 | nao |

<details><summary>Detalhe dos bloqueios</summary>

- **4x** INSERT em TBLVPMARCADOR

</details>

## Como migrar

```
/migrar-teste <NomeDaClasseTest>   # um teste (comece pelo nº 1)
/migrar-modulo marcador            # a fila inteira, um por vez
```

Regras que valem sempre: ISO-8859-1, validacao em fase A e fase B, um
teste por vez. Detalhe em `../../skills/migracao-massa-teste/SKILL.md`.

<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->

## Anotacoes

Decisoes tomadas, duvidas para o time, defeitos encontrados no `.sql`
original. Este bloco sobrevive a regeneracao.
