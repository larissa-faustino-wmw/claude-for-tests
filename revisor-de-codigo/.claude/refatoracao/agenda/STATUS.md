# Refatoracao -- modulo `agenda`

> Gerado por `massa.py plano`. O estado e deduzido do repositorio
> (presenca de `.sql` e de `@InvokeInit`), entao nao envelhece.
> Regenere depois de cada teste migrado. Anotacoes manuais no fim do
> arquivo sao preservadas.

| | |
|---|---|
| Classes de teste | 9 |
| Arquivos `.sql` restantes | 9 |
| Statements | 0 |
| Convertiveis automaticamente | 0 (0%) |
| Exigem decisao humana | 0 |
| Migrados / em fase A | 0 / 9 |

## Ordem sugerida

Menor esforco primeiro. `bloq` = statements que exigem decisao.

| # | Estado | Teste | stmts | auto | bloq | enc |
|---|---|---|---|---|---|---|
| 1 | FASE A | `PositivarAgendaVisitaCadastradaBackofficeTest` | 0 | 0 | 0 | !! UTF-8 |
| 2 | FASE A | `CadastrarAgendaTest` | 0 | 0 | 0 | !! UTF-8 |
| 3 | FASE A | `ReagendarAgendaNaoExecutadaTest` | 0 | 0 | 0 | !! UTF-8 |
| 4 | FASE A | `ValidarAgendaRecorrente` | 0 | 0 | 0 | !! UTF-8 |
| 5 | FASE A | `EmitirPedidoComAgendasVencidasTest` | 0 | 0 | 0 | !! UTF-8 |
| 6 | FASE A | `ValidarFrequenciaDeAgendaTest` | 0 | 0 | 0 | !! UTF-8 |
| 7 | FASE A | `RegistrarSaidaClienteTest` | 0 | 0 | 0 | ok |
| 8 | FASE A | `RegistrarEntradaClienteTest` | 0 | 0 | 0 | ok |
| 9 | FASE A | `EmitirAntecipacaoAgendaVisitasTest` | 0 | 0 | 0 | !! UTF-8 |

## Como migrar

```
/migrar-teste <NomeDaClasseTest>   # um teste (comece pelo nº 1)
/migrar-modulo agenda              # a fila inteira, um por vez
```

Regras que valem sempre: ISO-8859-1, validacao em fase A e fase B, um
teste por vez. Detalhe em `../../skills/migracao-massa-teste/SKILL.md`.

<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->

## Anotacoes

Decisoes tomadas, duvidas para o time, defeitos encontrados no `.sql`
original. Este bloco sobrevive a regeneracao.

### 2026-08-06 -- migracao dos 9 testes (Joaquim + Claude)

Os 9 testes ganharam `@InvokeInit prepararMassaDeDados()`. Os `.sql` continuam
no lugar: **so a fase A esta feita no papel; nem a fase A nem a fase B foram
executadas**, porque o Maven nao roda nesta maquina (o parent POM
`br.com.wmw:super-pom-pda:5.009` so tem `.lastUpdated` no `~/.m2` e nao ha
`db/`). A validacao ficou com o time de teste.

O que foi verificado sem Maven: sintaxe Java dos 9 arquivos via `javac`
(so restam erros de resolucao de dependencia), encoding ISO-8859-1, e a
formula de `diaDaSemana()` conferida contra `STRFTIME('%w') + 1` do SQLite
nos 7 dias da semana.

**Onda 0 aplicada aqui.** Foi criado
`presentation/ui/base/DatasTestUtil.java` (item 4 da proposta de utils):
`hoje`, `hojeMais`, `hojeMenos`, `agora`, `hojeUi`, `diaDaSemana`. Ele
destrava os 4 bloqueios do modulo e vale para os ~120 do projeto.
`referencias/mapeamento-sql-java.md` foi atualizado para apontar para a util
em vez de `LocalDate` cru.

**Posicao do metodo.** `prepararMassaDeDados()` e o primeiro metodo de cada
uma das 9 classes, antes do `@Test`, seguindo o padrao de
`test/ct033/t001/ValidaDevolucaoTotalEstoqueRemessasLiberadasTest`. Onde a
classe ja tinha `populaAgendaVisita()`, os dois `@InvokeInit` ficaram
agrupados no topo. A regra foi escrita na `SKILL.md` (passo 4) e no agente
`migrador-massa`.

#### Defeitos encontrados nos `.sql` originais

- **`EmitirPedidoComAgendasVencidasTest.sql`** grava `VLPARAMETRO = 'N'` no
  parametro **1033**, que e JSON. O texto `N` substituia o objeto inteiro e
  destruia a estrutura do parametro. Na migracao virou
  `setParametro(1033, "usa", "N")`, que e a intencao provavel -- **confirmar
  com quem conhece o caso**.
- **`ValidarFrequenciaDeAgendaTest.sql`** tem toda a massa de
  `TBLVPAGENDAVISITA` **comentada** (5 INSERTs + 4 UPDATEs de `NUDIASEMANA`).
  Nao foi migrada. As agendas vem hoje de `AgendaUtil.populaAgendaVisita()`,
  entao o bloco comentado parece ser residuo -- vale apagar do `.sql`.

#### Mudancas de comportamento aceitas

- **Parametro JSON: substituicao -> patch.** Vale para o 140 (7 testes), o
  1033 (3 testes). As chaves nao citadas passam a vir do banco base em vez de
  serem zeradas. E o ganho pretendido pela refatoracao (armadilha 5), mas um
  teste que dependia de uma chave ausente muda de comportamento.
- **`NMENTIDADE` / `VLCHAVE` ignorados.** 8 dos 9 testes filtravam por
  `NMENTIDADE = 'TBWMWSISTEMA'` e `VLCHAVE = '[1]'`; `ParametrosTestUtil` so
  filtra `CDPARAMETRO`. Com uma linha por parametro no banco base o efeito e
  o mesmo, mas nao foi possivel confirmar sem o banco -- ver a query do item 3
  da proposta de utils.

#### Pendencias

- Rodar fase A e fase B (renomear `<Teste>.sql` para `.sql.bak`) -- **time de
  teste**. Enquanto o `.sql` estiver no lugar, um teste verde nao prova que o
  Java se basta.
- Confirmar a intencao do parametro 1033 em `EmitirPedidoComAgendasVencidasTest`.
- Decidir se o bloco comentado de `ValidarFrequenciaDeAgendaTest.sql` sai.
