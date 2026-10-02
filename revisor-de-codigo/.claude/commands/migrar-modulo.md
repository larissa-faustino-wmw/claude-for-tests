---
description: Migra a massa de um modulo inteiro, um teste por vez, via subagente migrador-massa
argument-hint: <nome do modulo, ex.: pesquisa>
allowed-tools: Bash, Read, Edit, Write, Glob, Grep, Skill, Agent
---

Migre a massa de teste do modulo **$1**, um teste por vez.

Plano do modulo:

@.claude/refatoracao/$1/STATUS.md

Se o arquivo acima nao existir, rode
`python3 .claude/skills/migracao-massa-teste/scripts/massa.py plano` e liste os
modulos disponiveis em `.claude/refatoracao/` em vez de adivinhar o nome.

## Como executar

**1. Monte a fila.** Use a tabela "Ordem sugerida" do STATUS.md, de cima para
baixo. Pule linhas com estado `MIGRADO`. Anuncie a fila antes de comecar.

**2. Verifique a onda 0.** Se a secao "Bloqueios por causa raiz" disser que a
maior parte dos bloqueios some com mudanca nas utils, **pare e avise** antes de
migrar. Contornar o mesmo problema N vezes a mao e desperdicio -- a decisao de
seguir assim mesmo e do usuario, nao sua.

**3. Migre um por vez.** Para cada teste da fila, dispare o subagente
`migrador-massa` com o caminho do `.sql`. **Sequencial, nunca em paralelo:**
dois agentes editando massa ao mesmo tempo produzem conflito de contexto e
relatorio impossivel de auditar. Espere o relatorio de um antes de disparar o
proximo.

Nesta etapa os agentes **nao rodam Maven** -- so alteram codigo. A validacao e
em lote no passo 4, que e muito mais rapido que N inicializacoes do Maven.

Se um agente devolver `PRECISA DE DECISAO HUMANA`, nao decida por ele: registre
e siga para o proximo teste da fila.

**4. Valide o modulo em lote.** Rodar varias classes juntas e seguro: o
framework isola o banco por classe de teste
(`dadosTest/<NomeDaClasse>/dbs`, `BaseTotalUITest`), e o projeto ja roda com
`forkCount=4`.

```bash
# FASE A -- com os .sql ainda no lugar. Verde = o Java nao contradiz o SQL.
mvn test -Dtest=Teste1+Teste2+Teste3 -Denv.test=develop -Duser.language.format=pt -Dfile.encoding=ISO-8859-1

# FASE B -- sem os .sql. Verde = o Java se basta sozinho.
#   renomeie cada <Teste>.sql para <Teste>.sql.bak e rode de novo
mvn test -Dtest=Teste1+Teste2+Teste3 -Denv.test=develop -Duser.language.format=pt -Dfile.encoding=ISO-8859-1
```

Se a fase B ficar vermelha, **nao reverta o modulo inteiro**: identifique o
teste que quebrou, restaure so o `.sql` dele e trate individualmente.

Atencao ao ler o resultado: o surefire esta com `rerunFailingTestsCount=3`.
Um teste que falha e passa na repeticao aparece como sucesso no total. Procure
por "Flakes" na saida e trate como falha -- massa migrada pela metade costuma
se manifestar como intermitencia.

**5. Feche.**

```bash
# apagar os .bak so depois da fase B verde
python3 .claude/skills/migracao-massa-teste/scripts/massa.py encoding
python3 .claude/skills/migracao-massa-teste/scripts/massa.py plano
```

Escreva as decisoes do modulo no bloco de anotacoes do STATUS.md (abaixo do
marcador `<!-- ==== ANOTACOES`), que sobrevive a regeneracao.

## Relatorio final

Uma tabela com uma linha por teste -- teste, migrados/pendentes, fase A,
fase B -- e abaixo dela, em texto corrido:

- **Defeitos encontrados nos `.sql` originais** (statement quebrado, parametro
  que nunca foi aplicado). Reporte, nao conserte.
- **Mudancas de comportamento** aceitas (ex.: parametro JSON que passou de
  substituicao para patch).
- **Pendencias** que precisam de decisao humana, e de quem.

Se nao conseguiu rodar o Maven (sem VPN, `db/` vazio, dependencia do nexus
indisponivel), diga isso explicitamente e marque as fases como "nao executada".
Nunca reporte verde sem ter visto a saida do Maven.
