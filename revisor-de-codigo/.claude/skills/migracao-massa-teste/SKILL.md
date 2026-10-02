---
name: migracao-massa-teste
description: Migra a massa de dados de um teste TotalCross UI do arquivo .sql fixo para o metodo @InvokeInit em Java usando ParametrosTestUtil e TabelasTestUtil. Use quando o pedido envolver converter/refatorar/migrar massa de teste, arquivo .sql de teste, prepararMassaDeDados, ParametrosTestUtil ou TabelasTestUtil. Nao use para escrever novos passos de teste ou Page Objects.
---

# Migracao da massa de teste: .sql -> @InvokeInit

## Onde esta o trabalho

`.claude/refatoracao/` tem o painel geral (`README.md`) e uma pasta por modulo
de `src/test/.../ui/test/`, cada uma com `STATUS.md`: inventario do modulo,
ordem sugerida de migracao e bloqueios por causa raiz.

Esses arquivos sao **gerados** e o estado de cada teste e deduzido do proprio
repositorio (existe `.sql`? existe `@InvokeInit`?), entao nao envelhecem.
Regenere apos migrar qualquer teste:

```bash
python3 .claude/skills/migracao-massa-teste/scripts/massa.py plano
```

Anotacoes manuais escritas abaixo do marcador `<!-- ==== ANOTACOES` sao
preservadas na regeneracao. Registre ali as decisoes do modulo.

## Contexto do mecanismo (leia antes de mexer)

Ordem de execucao real, em `BaseTotalUITest.invokeInit()`:

1. `executeMethods(pdaTotalUITestDataObject)` -> roda os `@InvokeInit` de
   `PDATotalUITestConfigureExtensionContext`, comecando por
   `invokeFileSql()` (`order = -1000`), que executa `<FQCN da classe>.ddl`
   e depois `<FQCN da classe>.sql`.
2. `executeMethods(getRequiredTestInstance())` -> roda os `@InvokeInit`
   declarados **na propria classe de teste**.

Consequencias que governam toda a estrategia:

- **O Java sempre roda depois do .sql.** Da para conviver com os dois no mesmo
  teste durante a migracao; o Java sobrescreve. Isso permite migracao
  incremental e reversivel, sem big bang.
- `findMethods` usa `getDeclaredMethods()`, entao `@InvokeInit` funciona em
  metodo `private`, e **nao e herdado** de superclasse.
- A chave do mapa em `findMethods` e o **nome do metodo**. Dois `@InvokeInit`
  com o mesmo nome na mesma classe sao impossiveis; mantenha
  `prepararMassaDeDados` como nome unico por classe.
- Excecao dentro do `@InvokeInit` vira `InvokeInitException` e derruba o teste
  antes do primeiro passo -- falha alto e claro, ao contrario do .sql.

## Regra inegociavel: ISO-8859-1

Todo `.java`/`.sql`/`.ddl` sob `src/` e ISO-8859-1 (`pom.xml`:
`project.build.sourceEncoding`, surefire `-Dfile.encoding=ISO-8859-1`).
400 arquivos do projeto tem bytes Latin-1 invalidos em UTF-8.

- **Ler:** `iconv -f ISO-8859-1 -t UTF-8 <arquivo>`. Ler direto produz `�`
  no lugar dos acentos, e um `Edit` feito sobre esse texto grava a perda no disco.
- **Escrever:** prefira `python3 ... encoding="iso-8859-1"` ou o `massa.py converter -o`.
  Se usar `Edit`, mexa apenas em linhas sem acento.
- O hook `PostToolUse` (`.claude/scripts/garantir_iso8859.py`) reconverte UTF-8
  automaticamente e **bloqueia** quando detecta U+FFFD. Se ele bloquear, reverta
  o arquivo em vez de tentar consertar o caractere.
- Nunca introduza aspas curvas, travessao ou reticencias tipograficas: nao
  existem em Latin-1.

## Procedimento

### 1. Analisar antes de converter

```bash
python3 .claude/skills/migracao-massa-teste/scripts/massa.py analisar <caminho>.sql
```

Saida marca cada statement como `OK` (convertivel) ou `!!` (bloqueio/aviso).
**Nao converta nada antes de ler os bloqueios.** Eles quase sempre apontam uma
decisao de teste, nao um detalhe de sintaxe.

### 2. Gerar o esqueleto

```bash
python3 .claude/skills/migracao-massa-teste/scripts/massa.py converter <caminho>.sql
```

Emite o metodo `prepararMassaDeDados()` com os statements convertidos, agrupados
em `// 1. Parametros`, `// 2. Tabelas` e `// 3. PENDENTE DE MIGRACAO MANUAL`.
O gerador e literal e conservador: ele preserva a tipagem (valor com aspas no SQL
vira `String`, sem aspas vira numero -- que e exatamente o que
`TabelasTestUtil.formatarValor()` distingue).

### 3. Revisar (esta e a etapa que exige julgamento)

Consulte `referencias/armadilhas.md` e trate:

- todo bloco `// TODO MIGRACAO`;
- todo comentario `// REVISAR:` que o gerador deixou;
- datas fixas que deveriam ser relativas (ver secao Datas em `referencias/mapeamento-sql-java.md`).

Melhore o resultado bruto: agrupe por intencao, nomeie constantes locais para
codigos repetidos (produto, cliente, nota) e escreva um comentario curto dizendo
**o que** a massa representa, nao o que a linha faz.

### 4. Inserir na classe de teste

**Posicao: `prepararMassaDeDados()` e o primeiro metodo da classe**, logo apos
a declaracao (e apos os campos, se houver), antes de qualquer `@Test`. Quem
abre o arquivo le a massa antes dos passos -- e a massa e a pre-condicao dos
passos. Se a classe tiver outros `@InvokeInit` (por exemplo
`populaAgendaVisita()`), agrupe todos ali, com `prepararMassaDeDados()` na
frente. Nao deixe a massa no fim do arquivo.

```java
@PDATotalUITest
public class ValidaAlgumaCoisaTest {

    @SuppressWarnings("checkstyle:MultipleStringLiterals")
    @InvokeInit
    private void prepararMassaDeDados() throws Exception {

        // 1. Parametros
        ParametrosTestUtil.setParametro(1605, "S");

        // 2. Tabelas
        TabelasTestUtil.insert("TBLVPPRODUTO", ...);
    }

    @Test
    public void deveFazerAlgumaCoisa() {
        ...
    }
}
```

Use a indentacao que o arquivo ja usa (tab ou espaco) -- nao converta o
arquivo inteiro so por causa do metodo novo.

Imports necessarios:

```java
import br.com.wmw.lavenderepda.presentation.ui.base.ParametrosTestUtil;
import br.com.wmw.lavenderepda.presentation.ui.base.TabelasTestUtil;
import br.com.wmw.totalcross.test.api.annotation.InvokeInit;
```

Confira o pacote real das utils antes de escrever o import -- ele ja variou entre
branches (`...ui.base` vs `...ui.test.util`):

```bash
find src/test -name 'ParametrosTestUtil.java'
```

O metodo declara `throws Exception` e leva
`@SuppressWarnings("checkstyle:MultipleStringLiterals")` (nomes de coluna se
repetem por natureza).

### 5. Validar em duas fases

**Fase A -- comparacao (obrigatoria).** Mantenha o `.sql` no lugar, adicione o
Java e rode o teste. Como o Java roda depois, o resultado tem de ser identico.
Verde aqui significa que o Java, no minimo, nao contradiz o SQL.

**Fase B -- corte.** Renomeie o `.sql` para `.sql.bak`, rode de novo. Verde aqui
significa que o Java e **suficiente** sozinho. So entao apague o `.bak`.

Pular a fase B e o erro classico: o teste passa porque o `.sql` continua fazendo
o trabalho e ninguem percebe que a migracao ficou incompleta.

```bash
mvn test -Dtest=<NomeDoTeste> -Denv.test=develop -Duser.language.format=pt -Dfile.encoding=ISO-8859-1
```

### 6. Fechar

```bash
python3 .claude/skills/migracao-massa-teste/scripts/massa.py encoding
python3 .claude/skills/migracao-massa-teste/scripts/massa.py plano
```

Registre no `STATUS.md` do modulo (bloco de anotacoes) o que exigiu decisao e
o que ficou pendente. Migre um teste por vez -- diff pequeno e revisavel vale
mais que lote grande.

## Limites -- quando parar e perguntar

Pare e leve para a pessoa responsavel pelo caso de teste quando:

- o `.sql` configura um parametro por `NMENTIDADE`/`VLCHAVE` especifico e o teste
  aparenta depender disso (`ParametrosTestUtil` nao tem esse escopo hoje);
- o bloqueio exige criar metodo novo em `TabelasTestUtil` (`delete`, blob);
- o statement esta sintaticamente quebrado no `.sql` original -- e um bug do
  teste, nao da migracao. Reporte; nao adivinhe a intencao;
- o teste fica vermelho na fase B e a causa nao e obvia em uma leitura.

Migracao parcial declarada (com `// TODO MIGRACAO` no codigo) e um resultado
aceitavel. Migracao que "passa" porque escondeu o problema, nao.
