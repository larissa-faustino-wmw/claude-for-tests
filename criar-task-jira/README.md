# criar-task-jira

Skill do Claude que **monta e cria atividades no Jira da WMW** (`jira2.wmw.com.br`) a partir do relato do tester, seguindo os guias do time de QA. Ela pergunta o que falta, mostra o título e a descrição para você aprovar, cria a atividade no Jira pelo Chrome e devolve o link.

Substitui a antiga `gerador-de-subtask-bug-jira`, que só montava o texto de Defects para copiar e colar.

## Para que serve

- **Cria seis tipos de atividade**, cada um com as regras do seu guia:

  | Tipo | Quando | Guia |
  |---|---|---|
  | Defect | bug encontrado testando uma Story ou um Bug (subtask) | [GUIA-JIRA-002](https://confluence.wmw.com.br/confluence/x/AgA-QQ) |
  | Bug | bug interno encontrado pelo time de testes, sem atividade pai | [GUIA-JIRA-001](https://confluence.wmw.com.br/confluence/x/EADdQQ) |
  | Testing | subtask de teste quando o QA vai testar uma Story ou um Bug | regras do time (abaixo) |
  | Test | teste de versão (**Delivery**) ou homologação de cliente ou funcionalidade (**Other**) | regras do time (abaixo) |
  | Suggestion | melhoria ou ideia para o sistema | [Guia de sugestões](https://confluence.wmw.com.br/confluence/x/MYDxOw) |
  | Test Automated | cenário de teste automatizado | [GUIA-JIRA-003](https://confluence.wmw.com.br/confluence/x/GwDdQQ) |

  Você também pode pedir outro tipo (Story, Task, Ajustes Doc…). A skill monta com base no que você passar e no que esse tipo precisa, e deixa a conferência final com você.

- **Tira todas as dúvidas de uma vez**, antes de escrever. Só pergunta o que muda o conteúdo (develop, Phase, ambiente, massa, resultado esperado). Campos com regra fixa no guia ela preenche sozinha.
- **Não cria nada sem a sua aprovação.** Você vê título, descrição e campos antes.
- **Não duplica**: antes de criar qualquer atividade, inclusive subtask, busca no Jira por palavras-chave do problema ou do tema, e conta o que encontrou. Se já existe, não cria e sugere comentar na existente; se é parecida, propõe vincular.
- **Formata a descrição no padrão do time**: títulos de seção em Heading 2, citações em Paragraph quote, logs em bloco de código, comparativos em tabela.

## Quando usar

A skill entra sozinha quando você pede para abrir, criar, registrar, montar ou revisar uma atividade no Jira. Por exemplo:

- "vamos abrir esse bug", "monta o defect", "preciso reportar isso";
- "abre a testing da VENDAS-25199";
- "cria a atividade de automação desse cenário";
- "quero sugerir uma melhoria na tela de clientes";
- "essa atividade está completa?";
- ou quando você só cola um relato, prints, um log ou uma anotação.

Para chamar direto: `/criar-task-jira`.

## O que você precisa ter

- **Claude in Chrome**: a extensão instalada e conectada, com o Jira (`jira2.wmw.com.br`) liberado nas permissões de site.
- **Estar logado no Jira** nesse Chrome. A skill nunca digita senha: se cair na tela de login, ela pede para você entrar.
- **Opcional:** o MCP interno da WMW (leitura de Jira e Confluence). Com ele, a skill lê a atividade pai e procura duplicidade sem abrir o navegador.

Sem o Chrome conectado, a skill entrega o título, a descrição (pronta para colar no modo Text do Jira) e os campos para você criar na mão.

## Como usar

1. **Peça a atividade** e cole o relato como estiver, com prints e logs. Se for subtask (Defect ou Testing), informe a chave da atividade pai.
2. **Confirme o tipo.** A skill sempre pergunta, mesmo quando o relato deixa claro.
3. **Responda à rodada de dúvidas.** "Não sei" e "não se aplica" valem.
4. **Aprove** título, descrição e campos, ou peça ajustes.
5. **Acompanhe a criação** no Chrome: a skill abre uma aba nova, preenche, confere e cria.
6. **Confira pelo link** que ela devolve e complete o que ficou com você: prints que só estavam no chat, o link da carga no lugar de `< anexar carga >`.

Exemplos de pedido:

```
Abre um defect na VENDAS-25526: os totalizadores não batem depois de aplicar o cashback.
Valor do pedido 4800,00, cupom de 7777,77... [prints anexos]

Cria a testing da VENDAS-25199 pra mim.

Quero abrir uma sugestão: a lista de clientes poderia filtrar por cidade.

Cria a atividade de automação do cenário de tributação personalizada com FECOP tipo 2.
```

Com vários itens de uma vez (por exemplo, três bugs), a skill faz uma rodada de dúvidas, uma aprovação com tudo numerado e cria uma atividade por item.

## Padrões que a skill segue

**Título:** texto puro, sem caracteres especiais, no formato `Nome da tela - Descrição curta do problema`. Exemplo: `Novo cliente - Falha ao salvar cadastro com CNPJ duplicado`. A Testing tem título fixo: `Testing - <título da atividade pai>`.

**Descrição:**

| Conteúdo | Formato no Jira |
|---|---|
| Título de seção | Heading 2 |
| Texto | Paragraph |
| Citação do erro ou de documentação | Paragraph quote |
| Código ou log | bloco de código (Other → Code) |
| Comparativo ou dados de tabela | tabela (Other → Table) |
| Separação | Horizontal ruler |
| Pedido de ação a alguém | User mention (`@usuário`) |

**Testing:** atribuída ao QA que vai testar (normalmente quem está logado) e movida para **Em Andamento** logo depois de criada.

**Test:** Delivery tem o título `Versão <versão> de <dd/mm/aaaa>` e a descrição com facilitador(a), branch e métricas (`[DiasEstimados:…]`, `[NrTesters:…]`…), como nas versões anteriores. Other (homologação) leva o cliente no Customer e no título.

## Bom saber

- **Phase e SDLC phase são campos diferentes.** Phase é *como* você achou (manual ou automatizado). SDLC phase é *em que etapa* (Development, Delivery, Homologation, Production).
- **Bug com Phase "Automated testing" é sempre Priority Highest** (GUIA-JIRA-001).
- **Develop:** o Defect pede verificar se o problema também ocorre na develop. Na homologação de uma versão que ainda não chegou na develop, a skill não pergunta e registra isso na descrição.
- **Sugestão de cliente** não é Suggestion: segue o Processo de Orçamentos. E é **uma sugestão por tema**.
- **Test Automated:** Component/s e Fix Version/s ficam em branco na criação. Se você não tiver as horas orçadas, a skill pode calcular com `orcamento-modelo-antigo` ou `orcamento-refatoracao`.
- **Dados sensíveis** (CPF, CNPJ, e-mail, telefone, senha) em prints e logs: a skill avisa para ocultar antes de anexar.
- **Testing x Test:** Testing é a subtask de teste de uma Story ou de um Bug; Test é uma atividade solta, para o teste da versão (Delivery) ou para homologação (Other).
- Para descobrir por que um teste automatizado falhou antes de abrir o bug, use a skill `analise-logs-jenkins`.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `SKILL.md` | o fluxo: tipo, contexto, dúvidas, aprovação, criação e link |
| `references/defect.md` | Defect: verificações, campos, modelo de descrição e exemplo completo |
| `references/bug.md` | Bug interno: diferenças em relação ao Defect |
| `references/testing.md` | Testing: título, assign e Em Andamento |
| `references/test.md` | Test: Delivery (versão) e Other (homologação) |
| `references/suggestion.md` | Suggestion: verificações do guia, campos e modelo |
| `references/test-automated.md` | Test Automated: campos, labels da PQA-JIRA-000 e modelo |
| `references/formatacao-jira.md` | como produzir cada formato da descrição (Heading 2, quote, código, tabela) e os erros comuns |
| `references/criacao-chrome.md` | o passo a passo no navegador: login, tela de criação, preenchimento, conferência |

Os guias foram conferidos em 10/11/2026 (GUIA-JIRA-001 v4, GUIA-JIRA-002 v12, GUIA-JIRA-003 v1, Guia de sugestões v2, PQA-JIRA-000 v13). Se um guia mudar, atualize a referência do tipo. Dúvidas sobre os padrões: Larissa Faustino, responsável pelos guias.

## Instalação

Copie a pasta `criar-task-jira/` inteira, com a subpasta `references/`:

- **Claude Code**: em `~/.claude/skills/`, ou em `.claude/skills/` do projeto;
- **claude.ai**: suba a pasta como skill nas configurações de Skills.

Se você tinha a `gerador-de-subtask-bug-jira`, remova-a para as duas não disputarem os mesmos pedidos.
