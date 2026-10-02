# Refatoracao -- modulo `nfe`

> Gerado por `massa.py plano`. O estado e deduzido do repositorio
> (presenca de `.sql` e de `@InvokeInit`), entao nao envelhece.
> Regenere depois de cada teste migrado. Anotacoes manuais no fim do
> arquivo sao preservadas.

| | |
|---|---|
| Classes de teste | 3 |
| Arquivos `.sql` restantes | 3 |
| Statements | 66 |
| Convertiveis automaticamente | 63 (95%) |
| Exigem decisao humana | 3 |
| Migrados / em fase A | 0 / 0 |

## Ordem sugerida

Menor esforco primeiro. `bloq` = statements que exigem decisao.

| # | Estado | Teste | stmts | auto | bloq | enc |
|---|---|---|---|---|---|---|
| 1 | NAO INICIADO | `ValidarGeracaoNFEFechamentoPedidoTest` | 13 | 13 | 0 | ok |
| 2 | NAO INICIADO | `ValidarUtilizacaoNotaFiscalEletronicaAgrupandoOsItensPorReferenciaTest` | 34 | 33 | 1 | ok |
| 3 | NAO INICIADO | `ValidarFiltroPedidosCamposNFeCapaPedidoTituloClienteTest` | 19 | 17 | 2 | ok |

## Bloqueios por causa raiz

| Causa | Qtd | Resolvivel na util? |
|---|---|---|
| expressao de data sem equivalente em DatasTestUtil | 3 | nao |

<details><summary>Detalhe dos bloqueios</summary>

- **3x** INSERT em TBLVPPEDIDO -- DATE/TIME sem 'localtime' responde em UTC; DatasTestUtil e local. Confirme com o time se a intencao era a data local antes de usar hoje().

</details>

## Como migrar

```
/migrar-teste <NomeDaClasseTest>   # um teste (comece pelo nº 1)
/migrar-modulo nfe                 # a fila inteira, um por vez
```

Regras que valem sempre: ISO-8859-1, validacao em fase A e fase B, um
teste por vez. Detalhe em `../../skills/migracao-massa-teste/SKILL.md`.

<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->

## Anotacoes

Decisoes tomadas, duvidas para o time, defeitos encontrados no `.sql`
original. Este bloco sobrevive a regeneracao.
