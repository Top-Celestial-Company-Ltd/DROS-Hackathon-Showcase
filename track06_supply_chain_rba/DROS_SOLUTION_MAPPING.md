# DROS-VEP #06 解法對應說明書 (Solution Mapping)
# Track 06｜加分題 · Track 01 延伸 · 供應鏈與貿易金融
# RBA 供應鏈合規的可驗證憑證機制

> **VEP 識別名稱**：DROS SupplyProof VEP #06  
> **適用法規**：RBA（Responsible Business Alliance）行為準則、W3C Verifiable Credentials 2.0、歐盟 CSDD 指令（供應鏈盡職調查）、金融監理合規 ESG 揭露要求  
> **核心痛點**：RBA 稽核仍高度依賴人工與紙本；如何讓供應鏈合規證明**持續可驗證**，同時**不必揭露工廠的完整內部資料**？  
> **專利保護**：U.S. PPA No. 64/111,973 (Patent Pending)

---

## 🎯 痛點精確解讀 (Problem Framing)

| 痛點維度 | 問題描述 | 傳統方案的缺口 |
| :--- | :--- | :--- |
| **稽核高度依賴人工與紙本** | 每年 RBA 稽核需要派員到工廠、收集紙本報告，耗時 3-6 個月，成本高昂 | 稽核結果無法即時數位化與跨機構共享 |
| **合規證明無法被採購 AI 驗證** | 採購方的 AI Agent 想驗證供應商是否符合 RBA 標準，但無法安全存取原始資料 | 要嘛全公開（洩露商業機密），要嘛完全不透明（AI 無法驗證） |
| **完整稽核報告洩露商業機密** | 工廠勞工人數、事故紀錄、組織架構、廢棄物清單屬於高度商業敏感資料 | 傳統 API 要嘛全給要嘛全擋，缺乏細粒度選擇性揭露機制 |
| **憑證偽造與過期重放** | 詐欺性供應商偽造合規憑證，或重放過期認證欺騙採購商 | 無密碼學驗證機制，人工肉眼難以識別偽造 |
| **撤銷後憑證繼續流通** | 工廠被 RBA 取消認證後，舊憑證仍可能被繼續使用 | 撤銷延遲，買方收到已撤銷憑證而不自知 |

---

## 🏗️ DROS SupplyProof VEP 解法架構

### 核心創新：選擇性揭露矩陣 (Selective Disclosure Matrix)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│           DROS SupplyProof VEP — Selective Disclosure Policy Matrix          │
├───────────────────┬──────────────────┬───────────────┬───────────────────────┤
│ RBA 類別          │ 採購 AI 可取得    │ 採購 AI 禁止  │ 可驗不可讀 (Hash)     │
├───────────────────┼──────────────────┼───────────────┼───────────────────────┤
│ 勞工權益 (Labor)  │ compliant=TRUE   │ worker_count  │ score_hash (SHA-256)  │
│                   │                  │ audit_details │                       │
├───────────────────┼──────────────────┼───────────────┼───────────────────────┤
│ 健康安全 (H&S)    │ compliant=TRUE   │ incident_log  │ score_hash (SHA-256)  │
│                   │                  │ facility_map  │                       │
├───────────────────┼──────────────────┼───────────────┼───────────────────────┤
│ 環境 (Env)        │ compliant=TRUE   │ emission_raw  │ score_hash (SHA-256)  │
│                   │                  │ waste_records │                       │
├───────────────────┼──────────────────┼───────────────┼───────────────────────┤
│ 商業倫理 (Ethics) │ compliant=TRUE   │ bribery_cases │ score_hash (SHA-256)  │
│                   │                  │ vendor_list   │                       │
├───────────────────┼──────────────────┼───────────────┼───────────────────────┤
│ 管理體系 (Mgmt)   │ compliant=TRUE   │ org_chart     │ score_hash (SHA-256)  │
│                   │                  │ policy_docs   │                       │
└───────────────────┴──────────────────┴───────────────┴───────────────────────┘
      ↑ VEP PERMIT                  ↑ VEP HARD DENY        ↑ ZKP-Lite Hash只驗
```

### 技術棧整合層 (Integration Stack)

| 層級 | 技術組件 | 角色 |
| :--- | :--- | :--- |
| **L0 - 身份層** | 供應商 DIT + 採購方 BuyBot-AI DIT | 雙向身份綁定，防偽造採購商套取資料 |
| **L1 - 帶內代理層** | DROS VEP C-ABI Gate | 26.1μs 帶內攔截所有 Tool Call，執行 SD 政策 |
| **L2 - 選擇性揭露層** | SD-Gate Policy Engine | 解析 `rba_selective_disclosure_v2.yaml`，精確控制每個欄位的揭露層級 |
| **L3 - 零知識證明層** | ZKP-Lite (Groth16) | 生成 π 證明「合規分數 ≥ 80」而不洩露分數本身 |
| **L4 - 憑證格式層** | W3C VC 2.0 + DROS-SD Extension | 標準可驗證憑證格式，跨買方/稽核機構/銀行通用 |
| **L5 - 稽核層** | SHA-256 Merkle Chain | 每筆查驗產生不可篡改密碼學憑證鏈 |

---

## 🔒 6 大信任要點對應說明 (Governance Gap Memo)

### 1. Principal — 代表誰？

**問題**：供應商如何確認「申請查驗合規的是真正的採購商 AI，不是競爭對手偽冒套取商業情報」？

**DROS 解法**：
- **雙向 DIT 綁定**：供應商 DID (did:dros:fab-tw-01) + 採購方 BuyBot-AI DIT 在查驗請求 Header 中同時呈現
- VEP 先驗證採購方身份合法，再啟動選擇性揭露政策
- 未認證的採購方身份直接收 403，不觸發任何揭露

```json
{
  "@context": "W3C-VC-2.0 + DROS-SD",
  "supplier_did": "did:dros:fab-tw-01",
  "buyer_agent": "BuyBot-AI v2.3",
  "rba_cert_id": "RBA-2026-TW-88821",
  "query_scope": "verify_rba_cert_only"
}
```

---

### 2. Authorization — 採購 AI 被授權做什麼？

**問題**：採購 AI 被允許查驗合規狀態，但不能存取工廠內部資料，這條邊界如何技術上落地？

**DROS 解法**：
- **選擇性揭露矩陣**（見上方表格）硬性定義每個欄位的揭露策略
- 採購 AI 的授權範圍僅有 `verify_rba_cert()`，得到的回傳是：
  - 各項合規狀態 = TRUE/FALSE（REVEAL）
  - 分數雜湊值（可驗證但不可逆推）
  - Groth16 ZKP 證明 π（可驗證分數 ≥ 門檻，不洩露數值）
- 原始稽核細節、人員名單、事故日誌 → 全部 VEP HARD DENY

---

### 3. Tool / Action — 哪些工具呼叫被控制？

**問題**：採購 AI 若嘗試直接讀取工廠 ERP 或完整稽核報告 PDF，如何被阻止？

**DROS 解法**：
- **VEP C-ABI Tool Interceptor** 帶內攔截：
  - `verify_rba_cert()` → **PERMIT**，26.1μs 決策，回傳選擇性揭露 VC
  - `read_full_audit_report()` → **DENY**，26.1μs 決策，HTTP 403
  - `query_worker_count()` → **DENY**，HTTP 403
  - `access_factory_erp()` → **DENY**，HTTP 403
- 供應商 ERP 與稽核資料庫與 VEP 網關物理隔離，採購 AI 無直接路由

---

### 4. Policy Gate — 選擇性揭露閘門（Track 06 核心創新）

**問題**：如何在技術上保證「採購方可以相信工廠合規，但工廠不必公開任何原始數據」？

**DROS 解法**：**ZKP-Lite 選擇性揭露閘門**

- **步驟 1**：VEP SD-Gate 讀取 `rba_selective_disclosure_v2.yaml` 選擇性揭露政策
- **步驟 2**：從稽核資料庫取得原始分數（VEP 內部，採購 AI 無法存取）
- **步驟 3**：產生 Groth16 零知識證明 `π`，數學上可驗證「各類合規分數均 ≥ 80」
- **步驟 4**：只將 `{compliant=TRUE, score_hash, π}` 傳回採購 AI
- **採購 AI 收到的結論**：「這個供應商通過 RBA 稽核」— 有密碼學證明，不需信任紙本

> 這等同於學術界的 **零知識證明（Zero-Knowledge Proof）** 在供應鏈合規場景的具體工程應用。

---

### 5. Audit Log — 如何追溯每次合規查驗？

**問題**：銀行或監理機關要求提供「採購商在何時驗證了哪個供應商的哪條 RBA 規範」，如何提供合規舉證？

**DROS 解法**：
- **W3C VC 2.0 標準格式**：每筆查驗產生可驗證憑證
- **SHA-256 Merkle Hash Chain**：每筆憑證與前後記錄鏈結，任何篡改可被數學驗證
- 憑證欄位包含：時間戳、採購方 DIT、供應商 DIT、RBA 認證 ID、SD 政策版本、ZKP-Lite π
- 銀行、監理機關、客戶均可獨立核實，不需聯繫供應商本身

```json
{
  "vc_type": "RBA-Compliance-VC",
  "timestamp": "2026-08-05T08:00:00Z",
  "buyer_agent": "BuyBot-AI v2.3",
  "supplier_did": "did:dros:fab-tw-01",
  "rba_cert": "RBA-2026-TW-88821",
  "overall_compliant": true,
  "zkp_proof": "π=Groth16:0x3f9a...c721",
  "merkle_hash": "0xc8f3a2b1..."
}
```

---

### 6. Expiry / Revocation — RBA 撤銷後如何立即失效？

**問題**：工廠被 RBA 取消認證（如發現違規用工），舊憑證是否還能被採購 AI 使用？

**DROS 解法**：
- **O(1) RCU 原子換指針**：RBA Registry 發出撤銷訊號後
  - VEP 記憶體中 Token 狀態原子切換（< 1μs）
  - 所有後續 `verify_rba_cert()` 呼叫立即收 `HTTP 403 RBA_CERT_REVOKED`
  - 無需等待 Session 逾時，無延遲視窗
- **過期重放防禦**：VEP 在每次查驗時主動向 RBA Registry API 確認憑證當前狀態，不依賴本地快取的過期時間戳

---

## 🆚 為什麼這題是加分題？DROS 的核心優勢

傳統供應鏈合規面臨「透明 vs 機密」的零和困境：

- **全公開** → 工廠商業機密外洩（競爭對手取得人力成本、廢棄物資料）
- **全不公開** → 採購 AI 無法驗證合規（回到人工紙本稽核原點）

**DROS SupplyProof VEP 打破零和**：
- 選擇性揭露：AI 可以得到「合規 = TRUE」的密碼學保證（不依賴信任）
- 商業機密保護：工廠內部資料從未離開供應商側的 VEP 邊界
- ZKP-Lite：技術上等同論文級零知識證明，可供學術與法律採信

---

## 🆚 競品定位 (Competitive Positioning)

| 方案 | 選擇性揭露 | ZKP 保護 | 可撤銷 | 跨機構標準格式 | 即時性 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **DROS SupplyProof VEP** | ✅ 欄位級 SD 矩陣 | ✅ Groth16 ZKP | ✅ O(1) RCU | ✅ W3C VC 2.0 | ✅ 26.1μs |
| 傳統紙本 RBA 稽核 | ❌ 全公開或全不給 | ❌ 無 | ❌ 無效 | ❌ PDF/紙本 | ❌ 月/季 |
| 區塊鏈存證 | ⚠️ 上鏈即公開 | ❌ 無 | ❌ 不可撤銷 | ⚠️ 各鏈不互通 | ⚠️ 秒~分鐘 |
| 傳統 API Token | ❌ 全開或全關 | ❌ 無 | ⚠️ 分鐘級 | ❌ 自定義格式 | ⚠️ 秒 |

---

## 🚀 展示台快速驗證

```bash
python server.py
# 開啟: http://localhost:8000/track06_supply_chain_rba/
```

**評審 1 分鐘 Demo 路徑**：
1. **查驗申請** → BuyBot-AI 呼叫 verify_rba_cert()，VEP 啟動 SD 政策
2. **選擇性揭露 VC** → 五大類合規 = TRUE，原始資料全部 REDACTED，ZKP π 附上
3. **越權讀報告攔截** → read_full_audit_report() 26.1μs 收 403
4. **RBA 憑證撤銷** → O(1) RCU，所有後續查驗立即收 403
5. **Merkle 憑證出示** → 點擊任一 Audit Log 出示 W3C VC + ZKP-Lite 密碼學證明

---

*專利聲明：DROS 執行治理與安全技術已申請美國臨時專利保護（U.S. PPA No. 64/111,973）。*  
*© 2026 OpenShip Ecosystem. All Rights Reserved.*
