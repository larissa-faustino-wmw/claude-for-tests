# Refatoracao -- modulo `financeiro`

> Gerado por `massa.py plano`. O estado e deduzido do repositorio
> (presenca de `.sql` e de `@InvokeInit`), entao nao envelhece.
> Regenere depois de cada teste migrado. Anotacoes manuais no fim do
> arquivo sao preservadas.

| | |
|---|---|
| Classes de teste | 2 |
| Arquivos `.sql` restantes | 1 |
| Statements | 16 |
| Convertiveis automaticamente | 15 (94%) |
| Exigem decisao humana | 1 |
| Migrados / em fase A | 0 / 0 |

## Ordem sugerida

Menor esforco primeiro. `bloq` = statements que exigem decisao.

| # | Estado | Teste | stmts | auto | bloq | enc |
|---|---|---|---|---|---|---|
| 1 | NAO INICIADO | `ValidarEmissaoPedidoClienteAtrasadoRedeTest` | 16 | 15 | 1 | ok |

## Bloqueios por causa raiz

| Causa | Qtd | Resolvivel na util? |
|---|---|---|
| whitelist PARAMETROS_JSON | 1 | sim |

**1 dos 1 bloqueios deste modulo somem** com as melhorias em
`../../skills/migracao-massa-teste/referencias/proposta-melhorias-utils.md`.
Considere resolver a util antes de migrar este modulo -- e uma
mudanca contra 1 ocorrencias.

<details><summary>Detalhe dos bloqueios</summary>

- **1x** Parametro 923 grava JSON mas NAO esta em ParametrosTestUtil.PARAMETROS_JSON. Sem adicionar o id la, setParametro() sobrescreve o JSON inteiro e corrompe a massa. Adicione 923 ao Set antes de migrar.

</details>

## Como migrar

```
/migrar-teste <NomeDaClasseTest>   # um teste (comece pelo nº 1)
/migrar-modulo financeiro          # a fila inteira, um por vez
```

Regras que valem sempre: ISO-8859-1, validacao em fase A e fase B, um
teste por vez. Detalhe em `../../skills/migracao-massa-teste/SKILL.md`.

<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->

## Anotacoes

Decisoes tomadas, duvidas para o time, defeitos encontrados no `.sql`
original. Este bloco sobrevive a regeneracao.
