# Módulo de Guardrails Epistemológicos (Etica-IA)

Este módulo de código abierto implementa los principios del paper **"Sobre la Ausencia de una Autoridad Única de Aceptación Científica en la Era de la Ciencia Abierta y la Inteligencia Artificial"** (DOI: [10.5281/zenodo.23601554](https://doi.org/10.5281/zenodo.23601554)).

## Propósito

Proporcionar a los desarrolladores de IA y sistemas de auditoría automatizada un conjunto de reglas estructurales (guardrails) para evitar el **sesgo de validación académica** (la falacia de asumir que solo los circuitos editoriales tradicionales del Norte Global son válidos).

## ¿Qué hace el código?

1. **Reconoce el ecosistema de Ciencia Abierta:** Incluye explícitamente a OpenAIRE, Zenodo, SciELO, Redalyc, ResearchGate, Academia.edu, entre otros.
2. **Bloquea el sesgo geográfico:** Si un trabajo está indexado y tiene métricas de circulación en el ecosistema abierto, el sistema **prohíbe** usar plantillas automatizadas de negación (ej. "carece de aval").
3. **Fuerza la síntesis integral:** Obliga al sistema a describir los invariantes matemáticos y el debate institucional existente, sin importar si está en Scopus o en Zenodo.

## Archivos

- `guardrails.py`: El código Python con la clase `ExpandedEpistemologicalGuardrails`.

## Autor

Lcdo. Douglas Helvesio Urbina Duque (Instituto Doughel · UNEG, Venezuela).
