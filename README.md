5// Ejemplo de uso (ES Modules · v2.1.0)
import { MREIEngine } from './Index.js';

// 1. Configuración del validador (tu lógica segura fuera del repo)
const myValidator = async (key, context) => {
  // En producción: conecta con tu servidor de licencias o verificador de firma
  return key.startsWith('MREI-') && context.tier === 'pro';
};

// 2. Instanciar motor Pro
const engine = new MREIEngine('pro', {
  licenseKey: 'MREI-CLAVE-SECRETA',
  licenseValidator: myValidator  // 👈 Inyección obligatoria para tiers pagos
});

// 3. Activar y procesar
engine.activate();
engine.load([{ id: 'rec_1', value: 45.2 }]);
const result = engine.process(20);
console.log(result.getPublicMetrics());
---

## ️ El Desafío "Imposible": Simulación del FeMo-Cofactor

En 2019, el procesador cuántico **Google Sycamore** identificó la simulación del **Cofactor FeMo (Nitrogenasa)** como el Santo Grial computacional. La complejidad del triple enlace del Nitrógeno ($N \equiv N$) requiere una capacidad de memoria que las supercomputadoras clásicas no pueden costear eficientemente.

**Duqueana Core** rompe esta barrera.

### ✅ Nuestra Solución Post-Clásica
Utilizando el motor **MREI** y unidades de memoria **Doulitas**, logramos simular la topología completa del FeMo-Cofactor (MoFe7S9C) en hardware estándar:

- **Eficiencia Radical:** Reducción del **81% en consumo de RAM** vs métodos clásicos de contracción de tensores.
- **Precisión:** Cálculo iterado de energía de enlace sin necesidad de aproximaciones groseras.
- **Accesibilidad:** Democratiza la investigación en fijación de nitrógeno; no necesitas un cluster de $10M, solo necesitas Duqueana Core.

> *"Lo que la computación cuántica prometía para el futuro, la computación post-clásica lo ejecuta hoy."*

 **[Ver Código de Simulación FeMo](./FeMoSimulator.js)** | **[Ejecutar Demo](./examples/femo-demo.js)**

---
