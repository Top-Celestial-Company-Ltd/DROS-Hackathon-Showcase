"""DROS-VEP-lite Hackathon Verification Suite (v2 — Real Hooks)"""
import unittest, json, time, sys, pathlib, base64
if sys.platform == 'win32': sys.stdout.reconfigure(encoding='utf-8')
_HB = pathlib.Path(__file__).resolve().parent.parent / "DROS商品專案暫存"
def _ih(pkg, mod):
    d = str(_HB / pkg / "INTEGRATION_HOOKS")
    if d not in sys.path: sys.path.insert(0, d)
    return __import__(mod)
ESPR = _ih("DROS-ESPR-DPP-Package", "espr_redactor_hook")
FIN = _ih("DROS-FinRisk-Privacy-Package", "finrisk_monitor_hook")
HIP = _ih("DROS-Health-HIPAA-Package", "hipaa_phi_shield_hook")
from sanctions_checker import SanctionsChecker

class TestDROSVEP(unittest.TestCase):
    def test_01_espr(self):
        r = ESPR.ESPRZeroKnowledgeRedactor()
        self.assertGreater(len(r.redact_rules), 0)
        b = {"pid":"P1","ct":"12.4","bom":{"wafer_baking_temp":"1250C","component":"ok"}}
        x = r.redact_payload(b)
        self.assertIn("REDACTED", x["bom"]["wafer_baking_temp"])
    def test_02_finrisk(self):
        m = FIN.FinRiskPrivacyMonitor()
        t = {"tx":"T1","amount_usd":500,"user":{"real_name":"J","ssn":"123"}}
        self.assertEqual(m.process_transaction(t,5,0.1)["status"], "APPROVED")
        self.assertIn("ANONYMIZED", m.process_transaction(t,5,0.1)["payload"]["user"]["ssn"])
    def test_03_sanctions(self):
        c = SanctionsChecker()
        self.assertGreater(c.get_entry_count(), 0)
        self.assertGreater(len(c.check_entity("Hassan Al-Mutairi")), 0)
        self.assertEqual(len(c.check_entity("John Smith")), 0)
    def test_04_hipaa(self):
        s = HIP.HIPAAPHIShield()
        e = {"resourceType":"P","patient":{"name":"J","ssn":"987"}}
        self.assertEqual(s.intercept_fhir_request(e,None)["status"], "DROP_REQUEST_403")
        h = base64.urlsafe_b64encode(json.dumps({"alg":"HS256"}).encode()).rstrip(b"=").decode()
        exp = int(time.time()) + 3600
        p = base64.urlsafe_b64encode(json.dumps({"sub":"p1","exp":exp}).encode()).rstrip(b"=").decode()
        self.assertEqual(s.intercept_fhir_request(e,f"{h}.{p}.d")["status"], "APPROVED")
        bg = s.intercept_fhir_request(e,None,break_glass=True,break_glass_authoriser="Dr",break_glass_reason="ER")
        self.assertEqual(bg["status"], "APPROVED")
        acts = [x["action"] for x in s.get_audit_log()]
        self.assertIn("BREAK_GLASS_ACTIVATED", acts)
    def test_05_yaml(self):
        self.assertIn("POLICY", ESPR.ESPRZeroKnowledgeRedactor().replacement)
        self.assertIn("tx_frequency_3min", FIN.FinRiskPrivacyMonitor().risk_thresholds)
        self.assertGreater(len(HIP.HIPAAPHIShield().phi_rules), 4)

if __name__ == "__main__":
    print("="*60)
    print("DROS-VEP Verification Suite (Real Hooks)")
    print(f"  ESPR: {ESPR.__file__}")
    print(f"  FIN:  {FIN.__file__}")
    print(f"  HIP:  {HIP.__file__}")
    print("="*60)
    u = unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(TestDROSVEP))
    if u.wasSuccessful(): print("\nALL 5 PILLARS PASSED")
    else: sys.exit(1)

