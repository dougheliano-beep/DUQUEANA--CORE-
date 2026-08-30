#!/usr/bin/env python3
"""
Doulita Token Compressor - Research Preview Demo
Instituto Doughel de Investigación Digital | Agosto 2026

⚠️ AVISO: Este script aplica un FACTOR FIJO DE SIMULACIÓN (98.5%).
NO ejecuta el algoritmo propietario Doulita/MREI ni realiza reconstrucción semántica.
Es una demostración reproducible del flujo y cálculo de reducción.
"""
import sys
from datetime import datetime, timedelta

class DoulitaLicenseManager:
    def __init__(self, license_key=None, trial_days=7):
        self.license_key = license_key
        self.trial_days = trial_days
        self.install_file = ".doulita_install_date"

    def _get_install_date(self):
        try:
            with open(self.install_file, 'r', encoding='utf-8') as f:
                return datetime.fromisoformat(f.read().strip())
        except FileNotFoundError:
            now = datetime.now()
            with open(self.install_file, 'w', encoding='utf-8') as f:
                f.write(now.isoformat())
            return now

    def check_access(self):
        if self.license_key and self._validate_license(self.license_key):
            return True, "✅ Licencia válida: acceso completo"
        
        install_date = self._get_install_date()
        expiry_date = install_date + timedelta(days=self.trial_days)
        days_remaining = (expiry_date - datetime.now()).days
        
        if datetime.now() > expiry_date:
            return False, f"""
❌ Período de prueba agotado.
📅 Instalado: {install_date.strftime('%Y-%m-%d')}
📅 Expiró: {expiry_date.strftime('%Y-%m-%d')}

🔓 Para acceso continuo o revisión técnica:
   • Colaboración académica: institute@doughel.org
   • Integración empresarial: institute@doughel.org
   • Revisión bajo NDA: institute@doughel.org
🌐 https://doughelinst-bygtwdbf.manus.space
"""
        return True, f"✅ Trial activo (Research Preview) · Quedan {days_remaining} día(s)"

    def _validate_license(self, key):
        valid_prefixes = ["DOUGHEL-PRO-", "DOUGHEL-ENT-", "DOUGHEL-RESEARCH-"]
        return any(key.startswith(p) for p in valid_prefixes)


class DoulitaDemoSimulator:
    def __init__(self, license_key=None):
        self.license = DoulitaLicenseManager(license_key)
        self.reduction_factor = 0.985
        self.token_ratio = 4

    def generate_logs(self, n=1000):
        logs = []
        base = datetime(2026, 8, 30, 10, 0, 0)
        for i in range(n):
            if i % 10 == 0:
                t, m = "ERROR", f"Timeout /api/orders - ID:{i}"
            elif i % 5 == 0:
                t, m = "WARN", f"High latency - {100+i}ms"
            else:
                t, m = "INFO", f"GET /api/users 200 {40+(i%10)}ms - ID:{i}"
            ts = base.replace(second=i%60, minute=(i//60)%60)
            logs.append(f"[{t}] {ts.strftime('%Y-%m-%d %H:%M:%S')} {m}")
        return "\n".join(logs)

    def estimate_tokens(self, text):
        return len(text) // self.token_ratio

    def simulate_compression(self, text):
        orig_chars = len(text)
        orig_tokens = self.estimate_tokens(text)
        comp_tokens = int(orig_tokens * (1 - self.reduction_factor))
        reduction = ((orig_tokens - comp_tokens) / orig_tokens) * 100
        return {
            "chars": orig_chars,
            "orig_tokens": orig_tokens,
            "comp_tokens": comp_tokens,
            "reduction_pct": round(reduction, 2),
            "ratio": f"1:{int(orig_tokens / max(comp_tokens, 1))}",
            "note": "SIMULACIÓN con factor fijo (98.5%). No ejecuta algoritmo Doulita propietario."
        }

    def run(self, n=1000):
        access_ok, msg = self.license.check_access()
        print(msg)
        if not access_ok:
            return False
        
        print("\n" + "="*70)
        print(" DOULITA TOKEN COMPRESSOR - RESEARCH PREVIEW DEMO")
        print(" Instituto Doughel de Investigación Digital")
        print(" DOI: 10.5281/zenodo.22168535")
        print("="*70 + "\n")
        
        print("[1] Generando datos de prueba...")
        data = self.generate_logs(n)
        print(f"    ✓ Registros: {n}")
        
        print("\n[2] Métricas originales (estimación)...")
        print(f"    ✓ Caracteres: {len(data):,}")
        print(f"    ✓ Tokens estimados: ~{self.estimate_tokens(data):,}")
        
        print("\n[3] Aplicando compresión geométrica (SIMULACIÓN)...")
        print(f"     Factor configurado: {self.reduction_factor*100}%")
        print(f"     No se ejecuta el compresor propietario Doulita")
        
        res = self.simulate_compression(data)
        
        print("\n[4] RESULTADOS:")
        print("-"*70)
        print(f"{'Indicador':<45} | {'Valor':>20}")
        print("-"*70)
        print(f"{'Registros':<45} | {n:>20,}")
        print(f"{'Caracteres de entrada':<45} | {res['chars']:>20,}")
        print(f"{'Tokens originales (est.)':<45} | {res['orig_tokens']:>20,}")
        print(f"{'Tokens comprimidos (sim)':<45} | {res['comp_tokens']:>20,}")
        print(f"{'Reducción configurada':<45} | {res['reduction_pct']:>19.1f}%")
        print(f"{'Ratio':<45} | {res['ratio']:>20}")
        print("-"*70)
        
        print("\n[5] DECLARACIÓN DE ALCANCE:")
        print("-"*70)
        print("✅ Ejecución terminada sin errores")
        print("️  RESULTADO SIMULADO: Factor fijo, no algoritmo final")
        print("️  No valida reconstrucción semántica ni preservación de contexto")
        print("📄 Ver matriz de validación completa: DOI 10.5281/zenodo.22168535")
        print("\n ¿Necesitas acceso continuo o revisión técnica?")
        print("   📧 institute@doughel.org")
        print("   🌐 doughelinst-bygtwdbf.manus.space")
        print("-"*70)
        return True


def main():
    license_key = None
    if "--license" in sys.argv:
        idx = sys.argv.index("--license")
        if idx + 1 < len(sys.argv):
            license_key = sys.argv[idx + 1]
    sim = DoulitaDemoSimulator(license_key=license_key)
    return 0 if sim.run(n=1000) else 1

if __name__ == "__main__":
    sys.exit(main())
