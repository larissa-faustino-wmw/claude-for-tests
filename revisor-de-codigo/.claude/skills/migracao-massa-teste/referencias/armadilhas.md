# Armadilhas da migracao

Ordenadas por dano potencial. Todas foram observadas na massa atual do projeto.

---

## 1. Parametro JSON fora do whitelist -> corrompe o parametro em silencio

`ParametrosTestUtil.setParametro` decide o caminho pelo `Set PARAMETROS_JSON`:

```java
if (PARAMETROS_JSON.contains(cdParametro)) {
    patchJsonDb(cdParametro, chave, valor);   // json_set, preserva o resto
} else {
    updateSimples(cdParametro, valor);        // sobrescreve a coluna inteira
}
```

Se o parametro guarda JSON mas o codigo **nao esta no Set**, `setParametro` cai
em `updateSimples` e troca `{"usa":"S","exibeSaldoNegativo":"S"}` pelo texto
`S`. O parametro deixa de ser JSON. Nada acusa: nao ha excecao, nao ha log --
o teste passa a exercitar uma configuracao diferente da pretendida.

Pior: a sobrecarga de tres argumentos **descarta a chave silenciosamente**
nesse caminho (`// Se o tester tentar passar chave para parametro que nao e
JSON, seta normal`). Ou seja, `setParametro(923, "exibeSaldoNegativo", "S")`
grava `VLPARAMETRO = 'S'`.

**Caso real neste repositorio:** parametro **923**
(`ValidarSaldoVerbaNegativoTest`) grava
`'{ "usa":"S", "exibeSaldoNegativo":"S"}'` e nao consta em `PARAMETROS_JSON`.

**Antes de migrar:** adicione o codigo ao `Set` em `ParametrosTestUtil.java`.
O `massa.py` bloqueia a conversao nesse caso, de proposito.

> Melhoria estrutural: o whitelist e uma lista manual de 249 numeros que precisa
> ser mantida a mao. `patchJsonDb` ja tem o `CASE WHEN VLPARAMETRO LIKE '{%'`
> para detectar JSON em tempo de execucao -- o mesmo teste poderia decidir o
> caminho e tornar o `Set` desnecessario. Ver `proposta-melhorias-utils.md`.

---

## 2. `NMENTIDADE` / `VLCHAVE` ignorados -> escopo maior que o pretendido

**533 dos statements de parametro** filtram por entidade:

```sql
UPDATE TBLVPVALORPARAMETRO SET VLPARAMETRO='...'
WHERE CDSISTEMA=1 AND CDPARAMETRO=220
  AND NMENTIDADE='TBWMWSISTEMA' AND VLCHAVE='[1]';
```

`ParametrosTestUtil` filtra **somente** `CDPARAMETRO`. Se a tabela tiver mais de
uma linha para o mesmo parametro (escopo por sistema, empresa ou representante),
a migracao passa a atualizar todas.

Na pratica, com o banco base padrao, quase sempre existe uma linha so e o
resultado e identico -- por isso a fase A/B de validacao existe. Mas o
comportamento **nao e equivalente**, e o `massa.py` avisa em cada ocorrencia.

Se um teste depender do escopo, ele precisa de uma sobrecarga nova
(`setParametro(cd, entidade, chave, valor, vlChave)`) ou de
`DatabasePrepareTestUtil.executeUpdate` direto. Nao force o encaixe.

---

## 3. `null` virando a String `"null"`

Ver `mapeamento-sql-java.md`. Sempre `null` (literal Java), nunca `"null"`.

---

## 4. Numero com aspas / texto sem aspas

`formatarValor()` so omite as aspas para `instanceof Number`. Trocar
`"1"` por `1` em `CDEMPRESA` muda o valor gravado de `'1'` para `1`. Em SQLite,
com afinidade de coluna TEXT, `1` e `'1'` podem comparar diferente. Preserve o
que estava no `.sql`.

---

## 5. Semantica do JSON muda: substituicao -> patch

O `.sql` gravava o objeto **inteiro**; `setParametro` faz `json_set` de **uma
chave**. As chaves nao mencionadas deixam de ser resetadas e passam a vir do
banco base.

Isso e o ganho da refatoracao (o teste para de quebrar quando o parametro ganha
chave nova), mas e uma mudanca de comportamento: um teste que dependia de uma
chave estar ausente/no default agora depende do banco. Quando a chave importa
para o cenario, **declare-a explicitamente**, mesmo que o `.sql` nao declarasse.

---

## 6. O `.sql` continua rodando durante a migracao

`invokeFileSql()` (`order = -1000`) roda antes do `@InvokeInit` da classe.
Se o `.sql` nao for removido, o teste passa mesmo com a migracao incompleta.
E util na fase A e enganoso se a fase B for pulada. Sempre rode a fase B.

---

## 7. Statement quebrado no `.sql` original

O `.sql` nao e compilado nem validado por ninguem. Erro de digitacao vive ali
por anos.

**Caso real:**
`estoque/produtoFalta/ValidarBloqueioProdutoSemEstoqueUnidadeAlternativaGridFaltaTest.sql`

```sql
UPDATE TBLVPVALORPARAMETRO SET VLPARAMEEMA=1 ANTRO='1;3;168;11;6;7;4;41;13;'
WHERE CDSISTD CDPARAMETRO=220 AND NMENTIDADE='TBWMWSISTEMA' AND VLCHAVE='[1]';
```

Um recorte de texto embaralhou `VLPARAMETRO=` com `CDSISTEMA=1 AND`. O statement
e invalido; o parametro 220 **nunca foi configurado** nesse teste. O teste passa
por outro motivo.

Ao encontrar algo assim: **reporte, nao adivinhe**. A intencao provavel
(`VLPARAMETRO='1;3;168;11;6;7;4;41;13;'` para o parametro 220) precisa ser
confirmada por quem conhece o caso de teste antes de virar codigo.

Esse tipo de defeito e o argumento mais forte da migracao: em Java o compilador
e o `massa.py` acusam na hora.

---

## 8. Encoding

Coberto na SKILL.md. Resumo operacional:

- ler com `iconv -f ISO-8859-1 -t UTF-8`;
- escrever com `encoding="iso-8859-1"`;
- se o hook bloquear por U+FFFD, restaurar da copia `.orig` e refazer;
- 4 `.sql` do projeto **ja** derivaram para UTF-8 (`massa.py encoding` lista).
