# Refatoracao -- modulo `grade`

> Gerado por `massa.py plano`. O estado e deduzido do repositorio
> (presenca de `.sql` e de `@InvokeInit`), entao nao envelhece.
> Regenere depois de cada teste migrado. Anotacoes manuais no fim do
> arquivo sao preservadas.

| | |
|---|---|
| Classes de teste | 6 |
| Arquivos `.sql` restantes | 6 |
| Statements | 322 |
| Convertiveis automaticamente | 322 (100%) |
| Exigem decisao humana | 0 |
| Migrados / em fase A | 0 / 0 |

## Ordem sugerida

Menor esforco primeiro. `bloq` = statements que exigem decisao.

| # | Estado | Teste | stmts | auto | bloq | enc |
|---|---|---|---|---|---|---|
| 1 | NAO INICIADO | `ValidarAtualizacaoEstoqueGradeVendaTest` | 46 | 46 | 0 | ok |
| 2 | NAO INICIADO | `ValidarBloqueioFechamentoPedidoComGradeProdutoSemEstoqueTest` | 47 | 47 | 0 | ok |
| 3 | NAO INICIADO | `ValidarInsercaoItensGradeQuantidadeReplicacaoItemTest` | 53 | 53 | 0 | ok |
| 4 | NAO INICIADO | `ValidarBloqueioPedidoVendaEmGradeTest` | 54 | 54 | 0 | ok |
| 5 | NAO INICIADO | `ValidarAtualizacaoEstoqueGradeBonificacaoTest` | 60 | 60 | 0 | ok |
| 6 | NAO INICIADO | `ValidarAtualizacaoEstoqueGradeVendaQuantidadesFracionadasTest` | 62 | 62 | 0 | ok |

## Como migrar

```
/migrar-teste <NomeDaClasseTest>   # um teste (comece pelo nº 1)
/migrar-modulo grade               # a fila inteira, um por vez
```

Regras que valem sempre: ISO-8859-1, validacao em fase A e fase B, um
teste por vez. Detalhe em `../../skills/migracao-massa-teste/SKILL.md`.

<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->

## Anotacoes

Decisoes tomadas, duvidas para o time, defeitos encontrados no `.sql`
original. Este bloco sobrevive a regeneracao.
