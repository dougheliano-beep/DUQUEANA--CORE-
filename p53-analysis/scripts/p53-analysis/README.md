# 🧬 p53 Structural Restoration Analysis (IED)

Herramienta de verificación determinista para la detección de puntos de ruptura geométrica en mutaciones de la proteína p53 y el cálculo del vector de corrección estructural mínima, impulsada por el paradigma de **Inteligencia Estructural Duqueana (IED)** y el Motor MREI v2.1.1.

> ⚠️ **Nota Académica:** Esta herramienta proporciona un marco heurístico y computacional para analizar la coherencia estructural del plegamiento proteico. No constituye un diagnóstico médico ni una demostración formal de propiedades biológicas. El núcleo computacional determinista y las invariantes exactas son propiedad intelectual reservada.

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
