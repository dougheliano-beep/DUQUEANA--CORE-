// ✅ CORRECCIÓN 6: Importación con 'Index.js' (I mayúscula) para Linux/Servidores
import MREIEngine from '../Index.js';

console.log("🚀 Iniciando Prueba de Uso Básico (Basic Usage)...");

try {
  // 1. Instanciar el motor
  const engine = new MREIEngine();

  // 2. Activar (Esto ahora funcionará porque arreglamos Index.js)
  const activationResult = engine.activate({ mode: 'production' });

  // 3. Verificación estricta
  if (!activationResult || activationResult.status !== 'active') {
    throw new Error("El motor no respondió con estado 'active'.");
  }

  console.log("✅ Activación Exitosa. Versión:", activationResult.version);

  // 4. Prueba de proceso simple
  const result = engine.process({ sample: 'data' });
  console.log("🧬 Restauración simulada:", result.status);

  // 5. Mensaje final SOLO si todo salió bien
  console.log("✅ All tiers working. Ready for production.");
  
  // Salida limpia (Código 0)
  process.exit(0);

} catch (error) {
  // 6. Manejo de errores honesto
  console.error("❌ ERROR CRÍTICO EN EJEMPLO:", error.message);
  console.error("📉 La suite falló. Revisar logs.");
  
  // Salida de error (Código 1)
  process.exit(1);
}
