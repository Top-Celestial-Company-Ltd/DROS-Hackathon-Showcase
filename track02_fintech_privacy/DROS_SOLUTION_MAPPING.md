# Track 02 專屬：DROS-VEP 解決方案對應說明書 (Fintech & Payment Privacy)

> **主題**：電商與第三方支付 ── 隱私保護下的可疑行為偵測  
> **核心技術內核**：DROS-VEP Lite (Deterministic Behavioral Vector Gate & $O(1)$ Token Freezing)

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

## 一、 題目缺口與現實產業痛點 (Governance Gap & Industry Context)

### 🏦 產業背景：KYC 之後的治理真空

電商支付詐欺的最棘手之處，在於 **人頭帳戶（Mule Accounts）與帳戶盜用（ATO）幾乎都發生在已通過 KYC 驗證的「正常帳戶」上**。傳統防詐手段在 KYC 核身之後便幾乎失去武器：

```
傳統支付安全的防線：

  開戶審核（KYC）         交易後監控（事後）
      ✅ 嚴格審查          ⚠️ 只能事後發現
         │                     │
  ─────────────────────────────────────────→ 時間
                │
          ❌ 治理真空期
      帳戶已通過 KYC，
    但 AI Agent 在此期間
    可以自由讀取客戶明細、
    無限制地發起 API 呼叫，
    且沒有任何「執行期管束」
```

### 🔴 三個核心矛盾

**矛盾 1：要偵測洗錢，但又不能碰客戶個資**

> 跨機構聯防洗錢需要分析「這個帳戶近期的轉帳對象與頻率」，但此類資料涉及他人個資。直接傳入 AI 模型即違反 GDPR（最高罰款：全球營業額 4% 或 2,000 萬歐元，取高者）與台灣個資法。

**矛盾 2：風控 AI Agent 的行為無法被信任**

> 假設我們授權一個「風控 AI Agent」分析可疑帳戶。但這個 Agent 如果被攻擊者透過 Prompt Injection 操控，它可能會：
> - 自行呼叫 `get_customer_full_profile()` 讀取完整個資
> - 自行觸發 `transfer()` 函式將資金轉至攻擊者帳戶
> - 傳統系統對此完全沒有防禦能力

**矛盾 3：現有隱私技術（聯邦學習、同態加密）無法治理 Agent 的動態行為**

> 聯邦學習確保訓練資料不離開各機構，同態加密保護靜態資料存取。但這些技術回答不了：
> - 「這個 Agent 被授權讀取哪些特徵向量？」
> - 「它觸發了哪些動作？這些動作何時到期？」
> - 「如果偵測到異常，能在 1 秒內撤銷它的全部授權嗎？」

### ❌ 傳統解法的致命缺陷

| 傳統解法 | 看起來能解決... | 實際致命缺陷 |
| :--- | :--- | :--- |
| 靜態規則引擎（人工設定閾值） | 攔截已知洗錢模式 | 無法即時適應新型人頭分散手法；規則更新需人工介入 |
| 直接丟原始交易明細給 AI 模型 | 高精度洗錢偵測 | 違反 GDPR、個資法，一次違規罰款遠超模型帶來的效益 |
| 只做 API Gateway 流量控制 | 阻止高頻 API 濫用 | 無法區分「合法高頻風控查詢」與「惡意洗錢特徵掃描」 |
| LLM Prompt 警告（「請勿讀取個資」） | 軟性提醒 AI | Prompt Injection 攻擊可完全繞過文字層防禦 |

---

## 二、 DROS-VEP 解法：帶內行為向量閘門架構

### 🔧 核心解法：在帶內將原始交易明細轉換為去識別化行為特徵向量，風控 AI 零接觸個資

```
支付系統 / 外部風控 Agent 發出查詢
        │
        │  HTTP POST /api/v1/risk/analyze
        │  Body: { "account_token": "TOK-9982-HASHED", "window_seconds": 180 }
        ▼
┌──────────────────────────────────────────────────────────────┐
│  【DROS VEP Policy Gate】── 帶內行為向量攔截點                │
│                                                              │
│  Step 1: 驗證 DIT Token                                      │
│    - 解析 X-DIT-Token 標頭，確認請求來自授權的風控 Agent       │
│    - Token 包含：Principal = "Fintech-Risk-Agent#402"        │
│      Scope = ["risk:analyze_vector", "account:read_stats"]  │
│    - 確認不含 "account:read_pii"（個資讀取）                  │
│      確認不含 "payment:execute"（支付執行）                   │
│                                                              │
│  Step 2: 從核心帳務系統讀取完整記錄（仍在記憶體中）            │
│    - 取出：user.name, user.ssn, card_number, 交易明細 × 248  │
│                                                              │
│  Step 3: 帶內去識別化 → 只計算統計行為特徵，丟棄個資          │
│    - user.name → 丟棄（不進入 AI 輸入）                      │
│    - user.ssn  → 丟棄（不進入 AI 輸入）                      │
│    - card_number → 丟棄（不進入 AI 輸入）                    │
│    - 保留計算：                                               │
│      ✅ tx_frequency_3min = 24（3 分鐘內交易次數）            │
│      ✅ fan_out_node_count = 20（不同收款帳戶數）             │
│      ✅ amount_variance = 0.02（金額方差，趨近 0 = 分拆特徵） │
│                                                              │
│  Step 4: 將行為向量送入風控邏輯，取得風險分數                  │
│    - anomaly_score = 0.94（高風險：3 分鐘內分散轉出至 20 個  │
│      帳戶，每筆金額近乎一致 → 人頭洗錢特徵）                   │
│                                                              │
│  Step 5: 依分數決定 Policy Action                             │
│    - 0.94 > 閾值 0.8 → 觸發 INTERCEPT_AND_SUSPEND            │
│    - 支付 Token 進入 HITL 懸停，等待風控中心二階確認           │
│    - 所有決策寫入 SHA-256 Merkle 稽核鏈                       │
└──────────────────────────────────────────────────────────────┘
        │
        │  回傳已去識別化的行為向量分析結果
        ▼
風控 AI Agent 收到：
  ✅ 行為向量與風險分數（可操作）
  🚫 客戶姓名、身份證、信用卡號（永不傳出）
```

### 🚨 $O(1)$ 常數時間 Token 凍結機制（為何能 < 1 秒凍結？）

傳統凍卡需要查詢資料庫、通知各微服務，往往耗時數秒甚至分鐘。DROS 採用 **RCU（Read-Copy-Update）** 記憶體指針交換技術：

```
凍結前：
  VEP 閘門 → [Token_Registry_Pointer] → [有效 Token 表]
                                            ↑
                                   包含 "TOK-9982-HASHED" = ACTIVE

風控中心點擊「一鍵凍結」：
  1. 在記憶體中複製一份新的 Token 表
  2. 在新表中將 "TOK-9982-HASHED" 標記為 FROZEN
  3. 原子性（Atomic）交換指針 ← 此步驟耗時 < 1 微秒

凍結後：
  VEP 閘門 → [Token_Registry_Pointer] → [新 Token 表]
                                            ↑
                                   "TOK-9982-HASHED" = FROZEN

效果：所有正在執行的 Agent API 請求，
      在下一次 VEP 閘門檢查時（26.1μs 內）
      立即收到 403 FORBIDDEN
```

---

## 三、 DROS-VEP 之 6 大信任要點精確對應解法 (6 Pillars Alignment)

| 信任要素 | 對應的 DROS 機制 | 機制運作說明（技術細節） |
| :--- | :--- | :--- |
| **1. Principal (身份：代表誰)** | **DIT Token 帶內身份注入** | 風控 Agent 啟動時自動注入加密身份憑證。憑證內含 `Fintech-Risk-Agent#402` 與 KYC 帳戶關聯 Hash，確保風控主體可合規追溯且不可偽造。 |
| **2. Authorization (授權範圍)** | **Scope 宣告式隱私特徵授權矩陣** | `vajra_policy.yaml` 明確宣告 `PERMIT: risk:analyze_vector`（行為向量分析）、`PROHIBITED: account:read_pii`（原始個資）、`PROHIBITED: payment:execute`（直接觸發支付）。Scope 矩陣在二進位層查表，無法被語意繞過。 |
| **3. Tool/Action Bound (行動邊界)** | **VEP Interceptor 二進位帶內攔截** | 風控 Agent 在呼叫棧層面被限制只能執行 `analyze_behavior_vector()`。任何嘗試呼叫 `get_customer_profile()`、`execute_transfer()` 等工具的請求，在 FFI 二進位邊界 26.1μs 內被硬性熔斷。AI 的語意推理完全無法繞過此物理層。 |
| **4. Policy Gate (資料過濾閘門)** | **行為向量帶內去識別化轉換** | 原始帳務記錄在伺服器記憶體中被讀取，帶內計算行為統計特徵（頻率、方差、分散度），個資欄位在記憶體中被覆寫後才允許向外傳輸。風控 AI 的輸入資料中從不存在個資。 |
| **5. Audit Log (不可竄改稽核)** | **SHA-256 Merkle 雜湊鏈** | 每次風控掃描、HITL 掛起、Token 凍結決策均寫入 Merkle 鏈。各筆記錄包含前筆 Hash，任何篡改使後續所有 Hash 失效。監管機構可獨立計算雜湊值驗證稽核完整性。 |
| **6. Revocation (動態撤銷)** | **$O(1)$ RCU 常數時間 Token 凍結** | 風控中心點擊「凍結」後，透過 RCU 原子指針交換完成 Token 廢止，整體延遲 < 1 秒。後續所有支付 API 請求一律回傳 `403 FORBIDDEN`，無論 Agent 正在執行哪個步驟。 |

---

## 四、 評審 1 分鐘極速導覽演練場景對照 (Demo Scene Script)

在 Track 02 展演控制台中，點擊頂部 **`🎬 評審 1 分鐘極速視覺演練`** 可依序展演：

**場景 1 ── 合規查詢：風控 Agent 讀取去識別化行為向量，個資零接觸**
> 風控 Agent（`Fintech-Risk-Agent#402`）發送風險分析請求。VEP 在帶內完成去識別化轉換，僅向 Agent 回傳行為向量（頻率=3/分、分散度=0.02）。風險分數 0.12，無異常。整個過程中客戶姓名、身份證、信用卡號均未離開伺服器。

**場景 2 ── 洗錢特徵偵測：高風險行為觸發 HITL 交易掛起**
> 系統偵測到同一帳戶 3 分鐘內向 20 個收款帳戶分散轉出，每筆金額近乎一致（方差 0.02），風險分數 0.94。VEP Policy Gate 即時掛起所有待處理支付，風控中心控制台彈出 HITL 二階確認視窗，需人工簽署才能放行或拒絕。

**場景 3 ── 緊急凍結：風控中心一鍵凍結支付 Token**
> 風控中心點擊「一鍵凍結」，$O(1)$ RCU 機制在 < 1 秒內完成 Token 廢止。風控 Agent 的後續所有支付 API 呼叫立即收到 `403 FORBIDDEN`，帳戶進入防護模式。

**場景 4 ── 密碼學稽核：出示可獨立驗證的 Merkle 決策憑證**
> 點擊任一 Audit Log 條目，展示 SHA-256 Merkle Hash 鏈結憑證（包含 HITL 掛起決策與 Token 凍結記錄）。監管機構可自行計算雜湊值驗證記錄完整性，符合 GDPR Article 5(f) 完整性與保密性要求。

---

## 五、 技術定位：DROS 在現有安全技術棧中的角色 (Competitive Positioning)

> 📌 **給技術評審的定位說明**：DROS 不是既有安全工具的替代方案，而是一個新類別──**AI Agent 執行期治理 (AI Agent Runtime Governance)**。以下對比說明各技術的防禦層次與能力範圍。

| 能力維度 | Intel TDX / Confidential VM | Data Clean Room | API Gateway | **DROS VEP** |
| :--- | :---: | :---: | :---: | :---: |
| **防禦層次** | 基礎設施層（防雲端廠商） | 資料協作層（批次聚合） | 網路閘道層（流量控制） | **AI Agent 執行期層（應用行為治理）** |
| 防止雲端廠商 / Hypervisor 窺視 | ✅ 強（TEE 記憶體加密） | ✅ 中 | ❌ | ❌（非設計目標） |
| **欄位級動態 Policy 遮蔽 – 即時去識別化轉換** | ❌ 無欄位層概念 | ⚠️ 部分（批次聚合，非即時） | ⚠️ 部分（靜態規則，無 AI 語意感知） | ✅ **帶內 26.1μs 動態轉換** |
| **AI Agent 骏入 / 越權 Tool Call 治理** | ❌ | ❌ | ❌ | ✅ **C-ABI 物理熔斷** |
| **不可竄改風控稽核鏈（監管機構可獨立驗證）** | ⚠️ 部分（TEE Attestation） | ❌ | ❌ | ✅ **SHA-256 Merkle Chain** |
| Human-in-the-Loop 高風險轉帳懸停 | ❌ | ❌ | ❌ | ✅ **HITL 雙重簽署** |
| **O(1) 秒級 Payment Token 凍結** | ❌ | ❌ | ⚠️ 部分（需重新部署） | ✅ **RCU 原子交換** |

### 📌 互補關係宣告（重要）

**Confidential Computing（Intel TDX / Azure Confidential VM）與 DROS 為互補而非競爭關係。**

- **Confidential Computing 的防禦目標**：防止雲端廠商或 Hypervisor 從基礎設施層窺視 TEE 記憶體中的程式碼與資料。
- **DROS 的防禦目標**：防止 AI 風控 Agent 在應用執行期越權讀取客戶個資、娪數豐寮起支付 Token 或褒入語意誘騙。
- **部署建議**：兩者可同時部署，實現縱深防禦（Defense in Depth）。

**Data Clean Room 的對比說明：**

> Data Clean Room（如 Google PAIR、AWS Clean Rooms）的設計目的是「兩個機構想分析共同客戶，但不希望對方看到自己的詳細清單」──批次離線資料協作工具。它無法用於「即時 API 回應中的欄位動態去識別化」。對於本題所需的「風控 Agent 即時導出去識別化行為特徵向量」與「支付 Token O(1) 凍結」，屬於不同層次的方案。

---

## 六、 10 秒極速可重現命令 (Zero-Dependency Verification)

```bash
# 1. 執行 TDD 單元測試 (0.005 秒驗證 Track 02 5 大斷言)
python test_verification_suite.py

# 2. 開啟 Track 02 專屬獨立 VEP 控制台
python server.py
# 瀏覽器存取: http://localhost:8000/track02_fintech_privacy/index.html
```

---

*專利聲明：DROS 執行治理與安全技術已申請美國臨時專利保護（U.S. Provisional Patent Application No. 64/111,973）。*  
*© 2026 OpenShip Ecosystem. All Rights Reserved.*
