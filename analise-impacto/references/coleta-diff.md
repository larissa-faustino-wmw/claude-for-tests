# Coleta do diff

Os repositórios ficam em `projetos/` da raiz do workspace (`C:\WMW\dev\wmwvendas\projetos\<repo>` na máquina do time). Tester sem os repositórios: oriente a clonar antes (ver o `CLAUDE.md` da raiz do workspace).

Sempre com `git -C projetos/<repo>` e referências `origin/...`: **nunca** `checkout`, `pull`, `reset` ou qualquer comando que mude o branch ou os arquivos de trabalho do tester.

## Repositórios a olhar

| Repositório | O que tem |
|---|---|
| `lavenderepda` | app (telas, services, DAO, sync do lado do app) |
| `lavendereweb` | telas web (xhtml, managed beans) |
| `lavenderecore` | regra de negócio e persistência do web (services, domain, sqlmap) |
| `framework-*` | só se a branch existir neles: mudança de framework afeta tudo o que usa o componente |

## O fluxo das branches

| Branch | O que tem |
|---|---|
| `main` | a última versão liberada. **É sempre a base do comparativo** |
| `release` | a versão em teste na semana de Delivery (a `develop` incrementada na `release` pelo facilitador), mais as correções feitas durante a Delivery |
| `develop` | as atividades já liberadas pelo QA, a caminho da próxima versão; durante a Delivery já recebe a sprint seguinte |
| `*VENDAS-xxxxx*` | a branch da atividade, trabalhada pelo dev e testada pelo QA antes de ir para a `develop` |

Ciclo: atividade testada → incrementada na `develop` → na Delivery, `develop` → `release` → testes → `release` → `main` → versão liberada → `main` → `develop`.

Consequências para a análise:

- `origin/main..<qualquer branch>` = tudo o que ainda não foi liberado nela. Limita a busca e descarta o histórico antigo.
- Uma branch de atividade carrega também o que já estava na `develop` e não foi liberado. Por isso a atividade se isola **pela chave**, dentro de `main..branch`.

## 1. Atualizar e achar a branch

```
git -C projetos/<repo> fetch --quiet origin
git -C projetos/<repo> branch -r --list "*VENDAS-xxxxx*"
```

As branches levam a chave no nome com prefixos variados (`origin/VENDAS-25440`, `origin/Angel-VENDAS-10781`, `origin/Branch_VENDAS-18185`). Mais de uma branch com a chave: use a de commit mais recente (`git log -1 --format=%ci origin/<branch>`) e cite as outras.

## 2. Os commits da atividade

Base `main`, filtro pela chave:

```
git -C projetos/<repo> log origin/main..origin/<branch> --no-merges --format="%h %ci %s" --grep="VENDAS-xxxxx"
git -C projetos/<repo> show --stat --format="%h %s" <commit>
git -C projetos/<repo> show <commit> -- <arquivo>
```

Sem o filtro, o diff traz o trabalho de outras atividades. Conferido em VENDAS-25440 (10/11/2026): `git diff --stat origin/main...origin/VENDAS-25440` deu 27 arquivos, com commits de VENDAS-25356, VENDAS-25204 e da versão 9.064-7; filtrando pela chave, 1 commit e 5 arquivos.

- Junte os arquivos de todos os commits da atividade: é esse o escopo da análise.
- Mais de um commit no mesmo arquivo: leia o efeito final com `git diff <primeiro commit>^ <último commit> -- <arquivo>`, mas só para os arquivos da atividade.
- A atividade tem commits sem a chave na mensagem (o tester ou o dev avisam, ou o resumo não bate com o que se esperava)? Liste `git log origin/develop..origin/<branch> --no-merges --format="%h %s"` (o que a branch tem e a `develop` ainda não) e descarte os que têm a chave de outra atividade.
- Subtask: o commit leva a chave da principal e a da subtask; procure pelas duas.

## 3. Branch já mergeada ou apagada

A mensagem de commit do time leva o código da atividade (subtask leva também o da principal):

```
git -C projetos/<repo> log origin/main..origin/develop --no-merges --oneline --grep="VENDAS-xxxxx"
git -C projetos/<repo> show --stat <commit>
```

Na semana de Delivery, procure também em `origin/main..origin/release`. Se o commit já está na `main`, a atividade já foi liberada: a análise vira de reteste (Bug que voltou), e o código a olhar é o da correção nova.

## 4. Classificar os arquivos

| Tipo | Como reconhecer | Por que importa |
|---|---|---|
| Domain | `business/domain/`, `TABLE_NAME` (app) ou `@TableName` (web) | coluna nova ou mudada afeta sync, telas e relatórios da entidade |
| DAO / sqlmap | `integration/dao/`, `*.xml` de sqlmap | consulta mudada afeta todas as telas que listam a entidade |
| Service | `business/service/` | regra mudada afeta todos os chamadores |
| Tela | `presentation/ui/` (app), `*.xhtml` e managed bean (web) | impacto local, mas veja componentes compartilhados (base, abstract) |
| Parâmetro | `LavenderePdaConfig`, `ConfigParametro`, `ValorParametro` | todos os pontos que leem o mesmo parâmetro |
| Sincronização | DTOs e classes de sync, `30-correspondencia-app-web.md` | dado que não chega ou chega errado na outra stack |
| Mensagens | `Messages_*.properties` | texto que o tester valida; quebra asserts do `totaluitest` |
| Script de banco | `docs/modelo-er/scripts`, menção a script do wadmin | atualização de versão, bases de cliente |

Fontes `.java` estão em ISO-8859-1: acentos podem aparecer tortos no diff.
