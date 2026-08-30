# 🧬 Doulita Token Compressor
### Geometric Context Compression for LLMs | Research Preview

> **DOI:** [10.5281/zenodo.22168535](https://doi.org/10.5281/zenodo.22168535)  
> **Estado:** Research Preview (Agosto 2026) | **Instituto Doughel de Investigación Digital**

⚠️ **AVISO IMPORTANTE:** Este repositorio contiene una demostración reproducible del flujo y cálculo de reducción. El script aplica un **factor fijo de simulación (98.5%)** y **NO ejecuta el algoritmo propietario Doulita/MREI**. No constituye validación de producción, auditoría externa ni preservación semántica certificada.

---

##  Benchmarks Preliminares (Declarados)
| Tipo de entrada | Original | Comprimido (sim.) | Ahorro |
|----------------|----------|-------------------|--------|
| Server logs (10k líneas) | ~10,000 tokens | ~120 tokens | 98.8% |
| JSON grande (500 KB) | ~5,000 tokens | ~85 tokens | 98.3% |
| Mapa de codebase | ~2,000 tokens | ~40 tokens | 98.0% |

*Nota: Métricas estimadas con `tiktoken`. Resultados reales varían según entropía de datos, tokenizer y versión del código. Requieren dataset, código ejecutable y revisión independiente para convertirse en benchmark auditable.*

---

## 🛡️ Propiedad Intelectual y Acceso
El algoritmo central de compresión geométrica, reglas MREI, unidades Doulita y código fuente completo son **tecnología propietaria** del Instituto Doughel.

| Modalidad | Alcance |
|-----------|---------|
| 🎓 Colaboración académica | Evaluación no comercial bajo autorización escrita |
| 🏢 Integración empresarial | Asistencia técnica, adaptación y soporte contractual |
| 🔐 Revisión bajo NDA | Acceso a código/componentes definidos bajo acuerdo de confidencialidad |

Este repositorio **no concede licencia** para extraer, reconstruir ni redistribuir el algoritmo propietario.

---

## ✅ Estado de Validación (Matriz)
| Afirmación | Estado en esta versión |
|------------|------------------------|
| Script ejecutado sin errores | ✅ Confirmado |
| Reducción del 98.5% | ️ Simulación configurada (factor fijo) |
| Preservación semántica |  Hipótesis de diseño (pendiente de prueba) |
| Benchmarks 98.0–98.8% | 📋 Declarados (pendientes de archivo y repetición) |
| Compatibilidad con APIs LLM | 🧩 Conceptual (depende de integración por proveedor) |

---

## 🚀 Demostración Rápida
```bash
# Ejecutar demo con trial de 7 días
python demo.py

# Ejecutar con licencia válida
python demo.py --license DOUGHEL-PRO-XYZ
