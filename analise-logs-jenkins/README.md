# analise-logs-jenkins

Skill do Claude que lê o log de uma execução de testes automatizados do **TotalUiTest** e devolve um diagnóstico pronto para agir: quais testes falharam, por quê, se o problema é do teste, do ambiente ou do produto, e o que o tester deve fazer em seguida.

## Para que serve

Um console do Jenkins tem milhares de linhas, e a informação útil cabe em algumas dezenas. A skill encontra essas linhas, junta as que têm a mesma causa e explica em português:

- **lista os testes com falha ou erro**, com a classe, o método e a linha;
- **classifica cada falha** em uma de três categorias, sempre com o trecho do log que comprova:
  - **Problema no teste**: espera, massa ou localizador errado;
  - **Ambiente / infra**: banco não baixado, agente sem recurso, fork que morreu;
  - **Provável bug do produto**: o app se comportou errado de forma consistente;
- **agrupa as falhas que têm a mesma causa**, para que dez testes quebrados pela mesma regressão virem um item só;
- **investiga testes flaky** (que às vezes passam e às vezes não): diz se dá para confirmar, qual a causa provável e o que mudar no teste;
- **orienta o próximo passo**: corrigir o teste, reexecutar ou reproduzir manualmente e abrir um Defect.

## Quando usar

A skill entra sozinha quando você:

- cola ou anexa um log do Jenkins, um `consoleText`, a saída do Maven na IDE ou os XML de `target/surefire-reports`;
- cola um trecho com `Tests run:`, `BUILD FAILURE`, `<<< FAILURE!`, `DriverWaitException`, `TimeoutException` ou `AssertionFailedError`;
- pergunta coisas como "por que o build quebrou?", "quais testes falharam?", "esse teste é flaky?" ou "analisa a execução noturna";
- ou só diz "olha esse log" ou "o que aconteceu aqui?".

Para chamar direto: `/analise-logs-jenkins`.

## Como usar

1. Baixe o log do build (no Jenkins: **Console Output → View as plain text**, ou o `consoleText` do job) e cole no chat ou anexe o arquivo.
2. Se quiser saber se um teste é flaky, **mande o log de dois ou mais builds** do mesmo commit. Com um build só, a skill no máximo diz "suspeito de flaky".
3. Se tiver, mande também o **print da falha** (`dadosTest/<Classe>/imagens/<metodo>/`). Ele resolve a maioria dos erros "Erro ao esperar a tela X abrir".
4. Se estiver no Claude Code com o repositório `totaluitest` aberto, a skill confere no código: abre a classe na linha da falha, a massa (`@InvokeInit`) e o Page Object. Ela **propõe** a correção, mas não altera arquivos sem você pedir.

Exemplos de pedido:

```
Olha esse log da execução noturna, o que quebrou?  [anexo consoleText.txt]

Esse teste passou ontem e falhou hoje, é flaky?  [anexo build-120.txt e build-121.txt]

Por que o EfetuarPagamentoPadraoTest deu DriverWaitException?
```

## O que você recebe

```
Resumo — total de testes, falhas, erros, flaky e duração, mais 1 ou 2 frases sobre o que aconteceu
Testes com problema — tabela: classe, método, tipo, causa provável, categoria
Diagnóstico — por grupo: evidência do log, raciocínio e o que confirmaria a hipótese
Flaky — confirmados ou suspeitos, com causa e mudança sugerida no teste
Próximos passos para o QA Tester — em ordem de prioridade
Observações do pipeline — só se houver: credenciais expostas, encoding, configuração
```

O tamanho da resposta acompanha o problema: um build com uma falha recebe uma resposta curta.

## Bom saber

- **Senhas e tokens** que aparecem no log nunca são repetidos na resposta. A skill avisa e sugere mascarar no Jenkins.
- **Acentos estragados** (`D�bito`) são problema de encoding do log, não do teste.
- **Muitos testes "Skipped"** depois de uma falha são esperados: o projeto para de rodar testes novos após a primeira falha (`skipAfterFailureCount=1`).
- **No TotalUiTest, um valor errado pode aparecer como Error, não como Failure**: o `waitValue` que não bate vira `DriverWaitException` com `Expected : / Actual :`. A skill trata isso como divergência de valor.
- Para abrir o Defect depois do diagnóstico, use a skill `criar-task-jira`.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `SKILL.md` | as instruções que o Claude segue |
| `references/padroes-totaluitest.md` | as mensagens de erro do framework, o que cada uma significa e como decidir a categoria; configuração do Surefire; onde ficam prints e banco da falha |
| `references/flaky.md` | causas de testes instáveis no TotalUiTest, com sinal no log, correção e como confirmar |

As referências foram escritas a partir do código do `totaluitest` (branch `develop`, novembro/2026). Se o framework mudar (timeouts, mensagens, configuração do Surefire), atualize os dois arquivos.

## Instalação

Copie a pasta `analise-logs-jenkins/` inteira, com a subpasta `references/`:

- **Claude Code**: em `~/.claude/skills/`, ou em `.claude/skills/` do projeto;
- **claude.ai**: suba a pasta como skill nas configurações de Skills.

Sem a pasta `references/`, a skill funciona, mas perde o catálogo de erros e de flaky.
