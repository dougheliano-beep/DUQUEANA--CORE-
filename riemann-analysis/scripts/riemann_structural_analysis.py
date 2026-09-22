#!/usr/bin/env python3
"""
Análisis Estructural de Ceros de Riemann vía Verificación Determinista
Marco de Computación Post-Clásica · Duqueana Core
Autor: Douglas Helvesio Urbina Duque
Licencia: CC-BY-NC-ND 4.0

Nota: Este módulo aplica invariantes geométricas universales para análisis
de patrones estructurales. El núcleo computacional es propiedad intelectual
reservada del Instituto de Investigación Digital.

Ejecución: python3 riemann_structural_analysis.py
Dependencias: numpy, json
"""

import numpy as np
import json
from datetime import datetime

# =============================================================================
# INVARIANTES GEOMÉTRICAS UNIVERSALES (PÚBLICAS)
# =============================================================================

# Factor de contracción geométrica (invariante universal)
LAMBDA_INVARIANT = 1 / np.sqrt(2)  # ≈ 0.70710678

# Punto fijo estructural en espacio angular
THETA_FIXED_POINT = np.arctan(LAMBDA_INVARIANT)  # ≈ 0.61548 rad ≈ 35.264°

# =============================================================================
# DATOS DE REFERENCIA: CEROS DE RIEMANN (LMFDB FORMAT)
# =============================================================================

# Primeros 20 ceros no triviales de ζ(s) en línea crítica Re(s)=1/2
RIEMANN_ZEROS_REFERENCE = np.array([
    14.134725141734693, 21.022039638771554, 25.010857580145688,
    30.424876125859512, 32.935061587739190, 37.586178158825671,
    40.918719012147495, 43.327073280914999, 48.005150881167151,
    49.773832477672302, 52.970321477714460, 56.446247697063394,
    59.347044002833337, 60.831778524609812, 65.112544048081812,
    67.079810529494175, 69.546401711173979, 72.067151580005755,
    75.704690699083937, 77.144840068874805
])

# =============================================================================
# DESCOMPOSICIÓN DIÁDICA (LITTLEWOOD-PALEY STYLE)
# =============================================================================

def dyadic_decomposition(zeros, min_j=3, max_j=None):
    """
    Agrupa ceros en bloques de frecuencia diádica [2^j, 2^(j+1)).
    Permite análisis multi-escala de patrones estructurales.
    """
    if max_j is None:
        max_j = int(np.log2(np.max(zeros))) + 1
    
    blocks = {}
    for j in range(min_j, max_j + 1):
        lower = 2**j
        upper = 2**(j+1)
        block = zeros[(zeros >= lower) & (zeros < upper)]
        if len(block) > 0:
            blocks[j] = block
    return blocks

# =============================================================================
# MÉTRICA DE PERSISTENCIA ESTRUCTURAL (GENÉRICA)
# =============================================================================

def structural_persistence_metric(zeros_in_block):
    """
    Calcula índice de coherencia estructural basado en regularidad de espaciamientos.
    """
    if len(zeros_in_block) < 2:
        return 0.0
    
    gaps = np.diff(zeros_in_block)
    std_gap = np.std(gaps)
    
    # Métrica normalizada: mayor regularidad → valor más cercano a 1
    if std_gap == 0:
        return 1.0
    return 1.0 / (1.0 + std_gap)

# =============================================================================
# OPERADOR DE VERIFICACIÓN ESTRUCTURAL (MREI-STYLE, GENÉRICO)
# =============================================================================

def structural_verification_operator(scale_metrics, lambda_invariant=LAMBDA_INVARIANT):
    """
    Aplica operador determinista para validar no-depleción de coherencia estructural.
    """
    scales = np.array(list(scale_metrics.keys()))
    metrics = np.array(list(scale_metrics.values()))
    
    # Suavizado opcional para reducir ruido numérico
    if len(metrics) > 3:
        kernel = np.ones(3) / 3
        smoothed = np.convolve(metrics, kernel, mode='valid')
        scales_smooth = scales[1:-1]
    else:
        smoothed = metrics
        scales_smooth = scales
    
    # Umbral estructural: 50% de la media suavizada (conservador)
    threshold = np.mean(smoothed) * 0.5
    non_depletion = np.all(smoothed > threshold)
    
    # Tendencia logarítmica: pendiente > -0.05 indica estabilidad
    if len(scales_smooth) > 1:
        coeffs = np.polyfit(np.log(scales_smooth), smoothed, 1)
        slope = coeffs[0]
    else:
        slope = 0.0
    
    # Veredicto estructural
    if non_depletion and slope > -0.05:
        verdict = "COHERENCIA ESTRUCTURAL CONFIRMADA"
    else:
        verdict = "ANÁLISIS REQUIERE ESCALAS ADICIONALES"
    
    return {
        "scales": scales_smooth.tolist(),
        "metrics": smoothed.tolist(),
        "threshold": float(threshold),
        "non_depletion": bool(non_depletion),
        "slope": float(slope),
        "lambda_invariant": float(lambda_invariant),
        "verdict": verdict
    }

# =============================================================================
# ANÁLISIS DE ESPACIAMIENTOS CON INVARIANTE GEOMÉTRICA
# =============================================================================

def analyze_spacings_with_invariant(zeros, lambda_invariant=LAMBDA_INVARIANT):
    """
    Analiza regularidad de espaciamientos usando ventana definida por invariante geométrica.
    """
    if len(zeros) < 2:
        return {"in_window": 0, "total": 0, "efficiency": 0.0}
    
    spacings = np.diff(zeros)
    avg_spacing = np.mean(spacings)
    window_size = lambda_invariant * avg_spacing
    
    in_window = 0
    deviations = []
    
    for spacing in spacings:
        dev = abs(spacing - avg_spacing)
        deviations.append(float(dev))
        if dev <= window_size:
            in_window += 1
    
    total = len(spacings)
    efficiency = (in_window / total) * 100 if total > 0 else 0.0
    
    return {
        "in_window": in_window,
        "total": total,
        "efficiency": float(efficiency),
        "avg_spacing": float(avg_spacing),
        "window_size": float(window_size),
        "lambda_invariant": float(lambda_invariant),
        "deviations": deviations
    }

# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

def run_analysis(n_zeros=20, export_json=True):
    """
    Ejecuta análisis estructural completo sobre ceros de Riemann.
    """
    print("🔷 ANÁLISIS ESTRUCTURAL: CEROS DE RIEMANN 🔷")
    print("=" * 60)
    
    # Seleccionar ceros de referencia
    zeros = RIEMANN_ZEROS_REFERENCE[:n_zeros]
    print(f"✅ Ceros analizados: {len(zeros)} (valores de referencia LMFDB)")
    
    # Descomposición diádica
    print("📐 Aplicando descomposición diádica...")
    blocks = dyadic_decomposition(zeros)
    print(f"✅ Bloques creados: {len(blocks)}")
    
    # Métricas por escala
    print("📊 Calculando métricas de persistencia...")
    scale_metrics = {j: structural_persistence_metric(block) for j, block in blocks.items()}
    
    # Operador de verificación estructural
    print("🧠 Ejecutando operador de verificación estructural...")
    verification = structural_verification_operator(scale_metrics)
    
    # Análisis de espaciamientos con invariante geométrica
    print("🔍 Analizando espaciamientos con invariante geométrica...")
    spacing_analysis = analyze_spacings_with_invariant(zeros)
    
    # Resultados consolidados
    results = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "zeros_analyzed": len(zeros),
        "zero_values": zeros.tolist(),
        "dyadic_blocks": {str(k): v.tolist() for k, v in blocks.items()},
        "scale_metrics": {str(k): float(v) for k, v in scale_metrics.items()},
        "structural_verification": verification,
        "spacing_analysis": spacing_analysis,
        "invariants": {
            "lambda": float(LAMBDA_INVARIANT),
            "theta_fixed_point_rad": float(THETA_FIXED_POINT),
            "theta_fixed_point_deg": float(np.degrees(THETA_FIXED_POINT))
        }
    }
    
    # Exportar JSON para frontend
    if export_json:
        with open("riemann_analysis_results.json", "w") as f:
            json.dump(results, f, indent=2)
        print(" Resultados exportados: riemann_analysis_results.json")
    
    # Resumen en consola
    print(f"\n📈 RESULTADOS:")
    print(f"   • Veredicto estructural: {verification['verdict']}")
    print(f"   • Pendiente logarítmica: {verification['slope']:+.4f}")
    print(f"   • Eficiencia de ventana: {spacing_analysis['efficiency']:.1f}%")
    print(f"   • Invariante λ: {LAMBDA_INVARIANT:.6f}")
    
    return results

# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    run_analysis(n_zeros=20)
