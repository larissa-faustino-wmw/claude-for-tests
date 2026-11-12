# Testes flaky no TotalUiTest — causas e correções

Use quando um teste for confirmado ou suspeito de flaky. Para cada caso, aponte a causa mais provável pela evidência e proponha uma mudança no teste. **Aumentar timeout não é correção**: o `TIME_WAIT` já é de 30 s no Linux; se 30 s não bastaram, a condição esperada está errada ou o app travou.

## Como confirmar

- **Mais de um build com o mesmo commit**: peça os logs e compare o histórico do teste.
- **Rerun no mesmo build**: o pom vem com `rerunFailingTestsCount=0`. Para medir, rode com `-Dsurefire.rerunFailingTestsCount=2`; `Run 1: FAIL / Run 2: PASS` confirma.
- **Localmente**: rode a classe isolada várias vezes (`mvn test -Dtest=<Classe> -Denv.test=develop -Duser.language.format=pt -Dfile.encoding=ISO-8859-1`) e depois junto com as classes que rodavam em paralelo no Jenkins. Passar sozinha e falhar junto aponta interferência (item 5).

## Catálogo

### 1. Ler o valor antes de ele estar pronto
- **Sinal**: `AssertionFailedError` com valor vazio, zero ou o valor anterior; às vezes passa.
- **Causa**: `getValue(...)` seguido de `assertEquals` imediato, enquanto o app ainda recalcula (total do pedido, impostos, desconto).
- **Correção**: trocar por `waitValue(valorEsperado, id)` — ele espera o valor chegar e, se não chegar, mostra `Expected/Actual` no log.

### 2. Esperar a tela, mas não o conteúdo
- **Sinal**: elemento de lista/grid não encontrado logo depois de um `waitOpening` que passou.
- **Causa**: `waitOpening` retorna quando a janela existe e terminou de pintar, não quando a lista terminou de carregar.
- **Correção**: esperar o que o passo seguinte usa — `waitOpeningList(idList)`, `waitOpeningActiveTabs(...)` ou `waitValue` no campo que vai ser lido.

### 3. Espera fixa
- **Sinal**: `Thread.sleep`/`expecTime(<ms>)` no passo anterior à falha.
- **Correção**: substituir por uma condição (itens 1 e 2). Espera fixa é curta no agente lento e desperdício no rápido.

### 4. Massa compartilhada entre métodos da mesma classe
- **Sinal**: o método falha quando roda depois de outro da mesma classe; sozinho, passa.
- **Causa**: a classe usa a mesma cópia de banco; um método grava (pedido, saldo, flag) e o outro assume o estado inicial. `@InvokeInit(unique = true)` roda a massa uma vez só por classe, não antes de cada método. A ordem dos métodos no JUnit 5 não é garantida sem `@TestMethodOrder`.
- **Correção**: tornar cada método independente — massa por método (`@InvokeInit` sem `unique`), ou limpar o que o método criou; só use `@TestMethodOrder` quando a sequência for o próprio cenário.

### 5. Interferência entre execuções paralelas
- **Sinal**: falha só no Jenkins (4 forks, `parallel=classes`); assinatura muda a cada vez; passa sozinha.
- **Causa**: recurso compartilhado fora do banco da classe — arquivos em `dadosTest/`, arquivos temporários ou de configuração do app, o banco base em `./db/<versão>/`.
- **Correção**: identificar o recurso e isolar por classe; como contorno, agrupar as classes que disputam o recurso numa execução sem paralelismo. Registre quais classes rodavam juntas.

### 6. Data e hora
- **Sinal**: falha em horário específico (virada de minuto/hora/dia, fim de mês) ou depois de uma data.
- **Causa**: massa com data fixa que venceu (validade de preço, prazo, campanha), comparação de horário que cruza o minuto, diferença de fuso entre Windows local e agente Linux.
- **Correção**: gerar datas relativas a hoje na massa; para horário, o framework tem `expectChageMinute()` (espera virar o minuto) — use antes de passos sensíveis ao minuto.

### 7. Diálogo ou aviso assíncrono por cima
- **Sinal**: `DriverClickException … Não está visivel na tela` ou `is an instance of` com uma janela inesperada; o print mostra uma mensagem.
- **Causa**: aviso que aparece só às vezes (sincronização, mensagem de sistema, popup condicionado a dado) intercepta o clique.
- **Correção**: tratar o aviso explicitamente quando ele faz parte do fluxo, ou montar a massa para que ele não apareça.

### 8. Ordem não determinística
- **Sinal**: o teste clica no "primeiro item" e às vezes pega outro.
- **Causa**: consulta sem `ORDER BY` estável; a ordem varia com o banco/SGBD.
- **Correção**: selecionar o item pelo código/descrição, não pela posição.

### 9. Ambiente instável
- **Sinal**: vários testes sem relação falham em espera no mesmo intervalo; fork morto; Xvfb/TotalCross com erro; sem assinatura em comum.
- **Correção**: não é do teste. Reexecutar e, se repetir, levar ao responsável pelo agente com o horário e o build.

## O que dizer quando não dá para confirmar

Com um build só, escreva "suspeito de flaky", diga qual item do catálogo o padrão sugere e peça o log de outros builds (ou um rerun) para confirmar.
