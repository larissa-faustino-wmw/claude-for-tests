# analise-impacto-delivery

Skill do Claude para a **semana de Delivery**: aponta os riscos da versão que nenhuma outra camada de teste enxerga, e calibra a regressão fixa contra os bugs reais.

## Por que existe

Na Delivery, cada atividade já foi testada sozinha na sua branch (e analisada com a `analise-impacto`), e a regressão fixa cobre os fluxos largos. O que sobra só aparece com **tudo junto na `release`**:

- duas atividades que mexem no mesmo arquivo ou método, testadas separadas e nunca juntas;
- commits sem atividade, que ninguém testou de propósito;
- correções feitas durante a Delivery, que só o reteste do Defect cobre;
- atividades que mudaram depois de liberadas pelo QA.

## Os dois modos

| Modo | Quando | Exemplo de pedido |
|---|---|---|
| **Versão** | depois que o facilitador incrementa a `develop` na `release`, e antes de liberar | "analisa os riscos da versão 9.070", "o que entrou na release sem atividade?" |
| **Calibração** | de tempos em tempos | "a regressão fixa está pegando os bugs?" |

## O que você recebe

**Modo versão:** o resumo do que entrou (commits e atividades por repositório), as divergências com o fixVersion do Jira e a tabela de riscos. Cada risco vem com a evidência (commit e arquivo) e com onde aprofundar o teste, além da regressão fixa.

**Modo calibração:** sugestões de casos a criar, detalhar ou enxugar nas pastas de regressão do Squash, cada uma com os bugs que a justificam, e um resumo da qualidade dos casos (sem resultado esperado, sem requirement, em andamento).

## Como compara

A base é sempre a **`main`** (a última versão liberada). O escopo da versão é `main..release`. Antes do incremento, é `main..develop`, conferindo o fixVersion, porque a `develop` pode já ter a sprint seguinte. A skill lê as branches remotas (`origin/...`) e não mexe no seu branch de trabalho.

## O que você precisa ter

- **Os repositórios clonados** em `projetos/` do workspace (`lavenderepda`, `lavendereweb`, `lavenderecore`).
- **MCP interno da WMW**: fixVersion, histórico de bugs.
- **Claude in Chrome** logado no Squash, para a calibração (leitura das pastas pela API do Squash).
- Rodar no **Claude Code**, dentro do workspace.

## Bom saber

- **Somente leitura.** Os casos sugeridos viram casos de verdade com a `gerador-de-testcases`.
- Não refaz a análise de cada atividade; isso é da `analise-impacto`.
- Poucos riscos bem fundamentados: o teste da Delivery tem prazo.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `SKILL.md` | o fluxo das branches e os passos dos modos versão e calibração |
| `references/rastreio-impacto.md` | como seguir uma alteração até o fluxo do usuário |
| `references/riscos.md` | matriz de risco e critério de automação |
| `references/calibracao.md` | a regressão fixa no Squash e como cruzar com os bugs |
| `references/modelo-saida.md` | o formato da entrega do modo versão |

## Instalação

Copie a pasta `analise-impacto-delivery/` inteira, com `references/`, em `~/.claude/skills/` ou em `.claude/skills/` do workspace. Precisa do Claude Code.
