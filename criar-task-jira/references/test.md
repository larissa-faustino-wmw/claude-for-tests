# Test — teste de versão ou homologação

Atividade **solta** (não é subtask) do tipo `Test`, no projeto Vendas. Não confundir com a **Testing**, que é a subtask de teste de uma Story ou de um Bug (`references/testing.md`).

Os QAs usam dois tipos de Test:

| Tipo de Test | Quando |
|---|---|
| **Delivery** | teste da versão no processo de delivery (ex.: "Versão 9.070 de 06/11/2026") |
| **Other** | homologação de um cliente ou de uma funcionalidade específica |

Não há guia no Confluence para este tipo. As regras abaixo vêm do time de QA e do padrão das atividades existentes (VENDAS-25520, VENDAS-24892, VENDAS-25439, VENDAS-22610, conferidas em 10/11/2026).

Criação: botão **Create** → Project `Vendas` → Issue Type `Test` → no formulário, o campo que define o tipo de Test (opções **Delivery** e **Other**). Na primeira criação, leia o nome exato do campo na tela; se ele não aparecer, pergunte ao tester em vez de seguir sem ele.

## O que já existe (antes de criar)

Além da busca por palavras-chave do `SKILL.md`:

- **Delivery**: `project = VENDAS AND issuetype = Test AND fixVersion = "<versão>"`. Uma versão tem um Test de Delivery só; se já existe, avise e não crie.
- **Other**: Tests do mesmo cliente ou da mesma funcionalidade ainda abertos (`project = VENDAS AND issuetype = Test AND resolution = Unresolved AND text ~ "<cliente ou funcionalidade>"`). Pode ser o caso de usar o existente.

## Delivery

### O que perguntar (só o que faltar)

- **Versão** e **data** da versão.
- **Facilitador(a)** do teste.
- **Branch** (normalmente `release`).
- **Métricas**: dias estimados, número de testers, horas diárias por tester e clientes testados. Dias realizados ficam iguais aos estimados na criação, salvo se o tester disser outra coisa (sugestão).

### Campos

| Campo | Valor |
|---|---|
| Issue Type | `Test`, tipo **Delivery** |
| Summary | **`Versão <versão> de <dd/mm/aaaa>`** (ex.: `Versão 9.070 de 06/11/2026`) |
| Priority | `Medium` |
| Fix Version/s | a versão testada |
| Customer | `WMW` |
| Assignee | o facilitador(a) |
| Description | modelo abaixo |

### Modelo de descrição

O padrão das atividades existentes, no modo Text (negrito com `*` e lista com `*`, como nelas):

```
*Facilitador(a):* <nome>

*Branch:*
<branch>

*Métricas:*
* [DiasEstimados:<n>]
* [DiasRealizados:<n>]
* [NrTesters:<n>]
* [HorasDiariasTesters:<n>]
* [ClientesTestados:<cliente>, <cliente>]
```

As métricas ficam entre colchetes no formato `[Chave:valor]`, porque são lidas depois para indicadores: mantenha os nomes das chaves e os colchetes exatamente assim, **sem escapar** (é como estão nas atividades existentes; um `\` a mais quebra a leitura).

## Other — homologação de cliente ou funcionalidade

### O que perguntar (só o que faltar)

- **O que está sendo homologado**: o cliente, a funcionalidade, ou a atividade de origem (VENDAS-xxxxx).
- **Customer**: o cliente da homologação (`WMW` se for interna).
- **Objetivo e escopo**: o que precisa ser validado, a lista de itens ou atividades envolvidas, o que fica fora.
- **Fix Version/s**, se a homologação é de uma versão específica.

### Campos

| Campo | Valor |
|---|---|
| Issue Type | `Test`, tipo **Other** |
| Summary | homologação de cliente: `<Cliente> - <descrição curta>` (ex.: `Agrupadora Contabilista - Projeto Final Go Live`); de funcionalidade a partir de uma atividade: `<VENDAS-xxxxx> <título da atividade>` |
| Priority | `Medium` |
| Customer | o cliente; `WMW` se interna |
| Assignee | o QA responsável — geralmente o logado |
| Linked Issues | a atividade de origem e Tests anteriores do mesmo cliente |
| Description | modelo abaixo |

### Modelo de descrição (sugestão)

As atividades existentes não seguem um modelo fixo. Este é o sugerido pela skill:

```
h2. Objetivo

<o que está sendo homologado e para quê>

h2. Escopo

# <item, atividade ou funcionalidade a validar>
# <item>

h2. Fora do escopo

<o que não será validado, se houver>
```

Seções que não se aplicam são omitidas.
