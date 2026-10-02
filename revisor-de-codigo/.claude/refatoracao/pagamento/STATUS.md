# Refatoracao -- modulo `pagamento`

> Gerado por `massa.py plano`. O estado e deduzido do repositorio
> (presenca de `.sql` e de `@InvokeInit`), entao nao envelhece.
> Regenere depois de cada teste migrado. Anotacoes manuais no fim do
> arquivo sao preservadas.

| | |
|---|---|
| Classes de teste | 5 |
| Arquivos `.sql` restantes | 4 |
| Statements | 21 |
| Convertiveis automaticamente | 10 (48%) |
| Exigem decisao humana | 11 |
| Migrados / em fase A | 0 / 0 |

## Ordem sugerida

Menor esforco primeiro. `bloq` = statements que exigem decisao.

| # | Estado | Teste | stmts | auto | bloq | enc |
|---|---|---|---|---|---|---|
| 1 | NAO INICIADO | `EfetuarMultiplosPagamentosTest` | 4 | 3 | 1 | ok |
| 2 | NAO INICIADO | `EfetuarPagamentoPadraoTest` | 4 | 2 | 2 | ok |
| 3 | NAO INICIADO | `ValidarOrdemMensagemPagamentoTituloTest` | 7 | 4 | 3 | ok |
| 4 | NAO INICIADO | `EfetuarPagamentoComTituloTest` | 6 | 1 | 5 | ok |

## Bloqueios por causa raiz

| Causa | Qtd | Resolvivel na util? |
|---|---|---|
| delete() em TabelasTestUtil | 9 | sim |
| expressao de data sem equivalente em DatasTestUtil | 2 | nao |

**9 dos 11 bloqueios deste modulo somem** com as melhorias em
`../../skills/migracao-massa-teste/referencias/proposta-melhorias-utils.md`.
Considere resolver a util antes de migrar este modulo -- e uma
mudanca contra 9 ocorrencias.

<details><summary>Detalhe dos bloqueios</summary>

- **9x** DELETE nao tem equivalente em TabelasTestUtil. Use DatabasePrepareTestUtil.executeUpdate(...) ou crie TabelasTestUtil.delete().
- **1x** INSERT em TBLVPFICHAFINANCEIRA -- DATE/TIME sem 'localtime' responde em UTC; DatasTestUtil e local. Confirme com o time se a intencao era a data local antes de usar hoje().
- **1x** INSERT em TBLVPTITULOFINANCEIRO -- DATE/TIME sem 'localtime' responde em UTC; DatasTestUtil e local. Confirme com o time se a intencao era a data local antes de usar hoje().

</details>

## Como migrar

```
/migrar-teste <NomeDaClasseTest>   # um teste (comece pelo nº 1)
/migrar-modulo pagamento           # a fila inteira, um por vez
```

Regras que valem sempre: ISO-8859-1, validacao em fase A e fase B, um
teste por vez. Detalhe em `../../skills/migracao-massa-teste/SKILL.md`.

<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->

## Anotacoes

Decisoes tomadas, duvidas para o time, defeitos encontrados no `.sql`
original. Este bloco sobrevive a regeneracao.
