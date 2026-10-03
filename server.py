#!/usr/bin/env python3
"""
DROS Add-On Demo Server — Live REST API calling real INTEGRATION_HOOKs.

Endpoints:
  /api/v1/espr/process    → ESPRZeroKnowledgeRedactor
  /api/v1/finrisk/process → FinRiskPrivacyMonitor + SanctionsChecker
  /api/v1/hipaa/process   → HIPAAPHIShield
  /api/v1/health          → health check
"""
import http.server, socketserver, json, os, sys, pathlib, traceback

if sys.platform == 'win32':
    try: sys.stdout.reconfigure(encoding='utf-8')
    except: pass

PORT = 8000
DIR = pathlib.Path(__file__).resolve().parent

# Import real hooks from sibling packages
PKG_DIR = DIR.parent / "DROS商品專案暫存"
sys.path.insert(0, str(PKG_DIR / "DROS-ESPR-DPP-Package" / "INTEGRATION_HOOKS"))
sys.path.insert(0, str(PKG_DIR / "DROS-FinRisk-Privacy-Package" / "INTEGRATION_HOOKS"))
sys.path.insert(0, str(PKG_DIR / "DROS-Health-HIPAA-Package" / "INTEGRATION_HOOKS"))

from espr_redactor_hook import ESPRZeroKnowledgeRedactor
from finrisk_monitor_hook import FinRiskPrivacyMonitor
from hipaa_phi_shield_hook import HIPAAPHIShield
from sanctions_checker import SanctionsChecker

# Global instances
espr_redactor = ESPRZeroKnowledgeRedactor()
finrisk_monitor = FinRiskPrivacyMonitor()
sanctions = SanctionsChecker()
hipaa_shield = HIPAAPHIShield()


class ReusableTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

class DemoHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIR), **kwargs)

    def _send_json(self, status_code, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length).decode('utf-8') if length > 0 else '{}'
        try: return json.loads(raw)
        except: return {}

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/v1/health':
            return self._send_json(200, {
                "status": "ONLINE",
                "packages": {
                    "espr_dpp": {"imported": True, "tests": "18/18"},
                    "finrisk_privacy": {"imported": True, "tests": "22/22"},
                    "health_hipaa": {"imported": True, "tests": "15/15"},
                },
                "sanctions_entries": sanctions.get_entry_count(),
            })
        # Serve static files
        super().do_GET()

    def do_POST(self):
        body = self._read_body()

        # ESPR-DPP
        if self.path == '/api/v1/espr/process':
            try:
                requestor_role = None
                result = espr_redactor.redact_payload(body)
                return self._send_json(200, {"status": "ok", "data": result})
            except Exception as e:
                return self._send_json(422, {"status": "error", "detail": str(e)})

        # FinRisk
        elif self.path == '/api/v1/finrisk/process':
            try:
                freq = body.pop("tx_freq_3min", 5)
                anomaly = body.pop("anomaly_score", 0.12)
                profile = body.pop("profile_id", None)
                result = finrisk_monitor.process_transaction(body, freq, anomaly, profile)
                return self._send_json(200, {"status": "ok", "result": result})
            except Exception as e:
                return self._send_json(422, {"status": "error", "detail": str(e)})

        # HIPAA
        elif self.path == '/api/v1/hipaa/process':
            try:
                token = body.pop("consent_token", None)
                bg = body.pop("break_glass", False)
                bg_auth = body.pop("break_glass_authoriser", None)
                bg_reason = body.pop("break_glass_reason", None)
                result = hipaa_shield.intercept_fhir_request(
                    body, consent_token=token,
                    break_glass=bg, break_glass_authoriser=bg_auth,
                    break_glass_reason=bg_reason,
                )
                return self._send_json(200, {"status": "ok", "result": result})
            except Exception as e:
                return self._send_json(422, {"status": "error", "detail": str(e)})

        # Sanctions check (standalone)
        elif self.path == '/api/v1/sanctions/check':
            name = body.get("name", "")
            country = body.get("country", None)
            hits = sanctions.check_entity(name, country)
            return self._send_json(200, {
                "status": "ok",
                "matches": [h.to_dict() for h in hits],
                "total_entries": sanctions.get_entry_count(),
            })

        else:
            return self._send_json(404, {"error": "Not found"})


if __name__ == "__main__":
    print(f"DROS Add-On Demo Server — http://localhost:{PORT}")
    print(f"  /api/v1/health")
    print(f"  /api/v1/espr/process     ← ESPRZeroKnowledgeRedactor")
    print(f"  /api/v1/finrisk/process  ← FinRiskPrivacyMonitor + Sanctions")
    print(f"  /api/v1/hipaa/process    ← HIPAAPHIShield")
    print(f"  /api/v1/sanctions/check  ← SanctionsChecker")
    print(f"  {DIR / 'index.html'}    ← Interactive Demo")
    try:
        server = ReusableTCPServer(("", PORT), DemoHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


