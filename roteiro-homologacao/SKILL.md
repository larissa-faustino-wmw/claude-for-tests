---
name: roteiro-homologacao
description: Monta o roteiro de homologação de um cliente ou de uma funcionalidade para um cliente no Lavendere e o cadastra como campanha de execução na pasta HOMOLOGAÇÕES do Squash TM — a partir da Test (agrupadora, tipo Other) ou da atividade de origem, levanta o escopo (Codings, Defects, critérios de aceite, branch e scripts), o histórico do cliente (homologações anteriores, bugs em produção, features com mais problema) e a configuração real da base do cliente, e organiza a campanha com uma iteração por atividade, a regressão básica (SMOKETEST) e a regressão do cliente. Use SEMPRE que o usuário pedir roteiro, plano ou campanha de homologação, homologar um cliente, um projeto, um go live ou uma funcionalidade para um cliente, ou mencionar agrupadora de cliente ou Test Other — mesmo que diga só "monta a homologação da Contabilista".
---

# Roteiro de homologação

Homologação no Lavendere é testar, **na base do próprio cliente**, o que foi feito para ele: um projeto (agrupadora com várias Codings e Defects, às vezes com branch própria) ou uma funcionalidade específica. O roteiro fica no Squash como uma **campanha na pasta HOMOLOGAÇÕES**; esta skill monta a campanha completa, com o que testar em cada atividade, a regressão básica e a regressão do que o cliente usa.

Nada é criado no Squash nem no Jira sem aprovação.

## Entrada

| O que o usuário traz | O que fazer |
|---|---|
| a Test agrupadora (`VENDAS-xxxxx`, tipo Test, Other) | usar como escopo |
| a atividade de origem e o cliente | procurar a agrupadora existente; não havendo, a homologação é de uma atividade só |
| só o cliente | procurar as Test abertas do cliente (`project = VENDAS AND issuetype = Test AND Customer = "<cliente>" AND resolution is EMPTY`) e perguntar qual |

**A agrupadora é criada pelo QA ou pelo PO.** Se ela ainda não existe e o tester quer, ofereça criar com a `criar-task-jira` (tipo Test, Other); se é o PO quem vai criar, monte o roteiro com as atividades informadas e deixe o vínculo para depois.

## Fluxo

### 1. Levantar o escopo

Detalhes em `references/levantamento.md`.

- **Itens da homologação:** as subtasks da agrupadora (Codings, Defects) e as atividades ligadas a ela; ou a atividade de origem. Para cada item: o que mudou (descrição, critérios de aceite), status (pronto para homologar ou não), Defects já abertos e os casos que já existem no Squash (requirement com a Reference = chave).
- **Código e ambiente:** nos comentários e na descrição, a branch do cliente (ex.: `politriz_9.053`), os projetos alterados, "POSSUI SCRIPT" e onde estão os scripts, a versão base.
- **Homologações anteriores do cliente:** as Test anteriores do mesmo cliente (agrupadoras de outras versões) e as campanhas dele na pasta HOMOLOGAÇÕES do Squash; o que ficou pendente ou falhou nelas.
- **Histórico do cliente em produção:** bugs com `Customer = "<cliente>"` nos últimos meses, agrupados por feature; os bugs dele corrigidos recentemente (precisam ser reconferidos na base dele).

### 2. Ler a configuração na base do cliente

A homologação usa a base do próprio cliente. A skill só **lê**, e nunca digita senha: detalhes em `references/levantamento.md` §Base do cliente.

- os parâmetros ligados (`TBLVPVALORPARAMETRO` no App; o equivalente da Web) que tocam as atividades do escopo;
- o que existe de massa para os cenários (empresas, representantes, tipos de pedido, tabelas de preço, clientes com a condição exigida).

Isso define os cenários **com a configuração real** do cliente, em vez de supor. Sem acesso à base, peça ao tester o resultado das consultas.

### 3. Impacto do código do cliente

Para agrupadora com branch própria, aplique a coleta da `analise-impacto` na branch do cliente (base `main`, commits com as chaves do escopo). Os side effects encontrados entram na regressão do cliente.

### 4. Montar o roteiro

Estrutura da campanha em `references/estrutura-squash.md`. Em resumo:

| Iteração | Conteúdo |
|---|---|
| `<TIME> - VENDAS-xxxxx - <título>` (uma por atividade do escopo) | os casos que já existem no requirement da atividade + os cenários de homologação na base do cliente (configuração real, massa do cliente) |
| `GERAL - Regressão básica` | os casos `SMOKETEST-…-APP` e `-WEB` (fluxo padrão de pedido, novo cliente, sincronização, logs, supervisor…) |
| `<CLIENTE> - Regressão do cliente` | o que o cliente usa e foi tocado: features dele com bug recente, bugs dele corrigidos recentemente, side effects da branch |

O TIME vem do módulo da Feature (Comercial = HYDRA; Comunicação, Contábil/Fiscal, CRM, Estoque, Financeiro e Inteligência de Vendas = SHIELD; Sistema = TERMINATOR, conforme os Manuais de Configuração).

Cenários novos (que não existem como caso no Squash) são gerados no padrão da `gerador-de-testcases` e vinculados ao requirement da atividade, para entrarem na iteração.

### 5. Apresentar para aprovação

Formato em `references/modelo-roteiro.md`: resumo da homologação (cliente, escopo, ambiente, branch, scripts), as iterações com os casos de cada uma (existentes e novos), os riscos, o que fica fora do escopo e, em go live, o checklist final. Feche com:

> Campanha: `HOMOLOGAÇÕES / <campanha>`, <n> iterações, <n> casos (<n> novos). Posso cadastrar no Squash?

### 6. Cadastrar no Squash

Pelo Chrome (a API do Squash só para ler), seguindo `references/estrutura-squash.md` §Cadastro: os casos novos primeiro (com a `gerador-de-testcases`), depois a campanha, as iterações e o plano de teste de cada uma. Devolva o link da campanha e de cada iteração.

Se a agrupadora existe no Jira, ofereça comentar nela o link da campanha.

## Armadilhas

- **Status no JQL vão em inglês:** "Aberto" = `Open`, "Em Andamento" = `In Progress`, "Fechado" = `Closed`. Com o nome em português, o Jira recusa a consulta.
- **Customer no JQL vai com o código:** `Customer = "Contabilista [2593]"`.
- **O que importa está nos comentários.** Branch do cliente, projetos alterados e "POSSUI SCRIPT" costumam estar nos comentários da agrupadora, não em campos.
- **"Não tem suporte" é fora do escopo.** A descrição da agrupadora às vezes diz o que a entrega não cobre: isso vai para "fora do escopo", não para cenário.
- **Subtasks da agrupadora são Coding e Defect**, muitas sem Feature e sem Customer: o TIME da iteração pode precisar ser perguntado.
- **Os casos SMOKETEST da Web têm "-Copy1" no nome**; procure pela Reference (`SMOKETEST-…-WEB`), não pelo nome.
- **Na iteração "GERAL - Regressão básica", a Reference é o cliente.**

## Cuidados

- **Só leitura na base do cliente.** Nenhum INSERT, UPDATE ou DELETE; nada de senha digitada pela skill.
- Dados do cliente (CNPJ, nomes de clientes dele, valores) ficam fora dos casos do Squash: use descrições ("cliente com limite de crédito bloqueado") e os códigos internos.
- Item do escopo que ainda não está pronto para homologar: liste à parte, não monte iteração vazia sem avisar.
- Não duplique campanha: se já existe campanha do cliente para a mesma entrega, proponha acrescentar iterações nela.
- Nada é criado sem aprovação.
