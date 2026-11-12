# Modelos de comentário (modo Text do Jira)

## Liberada

```
h2. Liberada pelo QA

*Ambiente:* <Tomcat de dev / homologação> · *Base:* <base> · *Branch:* <branch>

h2. Casos executados

[Squash - VENDAS-xxxxx|<link do requirement ou da iteração>]

||Status||Casos||
|Passou|<n>|
|Não testável|<n> (<motivo>)|

h2. Defects

||Defect||Situação||
|[VENDAS-aaaaa|https://jira2.wmw.com.br/browse/VENDAS-aaaaa]|corrigido e retestado|

h2. Side effects

<cobertos pelos casos X, Y; ou "não houve análise de impacto">
```

## Liberada com ressalva

O mesmo, com a seção:

```
h2. Ressalvas

* <pendência aceita> — aceita por [~<usuario>], segue em [VENDAS-bbbbb|https://jira2.wmw.com.br/browse/VENDAS-bbbbb]
```

## Devolvida ao dev

```
h2. Devolvida ao desenvolvimento

[~<usuario do dev>], a atividade voltou do teste pelos pontos abaixo.

h2. O que precisa ser feito

# <caso que falhou ou Defect aberto> — [VENDAS-aaaaa|https://jira2.wmw.com.br/browse/VENDAS-aaaaa]
# <commit depois do teste: reteste necessário>

h2. Já validado

<os casos que passaram, para não retestar tudo>
```

Regras: links do Jira sempre completos; nada de dado de cliente além do nome que já está na atividade; `*`, `_`, `[` e `{` soltos no texto precisam de escape (ver a `criar-task-jira`, `references/formatacao-jira.md`).
