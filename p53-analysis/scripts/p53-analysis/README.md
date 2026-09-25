# 🧬 p53 Structural Restoration Analysis (IED)

Herramienta de verificación determinista para la detección de puntos de ruptura geométrica en mutaciones de la proteína p53 y el cálculo del vector de corrección estructural mínima, impulsada por el paradigma de **Inteligencia Estructural Duqueana (IED)** y el Motor MREI v2.1.1.

> ⚠️ **Nota Académica:** Esta herramienta proporciona un marco heurístico y computacional para analizar la coherencia estructural del plegamiento proteico. No constituye un diagnóstico médico ni una demostración formal de propiedades biológicas. El núcleo computacional determinista y las invariantes exactas son propiedad intelectual reservada.
## 🔑 Características Clave (IED)

- **Detección del Ángulo de Ruptura:** Identifica la escala diádica exacta ($2^j$) donde la coherencia estructural del plegamiento colapsa.
- **Vector de Restauración:** Calcula la magnitud de la corrección estructural mínima necesaria para recuperar la coherencia nativa (>0.85).
- **Unidades Doulita:** Emplea bloques atómicos optimizados (~128 bytes) para reducir el consumo de RAM en un **81%**.
- **Determinismo Puro:** Resultados 100% reproducibles (`seed=42`).
- **Trazabilidad:** Hash SHA-256 único por ejecución.

## 🔐 Modelo de Acceso
- ✅ **Público:** Framework IED, concepto de Ángulo de Ruptura, métricas Doulita, pipeline reproducible.
- 🔒 **Reservado:** Valores exactos de invariantes, fórmula del vector de restauración, núcleo MREI completo.

##  Métricas Esperadas
- **Huella de Memoria:** Reducción del 81% vs métodos estándar.
- **Coherencia Estructural:** Verificación de estabilidad post-corrección.
- **RAM Utilizada:** ~6 KB (hardware clásico optimizado).

## 🔗 Volver al [README Principal](../README.md)

🇻🇪 Universidad Nacional Experimental de Guayana (UNEG) · Venezuela  
📜 Licencia: CC-BY-NC-ND 4.0 · Ciencia Abierta UNESCO 2021
## 📖 Arquitectura

```text
p53-analysis/
├── README.md                                     # Este documento
├── scripts/
│   └── p53_structural_restoration.py             # Backend: Detección de Ángulo de Ruptura y Vector de Restauración
└── outputs/
    └── p53_restoration_results.json              # Salida determinista con trazabilidad SHA-256
pip install numpy
python scripts/p53_structural_restoration.py
# Genera: p53_restoration_results.json (determinista, seed=42)
@misc{urbina_duque_2026_p53_restoration_ied,
  author = {Urbina Duque, Douglas Helvesio},
  title = {Duqueana Core - p53 Structural Restoration Analysis v1.0.0: Verificación Determinista vía IED y Ángulo de Ruptura},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/dougheliano-beep/DUQUEANA--CORE-/tree/main/p53-analysis}
}
