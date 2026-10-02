# Mapeamento SQL -> Java

Referencia de conversao. Numeros medidos sobre os 208 `.sql` do projeto
(2701 statements) em 2026-08.

## Tabela de correspondencia

| SQL | Java | Cobertura |
|---|---|---|
| `UPDATE TBLVPVALORPARAMETRO SET VLPARAMETRO='X' WHERE CDPARAMETRO=N` | `ParametrosTestUtil.setParametro(N, "X")` | automatico |
| idem, com valor JSON | `ParametrosTestUtil.setParametro(N, "chave", "valor")` por chave | automatico + revisao |
| `INSERT INTO T (cols) VALUES (vals)` | `TabelasTestUtil.insert("T", "col", val, ...)` | automatico |
| `INSERT ... VALUES (a),(b)` | uma chamada `insert()` por tupla | automatico |
| `UPDATE T SET c=v WHERE w` | `TabelasTestUtil.update("T", "w", "c", v)` | automatico |
| `UPDATE T SET c=v` (sem WHERE) | `TabelasTestUtil.update("T", null, "c", v)` | automatico |
| `DELETE FROM T WHERE w` | sem equivalente -- ver abaixo | manual (14 casos) |
| `ALTER TABLE` / DDL | permanece em `.ddl`/`.sql` | manual (15 casos) |
| `DATE('now')`, `STRFTIME(...)` | data calculada em Java | manual (~120 casos) |
| `X'...'` (blob hex) | sem equivalente | manual (2 casos) |
| `CDPARAMETRO IN ('a','b')` | uma chamada por codigo | manual (3 casos) |

## Fidelidade de tipos -- a regra que nao pode ser quebrada

`TabelasTestUtil.formatarValor()`:

```java
if (valor == null) return "NULL";
if (valor instanceof Number) return valor.toString();
return "'" + valor.toString().replace("'", "''") + "'";
```

Portanto o tipo Java decide se o valor sai com aspas no SQL final:

| SQL original | Java correto | Java ERRADO |
|---|---|---|
| `'1'` | `"1"` | `1` |
| `1` | `1` | `"1"` |
| `100.0000000` | `100.0000000` | `"100.0000000"` |
| `null` | `null` | `"null"` |

`"null"` (String) grava a palavra `null` como texto na coluna. E o erro de
conversao mais silencioso que existe -- a coluna deixa de ser NULL e passa a
conter quatro caracteres.

Colunas `CDEMPRESA`, `CDREPRESENTANTE`, `CDPRODUTO` e `rowkey` sao gravadas como
texto na massa atual. Mantenha `String`.

## Datas: o maior grupo de "bloqueios"

~120 dos 167 bloqueios sao funcoes de data do SQLite. Nao sao um problema
tecnico -- sao justamente o caso de uso que motivou a refatoracao: massa que
depende do dia da execucao.

```sql
DATE('now', 'localtime')
```

```java
TabelasTestUtil.tabela("TBLVPVISITA").set("DTVISITA", DatasTestUtil.hoje()) ...
```

Use `DatasTestUtil` (`presentation/ui/base/DatasTestUtil.java`). Nao instancie
`LocalDate`/`SimpleDateFormat` dentro do teste -- a util ja fixa o formato que
o banco grava (`yyyy-MM-dd`) e o que a UI exibe (`dd/MM/yyyy`).

| SQLite | `DatasTestUtil` |
|---|---|
| `DATE('now','localtime')` | `hoje()` |
| `DATE('now','+N days')` | `hojeMais(N)` |
| `DATE('now','-N days')` | `hojeMenos(N)` |
| `TIME('now','localtime')` | `agora()` |
| `STRFTIME('%w', DATE('now','localtime')) + 1` | `diaDaSemana()` |

Para assertiva sobre o texto da tela: `hojeUi()` e `hojeUi(dias)`.

Sem equivalente na util (`+1 month`, `start of month`, ...): calcule com
`java.time` no teste e considere propor o metodo na util se repetir.

Cuidado com `STRFTIME('%w', ...)`: SQLite retorna 0 para domingo;
`DayOfWeek.getValue()` retorna 7 para domingo e 1 para segunda. `diaDaSemana()`
ja reproduz a semantica do SQL original (domingo -> 1). Confira contra a regra
de negocio de `NUDIASEMANA` antes de aceitar.

## DELETE

Nao existe `TabelasTestUtil.delete()`. Duas saidas:

```java
// A) enquanto nao houver metodo dedicado
DatabasePrepareTestUtil.executeUpdate("DELETE FROM TBLVPFAIXABOLETO WHERE CDEMPRESA = '1'");
```

```java
// B) melhoria sugerida em TabelasTestUtil (14 casos justificam)
public static void delete(String tabela, String where) throws Exception {
    StringBuilder sql = new StringBuilder("DELETE FROM ").append(tabela);
    if (where != null && !where.trim().isEmpty()) {
        sql.append(" WHERE ").append(where);
    }
    DatabasePrepareTestUtil.executeUpdate(sql.append(";").toString());
}
```

## Blob hexadecimal

Dois testes de marcador inserem PNG como `X'89504E47...'` em `IMMARCADORATIVO`.
`formatarValor()` colocaria aspas e gravaria a string hex como texto.
Mantenha esses statements no `.sql` (migracao parcial) ate haver suporte a blob.

## Formato do resultado

Alinhe-se ao exemplo de referencia (`CT033-T001`): parametros primeiro, tabelas
depois, numeradas por bloco de intencao.

```java
@SuppressWarnings("checkstyle:MultipleStringLiterals")
@InvokeInit
private void prepararMassaDeDados() throws Exception {

    // 1. Parametros de remessa e impressao
    ParametrosTestUtil.setParametro(1605, "S");
    ParametrosTestUtil.setParametro(1606, "7");

    // 2. Produtos usados no cenario
    TabelasTestUtil.insert("TBLVPPRODUTO",
            "CDEMPRESA", "1", "CDREPRESENTANTE", "1", "CDPRODUTO", "1000",
            "DSPRODUTO", "PRODUTO TESTE REMESSA 01", "FLSITUACAO", 1,
            "CDUNIDADE", "UN", "rowkey", "1;1;1000;"
    );
}
```
