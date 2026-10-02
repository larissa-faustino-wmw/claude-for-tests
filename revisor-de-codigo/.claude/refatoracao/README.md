# Refatoracao da massa de teste -- painel por modulo

> Gerado por `python3 .claude/skills/migracao-massa-teste/scripts/massa.py plano`.
> Regenere apos cada teste migrado. Anotacoes no fim sao preservadas.

Migrar a massa de `<Teste>.sql` para `@InvokeInit` com `ParametrosTestUtil`
e `TabelasTestUtil`, **um modulo por vez**, comecando pelos de menor risco
para o processo amadurecer antes de encostar nos dificeis.

| Total | |
|---|---|
| `.sql` restantes | 208 |
| Statements | 2469 |
| Convertiveis automaticamente | 2433 (98.5%) |
| Exigem decisao humana | 36 |
| Testes ja migrados | 0 |

## Ordem sugerida

Ordenado por proporcao de bloqueios, depois por tamanho.

| Onda | Modulo | `.sql` | stmts | auto | bloq | migrados |
|---|---|---|---|---|---|---|
| 1 | [`agenda`](agenda/STATUS.md) | 9 | 0 | 0% | 0 | 0 |
| 1 | [`autorizacaoNegociacao`](autorizacaoNegociacao/STATUS.md) | 2 | 0 | 0% | 0 | 0 |
| 1 | [`boleto`](boleto/STATUS.md) | 1 | 0 | 0% | 0 | 0 |
| 1 | [`pesquisa`](pesquisa/STATUS.md) | 3 | 3 | 100% | 0 | 0 |
| 1 | [`descontoAcrescimo`](descontoAcrescimo/STATUS.md) | 8 | 36 | 100% | 0 | 0 |
| 2 | [`rentabilidade`](rentabilidade/STATUS.md) | 1 | 72 | 100% | 0 | 0 |
| 2 | [`pontuacao`](pontuacao/STATUS.md) | 7 | 105 | 100% | 0 | 0 |
| 2 | [`sugestao`](sugestao/STATUS.md) | 10 | 105 | 100% | 0 | 0 |
| 2 | [`verba`](verba/STATUS.md) | 19 | 131 | 100% | 0 | 0 |
| 2 | [`logistica`](logistica/STATUS.md) | 10 | 193 | 100% | 0 | 0 |
| 2 | [`grade`](grade/STATUS.md) | 6 | 322 | 100% | 0 | 0 |
| 2 | [`tributacao`](tributacao/STATUS.md) | 30 | 592 | 100% | 0 | 0 |
| 3 | [`estoque`](estoque/STATUS.md) | 35 | 342 | 99% | 3 | 0 |
| 3 | [`politica`](politica/STATUS.md) | 12 | 123 | 98% | 3 | 0 |
| 3 | [`cliente`](cliente/STATUS.md) | 15 | 118 | 97% | 3 | 0 |
| 3 | [`pedido`](pedido/STATUS.md) | 17 | 152 | 97% | 5 | 0 |
| 3 | [`nfe`](nfe/STATUS.md) | 3 | 66 | 95% | 3 | 0 |
| 3 | [`multiplaInsercao`](multiplaInsercao/STATUS.md) | 11 | 57 | 95% | 3 | 0 |
| 3 | [`financeiro`](financeiro/STATUS.md) | 1 | 16 | 94% | 1 | 0 |
| 3 | [`marcador`](marcador/STATUS.md) | 4 | 15 | 73% | 4 | 0 |
| 3 | [`pagamento`](pagamento/STATUS.md) | 4 | 21 | 48% | 11 | 0 |

Sem massa `.sql` (nada a migrar): `login`, `recados`.

## Causa raiz dos 36 bloqueios

| Causa | Qtd | Resolvivel na util? |
|---|---|---|
| delete() em TabelasTestUtil | 13 | sim |
| analise caso a caso | 10 | nao |
| expressao de data sem equivalente em DatasTestUtil | 6 | nao |
| DDL -- permanece no .sql (correto) | 4 | nao |
| blob hexadecimal | 2 | nao |
| whitelist PARAMETROS_JSON | 1 | sim |

**14 dos 36 bloqueios (39%) somem com mudanca nas utils** -- delete() em TabelasTestUtil, whitelist PARAMETROS_JSON.
A cobertura automatica passaria de 98.5% para 99.1%.

`DatasTestUtil` ja esta implementado -- as expressoes de data cobertas
por ele sao convertidas automaticamente e nao contam como bloqueio.

Por isso a **onda 0** existe: mexer nas utils primeiro e uma mudanca
pequena contra 14 ocorrencias. Fazer o contrario significa contornar
o mesmo problema 14 vezes a mao.

Modulos mais beneficiados: `pagamento` (9), `estoque` (2), `pedido` (2), `financeiro` (1).

**Onda 0** -- ajustar as utils. Ver
`../skills/migracao-massa-teste/referencias/proposta-melhorias-utils.md`.

**Onda 1** -- piloto. Poucos bloqueios: serve para validar o processo
ponta a ponta (incluindo fase A/B com o banco baixado) antes de escalar.

**Onda 2** -- volume. O processo ja esta calibrado; aqui esta a maior parte
do ganho. Vale rodar o subagente `migrador-massa` um teste por vez.

**Onda 3** -- o que sobra depois da onda 0. Se a onda 0 nao for feita, e
aqui que o trabalho manual se concentra.

> As ondas sao ordenadas pela proporcao de bloqueios **hoje**. Depois da
> onda 0, regenere este painel: varios modulos mudam de posicao.

## Fluxo por modulo

1. `/auditar-massa` -- panorama atualizado.
2. Abrir o `STATUS.md` do modulo e seguir a ordem sugerida.
3. Migrar:
   - `/migrar-teste <NomeDaClasseTest>` -- um teste, com validacao propria.
     Use no primeiro teste de cada modulo, para conferir o resultado.
   - `/migrar-modulo <modulo>` -- a fila inteira via subagente, um por vez,
     com validacao em lote no fim. Use depois que o primeiro deu certo.
4. Validar fase A (com `.sql`) e fase B (sem `.sql`). Sem fase B o teste
   pode estar passando por causa do `.sql`, nao da migracao.
5. Regenerar: `massa.py plano`.

<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->

## Anotacoes

Decisoes de escopo e pendencias para o time.
