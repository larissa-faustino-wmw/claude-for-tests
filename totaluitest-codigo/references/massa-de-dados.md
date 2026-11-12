# Massa de dados no código

A massa roda num método anotado com `@InvokeInit` (`br.com.wmw.totalcross.test.api.annotation.InvokeInit`), chamado antes do teste. Os utils ficam em `src/test/java/br/com/wmw/lavenderepda/presentation/ui/base/`. Assinaturas conferidas no `totaluitest` (develop, 10/11/2026).

## `@InvokeInit`

```java
@InvokeInit
public void prepararMassaDeDados() throws Exception { ... }
```

Aceita `order` (ordem entre vários métodos, padrão 0) e `unique` (roda uma vez só, padrão false).

Cada bloco da massa leva um comentário numerado dizendo o que configura e para quê, como nos testes novos:

```java
// 2. Parâmetro 970 (configCalculoDeTributacaoPersonalizado): tributação personalizada com 2 casas para CBS/IBS
```

## `ParametrosTestUtil`

| Chamada | Uso |
|---|---|
| `setParametro(int cd, String valor)` | parâmetro simples: grava o valor. Se o parâmetro é JSON (está em `PARAMETROS_JSON`), grava o valor na chave `usa` |
| `setParametro(int cd, String chave, String valor)` | uma chave só de um parâmetro JSON |
| `setParametro(int cd, Map<String, Object> map)` | várias chaves de um parâmetro JSON, uma a uma (patch com `json_set`: as chaves que você não passar ficam como estão) |

**Parâmetros JSON e a lista `PARAMETROS_JSON`.** O util só trata como JSON os códigos listados no `Set PARAMETROS_JSON` do `ParametrosTestUtil`. Consequências:

- Parâmetro JSON **fora da lista** + `Map`: **nada é gravado**, sem erro. O teste roda com a configuração errada.
- Parâmetro JSON **fora da lista** + `String`: o JSON inteiro é trocado pela string (ex.: `"N"`). O app não consegue ler o parâmetro, componentes somem da tela e o teste termina em `TimeoutException`.

Antes de usar um parâmetro JSON, confira se o código está na lista. Se não estiver, acrescente-o (na faixa numérica certa) e liste o `ParametrosTestUtil.java` em Classes alteradas.

Parâmetro com vários valores numéricos usa o formato do próprio parâmetro (ex.: `"10;5"`, `"11;6;7;1;4;3;24:2;13;"`). Quando não souber o formato, procure o parâmetro em outros testes ou no código do `lavenderepda` (`LavenderePdaConfig`).

Importe `java.util.HashMap` e `java.util.Map` quando houver `Map`.

## `TabelasTestUtil`

| Chamada | Uso |
|---|---|
| `insert("TABELA", "COL1", val1, "COL2", val2, ..., "rowkey", "a;b;c;")` | insert; pares coluna/valor (número ímpar de argumentos lança `IllegalArgumentException`); **sempre termine com o par `rowkey`** |
| `update("TABELA", "WHERE", "COL1", val1, ...)` | update com a cláusula WHERE sem a palavra `WHERE` (ex.: `"CDPRODUTO = '10'"`) |
| `delete("TABELA", "WHERE")` | delete; WHERE nulo ou vazio apaga a tabela inteira, então nunca passe vazio por engano |
| `tabela("TABELA").set(...).where(...).executeUpdate()` | forma encadeada, equivalente |

Valores: `String` vira texto entre aspas; `Number` vai sem aspas; `null` vira `NULL`.

**Rowkey**: siga o formato das rowkeys da mesma tabela em testes existentes (as chaves na ordem da PK, separadas por `;`, terminando em `;`). Quando a rowkey depende de um id gerado no teste (ex.: número do pedido), capture o id na tela e monte a rowkey no passo.

**Fonte das colunas**: a classe de domain do `lavenderepda` (`TABLE_NAME`), não o `docs/modelo-er/`.

## `DatasTestUtil`

Para datas dinâmicas, use o util em vez de data fixa ou `SimpleDateFormat` novo:

| Chamada | Retorna |
|---|---|
| `hoje()`, `hojeMais(n)`, `hojeMenos(n)` | data no formato do banco (`yyyy-MM-dd`), para a massa |
| `hojeUi()`, `hojeUi(n)` | data no formato da tela (`dd/MM/yyyy`), para os asserts |
| `agora()`, `diaDaSemana()`, `diaDaSemana(n)` | hora atual e dia da semana |

Testes antigos usam `SimpleDateFormat`; em teste novo ou refatorado, prefira o `DatasTestUtil`.

## Erros comuns na massa

- Parâmetro JSON fora de `PARAMETROS_JSON` (acima).
- Insert sem `rowkey`, ou rowkey em formato diferente do da tabela.
- Data fixa: o teste quebra no dia seguinte ou no fim de semana.
- Massa copiada de util compartilhado (ex.: `UtilAgenda.populaAgendaVisita`) em vez de trazida para a classe: o teste passa a depender do que outro teste configura.
- Massa que não bate com o cenário (parâmetro com valor diferente do documentado).
