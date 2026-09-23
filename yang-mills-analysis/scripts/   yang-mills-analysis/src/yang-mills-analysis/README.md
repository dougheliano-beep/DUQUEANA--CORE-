#  Yang-Mills Structural Analysis

Herramienta de validación estructural para el análisis de estabilidad en campos de gauge y verificación de la brecha espectral (Mass Gap), impulsada por el marco de **IA post-clásica Duqueana Core**.

> ️ **Nota Académica:** Esta herramienta **no demuestra la existencia del Mass Gap ni resuelve el Problema del Milenio de Yang-Mills**.
> Proporciona un framework heurístico y determinista para analizar coherencia estructural en configuraciones de retículo, con trazabilidad total y ~6 KB RAM. Los resultados son indicadores de patrón,
>  no pruebas matemáticas formales.

## 📖 Arquitectura
yang-mills-analysis/
├── README.md                              # Este documento
├── scripts/
│   └── yang_mills_structural_analysis.py  # Backend: generación determinista + MREI Engine v2.1.1
└── src/
    └── YangMillsStructuralDashboard.jsx   # Frontend React: visualización + hash SHA-256
    @misc{urbina_duque_2026_yang_mills_structural,
  author = {Urbina Duque, Douglas Helvesio},
  title = {Yang-Mills Structural Analysis: Heuristic Validation via Post-Classical Deterministic AI},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/dougheliano-beep/DUQUEANA--CORE-/tree/main/yang-mills-analysis}
}
    
## 🚀 Ejecución

### Backend (Python)
```bash
pip install numpy
python scripts/yang_mills_structural_analysis.py
# Genera: yang_mills_analysis_results.json (determinista, seed=42)
npm install
npm run dev
# Acceder a: http://localhost:3000

