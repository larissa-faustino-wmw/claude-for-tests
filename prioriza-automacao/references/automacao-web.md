# Automação Web (webuitest)

O time ainda não automatiza a Web, e quer começar. O repositório `projetos/webuitest` (Playwright Java + JUnit 5) já existe, contra o Tomcat local de dev.

## O que o webuitest já tem (11/2026)

- Configuração lida do Tomcat do dev (porta do `server.xml`, banco do `wmw_database_config`) e do `workspace.properties`/`webuitest.properties`.
- Sessão web (`SessaoWeb`), login, abertura de itens de menu (`ItemMenu`, `CatalogoMenu`), resultado de abertura de tela e leitura de erro do log do Tomcat.
- Um smoke de abertura de telas pelo menu.
- Acesso ao banco de teste (`BancoTeste`).

Ou seja: **abrir telas e verificar que não quebram** já existe. Fluxo de negócio (preencher, gravar, conferir valor calculado) ainda não tem Pages nem utilitários de massa como o TotalUiTest.

## Regras do repositório que afetam os cenários

- **O banco não tem reset:** teste que grava precisa apagar o que criou, inclusive quando falha. Cenário Web que grava (aprovar pedido, cadastrar) custa mais.
- Abrir item de menu executa o comando da ação: cenários que abrem telas novas precisam do dev conferir os comandos.
- Teste de integração usa `AmbienteLocal.carregaOuPula()`.

Para escrever os testes Web, use a skill `webuitest-codigo` (regras de Playwright em Java para as telas JSF e a infraestrutura do repositório).

## Como isso entra na priorização

- Marque a plataforma como **Web** e diga, na sugestão, o que falta no webuitest para ela ("precisa de Page da tela de aprovação de desconto promocional e de limpeza do pedido gravado").
- Fator automatizável 0,8 para fluxo simples de tela; 0,6 quando precisa de suporte novo (a maior parte dos primeiros cenários).
- **Sugira começar pelo que dá mais retorno com menos infraestrutura:** telas Web com bug de produção recorrente que só precisam abrir, filtrar e conferir valor (a tela de aprovação de desconto promocional "sem informação" da Rasip, por exemplo). Os primeiros cenários Web constroem a base (Pages, massa, limpeza) que os próximos reaproveitam: diga isso no porte.
- Ao final da lista, um parágrafo "Para começar a Web": os 2 ou 3 cenários Web de maior pontuação e a infraestrutura que eles exigem.
