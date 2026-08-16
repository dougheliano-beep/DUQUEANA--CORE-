// audit_test.js
// Pruebas de auditoría para Duqueana Core v2.1.0
import { MREIEngine, TIERS } from './Index.js';

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (error) {
    console.log(` ${name}: ${error.message}`);
    failed++;
  }
}

console.log('🔬 Running audit tests for Duqueana Core v2.1.0\n');

// Test 1: Tiers existen
test('TIERS object is frozen and contains 3 tiers', () => {
  if (!TIERS.community || !TIERS.pro || !TIERS.enterprise) {
    throw new Error('Missing tiers');
  }
  if (Object.isFrozen(TIERS) === false) {
    throw new Error('TIERS not frozen');
  }
});

// Test 2: Community tier funciona sin licencia
test('Community tier activates without license', () => {
  const engine = new MREIEngine('community');
  engine.activate();
  if (!engine.activated) {
    throw new Error('Community activation failed');
  }
});

// Test 3: Pro tier requiere validador
test('Pro tier requires license validator', () => {
  try {
    new MREIEngine('pro', { licenseKey: 'MREI-TEST' });
    throw new Error('Should require validator');
  } catch (e) {
    if (!e.message.includes('LICENSE_VALIDATOR_REQUIRED')) {
      throw e;
    }
  }
});

// Test 4: Pro tier con validador funciona
test('Pro tier works with valid validator', () => {
  const validator = (key) => key.includes('TEST');
  const engine = new MREIEngine('pro', { 
    licenseKey: 'MREI-TEST-KEY', 
    licenseValidator: validator 
  });
  engine.activate();
  if (!engine.activated) {
    throw new Error('Pro activation failed');
  }
});

// Test 5: Métricas están capadas
test('Public metrics show capped values', () => {
  const validator = (key) => true;
  const engine = new MREIEngine('pro', { 
    licenseKey: 'MREI-TEST', 
    licenseValidator: validator 
  });
  engine.activate();
  const metrics = engine.getPublicMetrics();
  if (metrics.savingsPercent !== 65) {
    throw new Error(`Expected 65%, got ${metrics.savingsPercent}%`);
  }
});

// Test 6: Load y process funcionan
test('Load and process data correctly', () => {
  const validator = (key) => true;
  const engine = new MREIEngine('community', { licenseValidator: validator });
  engine.activate();
  const records = [{id: 'test1', value: 100}, {id: 'test2', value: 200}];
  engine.load(records);
  const result = engine.process(10);
  if (result.recordsProcessed !== 2) {
    throw new Error('Processing failed');
  }
});

// Test 7: Anti-brute-force funciona
test('Anti-brute-force blocks after 5 attempts', () => {
  const validator = (key) => false; // Siempre inválido
  for (let i = 0; i < 5; i++) {
    try {
      new MREIEngine('pro', { 
        licenseKey: 'INVALID', 
        licenseValidator: validator 
      });
    } catch (e) {
      if (e.message.includes('LICENSE_LOCKED')) {
        console.log('✅ Anti-brute-force triggered at attempt ' + (i+1));
        return;
      }
    }
  }
  throw new Error('Brute-force protection not working');
});

// Test 8: Límite de records funciona
test('Record limit enforcement', () => {
  const engine = new MREIEngine('community');
  engine.activate();
  try {
    const tooManyRecords = Array(1001).fill({id: 'test', value: 1});
    engine.load(tooManyRecords);
    throw new Error('Should have thrown RECORD_LIMIT_EXCEEDED');
  } catch (e) {
    if (!e.message.includes('RECORD_LIMIT_EXCEEDED')) {
      throw e;
    }
  }
});

console.log(`\n${'='.repeat(50)}`);
console.log(`Audit Results: ${passed} passed, ${failed} failed`);
console.log(`${'='.repeat(50)}`);

if (failed > 0) {
  process.exit(1);
}
