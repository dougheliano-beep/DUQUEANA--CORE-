import MREIEngine from '../index.js';

console.log("🚀 Iniciando Prueba de Uso Básico (Basic Usage)...");

try {
  // 1. Creamos la instancia del motor
  const engine = new MREIEngine();

  // 2. Ejecutamos el método activate() que acabamos de arreglar
  const activationResult = engine.activate({ mode: 'production' });

  // 3. Verificamos que realmente se activó
  if (!activationResult || activationResult.status !== 'active') {
    throw new Error("El motor no respondió correctamente a activate().");
  }

  console.log("✅ Activación Exitosa. Estado:", activationResult.status);

  // 4. Mensaje final de éxito (Solo si todo salió bien)
  console.log("✅ All tiers working. Ready for production.");
  
  // Salimos con código 0 (Éxito total)
  process.exit(0);

} catch (error) {
  // 5. Si algo falla, lo reportamos honestamente
  console.error("❌ ERROR CRÍTICO EN EJEMPLO:", error.message);
  console.error("📉 La prueba falló. Revisar logs.");
  
  // Salimos con código 1 (Fallo detectado)
  process.exit(1);
}
