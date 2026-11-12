# Checklist da revisão

Marque cada item como ok, problema (com severidade) ou não se aplica. App = `totaluitest`; Web = `webuitest`.

## 1. Caso do Squash × código

- [ ] Cada passo do caso tem o `/* Passo N: */` correspondente, na mesma ordem.
- [ ] Cada resultado esperado tem `/* Resultado Esperado N: */` e **asserção que o prova com o valor** (não só "a tela abriu").
- [ ] Pré-requisitos do caso (parâmetros, massa) estão na massa do teste, com os mesmos valores.
- [ ] Nada que o caso não pede (passo extra sem resultado esperado).
- [ ] Caso de persistência App → Web: as três etapas (gravou, sincronizou, conferiu na Web) ou a chamada ao PERSISTENCIA-001.

## 2. Falso positivo

- [ ] Nenhum `return`, `if` ou `try/catch` que deixa o teste verde sem testar (ex.: "se for fim de semana, sai").
- [ ] Nenhuma asserção de uma variável com ela mesma, ou com um valor lido no passo anterior da própria tela.
- [ ] Contagem que garante **qual** item foi validado, não só quantos.
- [ ] Resultado esperado que não repete o anterior.
- [ ] A asserção principal falharia com o valor errado (prova em cópia temporária ou raciocínio explícito).

## 3. Asserções

- [ ] App: `assertEquals(esperado, obtido, "mensagem")` com o valor concreto; `getMessage()` para mensagem do app; string de item completa.
- [ ] Web: `assertThat(locator).hasText/hasValue/hasCount(...)` (web-first); nenhum `innerText()`/`inputValue()` comparado com `assertEquals`.
- [ ] Nenhum `assertNotNull`/`assertTrue`/`contains`/`startsWith` onde o objetivo é o valor.
- [ ] Mensagem da asserção (App) corresponde ao campo validado, sem duplicar.

## 4. Esperas e estabilidade

- [ ] Nenhum `Thread.sleep`, `waitForTimeout` ou timeout aumentado.
- [ ] App: `waitOpening(...)` depois de cada ação que abre tela, janela ou mensagem; `waitValue` para valor que vem do banco; sem `waitOpening` redundante; espera logo depois da ação, não no começo do passo seguinte.
- [ ] Web: tela no iframe `#contentFrame`; espera pela resposta quando precisa dela (`waitForResponse`); nada dependente de `NETWORKIDLE`.
- [ ] Três rodadas seguidas passando (seção 3 da skill).

## 5. Massa e dados

- [ ] App: massa no `@InvokeInit` da própria classe (não em util compartilhado nem em `.sql` solto); `insert` com `rowkey`; `update` com `WHERE`.
- [ ] Parâmetro JSON: código presente em `PARAMETROS_JSON`; `Map` com as chaves certas.
- [ ] Datas pelo `DatasTestUtil` (App) ou relativas a hoje; nenhuma data fixa.
- [ ] Web: massa criada pelo teste com marcador único e apagada em `@AfterEach`/`finally`; parâmetro alterado restaurado.
- [ ] Nenhum dado real (CPF, CNPJ, e-mail, telefone).
- [ ] Não depende de dado de outro teste nem da ordem de execução.

## 6. Padrão e documentação

- [ ] JavaDoc da classe: título, `@author`, `@version`, `@see` do Squash e do Jira (obrigatórios); Confluence quando houver cenário anterior (link com `pageId`).
- [ ] Comentários de passo multilinha com `/*`, nunca `//` nem `/**` dentro do método.
- [ ] Nome da classe com verbo + comportamento + `Test`; método `deve…`.
- [ ] Seletores e valores fixos de negócio nas Pages (constantes), não espalhados no teste.
- [ ] Método novo em Page só quando não havia equivalente (`Grep` na Page e na `BasePage`), marcado com comentário.
- [ ] Variáveis: só quando reutilizadas, `final`, perto do primeiro uso.
- [ ] Encoding: `file -b` diz ISO-8859 (ou ASCII) com CRLF; nenhum `EF BF BD`/`ï¿½`. Web: ASCII puro (acento por `\uXXXX`).

## 7. Escopo

- [ ] Nenhuma alteração no código de produção (`lavenderepda`, `lavendereweb`) para atender o teste.
- [ ] Alterações em outros testes, Pages ou utils justificadas e listadas.
- [ ] `git status` limpo depois da revisão (a revisão não deixou nada).
