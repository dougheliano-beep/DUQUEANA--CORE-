# Doughelia: Primera Arquitectura de Inteligencia Artificial Estructural Duqueana (IED)

**Autor:** Lcdo. Douglas Helvesio Urbina Duque
**ORCID:** 0009-0005-1230-7549
**Institución:** Instituto Doughel · UNEG, Venezuela
**Licencia:** CC BY-NC-ND 4.0

## ¿Qué es Doughelia?

Es la primera arquitectura de Inteligencia Artificial desarrollada bajo el paradigma de la **Inteligencia Estructural Duqueana (IED)**. No es un modelo de lenguaje desde cero, sino un **Framework de Orquestación Iterativa** que actúa sobre modelos preentrenados para garantizar el rigor epistemológico y reducir drásticamente el consumo de recursos.

## Arquitectura de 3 Agentes

1. **Generador:** Genera una respuesta base.
2. **Crítico Epistemológico:** Evalúa la respuesta contra los Guardrails y el SAG (≥ 0.90). Si falla, la rechaza.
3. **Optimizador:** Ajusta la consulta para la siguiente iteración hasta lograr la convergencia.

## Eficiencia y Consumo de RAM

A diferencia de los modelos de lenguaje tradicionales que requieren cargar gigabytes de pesos en memoria para cada inferencia, Doughelia opera mediante un protocolo de **carga bajo demanda**. 

Las simulaciones preliminares demuestran que esta arquitectura logra una **reducción del 90% en el consumo de memoria RAM**, permitiendo que el framework de validación se ejecute en hardware de consumo convencional (PCs estándar) con una huella operativa mínima.

## Archivos del Módulo

- `doughelia_architecture.py`: Esqueleto de la arquitectura de los 3 agentes (Python).
- `doughelia_codemeta.json`: Metadatos del software para indexación.

## Nota sobre el Motor MREI

Doughelia utiliza el Motor MREI como base para la validación iterativa, pero es una capa independiente. El motor MREI permanece como propiedad intelectual del Instituto Doughel.

## Enlace a Zenodo

*https://doi.org/10.5281/zenodo.23679560*
