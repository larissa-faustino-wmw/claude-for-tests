# Refatoracao -- modulo `pedido`

> Gerado por `massa.py plano`. O estado e deduzido do repositorio
> (presenca de `.sql` e de `@InvokeInit`), entao nao envelhece.
> Regenere depois de cada teste migrado. Anotacoes manuais no fim do
> arquivo sao preservadas.

| | |
|---|---|
| Classes de teste | 18 |
| Arquivos `.sql` restantes | 17 |
| Statements | 152 |
| Convertiveis automaticamente | 147 (97%) |
| Exigem decisao humana | 5 |
| Migrados / em fase A | 0 / 0 |

## Ordem sugerida

Menor esforco primeiro. `bloq` = statements que exigem decisao.

| # | Estado | Teste | stmts | auto | bloq | enc |
|---|---|---|---|---|---|---|
| 1 | NAO INICIADO | `EmitirPedidoTrocaOrdenacaoDescricaoTest` | 2 | 2 | 0 | ok |
| 2 | NAO INICIADO | `EmitirPedidoSemUtilizarGondolaTest` | 3 | 3 | 0 | ok |
| 3 | NAO INICIADO | `EmitirPedidoUtilizandoGondolaTest` | 3 | 3 | 0 | ok |
| 4 | NAO INICIADO | `EmitirPedidoTrocaOrdenacaoDescricaoMotivoTrocaPorItemTest` | 4 | 4 | 0 | ok |
| 5 | NAO INICIADO | `EmitirPedidoTrocaOrdenacaoCodigoEDoisTiposPedidoTrocaTest` | 4 | 4 | 0 | ok |
| 6 | NAO INICIADO | `EmitirPedidoValorMinimoVendaCondicaoPagamentoTest` | 5 | 5 | 0 | ok |
| 7 | NAO INICIADO | `EmitirPedidoValorMinimoVendaCondicaoPagamentoSemAtingirMinimoTest` | 5 | 5 | 0 | ok |
| 8 | NAO INICIADO | `EmitirPedidoNovoClienteSemClienteComListaDeItensPadraoTest` | 8 | 8 | 0 | ok |
| 9 | NAO INICIADO | `ValidarPedidoUnidadeAlternativaTrocaTabelaPrecoTest` | 12 | 12 | 0 | ok |
| 10 | NAO INICIADO | `EmitirPedidoItemBonificadoEItemDeVendaTest` | 14 | 14 | 0 | ok |
| 11 | NAO INICIADO | `EmitirPedidoValidandoEstoqueVerbaTributacaoDescontosTest` | 15 | 15 | 0 | ok |
| 12 | NAO INICIADO | `EmitirPedidoNovoClienteSemClienteSemCarrosselFotosTest` | 29 | 29 | 0 | ok |
| 13 | NAO INICIADO | `ValidarEdicaoBonificacaoExtrapolandoEstoqueTest` | 7 | 6 | 1 | ok |
| 14 | NAO INICIADO | `ValidarEstoqueItemBonificadoPedidoNormalTest` | 7 | 6 | 1 | ok |
| 15 | NAO INICIADO | `ValidarBloqueioPedidoNovoClienteTest` | 7 | 6 | 1 | ok |
| 16 | NAO INICIADO | `ValidarEstoqueItensTrocaRecolherPedidoComoDescontoTest` | 13 | 12 | 1 | ok |
| 17 | NAO INICIADO | `EmitirPedidoNovoClienteComTipoDeFreteTest` | 14 | 13 | 1 | ok |

## Bloqueios por causa raiz

| Causa | Qtd | Resolvivel na util? |
|---|---|---|
| delete() em TabelasTestUtil | 2 | sim |
| DDL -- permanece no .sql (correto) | 2 | nao |
| expressao de data sem equivalente em DatasTestUtil | 1 | nao |

**2 dos 5 bloqueios deste modulo somem** com as melhorias em
`../../skills/migracao-massa-teste/referencias/proposta-melhorias-utils.md`.
Considere resolver a util antes de migrar este modulo -- e uma
mudanca contra 2 ocorrencias.

<details><summary>Detalhe dos bloqueios</summary>

- **2x** DELETE nao tem equivalente em TabelasTestUtil. Use DatabasePrepareTestUtil.executeUpdate(...) ou crie TabelasTestUtil.delete().
- **2x** DDL nao pertence a massa de dados. Manter em .ddl/.sql ou DatabasePrepareTestUtil.executeUpdate(...).
- **1x** INSERT em TBLVPPEDIDOERP -- DATE/TIME sem 'localtime' responde em UTC; DatasTestUtil e local. Confirme com o time se a intencao era a data local antes de usar hoje().

</details>

## Como migrar

```
/migrar-teste <NomeDaClasseTest>   # um teste (comece pelo nº 1)
/migrar-modulo pedido              # a fila inteira, um por vez
```

Regras que valem sempre: ISO-8859-1, validacao em fase A e fase B, um
teste por vez. Detalhe em `../../skills/migracao-massa-teste/SKILL.md`.

<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->

## Anotacoes

Decisoes tomadas, duvidas para o time, defeitos encontrados no `.sql`
original. Este bloco sobrevive a regeneracao.
