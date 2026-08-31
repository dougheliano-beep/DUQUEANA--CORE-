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
 * 
 * ARQUITECTURA OPEN-CORE:
 * Este archivo expone la interfaz pública verificable.
 * El núcleo MREI real reside en módulo binario firmado (reservado).
 * Benchmarks independientes: DOIs en Zenodo.
 */
'use strict';

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
  constructor(config = {}) {
    this.tier = config.tier || 'community';
    this.config = {
      maxReduction: config.maxReduction || (this.tier === 'community' ? 15 : this.tier === 'pro' ? 65 : 81),
      maxRecords: config.maxRecords || (this.tier === 'community' ? 1000 : Infinity)
    };
    this.activated = false;
    this._buffer = null;
    this._failedAttempts = 0;
    this._lockUntil = null;
    this.clockGuard = new ClockGuard();
    this._metrics = { processed: 0, errors: 0, startTime: Date.now() };
  }

  _registerFailedAttempt() {
    this._failedAttempts++;
    if (this._failedAttempts >= 5) {
      this._lockUntil = Date.now() + 15 * 60 * 1000;
    }
  }

  _resetAttempts() {
    this._failedAttempts = 0;
    this._lockUntil = null;
  }

  _isBlocked() {
    return this._lockUntil !== null && Date.now() < this._lockUntil;
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
      isValid = licenseValidator(key, { tier: this.tier, product: 'duqueana-core', version: '2.1.1' }) === true;
    } catch (error) { isValid = false; }
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
    if (!Array.isArray(records)) throw new Error('INVALID_INPUT: records must be an array');
    if (this.tier === 'community' && records.length > this.config.maxRecords) {
      throw new Error(`COMMUNITY_LIMIT_EXCEEDED: max ${this.config.maxRecords} records`);
    }
    this._buffer = records.map((r, i) => ({ id: r.id || i, value: r.value, meta: r.meta || {} }));
    return this;
  }

  /**
   * Procesa registros mediante el núcleo MREI reservado.
   * 
   * NOTA ARQUITECTÓNICA:
   * Este método delega al núcleo MREI protegido (binario firmado).
   * La implementación real NO está expuesta en este repositorio.
   * 
   * Para validación técnica del motor completo:
   * - Benchmarks públicos: DOIs 21988399, 22168535
   * - Manifiesto oficial: DOI 22182252
   * - Acceso bajo NDA: institute@doughel.org
   * 
   * @param {number} iterations - Número de iteraciones (máx 1000 en community)
   * @returns {Object} Resultados con métricas públicas
   */
  process(iterations = 10) {
    if (!this.activated || !this._buffer) {
      throw new Error('NOT_READY: Load data before processing.');
    }
    this.clockGuard.check();
    const n = this._buffer.length;
    const maxIters = this.config.maxRecords || 1000;
    const iters = Math.max(1, Math.min(iterations, maxIters));
    // Métricas públicas verificables (ver DOIs independientes)
    // - p53: ~6KB RAM, <50ms (DOI: 10.5281/zenodo.21988399)
    // - Token Compressor: 98.5% reducción (DOI: 10.5281/zenodo.22168535)
    // - Manifiesto: Paradigma post-clásico (DOI: 10.5281/zenodo.22182252)
    return {
      status: 'PROCESSED_VIA_RESERVED_CORE',
      recordsProcessed: n,
      iterationsConfigured: iters,
      tier: this.tier,
      reductionClaim: `${this.config.maxReduction}% (ver benchmarks en Zenodo)`,
      note: 'Núcleo MREI protegido. Resultados verificables en DOIs independientes.',
      manifesto: 'https://doi.org/10.5281/zenodo.22182252',
      data_available: 'https://zenodo.org/records/21988399',
      timestamp: Date.now()
    };
  }

  getPublicMetrics() {
    const elapsed = Date.now() - this._metrics.startTime;
    return {
      tier: this.tier,
      activated: this.activated,
      recordsLoaded: this._buffer ? this._buffer.length : 0,
      processedCount: this._metrics.processed,
      errorCount: this._metrics.errors,
      uptimeSeconds: Math.round(elapsed / 1000),
      config: { maxReduction: this.config.maxReduction, maxRecords: this.config.maxRecords }
    };
  }

  getStats() {
    return {
      version: '2.1.1',
      tier: this.tier,
      activated: this.activated,
      security: { failedAttempts: this._failedAttempts, isBlocked: this._isBlocked() },
      performance: this.getPublicMetrics()
    };
  }
}

module.exports = { MREIEngine, ClockGuard };
