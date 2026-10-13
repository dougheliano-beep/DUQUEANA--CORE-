# 🧬 Duqueana Core Biolab · Génesis

## Módulo p53-analysis

Módulo determinista para el análisis estructural de la proteína supresora de tumores **p53** y sus variantes. Incluye demos ejecutables, especificación de verificación y metadatos oficiales.

**DOI conceptual:** [10.5281/zenodo.23289817](https://doi.org/10.5281/zenodo.23289817)

---

## 📌 Qué es este módulo

El módulo **p53-analysis** forma parte del ecosistema **Duqueana Core Biolab** y hospeda las aplicaciones de **Génesis** sobre la proteína p53 y sus complejos:

- **p53 wild-type** — conformación nativa.
- **p53-R175H** — mutación hotspot en cáncer.
- **Complejo p53-MDM2** — interfaz proteína-proteína crítica en oncología.

Todos los demos exponen **únicamente la interfaz** y la **trazabilidad criptográfica (SHA-256)**. El motor determinista propietario del Instituto Doughel **no está incluido** en este repositorio.

---

## 📦 Contenido del módulo

### Demos ejecutables

| Archivo | Descripción |
|---|---|
| `genesis_p53_adn_demo.py` | Interfaz general del módulo Génesis (p53-ADN). Demo de trazabilidad SHA-256 sobre interfaz de entrada/salida. |
| `analisis_mutacion_r175h_demo.py` | Análisis comparativo Wild-Type vs mutación R175H. Interfaz determinista con trazabilidad por variante. |
| `analisis_ppi_p53_mdm2_demo.py` | Análisis de la interfaz proteína-proteína p53-MDM2. Comparación de configuraciones WT y alteradas. |

### Documentos oficiales

| Documento | DOI |
|---|---|
| Paper inaugural de Génesis | [10.5281/zenodo.23289817](https://doi.org/10.5281/zenodo.23289817) |
| Protocolo de Verificación Génesis v1.0 | [10.5281/zenodo.23330991](https://doi.org/10.5281/zenodo.23330991) |

### DOIs de versión

| Versión | DOI | Descripción |
|---|---|---|
| v1.0.0 | [10.5281/zenodo.23304435](https://doi.org/10.5281/zenodo.23304435) | Release inicial del módulo Génesis |
| v1.0.1 | [10.5281/zenodo.23307303](https://doi.org/10.5281/zenodo.23307303) | Análisis de mutación R175H |
| v1.0.2 | [10.5281/zenodo.23321645](https://doi.org/10.5281/zenodo.23321645) | Interfaz proteína-proteína p53-MDM2 |

### Secuencia canónica de referencia

- `input/p53_HUMAN_WT_393aa.fasta` — Secuencia canónica de p53 humana (UniProt P04637, isoforma 1, 393 aa).

---

## 🚀 Cómo ejecutar los demos

Todos los demos **no requieren dependencias externas** (solo biblioteca estándar de Python 3).

### Demo general

```bash
python genesis_p53_adn_demo.py
