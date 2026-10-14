#!/usr/bin/env python3
# ==============================================================================
# ANÁLISIS: λ = 1/√2 vs distribución de RG en espines finales GWTC
# ==============================================================================
# Paper: DOI 10.5281/zenodo.23378132
# Pre-registro: DOI 10.5281/zenodo.23376842
# Autor: Lcdo. Douglas Helvesio Urbina Duque
# Instituto Doughel · UNEG, Venezuela · ORCID 0009-0005-1230-7549
# Licencia: CC BY-NC-ND 4.0
# ==============================================================================

import csv
import json
import math
import random

LAMBDA = 1.0 / math.sqrt(2.0)
MU_RG = 0.73
SIGMA_RG = 0.05
SIGNIFICANCIA = 0.05
N_BOOTSTRAP = 10000
RANGO_CONCENTRACION = 0.02
CSV_PATH = "chif_gwtc.csv"

print("=" * 80)
print("🌌 ANÁLISIS: λ = 1/√2 vs RG en espines finales GWTC")
print("=" * 80)
print(f"\nPaper: DOI 10.5281/zenodo.23378132")
print(f"Pre-registro: DOI 10.5281/zenodo.23376842")
print(f"λ = {LAMBDA:.6f}")
print(f"Distribución nula RG: N({MU_RG}, {SIGMA_RG})")
print("=" * 80)

print("\n[1/5] Leyendo datos...")
eventos = []
with open(CSV_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        eventos.append({
            "nombre": row["evento"],
            "chi_f": float(row["chi_f"]),
            "err_pos": float(row["error_pos"]),
            "err_neg": float(row["error_neg"]),
            "fuente": row["fuente"],
        })

valores = [e["chi_f"] for e in eventos]
n = len(valores)
print(f"   ✅ {n} eventos cargados.")

print("\n[2/5] Estadísticas descriptivas...")
media = sum(valores) / n
varianza = sum((v - media) ** 2 for v in valores) / n
desv = math.sqrt(varianza)
mediana = sorted(valores)[n // 2]

print(f"   n = {n}")
print(f"   media = {media:.4f}")
print(f"   mediana = {mediana:.4f}")
print(f"   desv. est. = {desv:.4f}")

random.seed(20261014)
boot = []
for _ in range(N_BOOTSTRAP):
    m = [random.choice(valores) for _ in range(n)]
    boot.append(sum(m) / n)
boot.sort()
ic_inf = boot[int(0.025 * N_BOOTSTRAP)]
ic_sup = boot[int(0.975 * N_BOOTSTRAP)]
print(f"   IC 95%: [{ic_inf:.4f}, {ic_sup:.4f}]")

print("\n[3/5] Tests estadísticos...")

def ks_normal(vals, mu, sigma):
    nn = len(vals)
    orden = sorted(vals)
    D = 0.0
    for i, x in enumerate(orden):
        z = (x - mu) / sigma
        F_teo = 0.5 * (1 + math.erf(z / math.sqrt(2)))
        F_emp = (i + 1) / nn
        D = max(D, abs(F_emp - F_teo), abs(F_teo - i / nn))
    lam = (math.sqrt(nn) + 0.12 + 0.11 / math.sqrt(nn)) * D
    p = 2 * sum((-1) ** (k - 1) * math.exp(-2 * k * k * lam * lam) for k in range(1, 100))
    return D, max(0.0, min(1.0, p))

D_rg, p_rg = ks_normal(valores, MU_RG, SIGMA_RG)
D_lam, p_lam = ks_normal(valores, LAMBDA, SIGMA_RG)

print(f"\n   KS vs λ = {LAMBDA:.4f}: D = {D_lam:.4f}, p = {p_lam:.4f}")
print(f"   KS vs RG = {MU_RG}: D = {D_rg:.4f}, p = {p_rg:.4f}")

dentro_lam = sum(1 for v in valores if abs(v - LAMBDA) <= RANGO_CONCENTRACION)
dentro_rg = sum(1 for v in valores if abs(v - MU_RG) <= RANGO_CONCENTRACION)
dist_lam = sum(abs(v - LAMBDA) for v in valores) / n
dist_rg = sum(abs(v - MU_RG) for v in valores) / n

print(f"\n   Concentración en λ ± {RANGO_CONCENTRACION}: {dentro_lam}/{n}")
print(f"   Concentración en μ_RG ± {RANGO_CONCENTRACION}: {dentro_rg}/{n}")
print(f"   Distancia media a λ: {dist_lam:.4f}")
print(f"   Distancia media a RG: {dist_rg:.4f}")

print("\n[4/5] Veredicto...")
print("=" * 80)

if dist_lam < dist_rg and p_lam > p_rg:
    veredicto = "λ ES MEJOR DESCRIPTOR QUE RG"
elif dist_lam < dist_rg:
    veredicto = "λ tiene menor distancia media; RG compatible"
else:
    veredicto = "RG ES MEJOR DESCRIPTOR QUE λ"

print(f"\n{veredicto}")
print(f"\n   n = {n}")
print(f"   Media χ_f = {media:.4f} (IC 95%: [{ic_inf:.4f}, {ic_sup:.4f}])")

resultado = {
    "paper_doi": "10.5281/zenodo.23378132",
    "pre_registro_doi": "10.5281/zenodo.23376842",
    "fuente_rg": "Lousto et al. (2010), PRD 81, 084023",
    "lambda": LAMBDA,
    "mu_rg": MU_RG,
    "sigma_rg": SIGMA_RG,
    "n_eventos": n,
    "descriptivo": {"media": media, "mediana": mediana, "desv_std": desv},
    "bootstrap": {"ic_95_inf": ic_inf, "ic_95_sup": ic_sup},
    "ks_vs_lambda": {"D": D_lam, "p_valor": p_lam},
    "ks_vs_rg": {"D": D_rg, "p_valor": p_rg},
    "concentracion": {"lambda": dentro_lam, "rg": dentro_rg},
    "distancias": {"lambda": dist_lam, "rg": dist_rg},
    "veredicto": veredicto,
}
with open("resultado_analisis_v2.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False)

print(f"\n[5/5] Resultado guardado en: resultado_analisis_v2.json")
print("=" * 80)
print("🏁 ANÁLISIS COMPLETADO")
print("=" * 80)
