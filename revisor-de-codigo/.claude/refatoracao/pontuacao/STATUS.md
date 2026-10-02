# Refatoracao -- modulo `pontuacao`

> Gerado por `massa.py plano`. O estado e deduzido do repositorio
> (presenca de `.sql` e de `@InvokeInit`), entao nao envelhece.
> Regenere depois de cada teste migrado. Anotacoes manuais no fim do
> arquivo sao preservadas.

| | |
|---|---|
| Classes de teste | 7 |
| Arquivos `.sql` restantes | 7 |
| Statements | 105 |
| Convertiveis automaticamente | 105 (100%) |
| Exigem decisao humana | 0 |
| Migrados / em fase A | 0 / 0 |

## Ordem sugerida

Menor esforco primeiro. `bloq` = statements que exigem decisao.

| # | Estado | Teste | stmts | auto | bloq | enc |
|---|---|---|---|---|---|---|
| 1 | NAO INICIADO | `EmitirPedidoProdutosComPontuacaoTest` | 13 | 13 | 0 | ok |
| 2 | NAO INICIADO | `EmitirPedidoProdutosComPontuacaoIgnorandoQuantidadeItensTest` | 13 | 13 | 0 | ok |
| 3 | NAO INICIADO | `EmitirPedidoProdutosComPontuacaoRealizadaMenorQuePontuacaoBaseTest` | 14 | 14 | 0 | ok |
| 4 | NAO INICIADO | `EmitirPedidoProdutosComPontuacaoConsiderandoValorTotalPedidoTest` | 14 | 14 | 0 | ok |
| 5 | NAO INICIADO | `EmitirPedidoProdutosComPontuacaoRealizadaMaiorIgualPontuacaoBaseTest` | 14 | 14 | 0 | ok |
| 6 | NAO INICIADO | `EmitirPedidoProdutosComPontuacaoUnidadeTest` | 16 | 16 | 0 | ok |
| 7 | NAO INICIADO | `EmitirPedidoProdutosComPontuacaoEUnidadesAlternativasTest` | 21 | 21 | 0 | ok |

## Como migrar

```
/migrar-teste <NomeDaClasseTest>   # um teste (comece pelo nº 1)
/migrar-modulo pontuacao           # a fila inteira, um por vez
```

Regras que valem sempre: ISO-8859-1, validacao em fase A e fase B, um
teste por vez. Detalhe em `../../skills/migracao-massa-teste/SKILL.md`.

<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->

## Anotacoes

Decisoes tomadas, duvidas para o time, defeitos encontrados no `.sql`
original. Este bloco sobrevive a regeneracao.
