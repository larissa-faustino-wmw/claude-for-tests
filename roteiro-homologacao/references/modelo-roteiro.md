# Modelo do roteiro para aprovação

## Homologação <Cliente> — <projeto ou entrega>

| | |
|---|---|
| Agrupadora | VENDAS-xxxxx (<status>), criada por <QA/PO> |
| Cliente | <Cliente [código]> |
| Base | base do cliente <nome/identificação, sem credencial> |
| Versão base / branch | <9.0xx> / `<branch do cliente>` |
| Scripts | <onde estão; atividade com scripts de apoio> |
| Homologações anteriores | <Test e campanhas anteriores, com o que ficou pendente> |

**Configuração do cliente que importa** (da base)

| Parâmetro | Valor no cliente | Por que importa |
|---|---|---|
| 395 (configuração de verba) | `consomeRetornoVerbaVigente` = S | a VENDAS-22610 não suporta recálculo nesse caso: fora do escopo |

**Campanha:** `HOMOLOGAÇÕES / <Cliente> - <entrega> - <mês/ano>`

| Iteração | Casos existentes | Casos novos | Observação |
|---|---:|---:|---|
| HYDRA - VENDAS-23918 - Persistir a opção "Replica ordem de compra para os itens" | 2 | 1 | novo: com a configuração de ordem de compra do cliente |
| SHIELD - VENDAS-23836 - Margem negativa do pedido não gera pendência | 1 | 2 | Defect: reconferir na base do cliente |
| GERAL - Regressão básica | 21 (SMOKETEST App e Web) | 0 | |
| CONTABILISTA - Regressão do cliente | 3 | 2 | features com bug recente: Pedidos Pendentes, Condição de Pagamento |

Para cada caso novo: nome, pré-requisitos (configuração e massa do cliente), passos e resultado esperado, no padrão da `gerador-de-testcases`.

**Fora do escopo:** <o que a agrupadora diz que não tem suporte; itens não prontos para homologar>

**Riscos:** <side effects da branch, bugs do cliente em áreas tocadas, dependências (ERP, scripts)>

**Checklist de go live** (só em go live): scripts aplicados na base, versão e branch corretas no ambiente, carga gerada e recebida no App, sincronização ida e volta, regressão básica sem falha, Defects da homologação fechados ou aceitos pelo cliente.

> Campanha: `HOMOLOGAÇÕES / <campanha>`, <n> iterações, <n> casos (<n> novos). Posso cadastrar no Squash?
