#!/usr/bin/env python3
# ==============================================================================
# DUQUEANA CORE BIOLAB - DEMO DE ANÁLISIS DE MUTACIÓN
# Módulo: Génesis v1.0 (p53 R175H vs Wild-Type)
# Autor: Douglas Helvesio Urbina Duque | Instituto Doughel
# ORCID: 0009-0005-1230-7549
# DOI: 10.5281/zenodo.23289817
# Licencia: CC BY-NC-ND 4.0 (Uso académico con citación obligatoria).
#           Uso comercial prohibido sin licencia del Instituto Doughel.
#
# ------------------------------------------------------------------------------
# ALCANCE DE ESTE ARCHIVO
# ------------------------------------------------------------------------------
# Este demo expone únicamente la interfaz de análisis comparativo de variantes.
# El motor determinista del Instituto Doughel no está incluido en este archivo.
# Los scores mostrados son valores de referencia ilustrativos.
# ==============================================================================

import hashlib
import json
from typing import Dict, Any

# ------------------------------------------------------------------------------
# METADATOS OFICIALES
# ------------------------------------------------------------------------------
METADATOS = {
    "autor": "Douglas Helvesio Urbina Duque",
    "institucion": "Instituto Doughel · UNEG · UNET, Venezuela",
    "orcid": "0009-0005-1230-7549",
    "modulo": "Génesis v1.0",
    "doi": "10.5281/zenodo.23289817",
    "doi_version": "10.5281/zenodo.23304435",
    "licencia": "CC BY-NC-ND 4.0",
}

# Scores de referencia ilustrativos (no son output del motor real)
SCORES_REFERENCIA = {
    "Wild-Type": 0.9874,
    "R175H": 0.7235,
}


def analizar_mutacion_p53(tipo_variante: str) -> Dict[str, Any]:
    """
    Interfaz pública para analizar variantes de p53.

    NOTA: Los scores retornados son valores de referencia ilustrativos.
    La validación estructural real se ejecuta con el núcleo propietario
    del Instituto Doughel.

    Retorna un diccionario con variante, score de referencia, hash de
    trazabilidad y metadatos oficiales.
    """
    # 1. Normalización de entrada
    entrada = json.dumps(
        {"proteina": "p53", "variante": tipo_variante},
        sort_keys=True,
    )

    # 2. Score de referencia (ilustrativo)
    score = SCORES_REFERENCIA.get(tipo_variante, 0.0)

    # 3. Generación de hash SHA-256
    payload = (
        f"{entrada}"
        f"|score:{score:.4f}"
        f"|modelo:genesis_v1.0"
        f"|analisis:mutacion"
        f"|demo:v1.0"
        f"|doi:{METADATOS['doi']}"
    )
    hash_trazabilidad = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    return {
        "variante": tipo_variante,
        "score_coherencia_estructural": score,
        "hash_trazabilidad_sha256": hash_trazabilidad,
        "estado": "ANÁLISIS DETERMINISTA COMPLETADO",
        "metadatos": {
            "autor": METADATOS["autor"],
            "institucion": METADATOS["institucion"],
            "orcid": METADATOS["orcid"],
            "doi": METADATOS["doi"],
            "licencia": METADATOS["licencia"],
        },
    }


# ==============================================================================
# EJECUCIÓN COMPARATIVA
# ==============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print(" DUQUEANA CORE BIOLAB | GÉNESIS v1.0")
    print(" Análisis Comparativo: p53 Wild-Type vs Mutación R175H")
    print("=" * 70)

    variantes = ["Wild-Type", "R175H"]

    print("\n[INFO] Ejecutando análisis determinista de variantes...\n")

    for variante in variantes:
        resultado = analizar_mutacion_p53(variante)
        print(f" Variante : {resultado['variante']}")
        print(f" Score    : {resultado['score_coherencia_estructural']:.4f} (referencia)")
        print(f" Hash     : {resultado['hash_trazabilidad_sha256']}")
        print(f" Estado   : {resultado['estado']}")
        print("-" * 70)

    print("\n NOTA: Ejecuciones repetidas con los mismos parámetros generan")
    print("       idéntico hash. Los scores son valores de referencia.")
    print("=" * 70)
    print(f" DOI Oficial : {METADATOS['doi']}")
    print(f" DOI Versión : {METADATOS['doi_version']}")
    print(f" Licencia    : {METADATOS['licencia']} | Instituto Doughel, Venezuela")
    print("=" * 70)
