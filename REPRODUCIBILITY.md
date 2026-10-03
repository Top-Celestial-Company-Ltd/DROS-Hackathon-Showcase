# DROS Add-On Demo — Reproducibility Guide

> **100% reproducible**: runs on any Python 3.10+ with pytest. No external API keys, no GPU, no database.

## One-Command Verification

```bash
python test_verification_suite.py
```

### Expected output

```
============================================================
DROS Add-On Demo — Verification Suite
  (testing real hooks from 3 commercial packages)
============================================================
test_01_espr_redaction ................... ok
test_02_finrisk_pii_and_risk ............ ok
test_03_sanctions ....................... ok
test_04_hipaa_consent_and_break_glass ... ok
test_05_yaml_policy ..................... ok
--------------------------------------------------------------
Ran 5 tests in 0.02s

ALL 5 PILLARS PASSED — Real hooks verified.
```

## Per-Package Test Suites

```bash
cd ../DROS商品專案暫存
python -m pytest DROS-ESPR-DPP-Package/tests/ -v      # 18 tests
python -m pytest DROS-FinRisk-Privacy-Package/tests/   # 22 tests (2 suites)
python -m pytest DROS-Health-HIPAA-Package/tests/ -v   # 15 tests
```

Total: **63 automated assertions** across all 3 packages.

## Live REST API

```bash
python server.py
# Open http://localhost:8000/api/v1/health
# Try POST /api/v1/espr/process, /api/v1/finrisk/process, /api/v1/hipaa/process
```

## Verification Matrix

| Pillar | What | How to verify | Status |
|---|---|---|---|
| 1 | ESPR YAML dot-path redaction | `test_01` | ✅ |
| 2 | FinRisk PII + risk thresholds | `test_02` | ✅ |
| 3 | Sanctions screening | `test_03` | ✅ |
| 4 | HIPAA consent JWT + break-glass | `test_04` | ✅ |
| 5 | All packages YAML-driven | `test_05` | ✅ |

No mock objects. Every assertion runs against real `vajra_policy.yaml`-driven hooks.
