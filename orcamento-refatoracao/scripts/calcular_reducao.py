#!/usr/bin/env python3
"""Calcula horas totais, restantes e % de redução do orçamento (modelo antigo x horas reais).

Uso:
  python3 calcular_reducao.py --analise 12 --codificacao 12 --reais 3:25
  python3 calcular_reducao.py --analise 12 --codificacao 12          (sem horas reais)
Horas aceitam: 12 | 12,5 | 12.5 | 3:25 | 03:25:00
"""
import argparse


def para_minutos(valor):
    if valor is None or str(valor).strip() == "":
        return None
    v = str(valor).strip().replace(",", ".")
    if ":" in v:
        partes = [int(p) for p in v.split(":")]
        while len(partes) < 3:
            partes.append(0)
        h, m, s = partes[:3]
        return h * 60 + m + s / 60
    return float(v) * 60


def hms(minutos):
    total = round(minutos * 60)
    h, resto = divmod(total, 3600)
    m, s = divmod(resto, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--analise", required=True)
    p.add_argument("--codificacao", required=True)
    p.add_argument("--reais")
    a = p.parse_args()

    an, co = para_minutos(a.analise), para_minutos(a.codificacao)
    total = an + co
    reais = para_minutos(a.reais)
    print(f"Análise e configuração: {hms(an)}")
    print(f"Codificação:            {hms(co)}")
    print(f"Horas totais:           {hms(total)}")
    if reais is None or total == 0:
        print("Horas reais:            (em branco)")
        print("Horas restantes:        (em branco)")
        print("% Redução:              (em branco)")
        return
    restante = total - reais
    pct = restante / total * 100
    print(f"Horas reais:            {hms(reais)}")
    print(f"Horas restantes:        {hms(restante)}")
    print(f"% Redução:              {pct:.2f}%".replace(".", ","))


if __name__ == "__main__":
    main()
