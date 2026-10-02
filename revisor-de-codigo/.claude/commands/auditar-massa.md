---
description: Inventario da massa .sql restante, ranqueada por esforco de migracao
allowed-tools: Bash, Read, Grep
---

Painel por modulo (regenera `.claude/refatoracao/`):

!`python3 .claude/skills/migracao-massa-teste/scripts/massa.py plano`

Inventario por arquivo:

!`python3 .claude/skills/migracao-massa-teste/scripts/massa.py inventario`

Verificacao de encoding:

!`python3 .claude/skills/migracao-massa-teste/scripts/massa.py encoding`

Com base nisso, produza um relatorio curto:

- **Progresso** -- quantos testes ja usam `@InvokeInit` vs quantos ainda tem
  `.sql` (compare com `grep -rl "@InvokeInit" src/test`).
- **Proxima onda** -- os 10 arquivos que eu deveria migrar em seguida, com
  justificativa de ordem (esforco baixo primeiro; agrupe por diretorio para
  aproveitar contexto).
- **Bloqueios sistemicos** -- use a tabela de causa raiz do painel. Diga
  quantos bloqueios somem com cada mudanca nas utils e se compensa fazer a
  onda 0 antes de continuar migrando.
  Consulte `referencias/proposta-melhorias-utils.md`.
- **Riscos** -- arquivos com encoding errado, statements quebrados, parametros
  JSON fora do whitelist.

Nao migre nada neste comando. Isso e leitura e planejamento.
