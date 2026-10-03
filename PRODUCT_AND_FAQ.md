# DROS Add-On Demo — Product & FAQ

## What is this?

This showcase demonstrates **3 commercial DROS Add-On Packages** in a live, testable environment.
Each package enforces data governance policies (redaction, anonymization, consent verification,
risk thresholds, sanctions screening) through YAML-driven Python hooks.

## Packages

| Package | Domain | Key Features |
|---|---|---|
| DROS-ESPR-DPP | EU Carbon Passport | BOM redaction, role-based disclosure, public verifiable fields |
| DROS-FinRisk-Privacy | Financial AML/KYC | PII anonymization, behavioral risk, sanctions lists |
| DROS-Health-HIPAA | Healthcare PHI | Safe Harbor 18, consent JWT, break-glass override |

## FAQ

**Q: Are these mock demos?**
No. Every API call runs against real INTEGRATION_HOOK code from the commercial packages.
The verification suite (`test_verification_suite.py`) asserts against real YAML-loaded policies.

**Q: Where are the actual packages?**
In `../DROS商品專案暫存/DROS-*-Package/`. Each has source code, tests, policy files, and documentation.

**Q: What changed from the competition submission?**
The original hackathon materials have been archived. This repository now serves as
a **live demo platform** for the 3 commercial Add-On Packages.

**Q: Do I need a license key to run the demo?**
No. The demo mode uses built-in fallback policies. License key activation applies
only in production DROS Enterprise deployments via VajraAgent.
