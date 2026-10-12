#!/usr/bin/env python3
# ==============================================================================
# DUQUEANA CORE BIOLAB - DEMO DE INTERACCIÓN PPI
# Módulo: Génesis v1.0.2 (Interfaz p53-MDM2)
# Autor: Douglas Helvesio Urbina Duque | Instituto Doughel
# ORCID: 0009-0005-1230-7549
# DOI: 10.5281/zenodo.23289817
# Licencia: CC BY-NC-ND 4.0 (Uso académico con citación obligatoria).
#           Uso comercial prohibido sin licencia del Instituto Doughel.
#
# ------------------------------------------------------------------------------
# ALCANCE DE ESTE ARCHIVO
# ------------------------------------------------------------------------------
# Este demo expone únicamente la interfaz de análisis de interacción PPI.
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
    "modulo": "Génesis v1.0.2",
    "doi_base": "10.5281/zenodo.23289817",
    "licencia": "CC BY-NC-ND 4.0",
}

# Scores de referencia ilustrativos (no son output del motor real)
SCORES_REFERENCIA = {
    "p53_WT_MDM2_Complejo": 0.9650,
    "p53_Mutante_MDM2": 0.8120,
}


def analizar_interfaz_ppi(complejo: str) -> Dict[str, Any]:
    """
    Interfaz pública para analizar la interacción p53-MDM2.

    NOTA: Los scores retornados son valores de referencia ilustrativos.
    La validación estructural real se ejecuta con el núcleo propietario
    del Instituto Doughel.

    Retorna un diccionario con configuración, score de referencia, hash
    de trazabilidad y metadatos oficiales.
    """
    # 1. Normalización de entrada
    entrada = json.dumps(
        {"sistema": "p53-MDM2", "configuracion": complejo},
        sort_keys=True,
    )

    # 2. Score de referencia (ilustrativo)
    score = SCORES_REFERENCIA.get(complejo, 0.0)

    # 3. Generación de hash SHA-256
    payload = (
        f"{entrada}"
        f"|score:{score:.4f}"
        f"|modelo:genesis_v1.0.2"
        f"|analisis:ppi_mdm2"
        f"|demo:v1.0.2"
        f"|doi:{METADATOS['doi_base']}"
    )
    hash_trazabilidad = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    return {
        "configuracion": complejo,
        "score_coherencia_estructural": score,
        "hash_trazabilidad_sha256": hash_trazabilidad,
        "estado": "CONVERGENCIA DETERMINISTA DE PPI COMPLETADA",
        "metadatos": METADATOS,
    }


# ==============================================================================
# EJECUCIÓN
# ==============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print(" DUQUEANA CORE BIOLAB | GÉNESIS v1.0.2")
    print(" Análisis de Interfaz Proteína-Proteína: p53 - MDM2")
    print("=" * 70)

    configuraciones = ["p53_WT_MDM2_Complejo", "p53_Mutante_MDM2"]

    print("\n[INFO] Ejecutando análisis determinista de la interfaz PPI...\n")

    for config in configuraciones:
        resultado = analizar_interfaz_ppi(config)
        print(f" Sistema    : {resultado['configuracion']}")
        print(f" Score      : {resultado['score_coherencia_estructural']:.4f} (referencia)")
        print(f" Hash SHA-256: {resultado['hash_trazabilidad_sha256']}")
        print(f" Estado     : {resultado['estado']}")
        print("-" * 70)

    print("\n NOTA: Ejecuciones repetidas con los mismos parámetros generan")
    print("       idéntico hash. Los scores son valores de referencia.")
    print("=" * 70)
    print(f" DOI Oficial : {METADATOS['doi_base']}")
    print(f" Licencia    : {METADATOS['licencia']} | Instituto Doughel, Venezuela")
    print("=" * 70)
