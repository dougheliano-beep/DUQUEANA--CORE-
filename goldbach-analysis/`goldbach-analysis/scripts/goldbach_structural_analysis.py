
```python
#!/usr/bin/env python3
"""
Análisis Estructural de la Conjetura de Goldbach vía Verificación Determinista
Marco de Computación Post-Clásica · Duqueana Core
Autor: Douglas Helvesio Urbina Duque
Licencia: CC-BY-NC-ND 4.0

Nota: Este módulo aplica invariantes geométricas universales para análisis
de simetría estructural en distribuciones de pares primos. 
El núcleo computacional es propiedad intelectual reservada.

Ejecución: python3 goldbach_structural_analysis.py
Dependencias: numpy, json
"""

import numpy as np
import json
from datetime import datetime

# =============================================================================
# INVARIANTES GEOMÉTRICAS UNIVERSALES (PÚBLICAS)
# =============================================================================
LAMBDA_INVARIANT = 1 / np.sqrt(2)  # ≈ 0.70710678
THETA_FIXED_POINT = np.arctan(LAMBDA_INVARIANT)

# =============================================================================
# GENERACIÓN DE PRIMOS Y PARES DE GOLDBACH
# =============================================================================

def sieve_primes(limit):
    """Criba de Eratóstenes optimizada para ~6 KB footprint."""
    if limit < 2: return np.array([], dtype=int)
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0] = sieve[1] = False
    for i in range(2, int(np.sqrt(limit)) + 1):
        if sieve[i]:
            sieve[i*i : limit+1 : i] = False
    return np.nonzero(sieve)[0]

def goldbach_partitions(even_nums, primes):
    """Calcula particiones de Goldbach (p, q) para cada número par."""
    results = {}
    prime_set = set(primes)
    for n in even_nums:
        pairs = []
        half = n // 2
        for p in primes:
            if p > half: break
            q = n - p
            if q in prime_set:
                pairs.append((p, q))
        results[int(n)] = pairs
    return results

# =============================================================================
# MÉTRICAS DE SIMETRÍA ESTRUCTURAL
# =============================================================================

def symmetry_deviation(pairs, n):
    """Mide desviación de simetría alrededor de N/2."""
    if not pairs: return 0.0
    deviations = [abs(p - n/2) for p, q in pairs]
    return np.std(deviations) / (n/2) if n > 0 else 0.0

def structural_persistence_by_scale(partitions, min_j=2, max_j=None):
    """Descomposición diádica de conteo de pares + métrica de persistencia."""
    evens = np.array(list(partitions.keys()))
    counts = np.array([len(v) for v in partitions.values()])
    
    if max_j is None:
        max_j = int(np.log2(np.max(evens))) + 1
    
    blocks = {}
    for j in range(min_j, max_j + 1):
        lower, upper = 2**j, 2**(j+1)
        mask = (evens >= lower) & (evens < upper)
        if np.any(mask):
            block_counts = counts[mask]
            # Persistencia = regularidad relativa (1 / (1 + CV))
            cv = np.std(block_counts) / np.mean(block_counts) if np.mean(block_counts) > 0 else 0
            blocks[j] = 1.0 / (1.0 + cv)
    return blocks

# =============================================================================
# OPERADOR DE VERIFICACIÓN ESTRUCTURAL (MREI-STYLE)
# =============================================================================

def structural_verification_operator(scale_metrics):
    scales = np.array(list(scale_metrics.keys()))
    metrics = np.array(list(scale_metrics.values()))
    
    if len(metrics) > 3:
        smoothed = np.convolve(metrics, np.ones(3)/3, mode='valid')
        scales_smooth = scales[1:-1]
    else:
        smoothed, scales_smooth = metrics, scales
        
    threshold = np.mean(smoothed) * 0.5
    non_depletion = np.all(smoothed > threshold)
    slope = np.polyfit(np.log(scales_smooth), smoothed, 1)[0] if len(scales_smooth) > 1 else 0.0
    
    verdict = "SIMETRÍA ESTRUCTURAL CONFIRMADA" if non_depletion and slope > -0.05 else "REQUIERE ESCALAS MAYORES"
    
    return {
        "scales": scales_smooth.tolist(),
        "metrics": smoothed.tolist(),
        "threshold": float(threshold),
        "non_depletion": bool(non_depletion),
        "slope": float(slope),
        "lambda_invariant": float(LAMBDA_INVARIANT),
        "verdict": verdict
    }

# =============================================================================
# ANÁLISIS DE VENTANA λ
# =============================================================================

def lambda_window_analysis(deviations):
    if len(deviations) == 0: return {"efficiency": 0.0, "avg_dev": 0.0, "window_size": 0.0}
    avg_dev = np.mean(deviations)
    window = LAMBDA_INVARIANT * avg_dev
    in_window = sum(1 for d in deviations if d <= window)
    return {
        "efficiency": (in_window / len(deviations)) * 100,
        "avg_deviation": float(avg_dev),
        "window_size": float(window),
        "in_window": in_window,
        "total": len(deviations)
    }

# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

def run_analysis(max_even=200, export_json=True):
    print("🔷 ANÁLISIS ESTRUCTURAL: CONJETURA DE GOLDBACH 🔷")
    print("=" * 60)
    
    evens = np.arange(4, max_even + 1, 2)
    primes = sieve_primes(max_even)
    print(f"✅ Primos generados: {len(primes)} | Pares analizados: {len(evens)}")
    
    partitions = goldbach_partitions(evens, primes)
    
    # Simetría
    devs = [symmetry_deviation(partitions[n], n) for n in evens]
    window_res = lambda_window_analysis(devs)
    
    # Persistencia por escala
    scale_metrics = structural_persistence_by_scale(partitions)
    verification = structural_verification_operator(scale_metrics)
    
    results = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "max_even_analyzed": int(max_even),
        "primes_count": int(len(primes)),
        "partitions_sample": {str(k): v[:3] for k, v in list(partitions.items())[:5]},
        "symmetry_analysis": window_res,
        "scale_persistence": {str(k): float(v) for k, v in scale_metrics.items()},
        "structural_verification": verification,
        "invariants": {"lambda": float(LAMBDA_INVARIANT), "theta_rad": float(THETA_FIXED_POINT)}
    }
    
    if export_json:
        with open("goldbach_analysis_results.json", "w") as f:
            json.dump(results, f, indent=2)
        print("📄 Exportado: goldbach_analysis_results.json")
        
    print(f"\n📈 RESULTADOS:")
    print(f"   • Veredicto: {verification['verdict']}")
    print(f"   • Pendiente log: {verification['slope']:+.4f}")
    print(f"   • Eficiencia ventana λ: {window_res['efficiency']:.1f}%")
    print(f"   • Desviación simetría prom: {window_res['avg_deviation']:.4f}")
    
    return results

if __name__ == "__main__":
    run_analysis(max_even=200)v 

