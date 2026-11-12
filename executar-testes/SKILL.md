---
name: executar-testes
description: Executa os casos de teste do Squash TM de uma atividade, de uma sprint, da Delivery de uma versão ou de uma homologação de cliente, no App (TotalCross, pelo agente tcui ou pelo teste automatizado do totaluitest) e na Web (wmwvendas, pelo Chrome ou pelo teste do webuitest quando houver), ou guia o tester na execução manual — confere cada passo contra o resultado esperado, guarda a evidência, registra o resultado na execução do Squash e aponta as falhas para virar Defect. Use SEMPRE que o usuário pedir para executar, rodar, testar ou retestar os casos de uma atividade VENDAS-xxxxx, uma iteração ou campanha do Squash, a regressão da Delivery, a homologação de um cliente, ou para registrar resultado de execução no Squash — mesmo que diga só "executa os testes da VENDAS-25526".
---

# Executar os testes

Executa os casos que já estão no Squash e registra o resultado lá. Vale para App e Web, e para os quatro momentos do tester: a atividade (reteste incluso), a sprint, a Delivery e a homologação.

O princípio vem do aceite dos devs: **observar o comportamento, com evidência**. Caso aprovado sem evidência não é caso aprovado.

## 1. O que executar

| Pedido | De onde vêm os casos |
|---|---|
| uma atividade (`VENDAS-xxxxx`) | os casos do requirement com Reference = a chave, no plano da sprint em Executions |
| uma iteração ou campanha | o plano de teste dela (`iterations/<id>/test-plan`) |
| a Delivery da versão | a campanha da versão na pasta VERSÕES: regressão fixa, reteste das atividades e os riscos da `analise-impacto-delivery` |
| uma homologação | a campanha do cliente na pasta HOMOLOGAÇÕES (`roteiro-homologacao`) |
| reteste depois de uma correção | os casos que falharam e os side effects da `analise-impacto` no modo reteste |

Leia pela API do Squash (só leitura; `references/squash-execucao.md`): para cada item, o caso (passos, pré-requisitos, resultado esperado), o status atual e a última execução. Mostre a lista com o modo proposto para cada caso e espere o ok antes de começar.

## 2. Escolher o modo de cada caso

Em ordem de preferência:

| Modo | Quando | Como |
|---|---|---|
| **Automatizado** | o caso tem teste automatizado (classe do `totaluitest` ou do `webuitest`, no Squash ou no Component/s da Test Automated) | roda o teste e lê o resultado (`references/modo-app.md` ou `references/modo-web.md`) |
| **Assistido no App** | caso do App, sem teste automatizado, e o agente tcui disponível | dirige o app pelo agente, passo a passo (`references/modo-app.md`) |
| **Assistido na Web** | caso da Web, sem teste automatizado, e o Chrome conectado | dirige o wmwvendas pelo Claude in Chrome (`references/modo-web.md`) |
| **Manual guiado** | nenhum dos anteriores, ou o caso pede o que a skill não faz (aparelho físico, impressora, ERP, dado que só o tester vê) | apresenta um passo por vez; o tester executa e responde o que viu |

Um mesmo caso pode misturar: os passos de tela pelo agente e a conferência na Web pelo Chrome, por exemplo, na persistência App → Web (PERSISTENCIA-001).

## 3. Preparar o ambiente

Antes do primeiro caso:

- **Qual ambiente e qual base:** Tomcat de dev ou ambiente de homologação; base de teste, base da versão ou base do cliente. Registre na execução.
- **Backup da base do App** antes de usar o agente (o login e a navegação gravam nela); trabalhe numa cópia.
- **Pré-requisitos dos casos:** parâmetros e massa. O que a skill alterar (parâmetro, por exemplo) ela anota para restaurar no fim.
- **Não suba, derrube ou troque de branch sem perguntar:** Tomcat, agente tcui e branch de repositório podem estar em uso pelo tester.

## 4. Executar, caso a caso

Para cada passo:

1. faça a ação (pelo modo do caso);
2. confira o resultado esperado **com o valor**: o que a tela mostra, o que o banco gravou, o que o log registrou;
3. guarde a evidência (print da tela, valor lido, linha da tabela, trecho de log) em `evidencias/<caso>/` na pasta de trabalho da execução;
4. anote o status do passo: **passou**, **falhou**, **bloqueado** (não deu para executar por causa de outro problema) ou **não testável** (o caso não se aplica a este ambiente), com o motivo.

Os pontos que mais escondem defeito estão em `references/pontos-de-defeito.md`: erro só no log do Tomcat, o que se perde na sincronização, o parâmetro desligado, os idiomas, dado de outro teste. Olhe-os em todo caso que grava ou sincroniza.

Falha de um passo: termine o caso só se os passos seguintes ainda fizerem sentido; senão, marque o resto como bloqueado. Siga para o próximo caso: um defeito não para a execução inteira, a menos que bloqueie todos.

## 5. Registrar no Squash

Depois de cada caso (ou em lote no fim, se o tester preferir), registre a execução pela tela do Squash (`references/squash-execucao.md`): status de cada passo, comentário com o ambiente e o que foi visto, e as evidências anexadas. **Mostre o que vai registrar antes de gravar** na primeira vez; depois, siga no mesmo padrão e mostre o resumo no fim.

## 6. Falhas viram Defect

Para cada falha, prepare o relato para a `criar-task-jira` (tipo Defect, na atividade; ou Bug, fora de uma atividade): tela, passos até a falha, resultado atual com o valor, resultado esperado do caso, ambiente, base e as evidências. A `criar-task-jira` faz a busca por duplicidade, a rodada de dúvidas e a aprovação. Com o Defect criado, coloque a chave no comentário da execução do Squash.

## 7. Encerrar

- Restaure o que alterou (parâmetros, base do App) e diga o que ficou no banco de dev (registros criados).
- Feche o agente tcui e as abas que a skill abriu, se foi ela que abriu.
- **Resumo:** casos por status (passou, falhou, bloqueado, não testável, não executado), os Defects abertos com as chaves, o que ficou pendente e por quê.
- Próximo passo: com tudo passando numa atividade, ofereça a `liberar-atividade`; com falhas, o reteste depois da correção.

## Armadilhas

- **O agente tcui só existe na branch `tcui-split-tc5` do `totaluitest`.** Confira com `git -C projetos/totaluitest branch --show-current`; em outra branch, não troque sem o tester mandar (é o repositório de trabalho dele).
- **O app do agente grava na base.** Sem backup, a execução muda a base de teste dos próximos.
- **A DSL dos testes acha controle pelo `ID`; o agente também pelo nome do campo Java.** Para execução isso não importa, mas um controle que só o agente acha não serve de molde para automação.
- **`WmwMessageBox` não traz o tipo da mensagem:** erro e aviso só se distinguem pelo texto.
- **Listas do App carregam em outra thread:** o contador muda depois de a ação responder; espere o valor (`/waitValue`), não leia na hora.
- **Na Web, a tela fica no iframe `#contentFrame`,** e mensagem de erro do JSF pode existir escondida: só conta a visível.
- **O `error.log` do Tomcat é compartilhado:** erro que aparece durante a execução pode ser de outra pessoa usando o mesmo Tomcat.
- **Status no Squash não se desfaz sozinho:** registrar "passou" por engano exige corrigir a execução na tela. Na dúvida, deixe para o fim e confirme com o tester.

## Cuidados

- Nada é registrado no Squash nem aberto no Jira sem o padrão aprovado pelo tester; Defect só pela `criar-task-jira`, com aprovação.
- Não digite senha real: na tela de login do Squash, do Jira ou da Web de homologação, peça para o tester entrar. Credencial de teste só no Tomcat local, e só a que está no arquivo de configuração do workspace.
- Na base do cliente, nenhuma alteração além do que o próprio caso faz pela tela.
- Não marque como passou o que não foi conferido.
