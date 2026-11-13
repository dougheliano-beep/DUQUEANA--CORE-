"""
Índice de Equilibrio Estructural (C) — Generador de gráficos.
Instituto Doughel · UNEG

Genera dos gráficos comparativos:
  1. Barras del Índice C (clásico vs. IED).
  2. Radar de eficiencia (Em, V, Q).

Uso:
    pip install matplotlib numpy
    python graficos.py
"""

import matplotlib.pyplot as plt
import numpy as np

# ==============================================================================
# DATOS (Entorno: 4 GB RAM, sin GPU dedicada)
# ==============================================================================

# Modelo Clásico (inviable en 4GB: usa swap severo)
em_clasico = 10.0
v_clasico = 5.0
q_clasico = 68.0

# Modelo IED (proyección basada en compresión DouSan del 75%)
em_ied = 85.0
v_ied = 85.0
q_ied = 68.0

# ==============================================================================
# CÁLCULO DEL ÍNDICE C
# ==============================================================================

def calcular_C(em, v, q):
    """Distancia euclidiana al cuadrado respecto al ideal (100, 100, 100)."""
    return (100 - em) ** 2 + (100 - v) ** 2 + (100 - q) ** 2

C_clasico = calcular_C(em_clasico, v_clasico, q_clasico)
C_ied = calcular_C(em_ied, v_ied, q_ied)
mejora = ((C_clasico - C_ied) / C_clasico) * 100

print("=" * 60)
print(" ÍNDICE DE EQUILIBRIO ESTRUCTURAL (C)")
print(" Entorno: 4 GB RAM (sin GPU dedicada)")
print("=" * 60)
print(f"  Modelo Clásico (inviable en 4GB): C = {C_clasico:,.2f}")
print(f"  Modelo IED (proyección DouSan):   C = {C_ied:,.2f}")
print(f"  Mejora en equilibrio:             {mejora:.1f}%")
print("=" * 60)

# ==============================================================================
# GRÁFICO 1: BARRAS DEL ÍNDICE C
# ==============================================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

barras = ax1.bar(
    ['Modelo Clásico\n(14B Q4 en 4GB)', 'Modelo IED\n(DouSan + MREI)'],
    [C_clasico, C_ied],
    color=['#d9534f', '#0055A4'],
    edgecolor='black',
)
ax1.set_ylabel('Índice de Desequilibrio (C) [Menor es mejor]', fontsize=11)
ax1.set_title('Reducción del Desequilibrio Estructural', fontweight='bold')
ax1.set_ylim(0, C_clasico * 1.15)

for barra in barras:
    yval = barra.get_height()
    ax1.text(
        barra.get_x() + barra.get_width() / 2,
        yval + C_clasico * 0.02,
        f'{int(yval):,}',
        ha='center', va='bottom', fontweight='bold',
    )
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# ==============================================================================
# GRÁFICO 2: RADAR DE EFICIENCIA (Em, V, Q)
# ==============================================================================

categorias = ['Eficiencia Mem. (Em)', 'Velocidad (V)', 'Calidad (Q)']
N = len(categorias)

valores_clasico = [em_clasico, v_clasico, q_clasico] + [em_clasico]
valores_ied = [em_ied, v_ied, q_ied] + [em_ied]

angulos = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist() + [0]

ax2 = plt.subplot(1, 2, 2, polar=True)
ax2.plot(angulos, valores_clasico, color='red', linewidth=2,
         linestyle='dashed', label='Clásico (inviable)')
ax2.fill(angulos, valores_clasico, color='red', alpha=0.1)
ax2.plot(angulos, valores_ied, color='#0055A4', linewidth=2,
         label='IED (proyección DouSan)')
ax2.fill(angulos, valores_ied, color='#0055A4', alpha=0.25)

ax2.set_theta_offset(np.pi / 2)
ax2.set_theta_direction(-1)
plt.xticks(angulos[:-1], categorias, fontsize=10)
ax2.set_ylim(0, 100)
ax2.set_title('Proximidad al Estado Óptimo (100, 100, 100)',
              fontweight='bold', pad=20)
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

plt.tight_layout()
plt.savefig('graficos_equilibrio_ied_4gb.png', dpi=300, bbox_inches='tight')
print("\n✅ Gráficos guardados como 'graficos_equilibrio_ied_4gb.png'")
plt.show()
