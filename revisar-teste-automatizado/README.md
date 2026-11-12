# revisar-teste-automatizado

Skill do Claude, mais um **agente**, que **revisa um teste automatizado** do App (`totaluitest`) ou da Web (`webuitest`) em **contexto isolado**: quem revisa não é quem escreveu. O resultado é um parecer com severidade e status, como no code review dos devs.

## A pergunta da revisão

O teste prova o que o caso do Squash diz, de um jeito que **falha quando o sistema quebra** e **passa quando ele está certo**? Um teste que passa sempre é pior que nenhum, porque dá a falsa certeza.

## O que ela confere

1. **Caso × código:** cada passo e cada resultado esperado do Squash tem o passo e a asserção no código, com o valor.
2. **Falso positivo:** `return`, `if` ou `try/catch` que deixa verde sem testar; asserção de uma variável com ela mesma.
3. **Asserções:** fortes e com o valor concreto (`assertEquals` no App, as asserções do Playwright na Web).
4. **Esperas:** nada de `sleep`; `waitOpening`/`waitValue` no App, iframe e resposta na Web.
5. **Massa:** bate com o caso, é da própria classe, datas dinâmicas, parâmetro JSON na lista certa, limpeza na Web.
6. **Padrão:** JavaDoc com Squash e Jira, comentários de passo, nomes, Pages, encoding.
7. **Escopo:** nada alterado no código de produção.

E **roda o teste três vezes seguidas**, para ver se é estável. Sem ambiente para rodar, não aprova às cegas: o melhor status possível fica "aprovado com observações", com a pendência escrita.

## Status

| Status | Quando |
|---|---|
| APROVADO | nenhum crítico, alto nem médio; passou nas três rodadas |
| APROVADO COM OBSERVAÇÕES | nenhum crítico nem alto; médios poucos, ou não deu para rodar |
| MUDANÇAS SOLICITADAS | algum crítico ou alto |

O parecer fica em `projetos/<repo>/target/revisao-teste/<Classe>-review.md`, fora do git.

## Quando usar

- "revisa o teste da VENDAS-25597";
- "confere o ValidarIbsCbsPedidoMistoComESemIcmsStTest";
- ao fim da `totaluitest-codigo` ou da `webuitest-codigo`, antes de fechar a Test Automated.

## Como usar

**No Claude Code, pelo agente:** peça "revisa o teste X com o revisor". A sessão principal chama o agente `revisor-teste-automatizado`, que revisa num contexto limpo e devolve o status. Depois, a sessão principal oferece comentar o resumo na Test Automated e seguir para a `fechar-test-automated`.

**Sem agente (Codex, ChatGPT ou claude.ai):** abra uma **conversa nova** só para a revisão e chame a skill. O importante é não revisar na mesma conversa em que o teste foi escrito.

## Bom saber

- **A revisão não corrige.** Aponta onde, o quê, por que importa e a correção sugerida. Quem escreveu corrige e pede nova revisão.
- **CRÍTICO e ALTO vêm sempre confirmados**, com o trecho que prova ou a rodada que falhou.
- **Não deixa nada alterado:** a prova de que o teste pode falhar é feita numa cópia temporária.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `SKILL.md` | o fluxo: reunir, conferir, rodar, classificar e o parecer |
| `references/checklist.md` | o checklist completo, App e Web |
| `references/parecer.md` | o modelo do parecer |
| `agents/revisor-teste-automatizado.md` | o agente que roda a revisão em contexto isolado |

## Instalação

- **A skill:** copie a pasta `revisar-teste-automatizado/` para `~/.claude/skills/` ou `.claude/skills/` do workspace.
- **O agente:** copie `agents/revisor-teste-automatizado.md` para `~/.claude/agents/` ou `.claude/agents/` do workspace. Ele só funciona no Claude Code.
- Precisa também das skills `totaluitest-codigo` e `webuitest-codigo`, que são a régua da revisão.
