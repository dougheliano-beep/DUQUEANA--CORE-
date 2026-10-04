#!/usr/bin/env node
/**
 * Duqueana Core · MREI v2.1.1
 * Prueba de estrés y validación de límites de memoria para piloto controlado.
 * Autor: Lcdo. Douglas Helvesio Urbina Duque
 * 
 * Uso:
 *   node --expose-gc pilot_stress_test.mjs
 *   node --expose-gc pilot_stress_test.mjs --records=1000 --concurrency=2 --rounds=3
 *   node --expose-gc pilot_stress_test.mjs --quick
 */

import { createHash } from 'node:crypto';
import { mkdir, writeFile } from 'node:fs/promises';
import { performance } from 'node:perf_hooks';
import process from 'node:process';
import { pathToFileURL } from 'node:url';

const DEFAULTS = Object.freeze({
  module: './Index.js',
  tier: 'community',
  records: 1000,
  concurrency: 2,
  rounds: 3,
  iterations: 10,
  maxRssMb: 512,
  maxHeapMb: 256,
  maxInputMb: 10,
  timeoutMs: 120000,
  out: './pilot-stress-report.json',
  seed: 'duqueana-pilot-v2.1.1'
});

const HARD_LIMITS = Object.freeze({
  maxRecords: 100_000,
  maxConcurrency: 32,
  maxRounds: 1_000,
  maxIterations: 100_000,
  maxTimeoutMs: 3_600_000,
  maxInputMb: 512
});

function printHelp() {
  console.log(`
Duqueana Core · MREI v2.1.1 · Prueba de estrés

Uso:
  node --expose-gc pilot_stress_test.mjs [opciones]

Opciones:
  --module=./Index.js       Ruta al módulo MREI
  --tier=community          community | pro | enterprise
  --records=1000            Registros por trabajo
  --concurrency=2           Trabajos simultáneos por ronda
  --rounds=3                Número de rondas
  --iterations=10           Iteraciones solicitadas a process()
  --max-rss-mb=512          RSS máximo permitido
  --max-heap-mb=256         Heap máximo permitido
  --max-input-mb=10         Tamaño máximo de la carga
  --timeout-ms=120000       Tiempo máximo por trabajo
  --seed=texto              Semilla determinista
  --out=./report.json       Ruta del informe JSON
  --quick                   Modo rápido (records=100, rounds=1)
  --help                    Mostrar esta ayuda
`);
}

function parseArgs(argv) {
  const args = { ...DEFAULTS };
  for (const raw of argv) {
    if (raw === '--help' || raw === '-h') { printHelp(); process.exit(0); }
    if (raw === '--quick') {
      args.records = 100;
      args.rounds = 1;
      continue;
    }
    if (!raw.startsWith('--')) throw new Error(`Argumento no reconocido: ${raw}`);
    const separator = raw.indexOf('=');
    const key = separator === -1 ? raw.slice(2) : raw.slice(2, separator);
    const value = separator === -1 ? 'true' : raw.slice(separator + 1);
    const aliases = { 'max-rss-mb': 'maxRssMb', 'max-heap-mb': 'maxHeapMb', 'max-input-mb': 'maxInputMb', 'timeout-ms': 'timeoutMs' };
    const normalizedKey = aliases[key] || key;
    if (!(normalizedKey in args)) throw new Error(`Opción no reconocida: --${key}`);
    if (['tier', 'module', 'out', 'seed'].includes(normalizedKey)) {
      args[normalizedKey] = value;
    } else {
      const numberValue = Number(value);
      if (!Number.isFinite(numberValue)) throw new Error(`Valor numérico inválido: ${value}`);
      args[normalizedKey] = numberValue;
    }
  }
  validateArgs(args);
  return args;
}

function validateArgs(args) {
  const integerFields = ['records', 'concurrency', 'rounds', 'iterations', 'maxRssMb', 'maxHeapMb', 'maxInputMb', 'timeoutMs'];
  for (const field of integerFields) {
    if (!Number.isInteger(args[field]) || args[field] <= 0) throw new Error(`--${field} debe ser entero positivo.`);
  }
  if (!['community', 'pro', 'enterprise'].includes(args.tier)) throw new Error('--tier inválido.');
  if (args.records > HARD_LIMITS.maxRecords) throw new Error(`--records > ${HARD_LIMITS.maxRecords}`);
  if (args.concurrency > HARD_LIMITS.maxConcurrency) throw new Error(`--concurrency > ${HARD_LIMITS.maxConcurrency}`);
  if (args.rounds > HARD_LIMITS.maxRounds) throw new Error(`--rounds > ${HARD_LIMITS.maxRounds}`);
  if (args.iterations > HARD_LIMITS.maxIterations) throw new Error(`--iterations > ${HARD_LIMITS.maxIterations}`);
  if (args.timeoutMs > HARD_LIMITS.maxTimeoutMs) throw new Error(`--timeout-ms > ${HARD_LIMITS.maxTimeoutMs}`);
  if (args.maxInputMb > HARD_LIMITS.maxInputMb) throw new Error(`--max-input-mb > ${HARD_LIMITS.maxInputMb}`);
}

function bytesToMb(bytes) { return bytes / 1024 / 1024; }

function memorySnapshot() {
  const memory = process.memoryUsage();
  return {
    rssMb: Number(bytesToMb(memory.rss).toFixed(3)),
    heapUsedMb: Number(bytesToMb(memory.heapUsed).toFixed(3)),
    heapTotalMb: Number(bytesToMb(memory.heapTotal).toFixed(3))
  };
}

function sha256(value) {
  return createHash('sha256').update(JSON.stringify(value)).digest('hex');
}

function deterministicRecords(count, seed, round, worker) {
  return Array.from({ length: count }, (_, index) => ({
    id: `${seed}:r${round}:w${worker}:n${index}`,
    value: { sequence: index, signal: (index * 2654435761 + round * 97 + worker * 53) >>> 0 },
    meta: { source: 'pilot-stress-test', seed, round, worker }
  }));
}

function createLicenseOptions(tier) {
  if (tier === 'community') return {};
  return {
    licenseKey: `MREI-PILOT-${tier.toUpperCase()}-VALID`,
    licenseValidator: (key, context) => key.startsWith('MREI-PILOT-') && context?.tier === tier
  };
}

async function importEngine(modulePath) {
  const absoluteUrl = pathToFileURL(modulePath.startsWith('/') ? modulePath : `${process.cwd()}/${modulePath}`).href;
  const imported = await import(`${absoluteUrl}?pilot=${Date.now()}`);
  const Engine = imported.MREIEngine || imported.default;
  if (typeof Engine !== 'function') throw new Error('El módulo no exporta MREIEngine.');
  return Engine;
}

function withTimeout(promise, timeoutMs, label) {
  let timer;
  const timeout = new Promise((_, reject) => {
    timer = setTimeout(() => reject(new Error(`TIMEOUT: ${label} superó ${timeoutMs} ms.`)), timeoutMs);
  });
  return Promise.race([promise, timeout]).finally(() => clearTimeout(timer));
}

async function runWorker({ Engine, args, round, worker }) {
  const startedAt = performance.now();
  const before = memorySnapshot();
  const input = deterministicRecords(args.records, args.seed, round, worker);
  const inputHash = sha256(input);
  const serializedInputBytes = Buffer.byteLength(JSON.stringify(input), 'utf8');

  if (serializedInputBytes > args.maxInputMb * 1024 * 1024) {
    throw new Error(`INPUT_LIMIT: ${bytesToMb(serializedInputBytes).toFixed(3)} MB > ${args.maxInputMb} MB.`);
  }

  const engine = new Engine(args.tier, createLicenseOptions(args.tier));
  if (typeof engine.activate !== 'function') throw new Error('API_INCOMPATIBLE: activate() no existe.');
  engine.activate({ mode: 'pilot-stress-test' });
  if (typeof engine.load !== 'function' || typeof engine.process !== 'function') throw new Error('API_INCOMPATIBLE: load() y process() requeridos.');
  engine.load(input);
  const result = engine.process(args.iterations);
  const outputHash = sha256(result);
  const after = memorySnapshot();
  const elapsedMs = Number((performance.now() - startedAt).toFixed(3));

  return {
    round, worker, records: args.records,
    inputMb: Number(bytesToMb(serializedInputBytes).toFixed(3)),
    inputHash, outputHash,
    status: result?.status || 'unknown',
    recordsProcessed: result?.recordsProcessed ?? null,
    tier: result?.tier ?? args.tier,
    durationMs: elapsedMs,
    rssDeltaMb: Number((after.rssMb - before.rssMb).toFixed(3)),
    heapDeltaMb: Number((after.heapUsedMb - before.heapUsedMb).toFixed(3))
  };
}

async function runRound({ Engine, args, round }) {
  const startedAt = performance.now();
  const jobs = Array.from({ length: args.concurrency }, (_, index) =>
    withTimeout(runWorker({ Engine, args, round, worker: index + 1 }), args.timeoutMs, `ronda ${round}, worker ${index + 1}`)
  );
  const settled = await Promise.allSettled(jobs);
  const results = settled.filter(r => r.status === 'fulfilled').map(r => r.value);
  const errors = settled.filter(r => r.status === 'rejected').map(r => ({ round, error: r.reason?.message || String(r.reason) }));

  return {
    round,
    durationMs: Number((performance.now() - startedAt).toFixed(3)),
    results,
    errors
  };
}

function evaluateReport(report, args) {
  const allResults = report.rounds.flatMap(r => r.results);
  const allErrors = report.rounds.flatMap(r => r.errors);
  const rssPeakMb = Math.max(report.memoryStart.rssMb, ...allResults.map(r => r.rssDeltaMb + report.memoryStart.rssMb));
  const heapPeakMb = Math.max(report.memoryStart.heapUsedMb, ...allResults.map(r => r.heapDeltaMb + report.memoryStart.heapUsedMb));
  const uniqueInputHashes = new Set(allResults.map(r => r.inputHash));
  const successfulRecords = allResults.reduce((t, r) => t + (r.recordsProcessed || 0), 0);

  const checks = {
    noWorkerErrors: allErrors.length === 0,
    allWorkersProcessedExpectedRecords: allResults.every(r => r.recordsProcessed === args.records),
    rssWithinLimit: rssPeakMb <= args.maxRssMb,
    heapWithinLimit: heapPeakMb <= args.maxHeapMb,
    inputWithinLimit: allResults.every(r => r.inputMb <= args.maxInputMb),
    expectedWorkerCount: allResults.length === args.rounds * args.concurrency,
    deterministicInputGeneration: uniqueInputHashes.size === allResults.length,
    hasResults: allResults.length > 0
  };

  const passed = Object.values(checks).every(Boolean);
  report.summary = {
    passed,
    checks,
    workersExpected: args.rounds * args.concurrency,
    workersCompleted: allResults.length,
    errors: allErrors.length,
    totalRecordsProcessed: successfulRecords,
    rssPeakMb: Number(rssPeakMb.toFixed(3)),
    heapPeakMb: Number(heapPeakMb.toFixed(3)),
    recommendation: passed
      ? 'APTO PARA EL SIGUIENTE ESCALÓN DEL PILOTO. Estabilidad y determinismo validados.'
      : 'NO APTO: revisar errores o límites antes de aumentar la carga.'
  };
  return report;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const Engine = await importEngine(args.module);
  const report = {
    schemaVersion: '1.0.0',
    generatedAt: new Date().toISOString(),
    node: process.version,
    platform: process.platform,
    arch: process.arch,
    gcExposed: typeof global.gc === 'function',
    module: args.module,
    tier: args.tier,
    configuration: args,
    memoryStart: memorySnapshot(),
    rounds: []
  };

  console.log(`🚀 MREI v2.1.1 · Inicio de prueba de estrés (Tier: ${args.tier})`);
  console.log(JSON.stringify({ tier: args.tier, records: args.records, concurrency: args.concurrency, rounds: args.rounds, maxRssMb: args.maxRssMb, maxHeapMb: args.maxHeapMb }, null, 2));

  for (let round = 1; round <= args.rounds; round += 1) {
    if (typeof global.gc === 'function') global.gc();
    const roundReport = await runRound({ Engine, args, round });
    report.rounds.push(roundReport);
    console.log(`✅ Ronda ${round}/${args.rounds}: ${roundReport.results.length} éxitos, ${roundReport.errors.length} errores, ${roundReport.durationMs} ms`);
  }

  evaluateReport(report, args);
  report.memoryEnd = memorySnapshot();
  await mkdir(new URL('.', pathToFileURL(args.out)).pathname, { recursive: true }).catch(() => {});
  await writeFile(args.out, `${JSON.stringify(report, null, 2)}\n`, 'utf8');

  console.log('\n📊 Resumen:');
  console.log(JSON.stringify(report.summary, null, 2));
  console.log(`📁 Informe guardado en: ${args.out}`);
  process.exitCode = report.summary.passed ? 0 : 1;
}

main().catch(error => {
  console.error(`❌ ERROR FATAL: ${error.stack || error}`);
  process.exitCode = 1;
});
