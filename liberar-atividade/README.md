# liberar-atividade

Skill do Claude para o **último passo do tester numa atividade**: confere se o teste está completo, e então libera (ou devolve ao dev) com um comentário de resumo, fecha a Testing e sugere o que automatizar.

## Por que existe

Depois da liberação do QA, o dev incrementa a branch na `develop`. O que é liberado com pendência escondida (um caso não executado, um Defect sem destino, um commit feito depois do teste) só aparece na Delivery. A skill confere antes.

## O que ela confere

| Conferência | Para liberar |
|---|---|
| Casos executados | todos os casos do requirement da atividade com resultado no Squash: passou, ou não testável com motivo |
| Evidência | cada execução com comentário ou anexo |
| Defects | resolvidos e retestados, ou com destino decidido (aceito, outra atividade, legado) |
| Side effects | os da `analise-impacto` viraram caso e foram executados |
| Reteste | nenhum commit da atividade depois da última execução |
| Testing | atribuída e com horas lançadas |

## O que ela faz

1. Mostra as conferências (ok, pendente, não se aplica) e propõe: **liberar**, **liberar com ressalva** (pendência que você aceita, escrita no comentário) ou **devolver ao dev**.
2. Monta o comentário de resumo: ambiente, casos e placar, Defects, side effects e ressalvas, ou, na devolução, o que precisa ser feito.
3. Com o seu ok, comenta na atividade, fecha a Testing (liberada) e move a atividade. Na primeira vez, ela lê as transições na tela e pergunta qual o time usa.
4. Lista os casos que valem automatizar e oferece criar as Test Automated que você escolher.

## Quando usar

- "libera a VENDAS-25526";
- "a VENDAS-25321 pode ser liberada?";
- "devolve a VENDAS-24543 para o dev".

Para chamar direto: `/liberar-atividade`.

## O que você precisa ter

- **MCP interno da WMW** (atividade, subtasks, Defects).
- **Claude in Chrome** logado no Squash (ler as execuções) e no Jira (comentar e mover).
- **Os repositórios** em `projetos/`, para conferir se houve commit depois do teste. Sem eles, essa conferência fica como "não verificada".

## Bom saber

- **Quem decide é você.** A skill não libera com pendência que você não aceitou.
- Ela **não lança horas** (oferece o texto do worklog) e **não fecha Defect**.
- "Fechado" no Jira não basta: ela confere que a resolução ficou "Concluída", porque existem Testings fechadas sem resolução.

## Onde entra no fluxo do tester

`criar-task-jira` (Testing) → `analise-impacto` → `gerador-de-testcases` → `executar-testes` → `criar-task-jira` (Defects) → reteste → **`liberar-atividade`** → (candidatos) `prioriza-automacao` / `criar-task-jira` (Test Automated).

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `SKILL.md` | o fluxo: ler, conferir, decidir, comentar, aplicar e candidatos à automação |
| `references/conferencias.md` | as consultas no Jira, no Squash e no git |
| `references/modelos.md` | os comentários de liberada, liberada com ressalva e devolvida |

## Instalação

Copie a pasta `liberar-atividade/` inteira, com `references/`, em `~/.claude/skills/` ou em `.claude/skills/` do workspace.
