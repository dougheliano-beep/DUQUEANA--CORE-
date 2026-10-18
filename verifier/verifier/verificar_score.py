#!/usr/bin/env python3
# Verificador de Coherencia Estructural - Protocolo Genesis v1.0
# Version: v3.0.0
# Autor: Lcdo. Douglas Helvesio Urbina Duque
# ORCID: 0009-0005-1230-7549
# Instituto Doughel - UNEG, Venezuela
# Licencia: Apache 2.0
# DOI Zenodo: 10.5281/zenodo.23445380
#
# ALCANCE: Este script MIDE similitud entre dos archivos PDB.
# No genera estructuras. No contiene el Motor MREI.
# El motor es propiedad intelectual del Instituto Doughel.

import argparse
import hashlib
import math
import sys

import numpy as np


def leer_ca(path):
    ca = {}
    with open(path) as f:
        for line in f:
            if not line.startswith("ATOM"):
                continue
            if line[12:16].strip() != "CA":
                continue
            if line[16].strip() not in ("", "A"):
                continue
            if line[26].strip():
                raise ValueError("Codigo de insercion no soportado")
            chain = line[21].strip() or "A"
            try:
                resid = int(line[22:26].strip())
            except ValueError:
                continue
            amino = line[17:20].strip() or "UNK"
            key = (chain, resid)
            if key in ca:
                raise ValueError(f"Clave duplicada: {key}")
            ca[key] = (
                amino,
                (
                    float(line[30:38]),
                    float(line[38:46]),
                    float(line[46:54]),
                ),
            )
    return ca


def kabsch(P, Q):
    cP = P.mean(axis=0)
    cQ = Q.mean(axis=0)
    Pc = P - cP
    Qc = Q - cQ
    H = Pc.T @ Qc
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1.0, 1.0, d]) @ U.T
    P_rot = (R @ Pc.T).T
    diff = P_rot - Qc
    rmsd = math.sqrt((diff ** 2).sum() / P.shape[0])
    return P_rot, rmsd


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def calcular(salida_path, referencia_path, dmax=5.0):
    if dmax <= 0 or not math.isfinite(dmax):
        raise ValueError("D_max debe ser finito y positivo")

    ca_s = leer_ca(salida_path)
    ca_r = leer_ca(referencia_path)

    if set(ca_s.keys()) != set(ca_r.keys()):
        faltan = set(ca_r) - set(ca_s)
        sobran = set(ca_s) - set(ca_r)
        raise ValueError(
            f"Correspondencia invalida. Faltan: {sorted(faltan)}. "
            f"Sobran: {sorted(sobran)}"
        )

    comunes = sorted(ca_s.keys())
    if len(comunes) < 3:
        raise ValueError("Se requieren al menos 3 residuos")

    for k in comunes:
        if ca_s[k][0] != ca_r[k][0]:
            raise ValueError(
                f"Aminoacido distinto en {k}: "
                f"{ca_s[k][0]} vs {ca_r[k][0]}"
            )

    P = np.array([ca_s[k][1] for k in comunes])
    Q = np.array([ca_r[k][1] for k in comunes])

    _, rmsd = kabsch(P, Q)
    score = max(0.0, min(1.0, 1.0 - (rmsd / dmax)))

    payload = (
        f"rmsd:{rmsd:.10f}|dmax:{dmax:.6f}|"
        f"S:{score:.10f}|n:{len(comunes)}"
    )

    return {
        "score": score,
        "rmsd": rmsd,
        "dmax": dmax,
        "n": len(comunes),
        "hash_salida": sha256(salida_path),
        "hash_referencia": sha256(referencia_path),
        "hash_resultado": hashlib.sha256(payload.encode()).hexdigest(),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--salida", required=True)
    p.add_argument("--referencia", required=True)
    p.add_argument("--dmax", type=float, default=5.0)
    a = p.parse_args()

    print("=" * 60)
    print(" VERIFICADOR - Protocolo Genesis v1.0 (v3.0.0)")
    print("=" * 60)

    try:
        r = calcular(a.salida, a.referencia, a.dmax)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    print(f" Score S         = {r['score']:.4f}")
    print(f" RMSD_Ca         = {r['rmsd']:.4f} A")
    print(f" D_max           = {r['dmax']:.2f} A")
    print(f" Residuos        = {r['n']}")
    print(f" Hash salida     = {r['hash_salida']}")
    print(f" Hash referencia = {r['hash_referencia']}")
    print(f" Hash resultado  = {r['hash_resultado']}")


if __name__ == "__main__":
    main()
