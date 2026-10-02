# Refatoracao -- modulo `pesquisa`

> Gerado por `massa.py plano`. O estado e deduzido do repositorio
> (presenca de `.sql` e de `@InvokeInit`), entao nao envelhece.
> Regenere depois de cada teste migrado. Anotacoes manuais no fim do
> arquivo sao preservadas.

| | |
|---|---|
| Classes de teste | 3 |
| Arquivos `.sql` restantes | 3 |
| Statements | 3 |
| Convertiveis automaticamente | 3 (100%) |
| Exigem decisao humana | 0 |
| Migrados / em fase A | 0 / 0 |

## Ordem sugerida

Menor esforco primeiro. `bloq` = statements que exigem decisao.

| # | Estado | Teste | stmts | auto | bloq | enc |
|---|---|---|---|---|---|---|
| 1 | NAO INICIADO | `ValidarPesquisaMercadoSemDependenciaClientePedidoTest` | 1 | 1 | 0 | ok |
| 2 | NAO INICIADO | `ValidarPesquisaMercadoCondicionandoClientePedidoTest` | 1 | 1 | 0 | ok |
| 3 | NAO INICIADO | `ValidarPesquisaMercadoSemDependenciaClienteMenuClienteTest` | 1 | 1 | 0 | ok |

## Como migrar

```
/migrar-teste <NomeDaClasseTest>   # um teste (comece pelo nº 1)
/migrar-modulo pesquisa            # a fila inteira, um por vez
```

Regras que valem sempre: ISO-8859-1, validacao em fase A e fase B, um
teste por vez. Detalhe em `../../skills/migracao-massa-teste/SKILL.md`.

<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->

## Anotacoes

Decisoes tomadas, duvidas para o time, defeitos encontrados no `.sql`
original. Este bloco sobrevive a regeneracao.
