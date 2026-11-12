# roteiro-homologacao

Skill do Claude que **monta o roteiro de homologação de um cliente** e o cadastra como **campanha na pasta HOMOLOGAÇÕES do Squash**. Vale para os dois formatos que o time usa: o projeto do cliente (agrupadora com várias Codings e Defects, às vezes com branch própria) e a funcionalidade específica para um cliente.

## Para que serve

- **Levanta o escopo:** as atividades da agrupadora (ou a atividade de origem), com critérios, Defects, casos que já existem, branch e scripts.
- **Usa o histórico do cliente:** homologações anteriores (no Jira e no Squash), bugs dele em produção, features em que ele mais tem problema e bugs dele corrigidos recentemente.
- **Lê a configuração real na base do cliente** (só leitura): os parâmetros ligados e a massa disponível, para os cenários refletirem como o cliente usa o sistema.
- **Monta a campanha no padrão do time:** uma iteração por atividade (`<TIME> - VENDAS-xxxxx - <título>`), a `GERAL - Regressão básica` com os casos SMOKETEST, e uma regressão do cliente.
- **Cadastra no Squash** depois da sua aprovação, criando antes os casos novos (pela `gerador-de-testcases`).

## Quando usar

- "monta a homologação da Contabilista";
- "roteiro de homologação da VENDAS-25439";
- "preciso homologar a VENDAS-19174 para a Braile";
- "prepara o go live da Politriz".

Para chamar direto: `/roteiro-homologacao`.

## O que você precisa ter

- **MCP interno da WMW** (agrupadora, atividades, bugs do cliente).
- **Claude in Chrome** logado no Squash (leitura pela API e cadastro pela tela).
- **Acesso à base do cliente**: se a skill não tiver conexão configurada, ela te entrega as consultas (só SELECT) para você rodar e colar o resultado. Ela nunca digita senha.
- Para agrupadora com branch própria: os repositórios em `projetos/` (a análise de impacto da branch).

## A agrupadora

É criada pelo **QA ou pelo PO**. Se ainda não existe, a skill pode criar com a `criar-task-jira` (Test, tipo Other) quando você pedir; se o PO vai criar, ela monta o roteiro com as atividades que você informar.

## O que você recebe

O resumo da homologação (cliente, agrupadora, base, branch, scripts, homologações anteriores), a configuração do cliente que importa, as iterações com os casos existentes e novos de cada uma, o que fica fora do escopo, os riscos e, em go live, um checklist final. Você aprova, e ela cadastra e devolve o link da campanha e de cada iteração.

## Bom saber

- **Só leitura na base do cliente**, e dados do cliente (CNPJ, nomes, contatos) não vão para o Squash: os casos usam descrições e códigos internos.
- Se já existe campanha do cliente para a mesma entrega, a skill propõe acrescentar iterações em vez de criar outra.
- O TIME do nome da iteração vem do módulo da Feature: Comercial = HYDRA; Comunicação, Contábil/Fiscal, CRM, Estoque, Financeiro e Inteligência de Vendas = SHIELD; Sistema = TERMINATOR.
- A skill não atribui nem executa os casos; isso fica com o time.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `SKILL.md` | o fluxo: escopo, base do cliente, impacto, roteiro, aprovação e cadastro |
| `references/levantamento.md` | as consultas no Jira, no Squash e na base do cliente |
| `references/estrutura-squash.md` | a pasta HOMOLOGAÇÕES, o padrão de campanha e iterações, e o cadastro |
| `references/modelo-roteiro.md` | o formato do roteiro para aprovação |

## Instalação

Copie a pasta `roteiro-homologacao/` inteira, com `references/`, em `~/.claude/skills/` ou em `.claude/skills/` do workspace.
