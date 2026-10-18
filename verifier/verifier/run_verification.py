#!/usr/bin/env python3
# Runner de Verificacion - Protocolo Genesis v1.0
# Version: v3.0.0
# Autor: Lcdo. Douglas Helvesio Urbina Duque
# ORCID: 0009-0005-1230-7549
# Instituto Doughel - UNEG, Venezuela
# Licencia: Apache 2.0
# DOI Zenodo: 10.5281/zenodo.23445380
#
# Ejecuta los 10 vectores de test_vectors.json contra verificar_score.py
# y reporta cuáles coinciden con los valores esperados.

import json
import os
import subprocess
import sys
import tempfile

VECTORS_JSON = "test_vectors.json"
VERIFICADOR = "verificar_score.py"


def escribir_pdb(path, puntos):
    with open(path, "w") as f:
        for i, p in enumerate(puntos, start=1):
            f.write(
                f"ATOM  {i:5d}  CA  {p['amino']:3s} "
                f"{p['chain']}{p['resid']:4d}    "
                f"{p['xyz'][0]:8.3f}{p['xyz'][1]:8.3f}{p['xyz'][2]:8.3f}"
                f"  1.00  0.00           C\n"
            )
        f.write("END\n")


def main():
    print("=" * 70)
    print(" VERIFICACION AUTOMATICA - Protocolo Genesis v1.0")
    print("=" * 70)

    with open(VECTORS_JSON) as f:
        data = json.load(f)

    refs = data["referencias"]
    casos = data["casos"]
    dmax = data["dmax"]

    tmpdir = tempfile.mkdtemp()
    print(f"\nDirectorio temporal: {tmpdir}")

    for ref_name, puntos in refs.items():
        path = os.path.join(tmpdir, f"ref_{ref_name}.pdb")
        escribir_pdb(path, puntos)
        print(f"  Referencia {ref_name}: {len(puntos)} puntos")

    ok = 0
    fallo = 0

    for caso_name, caso in casos.items():
        print(f"\n--- Caso: {caso_name} ---")
        print(f"    S_esperado = {caso['S_esperado']}")

        salida_path = os.path.join(tmpdir, f"{caso_name}.pdb")
        escribir_pdb(salida_path, caso["puntos"])

        ref_path = os.path.join(
            tmpdir, f"ref_{caso['referencia']}.pdb"
        )

        result = subprocess.run(
            [
                sys.executable,
                VERIFICADOR,
                "--salida",
                salida_path,
                "--referencia",
                ref_path,
                "--dmax",
                str(dmax),
            ],
            capture_output=True,
            text=True,
        )

        print(result.stdout or result.stderr)

        if caso["S_esperado"] == "ERROR":
            if result.returncode != 0:
                print("    OK: ERROR esperado")
                ok += 1
            else:
                print("    FALLO: se esperaba ERROR")
                fallo += 1
        else:
            try:
                score_line = [
                    l
                    for l in result.stdout.split("\n")
                    if "Score S" in l
                ][0]
                score_obtenido = float(
                    score_line.split("=")[1].strip()
                )
                if (
                    abs(score_obtenido - caso["S_esperado"])
                    < 1e-4
                ):
                    print("    OK: COINCIDE")
                    ok += 1
                else:
                    diff = abs(
                        score_obtenido - caso["S_esperado"]
                    )
                    print(f"    FALLO: NO COINCIDE (diff={diff:.6f})")
                    fallo += 1
            except Exception as e:
                print(f"    FALLO: no se pudo parsear ({e})")
                fallo += 1

    print("\n" + "=" * 70)
    print(f" RESUMEN: {ok} coinciden, {fallo} fallan")
    print("=" * 70)

    sys.exit(0 if fallo == 0 else 1)


if __name__ == "__main__":
    main()
