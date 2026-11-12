# analise-impacto

Skill do Claude que **encontra os side effects de uma alteração**: o que mais a atividade pode ter quebrado, além do que ela prometeu entregar. Ela lê o código alterado na branch da atividade, descobre quem mais usa esse código, confere o que já está coberto (casos da atividade, testes automatizados, regressão fixa) e devolve uma lista curta de side effects com risco, evidência e recomendação.

## Por que existe

O teste de uma versão hoje tem duas camadas:

- **Regressão fixa** (pastas `00. Testes de Regressão App` e `Web` no Squash): ampla, igual em toda versão, sem saber o que mudou.
- **Reteste das atividades** (sprint → requirements → casos): testa o que cada atividade entregou.

O side effect cai no meio: uma área que a atividade não pretendia mexer e que usa o código alterado. A skill traz essa análise para **o momento em que o QA pega a atividade**, para que o side effect vire caso de teste (e automação, quando vale) antes da Delivery.

## Quando usar

Ao pegar uma Story ou um Bug pronto na branch, ou no reteste de um Bug. Por exemplo: "analisa o impacto da VENDAS-25526", "o que mais essa correção pode quebrar?".

Na semana de Delivery, para os riscos da versão inteira (atividades que mexem nos mesmos arquivos, commits sem atividade, correções da Delivery) e para revisar a regressão fixa, use a **`analise-impacto-delivery`**.

## O que você recebe

- a mudança em uma frase e o código analisado (repositório, branch, commits);
- o **mapa de impacto**: alteração → onde mais é usada → fluxo do usuário;
- os **side effects**, em ordem de risco, cada um com a **evidência** (arquivo e método), a cobertura atual e a recomendação: **automatizar**, **virar caso**, **regressão fixa basta** ou **perguntar ao dev**;
- as perguntas ao dev quando o código não deixa claro.

No fim, ela oferece gerar os casos aprovados com a `gerador-de-testcases`, que os coloca no requirement da atividade e na sprint.

## O que você precisa ter

- **Os repositórios clonados** em `projetos/` do workspace: `lavenderepda`, `lavendereweb` e `lavenderecore`, no mínimo. A skill lê as branches remotas (`origin/...`) e **não mexe no seu branch de trabalho**.
- **MCP interno da WMW**: lê a atividade e o histórico de bugs da área.
- **Claude in Chrome** com você logado no Squash: para ler os casos da atividade e da regressão fixa pela API do Squash (só leitura).
- Rodar no **Claude Code**, dentro do workspace (a skill usa git e busca no código).

## Como a skill decide o risco

**Probabilidade** (quão direto o fluxo usa o código alterado) × **impacto** (valor financeiro ou fiscal, sincronização, fluxo diário, visual). O risco sobe quando a feature tem histórico de Defects, correções que voltaram, outra atividade aberta nas mesmas classes, ou quando só App ou só Web foi alterado numa regra que existe nos dois.

**Automatizar** quando é cálculo, sincronização, área com histórico de bug ou fluxo diário. **Fica manual** quando é visual, raro, depende de integração externa ou o TotalUiTest não suporta o componente.

## Bom saber

- **Somente leitura.** Não cria casos, não altera código, não commita.
- **Sem evidência, não é achado:** o que o código não sustenta vira pergunta ao dev.
- Poucos side effects bem fundamentados valem mais que uma lista longa: a skill limita a cerca de 8 e agrupa os de risco baixo.
- A regressão fixa conta como cobertura só do fluxo largo: o caso "Tributação" não cobre uma regra específica de FECOP.
- Branch não encontrada: a skill procura os commits pela chave na `develop` e, se não achar, pergunta.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `SKILL.md` | o fluxo da análise |
| `references/coleta-diff.md` | como achar a branch e ler o diff sem mexer no seu repositório |
| `references/rastreio-impacto.md` | como seguir cada tipo de alteração até o usuário; a outra stack; Squash; histórico do Jira |
| `references/riscos.md` | matriz de risco e critério de automação |
| `references/modelo-saida.md` | o formato da entrega |

## Instalação

Copie a pasta `analise-impacto/` inteira, com a subpasta `references/`, em `~/.claude/skills/` ou em `.claude/skills/` do workspace. Precisa do Claude Code (não funciona só no claude.ai, porque lê os repositórios).
