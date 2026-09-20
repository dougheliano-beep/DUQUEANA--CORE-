/**
 * Duqueana Core · MREI Engine v2.1.1
 * Public Open-Core interface. The protected computational core is not included.
 */

const VERSION = '2.1.1';

export const TIERS = Object.freeze({
  community: Object.freeze({ name: 'community', savingsPercent: 15, maxRecords: 1000 }),
  pro: Object.freeze({ name: 'pro', savingsPercent: 65, maxRecords: Infinity }),
  enterprise: Object.freeze({ name: 'enterprise', savingsPercent: 81, maxRecords: Infinity })
});

// License-attempt state is intentionally module-scoped so that repeated
// attempts made by new engine instances are still subject to the lockout.
const licenseState = new Map();

class ClockGuard {
  constructor() {
    this.initialTime = Date.now();
  }

  check() {
    if (Date.now() < this.initialTime) {
      throw new Error('SECURITY_ANOMALY: System clock manipulation detected.');
    }
  }
}

export class MREIEngine {
  /**
   * Supports both forms:
   *   new MREIEngine('community')
   *   new MREIEngine('pro', { licenseKey, licenseValidator })
   *   new MREIEngine({ tier: 'pro', licenseKey, licenseValidator })
   */
  constructor(tierOrConfig = 'community', options = {}) {
    const config = typeof tierOrConfig === 'string'
      ? { ...options, tier: tierOrConfig }
      : { ...tierOrConfig };

    this.tier = config.tier || 'community';
    if (!TIERS[this.tier]) {
      throw new Error(`INVALID_TIER: unsupported tier '${this.tier}'.`);
    }

    const tierDefaults = TIERS[this.tier];
    this.config = {
      maxReduction: config.maxReduction ?? tierDefaults.savingsPercent,
      maxRecords: config.maxRecords ?? tierDefaults.maxRecords
    };
    this.activated = false;
    this._buffer = null;
    this._failedAttempts = 0;
    this._lockUntil = null;
    this.clockGuard = new ClockGuard();
    this._metrics = { processed: 0, errors: 0, startTime: Date.now() };

    if (this.tier !== 'community') {
      if (typeof config.licenseValidator !== 'function') {
        throw new Error('LICENSE_VALIDATOR_REQUIRED: paid tiers require a license validator.');
      }
      this._validateLicense(config.licenseKey, config.licenseValidator);
    }
  }

  _stateFor(key) {
    const state = licenseState.get(key) || { failedAttempts: 0, lockUntil: null };
    licenseState.set(key, state);
    return state;
  }

  _registerFailedAttempt(key) {
    const state = this._stateFor(key);
    state.failedAttempts += 1;
    if (state.failedAttempts >= 5) {
      state.lockUntil = Date.now() + 15 * 60 * 1000;
    }
    this._failedAttempts = state.failedAttempts;
    this._lockUntil = state.lockUntil;
  }

  _resetAttempts(key) {
    licenseState.delete(key);
    this._failedAttempts = 0;
    this._lockUntil = null;
  }

  _validateLicense(key, licenseValidator) {
    const state = this._stateFor(key);
    this._failedAttempts = state.failedAttempts;
    this._lockUntil = state.lockUntil;

    if (state.lockUntil !== null && Date.now() < state.lockUntil) {
      throw new Error('LICENSE_LOCKED: Access temporarily blocked due to repeated invalid attempts.');
    }
    if (typeof key !== 'string' || (!key.startsWith('MREI-') && !key.startsWith('LIC-'))) {
      this._registerFailedAttempt(key);
      throw new Error(`INVALID_LICENSE: ${this.tier} requires a valid license prefix.`);
    }
    if (key.length < 12) {
      this._registerFailedAttempt(key);
      throw new Error('INVALID_LICENSE: malformed key length');
    }

    let isValid = false;
    try {
      isValid = licenseValidator(key, {
        tier: this.tier,
        product: 'duqueana-core',
        version: VERSION
      }) === true;
    } catch {
      isValid = false;
    }
    if (!isValid) {
      this._registerFailedAttempt(key);
      throw new Error('INVALID_LICENSE: external validation rejected the credential.');
    }
    this._resetAttempts(key);
    return true;
  }

  load(records) {
    if (!Array.isArray(records)) {
      throw new Error('INVALID_INPUT: records must be an array');
    }
    if (records.length > this.config.maxRecords) {
      throw new Error(`RECORD_LIMIT_EXCEEDED: max ${this.config.maxRecords} records`);
    }
    this._buffer = records.map((record, index) => ({
      id: record.id ?? index,
      value: record.value,
      meta: record.meta ?? {}
    }));
    return this;
  }

  process(iterations = 10) {
    if (!this.activated || !this._buffer) {
      throw new Error('NOT_READY: Load data before processing.');
    }
    this.clockGuard.check();
    const maxIters = Number.isFinite(this.config.maxRecords)
      ? this.config.maxRecords
      : 1000;
    const iters = Math.max(1, Math.min(Number(iterations) || 1, maxIters));
    this._metrics.processed += this._buffer.length;

    return {
      status: 'PROCESSED_VIA_RESERVED_CORE',
      recordsProcessed: this._buffer.length,
      iterationsConfigured: iters,
      tier: this.tier,
      reductionClaim: `${this.config.maxReduction}% (ver public benchmarks)`,
      note: 'Protected MREI core; this public interface exposes metadata only.',
      timestamp: Date.now()
    };
  }

  getPublicMetrics() {
    const elapsed = Date.now() - this._metrics.startTime;
    return {
      processedCount: this._metrics.processed,
      errorCount: this._metrics.errors,
      uptimeSeconds: Math.round(elapsed / 1000),
      savingsPercent: this.config.maxReduction,
      config: { maxReduction: this.config.maxReduction, maxRecords: this.config.maxRecords }
    };
  }

  getStats() {
    return {
      version: VERSION,
      tier: this.tier,
      activated: this.activated,
      security: {
        failedAttempts: this._failedAttempts,
        isBlocked: this._lockUntil !== null && Date.now() < this._lockUntil
      },
      performance: this.getPublicMetrics()
    };
  }
}

export { ClockGuard };
export default MREIEngine;
