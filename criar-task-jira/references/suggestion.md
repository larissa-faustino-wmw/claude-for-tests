# Suggestion — sugestão de melhoria

**Guia:** [Guia - Como abrir sugestões no Jira](https://confluence.wmw.com.br/confluence/x/MYDxOw) (conferido na versão 2, em 10/11/2026). Se o guia mudar, atualize este arquivo.

Criação: botão **Create** → Project do sistema da sugestão → Issue Type `Suggestion`.

Depois de criada, a sugestão entra no Fluxo de Sugestões e passa por triagem. Sugestão sem os dados mínimos é bloqueada e devolvida ao Reporter — por isso a descrição precisa vir completa.

## Verificações antes de abrir (do guia)

1. **Buscar no Jira** por palavras-chave da sugestão: ela pode já existir ou já ter recebido retorno. Com acesso ao Jira, faça a busca (`text ~ "<palavras>"`) e mostre o que encontrou.
2. **Buscar no Confluence** pelo mesmo motivo (com o MCP interno, `search_knowledge_base`).
3. **É do sistema como um todo, de um cliente ou uma exceção?**
   - De cliente: segue o Processo de Orçamentos, não Suggestion. Avise e não crie.
   - Exceção: avalie com o tester se vale seguir, porque aumenta o código, a complexidade e a manutenção.
4. **Conversar com o time** para validar a sugestão. Pergunte se já foi conversado; se não, lembre em uma linha e deixe a decisão com o tester.

**Uma sugestão por tema**: cada tema pode ir para um time diferente. Se o relato tiver mais de um tema, proponha separar.

## O que perguntar (só o que faltar)

- **Projeto** (sistema da sugestão), se não estiver claro.
- **Justificativa**: a dor do usuário ou do cliente, se o relato só traz a ideia.
- **Configurações atuais**: quais funcionalidades envolvem a sugestão.
- **Impacto no sistema**: as perguntas da seção "Impacto no Sistema" que o relato não responde.
- **Customer**, quando a sugestão veio de um cliente.

## Campos

| # | Campo | Valor | Perguntar? |
|---|---|---|---|
| 1 | Summary | tema ou propósito da sugestão, no padrão `Tela - descrição curta` | não |
| 2 | Description | modelo abaixo | — |
| 3 | Customer | `WMW` para sugestão interna; o cliente, quando veio dele | só se veio de cliente e não disse qual |
| 4 | Attachment | documentos que apoiam a análise, citados na Description | — |

## Modelo de descrição

Seções em Heading 2, nesta ordem:

```
h2. Descrição da Sugestão

<qual é a sugestão para o projeto>

h2. Justificativa

<por que a mudança é necessária; qual a dor do usuário ou do cliente>

h2. Configurações atuais

<quais funcionalidades (casos de uso) envolvem a sugestão. Se não existe funcionalidade no sistema: O SISTEMA NÃO POSSUI ESTA FUNCIONALIDADE>

h2. Impacto no Sistema

Como essa mudança afetará outras partes do projeto?
R: <resposta>

Existem dependências que precisam ser consideradas? Se sim, quais?
R: <resposta>

A alteração deve ser aplicada à carga de supervisor?
R: <resposta>

Há relatórios e PDFs envolvidos na alteração? Se sim, quais?
R: <resposta>

Afeta o Sync e/ou a Integração?
R: <resposta>

h2. Riscos e Considerações

<riscos ou considerações importantes associados à mudança>
```

Todas as respostas "R:" precisam estar preenchidas na aprovação; "Não" ou "Não se aplica" são respostas válidas. Na Justificativa, se o tester tiver dificuldade, o guia indica o treinamento "Processo e análise para entrega de valor ao cliente" da Universidade Corporativa.
