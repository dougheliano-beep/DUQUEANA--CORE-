// Ejemplo de uso (ES Modules · v2.1.0)
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
