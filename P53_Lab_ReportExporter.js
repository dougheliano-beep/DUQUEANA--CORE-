/**
 * Duqueana Core · P53 Lab Report Exporter (v1.0)
 * Author: Douglas Helvesio Urbina Duque (UNET)
 * DOI: 10.5281/zenodo.21988399
 * License: CC-BY-NC-ND 4.0
 * 
 * @description Genera hipótesis computacionales estructuradas para validación experimental en laboratorio
 * @usage Integrar con P53_Repair_Simulator.js
 */

export default class P53_LabReportExporter {
  constructor(config = {}) {
    this._cfg = {
      institution: config.institution || 'Universidad Nacional Experimental del Táchira (UNET)',
      doi: config.doi || '10.5281/zenodo.21988399',
      orcid: config.orcid || '0009-0005-1230-7549',
      version: config.version || 'v1.0'
    };
  }

  /**
   * Genera reporte completo listo para laboratorio
   */
  generate(mutId, strategyId, simResult) {
    const report = {
      metadata: {
        title: `Computational Hypothesis: ${strategyId} for TP53 ${mutId}`,
        generated_by: `Duqueana Core · MREI Engine ${this._cfg.version}`,
        timestamp: new Date().toISOString(),
        author_orcid: this._cfg.orcid,
        doi_reference: this._cfg.doi,
        institution: this._cfg.institution
      },
      hypothesis: {
        mutation: mutId,
        proposed_intervention: strategyId,
        predicted_stability_recovery: simResult.stability || 'N/A',
        predicted_functional_restoration: simResult.functional || false,
        mechanistic_rationale: this._getRationale(mutId, strategyId),
        confidence_level: 'computational (requires wet-lab validation)'
      },
      experimental_protocol: this._buildProtocol(mutId, strategyId),
      legal_disclaimer: {
        nature: 'Todas las predicciones son simulaciones in silico generadas por el motor MREI.',
        not_medical_advice: true,
        required_validations: [
          'Ensayo de unión a ADN (EMSA o SPR)',
          'Estabilidad térmica (DSF o nanoDSF)',
          'Ensayo de viabilidad celular con línea mutante isogénica',
          'Confirmación estructural (cristalografía o Cryo-EM si es viable)'
        ],
        regulatory_note: 'No constituye aval clínico. Sujeto a aprobación de comités de ética y entes regulatorios.'
      }
    };

    return report;
  }

  /**
   * Exporta a JSON estructurado (para pipelines bioinformáticos)
   */
  exportJSON(report, pretty = true) {
    return JSON.stringify(report, null, pretty ? 2 : 0);
  }

  /**
   * Exporta a Markdown (para compartir con PIs/laboratorios)
   */
  exportMarkdown(report) {
    return `# 🧪 Hipótesis Computacional para Validación Experimental
**Mutación:** \`${report.hypothesis.mutation}\`  
**Intervención Propuesta:** \`${report.hypothesis.proposed_intervention}\`  
**Generado por:** ${report.metadata.generated_by}  
**DOI de Referencia:** ${report.metadata.doi_reference}  
**Fecha:** ${new Date(report.metadata.timestamp).toLocaleDateString('es-ES')}

---

## 📊 Predicción MREI
- **Recuperación de Estabilidad:** ${report.hypothesis.predicted_stability_recovery}
- **Restauración Funcional Esperada:** ${report.hypothesis.predicted_functional_restoration ? '✅ Sí' : '❌ No'}
- **Nivel de Confianza:** ${report.hypothesis.confidence_level}

## 🔬 Protocolo Sugerido
${this._formatProtocol(report.experimental_protocol)}

## ⚖️ Nota Legal y Científica
${report.legal_disclaimer.nature}  
🔹 No es consejo médico ni prescripción.  
🔹 Requiere validación wet-lab independiente.  
🔹 Criterio de éxito: **>70% de restauración funcional en ≥2 ensayos ortogonales**.
`;
  }

  // ─── MÉTODOS INTERNOS ───
  _getRationale(mut, strat) {
    const map = {
      'R175H': 'Mutación estructural que desestabiliza el núcleo del DBD. Chaperones o estabilizadores geométricos pueden restaurar el plegamiento nativo.',
      'G245S': 'Similar a R175H. Pérdida de coordinación local. Compuestos con afinidad por la cavidad colapsada muestran potencial in silico.',
      'R248Q': 'Mutación de contacto directo con ADN. Restauradores de interfaz o péptidos miméticos pueden recuperar la orientación de unión.',
      'R273H': 'Hotspot de contacto. Alta predictibilidad de restauración con moléculas que optimizan la electrostática de la superficie DBD.',
      'R282W': 'Desestabilización severa. Requiere intervención de alta afinidad o edición génica para restauración funcional.'
    };
    return map[mut] || 'Análisis de compatibilidad geométrica MREI sugiere intervención viable.';
  }

  _buildProtocol(mut, strat) {
    return {
      primary_assays: [
        'Thermal Shift Assay (ΔTm ≥ 2°C vs. mutante no tratado)',
        'Electrophoretic Mobility Shift Assay (EMSA) con secuencia consenso p53',
        'Cell viability/proliferation en línea isogénica portadora de la mutación'
      ],
      controls: {
        positive: 'Wild-type p53 (recombinante o línea parental)',
        negative: 'Mutante sin tratamiento + vehículo',
        internal: 'Compuesto de referencia según literatura (ej. APR-246 para R175H)'
      },
      success_criteria: '>70% de recuperación funcional en ≥2 ensayos ortogonales',
      timeline_suggestion: '4-8 semanas para screening inicial, 3 meses para validación secundaria',
      safety_notes: 'Evaluar citotoxicidad off-target antes de escalado. Seguir guías ICH S9 para compuestos oncológicos experimentales.'
    };
  }

  _formatProtocol(protocol) {
    let md = '### 🔍 Ensayos Primarios\n';
    protocol.primary_assays.forEach(a => md += `- ${a}\n`);
    md += '\n### 🧪 Controles\n';
    md += `- **Positivo:** ${protocol.controls.positive}\n`;
    md += `- **Negativo:** ${protocol.controls.negative}\n`;
    md += `- **Referencia:** ${protocol.controls.internal}\n`;
    md += `\n### ✅ Criterios de Éxito\n${protocol.success_criteria}`;
    return md;
  }
}
