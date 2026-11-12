# Testing — subtask de teste

Toda **Story** ou **Bug** que passa por um QA Tester recebe uma subtask de teste. No Jira o tipo se chama **`Testing`** (não confundir com o tipo `Test`, que é atividade solta, usada por exemplo nas validações de versão).

Não há guia no Confluence para este tipo; as regras abaixo são do time de QA.

Criação: na atividade pai, **More → Create sub-task** → Issue Type `Testing`.

## O que já existe (antes de criar)

Além da busca por palavras-chave do `SKILL.md`, leia as subtasks da pai. Se já há uma Testing atribuída ao mesmo QA, avise e não crie outra. Se há uma Testing aberta sem responsável, (sugestão) proponha usar a existente: atribuir e mover para Em Andamento, em vez de criar.

## O que perguntar

Normalmente nada além da chave da atividade pai. O título e os campos são fixos.

## Campos

| Campo | Valor |
|---|---|
| Issue Type | `Testing` |
| Summary | **`Testing - <título da atividade pai>`**, com o título copiado da pai como está |
| Assignee | o QA que vai testar — geralmente o usuário logado no Jira |
| Description | em branco, salvo se o tester pedir algo |
| demais campos | o padrão da tela |

A regra de formatação de título (`Tela - descrição`) não vale aqui: o título é fixo.

## Depois de criar

1. **Assign** para o QA (se a tela de criação não tinha o campo Assignee): botão **Assign** na atividade, ou **Assign to me** quando for o usuário logado.
2. Mova para **Em Andamento** (In Progress): clique no botão de transição do fluxo que leva a esse status (geralmente "Iniciar Progresso" / "Start Progress"). Se o fluxo não oferecer essa transição a partir do status atual, avise o tester em vez de passar por outros status.
3. Confira na atividade: responsável e status.

## Exemplo

Atividade pai (fictícia): `VENDAS-XXXXX - Pedido - Desconto progressivo por faixa de quantidade`.
Título: `Testing - Pedido - Desconto progressivo por faixa de quantidade`. Assignee: usuário logado. Status final: Em Andamento.
