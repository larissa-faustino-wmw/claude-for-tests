#!/usr/bin/env python3
"""Mede o tamanho de uma refatoração para o novo padrão TotalUiTest.

Aceita qualquer combinação de arquivos:
  - .sql legado da massa (conta INSERT/UPDATE/DELETE, parâmetros, expressões de data)
  - .java (legado ou já refatorado: conta passos, asserts, inserts/updates via TabelasTestUtil,
    setParametro, datas, waitOpening)

Uso:
  python3 medir_refatoracao.py Teste.sql TesteAntigo.java TesteNovo.java
"""
import re
import sys
from pathlib import Path

DATA_SQL = re.compile(r"DATE\s*\(\s*'now'|DATETIME\s*\(\s*'now'|TIME\s*\(\s*'now'|STRFTIME\s*\(", re.I)


def medir_sql(texto):
    stmts = [s.strip() for s in texto.split(";") if s.strip() and not s.strip().startswith("--")]
    r = {"insert": 0, "update": 0, "delete": 0, "outros": 0, "parametros": 0, "parametros_json": 0, "datas": 0}
    for s in stmts:
        su = s.upper()
        if su.startswith("INSERT"):
            r["insert"] += 1
        elif su.startswith("UPDATE"):
            r["update"] += 1
        elif su.startswith("DELETE"):
            r["delete"] += 1
        else:
            r["outros"] += 1
        if "TBLVPVALORPARAMETRO" in su:
            r["parametros"] += 1
            if "{" in s or "JSON" in su:
                r["parametros_json"] += 1
        r["datas"] += len(DATA_SQL.findall(s))
    return r


def medir_java(texto):
    return {
        "passos": len(re.findall(r"Passo\s+\d+", texto)),
        "resultados_esperados": len(re.findall(r"Resultado Esperado\s+\d+", texto)),
        "asserts": len(re.findall(r"\bassert(Equals|True|False|NotNull|Null)\s*\(", texto)),
        "waitOpening": len(re.findall(r"waitOpening\s*\(", texto)),
        "tabelas_insert": len(re.findall(r"TabelasTestUtil\s*\.\s*(insert|tabela)\s*\(", texto)),
        "tabelas_update": len(re.findall(r"TabelasTestUtil\s*\.\s*update\s*\(", texto)),
        "setParametro": len(re.findall(r"setParametro\s*\(", texto)),
        "datas": len(re.findall(r"DatasTestUtil\.|LocalDate|SimpleDateFormat", texto)),
        "invoke_init": "@InvokeInit" in texto,
        "javadoc_squash": "squash" in texto.lower(),
        "linhas": texto.count("\n") + 1,
    }


def main(arquivos):
    if not arquivos:
        print(__doc__)
        return
    for a in arquivos:
        p = Path(a)
        texto = p.read_text(encoding="utf-8", errors="replace")
        print(f"\n== {p.name}")
        dados = medir_sql(texto) if p.suffix.lower() == ".sql" else medir_java(texto)
        for k, v in dados.items():
            print(f"  {k:22s} {v}")


if __name__ == "__main__":
    main(sys.argv[1:])
