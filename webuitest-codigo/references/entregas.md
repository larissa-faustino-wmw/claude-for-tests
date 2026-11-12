# Formato das entregas

## 1. Cenário

Um passo por linha, na numeração dos comentários do código:

| # | Passo | Resultado esperado |
|---|---|---|
| 1 | Efetuar login na Web e abrir a tela de Aprovação de Desconto Promocional | A tela abre sem mensagem de erro |
| 2 | Filtrar pelo representante "100" no filtro lateral | A lista mostra os 3 pedidos pendentes do representante, com valor e desconto de cada um |

Pré-requisitos (configuração e massa criada pelo teste) antes da tabela. Caso LVW já existe no Squash: liste as diferenças entre o caso e o código, em vez de reescrever. Criar ou atualizar casos é com a `gerador-de-testcases`.

## 2. Código

A classe completa e os trechos das outras alteradas (Page nova, método novo na infraestrutura, chave nova no `webuitest.properties.example`). Infraestrutura nova vem com uma linha dizendo por que foi criada.

## 3. Worklog do Jira

Primeira pessoa, na voz do tester (pode citar "com apoio do Claude"), frases diretas, sem emoji:

```
Criação do cenário COMERCIAL-LVW-012 na Web com apoio do Claude.
Tela aberta pela chave de menu 1,245 no iframe da aplicação.
Massa: pedido de teste criado e apagado pelo próprio teste (banco sem reset).
Validações: lista filtrada pelo representante e valores do desconto, com asserções do Playwright que esperam o carregamento.
Infraestrutura: criada a AprovacaoDescontoPromocionalPage, primeira Page da área comercial.
```

## 4. Classes alteradas

Caminho a partir de `src/`, ação entre parênteses:

```
- test/java/br/com/wmw/webuitest/comercial/ValidarFiltroAprovacaoDescontoPromocionalTest.java (criada)
- main/java/br/com/wmw/webuitest/web/comercial/AprovacaoDescontoPromocionalPage.java (criada: primeira Page da tela)
- main/java/br/com/wmw/webuitest/web/SessaoWeb.java (alterada: metodo abreTela(chaveMenu))
- webuitest.properties.example (alterada: chave nova comentada)
```

Os nomes de pacote acima são exemplo: siga a estrutura que o tester aprovar na primeira Page da área. A lista também serve para o Component/s da Test Automated.
