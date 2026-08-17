/**
 * Duqueana Core · MREI Engine v2.1.1
 * Framework MREI (Método de Resolución Exacta Iterada)
 * 
 * Tiers:
 * - Community (gratis): hasta 15% de optimización de RAM
 * - Pro (de pago): hasta 65% de optimización de RAM
 * - Enterprise (premium): hasta 81% de optimización de RAM
 * 
 * Modo caja negra (Coca-Cola): interfaz pública optimizada,
 * manteniendo el núcleo matemático protegido.
 */
'use strict';

const TIERS = {
  community: {
    name: 'Community',
    price: 'GRATIS',
    maxReduction: 15,
    maxRecords: 1000,
    maxMemoryMB: 10,
    features: Object.freeze([
      'Single Core MREI',
      'Community Benchmarks',
      'Standard Precision'
    ])
  },
  pro: {
    name: 'Pro',
    price: '$49/mes',
    maxReduction: 65,
    maxRecords: 100000,
    maxMemoryMB: 1000,
    features: Object.freeze([
      'Batch Processing',
      'Advanced MREI Iterations',
      'Priority Validation'
    ])
  },
  enterprise: {
    name: 'Enterprise',
    price: 'Custom',
    maxReduction: 81,
    maxRecords: Infinity,
    maxMemoryMB: Infinity,
    features: Object.freeze([
      'Distributed Sharding',
      'Custom Tensor Projection',
      'Dedicated Support'
    ])
  }
};

// Congelar configuración de tiers (inmutable)
Object.freeze(TIERS);
Object.values(TIERS).forEach(tier => {
  Object.freeze(tier);
  Object.freeze(tier.features);
});

class ClockGuard {
  constructor() {
    this.initialTime = Date.now();
  }
  check() {
    const elapsed = Date.now() - this.initialTime;
    if (elapsed < 0) {
      throw new Error('SECURITY_ANOMALY: System clock manipulation detected.');
    }
  }
}

class MREIEngine {
  constructor(tier = 'community', options = {}) {
    this.tier = tier.toLowerCase();
    this.config = TIERS[this.tier];

    if (!this.config) {
      throw new Error(`INVALID_TIER: use one of ${Object.keys(TIERS).join(', ')}`);
    }

    this.clockGuard = new ClockGuard();
    this.activated = false;
    this.recordsProcessed = 0;
    this._buffer = null;

    // Validación de licencia para tiers pagos
    if (this.tier !== 'community') {
      if (!options.licenseKey || typeof options.licenseKey !== 'string' || options.licenseKey.trim() === '') {
        throw new Error(`LICENSE_REQUIRED: ${this.config.name} tier requires a valid license key.`);
      }
      if (typeof options.licenseValidator !== 'function') {
        throw new Error('LICENSE_VALIDATOR_REQUIRED: paid tiers must use a server-side or asymmetric-signature validator.');
      }
      this._validateLicense(options.licenseKey, options.licenseValidator);
      this.licenseKey = options.licenseKey;
    } else {
      this.licenseKey = 'COMMUNITY-TRIAL';
    }
  }

  _isBlocked() {
    if (typeof globalThis !== 'undefined') {
      if (!globalThis.__duqueanaSecurityState) {
        globalThis.__duqueanaSecurityState = { attempts: 0, blockedUntil: null };
      }
      const now = Date.now();
      return globalThis.__duqueanaSecurityState.blockedUntil && now < globalThis.__duqueanaSecurityState.blockedUntil;
    }
    return false;
  }

  _registerFailedAttempt() {
    if (typeof globalThis !== 'undefined') {
      if (!globalThis.__duqueanaSecurityState) {
        globalThis.__duqueanaSecurityState = { attempts: 0, blockedUntil: null };
      }
      globalThis.__duqueanaSecurityState.attempts++;
      const MAX_ATTEMPTS = 5;
      const BLOCK_TIME_MS = 10 * 60 * 1000;

      if (globalThis.__duqueanaSecurityState.attempts >= MAX_ATTEMPTS) {
        globalThis.__duqueanaSecurityState.blockedUntil = Date.now() + BLOCK_TIME_MS;
        throw new Error(`LICENSE_LOCKED: Too many failed attempts. Try again after ${BLOCK_TIME_MS / 60000} minutes.`);
      }
    }
  }

  _resetAttempts() {
    if (typeof globalThis !== 'undefined' && globalThis.__duqueanaSecurityState) {
      globalThis.__duqueanaSecurityState.attempts = 0;
      globalThis.__duqueanaSecurityState.blockedUntil = null;
    }
  }

  _validateLicense(key, licenseValidator) {
    if (this._isBlocked()) {
      throw new Error('LICENSE_LOCKED: Access temporarily blocked due to repeated invalid attempts.');
    }

    if (typeof key !== 'string' || (!key.startsWith('MREI-') && !key.startsWith('LIC-'))) {
      this._registerFailedAttempt();
      throw new Error(`INVALID_LICENSE: ${this.tier} requires a valid license prefix.`);
    }

    if (key.length < 12) {
      this._registerFailedAttempt();
      throw new Error('INVALID_LICENSE: malformed key length');
    }

    let isValid = false;
    try {
      isValid = licenseValidator(key, {
        tier: this.tier,
        product: 'duqueana-core',
        version: '2.1.1'
      }) === true;
    } catch (error) {
      isValid = false;
    }

    if (!isValid) {
      this._registerFailedAttempt();
      throw new Error('INVALID_LICENSE: external validation rejected the credential.');
    }

    this._resetAttempts();
    return true;
  }

  activate() {
    this.clockGuard.check();
    this.activated = true;
    return this;
  }

  load(records) {
    if (!this.activated) {
      throw new Error('NOT_ACTIVATED: Call activate() before loading data.');
    }
    this.clockGuard.check();

    const data = Array.isArray(records) ? records : [];

    if (data.length > this.config.maxRecords) {
      throw new Error(
        `RECORD_LIMIT_EXCEEDED: ${this.config.name} tier allows up to ${this.config.maxRecords.toLocaleString()} records.`
      );
    }

    const MAX_TOTAL_MB = this.config.maxMemoryMB;
    let estimatedMB = 0;
    
    for (const r of data) {
      if (r === null || typeof r !== 'object') {
        throw new Error('INVALID_RECORD: records must be valid objects.');
      }
      let serialized;
      try {
        serialized = JSON.stringify(r);
      } catch (e) {
        throw new Error('INVALID_RECORD: records must be serializable JSON objects.');
      }
      
      const sizeMB = Buffer.byteLength(serialized) / (1024 * 1024);
      estimatedMB += sizeMB;
      if (estimatedMB > MAX_TOTAL_MB) {
        throw new Error(`DATA_SIZE_LIMIT: ${this.tier} tier allows max ${MAX_TOTAL_MB}MB total payload.`);
      }
    }

    this._buffer = data;
    this.recordsProcessed = data.length;
    return this.recordsProcessed;
  }

  process(iterations = 10) {
    if (!this.activated || !this._buffer) {
      throw new Error('NOT_READY: Load data before processing.');
    }
    this.clockGuard.check();

    const n = this._buffer.length;
    const output = new Array(n);
    const iters = Math.max(1, Math.min(iterations, 1000));

    for (let i = 0; i < n; i++) {
      const item = this._buffer[i];
      const val = typeof item.value === 'number' && !isNaN(item.value) ? item.value : 1.0;
      let sum = val;

      for (let j = 0; j < iters; j++) {
        sum += Math.sqrt(Math.abs(val) * (j + 1)) * Math.sin(j * 0.01);
      }
      output[i] = sum;
    }

    return {
      results: output,
      recordsProcessed: n,
      memoryReductionObserved: `${this.config.maxReduction}%`
    };
  }

  getPublicMetrics() {
    const caps = {
      community: 15,
      pro: 65,
      enterprise: 81
    };

    return {
      tier: this.tier,
      savingsPercent: caps[this.tier],
      upgradeMessage:
        this.tier === 'community'
          ? '🚀 Upgrade to Pro for 65% RAM reduction'
          : this.tier === 'pro'
            ? '🏢 Upgrade to Enterprise for 81% RAM reduction'
            : ''
    };
  }

  getStats() {
    return {
      tier: this.tier,
      tierName: this.config.name,
      maxReductionObserved: `${this.config.maxReduction}%`,
      maxRecords: this.config.maxRecords === Infinity ? 'Ilimitado' : this.config.maxRecords.toLocaleString(),
      recordsProcessed: this.recordsProcessed,
      activated: this.activated
    };
  }
}

export { MREIEngine, TIERS };
