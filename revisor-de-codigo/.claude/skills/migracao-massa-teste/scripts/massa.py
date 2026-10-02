#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
massa.py -- ferramentas de apoio a migracao da massa de teste SQL -> Java
            (ParametrosTestUtil / TabelasTestUtil).

Este script NAO substitui a revisao humana/IA: ele faz o trabalho mecanico
(parsing do SQL, conversao literal, deteccao de armadilhas) e marca
explicitamente tudo que nao pode ser convertido com seguranca.

Subcomandos:
  inventario [--json]        Audita todos os .sql do projeto e ranqueia por esforco.
  analisar   <arquivo.sql>   Classifica statement a statement, apontando riscos.
  converter  <arquivo.sql>   Emite o corpo do metodo @InvokeInit em Java.
  encoding   [arquivos...]   Verifica se os arquivos continuam em ISO-8859-1.

Encoding: todo .sql/.java do projeto e lido/escrito como ISO-8859-1.
A saida deste script no terminal e UTF-8.
"""

import argparse
import io
import json
import os
import re
import sys

# stdout sempre UTF-8, independente do locale (o build usa -Dfile.encoding=ISO-8859-1)
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ENCODING_FONTE = "ISO-8859-1"
RAIZ_TESTES = os.path.join("src", "test", "java")
PARAMETROS_UTIL = os.path.join(
    "src", "test", "java", "br", "com", "wmw", "lavenderepda",
    "presentation", "ui", "base", "ParametrosTestUtil.java",
)
TABELA_PARAMETRO = "TBLVPVALORPARAMETRO"

# ---------------------------------------------------------------------------
# Leitura do whitelist PARAMETROS_JSON da ParametrosTestUtil
# ---------------------------------------------------------------------------


def carregar_parametros_json(raiz="."):
    """Le o Set PARAMETROS_JSON declarado na ParametrosTestUtil.

    Retorna set() vazio se nao encontrar o arquivo -- nesse caso as checagens
    de JSON viram avisos em vez de erros.
    """
    caminho = os.path.join(raiz, PARAMETROS_UTIL)
    if not os.path.isfile(caminho):
        return None
    with open(caminho, "r", encoding=ENCODING_FONTE) as fh:
        fonte = fh.read()
    m = re.search(r"PARAMETROS_JSON\s*=\s*new\s+HashSet<>\s*\(\s*Arrays\.asList\((.*?)\)\s*\)",
                  fonte, re.DOTALL)
    if not m:
        return None
    corpo = re.sub(r"//[^\n]*", "", m.group(1))
    return {int(n) for n in re.findall(r"\b\d+\b", corpo)}


# ---------------------------------------------------------------------------
# Tokenizacao de SQL (respeita aspas simples/duplas e comentarios)
# ---------------------------------------------------------------------------


def _consumir_string(texto, i, saida):
    """Consome uma string literal iniciada em texto[i]. Devolve novo indice."""
    aspa = texto[i]
    saida.append(aspa)
    i += 1
    n = len(texto)
    while i < n:
        if texto[i] == aspa:
            if i + 1 < n and texto[i + 1] == aspa:  # escape '' ou ""
                saida.append(aspa * 2)
                i += 2
                continue
            saida.append(aspa)
            return i + 1
        saida.append(texto[i])
        i += 1
    return i  # string nao fechada -- SQL malformado


def separar_statements(sql):
    """Divide o SQL em (comentarios_precedentes, statement).

    Comentarios sao preservados para virarem comentarios Java.
    """
    resultado = []
    buf = []
    comentarios = []
    i, n = 0, len(sql)
    while i < n:
        c = sql[i]
        if c == "-" and i + 1 < n and sql[i + 1] == "-":
            fim = sql.find("\n", i)
            fim = n if fim == -1 else fim
            texto = sql[i + 2:fim].strip()
            if texto and not "".join(buf).strip():
                comentarios.append(texto)
            i = fim
            continue
        if c == "/" and i + 1 < n and sql[i + 1] == "*":
            fim = sql.find("*/", i + 2)
            fim = n if fim == -1 else fim + 2
            texto = sql[i + 2:fim - 2].strip()
            if texto and not "".join(buf).strip():
                comentarios.append(texto)
            i = fim
            continue
        if c in "'\"":
            i = _consumir_string(sql, i, buf)
            continue
        if c == ";":
            corpo = " ".join("".join(buf).split())
            if corpo:
                resultado.append((comentarios, corpo))
                comentarios = []
            buf = []
            i += 1
            continue
        buf.append(c)
        i += 1
    corpo = " ".join("".join(buf).split())
    if corpo:
        resultado.append((comentarios, corpo))
    return resultado


def separar_virgulas(texto):
    """Divide por virgulas no nivel 0 de parenteses, respeitando strings."""
    partes, buf = [], []
    prof = 0
    i, n = 0, len(texto)
    while i < n:
        c = texto[i]
        if c in "'\"":
            i = _consumir_string(texto, i, buf)
            continue
        if c == "(":
            prof += 1
        elif c == ")":
            prof -= 1
        elif c == "," and prof == 0:
            partes.append("".join(buf).strip())
            buf = []
            i += 1
            continue
        buf.append(c)
        i += 1
    partes.append("".join(buf).strip())
    return [p for p in partes if p]


def separar_tuplas(texto):
    """Extrai cada tupla `(...)` de uma clausula VALUES."""
    tuplas, buf = [], []
    prof = 0
    i, n = 0, len(texto)
    while i < n:
        c = texto[i]
        if c in "'\"":
            if prof > 0:
                i = _consumir_string(texto, i, buf)
            else:
                i = _consumir_string(texto, i, [])
            continue
        if c == "(":
            prof += 1
            if prof == 1:
                buf = []
                i += 1
                continue
        elif c == ")":
            prof -= 1
            if prof == 0:
                tuplas.append("".join(buf))
                i += 1
                continue
        if prof > 0:
            buf.append(c)
        i += 1
    return tuplas


# ---------------------------------------------------------------------------
# Conversao de valores SQL -> literais Java
# ---------------------------------------------------------------------------

# SQLite aceita ".0000000" (sem zero a esquerda) -- ocorre na massa atual.
RE_NUMERO = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$")
LIMITE_INT = 2 ** 31 - 1


def escapar_java(texto):
    saida = texto.replace("\\", "\\\\").replace('"', '\\"')
    saida = saida.replace("\r", "\\r").replace("\n", "\\n").replace("\t", "\\t")
    return '"' + saida + '"'


# --- Expressoes de data do SQLite -> DatasTestUtil -------------------------
#
# DatasTestUtil ja existe em .../presentation/ui/base/DatasTestUtil.java e cobre
# as variantes que a massa legada usa. Sem este mapeamento o conversor marcava
# todo DATE()/TIME() como "valor nao literal" e o plano acusava um bloqueio
# "helper de datas" que nao existe mais.

RE_FUNCAO_DATA_SQL = re.compile(
    r"^(?P<funcao>DATE|TIME|DATETIME)\s*\((?P<args>.*)\)$", re.IGNORECASE | re.DOTALL)
RE_MODIFICADOR_DIAS = re.compile(
    r"^['\"]\s*(?P<sinal>[+-])\s*(?P<qtd>\d+)\s*days?\s*['\"]$", re.IGNORECASE)
# (STRFTIME('%w', DATE(...)) + 1) -- a convencao de NUDIASEMANA, domingo = 1.
RE_DIA_SEMANA_SQL = re.compile(
    r"^\(?\s*STRFTIME\s*\(\s*['\"]%w['\"]\s*,\s*(?P<data>DATE\s*\(.*\))\s*\)\s*\+\s*1\s*\)?$",
    re.IGNORECASE | re.DOTALL)


def _deslocamento_em_dias(args):
    """Le os modificadores de DATE()/TIME() e devolve o deslocamento em dias.

    Devolve None quando nao da para reproduzir a expressao com fidelidade:

    - modificador que DatasTestUtil nao tem ('start of month', '+2 hours',
      'weekday 0');
    - ausencia de 'localtime'. Sem ele o SQLite responde em UTC, e
      DatasTestUtil trabalha em hora local -- entre 21h e a meia-noite no
      Brasil os dois dao dias diferentes. `date('now')` nao e `hoje()`.
    """
    dias = 0
    tem_localtime = False
    for arg in separar_virgulas(args):
        alvo = arg.strip()
        if not alvo:
            continue
        nu = alvo.strip("'\"").strip().lower()
        if nu == "localtime":
            tem_localtime = True
            continue
        if nu == "now":
            continue
        m = RE_MODIFICADOR_DIAS.match(alvo)
        if not m:
            return None
        dias += int(m.group("qtd")) * (-1 if m.group("sinal") == "-" else 1)
    return dias if tem_localtime else None


def _chamada_por_dias(zero, mais, menos, dias):
    if dias == 0:
        return zero
    if dias > 0:
        return mais % dias if mais else None
    return menos % abs(dias) if menos else None


def expressao_data_para_java(texto):
    """Converte uma expressao de data do SQLite na chamada equivalente de
    DatasTestUtil. Devolve None quando nao ha equivalente.

    DATE('now','localtime')                    -> DatasTestUtil.hoje()
    DATE('now','+2 day','localtime')           -> DatasTestUtil.hojeMais(2)
    DATE('now','-1 day','localtime')           -> DatasTestUtil.hojeMenos(1)
    TIME('now','localtime')                    -> DatasTestUtil.agora()
    (STRFTIME('%w', DATE('now','localtime'))+1)-> DatasTestUtil.diaDaSemana()
    """
    t = texto.strip()

    m = RE_DIA_SEMANA_SQL.match(t)
    if m:
        interna = RE_FUNCAO_DATA_SQL.match(m.group("data").strip())
        if not interna:
            return None
        dias = _deslocamento_em_dias(interna.group("args"))
        if dias is None:
            return None
        return ("DatasTestUtil.diaDaSemana()" if dias == 0
                else "DatasTestUtil.diaDaSemana(%d)" % dias)

    m = RE_FUNCAO_DATA_SQL.match(t)
    if not m:
        return None
    funcao = m.group("funcao").upper()
    dias = _deslocamento_em_dias(m.group("args"))
    if dias is None:
        return None
    if funcao == "DATE":
        return _chamada_por_dias("DatasTestUtil.hoje()",
                                 "DatasTestUtil.hojeMais(%d)",
                                 "DatasTestUtil.hojeMenos(%d)", dias)
    if funcao == "TIME":
        # Nao ha helper de hora deslocada; so a hora corrente tem equivalente.
        return "DatasTestUtil.agora()" if dias == 0 else None
    # DATETIME() nao tem equivalente em DatasTestUtil.
    return None


def motivo_expressao(valor):
    """Explica por que uma expressao nao virou literal Java.

    Sem isso o relatorio diz so "valor nao literal" e quem migra nao sabe se
    falta helper, se a expressao e composta ou se o problema e o fuso.
    """
    t = valor.strip()
    if not RX_FUNCAO_DATA.search(t):
        return ""
    m = RE_FUNCAO_DATA_SQL.match(t)
    if m and "localtime" not in m.group("args").lower():
        return (" -- DATE/TIME sem 'localtime' responde em UTC; DatasTestUtil e local. "
                "Confirme com o time se a intencao era a data local antes de usar hoje().")
    if not m:
        return (" -- expressao de data composta (concatenacao ou aritmetica). "
                "Monte o valor em Java e passe o resultado.")
    return (" -- modificador sem equivalente em DatasTestUtil. "
            "Converta a mao ou acrescente o helper.")


def valor_sql_para_java(valor):
    """Converte um literal SQL para literal Java.

    Retorna (literal_java, tipo) onde tipo em {null, numero, texto, data,
    expressao}. `expressao` significa que NAO da para converter automaticamente;
    `data` ja vem como chamada de DatasTestUtil, sem aspas.

    A fidelidade importa: TabelasTestUtil.formatarValor() so deixa o valor sem
    aspas quando ele e instanceof Number. Logo `'1'` (com aspas no SQL) precisa
    virar String em Java, e `1` (sem aspas) precisa virar numero.
    """
    t = valor.strip()
    if not t:
        return "null", "null"
    if t.upper() == "NULL":
        return "null", "null"
    if RE_NUMERO.match(t):
        if "." in t or "e" in t.lower():
            return t, "numero"
        return (t + "L" if abs(int(t)) > LIMITE_INT else t), "numero"
    if len(t) >= 2 and t[0] == t[-1] and t[0] in "'\"":
        interno = t[1:-1]
        interno = interno.replace(t[0] * 2, t[0])
        return escapar_java(interno), "texto"
    data = expressao_data_para_java(t)
    if data:
        return data, "data"
    return None, "expressao"


# ---------------------------------------------------------------------------
# Classificacao de statements
# ---------------------------------------------------------------------------

RE_UPDATE_PARAM = re.compile(
    r"^UPDATE\s+" + TABELA_PARAMETRO + r"\s+SET\s+(?P<set>.*?)(?:\s+WHERE\s+(?P<where>.*))?$",
    re.IGNORECASE | re.DOTALL)
RE_INSERT = re.compile(
    r"^INSERT\s+(?:OR\s+\w+\s+)?INTO\s+(?P<tabela>[\w\.]+)\s*\((?P<colunas>.*?)\)\s*VALUES\s*(?P<valores>.*)$",
    re.IGNORECASE | re.DOTALL)
RE_UPDATE = re.compile(
    r"^UPDATE\s+(?P<tabela>[\w\.]+)\s+SET\s+(?P<set>.*?)(?:\s+WHERE\s+(?P<where>.*))?$",
    re.IGNORECASE | re.DOTALL)
RE_CDPARAMETRO = re.compile(r"CDPARAMETRO\s*=\s*'?(\d+)'?", re.IGNORECASE)
RE_ATRIB = re.compile(r"^(?P<coluna>[\w\.]+)\s*=\s*(?P<valor>.*)$", re.DOTALL)
RE_PAR_JSON_CHAVE = re.compile(r'"([^"]+)"\s*:\s*("(?:[^"\\]|\\.)*"|[^,;}\s][^,;}]*)')


class Item(object):
    """Um statement SQL classificado."""

    def __init__(self, sql, comentarios):
        self.sql = sql
        self.comentarios = comentarios
        self.tipo = "desconhecido"     # parametro | insert | update | manual
        self.java = []                 # linhas Java geradas
        self.avisos = []               # riscos que exigem olho humano
        self.bloqueios = []            # impede conversao automatica
        self.tabela = None
        self.parametro = None

    @property
    def automatico(self):
        return not self.bloqueios and bool(self.java)


def _parse_atribuicoes(clausula):
    pares = []
    for parte in separar_virgulas(clausula):
        m = RE_ATRIB.match(parte.strip())
        if not m:
            return None
        pares.append((m.group("coluna").strip(), m.group("valor").strip()))
    return pares


def _chaves_json(bruto):
    """Extrai pares chave/valor de um VLPARAMETRO em formato JSON.

    Devolve (pares, json_valido). Faz fallback por regex quando o JSON esta
    malformado -- caso real no projeto (';' no lugar de ',').
    """
    try:
        dados = json.loads(bruto)
        if isinstance(dados, dict):
            return [(k, "" if v is None else str(v)) for k, v in dados.items()], True
    except (ValueError, TypeError):
        pass
    pares = []
    for chave, valor in RE_PAR_JSON_CHAVE.findall(bruto):
        valor = valor.strip()
        if len(valor) >= 2 and valor[0] == '"' and valor[-1] == '"':
            valor = valor[1:-1]
        pares.append((chave, valor))
    return pares, False


def classificar_parametro(item, m, parametros_json):
    item.tipo = "parametro"
    pares = _parse_atribuicoes(m.group("set"))
    where = (m.group("where") or "").strip()

    if pares is None or len(pares) != 1 or pares[0][0].upper() != "VLPARAMETRO":
        item.bloqueios.append(
            "UPDATE em %s altera colunas alem de VLPARAMETRO -- converter a mao." % TABELA_PARAMETRO)
        return
    if not where:
        item.bloqueios.append(
            "UPDATE em %s SEM WHERE: afeta TODOS os parametros. Revisar a intencao." % TABELA_PARAMETRO)
        return

    mcd = RE_CDPARAMETRO.search(where)
    if not mcd:
        item.bloqueios.append("Nao foi possivel identificar o CDPARAMETRO no WHERE: %s" % where)
        return

    cd = int(mcd.group(1))
    item.parametro = cd

    resto = RE_CDPARAMETRO.sub("", where)
    resto = re.sub(r"CDSISTEMA\s*=\s*'?\d+'?", "", resto, flags=re.IGNORECASE)
    resto = re.sub(r"\b(AND|OR)\b", "", resto, flags=re.IGNORECASE).strip()
    if resto:
        item.avisos.append(
            "WHERE tem filtro extra ignorado por ParametrosTestUtil (%s) -- confirme se e irrelevante." % resto)

    literal, tipo = valor_sql_para_java(pares[0][1])
    if tipo == "expressao":
        item.bloqueios.append("Valor do parametro nao e literal: %s" % pares[0][1])
        return

    bruto = pares[0][1].strip().strip("'\"")
    e_json = bruto.startswith("{")

    if e_json:
        chaves, valido = _chaves_json(bruto)
        if not valido:
            item.avisos.append(
                "JSON do parametro %d esta MALFORMADO no .sql original (separador invalido). "
                "Chaves recuperadas por heuristica -- CONFERIR contra a documentacao do parametro." % cd)
        if not chaves:
            item.bloqueios.append("Parametro %d parece JSON mas nenhuma chave foi extraida." % cd)
            return
        if parametros_json is not None and cd not in parametros_json:
            item.bloqueios.append(
                "Parametro %d grava JSON mas NAO esta em ParametrosTestUtil.PARAMETROS_JSON. "
                "Sem adicionar o id la, setParametro() sobrescreve o JSON inteiro e corrompe a massa. "
                "Adicione %d ao Set antes de migrar." % (cd, cd))
            return
        item.avisos.append(
            "Parametro %d e JSON: o .sql substituia o objeto inteiro; setParametro() faz json_set "
            "(patch). Chaves nao listadas passam a vir do banco base." % cd)
        for chave, valor in chaves:
            item.java.append('ParametrosTestUtil.setParametro(%d, %s, %s);'
                             % (cd, escapar_java(chave), escapar_java(valor)))
    else:
        if parametros_json is not None and cd in parametros_json:
            item.avisos.append(
                "Parametro %d esta em PARAMETROS_JSON mas o .sql gravava valor simples (%s). "
                "setParametro() vai aplicar json_set na chave \"usa\" -- confirme se e o esperado."
                % (cd, bruto))
            item.java.append('ParametrosTestUtil.setParametro(%d, "usa", %s);' % (cd, escapar_java(bruto)))
        else:
            item.java.append('ParametrosTestUtil.setParametro(%d, %s);' % (cd, escapar_java(bruto)))


def _formatar_pares(chamada, cabecalho, pares, recuo="    "):
    """Monta a chamada Java quebrando linhas em ~150 colunas.

    Indentacao aqui e relativa; quem emite (despejar) aplica o recuo do metodo.
    """
    linhas = ["%s(%s" % (chamada, cabecalho)]
    atual = recuo
    for i, (col, val) in enumerate(pares):
        trecho = "%s, %s" % (col, val)
        sufixo = "," if i < len(pares) - 1 else ""
        if len(atual) + len(trecho) + len(sufixo) > 140 and atual.strip():
            linhas.append(atual.rstrip())
            atual = recuo
        atual += trecho + sufixo + " "
    if atual.strip():
        linhas.append(atual.rstrip())
    linhas.append(");")
    return linhas


def classificar_insert(item, m):
    item.tipo = "insert"
    item.tabela = m.group("tabela").upper()
    colunas = [c.strip() for c in separar_virgulas(m.group("colunas"))]
    tuplas = separar_tuplas(m.group("valores"))

    if not tuplas:
        item.bloqueios.append("INSERT sem clausula VALUES literal (provavel INSERT ... SELECT).")
        return
    if len(tuplas) > 1:
        item.avisos.append("INSERT com %d tuplas foi desmembrado em %d chamadas insert()."
                           % (len(tuplas), len(tuplas)))

    for tupla in tuplas:
        valores = separar_virgulas(tupla)
        if len(valores) != len(colunas):
            item.bloqueios.append("INSERT em %s: %d colunas para %d valores."
                                  % (item.tabela, len(colunas), len(valores)))
            return
        pares = []
        for coluna, valor in zip(colunas, valores):
            literal, tipo = valor_sql_para_java(valor)
            if tipo == "expressao":
                item.bloqueios.append("INSERT em %s: valor nao literal na coluna %s -> %s%s"
                                      % (item.tabela, coluna, valor, motivo_expressao(valor)))
                return
            pares.append((escapar_java(coluna), literal))
        item.java.extend(_formatar_pares("TabelasTestUtil.insert",
                                         escapar_java(item.tabela) + ",", pares))


def classificar_update(item, m):
    item.tipo = "update"
    item.tabela = m.group("tabela").upper()
    where = (m.group("where") or "").strip()
    pares_sql = _parse_atribuicoes(m.group("set"))

    if pares_sql is None:
        item.bloqueios.append("Nao foi possivel interpretar a clausula SET do UPDATE em %s." % item.tabela)
        return
    if not where:
        item.avisos.append("UPDATE em %s SEM WHERE: afeta a tabela inteira (comportamento preservado)."
                           % item.tabela)

    pares = []
    for coluna, valor in pares_sql:
        literal, tipo = valor_sql_para_java(valor)
        if tipo == "expressao":
            item.bloqueios.append("UPDATE em %s: valor nao literal na coluna %s -> %s%s"
                                  % (item.tabela, coluna, valor, motivo_expressao(valor)))
            return
        pares.append((escapar_java(coluna), literal))

    cabecalho = "%s, %s," % (escapar_java(item.tabela), escapar_java(where) if where else "null")
    item.java.extend(_formatar_pares("TabelasTestUtil.update", cabecalho, pares))


def classificar(sql, comentarios, parametros_json):
    item = Item(sql, comentarios)
    cabeca = sql.lstrip()[:30].upper()

    m = RE_UPDATE_PARAM.match(sql)
    if m:
        classificar_parametro(item, m, parametros_json)
        return item

    m = RE_INSERT.match(sql)
    if m:
        classificar_insert(item, m)
        return item

    m = RE_UPDATE.match(sql)
    if m:
        classificar_update(item, m)
        return item

    item.tipo = "manual"
    if cabeca.startswith("DELETE"):
        item.bloqueios.append("DELETE nao tem equivalente em TabelasTestUtil. "
                              "Use DatabasePrepareTestUtil.executeUpdate(...) ou crie TabelasTestUtil.delete().")
    elif cabeca.startswith(("ALTER", "CREATE", "DROP", "PRAGMA")):
        item.bloqueios.append("DDL nao pertence a massa de dados. Manter em .ddl/.sql ou "
                              "DatabasePrepareTestUtil.executeUpdate(...).")
    else:
        item.bloqueios.append("Statement nao reconhecido pelo conversor.")
    return item


# ---------------------------------------------------------------------------
# Pipeline por arquivo
# ---------------------------------------------------------------------------


def analisar_arquivo(caminho, parametros_json):
    with open(caminho, "rb") as fh:
        bruto = fh.read()
    try:
        bruto.decode("ascii")
        encoding_detectado = "ASCII"
    except UnicodeDecodeError:
        try:
            bruto.decode("utf-8")
            encoding_detectado = "UTF-8"
        except UnicodeDecodeError:
            encoding_detectado = "ISO-8859-1"
    # Os 4 arquivos que ja derivaram para UTF-8 precisam ser lidos como UTF-8,
    # senao os acentos viram mojibake ao passarem pelo conversor.
    texto = bruto.decode("utf-8" if encoding_detectado == "UTF-8" else ENCODING_FONTE)
    itens = [classificar(sql, coments, parametros_json)
             for coments, sql in separar_statements(texto)]
    return itens, encoding_detectado


def caminho_java_do_sql(caminho_sql):
    candidato = caminho_sql[:-4] + ".java"
    return candidato if os.path.isfile(candidato) else None


def java_do_teste(base_sem_extensao):
    """Localiza o .java da classe de teste a partir do caminho do .sql.

    A convencao do projeto coloca o .sql ora ao lado do .java, ora dentro de
    um diretorio com o mesmo nome da classe.
    """
    candidatos = [base_sem_extensao + ".java"]
    pasta, nome = os.path.split(base_sem_extensao)
    candidatos.append(os.path.join(pasta, nome, nome + ".java"))
    candidatos.append(os.path.join(os.path.dirname(pasta), nome + ".java"))
    for c in candidatos:
        if os.path.isfile(c):
            return c
    return None


def estado_migracao(caminho_sql):
    """Deduz o estado da migracao do proprio repositorio -- nunca fica velho.

    NAO INICIADO : existe .sql e a classe nao tem @InvokeInit
    FASE A       : existe .sql e a classe ja tem @InvokeInit (os dois convivem)
    MIGRADO      : nao existe .sql e a classe tem @InvokeInit
    """
    base = caminho_sql[:-4]
    if base.endswith("_Retorno"):
        base = base[:-len("_Retorno")]
    caminho_java = java_do_teste(base)
    tem_invoke = False
    if caminho_java:
        with open(caminho_java, "rb") as fh:
            tem_invoke = b"@InvokeInit" in fh.read()
    tem_sql = os.path.isfile(caminho_sql)
    if tem_sql and tem_invoke:
        return "FASE A"
    if tem_sql:
        return "NAO INICIADO"
    return "MIGRADO" if tem_invoke else "?"


def listar_sqls(raiz="."):
    achados = []
    for base, _dirs, arquivos in os.walk(os.path.join(raiz, RAIZ_TESTES)):
        for arquivo in arquivos:
            if arquivo.endswith(".sql"):
                achados.append(os.path.join(base, arquivo))
    return sorted(achados)


# ---------------------------------------------------------------------------
# Comandos
# ---------------------------------------------------------------------------


def cmd_inventario(args):
    parametros_json = carregar_parametros_json()
    linhas = []
    for caminho in listar_sqls():
        itens, encoding_detectado = analisar_arquivo(caminho, parametros_json)
        auto = sum(1 for i in itens if i.automatico)
        bloq = sum(1 for i in itens if i.bloqueios)
        avisos = sum(len(i.linhas_aviso) if hasattr(i, "linhas_aviso") else len(i.avisos) for i in itens)
        linhas.append({
            "arquivo": os.path.relpath(caminho),
            "teste": os.path.basename(caminho)[:-4],
            "statements": len(itens),
            "automaticos": auto,
            "bloqueados": bloq,
            "avisos": avisos,
            "encoding": encoding_detectado,
            "tem_java": bool(caminho_java_do_sql(caminho)),
            "retorno_web": caminho.endswith("_Retorno.sql"),
        })

    if args.json:
        print(json.dumps(linhas, indent=2, ensure_ascii=False))
        return 0

    total = len(linhas)
    tot_st = sum(l["statements"] for l in linhas)
    tot_auto = sum(l["automaticos"] for l in linhas)
    tot_bloq = sum(l["bloqueados"] for l in linhas)
    limpos = [l for l in linhas if l["bloqueados"] == 0 and l["statements"] > 0]
    sujos = [l for l in linhas if l["bloqueados"] > 0]
    utf8 = [l for l in linhas if l["encoding"] == "UTF-8"]

    print("=" * 78)
    print("INVENTARIO DA MASSA DE TESTE (.sql)")
    print("=" * 78)
    print("Arquivos .sql .............. %d" % total)
    print("Statements ................. %d" % tot_st)
    print("  convertiveis automatico .. %d  (%.1f%%)" % (tot_auto, 100.0 * tot_auto / max(tot_st, 1)))
    print("  exigem decisao humana .... %d  (%.1f%%)" % (tot_bloq, 100.0 * tot_bloq / max(tot_st, 1)))
    print("Arquivos 100%% automatizaveis %d" % len(limpos))
    print("Arquivos com bloqueio ...... %d" % len(sujos))
    if utf8:
        print("\n!! %d arquivo(s) ja derivaram para UTF-8 (deveriam ser ISO-8859-1):" % len(utf8))
        for l in utf8[:10]:
            print("   %s" % l["arquivo"])

    print("\n--- ONDA 1: comecar por estes (sem bloqueios, menor esforco) ---")
    for l in sorted(limpos, key=lambda x: x["statements"])[:20]:
        print("  %3d st  %s" % (l["statements"], l["arquivo"]))

    print("\n--- ONDA FINAL: exigem analise (mais bloqueios primeiro) ---")
    for l in sorted(sujos, key=lambda x: -x["bloqueados"])[:15]:
        print("  %3d bloq / %3d st  %s" % (l["bloqueados"], l["statements"], l["arquivo"]))
    return 0


def cmd_analisar(args):
    parametros_json = carregar_parametros_json()
    itens, encoding_detectado = analisar_arquivo(args.arquivo, parametros_json)
    print("Arquivo : %s" % args.arquivo)
    print("Encoding: %s%s" % (encoding_detectado,
                              "   << ATENCAO: deveria ser ISO-8859-1" if encoding_detectado == "UTF-8" else ""))
    print("Statements: %d\n" % len(itens))
    for n, item in enumerate(itens, 1):
        marca = "OK " if item.automatico else "!! "
        print("%s[%02d] %-10s %s" % (marca, n, item.tipo, (item.tabela or
              ("parametro %s" % item.parametro if item.parametro else ""))))
        for b in item.bloqueios:
            print("      BLOQUEIO: %s" % b)
        for a in item.avisos:
            print("      aviso   : %s" % a)
    auto = sum(1 for i in itens if i.automatico)
    print("\nResumo: %d/%d automaticos, %d bloqueados."
          % (auto, len(itens), sum(1 for i in itens if i.bloqueios)))
    return 0 if auto == len(itens) else 1


def cmd_converter(args):
    parametros_json = carregar_parametros_json()
    itens, _enc = analisar_arquivo(args.arquivo, parametros_json)

    saida = []
    saida.append("    @SuppressWarnings(\"checkstyle:MultipleStringLiterals\")")
    saida.append("    @InvokeInit")
    saida.append("    private void prepararMassaDeDados() throws Exception {")
    saida.append("")

    parametros = [i for i in itens if i.tipo == "parametro"]
    tabelas = [i for i in itens if i.tipo in ("insert", "update")]
    manuais = [i for i in itens if i.tipo == "manual" or i.bloqueios]

    def despejar(titulo, grupo):
        if not grupo:
            return
        saida.append("        // %s" % titulo)
        for item in grupo:
            for c in item.comentarios:
                saida.append("        // %s" % c)
            if item.bloqueios:
                saida.append("        // TODO MIGRACAO -- converter a mao:")
                for b in item.bloqueios:
                    saida.append("        //   %s" % b)
                saida.append("        //   SQL: %s" % item.sql)
                saida.append("")
                continue
            for a in item.avisos:
                saida.append("        // REVISAR: %s" % a)
            for linha in item.java:
                saida.append("        " + linha)
            saida.append("")

    despejar("1. Parametros", [i for i in parametros if not i.bloqueios])
    despejar("2. Tabelas", [i for i in tabelas if not i.bloqueios])
    despejar("3. PENDENTE DE MIGRACAO MANUAL", manuais)

    saida.append("    }")
    texto = "\n".join(saida)

    if args.saida:
        with open(args.saida, "w", encoding=ENCODING_FONTE, errors="replace") as fh:
            fh.write(texto + "\n")
        print("Escrito em %s (%s)" % (args.saida, ENCODING_FONTE))
    else:
        print(texto)
    return 0


MARCA_NOTAS = "<!-- ==== ANOTACOES (preservado entre regeneracoes) ==== -->"
RAIZ_MODULOS = os.path.join(RAIZ_TESTES, "br", "com", "wmw", "lavenderepda",
                            "presentation", "ui", "test")
DIR_REFATORACAO = os.path.join(".claude", "refatoracao")


def _notas_existentes(caminho):
    """Recupera o bloco de anotacoes manuais de um STATUS.md ja existente."""
    if not os.path.isfile(caminho):
        return None
    with open(caminho, "r", encoding="utf-8", errors="replace") as fh:
        conteudo = fh.read()
    if MARCA_NOTAS in conteudo:
        return conteudo.split(MARCA_NOTAS, 1)[1].lstrip("\n")
    return None


def _dados_modulo(modulo, parametros_json):
    base = os.path.join(RAIZ_MODULOS, modulo)
    testes = []
    for pasta, _dirs, arquivos in os.walk(base):
        for arquivo in sorted(arquivos):
            if not arquivo.endswith(".sql"):
                continue
            caminho = os.path.join(pasta, arquivo)
            itens, encoding_detectado = analisar_arquivo(caminho, parametros_json)
            motivos = []
            causas = {}
            for item in itens:
                if not item.bloqueios:
                    continue
                motivos.extend(item.bloqueios)
                c = causa_raiz(item)
                causas[c] = causas.get(c, 0) + 1
            testes.append({
                "causas": causas,
                "arquivo": caminho,
                "nome": arquivo[:-4],
                "statements": len(itens),
                "automaticos": sum(1 for i in itens if i.automatico),
                "bloqueados": sum(1 for i in itens if i.bloqueios),
                "avisos": sum(len(i.avisos) for i in itens),
                "encoding": encoding_detectado,
                "estado": estado_migracao(caminho),
                "motivos": motivos,
            })
    total_java = sum(1 for p, _d, fs in os.walk(base) for f in fs if f.endswith(".java"))
    return testes, total_java


RX_FUNCAO_DATA = re.compile(r"(DATE\s*\(|STRFTIME\s*\(|TIME\s*\()", re.IGNORECASE)

# Causa raiz -> (rotulo, resolvivel por mudanca nas utils?)
CAUSAS = [
    ("delete() em TabelasTestUtil", True),
    ("expressao de data sem equivalente em DatasTestUtil", False),
    ("whitelist PARAMETROS_JSON", True),
    ("DDL -- permanece no .sql (correto)", False),
    ("blob hexadecimal", False),
    ("analise caso a caso", False),
]


def causa_raiz(item):
    """Classifica um bloqueio pela causa raiz, nao pelo sintoma.

    Serve para decidir o que vale corrigir na util (uma vez) em vez de
    contornar arquivo a arquivo (164 vezes).
    """
    texto = " ".join(item.bloqueios)
    if "DELETE nao tem" in texto:
        return "delete() em TabelasTestUtil"
    if "DDL nao pertence" in texto:
        return "DDL -- permanece no .sql (correto)"
    if "PARAMETROS_JSON" in texto:
        return "whitelist PARAMETROS_JSON"
    if "nao literal" in texto:
        if RX_FUNCAO_DATA.search(texto):
            # As variantes cobertas por DatasTestUtil ja sao convertidas em
            # valor_sql_para_java e nem chegam aqui. O que sobra e expressao
            # composta (concatenacao com ||, aritmetica) ou modificador que o
            # helper nao reproduz -- nao adianta mexer na util.
            return "expressao de data sem equivalente em DatasTestUtil"
        if "X'" in item.sql[:400]:
            return "blob hexadecimal"
    return "analise caso a caso"


def _resumo_motivos(testes):
    """Agrupa bloqueios equivalentes preservando a explicacao.

    O valor concreto ("-> date('now')") sai da chave, senao cada linha vira um
    grupo de um; a explicacao depois de " -- " fica, que e o que diz ao humano
    o que fazer.
    """
    contagem = {}
    for teste in testes:
        for motivo in teste["motivos"]:
            cabeca, sep, cauda = motivo.partition(" -- ")
            cabeca = cabeca.split("->")[0].split(":")[0].strip()
            chave = cabeca + (" -- " + " ".join(cauda.split()) if sep else "")
            contagem[chave] = contagem.get(chave, 0) + 1
    return sorted(contagem.items(), key=lambda kv: -kv[1])


def cmd_plano(args):
    parametros_json = carregar_parametros_json()
    modulos = sorted(d for d in os.listdir(RAIZ_MODULOS)
                     if os.path.isdir(os.path.join(RAIZ_MODULOS, d)))
    resumo = []

    for modulo in modulos:
        testes, total_java = _dados_modulo(modulo, parametros_json)
        destino = os.path.join(DIR_REFATORACAO, modulo)
        if not os.path.isdir(destino):
            os.makedirs(destino)
        caminho_status = os.path.join(destino, "STATUS.md")
        notas = _notas_existentes(caminho_status)

        st = sum(t["statements"] for t in testes)
        auto = sum(t["automaticos"] for t in testes)
        bloq = sum(t["bloqueados"] for t in testes)
        migrados = sum(1 for t in testes if t["estado"] == "MIGRADO")
        fase_a = sum(1 for t in testes if t["estado"] == "FASE A")

        causas_modulo = {}
        for teste in testes:
            for c, q in teste["causas"].items():
                causas_modulo[c] = causas_modulo.get(c, 0) + q
        destravaveis = sum(q for c, q in causas_modulo.items()
                           if dict(CAUSAS).get(c, False))

        resumo.append({
            "modulo": modulo, "java": total_java, "sql": len(testes),
            "statements": st, "automaticos": auto, "bloqueados": bloq,
            "migrados": migrados, "fase_a": fase_a,
            "causas": causas_modulo, "destravaveis": destravaveis,
        })

        linhas = []
        linhas.append("# Refatoracao -- modulo `%s`" % modulo)
        linhas.append("")
        linhas.append("> Gerado por `massa.py plano`. O estado e deduzido do repositorio")
        linhas.append("> (presenca de `.sql` e de `@InvokeInit`), entao nao envelhece.")
        linhas.append("> Regenere depois de cada teste migrado. Anotacoes manuais no fim do")
        linhas.append("> arquivo sao preservadas.")
        linhas.append("")
        linhas.append("| | |")
        linhas.append("|---|---|")
        linhas.append("| Classes de teste | %d |" % total_java)
        linhas.append("| Arquivos `.sql` restantes | %d |" % len(testes))
        linhas.append("| Statements | %d |" % st)
        linhas.append("| Convertiveis automaticamente | %d (%.0f%%) |"
                      % (auto, 100.0 * auto / max(st, 1)))
        linhas.append("| Exigem decisao humana | %d |" % bloq)
        linhas.append("| Migrados / em fase A | %d / %d |" % (migrados, fase_a))
        linhas.append("")

        if testes:
            linhas.append("## Ordem sugerida")
            linhas.append("")
            linhas.append("Menor esforco primeiro. `bloq` = statements que exigem decisao.")
            linhas.append("")
            linhas.append("| # | Estado | Teste | stmts | auto | bloq | enc |")
            linhas.append("|---|---|---|---|---|---|---|")
            ordenados = sorted(testes, key=lambda t: (t["bloqueados"], t["statements"]))
            for n, t in enumerate(ordenados, 1):
                enc = "!! UTF-8" if t["encoding"] == "UTF-8" else "ok"
                linhas.append("| %d | %s | `%s` | %d | %d | %d | %s |"
                              % (n, t["estado"], t["nome"], t["statements"],
                                 t["automaticos"], t["bloqueados"], enc))
            linhas.append("")

        if causas_modulo:
            linhas.append("## Bloqueios por causa raiz")
            linhas.append("")
            linhas.append("| Causa | Qtd | Resolvivel na util? |")
            linhas.append("|---|---|---|")
            mapa = dict(CAUSAS)
            for causa, qtd in sorted(causas_modulo.items(), key=lambda kv: -kv[1]):
                linhas.append("| %s | %d | %s |"
                              % (causa, qtd, "sim" if mapa.get(causa) else "nao"))
            linhas.append("")
            if destravaveis:
                linhas.append("**%d dos %d bloqueios deste modulo somem** com as melhorias em"
                              % (destravaveis, bloq))
                linhas.append("`../../skills/migracao-massa-teste/referencias/proposta-melhorias-utils.md`.")
                linhas.append("Considere resolver a util antes de migrar este modulo -- e uma")
                linhas.append("mudanca contra %d ocorrencias." % destravaveis)
                linhas.append("")

        motivos = _resumo_motivos(testes)
        if motivos:
            linhas.append("<details><summary>Detalhe dos bloqueios</summary>")
            linhas.append("")
            for motivo, qtd in motivos:
                linhas.append("- **%dx** %s" % (qtd, motivo))
            linhas.append("")
            linhas.append("</details>")
            linhas.append("")

        linhas.append("## Como migrar")
        linhas.append("")
        linhas.append("```")
        linhas.append("/migrar-teste <NomeDaClasseTest>   # um teste (comece pelo nº 1)")
        linhas.append("/migrar-modulo %s%s# a fila inteira, um por vez"
                      % (modulo, " " * max(1, 20 - len(modulo))))
        linhas.append("```")
        linhas.append("")
        linhas.append("Regras que valem sempre: ISO-8859-1, validacao em fase A e fase B, um")
        linhas.append("teste por vez. Detalhe em `../../skills/migracao-massa-teste/SKILL.md`.")
        linhas.append("")
        linhas.append(MARCA_NOTAS)
        linhas.append("")
        if notas is not None:
            linhas.append(notas.rstrip())
        else:
            linhas.append("## Anotacoes")
            linhas.append("")
            linhas.append("Decisoes tomadas, duvidas para o time, defeitos encontrados no `.sql`")
            linhas.append("original. Este bloco sobrevive a regeneracao.")
        linhas.append("")

        with open(caminho_status, "w", encoding="utf-8") as fh:
            fh.write("\n".join(linhas))

    _escrever_readme_refatoracao(resumo)
    print("Gerado %s para %d modulo(s)." % (DIR_REFATORACAO, len(modulos)))
    print("%-24s %5s %5s %6s %6s %8s" % ("modulo", ".sql", "stmt", "auto%", "bloq", "migrados"))
    for r in sorted(resumo, key=lambda x: (x["bloqueados"] * 1.0 / max(x["statements"], 1),
                                           x["statements"])):
        if not r["sql"] and not r["migrados"]:
            continue
        print("%-24s %5d %5d %5.0f%% %6d %8d"
              % (r["modulo"], r["sql"], r["statements"],
                 100.0 * r["automaticos"] / max(r["statements"], 1),
                 r["bloqueados"], r["migrados"]))
    return 0


def _escrever_readme_refatoracao(resumo):
    caminho = os.path.join(DIR_REFATORACAO, "README.md")
    notas = _notas_existentes(caminho)

    ativos = [r for r in resumo if r["sql"] or r["migrados"]]
    def dificuldade(r):
        return (r["bloqueados"] * 1.0 / max(r["statements"], 1), r["statements"])
    ordenados = sorted(ativos, key=dificuldade)

    tot_sql = sum(r["sql"] for r in resumo)
    tot_st = sum(r["statements"] for r in resumo)
    tot_auto = sum(r["automaticos"] for r in resumo)
    tot_bloq = sum(r["bloqueados"] for r in resumo)
    tot_mig = sum(r["migrados"] for r in resumo)

    l = []
    l.append("# Refatoracao da massa de teste -- painel por modulo")
    l.append("")
    l.append("> Gerado por `python3 .claude/skills/migracao-massa-teste/scripts/massa.py plano`.")
    l.append("> Regenere apos cada teste migrado. Anotacoes no fim sao preservadas.")
    l.append("")
    l.append("Migrar a massa de `<Teste>.sql` para `@InvokeInit` com `ParametrosTestUtil`")
    l.append("e `TabelasTestUtil`, **um modulo por vez**, comecando pelos de menor risco")
    l.append("para o processo amadurecer antes de encostar nos dificeis.")
    l.append("")
    l.append("| Total | |")
    l.append("|---|---|")
    l.append("| `.sql` restantes | %d |" % tot_sql)
    l.append("| Statements | %d |" % tot_st)
    l.append("| Convertiveis automaticamente | %d (%.1f%%) |"
             % (tot_auto, 100.0 * tot_auto / max(tot_st, 1)))
    l.append("| Exigem decisao humana | %d |" % tot_bloq)
    l.append("| Testes ja migrados | %d |" % tot_mig)
    l.append("")
    l.append("## Ordem sugerida")
    l.append("")
    l.append("Ordenado por proporcao de bloqueios, depois por tamanho.")
    l.append("")
    l.append("| Onda | Modulo | `.sql` | stmts | auto | bloq | migrados |")
    l.append("|---|---|---|---|---|---|---|")
    for n, r in enumerate(ordenados):
        onda = 1 if n < 5 else (2 if n < 12 else 3)
        l.append("| %d | [`%s`](%s/STATUS.md) | %d | %d | %.0f%% | %d | %d |"
                 % (onda, r["modulo"], r["modulo"], r["sql"], r["statements"],
                    100.0 * r["automaticos"] / max(r["statements"], 1),
                    r["bloqueados"], r["migrados"]))
    sem_massa = [r["modulo"] for r in resumo if not r["sql"] and not r["migrados"]]
    if sem_massa:
        l.append("")
        l.append("Sem massa `.sql` (nada a migrar): %s."
                 % ", ".join("`%s`" % m for m in sem_massa))

    causas_total = {}
    for r in resumo:
        for c, q in r["causas"].items():
            causas_total[c] = causas_total.get(c, 0) + q
    mapa = dict(CAUSAS)
    destravaveis = sum(q for c, q in causas_total.items() if mapa.get(c))

    if causas_total:
        l.append("")
        l.append("## Causa raiz dos %d bloqueios" % tot_bloq)
        l.append("")
        l.append("| Causa | Qtd | Resolvivel na util? |")
        l.append("|---|---|---|")
        for causa, qtd in sorted(causas_total.items(), key=lambda kv: -kv[1]):
            l.append("| %s | %d | %s |" % (causa, qtd, "sim" if mapa.get(causa) else "nao"))
        l.append("")
        projetado = 100.0 * (tot_auto + destravaveis) / max(tot_st, 1)
        pendentes = sorted(c for c, q in causas_total.items() if mapa.get(c) and q)
        l.append("**%d dos %d bloqueios (%.0f%%) somem com mudanca nas utils** -- %s."
                 % (destravaveis, tot_bloq, 100.0 * destravaveis / max(tot_bloq, 1),
                    ", ".join(pendentes) if pendentes else "nenhuma pendente"))
        l.append("A cobertura automatica passaria de %.1f%% para %.1f%%."
                 % (100.0 * tot_auto / max(tot_st, 1), projetado))
        l.append("")
        l.append("`DatasTestUtil` ja esta implementado -- as expressoes de data cobertas")
        l.append("por ele sao convertidas automaticamente e nao contam como bloqueio.")
        l.append("")
        l.append("Por isso a **onda 0** existe: mexer nas utils primeiro e uma mudanca")
        l.append("pequena contra %d ocorrencias. Fazer o contrario significa contornar" % destravaveis)
        l.append("o mesmo problema %d vezes a mao." % destravaveis)
        l.append("")
        mais = sorted((r for r in resumo if r["destravaveis"]),
                      key=lambda r: -r["destravaveis"])[:6]
        if mais:
            l.append("Modulos mais beneficiados: %s."
                     % ", ".join("`%s` (%d)" % (r["modulo"], r["destravaveis"]) for r in mais))
            l.append("")
        l.append("**Onda 0** -- ajustar as utils. Ver")
        l.append("`../skills/migracao-massa-teste/referencias/proposta-melhorias-utils.md`.")

    l.append("")
    l.append("**Onda 1** -- piloto. Poucos bloqueios: serve para validar o processo")
    l.append("ponta a ponta (incluindo fase A/B com o banco baixado) antes de escalar.")
    l.append("")
    l.append("**Onda 2** -- volume. O processo ja esta calibrado; aqui esta a maior parte")
    l.append("do ganho. Vale rodar o subagente `migrador-massa` um teste por vez.")
    l.append("")
    l.append("**Onda 3** -- o que sobra depois da onda 0. Se a onda 0 nao for feita, e")
    l.append("aqui que o trabalho manual se concentra.")
    l.append("")
    l.append("> As ondas sao ordenadas pela proporcao de bloqueios **hoje**. Depois da")
    l.append("> onda 0, regenere este painel: varios modulos mudam de posicao.")
    l.append("")
    l.append("## Fluxo por modulo")
    l.append("")
    l.append("1. `/auditar-massa` -- panorama atualizado.")
    l.append("2. Abrir o `STATUS.md` do modulo e seguir a ordem sugerida.")
    l.append("3. Migrar:")
    l.append("   - `/migrar-teste <NomeDaClasseTest>` -- um teste, com validacao propria.")
    l.append("     Use no primeiro teste de cada modulo, para conferir o resultado.")
    l.append("   - `/migrar-modulo <modulo>` -- a fila inteira via subagente, um por vez,")
    l.append("     com validacao em lote no fim. Use depois que o primeiro deu certo.")
    l.append("4. Validar fase A (com `.sql`) e fase B (sem `.sql`). Sem fase B o teste")
    l.append("   pode estar passando por causa do `.sql`, nao da migracao.")
    l.append("5. Regenerar: `massa.py plano`.")
    l.append("")
    l.append(MARCA_NOTAS)
    l.append("")
    l.append(notas.rstrip() if notas is not None else
             "## Anotacoes\n\nDecisoes de escopo e pendencias para o time.")
    l.append("")

    with open(caminho, "w", encoding="utf-8") as fh:
        fh.write("\n".join(l))


def cmd_encoding(args):
    alvos = args.arquivos or [c for c in listar_sqls()] + [
        os.path.join(b, f)
        for b, _d, fs in os.walk(RAIZ_TESTES) for f in fs if f.endswith(".java")]
    problemas = []
    for caminho in alvos:
        if not os.path.isfile(caminho):
            continue
        bruto = open(caminho, "rb").read()
        if b"\xef\xbf\xbd" in bruto:
            problemas.append((caminho, "CORROMPIDO: contem U+FFFD (acentos perdidos)"))
            continue
        try:
            bruto.decode("ascii")
            continue
        except UnicodeDecodeError:
            pass
        try:
            bruto.decode("utf-8")
            problemas.append((caminho, "UTF-8: deveria estar em ISO-8859-1"))
        except UnicodeDecodeError:
            pass  # ISO-8859-1, ok
    for caminho, motivo in problemas:
        print("%s: %s" % (caminho, motivo))
    print("\n%d arquivo(s) verificado(s), %d problema(s)." % (len(alvos), len(problemas)))
    return 1 if problemas else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("inventario", help="audita todos os .sql e ranqueia por esforco")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_inventario)

    p = sub.add_parser("analisar", help="classifica um .sql statement a statement")
    p.add_argument("arquivo")
    p.set_defaults(func=cmd_analisar)

    p = sub.add_parser("converter", help="emite o metodo @InvokeInit em Java")
    p.add_argument("arquivo")
    p.add_argument("-o", "--saida", help="grava em arquivo (ISO-8859-1) em vez de stdout")
    p.set_defaults(func=cmd_converter)

    p = sub.add_parser("plano", help="gera/atualiza .claude/refatoracao/<modulo>/STATUS.md")
    p.set_defaults(func=cmd_plano)

    p = sub.add_parser("encoding", help="verifica ISO-8859-1")
    p.add_argument("arquivos", nargs="*")
    p.set_defaults(func=cmd_encoding)

    args = parser.parse_args()
    if not getattr(args, "func", None):
        parser.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
