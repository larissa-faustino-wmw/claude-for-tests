# Plano de Ação — Desenvolvimento de Cenários Automatizados com IA

**Projeto:** `totaluitest` (suíte de testes de UI do WMW Vendas / `lavenderepda`)
**Data:** 2026-08-05
**Objetivo:** reduzir o custo de criar e manter cenários automatizados, usando IA como executora,
e elevar a consistência das entregas (nomes, rastreabilidade, diagnóstico de falha).

---

## 1. Tese central

**Não reescrever o framework.** O núcleo de automação (`Driver`, `DSL`, `By`, `DriverWait`,
`AppFactory`) está saudável — a evidência é objetiva: em 253 arquivos de teste existe **1** clique
por coordenada absoluta e **15** `sleep()`. Todo o resto usa espera explícita. Framework de UI ruim
não produz esse perfil.

O gargalo está na **camada de contexto**: escrever o Java do cenário é a parte fácil para uma IA;
o que ela não consegue adivinhar é o encoding dos arquivos, o ID do componente, o significado de
`CDPARAMETRO = 970`, a convenção de nomes e o estado da tela quando o teste falha.

> Este plano constrói essa camada de contexto. O `totaluitest` em si quase não é tocado.

---

## 2. Diagnóstico (medido no repo)

### Bloqueios diretos para IA

| Bloqueio | Evidência | Fase |
|---|---|---|
| Arquivos ilegíveis por IA | **235 de 253** `.java` não são UTF-8 válido | F1 |
| IDs de componente indescobríveis | **261 IDs distintos**, zero catálogo; o SpyTC exige mouse humano | F3 |
| Parâmetros de sistema opacos | `CDPARAMETRO = 133` em 11 fixtures, `970` carrega JSON — sem dicionário | F3 |
| Nenhuma convenção escrita | não existe `CLAUDE.md`, `docs/` nem template de cenário | F4 |
| Diagnóstico de falha pobre | falha gera apenas PNG; sem dump textual da tela | F5 |

### Custo de repetição (afeta humano e IA)

| Sintoma | Número |
|---|---|
| Linhas de fixture SQL | **19.010** em 231 arquivos (~82 linhas/cenário) |
| Testes que repetem o preâmbulo "logar → pedidos → novo pedido → filtrar cliente" | **199 de 253** |
| Testes com o cliente mágico `"1;1;1;"` | **190** |
| Testes com o item mágico `"1;1;10;"` | **117** |
| `PedidoPage` | **1.601 linhas** / 273 métodos de uma linha |
| `assertEquals` com literal solto | **5.513** |
| Fixtures `.sql` byte-a-byte idênticas | 4 grupos |

### Inconsistência de nomes e rastreabilidade

| Sintoma | Evidência |
|---|---|
| Numeração ambígua | **`ct1` e `ct001` coexistem** — idem `ct3`/`ct003`, `ct6`/`ct006`, `ct29`/`ct029` |
| Metadado em prosa livre | 210 apontam Confluence, **19** Squash, **7** Jira, 1 tem "Clientes afetados" |
| Typos em nome de classe | `EmicaoDePedido...` (Emissão), `EmitiPedido...` (Emitir) |
| Profundidade irregular | `ctNN/tNN` e `ctNN/tNN/sN` convivem sem regra explícita |

---

## 3. Fases

A ordem **não é negociável** entre F1 → F2. As demais podem correr em paralelo.

### F1 — Migração para UTF-8 `[BLOQUEADOR]`

Hoje a IA lê `Aus�ncia do nome do Cliente` e `PAG�VEL EM QUALQUER BANCO`. Ela não sabe qual
caractere era; ao gravar o arquivo escreve UTF-8 e corrompe os literais comparados contra o app.
**Toda** iniciativa de IA morre aqui.

**Tarefas**
1. Piloto: converter apenas `ct006` para UTF-8, ajustar `<project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>`,
   manter `-Dfile.encoding=ISO-8859-1` no runtime.
2. Rodar `ct006/t004` (tem assert com acento: `"PAGÁVEL EM QUALQUER BANCO ATÉ O VENCIMENTO"`) e confirmar aprovação.
3. Se aprovar: conversão em massa via `iconv` + commit isolado, **sem** nenhuma alteração de lógica no mesmo commit.
4. Adicionar `.gitattributes` fixando `*.java text working-tree-encoding=UTF-8` e um check de CI que falha em arquivo não-UTF-8.

**Premissa a validar (F1.2):** `file.encoding` governa I/O do app com o SQLite, não os literais
já compilados — logo os 5.513 asserts não deveriam ser afetados. **Isto é hipótese, não certeza.**
O piloto existe justamente para descobrir isso em 1 arquivo em vez de 253.

**Critério de aceite:** 100% dos `.java` passam em `iconv -f UTF-8 -t UTF-8`; suíte completa com a
mesma taxa de aprovação de antes da conversão (comparar contra baseline da F0).

**Risco:** médio. **Mitigação:** commit isolado e reversível; baseline de aprovação medido antes.

---

### F2 — Padronização de nomes e rastreabilidade

Depende de F1 — reescrever 253 arquivos antes do encoding destrói acentos em massa.

**Tarefas**
1. Padronizar numeração em 3 dígitos: `ct001/t001[/s01]`. Resolve as 4 colisões. Usar `git mv` para preservar histórico.
2. Corrigir typos de nome de classe (`Emicao` → `Emissao`, `Emiti` → `Emitir`).
3. Criar a anotação `@Cenario`, substituindo o javadoc em prosa:

```java
@Cenario(
    squash   = 2755,
    jira     = "VENDAS-20925",
    modulo   = Modulo.FINANCEIRO,
    titulo   = "Aplicação de índice financeiro em boleto offline",
    clientes = "PMB",
    versao   = "1.0")
```

4. Migrar os 234 cabeçalhos para a anotação (trabalho de IA, revisão humana por amostragem).
5. Gerar `docs/cenarios.md` a partir da anotação — índice deixa de ser mantido à mão.
6. Regra de CI: cenário novo sem `squash` preenchido falha o build.

**Por que anotação e não pasta/javadoc:** hoje a informação está em prosa, ninguém valida, e a IA
não tem formato para seguir — daí 210 Confluence contra 19 Squash. Campo tipado a IA preenche sem
inventar formato, e passa a ser grepável e validável.

**Critério de aceite:** zero colisão de numeração; 100% dos cenários com `@Cenario` válido;
`docs/cenarios.md` gerado no build.

**Risco:** baixo (mecânico). **Atenção:** renomeação em massa + integrações externas — conferir se
algum job de CI ou o Squash referencia caminho de pasta.

---

### F3 — Catálogos gerados (maior valor unitário)

> Regra: **catálogo gerado, nunca mantido à mão.** Documentação manual desatualiza e passa a
> envenenar a IA em vez de ajudar.

#### F3.1 — Catálogo de IDs de componente

A IA não tem mouse para usar o SpyTC, então chuta `btSalvarPedido` quando o certo é `btSalvarNovo`.
O framework já tem todas as peças: `Driver`, `getChildren()`, `IAddId.ADD_ID.getID()`, `Action.run`.

Harness que abre cada Form e despeja a árvore em `docs/ids/<Form>.md`:

```
CadPedidoForm
  lbDsCliente          BaseLabel      "CLIENTE PJ"
  cbTabelaPreco        BaseComboBox   → TABELA DE PRECO DESC/ACRE [2]
  btNovoItem           Button
  edQtItemFisico       EditText
  tabDinamica[Pagamentos|Detalhes|Boletos]
```

**Subproduto de alto valor:** o dump expõe os componentes **sem** ID — a lista exata do que pedir
ao time do app. É a causa raiz do único clique por coordenada do repo (`ct006/t004:182`, com o
comentário do autor explicando que "o totaluitest não enxerga esta grid").

#### F3.2 — Dicionário de parâmetros de sistema

`CDPARAMETRO = 970` sem dicionário faz a IA copiar SQL de outro teste sem entender e errar em
silêncio. Gerar `docs/parametros.md` com número → nome → significado → valores aceitos.

**A validar:** suspeito que as descrições estejam na própria base SQLite (tabela de definição de
parâmetros). Se estiverem, é geração automática. Requer a base baixada (`exec:exec@db`).
Se não estiverem, é extração do código do app — ver §6.

**Critério de aceite:** catálogos gerados por comando Maven e regenerados no CI; IA consegue
escrever um cenário novo consultando só os catálogos, sem perguntar ID a um humano.

**Risco:** baixo. **Esforço:** o maior das fases, mas paga em toda criação de cenário futura.

---

### F4 — `CLAUDE.md` + template de cenário

Sem receita explícita a IA improvisa e o time revisa lixo.

**Conteúdo mínimo**
- Como criar um cenário: pasta, `@Cenario`, `.sql`, Page Object, Flow.
- Como rodar **um** cenário só (hoje o caminho conhecido sobe 4 forks e baixa banco).
- Onde consultar ID (`docs/ids/`) e parâmetro (`docs/parametros.md`).
- Padrão obrigatório: passos numerados, `assertAll` por passo, mensagem em todo assert.
- Proibido: clique por coordenada absoluta, `sleep()`, ID inventado, SQL copiado sem entender.
- Massa de teste: quais clientes/itens/tabelas existem na base e o que cada um exercita.

**Entregável extra:** `docs/template-cenario.java` — cenário de referência comentado, que a IA usa
como molde.

**Critério de aceite:** um cenário novo escrito por IA seguindo só o `CLAUDE.md` passa em revisão
humana sem correção estrutural.

**Risco:** baixo. **Esforço:** pequeno. Melhor relação custo/benefício do plano.

---

### F5 — Diagnóstico de falha legível por máquina

Hoje `printInError()` salva PNG. Funciona, mas fecha o loop apenas com humano no meio.

**Tarefas**
1. Em `printInError()`, além do screenshot, dump textual da árvore da tela com IDs, tipos e valores
   no momento da falha (reaproveita o gerador da F3.1).
2. Registrar em texto: qual assert falhou, valor esperado vs. obtido, e a tela corrente.
3. Consolidar em `dadosTest/<Teste>/falha.md`.

**Por que importa:** é a diferença entre IA que precisa de um humano em cada iteração e IA que
converge sozinha — ela roda, falha, lê o que estava na tela, corrige.

**Critério de aceite:** dado só o `falha.md`, a IA identifica a causa e propõe correção sem rodar
de novo às cegas.

**Risco:** baixo (aditivo, não altera teste existente).

---

### F6 — Redução de superfície: Flows e massa nomeada

Incremental e permanente. Com IA vale mais do que valia: **menos superfície de API = menos
alucinação**.

**Tarefas**
1. `PedidoFlow` — mata o preâmbulo repetido em 199 de 253 testes:

```java
PedidoFlow pedido = PedidoFlow.novo()
        .paraCliente(Clientes.CLIENTE_PJ)
        .comTabelaPreco(Tabelas.DESC_ACRE_2)
        .abrir();
```

2. Massa nomeada — `"1;1;1;"` (190 usos) → `Clientes.CLIENTE_PJ`; `"1;1;10;"` (117 usos) → `Itens.ITEM_10`.
3. `assertAll` por passo. Com 5.513 asserts, `skipAfterFailureCount=1` e retry 3×, hoje o primeiro
   assert que falha esconde os demais do mesmo passo — um erro descoberto por rodada, e cada rodada
   sobe o app inteiro.
4. Fixtures SQL composáveis — presets nomeados no lugar de 82 linhas copiadas:

```java
Cenario.base().comBoletoOffline().comParametroSistema(38, "9").aplicar();
```

**A validar (F6.4):** quem carrega o `.sql` é `@PDATotalUITest`, que vem do jar do
`wmwvendasapp` e **não está neste repo**. Precisa confirmar se aceita SQL programático ou múltiplos
arquivos. Ver §6. Alternativa barata: pré-processador com `--@include base/pedido-padrao.sql`.

**Estratégia:** aditivo. Flow e constantes entram nos cenários **novos**; os 253 antigos migram
só quando alguém encostar neles. Nada de big bang.

**Critério de aceite:** cenário novo escrito com Flow tem ≤50% das linhas do equivalente antigo.

---

## 4. Sequenciamento

```
F1 (UTF-8) ──► F2 (nomes + @Cenario)
   │
   ├──► F3 (catálogos) ──┐
   ├──► F4 (CLAUDE.md) ──┼──► F6 (Flows / massa / assertAll)
   └──► F5 (diagnóstico) ┘
```

| Fase | Esforço relativo | Dependência | Valor para IA |
|---|---|---|---|
| F1 UTF-8 | P | — | **Bloqueador** |
| F2 Nomes + `@Cenario` | M | F1 | Médio (alto para o time) |
| F3 Catálogos | G | F1 | **Muito alto** |
| F4 `CLAUDE.md` | P | F3 parcial | **Muito alto** |
| F5 Diagnóstico | P/M | F3.1 | Alto |
| F6 Flows / massa | M (contínuo) | F1, F4 | Alto |

Melhor primeiro corte se houver pouca banda: **F1 + F4 + F3.1**. Já viabiliza IA escrevendo
cenário com ID correto e convenção clara.

---

## 5. Métricas

### Baseline a capturar antes de começar (F0)
- Tempo médio (pessoa-hora) para entregar um cenário novo hoje — **medir, não estimar**.
- Taxa de aprovação da suíte completa e número de reruns acionados (`rerunFailingTestsCount=3`).
- Tempo de wall-clock da suíte completa com `execs=4`.

### Alvos
| Métrica | Como medir | Alvo |
|---|---|---|
| Tempo para criar cenário novo | pessoa-hora por cenário entregue | **−50%** |
| Linhas escritas à mão por cenário | `.java` + `.sql` do commit | **−60%** |
| Cenário novo aprovado na 1ª execução | contagem simples | ≥70% |
| Cenários com `@Cenario` válido | check de CI | 100% |
| Arquivos não-UTF-8 | check de CI | 0 |
| Colisões de numeração | check de CI | 0 |
| Componentes sem ID no fluxo de pedido | catálogo F3.1 | tendência a 0 |

---

## 6. Acessos e dependências externas

### Acesso ao repositório do PDA (`wmwvendasapp` / `lavenderepda`) — **recomendado**

Não é bloqueador, mas destrava quatro coisas e reduz muito o esforço:

| O que destrava | Por quê |
|---|---|
| **F3.1** — extração estática de IDs | Os Forms declaram os IDs no código do app. Extrair estaticamente é mais barato e mais completo que só o dump dinâmico, que cobre apenas telas que o harness consegue abrir. |
| **F3.2** — dicionário de parâmetros | Se as descrições não estiverem no SQLite, estão nas constantes/definições do app. |
| **F6.4** — fixtures composáveis | `@PDATotalUITest` e o carregador de `.sql` vivem no app. Sem ler esse código, a decisão entre "SQL programático" e "pré-processador de include" é chute. |
| **Tickets de ID faltante** | Para abrir a demanda no lugar certo já apontando o Form e o componente (ex.: a grid de boletos do `ct006/t004`). |

### Outras dependências
- Base SQLite baixada (`mvn compile exec:exec@db`) para validar F3.2.
- Confirmar se algum job de CI ou o Squash referencia caminho de pasta de teste (impacta F2).
- Definir dono do `CLAUDE.md` — documento sem dono desatualiza e passa a atrapalhar.

---

## 7. Fora de escopo (decisão consciente)

| Item | Por quê não |
|---|---|
| Reescrever `Driver`/`DSL`/`By`/`AppFactory` | Está funcionando (1 coordenada, 15 sleeps em 253 testes). Reescrita consome meses e para a produção de cenários no meio. |
| Trocar a estrutura `ctNN/tNN` por outra taxonomia | Rastreia Squash/Jira. Padronizar a numeração resolve; trocar o modelo não aumenta produtividade. |
| Migrar de JUnit/TotalCross para outra stack | Não existe alternativa para automação de UI TotalCross. |
| Paralelismo além de `execs=4` | Otimização de execução, não de criação. Fora do objetivo deste plano. |

---

## 8. Débito de segurança (fora do plano, mas registrado)

Encontrado durante a análise, precisa de encaminhamento próprio:

- `pom.xml:23` — `nexus.auth` com credencial Basic base64 em claro, versionada.
- `src/test/resources/configTests/configEmail.properties` — senha SMTP em claro (`mail.smtp.host=smtp.wmw.com.br`).

Ambas estão no histórico do Git. Rotação das credenciais + migração para variável de ambiente ou
secret do CI. Não bloqueia nenhuma fase, mas não deve ficar aberto indefinidamente.

---

## 9. Próximo passo imediato

**Piloto de encoding (F1.1 + F1.2).** Converter `ct006` para UTF-8, rodar `ct006/t004` — que tem
assert com acento (`"PAGÁVEL EM QUALQUER BANCO ATÉ O VENCIMENTO"`) — e confirmar aprovação.

É a validação que destrava todo o resto do plano. Se a premissa sobre `file.encoding` estiver
errada, é infinitamente melhor descobrir em 1 arquivo do que em 253.
