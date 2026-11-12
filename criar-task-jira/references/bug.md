# Bug — bug interno

**Guia:** [GUIA-JIRA-001 - Como criar atividade de bugs internos no Jira](https://confluence.wmw.com.br/confluence/x/EADdQQ) (conferido na versão 4, em 10/11/2026). Se o guia mudar, atualize este arquivo.

Bug encontrado pelo time de testes **fora de uma atividade em teste** (sem atividade pai). Se o bug apareceu testando uma Story ou um Bug, o tipo certo é **Defect** (`references/defect.md`): confirme com o tester.

Criação: botão **Create** → Project `Vendas` ou `E-Commerce` → Issue Type `Bug`.

## Verificações antes de abrir (do guia)

1. Parâmetros relacionados ao problema e se houve alteração recente nos valores.
2. Documentação do processo, funcionalidade ou parâmetro.
3. Se não é uma melhoria não prevista em documento (aí não é Bug: conversar com o líder sobre Story ou Suggestion).

O guia do Bug **não** pede verificar na develop (o do Defect pede). (sugestão) Se o tester souber em que versão ou ambiente ocorre, registre na Descrição.

## O que já existe (antes de perguntar)

A busca por palavras-chave do `SKILL.md`. Inclua os Defects na busca (`issuetype in (Bug, Defect)`): o mesmo problema pode já ter sido reportado testando alguma atividade.

## O que perguntar (só o que faltar)

- **Projeto**: `Vendas` ou `E-Commerce`, se o relato não deixar claro.
- **Phase**: `Manual testing` ou `Automated testing`. Nunca assuma.
- **Environment**: `Web`, `App` e/ou `Other`.
- **Referências abertas, massa de dados, resultado esperado e evidências**: como no Defect (`references/defect.md`, "O que perguntar").

## Campos

Iguais aos do Defect (`references/defect.md`), com estas diferenças:

| Campo | No Bug |
|---|---|
| Issue Type | `Bug` |
| Project | `Vendas` ou `E-Commerce` |
| Priority | `Medium`; **sempre `Highest` quando Phase = `Automated testing`** |
| SDLC phase | `Development` = encontrado durante o desenvolvimento ou os testes da demanda, antes de ir para a develop ou para versão oficial/hotfix; `Delivery` = no processo de delivery da versão; `Homologation` = na homologação do sistema/funcionalidade (pouco usado pelo time de desenvolvimento); `Production` = encontrado pelo cliente usando a versão. Deduza do relato; pergunte se não der |

## Modelo de descrição

O mesmo do Defect: Descrição, Passos para reproduzir, Resultado atual, Resultado esperado e Backup/Carga disponível, cada título em Heading 2 (ver `references/defect.md`).
