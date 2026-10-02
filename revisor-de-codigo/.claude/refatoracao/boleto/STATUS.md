# Refatoracao -- modulo `boleto`

> Gerado por `massa.py plano`. O estado e deduzido do repositorio
> (presenca de `.sql` e de `@InvokeInit`), entao nao envelhece.
> Regenere depois de cada teste migrado. Anotacoes manuais no fim do
> arquivo sao preservadas.

| | |
|---|---|
| Classes de teste | 1 |
| Arquivos `.sql` restantes | 1 |
| Statements | 0 |
| Convertiveis automaticamente | 0 (0%) |
| Exigem decisao humana | 0 |
| Migrados / em fase A | 0 / 1 |

## Ordem sugerida

Menor esforco primeiro. `bloq` = statements que exigem decisao.

| # | Estado | Teste | stmts | auto | bloq | enc |
|---|---|---|---|---|---|---|
| 1 | FASE A | `EfetuarAplicacaoIndiceFinanceiroBoletoOfflineTest` | 0 | 0 | 0 | !! UTF-8 |

## Como migrar

```
/migrar-teste <NomeDaClasseTest>   # um teste (comece pelo nº 1)
/migrar-modulo boleto              # a fila inteira, um por vez
```

Regras que valem sempre: ISO-8859-1, validacao em fase A e fase B, um
teste por vez. Detalhe em `../../skills/migracao-massa-teste/SKILL.md`.

<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->

## Anotacoes

Decisoes tomadas, duvidas para o time, defeitos encontrados no `.sql`
original. Este bloco sobrevive a regeneracao.

### EfetuarAplicacaoIndiceFinanceiroBoletoOfflineTest (2026-08-06)

Criterio adotado: **o Java reproduz o `.sql` statement a statement, na mesma
ordem, sem suprimir repeticao**. A massa legada e o contrato conhecido do
cenario; remover statement porque "parece redundante" e mudanca de
comportamento disfarcada de limpeza, e so quem mantem o caso pode autorizar.

- DELETE da faixa resolvido com `DatabasePrepareTestUtil.executeUpdate`
  (sem `TabelasTestUtil.delete()`), preservando a ordem DELETE -> INSERT.
- `date/time('now','localtime')` -> `DatasTestUtil.hoje()/agora()`.
- Parametros 190 e 7 sao JSON e o `.sql` **substituia o objeto inteiro**.
  `ParametrosTestUtil.setParametro()` faz `json_set` (patch) e preservaria
  chaves do banco base -- comportamento diferente. Ficaram como
  `executeUpdate` com o UPDATE original, sem mudanca de semantica.
  Se isso virar padrao, vale um `ParametrosTestUtil.setParametroJson(cd, json)`.
- Parametro 1308 aparece duas vezes com o mesmo valor 'S' (statements 1 e 14):
  **reproduzido duas vezes**.
- TBLVPFAIXABOLETO tem dois INSERT com o mesmo rowkey '1;1;2;', diferindo em
  CDUSUARIO ('3897' e 'WMWROBOT') e na caixa da coluna ROWKEY/rowkey:
  **os dois reproduzidos**. Se a tabela tiver PK/unique, o segundo falha --
  no `.sql` isso passava batido por ser o ultimo statement do arquivo, mas em
  `@InvokeInit` vira excecao e derruba o teste. E o primeiro suspeito se a
  fase B quebrar. Perguntar a quem mantem o CT006-T004 se e engano de copia.
- Faixa com CDBOLETOCONFIG '1' e sem CDFAIXABOLETO parece resto de massa
  anterior a troca para a config '33.20'; mantida. Confirmar o proposito.

### Notas do modulo (2026-08-06)

- **Onda 0 dispensada, e o `massa.py` foi corrigido.** O plano acusava
  "helper de datas" como bloqueio mesmo com `DatasTestUtil` ja implementado.
  O conversor agora traduz as variantes cobertas
  (`DATE/TIME('now','localtime')`, `+/-N day`, `STRFTIME('%w',...)+1`) e elas
  deixaram de contar como bloqueio. Restou o `delete()`.
- **Ficam bloqueadas de proposito** as expressoes sem `'localtime'`
  (`DATE()`, `DATE('now')`): o SQLite responde em UTC e `DatasTestUtil` e
  local -- perto da meia-noite dao dias diferentes. Converter mudaria
  comportamento, entao o plano pede decisao humana.
- **Fases A e B nao executadas.** Nao ha `mvn` no PATH nem `mvnw` no projeto,
  e `db/` nao existe (banco base nunca baixado). Validacao pendente de ambiente.
- Enquanto a fase B nao rodar, o `.sql` continua no lugar -- nao apagar.
