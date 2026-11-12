---
name: analise-logs-jenkins
description: Analisa logs de execução de testes automatizados TotalUiTest (console do Jenkins, saída Maven/Surefire no terminal ou na IDE, relatórios surefire-reports XML) para listar as classes com falha ou erro, classificar a causa (problema no teste, ambiente/infra ou provável bug do produto), investigar testes flaky e sugerir como estabilizá-los, e orientar o QA Tester sobre como resolver ou reportar. Use SEMPRE que o usuário colar ou anexar um log do Jenkins, um consoleText, um trecho com "Tests run:", "BUILD FAILURE", "<<< FAILURE!", DriverWaitException, TimeoutException, AssertionFailedError, ou perguntar por que o build/pipeline/job quebrou, quais testes falharam, se um teste é flaky, por que um teste "às vezes passa às vezes não", ou pedir para analisar a execução noturna — mesmo que diga só "olha esse log" ou "o que aconteceu aqui?".
---

# Análise de logs de execução — TotalUiTest

Objetivo: transformar um log longo e barulhento em um diagnóstico que o QA Tester consiga agir em minutos. Quem lê é alguém do time de QA da WMW; responda **sempre em português do Brasil**, mesmo que o log, a pergunta ou o código estejam em inglês.

O que importa é a causa, não a transcrição do log. Um log do Jenkins tem milhares de linhas de pipeline, Maven e warnings de checksum; a informação útil cabe em poucas dezenas. Seu valor está em achar essas linhas, cruzá-las e dizer o que fazer.

## 1. Extrair os fatos

Não leia o log de cima para baixo: um consoleText tem milhares de linhas. Se ele foi colado no chat, salve-o em um arquivo e procure com busca (Grep) pelos sinais abaixo, depois leia só o contexto em volta de cada um.

| O que levantar | Onde procurar |
|---|---|
| Totais e status | `Tests run:` (o último é o total), `BUILD SUCCESS`/`BUILD FAILURE`, `Total time` |
| Falhas por método | `<<< FAILURE!`, `<<< ERROR!`, bloco `[ERROR] Failures:` / `[ERROR] Errors:` do resumo; nos XML, `<failure` e `<error` dentro de `<testcase` |
| Linha do teste | o primeiro frame `at br.com.wmw…Test.<metodo>(<Classe>Test.java:<linha>)` da stack |
| O que se esperava | as linhas logo abaixo de `TimeoutException` (`Expected : / Actual :`, `Expected Condition: …`) |
| Stack traces soltas | `Exception` com frames `totalcross.` ou `br.com.wmw.` fora do bloco de um teste; anote o horário/fork e qual teste rodava |
| Testes sem fim | `Running <Classe>` sem o `Tests run: … in <Classe>` correspondente; `The forked VM terminated` |
| Rerun / flaky | `Flakes:`, `Run 1:`, `flakyFailure`, `flakyError` |
| Pulados em cascata | `Skipped` alto com `skipAfterFailureCount` (ver referência) |
| Credenciais | `password`, `senha`, `token`, `Authorization`, `cookie` |

Aceite consoleText/.txt/.log, `TEST-*.xml` do Surefire e pastas (`target/surefire-reports`). Com **vários builds**, monte uma tabela teste × build (passou/falhou) para ver quem alterna. Com log grande, um script curto em Python na pasta temporária para contar e agrupar por assinatura (classe da exceção + primeira linha da mensagem) economiza leitura.

## 2. Classificar cada falha

Para cada teste com falha ou erro, decida **uma** categoria e diga o porquê com evidência do log:

| Categoria | Quando | Exemplos típicos |
|---|---|---|
| **Problema no teste** | o script, a massa ou a espera estão errados ou frágeis | localizador errado, massa que outro teste altera, espera curta, assert com valor fixo desatualizado |
| **Ambiente / infra** | a culpa é do lugar onde rodou | ambiente fora do ar, banco baixado incompleto, Xvfb/TotalCross instável, agente sem recurso, timeout do pipeline |
| **Provável bug do produto** | o app se comportou diferente do esperado de forma consistente | valor calculado errado em mais de um teste, mensagem que deixou de aparecer, NullPointerException em código `br.com.wmw` |

Use "provável" quando faltar prova; diga o que confirmaria. Os sinais que ajudam a decidir estão em `references/padroes-totaluitest.md` — leia quando houver `DriverWaitException`, `TimeoutException`, stack trace solta, ou quando a categoria não estiver óbvia.

Cruzamentos que mais mudam o diagnóstico:

- **Mesma assinatura em vários testes** → quase sempre uma causa só (massa compartilhada, regressão no produto, ambiente). Trate como um item, não como N problemas.
- **Stack trace solta da aplicação perto de uma falha de espera** → se uma exceção do app (`NullPointerException` em `totalcross.*` ou `br.com.wmw.*`) aconteceu enquanto o teste rodava e, segundos depois, ele falhou esperando uma tela ou botão, a tela provavelmente não abriu porque o app quebrou. A falha de espera é sintoma; a exceção é a causa.
- **Erro (Errors) x Falha (Failures)**: `Failure` = um assert comparou e deu diferente (o app respondeu, mas errado — olhe produto ou massa). `Error` = o teste não conseguiu chegar ao assert (espera, elemento, exceção — olhe timing, ambiente, crash do app). **Exceção no TotalUiTest:** `waitValue` que não bate vira `DriverWaitException` com `Expected : … / Actual : …` — aparece como Error, mas é divergência de valor; trate como Failure.
- **Execução paralela** (`-Dexecs=N`, padrão 4): testes que mexem no mesmo recurso podem interferir entre si. Note quais rodavam juntos.
- **Skipped em cascata**: o pom usa `skipAfterFailureCount=1` — depois da primeira falha os testes seguintes são pulados. Não trate os pulados como problemas próprios.

## 3. Flaky

Um teste é flaky quando falha e passa **sem mudança de código**. As evidências, da mais forte para a mais fraca:

1. Passou no rerun do mesmo build (bloco `Flakes:` do Surefire, `flakyFailure`/`flakyError` no XML, `Run 1: … Run 2: PASS`).
2. Alterna entre builds com o mesmo commit (tabela teste × build, ou o que o usuário contar).
3. Jenkins ou plugin marca como flaky.
4. Apenas um build disponível: **não afirme que é flaky**. Diga "suspeito de flaky" quando o padrão do erro for típico de instabilidade (espera/timeout sem exceção do app, sem assinatura repetida) e peça os logs de outros builds para confirmar.

Para cada flaky, aponte a fonte provável de instabilidade e uma mudança concreta no teste. O catálogo de causas e correções está em `references/flaky.md`. Sugira correções que ataquem a causa (esperar o estado certo, isolar a massa) e não apenas aumentar timeout — aumentar timeout esconde o problema e deixa a suíte mais lenta.

## 4. Com acesso ao projeto (IDE/terminal)

Quando houver acesso ao repositório `totaluitest`, não pare no log — confirme no código:

1. Abra a classe na linha apontada (ex.: `EfetuarPagamentoPadraoTest.java:76`) e o passo anterior: qual tela, qual botão, qual valor.
2. Veja a massa (`@InvokeInit`, `ParametrosTestUtil`, `TabelasTestUtil`) e se outros testes usam os mesmos registros.
3. Abra o Page Object envolvido para ver como a espera é feita.
4. `git log` recente nos arquivos do teste (`totaluitest`) e da tela ou regra envolvida no produto (`lavenderepda`, outro repo), quando disponíveis: uma mudança recente explica muita coisa.
5. Se o problema for do teste, proponha o ajuste no código (diff ou trecho). Se for do produto, mostre a evidência e o caminho para reproduzir manualmente.

Não altere arquivos do projeto sem o usuário pedir; proponha.

## 5. Orientar o QA Tester

Para cada item, diga o próximo passo de forma que um tester consiga executar:

- **Problema no teste**: o que corrigir e onde (classe, linha, Page Object, massa).
- **Ambiente / infra**: o que verificar (ambiente, banco baixado, agente) e quando vale apenas reexecutar.
- **Provável bug**: como reproduzir manualmente no app (cliente/pedido/parâmetro da massa), que evidência juntar (trecho do log, print, banco), e que a falha deve ser reportada como Defect. Oriente; não monte o Defect a menos que peçam (para isso existe a skill `criar-task-jira`).

## 6. Formato da resposta

Responda em português do Brasil, neste formato (ajuste o tamanho ao tamanho do problema — um build com uma falha não precisa de cinco seções cheias):

```markdown
## Resumo — build #<n> (<status>)
<total> testes · <falhas> falhas · <erros> erros · <flakes> flaky · <duração>
<1–2 frases: o que aconteceu, em linguagem direta>

## Testes com problema
| Classe | Método | Tipo | Causa provável | Categoria |
|---|---|---|---|---|
| <Classe>Test | <metodo> (linha) | Falha/Erro | <curta> | Teste / Ambiente / Provável bug |

## Diagnóstico
### <Grupo ou teste>
- **Evidência:** <linhas do log que sustentam — trechos curtos>
- **Por que acho isso:** <raciocínio>
- **O que confirmaria:** <quando não houver certeza>

## Flaky
<por teste: evidência, causa provável, mudança sugerida no teste — ou "nenhum confirmado; suspeitos: …">

## Próximos passos para o QA Tester
1. <ação concreta, por ordem de prioridade>

## Observações do pipeline
<avisos de configuração, encoding, credenciais expostas etc. — só se houver>
```

Agrupe no Diagnóstico os testes que têm a mesma causa. Nomes de classe, método e exceção ficam como estão no log (não traduza código).

## Armadilhas

- **`waitValue` falha como Error, não como Failure.** A mensagem `Expected : / Actual :` vem dentro de um `DriverWaitException`. É divergência de valor (assert), não problema de infraestrutura: não classifique pela palavra Error.
- **`waitOpening` engole a causa.** "Erro ao esperar a tela X abrir." não traz o motivo original. Procure o print em `dadosTest/<Classe>/imagens/<metodo>/` e a linha anterior do log.
- **`checkInError` é mensagem do app.** `DriverClickException` com um texto de negócio é uma WmwMessageBox de erro do produto: suspeite de massa ou de bug, não do teste.
- **Skipped não é falha.** Com `skipAfterFailureCount=1`, depois da primeira falha o Surefire pula o resto. Conte só os que falharam de fato.
- **Paralelismo esconde dependência.** `parallel=classes`, 4 forks e `reuseForks=false`: teste que só falha no Jenkins pode depender de dado de outra classe rodando ao mesmo tempo.
- **`println` não aparece.** Com `disable.system.out=true`, saída de console do teste não vai para o log.
- **Timeout diferente por SO.** `TIME_WAIT` é 20 s no Windows e 30 s no Linux: o mesmo teste pode passar no Jenkins e estourar na máquina do tester.

## Cuidados

- **Credenciais**: logs de pipeline às vezes trazem senha, token ou cookie em texto puro. Nunca reproduza esses valores na resposta; avise que o log expõe credenciais e sugira mascarar no Jenkins (ex.: `withCredentials`).
- **Caracteres corrompidos** (`D�bito`) são problema de encoding do log, não do teste. Leia como o texto original ("Débito") e mencione o aviso uma vez em Observações.
- Separe fato de hipótese. "O log mostra X" é fato; "provavelmente Y" é hipótese — deixe claro qual é qual.
