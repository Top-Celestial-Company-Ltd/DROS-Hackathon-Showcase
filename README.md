# DROS Add-On Demo Showcase

> **Live demonstration platform for 3 commercial DROS Add-On Packages:**
> ESPR-DPP (Carbon Passport), FinRisk-Privacy (Financial Risk & Privacy), Health-HIPAA (Medical PHI)

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![ESPR-DPP Tests](https://img.shields.io/badge/ESPR--DPP-18/18_✔️-brightgreen.svg)](../DROS商品專案暫存/DROS-ESPR-DPP-Package)
[![FinRisk Tests](https://img.shields.io/badge/FinRisk-22/22_✔️-brightgreen.svg)](../DROS商品專案暫存/DROS-FinRisk-Privacy-Package)
[![HIPAA Tests](https://img.shields.io/badge/HIPAA-15/15_✔️-brightgreen.svg)](../DROS商品專案暫存/DROS-Health-HIPAA-Package)

[English](README.md) | [繁體中文](README_zh.md)

---

## Overview

This repository demonstrates **3 DROS commercial Add-On Packages** in action.
Each package provides a YAML-driven INTEGRATION_HOOK that enforces data governance
policies — redaction, anonymization, consent verification, risk thresholds,
sanctions screening — on real payloads, not mock data.

### Packages Under Demo

| Package | Directory | Hook | Tests | Policy Domain |
|---|---|---|---|---|
| **DROS-ESPR-DPP** | `../DROS商品專案暫存/DROS-ESPR-DPP-Package/` | `espr_redactor_hook.py` | 18/18 | Carbon DPP, trade secret redaction, role-based disclosure |
| **DROS-FinRisk-Privacy** | `../DROS商品專案暫存/DROS-FinRisk-Privacy-Package/` | `finrisk_monitor_hook.py` + `sanctions_checker.py` | 22/22 | PII anonymization, AML thresholds, sanctions screening |
| **DROS-Health-HIPAA** | `../DROS商品專案暫存/DROS-Health-HIPAA-Package/` | `hipaa_phi_shield_hook.py` | 15/15 | PHI Safe Harbor 18, consent JWT, break-glass |

---

## Quick Start

```bash
# 1. Verify all 3 packages (63 tests total)
python test_verification_suite.py

# 2. Start the live demo server
python server.py

# 3. Open http://localhost:8000/index.html
```

### What you can do

| Feature | How |
|---|---|
| Run 63 real hook tests | `python test_verification_suite.py` |
| Live REST API calling real hooks | `python server.py` → `localhost:8000` |
| Interactive HTML demo | Open `index.html` or track pages |
| Inspect each package | `../DROS商品專案暫存/DROS-*-Package/` |
| Check test evidence | Each package: `tests/results/evidence_*.jsonl` |
| Read package docs | Each package: `README_INSTALL.md` + `TECHNICAL_APPENDIX.md` |

---

## Architecture

```
                        ┌─────────────────────────────────────┐
 HTTP Request / HTML    │  server.py / index.html             │
   Demo Payload  ───→   │  (Demo Entry Point)                 │
                        │        ↓                            │
                        │  vajra_policy.yaml ─→ INTEGRATION_HOOK
                        │    (YAML policy)      (Python hook) │
                        │        ↓                            │
                        │  Redacted / Approved / Blocked      │
                        │  + Audit Trail                      │
                        └─────────────────────────────────────┘
                              ↕
                    ../DROS商品專案暫存/DROS-*-Package/
                    (3 commercial Add-On Packages)
```

---

## Verification Suite

```bash
$ python test_verification_suite.py
============================================================
DROS-VEP Verification Suite (Real Hooks)
  ESPR: .../DROS-ESPR-DPP-Package/INTEGRATION_HOOKS/espr_redactor_hook.py
  FIN:  .../DROS-FinRisk-Privacy-Package/INTEGRATION_HOOKS/finrisk_monitor_hook.py
  HIP:  .../DROS-Health-HIPAA-Package/INTEGRATION_HOOKS/hipaa_phi_shield_hook.py
============================================================
test_01_espr ...................... ok
test_02_finrisk .................. ok
test_03_sanctions ................ ok
test_04_hipaa .................... ok
test_05_yaml ..................... ok
----------------------------------------------------------------------
Ran 5 tests in 0.02s → ALL 5 PILLARS PASSED
```

### What each pillar validates

- **Pillar 1**: ESPR dot-path redaction — YAML-driven, `re.fullmatch` matching
- **Pillar 2**: FinRisk PII anonymization + risk threshold enforcement
- **Pillar 3**: Sanctions list screening — exact + substring, case-insensitive
- **Pillar 4**: HIPAA consent JWT verification + break-glass emergency override
- **Pillar 5**: All 3 packages load from YAML (not hardcoded fallback)

---

## Live REST API

```bash
# Process a carbon BOM through the real ESPR hook
curl -X POST http://localhost:8000/api/v1/espr/process -H "Content-Type: application/json" -d '{"product_id":"DPP-1","bom":{"wafer_baking_temp":"1250C"}}'

# Check a transaction against FinRisk + sanctions
curl -X POST http://localhost:8000/api/v1/finrisk/process -H "Content-Type: application/json" -d '{"tx_id":"T1","amount_usd":50000,"user":{"real_name":"John","ssn":"123-45"}}'

# Submit EHR through HIPAA shield
curl -X POST http://localhost:8000/api/v1/hipaa/process -H "Content-Type: application/json" -d '{"resourceType":"Patient","patient":{"name":"Jane","ssn":"987-65"}}'
```

---

## Interactive HTML Demo

- **Central Demo Portal**: [`index.html`](index.html)
- **Track 01 — Carbon DPP**: [`track01_carbon_dpp/index.html`](track01_carbon_dpp/index.html)
- **Track 02 — Fintech Risk**: [`track02_fintech_privacy/index.html`](track02_fintech_privacy/index.html)
- **Track 03 — Healthcare**: [`track03_healthcare_insurance/index.html`](track03_healthcare_insurance/index.html)

---

## Package Reference

Each package is fully self-contained under `../DROS商品專案暫存/`:

- **Source code**: `.py` (restored from v1.0 `.pyc` black box)
- **Policy**: `vajra_policy.yaml` (YAML-driven, not hardcoded)
- **Matching**: `re.fullmatch` dot-path (no substring false positives)
- **Features**: Sanctions, break-glass, JWT verification, amount-tier profiles
- **Tests**: 63 pytest + `evidence_*.jsonl` output
- **Docs**: `README_INSTALL.md` + `TECHNICAL_APPENDIX.md`
