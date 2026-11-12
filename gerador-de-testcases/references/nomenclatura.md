# Reference, prefixo e pasta

O identificador de cada cenário é o campo **Reference** do caso de teste no Squash TM. Quando esta skill fala em "ID", é a Reference.

## Formato

| Plataforma (Environment do Jira) | Formato | Exemplo |
|---|---|---|
| App | `<PREFIXO>-LVP-<nnn>` | `COMISSAO-LVP-014` |
| Web | `<PREFIXO>-LVW-<nnn>` | `COMISSAO-LVW-007` |

- `<nnn>` tem sempre 3 dígitos.
- Casos de backend (API, banco, sincronização) usam o mesmo LVP ou LVW da plataforma da atividade.
- O nome do caso (Name) vai sem a Reference; no chat, o título é `<Reference> – <Nome>`.

## Prefixo

O prefixo vem da **Feature** da atividade, conferida na árvore dos [Manuais de Configuração](https://confluence.wmw.com.br/confluence/pages/viewpage.action?pageId=1212592) (Módulo → Sub-módulo → Funcionalidade).

A Feature do Jira tem o formato `Módulo > Sub-módulo - Funcionalidade`. O prefixo é o **sub-módulo**, em maiúsculas, sem acento, com `_` no lugar de espaço:

| Feature no Jira | Prefixo |
|---|---|
| `Comercial > Comissão - Configuração` | `COMISSAO-` |
| `Contábil/Fiscal > Faturamento - NF-e` | `FATURAMENTO-` |
| `CRM > Agenda de Visitas - Agenda de Visitas` | `AGENDA_DE_VISITAS-` ou o prefixo que a pasta já usa |
| `CRM > Novo Cliente - Cadastro` | `NOVO_CLIENTE-` |
| `Comercial > Emissão de Pedidos - Venda` | o prefixo da pasta de Emissão de Pedidos no Squash |

**A pasta existente manda.** Se o Squash já tem uma pasta para o sub-módulo com outro prefixo (`AGENDA-` em vez de `AGENDA_DE_VISITAS-`, `ATIVIDADES-` para Atividades do Pedido), use o prefixo que a pasta já usa. Nunca crie um segundo prefixo para o mesmo assunto.

Feature vazia: proponha o prefixo a partir da descrição e da árvore, e confirme na rodada de dúvidas.

## Quando a Feature não descreve o cenário

A Feature diz onde a história foi feita, não necessariamente o que o cenário testa. Exemplo: uma Story de `Comercial > Emissão de Pedidos - Venda` cujo cenário valida a base de cálculo do imposto é, na prática, um teste de `Contábil/Fiscal > Tributação`.

Nesses casos:

1. proponha o prefixo e a pasta do assunto que o cenário testa de fato, procurando na árvore dos Manuais de Configuração;
2. explique o motivo em uma linha na rodada de dúvidas ou na aprovação;
3. se não existe pasta para esse assunto no Squash, proponha uma pasta nova (nome e local) e só crie com aprovação;
4. o tester decide. Se ele preferir manter tudo na pasta da Feature, siga.

## Numeração

1. No Squash, procure as References que começam com `<PREFIXO>-LVP-` (ou `-LVW-`) — busca por Reference, ou a lista da pasta ordenada por Reference.
2. Pegue o **maior número** usado, mesmo que haja buracos na sequência. Não reaproveite números vagos.
3. Os novos casos continuam do próximo número, na ordem da matriz.
4. LVP e LVW têm numerações independentes.
5. Logo antes de cadastrar, confira de novo: se alguém usou o número no meio tempo, renumere e avise.

Nunca comece em 001 sem ter consultado. Sem acesso ao Squash, use `<PREFIXO>-LVP-???` e diga que a numeração ficou pendente.

## Caso compartilhado

`PERSISTENCIA-001 - Validação de Persistência de Dados APP e Sincronização com a Web` ([Squash 3463](https://squash.wmw.com.br/squash/test-case-workspace/test-case/3463/steps)) é chamado (Call test case) pelos cenários do App que gravam dados, em vez de repetir os passos de salvar, sincronizar e conferir na Web.
