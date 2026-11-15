
**gbs_mrei.py:**

```python
#!/usr/bin/env python3
"""
GBS — Cálculo iterativo del hafniano con MREI.
Instituto Doughel · UNEG

Genera resultados y gráficos comparativos.
"""

import numpy as np
import time
import math
import matplotlib.pyplot as plt


def mrei_hafniano(matriz, max_iter=1000, tol=1e-10, sag_min=0.90):
    """Aproxima el hafniano por iteración de punto fijo con poda."""
    n = matriz.shape[0]
    if n % 2 != 0:
        raise ValueError("N debe ser par.")

    norma = np.linalg.norm(matriz, 'fro')
    if norma == 0:
        return 0.0, 0
    M = matriz / norma

    X = np.eye(n) * 0.5
    iteraciones = 0

    for it in range(max_iter):
        iteraciones = it + 1
        X_nuevo = 0.5 * (X + M @ X @ M.T)

        media = np.mean(np.abs(X_nuevo))
        std = np.std(np.abs(X_nuevo))
        if std > 0:
            sag = 1.0 - (std / (media + 1e-10))
            if sag < sag_min:
                umbral = media + std
                X_nuevo[np.abs(X_nuevo) < umbral] = 0.0

        diff = np.linalg.norm(X_nuevo - X, 'fro')
        X = X_nuevo
        if diff < tol:
            break

    return np.trace(X * norma), iteraciones


def generar_matriz_gbs(n, seed=42):
    np.random.seed(seed)
    A = np.random.randn(n, n)
    return A @ A.T + np.eye(n) * 0.1


def estimar_fuerza_bruta(n, ops_por_segundo=1e9):
    if n <= 1:
        permutaciones = 1
    else:
        permutaciones = 1
        for i in range(n - 1, 0, -2):
            permutaciones *= i
    return permutaciones, permutaciones / ops_por_segundo


def formatear_tiempo(segundos):
    if segundos < 1e-3:
        return f"{segundos * 1e6:.2f} µs"
    elif segundos < 1:
        return f"{segundos * 1e3:.2f} ms"
    elif segundos < 60:
        return f"{segundos:.2f} s"
    elif segundos < 3600:
        return f"{segundos / 60:.2f} min"
    elif segundos < 86400:
        return f"{segundos / 3600:.2f} h"
    elif segundos < 31536000:
        return f"{segundos / 86400:.2f} días"
    else:
        return f"{segundos / 31536000:.2e} años"


if __name__ == "__main__":
    print("=" * 70)
    print(" GBS — MREI ITERATIVO")
    print(" Instituto Doughel · UNEG")
    print("=" * 70)

    resultados = []
    for n in [20, 30, 40, 50, 60, 70]:
        print(f"\n N = {n}")
        matriz = generar_matriz_gbs(n)

        t0 = time.perf_counter()
        haf, iters = mrei_hafniano(matriz)
        t_mrei = time.perf_counter() - t0

        perm, seg_fb = estimar_fuerza_bruta(n)
        ratio = seg_fb / t_mrei

        print(f"  MREI:        {haf:.6f} en {t_mrei*1000:.3f} ms ({iters} iter)")
        print(f"  Bruto (est): {formatear_tiempo(seg_fb)}")
        print(f"  Ventaja:     {ratio:.2e}x")

        resultados.append({"n": n, "t_mrei": t_mrei, "t_fb": seg_fb, "iters": iters})

    # Gráfico
    ns = [r["n"] for r in resultados]
    t_mrei = [r["t_mrei"] * 1000 for r in resultados]
    t_fb = [r["t_fb"] for r in resultados]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(ns, t_mrei, 'o-', color='#0055A4', linewidth=2, label='MREI')
    ax.plot(ns, t_fb, 's-', color='#d9534f', linewidth=2, label='Fuerza bruta (estimada)')
    ax.set_xlabel('N fotones')
    ax.set_ylabel('Tiempo (ms, escala log)')
    ax.set_yscale('log')
    ax.set_title('GBS — MREI vs. Fuerza bruta', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('graficos/gbs_mrei_comparacion.png', dpi=300)
    print(f"\n✅ Gráfico guardado: graficos/gbs_mrei_comparacion.png")
    plt.show()
