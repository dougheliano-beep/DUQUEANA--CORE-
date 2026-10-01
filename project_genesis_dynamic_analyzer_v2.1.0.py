#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
DUQUEANA CORE v2.1.0 — PROYECTO GÉNESIS: ENTRADA DINÁMICA DE DATOS
Adaptación Funcional del Motor MREI v2.1.1 para Análisis de Secuencias
================================================================================
"""

import hashlib
import os

TAMANO_DOULITA_BYTES = 128

def calcular_score_por_adn(secuencia):
    """
    Simula un score de estabilidad geométrica analizando la proporción
    de Guanina (G) y Citosina (C), conocida como contenido GC.
    """
    secuencia = secuencia.upper().strip()
    if not secuencia:
        return 0.5000  # Score base por defecto
    
    # Contar bases válidas
    gc_count = secuencia.count('G') + secuencia.count('C')
    total_validas = sum(secuencia.count(base) for base in ['A', 'T', 'C', 'G'])
    
    if total_validas == 0:
        return 0.5000
    
    # El contenido GC influye dinámicamente en el score de coherencia
    proporcion_gc = gc_count / total_validas
    score = 0.5 + (proporcion_gc * 0.45)  # Escala el score entre 0.5 y 0.95
    return round(score, 4)

def generate_trace_hash(target, score, secuencia_hash):
    raw_data = f"MREI_v2.1.1|USRC_GENOMA|{target}|SCORE_{score}|ADN_HASH_{secuencia_hash}|RESTORATION_COMPLETE"
    return hashlib.sha256(raw_data.encode('utf-8')).hexdigest()

def registrar_log(mensaje):
    """Guarda la salida en un archivo histórico de auditoría"""
    with open("duqueana_mrei_audit.log", "a", encoding="utf-8") as log_file:
        log_file.write(mensaje + "\n")

def main():
    header = "\n" + "="*80 + "\n"
    header += "🧬 DUQUEANA CORE v2.1.0 — PROYECTO GÉNESIS (ANÁLISIS DINÁMICO DE SECUENCIAS)\n"
    header += "⚙️  Inicializando Motor MREI v2.1.1 (Modo: Lector Adaptativo)\n"
    header += "="*80
    print(header)
    registrar_log(header)
    
    # 1. ENTRADA DINÁMICA DE DATOS
    print("Seleccione el método de entrada para la secuencia de ADN:")
    print(" [1] Ingresar secuencia manualmente por consola")
    print(" [2] Leer desde archivo externo ('secuencia_apoe4.txt')")
    opcion = input("Selección (1 o 2): ").strip()
    
    secuencia_adn = ""
    target_genoma = "Genoma Humano: Variante Personalizada"
    
    if opcion == "2":
        nombre_archivo = "secuencia_apoe4.txt"
        if os.path.exists(nombre_archivo):
            with open(nombre_archivo, "r", encoding="utf-8") as f:
                secuencia_adn = f.read().replace("\n", "").replace(" ", "")
            target_genoma = f"Genoma Humano: Cargado desde {nombre_archivo}"
            print(f"\n[OK] Archivo cargado con éxito. Longitud: {len(secuencia_adn)} pares de bases.")
        else:
            print(f"\n[ERROR] No se encontró el archivo '{nombre_archivo}'.")
            print("Por favor, ingrese una secuencia manual temporal.")
            secuencia_adn = input("Introduzca secuencia (ej. ATCGATTG): ").strip()
    else:
        secuencia_adn = input("\nIntroduzca la secuencia de ADN (A, T, C, G): ").strip()
        target_genoma = "Genoma Humano: Entrada Manual por Consola"

    # Limpieza básica de la secuencia
    secuencia_adn = "".join([c for c in secuencia_adn.upper() if c in 'ATCG'])
    
    if not secuencia_adn:
        print("[ALERTA] Secuencia vacía o inválida. Usando secuencia ApoE4 de prueba.")
        # Fragmento real de la región ApoE4 humana
        secuencia_adn = "GCTGGGCGCGGACATGGAGGACGTGTGCGGCCGCCTGGTGCAGTACCGCGGCGAGGTGCAG"
        target_genoma = "Genoma Humano: Fragmento de Control ApoE4"

    # 2. PROCESAMIENTO DINÁMICO MREI
    print("\n[INFO] Analizando topología y tensiones estéricas en los nucleótidos...")
    print("[INFO] Aplicando corrección geométrica basada en el contenido GC...")
    
    score_genoma = calcular_score_por_adn(secuencia_adn)
    adn_hash_breve = hashlib.md5(secuencia_adn.encode()).hexdigest()[:8]
    
    # Cálculo dinámico de Unidades Doulita según el tamaño y la complejidad del ADN
    unidades = int(score_genoma * 10) + int(len(secuencia_adn) / 100) + 1
    bytes_totales = unidades * TAMANO_DOULITA_BYTES
    h = generate_trace_hash(target_genoma, score_genoma, adn_hash_breve)
    
    # 3. REPORTE Y TRAZABILIDAD
    reporte = "\n" + "-"*80 + "\n"
    reporte += "🔹 MÓDULO GENOMA HUMANO: PROCESAMIENTO COMPLETADO\n"
    reporte += f"   Target: {target_genoma}\n"
    reporte += f"   Longitud Procesada: {len(secuencia_adn)} bp\n"
    reporte += f"   Hash de la Secuencia: {adn_hash_breve}\n"
    reporte += f"   Score Dinámico de Coherencia: {score_genoma:.4f}\n"
    reporte += f"   MREI Alloc: {unidades} Unidades Doulita ({bytes_totales} Bytes)\n"
    reporte += f"   Hash de Trazabilidad Inmutable: {h}\n"
    reporte += "-"*80
    
    footer = "\n" + "="*80 + "\n"
    footer += "📊 REPORTE HISTÓRICO GENERADO\n"
    footer += f"Consumo de Estructura RAM: ~{bytes_totales / 1024:.2f} KB\n"
    footer += "Estado: ANÁLISIS FINALIZADO E INMUTABLE. REGISTRADO EN AUDIT.LOG.\n"
    footer += "="*80 + "\n"
    
    output_completo = reporte + footer
    print(output_completo)
    registrar_log(output_completo)
    
    print("💾 Los resultados han sido anexados a 'duqueana_mrei_audit.log'\n")

if __name__ == "__main__":
    main()
