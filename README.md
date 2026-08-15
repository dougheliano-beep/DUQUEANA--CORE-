# ⚡ Duqueana Core (MREI Engine)

**High-performance post-classical computational runtime. Reduce RAM consumption by 39% to 81%.**

[![License: Custom](https://img.shields.io/badge/License-Source%20Available-yellow.svg)](LICENSE)

## 🎯 What is Duqueana Core?

Duqueana Core is the flagship computational runtime developed under the **MREI (Método de Resolución Exacta Iterada)** framework by Prof. Dr. Douglas Helvesio Urbina Duque (UNEG). It dramatically reduces memory consumption while maintaining high execution precision for complex mathematical and structural workloads.

---

## 📊 Benchmarks & Tiers

| Tier | Target Payload | RAM Optimization | Max Records |
| --- | --- | --- | --- |
| **Community** | Free / Personal | **39%** | 1,000 |
| **Pro** | Professional / Batch | **65%** | 100,000 |
| **Enterprise** | Distributed / Scale | **81%** | Unlimited |

---

## 🚀 Quick Start

### Installation

```bash
npm install duqueano-core
```

### Basic Usage

```javascript
import { MREIEngine } from 'duqueano-core';

// 1. Initialize engine for Pro tier with a valid license key
const engine = new MREIEngine('pro', { licenseKey: 'LIC-PRO-998877' });

// 2. Activate security and clock guards
engine.activate();

// 3. Load structured records
engine.load([
  { id: 'rec_1', value: 45.2 },
  { id: 'rec_2', value: -12.8 }
]);

// 4. Process with MREI iterations
const result = engine.process(20);
console.log(result);
```

---

## 🛡️ Security & Hardening

- **Immutable Configuration:** Deep-frozen configuration objects preventing runtime tampering.

- **Anti-Brute Force:** Automatic 10-minute temporary lockout after 5 consecutive invalid license attempts.

- **Payload DoS Protection:** Memory limit checks per tier to prevent out-of-memory errors.

- **Black-Box Architecture:** Exposes optimized client metrics without revealing proprietary core algorithms.

---

## 📄 License

Maintained under CC-BY-NC-ND 4.0 / Source-Available terms. See [LICENSE](LICENSE) for details.
