# DROS-VEP Lite 展演總對照說明書 (DROS Solution Mapping Master Overview)

> **全棧產品名稱**：DROS-VEP Lite 確定性 Agent 執行期治理與全棧企業網關  
> **發射部署平台**：OpenShip Multi-VEP Cloud Launchpad (`http://localhost:8000/index.html`)  
> **專利保護標示**：U.S. Provisional Patent Application No. 64/111,973 (Patent Pending)

---

## 🎯 專案核心定位 (Core Mission)

本專案非單純 LLM 應用程式，而是針對 AI Agent 執行期之 **企業級確定性治理與商業部署內核 (VEP Infrastructure)**。透過二進位 C-ABI 與 eBPF 網關帶內防線，提供 **26.1 微秒延遲、零文字檔依賴、$O(1)$ 常數時間動態撤銷與 SHA-256 Merkle 密碼學追溯稽核**。

---

## 📚 題目別「DROS 解法對應說明書」索引地圖

| 題目 Track | 主題情境 | 專屬解法對應說明書連結 | 專屬獨立 VEP 控制台 |
| :--- | :--- | :--- | :--- |
| **Track 01** | **製造貿易**：碳足跡與 DPP 數位產品護照資料流控制 | 📄 [Track 01 DROS 解法說明](https://github.com/Top-Celestial-Company-Ltd/DROS-Hackathon-Showcase/blob/main/track01_carbon_dpp/DROS_SOLUTION_MAPPING.md) | 🌐 [Alpha 製造 VEP](http://localhost:8000/track01_carbon_dpp/index.html) |
| **Track 02** | **電商與第三方支付**：隱私保護下的可疑行為偵測 | 📄 [Track 02 DROS 解法說明](https://github.com/Top-Celestial-Company-Ltd/DROS-Hackathon-Showcase/blob/main/track02_fintech_privacy/DROS_SOLUTION_MAPPING.md) | 🌐 [PayFlow 金融 VEP](http://localhost:8000/track02_fintech_privacy/index.html) |
| **Track 03** | **醫療保險**：跨產業資料合作的誘因與邊界 | 📄 [Track 03 DROS 解法說明](https://github.com/Top-Celestial-Company-Ltd/DROS-Hackathon-Showcase/blob/main/track03_healthcare_insurance/DROS_SOLUTION_MAPPING.md) | 🌐 [MediGuard 醫療 VEP](http://localhost:8000/track03_healthcare_insurance/index.html) |
| **Track 04** | **政府服務**：解決憑證碎片化背後的資料孤島，跨機關代理授權邊界（代查 / 代送件 / 本人確認三層控制） | 📄 [Track 04 DROS 解法說明](https://github.com/Top-Celestial-Company-Ltd/DROS-Hackathon-Showcase/blob/main/track04_gov_services/DROS_SOLUTION_MAPPING.md) | 🌐 [GovProxy VEP](http://localhost:8000/track04_gov_services/index.html) |
| **Track 05** | **普惠金融**：移工數位信任與防詐憑證機制，87萬移工多文件複合 DIT 綁定、三層漸進信任矩陣、SIM Swap 防禦與 O(1) 緊急凍結 | 📄 [Track 05 DROS 解法說明](https://github.com/Top-Celestial-Company-Ltd/DROS-Hackathon-Showcase/blob/main/track05_inclusive_finance/DROS_SOLUTION_MAPPING.md) | 🌐 [MigraTrust VEP](http://localhost:8000/track05_inclusive_finance/index.html) |
| **Track 06** | **供應鏈貿易金融 (加分題)**：RBA 稽核合規可驗證憑證，採購 AI Agent 可驗證工廠合規性但無法讀完整稽核報告，選擇性揭露閘門 + ZKP-Lite + W3C VC 2.0 | 📄 [Track 06 DROS 解法說明](https://github.com/Top-Celestial-Company-Ltd/DROS-Hackathon-Showcase/blob/main/track06_supply_chain_rba/DROS_SOLUTION_MAPPING.md) | 🌐 [SupplyProof VEP](http://localhost:8000/track06_supply_chain_rba/index.html) |

---

## 🔒 6 大信任要點通解框架 (The 6 Pillars Universal Framework)

不管大會公布何種新題目 (Track 03 ~ 06)，DROS-VEP Lite 均能以通用硬體與網關邊界實施鋼性防護：

1. **Principal (身份)**：DIT Token 帶內注入，強綁定團隊、企業與法人的加密 Key。
2. **Authorization (授權)**：Scope 矩陣明確宣告 `PERMIT` 與 `PROHIBITED` 動作與欄位。
3. **Tool/Action Bound (邊界)**：所有 Tool Call 必須過 C-ABI 網關，未授權動作在 26.1μs 內硬熔斷。
4. **Policy Gate (門閥)**：機密資料自動 Redact 遮蔽，高風險動作觸發 HITL 懸停雙簽。
5. **Audit Log (稽核)**：Tamper-Evident SHA-256 Merkle Chain，點擊出示可獨立驗證之 Cert Modal。
6. **Revocation (撤銷)**：$O(1)$ 常數時間 RCU Token 秒級註銷，管理者點擊瞬間中斷權限。

---

## ⚡ 10 秒極速可重現命令 (Zero-Dependency One-Command Verification)

```bash
# 1. 執行 TDD 單元測試 (0.005 秒驗證 5 大確定性安全要點)
python test_verification_suite.py

# 2. 啟動 OpenShip 雲端 Multi-VEP 發射台與 REST API
python server.py
# 存取網址: http://localhost:8000/index.html
```

---

*專利聲明：DROS 執行治理與安全技術已申請美國臨時專利保護（U.S. Provisional Patent Application No. 64/111,973）。*  
*© 2026 OpenShip Ecosystem. All Rights Reserved.*
