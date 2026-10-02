---
description: Migra a massa de um teste do .sql para @InvokeInit (ParametrosTestUtil/TabelasTestUtil)
argument-hint: <caminho do .sql ou nome da classe de teste>
allowed-tools: Bash, Read, Edit, Write, Glob, Grep, Skill
---

Migre a massa de teste de: **$1**

Siga a skill `migracao-massa-teste` do inicio ao fim. Nao pule etapas.

Antes de comecar, resolva o alvo:

!`python3 .claude/skills/migracao-massa-teste/scripts/massa.py analisar "$1" 2>/dev/null || find src/test -iname "*$1*.sql"`

Entregue, nesta ordem:

1. **Diagnostico** -- quantos statements, quantos automaticos, quais bloqueios.
2. **Decisao por bloqueio** -- para cada um: converti assim / deixei como TODO
   porque X. Se um bloqueio revelar defeito no `.sql` original, destaque-o
   separadamente; nao conserte por conta propria.
3. **A alteracao** -- o `@InvokeInit` na classe de teste, em ISO-8859-1.
4. **Validacao** -- resultado da fase A (com `.sql`) e da fase B (sem `.sql`),
   com a saida real do Maven. Se nao conseguir rodar (banco ausente em
   `./db/`), diga isso explicitamente em vez de afirmar que passou.
5. **Pendencias** -- o que ficou fora e por que.
