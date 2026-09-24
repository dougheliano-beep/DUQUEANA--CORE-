
#  Genomic Structural Analysis (IED)

Herramienta de verificación determinista para el análisis estructural de secuencias genómicas, impulsada por el paradigma de **Inteligencia Estructural Duqueana (IED)** y el Motor MREI v2.1.1.

> ️ **Nota Académica:** Esta herramienta **no es un diagnóstico médico**. Proporciona un framework heurístico y computacional para analizar patrones de coherencia y simetría en secuencias mediante descomposición diádica, con una eficiencia extrema de recursos (~6 KB RAM estimados para indexación básica) y trazabilidad total.

## 📖 Arquitectura
genomic-analysis/
├── README.md                              # Este documento
├── scripts/
│   └── genomic_structural_analysis.py     # Backend: Indexación con Doulitas + MREI Engine
└── src/
    └── GenomicStructuralDashboard.jsx     # Frontend: Visualización de escalas diádicas

    
## 🚀 Ejecución

### Backend (Python)
```bash
pip install numpy
python scripts/genomic_structural_analysis.py
# Genera: genomic_analysis_results.json (determinista, seed=42)
npm install
npm run dev
# Acceder a: http://localhost:3000
