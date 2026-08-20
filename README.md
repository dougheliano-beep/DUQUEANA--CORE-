# Duqueana Core · Framework Post-Clásico MREI

> **"La eficiencia radical no requiere infraestructura de élite. Requiere una nueva geometría de la información."**

[🌐 Demo Interactiva p53](https://ovq4vc2nsoh6o.space.minimax.io/) · [📄 Paper Zenodo](https://zenodo.org/records/21988399) · [📖 Wiki Técnica](https://github.com/dougheliano-beep/DUQUEANA--CORE-/wiki)

---

##  Visión
Duqueana Core es un entorno de ejecución post-clásico diseñado para romper las limitaciones de la computación clásica. Mediante el **MREI Engine** y unidades atómicas de memoria (**Doulitas** de 128 bytes), logra optimizaciones de RAM del **65–81%** y ejecución en **<50 ms**, sin dependencia de clusters, GPUs ni librerías externas.

##  Módulos Certificados (v1.0b)
| Módulo | Dominio | Función | Estado |
|--------|---------|---------|--------|
| `duq-memory` | `system::memory` | Gestor atómico de RAM (Doulitas) | ✅ Activo |
| `duq-femo` | `domain::biochemistry` | Simulación de cofactores metálicos (FeMo-CO) | ✅ Validado |
| `duq-p53` | `domain::oncology` | Screening de mutaciones hotspot TP53 | ✅ Publicado |
| `duq-p53-repair` | `domain::oncology` | Predicción de reparación funcional (COTI-2, APR-246, CRISPR) | ✅ Nuevo |

## ⚡ Eficiencia Radical
- 🔋 **RAM:** ~6 KB por simulación (vs. GBs en dinámica molecular clásica)
- ⏱️ **Tiempo:** <50 ms por ejecución de reparación
- 📉 **Reducción:** 99.9% menos recursos vs. métodos clásicos (GROMACS/AMBER)
- 🌍 **Portabilidad:** Ejecutable en hardware estándar, edge devices y entornos académicos limitados

## 🛡️ Modelo Open-Core & Protección de IP
- 🔓 **Interfaz Pública:** Stubs auditables, manifiestos de dirección, SDK abierto
- 🔒 **Núcleo Reservado:** MREI Engine v2.1.1 + lógica geométrica (binario firmado)
- 🧭 **Routing Direccional:** Sandbox estricto por dominio (`biochemistry`, `oncology`, `system`)
- 🔐 **Firmas Criptográficas:** SHA-256 + ORCID en cada módulo certificado

## 📚 Trazabilidad Académica
- 📄 **DOI:** [10.5281/zenodo.21988399](https://zenodo.org/records/21988399)
- 👤 **ORCID:** [0009-0005-1230-7549](https://orcid.org/0009-0005-1230-7549)
- 🏛️ **Afiliación:** Universidad Nacional Experimental de Guayana (UNEG), Venezuela
- 📜 **Licencia:** CC-BY-NC-ND 4.0 (núcleo) · Apache 2.0 (SDK público)

## 🧪 Uso Rápido
```bash
git clone https://github.com/dougheliano-beep/DUQUEANA--CORE-.git
cd DUQUEANA--CORE-
# Ejecutar simulación de reparación p53 (Node.js ≥ 16)
node -e "import('./modules/p53/P53_Repair_Simulator.js').then(m => {
  const sim = new m.default({ tier: 'pro' });
  console.log(sim.simulateRepair('R273H', 'COTI-2'));
});"
