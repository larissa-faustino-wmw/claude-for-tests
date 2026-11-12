---
name: revisar-teste-automatizado
description: Revisa um teste automatizado do Lavendere, do App (totaluitest, TotalUiTest) ou da Web (webuitest, Playwright), em contexto isolado — confere o código contra o caso do Squash (cada passo e resultado esperado), procura falso positivo, asserção fraca, espera faltando ou fixa, massa divergente, parâmetro JSON fora de PARAMETROS_JSON, limpeza de dados, encoding e padrão do time, roda o teste mais de uma vez para ver se é estável e grava um parecer com severidade (APROVADO, APROVADO COM OBSERVAÇÕES ou MUDANÇAS SOLICITADAS). Use SEMPRE que o usuário pedir para revisar, conferir ou avaliar um teste automatizado, uma classe *Test do totaluitest ou do webuitest, ou uma Test Automated antes de fechar — mesmo que diga só "revisa o teste da VENDAS-25597". Prefira rodar pelo agente revisor-teste-automatizado, para quem revisa não ser quem escreveu.
---

# Revisar teste automatizado

A revisão responde: **o teste prova o que o caso do Squash diz, de um jeito que falha quando o sistema quebra e passa quando ele está certo?** Um teste que passa sempre é pior que nenhum: dá a falsa certeza.

Rode em contexto isolado, pelo agente `revisor-teste-automatizado`: quem revisa não pode ter as suposições de quem escreveu. Fora do Claude Code (Codex, ChatGPT), abra uma conversa nova só para a revisão.

**Você não corrige o teste:** aponta, com `arquivo:linha` e a correção sugerida. O único arquivo que você grava é o parecer.

## 1. Reunir

- **O teste:** a classe (`*Test.java`) e o que ela usa e foi criado ou alterado junto: Pages, utils, `ParametrosTestUtil`, infraestrutura do `webuitest`. Com a chave da Test Automated, leia a descrição pelo MCP interno (Teste, Link do Squash, Cenário anterior) e o Component/s.
- **O caso do Squash:** passos, pré-requisitos e resultados esperados (API do Squash no Chrome, se disponível; senão, peça ao tester). Sem o caso, a revisão fica só no código, e o parecer diz isso.
- **O diff:** `git -C projetos/<repo> log --stat` e `git diff` da branch contra a base, para separar o que é deste teste do que já existia.

Plataforma: `projetos/totaluitest` = App (regras da skill `totaluitest-codigo`); `projetos/webuitest` = Web (regras da `webuitest-codigo`). Leia o `SKILL.md` e as referências da skill de código da plataforma antes de revisar: elas são a régua.

## 2. Conferir

Passe pelo `references/checklist.md`. Os blocos:

1. **Caso × código:** cada passo do Squash tem o `Passo N` no código, e cada resultado esperado tem asserção que o prova, com o valor.
2. **Falso positivo:** o teste falharia se o sistema estivesse errado?
3. **Asserções:** fortes, completas, com o valor esperado concreto.
4. **Esperas e estabilidade:** nada de espera fixa; espera onde a tela ou o valor demoram.
5. **Massa e dados:** bate com o caso, é da própria classe, limpa o que criou (Web), datas dinâmicas, parâmetro JSON certo.
6. **Padrão e documentação:** JavaDoc com Squash e Jira, comentários de passo, nomes, Page, encoding.
7. **Escopo:** não alterou código de produção nem outro teste sem motivo.

## 3. Rodar

Se o ambiente permitir (JDK, Maven, Tomcat para a Web, base para o App):

- rode **só este teste, três vezes seguidas**;
- registre o resultado de cada rodada e o tempo;
- passou nas três: estável; falhou em alguma: instável (veja a causa com o método da `analise-logs-jenkins`); falhou nas três: quebrado.

Não deu para rodar: diga por quê no parecer. **Nunca aprove "às cegas" o que depende de rodar**: sem rodada, o melhor status possível é APROVADO COM OBSERVAÇÕES, com a pendência escrita.

**Prova de que o teste pode falhar** (para as asserções principais, quando for barato): mude o valor esperado no código **numa cópia temporária** ou descreva o raciocínio; o teste tem de falhar. Nunca deixe a alteração no arquivo.

## 4. Classificar

| Severidade | Exemplos |
|---|---|
| **CRÍTICO** | falso positivo (passa sem testar: `return`, `if`, `try/catch` que engole, assert de uma variável com ela mesma); teste não compila ou não roda; encoding corrompido (`�`); alteração no código de produção do app; massa que apaga ou altera dado de outros testes (`DELETE` sem `WHERE`); credencial no código |
| **ALTO** | resultado esperado do Squash sem asserção; asserção fraca onde o valor é o objetivo (`assertNotNull`, `contains` no lugar da string completa); parâmetro JSON fora de `PARAMETROS_JSON` (o `Map` não grava); data fixa; teste que depende de outro ou da ordem; espera fixa (`sleep`); Web que grava e não limpa; instável nas rodadas |
| **MÉDIO** | espera faltando ou no lugar errado (risco de instabilidade); massa divergente do caso; massa vinda de util compartilhado; JavaDoc sem Squash ou Jira; passo sem Resultado Esperado; mensagem de asserção que não corresponde ao campo; método novo em Page sem necessidade (já existia um) |
| **BAIXO** | nome fora do padrão; variável intermediária desnecessária; variável não `final` usada mais de uma vez; import sobrando; comentário de passo de uma linha |
| **INFO** | dívida que já estava no repositório; sugestão de melhoria fora do teste |

Antes de registrar um CRÍTICO ou ALTO, **confirme**: mostre o trecho que prova, ou a rodada que falhou. Registre também os **destaques positivos**.

## 5. Parecer

Modelo em `references/parecer.md`. Grave em `projetos/<repo>/target/revisao-teste/<Classe>-review.md` (a pasta `target/` não vai para o git), em português, LF.

| Status | Quando |
|---|---|
| **APROVADO** | nenhum CRÍTICO, ALTO nem MÉDIO; rodou três vezes e passou |
| **APROVADO COM OBSERVAÇÕES** | nenhum CRÍTICO nem ALTO; MÉDIOs poucos e não bloqueantes, ou não deu para rodar |
| **MUDANÇAS SOLICITADAS** | algum CRÍTICO ou ALTO |

Ao terminar, devolva em poucas linhas: o status, os CRÍTICOs e ALTOs (uma linha cada) e o caminho do parecer.

## Depois (na sessão principal)

- **MUDANÇAS SOLICITADAS:** quem escreveu corrige (pela `totaluitest-codigo` ou `webuitest-codigo`) e pede nova revisão.
- **Aprovado:** ofereça comentar o resumo do parecer na Test Automated (pelo Chrome, com aprovação) e seguir para a `fechar-test-automated`.

## Armadilhas

- **Teste verde não é teste certo.** O defeito mais grave de um teste é passar quando o sistema está errado; procure isso primeiro.
- **`waitValue` falha como Error, não como Failure** (App): não confunda uma rodada vermelha por divergência de valor com problema de ambiente.
- **`PARAMETROS_JSON`:** parâmetro JSON fora da lista é ignorado em silêncio pelo `Map`; confira a lista no `ParametrosTestUtil`.
- **Teste do padrão antigo** (JavaDoc com CT-LVP, `// passo 1`) no meio do repositório não é régua: a régua é a skill de código da plataforma.
- **Rodar muda a base:** no App, a execução grava na cópia da base do teste (`dadosTest/<Classe>/`); na Web, o banco de dev não tem reset. Rodar três vezes é também um teste de limpeza.
- **Não deixe nada alterado:** prova de falha em cópia temporária; confira `git status` no fim.

## Cuidados

- Somente leitura no código e no Jira; o único arquivo gravado é o parecer.
- Não suba nem derrube Tomcat ou agente tcui sem combinar; se o ambiente não está de pé, registre e revise sem rodar.
- Não exponha senha nem dado de cliente no parecer.
