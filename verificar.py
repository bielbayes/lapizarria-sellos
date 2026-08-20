#!/usr/bin/env python3
"""Verifica la cadena de sellos de este repositorio. Sin dependencias.

    python verificar.py

Qué comprueba:
1. Que cada sello es realmente sha256(sello_anterior + hash_contenido).
2. Que cada eslabón enlaza con el anterior.
3. Que el historial publicado hoy produce el hash del último sello.

Si algo no cuadra, el historial se ha alterado después de sellarlo.
"""

import hashlib
import json
import sys
from pathlib import Path

GENESIS = "0" * 64
AQUI = Path(__file__).parent


def contenido_canonico(historial):
    lineas = []
    for p in sorted(historial["picks"], key=lambda x: (x["created_at_utc"], x["pick_id"])):
        lineas.append("PICK\t" + "\t".join("" if v is None else str(v) for v in [
            p["pick_id"], p["created_at_utc"], p["model_version"], p["match_id"],
            p["market"], p["selection"], p["model_probability"], p["fair_odds"],
            p["offered_odds"], p["bookmaker"], p["odds_snapshot"], p["edge"],
            p["stake_units"],
        ]))
    for r in sorted(historial["resoluciones"], key=lambda x: (x["resolved_at_utc"], x["resolution_id"])):
        lineas.append("RESOLUCION\t" + "\t".join("" if v is None else str(v) for v in [
            r["resolution_id"], r["pick_id"], r["resolved_at_utc"], r["outcome"],
            r["closing_odds"], r["clv"],
        ]))
    return "\n".join(lineas)


def main():
    cadena = [json.loads(l) for l in (AQUI / "chain.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    if not cadena:
        print("cadena vacia")
        return 0

    anterior = GENESIS
    for i, e in enumerate(cadena):
        if e["sello_anterior"] != anterior:
            print(f"FALLO: el eslabon {i} ({e['fecha']}) no enlaza con el anterior")
            return 1
        esperado = hashlib.sha256((anterior + e["hash_contenido"]).encode()).hexdigest()
        if esperado != e["sello"]:
            print(f"FALLO: el sello del eslabon {i} ({e['fecha']}) no cuadra con su contenido")
            return 1
        anterior = e["sello"]
    print(f"OK: {len(cadena)} sellos encadenados correctamente")
    print(f"    sello actual: {anterior}")

    historial = json.loads((AQUI / "historial.json").read_text(encoding="utf-8"))
    calculado = hashlib.sha256(contenido_canonico(historial).encode("utf-8")).hexdigest()
    ultimo = cadena[-1]["hash_contenido"]
    if calculado == ultimo:
        print(f"OK: el historial publicado ({len(historial['picks'])} picks) coincide con el ultimo sello")
        return 0
    print("FALLO: el historial publicado NO coincide con el ultimo sello")
    print(f"       calculado {calculado}")
    print(f"       sellado   {ultimo}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
