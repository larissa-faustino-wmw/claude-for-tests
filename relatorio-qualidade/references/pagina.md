# A página

Título: `Qualidade <versão>` (ex.: "Qualidade 9.068"). Subtítulo: data de liberação, data do corte e, se a versão tiver menos de 30 dias, o aviso "números ainda em maturação".

## Ordem das seções

**Para a gerência (topo, uma tela):**

1. **Placar** — quatro números grandes:
   - Contenção pela causa confirmada (com a cobertura do Issue Cause em letra menor);
   - Contenção pela versão afetada;
   - Escapes (problemas da versão);
   - Desvio do esforço da Delivery (realizado × planejado).

   Cada um com a variação contra a versão anterior (↑/↓ e pontos percentuais).
2. **Tendência** — um gráfico de linhas com as duas contenções nas últimas 5 versões, e barras discretas com os escapes por versão.
3. **Recomendações** — 3 a 5 itens curtos, cada um com a evidência e a ação.

**Para o QA (detalhe):**

4. **A versão em números** — entregas, correções, Defects internos, patches, horas.
5. **O que escapou** — tabela: chave (link), resumo, feature, prioridade, causa, Root Cause em uma frase.
6. **Onde doeu** — features com regressão confirmada ou suspeita; legado × mudança recente.
7. **Esforço da Delivery** — planejado × realizado, testers, clientes testados.
8. **Automação** — concluídas (de verdade × limpeza), fila, horas orçadas × reais e redução, bugs achados pela automação.
9. **Execução no Squash** — por iteração: passou, falhou, bloqueado, sem executar.
10. **Como ler** — as definições dos dois números de contenção e de "limpeza da fila", e as fontes (links das consultas e issues).

## Regras de conteúdo

- Números no formato brasileiro (`95,7%`, `169,4 h`, `20/10/2026`).
- Toda chave do Jira é link (`https://jira2.wmw.com.br/browse/<CHAVE>`).
- Seção sem dado: o título aparece, com "sem dado" e o motivo.
- Sem nome de pessoa em ranking ou comparação; o facilitador pode aparecer só como informação da Delivery.
- Texto curto: frases de leitura rápida, nada de parágrafos longos no topo.

## Forma

Siga a skill `artifact-design` (tokens de cor, modo escuro, largura de celular) e a `dataviz` para os gráficos (cores por série, sem legendas redundantes). Gráficos em SVG inline ou numa biblioteca permitida pela `artifact-design`. Nada de dado escondido só no gráfico: os valores estão também na tabela ou no rótulo.
