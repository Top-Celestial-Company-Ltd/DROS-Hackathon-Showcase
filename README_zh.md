# DROS Add-On Demo Showcase

> **三大 DROS 商業 Add-On Package 實測展示平台：**
> ESPR-DPP（碳護照）、FinRisk-Privacy（金融風控）、Health-HIPAA（醫療 PHI）

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![ESPR-DPP Tests](https://img.shields.io/badge/ESPR--DPP-18/18_✔️-brightgreen.svg)](../DROS商品專案暫存/DROS-ESPR-DPP-Package)
[![FinRisk Tests](https://img.shields.io/badge/FinRisk-22/22_✔️-brightgreen.svg)](../DROS商品專案暫存/DROS-FinRisk-Privacy-Package)
[![HIPAA Tests](https://img.shields.io/badge/HIPAA-15/15_✔️-brightgreen.svg)](../DROS商品專案暫存/DROS-Health-HIPAA-Package)

[English](README.md) | [繁體中文](README_zh.md)

---

## 概述

此專案實測展示 **3 套 DROS 商業 Add-On Package** 的真實運作。
每套套裝包提供 YAML 政策驅動的 INTEGRATION_HOOK，對真實 payload
執行資料治理（遮罩、匿名化、同意驗證、風險閾值、制裁篩選），非模擬資料。

### 展示套裝包

| 套裝包 | 目錄 | Hook | 測試 | 領域 |
|---|---|---|---|---|
| **DROS-ESPR-DPP** | `DROS商品專案暫存/DROS-ESPR-DPP-Package/` | `espr_redactor_hook.py` | 18/18 | 碳護照、營業秘密遮罩、角色揭露 |
| **DROS-FinRisk-Privacy** | `DROS商品專案暫存/DROS-FinRisk-Privacy-Package/` | `finrisk_monitor_hook.py` + `sanctions_checker.py` | 22/22 | PII 匿名化、AML 閾值、制裁篩選 |
| **DROS-Health-HIPAA** | `DROS商品專案暫存/DROS-Health-HIPAA-Package/` | `hipaa_phi_shield_hook.py` | 15/15 | PHI Safe Harbor 18、同意 JWT、Break-Glass |

---

## 快速開始

```bash
# 1. 驗證三套套裝包（63 項測試）
python test_verification_suite.py

# 2. 啟動實測示範伺服器
python server.py

# 3. 開啟 http://localhost:8000/index.html
```

### 能做什麼

| 功能 | 方式 |
|---|---|
| 執行 63 項真實 Hook 測試 | `python test_verification_suite.py` |
| 即時 REST API（呼叫真實 Hook） | `python server.py` → `localhost:8000` |
| 互動式 HTML 展示 | 開啟 `index.html` 或各 track 頁面 |
| 檢視各套裝包 | `DROS商品專案暫存/DROS-*-Package/` |
| 檢視測試證據 | 各套裝包 `tests/results/evidence_*.jsonl` |
| 閱讀套裝包文件 | 各套裝包 `README_INSTALL.md` + `TECHNICAL_APPENDIX.md` |

---

## 架構

```
 HTTP Request / HTML       server.py / index.html
   Demo Payload     ──→   (展示入口)
                                ↓
                        vajra_policy.yaml ─→ INTEGRATION_HOOK
                          (YAML 政策)         (Python hook)
                                ↓
                          Redacted / Approved / Blocked
                          + Audit Trail
                         ↕
                   DROS商品專案暫存/DROS-*-Package/
                   (3 套商業 Add-On Package)
```

---

## 驗證套件

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

### 五大支柱驗證

- **Pillar 1**: ESPR dot-path 遮罩 — YAML 驅動、`re.fullmatch` 比對
- **Pillar 2**: FinRisk PII 匿名化 + 風險閾值強制
- **Pillar 3**: 制裁名單篩選 — 精確 + 子字串、不分大小寫
- **Pillar 4**: HIPAA 同意 JWT 驗證 + Break-Glass 緊急覆蓋
- **Pillar 5**: 三套均從 YAML 載入規則（非硬編碼 fallback）

---

## 即時 REST API

```bash
# 透過真實 ESPR hook 處理碳 BOM
curl -X POST http://localhost:8000/api/v1/espr/process -H "Content-Type: application/json" -d '{"product_id":"DPP-1","bom":{"wafer_baking_temp":"1250C"}}'

# 檢查交易（FinRisk + 制裁）
curl -X POST http://localhost:8000/api/v1/finrisk/process -H "Content-Type: application/json" -d '{"tx_id":"T1","amount_usd":50000,"user":{"real_name":"John","ssn":"123-45"}}'

# 提交 EHR（HIPAA）
curl -X POST http://localhost:8000/api/v1/hipaa/process -H "Content-Type: application/json" -d '{"resourceType":"Patient","patient":{"name":"Jane","ssn":"987-65"}}'
```

---

## 互動 HTML 展示

- **中央入口**: [`index.html`](index.html)
- **Track 01 — 碳護照**: [`track01_carbon_dpp/index.html`](track01_carbon_dpp/index.html)
- **Track 02 — 金融風控**: [`track02_fintech_privacy/index.html`](track02_fintech_privacy/index.html)
- **Track 03 — 醫療**: [`track03_healthcare_insurance/index.html`](track03_healthcare_insurance/index.html)

---

## 套裝包參考

各套裝包完整自包含於 `DROS商品專案暫存/`：

- **原始碼**: `.py`（自 v1.0 `.pyc` 黑箱還原）
- **政策**: `vajra_policy.yaml`（YAML 驅動，非硬編碼）
- **比對**: `re.fullmatch` dot-path（無子字串 false positive）
- **功能**: 制裁篩選、Break-Glass、JWT 驗證、amount-tier profile
- **測試**: 63 項 pytest + `evidence_*.jsonl` 輸出
- **文件**: `README_INSTALL.md` + `TECHNICAL_APPENDIX.md`
