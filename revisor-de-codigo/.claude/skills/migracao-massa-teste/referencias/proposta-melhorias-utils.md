# Melhorias sugeridas nas utils

Cada item nasceu de um bloqueio medido na massa atual. Ordenado por
(casos destravados / esforco). Nada aqui foi aplicado -- e proposta.

---

## 1. `TabelasTestUtil.delete()` -- destrava 14 statements

Baixo esforco, simetrico ao que ja existe.

```java
public static void delete(String tabela, String where) throws Exception {
    StringBuilder sql = new StringBuilder("DELETE FROM ").append(tabela);
    if (where != null && !where.trim().isEmpty()) {
        sql.append(" WHERE ").append(where);
    }
    DatabasePrepareTestUtil.executeUpdate(sql.append(";").toString());
}
```

---

## 2. Detectar JSON em tempo de execucao -- elimina a classe 1 de armadilhas

Hoje `PARAMETROS_JSON` e um `Set` de 249 numeros mantido a mao. Toda vez que um
parametro passa a ser JSON no produto, o `Set` fica desatualizado e
`setParametro` corrompe o valor silenciosamente (caso do parametro 923).

`patchJsonDb` **ja** detecta JSON em SQL:

```sql
CASE WHEN VLPARAMETRO LIKE '{%' THEN VLPARAMETRO ELSE '{}' END
```

Se a decisao usasse o valor atual da coluna em vez do `Set`, o whitelist deixaria
de existir e a classe inteira de erro desapareceria:

```java
public static void setParametro(int cdParametro, String chave, String valor) throws Exception {
    if (chave != null || isJson(cdParametro)) {
        patchJsonDb(cdParametro, chave == null ? "usa" : chave, valor);
    } else {
        updateSimples(cdParametro, valor);
    }
}

private static boolean isJson(int cdParametro) throws Exception {
    // SELECT VLPARAMETRO LIKE '{%' FROM TBLVPVALORPARAMETRO WHERE CDPARAMETRO = ?
}
```

Requer um `executeQuery` em `DatabasePrepareTestUtil` (hoje so ha
`executeUpdate`). Enquanto isso nao existir, mantenha o `Set` e trate os
bloqueios do `massa.py` como obrigatorios.

**Correcao urgente, independente do resto:** a sobrecarga de tres argumentos
descarta a chave quando o parametro nao e JSON. Melhor lancar excecao do que
gravar valor errado em silencio.

---

## 3. Escopo por entidade -- 533 statements afetados

```java
public static void setParametro(int cdParametro, String nmEntidade, String vlChave,
                                String chave, String valor) throws Exception
```

`ParametrosTestUtil` filtra so por `CDPARAMETRO`; 533 statements da massa atual
filtram tambem por `NMENTIDADE`/`VLCHAVE`. Com o banco base padrao o efeito
tende a ser o mesmo, mas o contrato e mais largo do que o do `.sql`.

Antes de implementar, vale medir no banco base:

```sql
SELECT CDPARAMETRO, COUNT(*) FROM TBLVPVALORPARAMETRO
GROUP BY CDPARAMETRO HAVING COUNT(*) > 1;
```

Se o resultado vier vazio, a sobrecarga e desnecessaria e basta documentar.
O banco fica em `./db/<versao>/wmwvendas.sqlite3` (baixe com
`mvn compile exec:exec@db -Denv.test=develop`).

---

## 4. Helper de datas -- FEITO

Implementado em `presentation/ui/base/DatasTestUtil.java`: `hoje()`,
`hojeMais(int)`, `hojeMenos(int)`, `hojeUi()`, `hojeUi(int)`, `agora()`,
`diaDaSemana()`, `diaDaSemana(int)`.

O `massa.py` converte sozinho as variantes cobertas -- elas nao aparecem mais
como bloqueio no plano. Continuam bloqueadas de proposito:

- **`DATE()`/`DATE('now')` sem `'localtime'`** -- o SQLite responde em UTC e o
  helper e local. Perto da meia-noite dao dias diferentes, entao converter
  mudaria o comportamento; precisa de decisao de quem mantem o teste.
- **expressao composta** (`'1;1;1;'||(STRFTIME(...)+2)`) -- monte o valor em
  Java e passe pronto.
- **modificador sem equivalente** (`'start of month'`, `'+2 hours'`).

`hojeUi()` tambem serve as assertivas -- hoje cada teste recria um
`SimpleDateFormat("dd/MM/yyyy")` local.

---

## 5. Suporte a blob -- 2 statements

Dois testes de marcador inserem PNG como `X'89504E47...'`.
`formatarValor()` aspa o valor e grava a hex como texto.

```java
public static Object blobHex(String hex) { /* marcador para emitir X'...' sem aspas */ }
```

Volume baixo; manter esses dois no `.sql` e uma decisao legitima.

---

## 6. `executeQuery` em `DatabasePrepareTestUtil`

Pre-requisito do item 2, e habilita assertiva de estado de banco no fim do
teste (hoje so da para afirmar sobre a UI). Provavelmente o item de maior
alcance alem da migracao.
