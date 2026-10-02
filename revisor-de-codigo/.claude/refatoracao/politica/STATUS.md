# Refatoracao -- modulo `politica`

> Gerado por `massa.py plano`. O estado e deduzido do repositorio
> (presenca de `.sql` e de `@InvokeInit`), entao nao envelhece.
> Regenere depois de cada teste migrado. Anotacoes manuais no fim do
> arquivo sao preservadas.

| | |
|---|---|
| Classes de teste | 12 |
| Arquivos `.sql` restantes | 12 |
| Statements | 123 |
| Convertiveis automaticamente | 120 (98%) |
| Exigem decisao humana | 3 |
| Migrados / em fase A | 0 / 0 |

## Ordem sugerida

Menor esforco primeiro. `bloq` = statements que exigem decisao.

| # | Estado | Teste | stmts | auto | bloq | enc |
|---|---|---|---|---|---|---|
| 1 | NAO INICIADO | `EmitirPedidoPoliticaBonificacaoAutomaticaSomenteProprioConjuntoTest` | 6 | 6 | 0 | ok |
| 2 | NAO INICIADO | `EmitirPedidoPoliticaBonificacaoRemocaoBrindesAposPerderFaixaTest` | 7 | 7 | 0 | ok |
| 3 | NAO INICIADO | `EmitirPedidoPoliticaBonificacaoReducaoExclusaoItensComBonificacaoTest` | 7 | 7 | 0 | ok |
| 4 | NAO INICIADO | `EmitirPedidoPoliticaBonificacaoRemovendoBrindePedidoTest` | 8 | 8 | 0 | ok |
| 5 | NAO INICIADO | `EmitirPedidoPoliticaBonificacaoPorFaixaQuantidadeAutomaticaTest` | 10 | 10 | 0 | ok |
| 6 | NAO INICIADO | `EmitirPedidoPoliticaBonificacaoPorFaixaQuantidadeManualTest` | 10 | 10 | 0 | ok |
| 7 | NAO INICIADO | `EmitirPedidoPoliticaBonificacaoRemovendoItensBonificadosTest` | 14 | 14 | 0 | ok |
| 8 | NAO INICIADO | `EmitirPedidoPoliticaBonificacaoBaseFamiliaLinhaProdutosTest` | 14 | 14 | 0 | ok |
| 9 | NAO INICIADO | `EmitirPedidoPoliticaBonificacaoLinhasProdutosFamiliasTest` | 20 | 20 | 0 | ok |
| 10 | NAO INICIADO | `EmitirPedidoPoliticaBonificacaoComBrindeAutomaticoTest` | 8 | 7 | 1 | ok |
| 11 | NAO INICIADO | `EmitirPedidoAplicandoPoliticaBonificacaoValorItemOpcionalTest` | 9 | 8 | 1 | ok |
| 12 | NAO INICIADO | `EmitirPedidoPoliticaBonificacaoComBrindeOpcionalTest` | 10 | 9 | 1 | ok |

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
/migrar-modulo politica            # a fila inteira, um por vez
```

Regras que valem sempre: ISO-8859-1, validacao em fase A e fase B, um
teste por vez. Detalhe em `../../skills/migracao-massa-teste/SKILL.md`.

<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->

## Anotacoes

Decisoes tomadas, duvidas para o time, defeitos encontrados no `.sql`
original. Este bloco sobrevive a regeneracao.
