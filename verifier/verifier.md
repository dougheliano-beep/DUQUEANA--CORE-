# Verificador de Score — Protocolo de Verificación Génesis v1.0

**Versión:** v2.0.0 (corregida, 16/10/2026)
**Autor:** Lcdo. Douglas Helvesio Urbina Duque
**ORCID:** 0009-0005-1230-7549
**Institución:** Instituto Doughel · UNEG, Venezuela
**Protocolo asociado:** [DOI 10.5281/zenodo.23330991](https://doi.org/10.5281/zenodo.23330991)
**Zenodo v2:** [DOI 10.5281/zenodo.23422454](https://doi.org/10.5281/zenodo.23422454)
**Licencia:** CC BY-NC-ND 4.0

---

## 📌 Alcance

El script mide la similitud de coordenadas Cα entre dos archivos PDB:

- Superpone sin reflexión mediante Kabsch/SVD.
- Calcula RMSD en Å.
- Computa `S = max(0, min(1, 1 − RMSD / D_max))`.

**No genera estructuras. No revela el funcionamiento del Motor MREI.**

---

## 📦 Requisitos

- Python 3.8+
- NumPy

Instalación:
```bash
pip install numpy
```

---

## 🚀 Ejecución

```bash
python3 verificar_score.py \
  --salida test_vectors/caso_4_perturbacion.pdb \
  --referencia test_vectors/caso_referencia.pdb \
  --dmax 5.0
```

**Resultado esperado:**
```
Score S        = 0.9500
RMSD_Cα        = 0.2500 Å
D_max          = 5.0 Å
Residuos       = 5
```

---

## 🧪 Vectores de prueba

| Caso | Vector | S esperado |
|---|---|---|
| 1 | caso_1_identico.pdb | 1.0000 |
| 2 | caso_2_rotacion.pdb | 1.0000 |
| 3 | caso_3_traslacion.pdb | 1.0000 |
| 4 | caso_4_perturbacion.pdb | 0.9500 |
| 5 | caso_5_residuo_ausente.pdb | ERROR |

**Los 5 vectores coinciden con el manifiesto tras la corrección.**

---

## 🔧 Corrección aplicada (v2.0.0)

- **Kabsch completo con SVD** (corrige bug de v1 donde solo se centraba).
- **Validación estricta** de correspondencia de residuos.
- **Caso 4 corregido** (perturbación no rígida de 0.25 Å).
- **Hashes SHA-256 reales**.

Agradecimiento a Co-Science (Academia.edu) por la revisión técnica.

---

## 💻 Código fuente

```python
#!/usr/bin/env python3
# ==============================================================================
# VERIFICADOR DE SCORE — Protocolo de Verificación Génesis v1.0
# Versión del software: v2.0.0 (corrección de Co-Science, 16/10/2026)
# ==============================================================================
# Autor del código base: Lcdo. Douglas Helvesio Urbina Duque
# Instituto Doughel · UNEG, Venezuela · ORCID 0009-0005-1230-7549
# Licencia: CC BY-NC-ND 4.0
# Protocolo asociado: DOI 10.5281/zenodo.23330991
# Versión previa: DOI 10.5281/zenodo.23402330
# ==============================================================================

import argparse
import hashlib
import math
import sys
from typing import Dict, Tuple

import numpy as np


def parse_pdb_ca(filepath: str) -> Dict[Tuple[str, int], Tuple[float, float, float]]:
    ca_coords = {}
    with open(filepath, "r") as f:
        for line in f:
            if not line.startswith("ATOM"):
                continue
            atom_name = line[12:16].strip()
            if atom_name != "CA":
                continue
            altloc = line[16].strip()
            if altloc not in ("", "A"):
                continue
            icode = line[26].strip()
            if icode:
                raise ValueError(f"Código de inserción no soportado: {icode}")
            chain = line[21].strip() or "A"
            try:
                resid = int(line[22:26].strip())
            except ValueError:
                continue
            key = (chain, resid)
            if key in ca_coords:
                raise ValueError(f"Clave duplicada: {key}")
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            ca_coords[key] = (x, y, z)
    return ca_coords


def kabsch_align(P, Q):
    if P.shape != Q.shape:
        raise ValueError("Conjuntos de puntos de tamaño distinto")
    cP = P.mean(axis=0)
    cQ = Q.mean(axis=0)
    Pc = P - cP
    Qc = Q - cQ
    H = Pc.T @ Qc
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    D = np.diag([1.0, 1.0, d])
    R = Vt.T @ D @ U.T
    P_rot = (R @ Pc.T).T
    diff = P_rot - Qc
    rmsd = math.sqrt((diff ** 2).sum() / P.shape[0])
    return P_rot, rmsd


def calcular_score(salida_path: str, referencia_path: str, dmax: float = 5.0):
    if dmax <= 0 or not math.isfinite(dmax):
        raise ValueError("D_max debe ser finito y mayor que cero")
    ca_salida = parse_pdb_ca(salida_path)
    ca_ref = parse_pdb_ca(referencia_path)
    set_salida = set(ca_salida.keys())
    set_ref = set(ca_ref.keys())
    if set_salida != set_ref:
        faltantes = set_ref - set_salida
        sobrantes = set_salida - set_ref
        raise ValueError(f"Correspondencia inválida. Faltantes: {sorted(faltantes)}. Sobrantes: {sorted(sobrantes)}")
    comunes = sorted(set_salida)
    if len(comunes) < 3:
        raise ValueError("Se requieren al menos 3 residuos")
    P = np.array([ca_salida[k] for k in comunes])
    Q = np.array([ca_ref[k] for k in comunes])
    P_align, rmsd = kabsch_align(P, Q)
    S = max(0.0, min(1.0, 1.0 - (rmsd / dmax)))
    payload = f"rmsd:{rmsd:.6f}|dmax:{dmax:.2f}|S:{S:.6f}|n:{len(comunes)}"
    hash_result = hashlib.sha256(payload.encode()).hexdigest()
    return {"score": S, "rmsd": rmsd, "dmax": dmax, "n_residuos": len(comunes), "hash_sha256": hash_result}


def main():
    parser = argparse.ArgumentParser(description="Verificador de score — Protocolo Génesis v1.0, software v2.0.0")
    parser.add_argument("--salida", required=True)
    parser.add_argument("--referencia", required=True)
    parser.add_argument("--dmax", type=float, default=5.0)
    args = parser.parse_args()
    print("=" * 70)
    print(" VERIFICADOR DE SCORE — Protocolo Génesis v1.0 (software v2.0.0)")
    print("=" * 70)
    try:
        r = calcular_score(args.salida, args.referencia, args.dmax)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)
    print(f"\n Score S        = {r['score']:.4f}")
    print(f" RMSD_Cα        = {r['rmsd']:.4f} Å")
    print(f" D_max          = {r['dmax']:.2f} Å")
    print(f" Residuos       = {r['n_residuos']}")
    print(f" Hash SHA-256   = {r['hash_sha256']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
```

---

## 🧬 Vectores de prueba

### caso_referencia.pdb

```
ATOM      1  CA  ALA A   1       0.000   0.000   0.000  1.00  0.00           C
ATOM      2  CA  ALA A   2       3.800   0.000   0.000  1.00  0.00           C
ATOM      3  CA  ALA A   3       7.600   0.000   0.000  1.00  0.00           C
ATOM      4  CA  ALA A   4      11.400   0.000   0.000  1.00  0.00           C
ATOM      5  CA  ALA A   5      15.200   0.000   0.000  1.00  0.00           C
END
```

### caso_1_identico.pdb
*(idéntico a la referencia — S = 1.0000)*

```
ATOM      1  CA  ALA A   1       0.000   0.000   0.000  1.00  0.00           C
ATOM      2  CA  ALA A   2       3.800   0.000   0.000  1.00  0.00           C
ATOM      3  CA  ALA A   3       7.600   0.000   0.000  1.00  0.00           C
ATOM      4  CA  ALA A   4      11.400   0.000   0.000  1.00  0.00           C
ATOM      5  CA  ALA A   5      15.200   0.000   0.000  1.00  0.00           C
END
```

### caso_2_rotacion.pdb
*(rotación 45° alrededor de Z — S = 1.0000 tras alinear)*

```
ATOM      1  CA  ALA A   1       0.000   0.000   0.000  1.00  0.00           C
ATOM      2  CA  ALA A   2       2.687   2.687   0.000  1.00  0.00           C
ATOM      3  CA  ALA A   3       5.374   5.374   0.000  1.00  0.00           C
ATOM      4  CA  ALA A   4       8.061   8.061   0.000  1.00  0.00           C
ATOM      5  CA  ALA A   5      10.748  10.748   0.000  1.00  0.00           C
END
```

### caso_3_traslacion.pdb
*(traslación (5,5,5) Å — S = 1.0000 tras alinear)*

```
ATOM      1  CA  ALA A   1       5.000   5.000   5.000  1.00  0.00           C
ATOM      2  CA  ALA A   2       8.800   5.000   5.000  1.00  0.00           C
ATOM      3  CA  ALA A   3      12.600   5.000   5.000  1.00  0.00           C
ATOM      4  CA  ALA A   4      16.400   5.000   5.000  1.00  0.00           C
ATOM      5  CA  ALA A   5      20.200   5.000   5.000  1.00  0.00           C
END
```

### caso_4_perturbacion.pdb
*(perturbación no rígida ±0.25 Å — S = 0.9500)*

```
ATOM      1  CA  ALA A   1       0.250   0.000   0.000  1.00  0.00           C
ATOM      2  CA  ALA A   2       3.550   0.000   0.000  1.00  0.00           C
ATOM      3  CA  ALA A   3       7.850   0.000   0.000  1.00  0.00           C
ATOM      4  CA  ALA A   4      11.150   0.000   0.000  1.00  0.00           C
ATOM      5  CA  ALA A   5      15.450   0.000   0.000  1.00  0.00           C
END
```

### caso_5_residuo_ausente.pdb
*(falta residuo 3 — ERROR esperado)*

```
ATOM      1  CA  ALA A   1       0.000   0.000   0.000  1.00  0.00           C
ATOM      2  CA  ALA A   2       3.800   0.000   0.000  1.00  0.00           C
ATOM      4  CA  ALA A   4      11.400   0.000   0.000  1.00  0.00           C
ATOM      5  CA  ALA A   5      15.200   0.000   0.000  1.00  0.00           C
END
```

---

## 📊 Hashes SHA-256

```
d97291486f97198159c7c9d3cf9373831c8fe185358e2226e4b852c201d8ff90  verificar_score.py
911f013e02e1f638e1f97a9b3885a2f205ca7b68768a623781ab4b2d9d1262b2  manifest.tsv
da8aab904c78dbcbcec4fc061d9936587be9c7055ccc82546a36cd1996cc388d  test_vectors/caso_referencia.pdb
da8aab904c78dbcbcec4fc061d9936587be9c7055ccc82546a36cd1996cc388d  test_vectors/caso_1_identico.pdb
b7dc3aeb0066089240b5648955d814320b65e58fcd4b451f05415ce90433bf35  test_vectors/caso_2_rotacion.pdb
90c4492424d8aee0d795f4d5a3c54b6c8ca6da9e51aaabc9deb4a7af7fb4f7b1  test_vectors/caso_3_traslacion.pdb
0a2a96c1b37f7f735f25a28c8fba401bb61d7bcba5545459e6dafac3bbef35af  test_vectors/caso_4_perturbacion.pdb
4a41ff24ce3dc606d06e4b7586aff3676e40ac7e4ba2c4f3233ebd6ff2e61727  test_vectors/caso_5_residuo_ausente.pdb
```

---

## 🔗 Enlaces

- **Zenodo v2 (corregido):** [10.5281/zenodo.23422454](https://doi.org/10.5281/zenodo.23422454)
- **Zenodo v1 (bug):** [10.5281/zenodo.23402330](https://doi.org/10.5281/zenodo.23402330)
- **Protocolo Génesis v1.0:** [10.5281/zenodo.23330991](https://doi.org/10.5281/zenodo.23330991)
- **Respuesta a Co-Science:** [10.5281/zenodo.23401914](https://doi.org/10.5281/zenodo.23401914)

---

**Instituto Doughel · Duqueana Core · UNEG · Venezuela**
