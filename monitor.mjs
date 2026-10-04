#!/usr/bin/env node
/**
 * Duqueana Core · MREI v2.1.1 · Monitor de Producción en Tiempo Real
 * Autor: Lcdo. Douglas Helvesio Urbina Duque
 * 
 * Estrategia: Monitorización continua con alertas tempranas de umbral.
 * Uso:
 *   node --expose-gc monitor.mjs --duration=30 --threshold-mb=64
 */

import { writeFile } from 'node:fs/promises';
import { performance } from 'node:perf_hooks';
import process from 'node:process';
import { pathToFileURL } from 'node:url';

const DEFAULTS = Object.freeze({
  module: './Index.js',
  duration: 30,
  interval: 1000,
  thresholdMb: 64,
  thresholdLatency: 200,
  out: './production-monitor-log.json'
});

const CRITICAL_LIMITS = Object.freeze({
  maxMemoryMb: 128,
  maxLatencyMs: 1000
});

function parseArgs(argv) {
  const args = { ...DEFAULTS };
  for (const raw of argv) {
    if (raw.startsWith('--')) {
      const [key, val] = raw.slice(2).split('=');
      if (['duration', 'interval', 'thresholdMb', 'thresholdLatency'].includes(key)) {
        args[key] = Number(val);
      } else if (key === 'out') {
        args.out = val;
      }
    }
  }
  return args;
}

async function importEngine(modulePath) {
  const absoluteUrl = pathToFileURL(
    modulePath.startsWith('/') ? modulePath : `${process.cwd()}/${modulePath}`
  ).href;
  const imported = await import(`${absoluteUrl}?monitor=${Date.now()}`);
  const Engine = imported.MREIEngine || imported.default;
  if (typeof Engine !== 'function') {
    throw new Error('El módulo no exporta MREIEngine.');
  }
  return Engine;
}

function getMemory() {
  const m = process.memoryUsage();
  return {
    rss: Math.round(m.rss / 1024 / 1024),
    heap: Math.round(m.heapUsed / 1024 / 1024)
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const Engine = await importEngine(args.module);

  const engine = new Engine('enterprise', {
    licenseKey: 'MREI-MONITOR-VALID',
    licenseValidator: (k, ctx) => k.startsWith('MREI-') && ctx?.tier === 'enterprise'
  });
  engine.activate({ mode: 'production-monitor' });

  const logs = [];
  let secondsElapsed = 0;
  let alertCount = 0;

  console.clear();
  console.log(`📡 DUQUEANA CORE · MONITOR DE PRODUCCIÓN v2.1.1`);
  console.log(`⏱️  Duración: ${args.duration}s | 🧠 Umbral RAM: ${args.thresholdMb}MB | ⚡ Latencia Máx: ${args.thresholdLatency}ms\n`);

  const timer = setInterval(async () => {
    secondsElapsed++;
    const start = performance.now();

    // Carga simulada de producción
    engine.load(Array(500).fill({ id: `chk-${secondsElapsed}`, value: 1 }));
    const res = engine.process(10);

    const latency = Math.round(performance.now() - start);
    const mem = getMemory();

    // Lógica de alertas
    let status = '🟢 OK';
    let alertMsg = '';
    if (mem.rss > args.thresholdMb) {
      status = '🟡 MEMORY WARNING';
      alertMsg = `(RSS: ${mem.rss}MB > ${args.thresholdMb}MB)`;
      alertCount++;
    }
    if (latency > args.thresholdLatency) {
      status = '🟠 LATENCY WARNING';
      alertMsg = `(Lat: ${latency}ms > ${args.thresholdLatency}ms)`;
      alertCount++;
    }
    if (mem.rss > CRITICAL_LIMITS.maxMemoryMb || latency > CRITICAL_LIMITS.maxLatencyMs) {
      status = '🔴 CRITICAL ALERT';
      alertMsg = 'LÍMITES CRÍTICOS SUPERADOS';
      alertCount++;
    }

    const entry = {
      timestamp: new Date().toISOString(),
      uptime: secondsElapsed,
      status,
      alert: alertMsg,
      metrics: {
        rssMb: mem.rss,
        heapMb: mem.heap,
        latencyMs: latency,
        recordsProcessed: res.recordsProcessed
      }
    };
    logs.push(entry);

    console.log(`[+${secondsElapsed}s] ${status} | RAM: ${mem.rss}MB | Heap: ${mem.heap}MB | Lat: ${latency}ms ${alertMsg}`);

    if (typeof global.gc === 'function') global.gc();

    if (secondsElapsed >= args.duration) {
      clearInterval(timer);

      const summary = {
        status: 'COMPLETED',
        totalChecks: logs.length,
        alerts: alertCount,
        avgLatency: Math.round(logs.reduce((acc, l) => acc + l.metrics.latencyMs, 0) / logs.length),
        peakMemory: Math.max(...logs.map(l => l.metrics.rssMb)),
        recommendation: alertCount === 0
          ? 'APTO PARA PRODUCCIÓN: Estabilidad absoluta demostrada.'
          : 'REVISAR: Se detectaron picos de recursos.'
      };

      console.log(`\n\n📊 REPORTE FINAL:`);
      console.log(JSON.stringify(summary, null, 2));

      const report = {
        schema: 'duqueana-monitor-v1',
        engineVersion: '2.1.1',
        summary,
        logs
      };

      try {
        await writeFile(args.out, JSON.stringify(report, null, 2));
        console.log(`✅ Log guardado en ${args.out}`);
        process.exit(0);
      } catch (e) {
        console.error('Error guardando log:', e);
        process.exit(1);
      }
    }
  }, args.interval);
}

main().catch(e => { console.error(`❌ ERROR FATAL: ${e.message}`); process.exit(1); });
