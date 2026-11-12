# Estrutura da campanha no Squash

Conferida em 10/11/2026 no projeto VENDAS (id 6).

## Biblioteca de campanhas

```
VENDAS
├── HOMOLOGAÇÕES   (pasta 107)
│   ├── Entrega Rivatti - Junho 2026      (campanha)
│   ├── Regressão Múltipla Inserção       (campanha)
│   ├── CAMPOS CPF/CNPJ                   (campanha)
│   ├── 9.062-CONTABILISTA                (subpasta do cliente)
│   └── 10.000                            (campanha)
├── VERSÕES        (pasta 137)
└── TESTES INTERNOS (pasta 188)
```

## Padrão de uma campanha de homologação

Exemplo: **Entrega Rivatti - Junho 2026** (`/VENDAS/HOMOLOGAÇÕES/Entrega Rivatti - Junho 2026`).

| Elemento | Padrão |
|---|---|
| Campanha | `<Cliente> - <entrega ou projeto> - <mês/ano>` (ex.: `Entrega Rivatti - Junho 2026`); cliente com várias rodadas pode ter subpasta própria (`9.062-CONTABILISTA`) |
| Iteração por atividade | `<TIME> - VENDAS-xxxxx - <título da atividade>` (ex.: `HYDRA - VENDAS-18611 - Nova regra para pendenciar estoque crítico`) |
| Iteração de regressão | `GERAL - Regressão básica`, com Reference = o cliente (ex.: `Rivatti`) |
| Casos da regressão básica | o conjunto `SMOKETEST-xx.xx-APP` e `-WEB` (envio de dados Smartphone→Web, cadastro de novo cliente, pedido de venda, bonificado, troca, replicação, retorno, listagem, pedido para novo cliente, analisar logs, pedido na carga de supervisor) |
| Campo personalizado da campanha | `Fix Version` (preencha com a versão base da homologação, se houver) |

TIME pelo módulo da Feature da atividade: Comercial → HYDRA; Comunicação, Contábil/Fiscal, CRM, Estoque, Financeiro, Inteligência de Vendas → SHIELD; Sistema → TERMINATOR. Atividade sem Feature: pergunte, ou use `GERAL`.

Esta skill acrescenta uma iteração **`<CLIENTE> - Regressão do cliente`** quando o levantamento encontrar features do cliente com bug recente, bugs dele corrigidos recentemente ou side effects da branch. Se o time preferir, esses casos entram na `GERAL - Regressão básica`: pergunte na aprovação.

## Antes de criar

- Procure campanha do mesmo cliente e da mesma entrega (API, pasta 107 e subpastas). Existindo, proponha acrescentar as iterações nela.
- Os casos novos precisam existir na biblioteca antes de entrarem no plano: gere-os com a `gerador-de-testcases` (pasta do assunto, requirement da atividade) e só então monte o plano.

## Cadastro (pela tela, depois da aprovação)

1. **Campanha:** na pasta HOMOLOGAÇÕES (ou na subpasta do cliente), criar campanha com o nome aprovado; preencher `Fix Version` se houver.
2. **Iterações:** criar cada iteração com o nome aprovado; na de regressão, Reference = o cliente.
3. **Plano de teste:** em cada iteração, adicionar os casos aprovados (os do requirement da atividade, os novos e, na regressão, os SMOKETEST de App e/ou Web conforme o escopo).
4. Conferir pela API que cada iteração tem o número de casos aprovado (`iterations/<id>/test-plan`).
5. Devolver os links: `https://squash.wmw.com.br/squash/campaign-workspace/campaign/<id>/content` e de cada iteração.

Atribuição dos itens aos testers (assigned_to) e execução ficam com o time; a skill não executa casos nem muda status de execução.

Na tela de login, peça ao tester para entrar. Erro ao salvar: confira se o item foi criado antes de repetir.
