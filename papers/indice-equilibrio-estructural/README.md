# Índice de Equilibrio Estructural (C)

**Paper:** [DOI 10.5281/zenodo.24179269](https://doi.org/10.5281/zenodo.24179269)

**Autor:** Prof. Douglas Helvesio Urbina Duque (ORCID [0009-0005-1230-7549](https://orcid.org/0009-0005-1230-7549))

**Institución:** Instituto Doughel · Universidad Nacional Experimental de Guayana (UNEG), Venezuela

**Fecha:** Noviembre 2026

**Licencia:** CC BY-NC-ND 4.0

---

## Resumen

Métrica que evalúa el equilibrio entre Memoria (M), Velocidad (V) y Calidad (Q) en arquitecturas de IA. Mide la distancia euclidiana al cuadrado respecto al punto ideal (100, 100, 100).

## Fórmula

$$C = (100 - E_m)^2 + (100 - V_{norm})^2 + (100 - Q_{norm})^2$$

Donde:
- $E_m$ = Eficiencia de Memoria
- $V_{norm}$ = Velocidad Normalizada
- $Q_{norm}$ = Calidad Normalizada

## Resultados

| Métrica | Modelo Clásico (14B Q4 en 4GB) | Modelo IED (DouSan) |
|---|---|---|
| RAM Requerida | > 8.5 GB (swap severo) | ~ 2.3 GB |
| Eficiencia Mem. ($E_m$) | 0 (inviable) | 85.0 |
| Velocidad (tok/s) | < 1.0 | 15.0 – 20.0 |
| Calidad (MMLU %) | 68.0% | 68.0% |
| Índice C | > 14,000 (colapso) | ~ 1,500 |

**Mejora en equilibrio:** ~87-89%.

## Archivos

- [`paper.md`](./paper.md) — Paper completo en markdown.
- [`graficos.py`](./graficos.py) — Código Python para generar los gráficos comparativos.

## Cómo generar los gráficos

```bash
pip install matplotlib numpy
python graficos.py
