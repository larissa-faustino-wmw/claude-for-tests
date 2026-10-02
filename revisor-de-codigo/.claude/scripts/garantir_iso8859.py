#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hook PostToolUse: garante que todo .java/.sql sob src/ permaneca em ISO-8859-1.

Por que isso existe
-------------------
O projeto compila com -Dfile.encoding=ISO-8859-1 e project.build.sourceEncoding
= ISO-8859-1. As ferramentas de edicao do agente leem e escrevem UTF-8. Sem este
hook, toda edicao em arquivo acentuado:

  1) grava o arquivo em UTF-8 (quebra o build / vira mojibake no relatorio), ou
  2) grava U+FFFD onde havia acento (perda irreversivel de caractere).

Comportamento
-------------
  U+FFFD presente  -> exit 2 (bloqueia e devolve instrucao ao agente).
  UTF-8 com acento -> reconverte para ISO-8859-1 em silencio.
  Caractere fora do Latin-1 (ex.: aspas curvas, travessao) -> exit 2.
  ASCII puro ou ja ISO-8859-1 -> nada a fazer.

Exit codes: 0 = ok, 2 = erro devolvido ao agente.
"""

import json
import os
import sys

EXTENSOES = (".java", ".sql", ".ddl")
MARCA_FFFD = b"\xef\xbf\xbd"


def falhar(mensagem):
    sys.stderr.write(mensagem + "\n")
    sys.exit(2)


def main():
    try:
        evento = json.load(sys.stdin)
    except (ValueError, TypeError):
        return 0

    caminho = (evento.get("tool_input") or {}).get("file_path")
    if not caminho or not caminho.endswith(EXTENSOES):
        return 0
    if not os.path.isfile(caminho):
        return 0
    if "%ssrc%s" % (os.sep, os.sep) not in caminho and not caminho.startswith("src" + os.sep):
        return 0

    with open(caminho, "rb") as fh:
        bruto = fh.read()

    if MARCA_FFFD in bruto:
        falhar(
            "ENCODING: %s ficou com U+FFFD (caractere de substituicao).\n"
            "Isso significa que o conteudo acentuado original foi PERDIDO na edicao.\n"
            "Restaure o arquivo da copia .orig (ou peca ao usuario para restaurar)\n"
            "e refaca a alteracao assim:\n"
            "  1. leia com:  iconv -f ISO-8859-1 -t UTF-8 '%s'\n"
            "  2. escreva via script Python usando encoding='iso-8859-1',\n"
            "     ou edite apenas linhas sem acento.\n"
            "Nao tente 'consertar' os U+FFFD manualmente." % (caminho, caminho)
        )

    try:
        bruto.decode("ascii")
        return 0  # ASCII puro: valido nos dois encodings
    except UnicodeDecodeError:
        pass

    try:
        texto = bruto.decode("utf-8")
    except UnicodeDecodeError:
        return 0  # ja esta em ISO-8859-1

    try:
        convertido = texto.encode("iso-8859-1")
    except UnicodeEncodeError as erro:
        trecho = texto[max(0, erro.start - 40):erro.end + 40]
        falhar(
            "ENCODING: %s contem caractere fora do ISO-8859-1 na posicao %d.\n"
            "Trecho: ...%s...\n"
            "Substitua por equivalente Latin-1 (evite aspas curvas “ ”, travessao —, reticencias …)."
            % (caminho, erro.start, trecho)
        )

    with open(caminho, "wb") as fh:
        fh.write(convertido)
    sys.stderr.write("encoding: %s reconvertido UTF-8 -> ISO-8859-1\n" % caminho)
    return 0


if __name__ == "__main__":
    sys.exit(main())
