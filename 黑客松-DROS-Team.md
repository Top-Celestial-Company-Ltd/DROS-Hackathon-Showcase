# 黑客松團隊與方案介紹：DROS 團隊 (Top-Celestial Company Ltd.)

---

## 一、 團隊基本資訊與分工 (Team Roster & Responsibilities)

| 姓名 | 學歷與現職 | 團隊角色與分工 |
| :--- | :--- | :--- |
| **陳濬程 (Chun-Cheng (Jimmy) Chen)** | 德州大學 UTA EMBA / 政治大學經濟系<br>**Top-Celestial Company Ltd. (康宸園有限公司) 創辦人** | **團隊代表 / 核心技術平台架構師 / AI 協作**<br>• DROS (Deterministic Runtime Operating System) 創作者<br>• DROS-VajraClaw 微內核與 C-ABI 帶內攔截器研發<br>• U.S. PPA No. 64/111,973 發明人與學術論文作者 |
| **溫韋程** | 政治大學經濟系<br>**金融 / 保險產業專業經理人** | **金融與保險資安顧問 / AI 協作**<br>• Track 02 (Fintech AML) 與 Track 03 (HIPAA 醫療保險) 業務情境設計<br>• 金融跨機構隱私與洗錢聯防合規邊界規劃 |
| **楊英宗** | 政治大學經濟系<br>**產業 / 政府標案專案經理人** | **公部門與產業行政程序顧問 / AI 協作**<br>• Track 04 (政府代理服務) 與 Track 06 (RBA 供應鏈) 行政流程設計<br>• 跨機關憑證代查、代送件與本人授權三層控制矩陣規劃 |

---

## 二、 團隊相關經驗 (Team Relevant Experience)

1. **頂尖 AI Agent 執行期治理架構研發**：
   - 創立 **DROS (Deterministic Runtime Operating System)**，專注於解決自主 AI Agent 進入企業時的「執行期失控與資安漏洞」問題。
   - 研發 **DROS-VajraClaw** 開源邊界防線網關，實現帶內 26.1 微秒（$\mu\text{s}$）確定性物理層硬熔斷。
2. **堅實的專利與學術成果**：
   - 已申請美國臨時發明專利：**U.S. Provisional Patent Application No. 64/111,973**（*Patent Pending*）。
   - 在國際學術預印本庫（Zenodo / IEEE 樣式）發表 7 篇核心技術論文，涵蓋 C-ABI 帶內攔截、Merkle 稽核鏈、$O(1)$ RCU 動態撤銷、RedTeam 測試大腦與 **DROS-6P 大一統六大信任要點治理架構**。
3. **產業與公部門領域知識沉澱**：
   - 團隊成員橫跨 AI 系統架構、金融保險資安與政府標案行政實務，能將抽象的安全技術精確落地至真實商業與公部門場景。

---

## 三、 為什麼 DROS 適合解決這個問題？ (Why DROS is Uniquely Qualified)

### 3.1 核心痛點：Agentic Era 治理的現實基本門檻（速度與全覆蓋）

進入 Agentic Era，任何一個 AI Agent 都能在 1 秒內發起成千上萬次 Syscall 與 Tool Call。屆時企業面臨的現實是：內部/外來/惡意 Agent 所產生的 Syscall 數量呈爆發性成長。**如果治理系統本身的處理延遲不在微秒級（Microseconds）水位，治理系統本身就會被巨量 Agent 的請求打崩（自我 DDoS 崩潰）**。

傳統資安工具（IAM、Prompt Guardrails、SIEM）各據一方卻碎片化，**沒有任何一套傳統工具能同時閉環回答大會提出的六大信任問題**。

### 3.2 DROS 6 大信任要點閉環 (The 6 Pillars Universal Closure)

DROS 能夠在單一物理層 Runtime 內，以 **26.1 微秒（$\mu\text{s}$）決策延遲** 100% 閉環解答六大信任要點：

```
                              [ DROS 雙向 Multi-VEP 對接聯防架構 ]
                                               │
 ┌─────────────────────────────────────────────┼─────────────────────────────────────────────┐
 │                                             │                                             │
 ▼                                             ▼                                             ▼
┌───────────────────────────┐      ┌───────────────────────────┐      ┌───────────────────────────┐
│ 1️⃣ Principal (代表誰)       │      │ 2️⃣ Authorization (授權)   │      │ 3️⃣ Tool/Action (工具邊界) │
│ DIT Token (PKI 3-Tier)    │      │ Capability Bitmap 向量    │      │ C-ABI FFI 帶內攔截器      │
│ • 強綁定法人/團隊/公民    │      │ • 精確角色與 API 映射     │      │ • 26.1 μs 物理層熔斷      │
└─────────────┬─────────────┘      └─────────────┬─────────────┘      └─────────────┬─────────────┘
              │                                  │                                  │
 ─────────────┼──────────────────────────────────┼──────────────────────────────────┼─────────────
              │                                  │                                  │
 ▼            ▼                                  ▼                                  ▼
┌───────────────────────────┐      ┌───────────────────────────┐      ┌───────────────────────────┐
│ 4️⃣ Policy Gate (過濾門閥) │      │ 5️⃣ Audit Log (稽核追溯)   │      │ 6️⃣ Revocation (動態撤銷)  │
│ 遮蔽 / HITL / ZKP-Lite    │      │ SHA-256 Merkle 雜湊鏈     │      │ O(1) RCU 原子指針切換     │
│ • 機密遮蔽與雙簽懸停      │      │ • 法院採信之憑證 (Cert)   │      │ • 秒級 403 硬性阻斷       │
└───────────────────────────┘      └───────────────────────────┘      └───────────────────────────┘
```

1. **1️⃣ Principal (代表誰) ── DIT (Dros Identity Token)**
   - **三階動態 PKI 簽章 (3-Tier Dynamic PKI)**：當 Agent 被啟動或接收命令時，DROS 會在其 Request Header 帶內注入非對稱加密簽章之 DIT 憑證。此憑證由根 CA、企業端 VEP 網關與 Agent 實體三層密碼學簽署。
   - **執行期動態上下文綁定**：DIT 不僅包含「Agent 身份」，更綁定「委託人 (Principal) 身份、呼叫 Session ID、允許之 Scope 陣列與過期時間戳」。
   - **不可偽造性**：DIT Token 作用於二進位通訊標頭層，LLM 模型的文字生成層完全無權接觸或修改該 Token，杜絕了 Prompt 層面的身分偽造（Impersonation Attack）。

2. **2️⃣ Authorization (授權範圍) ── Capability Bitmap (能力位元圖)**
   - **暫存器層級位元映射 (Register-Level Bitmasking)**：在 VEP 網關加載政策時，系統會將數百種 API 方法與工具權限映射為二進位位元圖（Capability Bitmap）。例如 `Bit 0` 代表 `query_dpp`，`Bit 5` 代表 `execute_payment`。
   - **$O(1)$ 常數時間邏輯位元運算**：當 Agent 發起呼叫時，網關直接在 CPU 暫存器層級執行 `AND` 位元遮罩運算（Bitwise Masking），判定時間低於數納秒（nanoseconds），完全免去文字檔解析、字串比對或 JSON 反序列化開銷。
   - **嚴格的動態 Scope 隔離**：即使 Agent 被注入惡意指令要求呼叫 `execute_payment`，只要其 Capability Bitmap 中對應的位元為 `0`，請求在暫存器比對階段就直接被拒絕。

3. **3️⃣ Tool / Action Bound (工具邊界) ── C-ABI 帶內攔截器 (In-Band C-ABI Interceptor)**
   - **外國函式介面 (FFI) 帶內插樁**：DROS 的攔截點部署於 Agent SDK 呼叫外部 API 的二進位 C-ABI（C Application Binary Interface）邊界，而非外掛的網路代理（Proxy）。
   - **26.1 微秒確定性硬熔斷**：當 Agent 嘗試觸發未授權之工具呼叫（Tool Call）時，C-ABI 攔截器會在 **26.1 微秒（$\mu\text{s}$）內** 直接丟棄該呼叫，並向 Agent SDK 傳回確定性硬錯誤（Hard Error）。
   - **物理層隔離與串鏈阻斷**：此阻斷發生於記憶體分配與 Socket 傳送之前。即使黑客試圖透過「工具串鏈（Tool Chaining）」繞過防線，未經授權的下步呼叫依然會被 C-ABI 帶內熔斷硬性截斷。

4. **4️⃣ Policy Gate (過濾門閥) ── 資料遮蔽、HITL 與 ZKP-Lite 選擇性揭露**
   - **帶內動態資料去識別化 (In-Band Dynamic Redaction)**：API 回傳 Payload 在離開伺服器記憶體前，Policy Gate 會依據 DIT 權限自動進行欄位遮蔽，將敏感欄位物理覆寫為 `[REDACTED_BY_VEP]`，僅放行合規摘要。
   - **異步狀態懸停與雙重簽署 (HITL Suspension)**：針對高風險 API 呼叫，Policy Gate 會自動將交易掛起（Suspend）至安全佇列，並向 Principal 的手機端 App 推送 2FA 授權通知（設有 300 秒逾時機制），經真人簽署後方可解凍執行。
   - **ZKP-Lite 零知識證明閘門 (Groth16 Selective Disclosure)**：採用輕量化 Groth16 零知識證明演算法。系統能在**不傳遞任何原始敏感數據（如真實稽核分數或成本數字）的前提下**，向第三方驗證 Agent 輸出密碼學證明 $\pi$，證明「該數據 100% 符合法規門檻」，實現真正的選擇性揭露（Selective Disclosure）。

5. **5️⃣ Audit Log (稽核追溯) ── SHA-256 Merkle Hash Chain (防篡改密碼學稽核鏈)**
   - **密碼學前後鏈結 (Cryptographic Hash Linking)**：每次 Agent 發起請求、VEP 決策（放行、熔斷、遮蔽、懸停）與 API 回應，均會生成包含微秒級時間戳、Principal 身份與動作特徵的資料塊，並與前一筆紀錄的 Hash 進行 SHA-256 雙重雜湊。
   - **Merkle Root 樹狀錨定**：系統自動將歷史對決雜湊建構成 Merkle Tree，並定期將 Merkle Root 簽章錨定至不可竄改日誌中。
   - **獨立憑證出示 (Court-Admissible Cert Modal)**：點擊控制台上的任一日誌，可即時出示包含 Ed25519 簽章與 Merkle 驗證路徑的密碼學憑證（Certificate）。任何針對歷史日誌的單字竄改，都會導致整條雜湊鏈與 Merkle Root 驗證崩潰。

6. **6️⃣ Expiry / Revocation (動態撤銷) ── $O(1)$ RCU 常數時間指針切換**
   - **RCU（Read-Copy-Update）記憶體原子交換**：DROS 在共享記憶體層級實作 RCU 技術。管理員或資安系統發出「一鍵凍結 / 撤銷」指令時，系統直接在 CPU 暫存器層級執行 **原子指針切換 (Atomic Pointer Swap)**。
   - **$< 1$ 微秒記憶體切斷**：Token 指針會在 **$< 1\ \mu\text{s}$（微秒）內** 被原子覆寫為無效/空指針。
   - **零過期視窗 (Zero Stale-Session Window)**：指針切換後，後續所有來自該 Agent 的 API 請求，在下一個 $26.1\ \mu\text{s}$ 的 Pass 中一律傳回 `HTTP 403 FORBIDDEN`，整體撤銷在 1 秒之內於全網關 100% 生效，不留任何時間差漏洞。

---

### 3.3 升級架構：Multi-VEP 雙向對接 Zero-Trust Mesh (Multi-VEP Inter-Gate Protocol)

在現實的真實跨機構場景中，**根本不可能只有單一 VEP 網關獨裁**。每個機構/企業只會信任部署在自家內網邊界的 VEP。

DROS 支援 **Multi-VEP Peer-to-Peer 雙向對接**：
```
┌────────────────────────────────┐         跨機構安全邊界 (Zero-Trust Link)         ┌────────────────────────────────┐
│   甲機構 / 買方 / 醫院端 VEP    │ ───────────────────────────────────────────────► │   乙機構 / 賣方 / 保險端 VEP    │
│  (VEP-1: did:dros:requester)   │ ◄─────────────────────────────────────────────── │ (VEP-2: did:dros:responder)   │
└────────────────────────────────┘      帶內 Cryptographic Handshake (26.1μs)       └────────────────────────────────┘
```
- **雙端聯防**：攔截不是在單一節點發生，而是由請求端 VEP-1 與回應端 VEP-2 共同執行獨立的政策檢查（Policy Check）。
- **零信任穿透**：甲機構的 Agent 只能存取乙機構允許的去識別化數據或 ZKP 證明，完全無法穿透乙機構 VEP-2 的物理防線讀取原始資料庫。

---

## 四、 現有資安技術棧與 DROS 之定位對比 (Competitive Positioning)

DROS 不是既有資安工具的替代品，而是 **AI Agent 執行期治理 (AI Agent Runtime Governance)** 的新類別開創者：

| 能力維度 | Intel TDX / Confidential VM | Data Clean Room | API Gateway / WAF | Prompt Guardrails | **DROS Multi-VEP** |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **防禦層次** | 基礎設施層（防雲端廠商） | 資料協作層（批次） | 網路閘道層（流量） | 文字 Prompt 層 | **Agent 執行期層 (物理邊界)** |
| **防雲端廠商/Hypervisor** | ✅ 強 (TEE 記憶體加密) | ✅ 中 | ❌ | ❌ | ❌ (非設計目標，可互補) |
| **欄位級動態 Policy 遮蔽** | ❌ 無欄位概念 | ⚠️ 批次非即時 | ⚠️ 靜態無語意感知 | ⚠️ 僅文字替換 | **✅ 帶內 26.1μs 決策** |
| **Tool Call 越權硬熔斷** | ❌ | ❌ | ❌ | ❌ (Prompt 可繞過) | **✅ C-ABI 物理硬熔斷** |
| **ZKP 選擇性揭露** | ❌ | ❌ | ❌ | ❌ | **✅ ZKP-Lite (Groth16)** |
| **不可竄改稽核鏈** | ⚠️ 部分 (TEE Attestation) | ❌ | ❌ | ❌ | **✅ SHA-256 Merkle Chain** |
| **Human-in-the-Loop 懸停** | ❌ | ❌ | ❌ | ❌ | **✅ HITL 異步雙簽** |
| **秒級 Token 動態撤銷** | ❌ | ❌ | ⚠️ 需重新部署 | ❌ | **✅ $O(1)$ RCU 原子切換** |

> **💡 互補關係說明**：Confidential Computing（如 Intel TDX）防的是「惡意雲端廠商/Hypervisor」；DROS 防的是「AI Agent 在執行期內的越權行為、Prompt 注入與語意外洩」。兩者可 simultaneous 部署，達成真正的縱深防禦（Defense in Depth）。

---

## 五、 全賽道 (5+1 題) DROS 確定性解法對應地圖 (Solution Mapping Master)

> 🌐 **全棧展示與驗證平台**：`http://localhost:8000/index.html`  
> 🔗 **GitHub 開源展示倉庫**：[https://github.com/Top-Celestial-Company-Ltd/DROS-Hackathon-Showcase](https://github.com/Top-Celestial-Company-Ltd/DROS-Hackathon-Showcase)

| 題目 Track | 題目情境與痛點 | Multi-VEP 雙向對接解法 (P2P Inter-Gate Protocol) | 專屬獨立 VEP 控制台與解法文件 |
| :--- | :--- | :--- | :--- |
| **Track 01** | **製造貿易**：碳足跡與 DPP 數位產品護照資料流控制。採購 Agent 想查碳足跡，但台灣工廠怕 BOM 配方外洩。 | **歐盟買方 VEP-1 ◄► 台灣製造廠 VEP-2**<br>BOM 成本欄位帶內 REDACTED；採購下單觸發 HITL 人工簽署；產出 W3C 可驗證碳護照憑證。 | 🌐 [Alpha 製造 VEP](http://localhost:8000/track01_carbon_dpp/index.html)<br>📄 [Track 01 DROS 解法對應說明書](https://github.com/Top-Celestial-Company-Ltd/DROS-Hackathon-Showcase/blob/main/track01_carbon_dpp/DROS_SOLUTION_MAPPING.md) |
| **Track 02** | **電商與第三方支付**：隱私保護下的可疑行為偵測。第三方支付想聯防洗錢，但電商怕用戶銀行隱私外洩。 | **電商平台 VEP-1 ◄► 核心銀行 VEP-2**<br>銀行帳戶餘額帶內 REDACTED；洗錢風險分數 $>0.85$ 觸發帶內 26.1μs 硬性 BLOCK。 | 🌐 [PayFlow 金融 VEP](http://localhost:8000/track02_fintech_privacy/index.html)<br>📄 [Track 02 DROS 解法對應說明書](https://github.com/Top-Celestial-Company-Ltd/DROS-Hackathon-Showcase/blob/main/track02_fintech_privacy/DROS_SOLUTION_MAPPING.md) |
| **Track 03** | **醫療保險**：跨產業資料合作的誘因與邊界。保險理賠 Agent 想自動核賠，但醫院病歷含高度敏感 PHI。 | **保險理賠 VEP-1 ◄► 醫院 EHR VEP-2**<br>HIPAA 18 項 PHI 欄位帶內動態遮蔽；DIT 驗證病患電子同意書；違規讀病歷 403 阻斷。 | 🌐 [MediGuard 醫療 VEP](http://localhost:8000/track03_healthcare_insurance/index.html)<br>📄 [Track 03 DROS 解法對應說明書](https://github.com/Top-Celestial-Company-Ltd/DROS-Hackathon-Showcase/blob/main/track03_healthcare_insurance/DROS_SOLUTION_MAPPING.md) |
| **Track 04** | **政府服務**：解決憑證碎片化背後的資料孤島。Agent 代辦跨機關申請，如何劃分代查、代送件與本人確認。 | **戶政 VEP-1 ◄► 健保/稅務 VEP-2**<br>三層漸進授權：代查 API (PERMIT 26.1μs)、代送件 (HITL 推播確認)、簽署與跨機關橫移 (DENY)。 | 🌐 [GovProxy VEP](http://localhost:8000/track04_gov_services/index.html)<br>📄 [Track 04 DROS 解法對應說明書](https://github.com/Top-Celestial-Company-Ltd/DROS-Hackathon-Showcase/blob/main/track04_gov_services/DROS_SOLUTION_MAPPING.md) |
| **Track 05** | **普惠金融**：移工數位信任與防詐憑證機制。87 萬移工面臨開戶障礙，亦容易遭冒名與 SIM Swap 盜用。 | **移工 App VEP-1 ◄► 台灣銀行 VEP-2**<br>護照+ARC+勞動許可多文件複合 DIT；三層漸進信任矩陣；SIM Swap 行為異常引發 $O(1)$ 緊急凍結。 | 🌐 [MigraTrust VEP](http://localhost:8000/track05_inclusive_finance/index.html)<br>📄 [Track 05 DROS 解法對應說明書](https://github.com/Top-Celestial-Company-Ltd/DROS-Hackathon-Showcase/blob/main/track05_inclusive_finance/DROS_SOLUTION_MAPPING.md) |
| **Track 06** | **供應鏈貿易金融 (加分題)**：RBA 供應鏈合規可驗證憑證。採購 Agent 需驗證工廠合規，但工廠不能洩露完整稽核報告。 | **買方採購 VEP-1 ◄► 供應商工廠 VEP-2**<br>選擇性揭露閘門 (Selective Disclosure Matrix)；ZKP-Lite (Groth16) 數學驗證分數；W3C VC 2.0 憑證。 | 🌐 [SupplyProof VEP](http://localhost:8000/track06_supply_chain_rba/index.html)<br>📄 [Track 06 DROS 解法對應說明書](https://github.com/Top-Celestial-Company-Ltd/DROS-Hackathon-Showcase/blob/main/track06_supply_chain_rba/DROS_SOLUTION_MAPPING.md) |

---

## 六、 可驗證之客觀測試套件 (Verification Suite & Reproducibility)

作品附帶零依賴、可在一秒內重現之自動化測試腳本：

```bash
# 1. 執行 TDD 自動化單元測試 (驗證 5 大確定性核心斷言)
python test_verification_suite.py
```

**測試結果**：
- `test_01_principal_authorization_permit` ── 授權放行與寫入 Merkle Audit (PASSED)
- `test_02_policy_gate_sensitive_data_redaction` ── BOM/個資帶內遮蔽 (PASSED)
- `test_03_prompt_injection_threat_containment` ── 攻擊 Prompt 帶內阻斷 (PASSED)
- `test_04_instant_token_revocation` ── $O(1)$ RCU 撤銷傳回 403 (PASSED)
- `test_05_audit_log_cryptographic_integrity` ── SHA-256 Merkle 全鏈簽章驗證 (PASSED)

```bash
# 2. 啟動 OpenShip 雲端 Multi-VEP 展示控制台
python server.py
# 開啟瀏覽器存取: http://localhost:8000/index.html
```

---

*專利聲明：DROS 執行治理與安全技術已申請美國臨時專利保護（U.S. Provisional Patent Application No. 64/111,973）。*  
*© 2026 OpenShip Ecosystem & Top-Celestial Company Ltd. All Rights Reserved.*
