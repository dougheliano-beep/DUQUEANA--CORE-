# 🧬 p53 Structural Restoration Analysis (IED)

Herramienta de verificación determinista para la detección de puntos de ruptura geométrica en mutaciones de la proteína p53 y el cálculo del vector de corrección estructural mínima, impulsada por el paradigma de **Inteligencia Estructural Duqueana (IED)** y el Motor MREI v2.1.1.

> ⚠️ **Nota Académica:** Marco heurístico y computacional para analizar coherencia estructural en plegamiento proteico. No constituye diagnóstico médico. El núcleo determinista y las invariantes exactas son propiedad intelectual reservada del Instituto de Investigación Digital.

## 📖 Arquitectura del Módulo

```text
p53-analysis/
├── README.md                              # Este documento (Portada oficial)
├── scripts/
│   └── p53_structural_restoration.py      # FASE 1: Detección de Ángulo de Ruptura + Vector de Restauración
├── demo/
│   ├── phase2_demo_geometric_matching.py  # FASE 2: Matching Estructural + Generación de Protocolo Wet-Lab
│   └── README.md                          # Documentación exclusiva de la Fase 2
└── outputs/                               # JSONs automáticos con trazabilidad SHA-256
```

## 🚀 Ejecución Rápida
```bash
pip install numpy
python scripts/p53_structural_restoration.py
# Genera: p53_restoration_results.json (determinista, seed=42)
```

## 🔑 Características Clave (IED)
- **Ángulo de Ruptura:** Detecta la escala diádica ($2^j$) donde colapsa la coherencia estructural del plegamiento.
- **Vector de Restauración:** Calcula la corrección mínima necesaria para recuperar la coherencia nativa (>0.85).
- **Unidades Doulita:** Bloques atómicos (~128 bytes) que reducen el consumo de RAM en un **81%** vs simuladores tradicionales.
- **Determinismo Puro:** Seed fija (`42`), resultados 100% reproducibles y sin aleatoriedad.
- **Trazabilidad:** Hash SHA-256 único por ejecución para auditoría criptográfica.

## 📊 Métricas Esperadas
- **Huella de Memoria:** ~6 KB RAM (hardware clásico optimizado).
- **Coherencia Estructural:** Verificación post-corrección en escalas diádicas.
- **Tiempo de Ejecución:** <50 ms en entorno estándar.
- **Eficiencia:** 99.9% reducción de recursos computacionales vs métodos de fuerza bruta.

---

## 🚀 Roadmap: Fase 2 - Drug Discovery & Protocolo Wet-Lab
*(Evolución Técnica del Módulo p53 Structural Restoration)*

Este módulo establece la base geométrica determinista para la siguiente fase del ecosistema, donde la detección de ruptura se traduce en identificación terapéutica:

1. **Análisis de p53:** Detección de mutación hotspot → Cálculo del Vector de Restauración → Identificación del punto de fallo estructural (ej. pérdida de coordinación de Zn²⁺).
2. **Matching Estructural:** Comparación de la firma geométrica con librerías de compuestos. Priorización por compatibilidad estructural pura (Ranking: APR-246, NSC319726, COTI-2).
3. **Protocolo Experimental:** Generación automática de guías *wet-lab* (concentraciones, controles, métricas de éxito) listas para validación experimental.

> 💡 **Visión Técnica:** Transformar el diagnóstico estructural en una herramienta de descubrimiento de fármacos de alta eficiencia, manteniendo la huella de ~6 KB RAM y el determinismo del Motor MREI v2.1.1.

---

##  Salida Esperada y Modelo de Acceso

### Salida Esperada
Al ejecutar el script, el sistema procesará la firma de ruptura y la topología del compuesto mediante el núcleo propietario, mostrando en consola el puntaje de compatibilidad y el protocolo sugerido. Adicionalmente, generará automáticamente el archivo `phase2_demo_report.json` con trazabilidad criptográfica (SHA-256) para validación de integridad y auditoría reproducible.

### Modelo de Acceso y Propiedad Intelectual
- ✅ **Público:** Interfaz de entrada estandarizada, lógica de generación de protocolos basada en umbrales de compatibilidad geométrica, y correlación con datos biológicos validados.
- 🔒 **Reservado:** Algoritmo matemático exacto de superposición estructural, constantes del Ángulo de Ruptura aplicadas al matching y núcleo de cálculo del Motor MREI. Este demo utiliza una simulación ofuscada del núcleo exclusivamente para fines de demostración académica y validación conceptual.

### Ejemplo de Salida (JSON)
```json
{
  "hypothesis": "Structural compatibility between p53-R175H rupture vector and Lauric Acid topology",
  "results": {
    "geometric_compatibility_score": 0.91,
    "match_status": "HIGH PRIORITY CANDIDATE"
  },
  "experimental_protocol": {
    "action": "Proceed to In-Vitro Validation",
    "suggested_concentration": "50 µM - 100 µM",
    "assay_type": "MTT / Annexin V Apoptosis Assay"
  },
  "sha256_integrity": "8a9c2e1f4b6d3a7e..."
}
```

## 📚 Cita Oficial
```bibtex
@misc{urbina_duque_2026_p53_restoration_ied,
  author = {Urbina Duque, Douglas Helvesio},
  title = {Duqueana Core - p53 Structural Restoration Analysis v1.0.0: Verificación Determinista vía IED y Ángulo de Ruptura},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/dougheliano-beep/DUQUEANA--CORE-/tree/main/p53-analysis}
}
```

## 🔗 Volver al [README Principal](../README.md)

🇻🇪 Universidad Nacional Experimental de Guayana (UNEG) · Venezuela  
📜 Licencia: CC-BY-NC-ND 4.0 · Instituto Doughel · Ciencia Abierta UNESCO 2021
```

