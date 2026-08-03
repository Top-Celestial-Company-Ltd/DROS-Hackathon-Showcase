# DROS-VEP #04 解法對應說明書 (Solution Mapping)
# Track 04｜政府服務：解決憑證碎片化背後的資料孤島

> **VEP 識別名稱**：DROS GovProxy VEP #04  
> **適用法規**：行政院個資法、政府資訊公開法、MyData 框架、TW-FidO 國家身份驗證  
> **核心痛點**：當 AI Agent 代辦跨機關申請時，如何讓既有憑證安全流動，並清楚劃分「代查」、「代送件」與本人確認的授權邊界？  
> **專利保護**：U.S. PPA No. 64/111,973 (Patent Pending)

---

## 🎯 痛點精確解讀 (Problem Framing)

| 痛點維度 | 問題描述 | 傳統方案的缺口 |
| :--- | :--- | :--- |
| **憑證碎片化** | 戶政、健保、稅務各自有獨立 API 與憑證機制，Agent 需要橫跨多個機關 | Agent 拿到一張憑證後可自行跨機關呼叫，無法鋼性限制橫移 |
| **授權邊界模糊** | 「代查戶籍」與「代送戶籍遷移申請」屬於完全不同的風險等級，但傳統系統僅有登入/未登入兩種狀態 | 無法區分「代查」、「代送件」、「本人確認」三層不同授權強度 |
| **高風險動作失控** | Agent 若能「代送件」，理論上可在公民不知情下提交任意申請 | 缺乏帶內強制本人二次確認 (HITL) 機制 |
| **撤銷困難** | 公民若想終止 AI 代理授權，需聯絡客服或重設密碼，無即時效果 | 授權撤銷延遲數分鐘甚至數小時 |

---

## 🏗️ DROS GovProxy VEP 解法架構

### 三層授權邊界矩陣 (Three-Tier Authorization Scope Matrix)

```
┌─────────────────────────────────────────────────────────────────┐
│            DROS GovProxy VEP — Scope Permission Matrix          │
├─────────────────────────┬───────────────┬───────────────────────┤
│ Tool / Action           │ 授權層級       │ 執行政策              │
├─────────────────────────┼───────────────┼───────────────────────┤
│ query_household_reg()   │ 代查 (L1)     │ PERMIT 自動放行       │
│ query_tax_cert()        │ 代查 (L1)     │ PERMIT 自動放行       │
│ submit_application()    │ 代送件 (L2)   │ HITL 強制本人確認     │
│ sign_contract()         │ 本人簽署 (L3) │ DENY 硬性禁止代理     │
│ cross_agency_push()     │ 跨機關橫移    │ DENY 硬性禁止代理     │
└─────────────────────────┴───────────────┴───────────────────────┘
```

### 技術棧整合層 (Integration Stack)

| 層級 | 技術組件 | 角色 |
| :--- | :--- | :--- |
| **L0 - 身份層** | TW-FidO / PKI 國家憑證 | 公民身份綁定，DIT 代理憑證簽發 |
| **L1 - 帶內代理層** | DROS VEP C-ABI Gate | 26.1μs 帶內攔截所有 Tool Call，執行 Scope 矩陣判定 |
| **L2 - 數據閘道層** | MyData Gov Gateway | 跨機關 API 路由，VEP 注入攔截代理 |
| **L3 - HITL 確認層** | 公民 App 推播 + 300s 逾時 | 代送件動作強制暫停，待本人 App 二次確認 |
| **L4 - 稽核層** | SHA-256 Merkle Chain | 每筆代理 API 呼叫留存不可篡改密碼學憑證 |

---

## 🔒 6 大信任要點對應說明 (Governance Gap Memo)

### 1. Principal — 代表誰？

**問題**：Agent 代辦時，機關如何確認「現在操作的是 AI 代理，而非公民本人」？

**DROS 解法**：
- DIT（確定性身份標籤）雙層綁定：公民 TW-ID（A123456789）＋代理 AI 識別碼（GovAssist-AI v2.1）
- 兩者共同出現在每筆 API 呼叫 Header，機關系統可精確區分「代理查詢」vs「本人操作」

```json
{
  "dit_version": "v1.2-dros-gov",
  "principal": "陳小明 (TW-ID: A123456789)",
  "proxy_agent": "GovAssist-AI v2.1",
  "scope": ["query_household_reg", "query_tax_cert"]
}
```

---

### 2. Authorization — 被授權做什麼？

**問題**：「代查」和「代送件」的邊界如何硬性劃定？

**DROS 解法**：
- **L1 代查 PERMIT**：`query_*` 系列 Tool Call 直接放行，傳回結果自動去識別化（姓名、身分證號碼欄位 REDACTED）
- **L2 代送件 HITL**：`submit_application()` 強制觸發公民 App 推播，Agent 交易被硬性懸停 300 秒等待確認
- **L3 本人操作 DENY**：`sign_contract()`、`cross_agency_push()` 一律 HTTP 403，不給 Agent 任何代理空間

---

### 3. Tool / Action — 跨機關橫移如何被控制？

**問題**：Agent 拿到戶籍資料後，能否自行將資料橫推至健保署或稅務局？

**DROS 解法**：
- VEP C-ABI Gate 帶內攔截 `cross_agency_push()` 呼叫
- 決策延遲：**26.1μs**（遠低於任何網路 Round Trip Time）
- Agent 收到 `HTTP 403 FORBIDDEN`，Audit Log 同步寫入攔截記錄
- 機關間資料流動必須經由公民明確授權的 MyData 閘道，不允許 Agent 自行路由

---

### 4. Policy Gate — 高風險動作如何被擋？

**問題**：送件是不可逆動作，一旦 Agent 誤送，如何防止？

**DROS 解法**：
- **HITL (Human-In-The-Loop) 閘門**：檢測到 `submit_application()` 呼叫後：
  1. VEP Policy Gate 立即硬性懸停交易（不執行，不回傳成功）
  2. 推播通知發送至公民手機 App
  3. 公民確認 → 交易繼續；公民拒絕或逾時 300s → 交易取消並寫入拒絕日誌
- 完全不依賴 Agent 自律，由 VEP 帶內實施強制硬停

---

### 5. Audit Log — 如何追溯代辦行動？

**問題**：如果事後發現代辦有問題，如何舉證？

**DROS 解法**：
- SHA-256 Merkle Hash Chain：每筆代理 API 呼叫均產生密碼學雜湊
- 每筆 Log 包含：時間戳、公民 TW-ID、代理 AI 識別碼、Tool Call 名稱、Scope 判定結果、決策延遲
- Merkle Chain 前後鏈結，任何篡改均可被數學驗證
- 評審可在展示台直接點擊每筆 Log 彈出完整憑證

---

### 6. Expiry / Revocation — 公民如何即時撤銷？

**問題**：公民授權 AI 代辦後反悔，如何即時終止？

**DROS 解法**：
- **O(1) 常數時間 RCU 原子換指針**：公民點擊「撤銷代理」後
  - 記憶體中 Token 指針原子切換（無鎖操作，< 1μs）
  - 下一筆 API 請求立即收到 `HTTP 403 PATIENT_CONSENT_REVOKED`
  - 全程無需等待 Session 逾時，無延遲視窗

---

## 🆚 競品定位 (Competitive Positioning)

| 方案 | 授權邊界 | 跨機關橫移防護 | HITL 強制 | 撤銷速度 | 稽核強度 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **DROS GovProxy VEP** | ✅ 三層硬性矩陣 | ✅ C-ABI 26.1μs | ✅ 帶內強制懸停 | ✅ O(1) RCU | ✅ Merkle 密碼學 |
| OAuth 2.0 + Scope | ⚠️ 靜態宣告，無執行期強制 | ❌ 需應用層自律 | ❌ 無 | ⚠️ 分鐘級 | ❌ 無 |
| TW-FidO 單純認證 | ❌ 僅驗身份，無授權矩陣 | ❌ 無 | ❌ 無 | ❌ 需重認證 | ❌ 無 |
| 傳統 API Gateway | ⚠️ IP/Rate Limit 層 | ❌ 無語意感知 | ❌ 無 | ⚠️ 分鐘級 | ⚠️ 基本 Log |

---

## 🚀 展示台快速驗證

```bash
# 啟動 GovProxy VEP 展示台
python server.py
# 開啟: http://localhost:8000/track04_gov_services/
```

**評審 1 分鐘 Demo 路徑**：
1. **代查授權** → Agent 查詢戶籍，個資欄位自動 REDACTED
2. **越權攔截** → Agent 嘗試 cross_agency_push()，26.1μs 收 403
3. **本人 HITL 確認** → submit_application() 強制觸發 App 推播懸停
4. **緊急撤銷** → 公民撤銷代理授權，O(1) RCU 即時生效
5. **Merkle 憑證** → 點擊任一 Audit Log 出示密碼學憑證

---

*專利聲明：DROS 執行治理與安全技術已申請美國臨時專利保護（U.S. PPA No. 64/111,973）。*  
*© 2026 OpenShip Ecosystem. All Rights Reserved.*
