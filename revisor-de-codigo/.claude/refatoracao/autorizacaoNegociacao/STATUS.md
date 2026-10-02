# Refatoracao -- modulo `autorizacaoNegociacao`

> Gerado por `massa.py plano`. O estado e deduzido do repositorio
> (presenca de `.sql` e de `@InvokeInit`), entao nao envelhece.
> Regenere depois de cada teste migrado. Anotacoes manuais no fim do
> arquivo sao preservadas.

| | |
|---|---|
| Classes de teste | 1 |
| Arquivos `.sql` restantes | 2 |
| Statements | 0 |
| Convertiveis automaticamente | 0 (0%) |
| Exigem decisao humana | 0 |
| Migrados / em fase A | 0 / 2 |

## Ordem sugerida

Menor esforco primeiro. `bloq` = statements que exigem decisao.

| # | Estado | Teste | stmts | auto | bloq | enc |
|---|---|---|---|---|---|---|
| 1 | FASE A | `ValidarSolicitacaoAutorizacaoNegociacaoTest` | 0 | 0 | 0 | ok |
| 2 | FASE A | `ValidarSolicitacaoAutorizacaoNegociacaoTest_Retorno` | 0 | 0 | 0 | ok |

## Como migrar

```
/migrar-teste <NomeDaClasseTest>   # um teste (comece pelo nº 1)
/migrar-modulo autorizacaoNegociacao # a fila inteira, um por vez
```

Regras que valem sempre: ISO-8859-1, validacao em fase A e fase B, um
teste por vez. Detalhe em `../../skills/migracao-massa-teste/SKILL.md`.

<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->

## Anotacoes

Decisoes tomadas, duvidas para o time, defeitos encontrados no `.sql`
original. Este bloco sobrevive a regeneracao.

### 2026-08-06 -- migracao do modulo (fases A e B NAO executadas)

Maven indisponivel na maquina (`mvn not found`). O codigo esta migrado, mas
nenhuma das duas fases rodou. **Ninguem apague os `.sql` antes da fase B.**

**`_Retorno.sql` nao e massa de preparacao.** Ele roda no meio do teste
(passo 6), chamado por `DatabasePrepareTestUtil.execSqlRetornoWeb(getClass())`,
simulando o retorno da autorizacao vinda da web. Nao podia virar `@InvokeInit`:
antes do teste a linha de `TBLVPSOLAUTORIZACAO` nem existe, o update viraria
no-op e a assertiva "Autorizado" do passo 6 quebraria. Virou
`TabelasTestUtil.update("TBLVPSOLAUTORIZACAO", null, "FLAUTORIZADO", "S")`
no mesmo ponto do fluxo. O `where` nulo e suportado por `executeUpdate()` e
preserva o update sem WHERE do original.

Vale para os demais `_Retorno.sql` do repositorio: a migracao deles e para o
corpo do teste, nunca para `prepararMassaDeDados()`.

**Parametro 583: mudanca de comportamento aceita.** O `.sql` gravava o texto
simples `'N'` em VLPARAMETRO. O 583 esta no whitelist `PARAMETROS_JSON` de
`ParametrosTestUtil`, entao `setParametro` faz `json_set` em `$.usa` e o valor
gravado passa a ser `{"usa":"N"}`. A intencao (parametro desligado) se mantem e
o `CASE WHEN` de `patchJsonDb` existe justamente para esse legado, mas o texto
no banco nao e mais identico. **Confirmar com o responsavel pelo caso.**

**Parametros 1842, 1835, 456, 422:** substituicao total do JSON virou patch
chave a chave. Todas as chaves do `.sql` foram declaradas, entao so difere se
o banco base trouxer chaves extras -- que agora sobrevivem em vez de sumir.
Parametro 38 nao e JSON, seguiu como update simples.

**Risco conhecido na fase A:** com o `.sql` ainda no lugar, o INSERT em
`TBLVPAUTORIZACAO` (rowkey `20;BASICO;54;1;`) roda duas vezes. Se houver
unique/PK em rowkey, o segundo insert estoura `InvokeInitException`. Isso e
artefato da convivencia SQL+Java, nao erro da migracao -- nesse caso pule
direto para a fase B (renomear os `.sql` para `.bak`) antes de concluir que
a migracao esta errada.

**Defeitos no `.sql` original:** nenhum. Fora de escopo, nao corrigido: em
`deveSolicitarAutorizacao()` ha dois blocos rotulados `//passo 4` e um `;`
solto logo apos `getMessage()`.
