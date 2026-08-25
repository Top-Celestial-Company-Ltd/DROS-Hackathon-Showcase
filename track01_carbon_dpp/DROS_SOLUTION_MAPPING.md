# Track 01 專屬：DROS-VEP 解決方案對應說明書 (Manufacturing & Carbon DPP)

> **主題**：製造貿易 ── 碳足跡與 DPP 數位產品護照資料流控制  
> **核心技術內核**：DROS-VEP Lite (Deterministic Runtime Governance & Zero-Knowledge Data Redaction)

---

## 零、 DROS 整體機制導讀（不熟悉本系統的評審請從這裡開始）

### 🔍 DROS 是什麼？它解決的根本問題是什麼？

傳統 AI Agent 的最大安全缺口，不是 AI 模型本身，而是 **「AI Agent 被授權後，誰來管控它實際執行期的行為？」**

以信用卡舉例：銀行核發信用卡給你（核卡 = 授權），但你每筆消費仍受到「刷卡上限、境外管控、異常交易凍卡」等機制約束（執行期治理）。現在大多數企業的 AI Agent 只有「核卡」，沒有「刷卡管控」。DROS 就是那套執行期管控系統。

---

### 🏗️ DROS 架構的 3 個核心組件

```
┌──────────────────────────────────────────────────────────────────┐
│                    DROS 三層防禦架構示意                          │
│                                                                  │
│  【組件 A】DIT Token（身份憑證注入層）                            │
│   ↓ 每個 AI Agent 啟動時，系統自動注入一組加密身份憑證             │
│   ↓ 憑證綁定：「誰（Agent ID）+ 被授權做什麼（Scope）+ 到期時間」  │
│                                                                  │
│  【組件 B】VEP Policy Gate（帶內執行期策略閘門層）                 │
│   ↓ Agent 每次呼叫 API / Tool 時，必須先過這道閘門                │
│   ↓ 閘門比對 DIT Token 的 Scope 與本次動作是否吻合                │
│   ↓ 不吻合 → 26.1 微秒內在二進位層硬性熔斷，AI 完全無法繞過       │
│   ↓ 高風險動作 → 掛起交易，觸發人工雙重簽署（Human-in-the-Loop）  │
│                                                                  │
│  【組件 C】Merkle Audit Chain（不可竄改稽核追蹤層）               │
│   ↓ 每次決策（放行 / 熔斷 / 掛起）都寫入帶 SHA-256 雜湊的稽核鏈   │
│   ↓ 前後雜湊互相鏈結，任何竄改都會使整條鏈失效（可獨立驗證）       │
└──────────────────────────────────────────────────────────────────┘
```

### ⚡ 為什麼是「帶內 (In-Band)」，而不是「帶外 (Out-of-Band)」？

- **帶外方案（傳統）**：API Gateway / WAF 部署在 AI Agent 外部，Agent 在被攔截之前可能已完成惡意動作，或繞過 Gateway 直接呼叫底層 API。
- **DROS 帶內方案**：VEP Policy Gate 以 C 語言 ABI（二進位介面）嵌入在 Agent 執行時期的函式呼叫鏈中，Agent 在呼叫任何外部 Tool 之前，**物理上必須先通過閘門**，沒有繞過的可能性。

> 💡 **類比理解**：帶外 = 機場 X 光機在出境大廳外面（還沒進機場就可以繞過去）；帶內 = X 光機直接安裝在登機門走廊，完全無法繞過。

---

### 🖥️ 傳統作業系統 (OS) vs DROS 確定性治理作業系統對照表

DROS 之於 AI Agent，正如 Linux / POSIX 之於傳統電腦行程（Process）。DROS 實現了**「底層治理與上層業務的完全解耦」**，讓開發者專注應用目標，治理機制一鍵原生賦能：

| 治理維度 | 傳統作業系統 (Linux / POSIX OS) | **DROS 確定性 AI 治理作業系統 (AI Agent OS)** | 核心解決的痛點 |
| :--- | :--- | :--- | :--- |
| **1. 執行主體 (Subject)** | Process PID / User UID | **DIT Token (綁定法人 vLEI / 自然人 MyData)** | 解決「AI 到底是代表誰？出了事誰負責？」 |
| **2. 權限邊界 (Permission)** | File Permissions / POSIX ACL (rwx) | **Zero-Heap Capability Bitmaps (暫存器級位元圖)** | 解決「權限範圍多大？精確鎖定 Tool 與 API 呼叫」 |
| **3. 系統呼叫保護 (Syscall)** | Ring 0 / Kernel Mode 記憶體隔離 | **C-ABI 帶內攔截閘門 (In-Band VEP Gate)** | 解決「AI 意圖不可控，物理阻斷危險呼叫」 |
| **4. 異常處理 (Fault Handling)** | `SIGSEGV` / `SIGKILL` 核心崩潰保護 | **26.1 μs 帶內硬熔斷 (Hard Circuit-Breaker)** | 解決「Prompt Injection 越獄與惡意行為」 |
| **5. 存取稽核 (Auditing)** | `auditd` / Linux Journal 日誌 | **SHA-256 Merkle Hash 密碼學證據鏈** | 解決「事後偽造與串供，產出法院採信收據」 |
| **6. 資源回收 (Revocation)** | `kill -9` / Process Terminate | **$O(1)$ RCU 原子指針秒級動態撤銷** | 解決「授權過期或被撤銷後，背景 Agent 偷跑」 |

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        【上層：多元豐富的業務應用層 (Application Layer)】              │
│                                                                                        │
│   Track 01: 碳足跡計算      Track 02: 反詐特徵提取      Track 03: 醫療病歷解析         │
│   Track 04: 政府津貼試算    Track 05: 移工居留審核      Track 06: RBA 契約多模態審查   │
│                                                                                        │
│   👉 開發者只需專注：Prompt 工程、業務流程、UI 介面、演算法與任務目標！               │
└────────────────────────────────────────────────────────────────────────────────────────┘
                                            ▲
                                            │ 簡單極致的標準介面 (C-ABI / DIT / REST)
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   【底層：DROS-6P 確定性治理微內核 (Deterministic OS Kernel)】         │
│                                                                                        │
│   1. Principal (DIT 注入)       2. Authorization (位元圖映射)  3. Tool Bound (帶內阻斷)│
│   4. Policy Gate (微秒級熔斷)   5. Audit Log (Merkle 證據鏈)   6. Revocation (RCU 撤銷)│
│                                                                                        │
│   🛡️ 原生具備：二進位層級安全約束、零堆積分配、法院採信力、跨機構可信網狀聯防！        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 🔺 跨產業統一治理核心：DROS「黃金三角形模型 (The Golden Triangle)」

在所有產業高信任場景中，**AI 是 Detection & Knowledge Layer（分析引擎），DROS 則是 Execution Governance Layer（執行期治理底座）**。兩者透過「最小必要資訊」與「確定性門閥」完美閉環，解決「AI 不必被 100% 盲目信任，也能安全在真實世界執行」的世紀難題：

```
                    【REAL-WORLD DATA / ENTERPRISE CORE】
                                      │
                                      ▼
                        ┌───────────────────────────┐
                        │   DROS 執行期政策閘門層   │
                        └─────────────┬─────────────┘
                                      │
                 ┌────────────────────┴────────────────────┐
                 ▼                                         ▼
     【Allowed Data (最小必要揭露)】               【Forbidden Data (機密隔離)】
     • 製造: 去識別化碳足跡/製程係數               • 製造: 核心 BOM 原料成本/良率
     • 金融: 去識別化圖關聯特徵                    • 金融: 明文姓名/身分證號/帳戶明細
     • 醫療: ICD-10診斷碼/理賠金額                 • 醫療: 18項 PHI/病歷日誌/遺傳病史
     • 供應鏈: 合規狀態 TRUE / ZKP 證明            • 供應鏈: 工廠良率/全體薪資/組織圖
                 │                                         │
                 ▼                                         ▼
     ┌────────────────────────┐              ┌──────────────────────────┐
     │ 產業 AI Detection /    │              │ 💥 C-ABI 帶內硬性阻斷    │
     │ Domain Agent 決策引擎  │              │ (HTTP 403 26.1 μs 熔斷)  │
     └───────────┬────────────┘              └──────────────────────────┘
                 │
                 ▼ (Risk Score / Analysis / Draft Action)
     ┌────────────────────────┐
     │ DROS Policy Gate       │
     │ 帶內防禦 + 人類雙簽    │
     └───────────┬────────────┘
                 │
                 ▼
     【確定性執行 / Merkle 密碼學證據鏈】
```

---

## 一、 題目缺口與現實產業痛點 (Governance Gap & Industry Context)

### 🌍 產業背景：歐盟 ESPR / CBAM 法規強制上路

歐盟 **ESPR (Ecodesign for Sustainable Products Regulation)** 於 2026 年強制生效，要求所有進口至歐盟的製造產品必須出示 **DPP (Digital Product Passport)** 數位產品護照，內含可供機器讀取與 AI 查驗的碳足跡數據、循環性指標與供應鏈溯源記錄。

**出口商的現實困境：**

```
歐盟稽核員或查驗 AI Agent 要求：
  「請提供 DPP 護照資料，包含碳排放量與供應鏈原料來源」
                    ↓
台灣製造商的兩難困境：
  ✅ 提供完整資料 → 通關！但商業機密外洩：
    - 矽晶圓燒結溫度（核心製程配方）
    - BOM 物料清單（成本結構完全暴露）
    - 供應商報價（競爭對手立即知道你的成本）
  ❌ 拒絕提供     → 通關失敗！貨物被退回！
```

### 🤖 AI Agent 帶來的額外攻擊面

當企業導入 AI Agent 執行跨境通關作業時，出現了 **傳統 API 不存在** 的新型攻擊向量：

1. **Prompt Injection（提示詞注入）**：攻擊者在上傳至歐盟系統的 DPP 文件中嵌入惡意指令，誘騙企業內部 Agent 在回應時附帶輸出核心 BOM 配方。
2. **語意幻覺洩密（Hallucination Exfiltration）**：AI Agent 在自由生成回應時，可能因語意推理而「補充說明」了不應揭露的配方細節。
3. **跨工具越權串鏈（Tool Chaining Escape）**：攻擊者誘導 Agent 先合法讀取 DPP 摘要，再串接呼叫 `export_full_bom()` 工具，繞過個別工具的授權限制。

### ❌ 傳統解法的致命缺陷

| 傳統解法 | 看起來能解決... | 實際致命缺陷 |
| :--- | :--- | :--- |
| API Gateway 擋掉整個請求 | 阻止資料外洩 | 歐盟稽核員完全看不到任何資料，通關失敗 |
| 人工整理「安全版」DPP | 保護商業機密 | 每次人工處理成本高、不可擴展、無法即時 |
| LLM Prompt 警告（「請勿洩密」） | 軟性提醒 AI | Prompt Injection 100% 可繞過文字層防禦 |
| 聯邦學習 / 同態加密 | 保護原始數據 | 僅解決靜態數據問題，無法治理 Agent 的動態行為 |

---

## 二、 DROS-VEP 解法：帶內動態零知識過濾架構

### 🔧 核心解法：在 API 回應離開伺服器之前，於帶內自動過濾商業機密欄位

```
歐盟稽核 AI Agent 發出請求
        │
        │  HTTP GET /api/v1/dpp/CHIP-A1-2026
        ▼
┌──────────────────────────────────────────────────────────────┐
│  【DROS VEP Policy Gate】── 帶內攔截點                        │
│                                                              │
│  Step 1: 驗證 DIT Token                                      │
│    - 解析 X-DIT-Token 標頭，確認請求來自授權的稽核 Agent       │
│    - Token 包含：Principal = "EU-Auditor-Agent#992"           │
│      Scope = ["dpp:read_aggregated", "co2:read_verified"]    │
│                                                              │
│  Step 2: 比對 Scope 對請求資源的合法性                         │
│    - 請求目標：DPP 護照碳足跡資料 ✅ 在授權範圍內               │
│                                                              │
│  Step 3: 讀取後端 ERP 完整資料（含機密）                       │
│    - 從 SAP HANA 取出完整記錄（此階段資料仍在伺服器記憶體中）   │
│                                                              │
│  Step 4: 帶內欄位過濾（商業機密永不離開伺服器）                 │
│    - wafer_baking_temp:   "[REDACTED_BY_DROS_POLICY]"        │
│    - raw_bom_formula:     "[REDACTED_BY_DROS_POLICY]"        │
│    - supplier_unit_cost:  "[REDACTED_BY_DROS_POLICY]"        │
│    - ✅ carbon_total_co2:  "42.5 kg CO2e"  ← 放行             │
│    - ✅ eu_cbam_cert_id:   "CBAM-2026-TW-991" ← 放行          │
│                                                              │
│  Step 5: 對已過濾資料產出 SHA-256 Merkle 稽核憑證              │
│    - 每一筆放行與過濾決策都記錄在帶前後 Hash 鏈結的稽核鏈中     │
└──────────────────────────────────────────────────────────────┘
        │
        │  回傳已過濾、帶密碼學簽章的 DPP 合規回應
        ▼
歐盟稽核 AI Agent 收到：
  ✅ 碳足跡數據（合規通關）
  🚫 商業機密配方（永不傳出）
```

### 🚨 越權行為的即時熔斷機制

```
場景：攻擊者誘導 Agent 嘗試讀取原始 BOM 配方

  Agent 呼叫 Tool: export_raw_bom(product_id="CHIP-A1")
                    ↓
  【VEP Policy Gate 26.1μs 決策】
    - 比對 Scope：EU-Auditor-Agent#992 的 Scope 中不含 "bom:read_raw"
    - 判定：PROHIBITED_SCOPE_VIOLATION
                    ↓
  硬性熔斷：API 呼叫在二進位層直接切斷
  Agent 收到：403 FORBIDDEN + 稽核告警寫入 Merkle 鏈
                    ↓
  若為高風險行為（如嘗試 export 整個資料庫）：
  → VEP 升級為 HITL 懸停模式
  → 廠長控制台即時彈出雙重確認視窗
  → 廠長拒絕 → Agent 授權立即撤銷
```

---

## 三、 DROS-VEP 之 6 大信任要點精確對應解法 (6 Pillars Alignment)

| 信任要素 | 對應的 DROS 機制 | 機制運作說明（技術細節） |
| :--- | :--- | :--- |
| **1. Principal (身份：代表誰)** | **DIT Token 帶內身份注入** | Agent 啟動時自動注入加密 JWT 憑證（非由 Agent 自行聲稱身份）。憑證內含 Principal Hash：`EU-Auditor-Agent#992` 與非對稱簽章，偽造與竄改在加密層被拒絕。 |
| **2. Authorization (授權範圍)** | **Scope 宣告式權限矩陣** | 以 `vajra_policy.yaml` 靜態宣告 `PERMIT: dpp:read_aggregated_co2`、`PROHIBITED: bom:read_raw`。Scope 在編譯期解析為二進位查表，執行期零正則運算開銷。 |
| **3. Tool/Action Bound (行動邊界)** | **VEP Interceptor 二進位帶內攔截** | 所有 Tool Call 在呼叫棧層面經過 C-ABI 網關。攔截發生在 Python/Go SDK 的 FFI 邊界，AI 的文字輸出與語意推理無法影響此物理層的決策。 |
| **4. Policy Gate (資料過濾閘門)** | **Zero-Knowledge 欄位動態遮蔽** | 後端資料庫完整記錄在記憶體中被讀取，但在 TCP 封包組裝前，商業機密欄位在記憶體中被覆寫替換。攻擊者即使攔截網路封包也只看到 `[REDACTED]`。 |
| **5. Audit Log (不可竄改稽核)** | **SHA-256 Merkle 雜湊鏈** | 每筆決策記錄包含：時間戳、決策類型、前筆 Hash、本筆 Hash。任何試圖刪除或修改歷史記錄的動作都會使後續所有 Hash 失效，篡改立即可被偵測。 |
| **6. Revocation (動態撤銷)** | **$O(1)$ RCU Token 秒級註銷** | 廠長點擊撤銷後，Token 在一個讀寫鎖交換操作（RCU，Read-Copy-Update）內完成廢止。後續 Agent 的任何 API 請求皆立即收到 `403 FORBIDDEN`，整體延遲 < 1 秒。 |

---

## 四、 評審 1 分鐘極速導覽演練場景對照 (Demo Scene Script)

在 Track 01 展演控制台中，點擊頂部 **`🎬 評審 1 分鐘極速視覺演練`** 可依序展演：

**場景 1 ── 合規查詢：Agent 讀取碳足跡，商業機密自動過濾**
> Agent A（歐盟稽核代理）查詢供應商晶片 DPP 碳足跡。DIT Token 驗證通過，Scope 符合。系統在帶內過濾 BOM 配方，安全放行傳回 `42.5 kg CO2e` 摘要與 CBAM 合規證明。

**場景 2 ── 越權試探：Agent 嘗試導出原始配方，Policy Gate 熔斷**
> Agent A 受到 Prompt Injection 誘導，嘗試呼叫 `export_raw_bom()` 工具。VEP 在 26.1μs 內比對 Scope 不合，硬性熔斷請求，同步觸發廠長控制台 HITL 雙重確認視窗。

**場景 3 ── 緊急撤銷：廠長一鍵撤銷 Agent 授權**
> 廠長在控制台點擊「撤銷授權」，RCU Token 在 < 1 秒內廢止。Agent A 隨後的所有 API 呼叫一律收到 `403 FORBIDDEN`，授權即時終止。

**場景 4 ── 密碼學稽核：出示可獨立驗證的 Merkle 決策憑證**
> 點擊任一 Audit Log 條目，展示 SHA-256 Merkle Hash 鏈結憑證。評審可自行計算雜湊值驗證記錄未被篡改，展示密碼學可信度。

---

## 五、 技術定位：DROS 在現有安全技術棧中的角色 (Competitive Positioning)

> 📌 **給技術評審的定位說明**：DROS 不是既有安全工具的替代方案，而是一個新類別──**AI Agent 執行期治理 (AI Agent Runtime Governance)**。以下對比說明各技術的防禦層次與能力範圍，以利準確評估。

| 能力維度 | Intel TDX / Confidential VM | Data Clean Room | API Gateway | **DROS VEP** |
| :--- | :---: | :---: | :---: | :---: |
| **防禦層次** | 基礎設施層（防雲端廠商） | 資料協作層（批次聚合） | 網路閘道層（流量控制） | **AI Agent 執行期層（應用行為治理）** |
| 防止雲端廠商 / Hypervisor 窺視 | ✅ 強（TEE 記憶體加密） | ✅ 中 | ❌ | ❌（非設計目標） |
| **欄位級動態 Policy 遮蔽（即時 API 回應）** | ❌ 無欄位層概念 | ⚠️ 部分（批次聚合，非即時） | ⚠️ 部分（靜態規則，無 AI 語意感知） | ✅ **帶內 26.1μs 決策** |
| **AI Agent Tool Call 越權行為治理** | ❌ | ❌ | ❌ | ✅ **C-ABI 物理熔斷** |
| **即時輸出密碼學簽章合規憑證（DPP）** | ❌ | ❌ | ❌ | ✅ **SHA-256 Merkle 簽章** |
| 不可竄改稽核鏈（可獨立驗證） | ⚠️ 部分（TEE Attestation） | ❌ | ❌ | ✅ **完整 Merkle Chain** |
| Human-in-the-Loop 高風險動作懸停 | ❌ | ❌ | ❌ | ✅ **HITL 雙重簽署** |
| 秒級 Token 動態撤銷 | ❌ | ❌ | ⚠️ 部分（需重新部署） | ✅ **O(1) RCU 原子交換** |

### 📌 互補關係宣告（重要）

**Confidential Computing（Intel TDX / Azure Confidential VM）與 DROS 為互補而非競爭關係。**

- **Confidential Computing 的防禦目標**：防止雲端廠商、惡意系統管理員或受損 Hypervisor 從基礎設施層窺視 TEE 記憶體中的程式碼與資料。
- **DROS 的防禦目標**：防止 AI Agent 在應用執行期內越權行為（Prompt Injection、Tool Call 越界、語意幻覺洩密）。
- **部署建議**：兩者可同時部署，實現縱深防禦（Defense in Depth）。

**對本題（ESPR DPP 合規）的精確定位：**

> 歐盟稽核員發出的 DPP 查詢請求，其威脅模型是「AI Agent 被操控後，在應用層洩漏 BOM 商業機密」──這正是 DROS 帶內欄位遮蔽所針對的攻擊面。Confidential Computing 防護的是「雲端廠商窺視 ERP 伺服器記憶體」，屬於不同攻擊面。Data Clean Room 適用於多方離線批次資料協作，無法處理即時 API 回應的欄位動態遮蔽。

---

## 六、 10 秒極速可重現命令 (Zero-Dependency Verification)

```bash
# 1. 執行 TDD 單元測試 (0.005 秒驗證 Track 01 5 大斷言)
python test_verification_suite.py

# 2. 開啟 Track 01 專屬獨立 VEP 控制台
python server.py
# 瀏覽器存取: http://localhost:8000/track01_carbon_dpp/index.html
```

---

*專利聲明：DROS 執行治理與安全技術已申請美國臨時專利保護（U.S. Provisional Patent Application No. 64/111,973）。*  
*© 2026 OpenShip Ecosystem. All Rights Reserved.*
