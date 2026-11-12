# Rastreio do impacto

Parta de cada alteração relevante do diff e responda: **quem mais depende disso, e o usuário vê onde?**

## Por tipo de alteração

| Alteração | Como rastrear |
|---|---|
| Método de service mudou (assinatura ou regra) | `Grep` pelo nome do método no repositório; para cada chamador, suba até a tela ou o job. Em service base/abstract, inclua as subclasses |
| Método novo chamado de um fluxo existente | o fluxo existente inteiro passa a depender dele: leia o ponto de chamada e o que acontece se ele falhar ou devolver vazio |
| Classe base ou abstract de tela (`AbstractBase…Form`, `Base…`) | todas as telas que estendem: `Grep "extends <Classe>"` |
| Domain: coluna nova ou mudada | DAO/sqlmap da entidade, telas que a mostram, sincronização da tabela, relatórios e PDF |
| DAO / sqlmap: consulta mudada | todas as chamadas do método do DAO; listas e filtros que usam a consulta |
| Parâmetro (uso novo ou mudado) | `Grep` pelo nome do parâmetro (`LavenderePdaConfig.<nome>` no app, `ConfigParametro` no web): todos os pontos que o leem são candidatos |
| Cálculo (preço, desconto, imposto, comissão, cashback, estoque) | todas as telas que exibem o valor (capa, item, lista, totalizadores, PDF, impressão) e o que vai para o ERP e para a Web |
| Sincronização (DTO, envio, retorno) | a entidade nos dois sentidos; o caso compartilhado PERSISTENCIA-001 do Squash |
| `Messages_*.properties` | asserts do `totaluitest` que validam o texto (`Grep` pelo texto antigo em `projetos/totaluitest/src/test`) |
| Componente de framework | todas as telas que usam o componente; é o impacto mais largo |

Pare de subir quando chegar a um fluxo do usuário (tela, ação, relatório) ou a um ponto de integração (sync, ERP).

## A outra stack

App e web compartilham o domínio: `TBLVP<X>` no app, `TBLVW<X>` no web. Alteração de regra num lado costuma ter o par no outro.

- A correspondência das entidades: `docs/ia/comum/30-correspondencia-app-web.md`.
- A atividade mexeu só num lado? Verifique se o outro lado tem a mesma regra (o mesmo cálculo no `lavenderecore`) e se ficou divergente. Divergência entre as stacks é side effect de risco alto.

## Área de negócio

`docs/ia/comum/areas.tsv` dá a área de cada entidade; os mapas `docs/ia/pda/20-mapa-modulos.md` e `docs/ia/web/20-mapa-modulos.md` dão as telas e classes por área. Use a área para:

- achar as Features do Jira correspondentes (histórico de Defects);
- achar os casos da regressão fixa do mesmo assunto;
- achar a pasta de testes do `totaluitest` (`src/test/java/br/com/wmw/lavenderepda/presentation/ui/test/<área>/`).

Os mapas são rascunho: use como guia, não como verdade.

## Squash

Com o tester logado, a API REST do Squash responde na sessão do Chrome (navegar até a URL e ler com `get_page_text`). Só leitura.

| O quê | URL |
|---|---|
| Regressão fixa App (pasta 7) | `https://squash.wmw.com.br/squash/api/rest/latest/test-case-folders/7/content?size=500` |
| Regressão fixa Web (pasta 17) | `https://squash.wmw.com.br/squash/api/rest/latest/test-case-folders/17/content?size=500` |
| Um caso (passos, pré-requisitos, requisitos) | `https://squash.wmw.com.br/squash/api/rest/latest/test-cases/<id>` |

A regressão fixa tem um caso por assunto (Reference `PEDIDO-03.19 - APP` = Tributação; `ATUALIZAÇÃOSYNC-02.08 - APP` = Envio de dados Smartphone→Web…), com passos amplos e sem resultado esperado detalhado. Conta como cobertura do **fluxo largo**, não de uma regra específica.

Casos da atividade: os vinculados ao requirement com Reference `VENDAS-xxxxx`. Se não conseguir ler, peça ao tester a lista.

## Histórico no Jira

| Pergunta | Ferramenta |
|---|---|
| Essa feature costuma dar bug? | `jira_feature_hotspots` |
| Correções dessa área voltam? | `jira_rework` |
| Quais causas se repetem? | `jira_problem_causes` |
| Outras atividades abertas na mesma área | `search_jira_jql` com a Feature e `resolution = Unresolved` |

Outra atividade aberta que mexe nas mesmas classes (procure as branches dela com `git diff --stat` e compare os arquivos) é risco de conflito: cite as duas chaves.
