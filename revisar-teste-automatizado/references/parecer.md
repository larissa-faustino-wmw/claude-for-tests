# Modelo do parecer

```markdown
# Revisão: <Classe>Test

**Data:** <AAAA-MM-DD> · **Plataforma:** App (totaluitest) / Web (webuitest) · **Test Automated:** <VENDAS-xxxxx> · **Caso:** <Reference do Squash, com link> · **Status:** <APROVADO | APROVADO COM OBSERVAÇÕES | MUDANÇAS SOLICITADAS>

## Resumo

<O que o teste prova, se prova o que o caso diz, e o que impede ou não a aprovação, em um parágrafo.>

## Arquivos revisados

| arquivo | situação |
|---|---|
| `src/test/java/.../<Classe>Test.java` | criado / alterado |
| `src/test/java/.../page/<...>Page.java` | método novo `<...>` |

## Rodadas

| # | resultado | tempo |
|---|---|---|
| 1 | passou / falhou (motivo) | 1m12s |
| 2 | | |
| 3 | | |

<Ou: "não rodado — <motivo>".>

## Caso × código

| Passo | No caso | No código | Situação |
|---|---|---|---|
| 1 | <resumo> | `Passo 1`, linha <n> | ✅ / ⚠️ / ❌ |

## Problemas

Cada um: **Onde** (`arquivo:linha`) · **O que** · **Por que importa** · **Correção sugerida**. Ou "Nenhum." na severidade.

### 🔴 CRÍTICO
### 🟠 ALTO
### 🟡 MÉDIO
### 🟢 BAIXO
### ℹ️ INFO

## ✅ Destaques

## Veredito

<Próximos passos, em ordem: o que corrigir, o que rodar de novo.>
```

O resumo para comentar na Test Automated (se o tester quiser) é o Status, o Resumo e a lista de CRÍTICOs e ALTOs, no modo Text do Jira.
