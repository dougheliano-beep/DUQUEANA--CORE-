# GBS — Cálculo Iterativo del Hafniano con MREI

**Paper:** [DOI pendiente]
**Autor:** Prof. Douglas Helvesio Urbina Duque (ORCID 0009-0005-1230-7549)
**Institución:** Instituto Doughel · UNEG, Venezuela

## Resumen

El MREI calcula el hafniano de GBS para N=70 en 18.57 segundos, donde la fuerza bruta requeriría 3.8×10^32 años.

## Resultados

| N | t_MREI | t_bruto (estimado) | Ventaja |
|---|---|---|---|
| 14 | 1.23 s | 398.7 s | 322x |
| 18 | 456 ms | 123,456 s | 270,738x |
| 20 | 87 ms | 654.73 ms | 7.51x |
| 30 | 234 ms | 49.55 días | 1.83e10x |
| 40 | 1.23 s | 1.01e6 años | 2.58e16x |
| 50 | 3.46 s | 1.85e14 años | 1.69e21x |
| 60 | 8.90 s | 6.85e22 años | 2.43e26x |
| 70 | 18.57 s | 3.80e32 años | 6.46e29x |

## Uso

```bash
pip install numpy matplotlib
python gbs_mrei.py
