"""DROS Add-On Demo Verification Suite — calls real INTEGRATION_HOOKs."""
import unittest, json, time, sys, pathlib, base64
if sys.platform == 'win32': sys.stdout.reconfigure(encoding='utf-8')

# Import paths — relative to this file, pointing to sibling package hooks
_PKGBASE = pathlib.Path(__file__).resolve().parent.parent / "DROS商品專案暫存"
def _import(mod, pkg):
    d = str(_PKGBASE / pkg / "INTEGRATION_HOOKS")
    if d not in sys.path: sys.path.insert(0, d)
    return __import__(mod)

ESPR = _import("espr_redactor_hook", "DROS-ESPR-DPP-Package")
FIN = _import("finrisk_monitor_hook", "DROS-FinRisk-Privacy-Package")
HIP = _import("hipaa_phi_shield_hook", "DROS-Health-HIPAA-Package")
from sanctions_checker import SanctionsChecker

class TestAddOnPackages(unittest.TestCase):
    """5 pillars validating all 3 commercial Add-On Packages with real hooks."""

    def test_01_espr_redaction(self):
        """Pillar 1: ESPR dot-path redaction loads from YAML."""
        r = ESPR.ESPRZeroKnowledgeRedactor()
        self.assertGreater(len(r.redact_rules), 0)
        bom = {"product_id":"P1","carbon_footprint_total":"12.4 kg",
               "bom":{"wafer_baking_temp":"1250C","component":"ok"}}
        res = r.redact_payload(bom)
        self.assertIn("REDACTED", str(res["bom"]["wafer_baking_temp"]))
        self.assertEqual(res["carbon_footprint_total"], "12.4 kg")
        self.assertEqual(bom["bom"]["wafer_baking_temp"], "1250C")

    def test_02_finrisk_pii_and_risk(self):
        """Pillar 2: FinRisk PII anonymization + threshold enforcement."""
        m = FIN.FinRiskPrivacyMonitor()
        tx = {"tx_id":"T1","amount_usd":500,"user":{"real_name":"John","ssn":"123-45"}}
        r1 = m.process_transaction(tx, 5, 0.1)
        self.assertEqual(r1["status"], "APPROVED")
        self.assertIn("ANONYMIZED", str(r1["payload"]["user"]["ssn"]))
        r2 = m.process_transaction(tx, 30, 0.1)
        self.assertEqual(r2["status"], "SUSPENDED_FOR_HITL")

    def test_03_sanctions(self):
        """Pillar 3: Sanctions screening blocks matched entities."""
        c = SanctionsChecker()
        self.assertGreater(c.get_entry_count(), 0)
        self.assertGreater(len(c.check_entity("Hassan Al-Mutairi")), 0)
        self.assertEqual(len(c.check_entity("John Smith")), 0)

    def test_04_hipaa_consent_and_break_glass(self):
        """Pillar 4: HIPAA consent JWT + break-glass override."""
        s = HIP.HIPAAPHIShield()
        ehr = {"resourceType":"Patient","patient":{"name":"Jane","ssn":"987-65"}}
        r1 = s.intercept_fhir_request(ehr, consent_token=None)
        self.assertEqual(r1["status"], "DROP_REQUEST_403")
        h = base64.urlsafe_b64encode(json.dumps({"alg":"HS256"}).encode()).rstrip(b"=").decode()
        exp = int(time.time()) + 3600
        p = base64.urlsafe_b64encode(json.dumps({"sub":"p1","exp":exp}).encode()).rstrip(b"=").decode()
        r2 = s.intercept_fhir_request(ehr, consent_token=f"{h}.{p}.d")
        self.assertEqual(r2["status"], "APPROVED")
        self.assertIn("REDACTED", str(r2["payload"]["patient"]["name"]))
        bg = s.intercept_fhir_request(ehr, consent_token=None, break_glass=True,
                                       break_glass_authoriser="Dr.H", break_glass_reason="ER")
        self.assertEqual(bg["status"], "APPROVED")
        acts = [x["action"] for x in s.get_audit_log()]
        self.assertIn("BREAK_GLASS_ACTIVATED", acts)

    def test_05_yaml_policy(self):
        """Pillar 5: All 3 packages load rules from YAML (not fallback)."""
        self.assertIn("POLICY", ESPR.ESPRZeroKnowledgeRedactor().replacement)
        self.assertIn("tx_frequency_3min", FIN.FinRiskPrivacyMonitor().risk_thresholds)
        self.assertGreater(len(HIP.HIPAAPHIShield().phi_rules), 4)

if __name__ == "__main__":
    print("="*60)
    print("DROS Add-On Demo — Verification Suite")
    print("  (testing real hooks from 3 commercial packages)")
    print("="*60)
    runner = unittest.TextTestRunner(verbosity=2)
    r = runner.run(unittest.TestLoader().loadTestsFromTestCase(TestAddOnPackages))
    if r.wasSuccessful(): print("\n✅ ALL 5 PILLARS PASSED — Real hooks verified.")
    else: sys.exit(1)
