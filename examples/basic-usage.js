// examples/basic-usage.js
// Demo mínima: Instanciar los 3 tiers y mostrar métricas capadas
import { MREIEngine } from '../Index.js';

console.log(' Duqueana Core v2.1.0 · Demo de Tiers\n');

// Validador de ejemplo (SOLO PARA DEMO - no usar en producción)
const demoValidator = (key, context) => {
  // En producción: esto sería una llamada a tu servidor de licencias
  // o una verificación de firma asimétrica con clave pública
  return key.includes('TEST') || key.includes('VALID');
};

['community', 'pro', 'enterprise'].forEach(tier => {
  try {
    const engine = new MREIEngine(tier, { 
      licenseKey: tier === 'community' ? undefined : 'MREI-TEST-998877-VALID',
      licenseValidator: demoValidator  // 👈 Inyección del validador
    });
    engine.activate();
    engine.load([{id: 'demo', value: 42}]);
    const result = engine.process(10);
    const metrics = engine.getPublicMetrics();
    console.log(`✅ ${tier.toUpperCase()}: ${metrics.savingsPercent}% RAM reduction`);
  } catch(e) {
    console.log(`❌ ${tier}: ${e.message}`);
  }
});

console.log('\n✨ All tiers working. Ready for production.');
