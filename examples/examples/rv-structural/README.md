# 🦠 SARS-CoV-2 & Rhinovirus Structural Dynamics
**Duqueana Core · MREI v2.0**  
**Instituto Doughel · UNEG**

## 📖 Descripción
Este módulo analiza la **dinámica conformacional estructural** del SARS-CoV-2 (y variantes relacionadas), enfocándose en la transición energética del dominio RBD (Receptor Binding Domain) y la interacción con receptores (ACE2).

Utilizando el framework **Duqueana Core**, se evalúa:
- Energía de transición conformacional (Down → Up).
- Efectos de glicosilación en la estabilidad.
- Consistencia energética bajo el modelo MREI.

## 📂 Archivos
- `rv_simulation_results.json`: Resultados estructurales de la simulación.
- `spike_simulator.js` (o nombre del script): Script de cálculo energético.
- `README.md`: Este archivo.

##  Parámetros del Escenario

| Parámetro | Valor | Unidad |
|-----------|-------|--------|
| Energía RBD Down (Referencia) | 100.00 | u.e. |
| Energía RBD Up (Simulada) | 118.47 | u.e. |
| Efecto Glicosilación | -5.23 | u.e. |
| **Energía Neta Post-Glicosilación** | **113.24** | **u.e.** |

## 🔍 Interpretación Post-Clásica
Bajo el enfoque de **Estructura sobre Secuencia**:
1.  **Delta Energético:** La transición implica un costo de **18.47 u.e.**
2.  **Estabilidad:** La glicosilación actúa como estabilizador termodinámico.
3.  **Coherencia:** Los valores se mantienen dentro de los umbrales de plausibilidad física definidos por el Manifiesto Post-Clásico.

## ⚠️ Disclaimer
Este es un análisis *in silico* basado en topología estructural y energía potencial. No sustituye validación experimental wet-lab.

## 🔗 Referencias
- **DOI del Escenario:** [10.5281/zenodo.22380336](https://doi.org/10.5281/zenodo.22380336)
- **Autor:** Douglas Helvesio Urbina Duque (ORCID: 0009-0005-1230-7549)
