# Formatação da descrição no Jira

O Jira da WMW (8.14) tem dois modos no campo Description: **Visual**, com a barra de ferramentas (estilo do parágrafo, menu "+" / Other), e **Text**, que aceita marcação de texto (wiki markup). A marcação produz exatamente os mesmos formatos que a barra, e digitar texto é muito mais confiável no navegador do que clicar em menus. Por isso:

1. escreva a descrição no modo **Text** com a marcação abaixo;
2. troque para o modo **Visual** e confira se cada parte saiu no formato certo;
3. se algo não renderizou (texto `h2.` aparecendo literal, tabela quebrada), corrija no modo Text.

## Correspondência

| Formato pedido | Marcação no modo Text | Observações |
|---|---|---|
| Heading 2 | `h2. Descrição` | em linha própria, com linha em branco antes e depois |
| Paragraph | texto comum | parágrafos separados por uma linha em branco |
| Paragraph quote | `bq. texto` (um parágrafo) ou `{quote}` … `{quote}` (vários parágrafos) | para citação literal do erro ou de documentação; cite a fonte logo depois, em Paragraph |
| Bloco de código (Other → Code) | `{code}` … `{code}` | com linguagem quando for código: `{code:java}`, `{code:sql}`, `{code:xml}`. Log também vai em `{code}` |
| Tabela (Other → Table) | `\|\|Cabeçalho 1\|\|Cabeçalho 2\|\|` e depois `\|valor\|valor\|` por linha | uma linha da tabela por linha de texto, sem linha em branco no meio |
| Horizontal ruler | `----` | em linha própria |
| User mention | `[~usuario.jira]` | o nome de usuário do Jira (ex.: `larissa.faustino`), não o nome de exibição. No modo Visual, digitar `@` e escolher na lista dá o mesmo resultado |
| Lista numerada | `# passo` | uma linha por item; use nos passos para reproduzir |
| Lista com marcadores | `* item` | |

## Exemplo

Prévia (como aparece no chat para aprovação):

```markdown
## Descrição
Na aba Cashback do Pedido (App), ao aplicar um cupom acima do permitido, o sistema ajusta o valor e exibe:
> O valor do cashback foi ajustado para R$4.799,99, o maior valor que pode ser distribuído entre os itens do pedido.

## Resultado atual
| Campo | Reportado | Esperado | Diferença |
|---|---|---|---|
| Cashback total | 135.326,95 | 133.504,74 | 1.822,21 |
```

Marcação digitada no modo Text:

```
h2. Descrição

Na aba Cashback do Pedido (App), ao aplicar um cupom acima do permitido, o sistema ajusta o valor e exibe:

bq. O valor do cashback foi ajustado para R$4.799,99, o maior valor que pode ser distribuído entre os itens do pedido.

h2. Resultado atual

||Campo||Reportado||Esperado||Diferença||
|Cashback total|135.326,95|133.504,74|1.822,21|
```

## Caracteres que mudam o texto

No modo Text, alguns caracteres viram formatação. Quando forem texto, escape com `\`:

| Caractere | Vira | Escrever como texto |
|---|---|---|
| `*texto*` | negrito | `\*` |
| `_texto_` | itálico | `\_` |
| `-texto-` | riscado | `\-` (ex.: valores negativos colados a texto) |
| `+texto+` | sublinhado | `\+` |
| `[texto]` | link | `\[texto\]` |
| `{texto}` | macro | `\{texto\}` |
| `\|` dentro de célula de tabela | nova coluna | `\|` já escapado |
| `#` ou `*` no início da linha | lista | comece a linha com outra palavra, ou escape |

Exceção: as métricas do Test de Delivery (`[DiasEstimados:4.5]`) vão sem escape, como nas atividades existentes (ver `references/test.md`).

Dentro de `{code}` nada disso vale: o conteúdo fica literal. Por isso logs e trechos com muitos símbolos vão sempre em bloco de código.

## Erros comuns

- Esquecer a linha em branco antes de `h2.`: o título gruda no parágrafo anterior.
- Linha em branco no meio da tabela: a tabela vira duas.
- Colar log fora de `{code}`: `*`, `_` e `[` do log viram formatação.
- Usar `**negrito**` ou `## título` do Markdown: o Jira não entende e mostra os símbolos.
