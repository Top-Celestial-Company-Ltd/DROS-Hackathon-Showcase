# DROS-VEP Lite 展演總對照說明書 (DROS Solution Mapping Master Overview)



> **全棧產品名稱**：DROS-VEP Lite 確定性 Agent 執行期治理與全棧企業網關  

> **發射部署平台**：OpenShip Multi-VEP Cloud Launchpad (`http://localhost:8000/index.html`)  

> **專利保護標示**：U.S. Provisional Patent Application No. 64/111,973 (Patent Pending)



---



## 🎯 專案核心定位 (Core Mission)



本專案非單純 LLM 應用程式，而是針對 AI Agent 執行期之 **企業級確定性治理與商業部署內核 (VEP Infrastructure)**。透過二進位 C-ABI 與 eBPF 網關帶內防線，提供 **26.1 微秒延遲、零文字檔依賴、$O(1)$ 常數時間動態撤銷與 SHA-256 Merkle 密碼學追溯稽核**。



---



## 零、 DROS 整體機制導讀（DROS 3 大核心組件與帶內防禦）



### 🔍 DROS 是什麼？（全名與核心定義）

**DROS（Deterministic Runtime Operating System，確定性執行期作業系統）** 是一套專門為 AI Agent 執行期所設計的底層治理與行為邊界約束微內核（Kernel Substrate）。

其解決的根本問題是：**「AI Agent 被授權後，誰來管控它實際執行期的行為與 Tool Call？」**

以信用卡舉例：銀行核發信用卡給你（核卡 = 授權），但你每筆消費仍受到「刷卡上限、境外管控、異常交易凍卡」等機制約束（執行期治理）。現在大多數企業的 AI Agent 只有「核卡」，沒有「刷卡管控」。DROS 就是那套執行期管控系統。



---



### 🏗️ DROS 架構的 3 個核心組件

`
┌────────────────────────────────────────────────────────────────────────┐
│                    DROS 三層確定性執行期防禦架構                       │
│                                                                        │
│   【組件 A】DIT Token        【組件 B】VEP Policy Gate     【組件 C】Merkle Audit     │
│   (身分憑證注入層)          (帶內執行期策略閘門層)        (不可竄改稽核追蹤層)       │
│          │                           │                           │             │
│   密碼學強綁定 Agent ID       26.1 μs C-ABI 帶內硬熔斷    SHA-256 密碼學證據鏈       │
│   + 法人/自然人雙軌授權     + HITL 人類雙簽懸停機制     + 法庭採信不可否認性       │
└────────────────────────────────────────────────────────────────────────┘
`

#### 🛡️ 3 大核心組件深入說明：

1. **【組件 A】DIT Token（身份憑證注入層 / Principal Injection）**
   - 每個 AI Agent 啟動時，系統自動注入一組不可偽造的加密身分憑證。
   - 憑證強綁定：**「誰（Agent ID / 法人 vLEI / 自然人 MyData）＋ 被授權做什麼（Scope 位元圖）＋ 到期時間」**。

2. **【組件 B】VEP Policy Gate（帶內執行期策略閘門層 / In-Band Enforcement Gate）**
   - Agent 每次發起 API / Tool 呼叫時，物理上必須先通過此閘門。
   - 閘門在二進位層比對 DIT Token 的 Scope 與本次動作是否吻合：
     - **不吻合** ➔ **26.1 μs 內在 C-ABI 層硬性熔斷**，拋出 HTTP 403 FORBIDDEN，AI 完全無法繞過。
     - **高風險動作** ➔ 自動掛起交易，觸發人類雙重簽署（Human-in-the-Loop）。

3. **【組件 C】Merkle Audit Chain（不可竄改稽核追蹤層 / Cryptographic Audit Trail）**
   - 每次執行決策（放行 / 熔斷 / 掛起）都即時寫入帶有 **SHA-256 雜湊的 Merkle 稽核鏈**。
   - 前後雜湊嚴密鏈結，任何單一節點被竄改都會使整條鏈失效，產出具備法庭採信力的密碼學存證收據。

### ⚡ 為什麼是「帶內 (In-Band)」，而不是「帶外 (Out-of-Band)」？

- **帶外方案（傳統）**：API Gateway / WAF 部署在 AI Agent 外部，Agent 在被攔截之前可能已完成惡意動作，或繞過 Gateway 直接呼叫底層 API。
- **DROS 帶內方案**：VEP Policy Gate 以 C 語言 ABI（二進位介面）嵌入在 Agent 執行時期的函式呼叫鏈中，Agent 在呼叫任何外部 Tool 之前，**物理上必須先通過閘門**，沒有繞過的可能性。

> 💡 **類比理解**：帶外 = 機場 X 光機在出境大廳外面（還沒進機場就可以繞過去）；帶內 = X 光機直接安裝在登機門走廊，完全無法繞過。

---

## 🖥️ 抽象哲學類比：POSIX 與 DROS 的系統治理哲學



> **"POSIX did not eliminate application complexity; it eliminated the need for every application to reinvent the underlying operating-system interface."**  

> 

> **"DROS aims to apply the same abstraction principle to Agent governance: applications should express business intent and policy, while deterministic execution enforcement is provided by a shared substrate."**



DROS 之於 AI Agent，正是採用了相同的**分層抽象與關注點分離哲學**。傳統「Application-first governance」會導致治理複雜度隨應用與框架數量呈乘法級膨脹（$\text{Frameworks} \times \text{Applications} \times \text{Governance}$）；而 DROS 將治理下沉為共享基礎設施，**使治理複雜度不再隨應用程式數量增長 (Governance complexity stops scaling with application count)**：



| 治理維度 | 傳統作業系統 (Linux / POSIX OS) | **DROS 確定性 AI 治理作業系統 (AI Agent OS)** | 核心解決的痛點 |

| :--- | :--- | :--- | :--- |

| **1. 執行主體 (Subject)** | Process PID / User UID | **DIT Token (綁定法人 vLEI / 自然人 MyData)** | 解決「AI 到底是代表誰？出了事誰負責？」 |

| **2. 權限邊界 (Permission)** | File Permissions / POSIX ACL (rwx) | **Zero-Heap Capability Bitmaps (暫存器級位元圖)** | 解決「權限範圍多大？精確鎖定 Tool 與 API 呼叫」 |

| **3. 系統呼叫保護 (Syscall)** | Ring 0 / Kernel Mode 記憶體隔離 | **C-ABI 帶內攔截閘門 (In-Band VEP Gate)** | 解決「AI 意圖不可控，物理阻斷危險呼叫」 |

| **4. 異常處理 (Fault Handling)** | `SIGSEGV` / `SIGKILL` 核心崩潰保護 | **26.1 μs 帶內硬熔斷 (Hard Circuit-Breaker)** | 解決「Prompt Injection 越獄與惡意行為」 |

| **5. 存取稽核 (Auditing)** | `auditd` / Linux Journal 日誌 | **SHA-256 Merkle Hash 密碼學證據鏈** | 解決「事後偽造與串供，產出法院採信收據」 |

| **6. 資源回收 (Revocation)** | `kill -9` / Process Terminate | **$O(1)$ RCU 原子指針秒級動態撤銷** | 解決「授權過期或被撤銷後，背景 Agent 偷跑」 |



---



## 🔺 跨產業統一治理核心：DROS「黃金三角形模型 (The Golden Triangle)」



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

     • 金融: 去識別化圖關聯特徵/行為向量           • 金融: 明文姓名/身分證號/原始帳戶明細

     • 醫療: ICD-10診斷碼/理賠金額/住院天數        • 醫療: 18項 PHI/病歷日誌/遺傳病史

     • 政府: 補助門檻試算條件 (年齡/所得級距)      • 政府: 跨機關完整稅籍/醫療病歷

     • 普惠金融: 居留許可狀態/合法就業證明         • 普惠金融: 完整母國銀行帳號/私密密碼

     • 供應鏈: 合規狀態 TRUE / ZKP 證明            • 供應鏈: 工廠良率/全體薪資/組織圖

                 │                                         │

                 ▼                                         ▼

     ┌────────────────────────┐              ┌──────────────────────────┐

     │ 產業 AI Detection /    │              │ 💥 C-ABI 帶內硬性阻斷    │

     │ Domain Agent 決策引擎  │              │ (HTTP 403 26.1 μs 熔斷)  │

     └───────────┬────────────┘              └──────────────────────────┘

                 │

                 ▼ (Risk Score / Analysis / Pre-check)

     ┌────────────────────────┐

     │ DROS Policy Gate       │

     │ 帶內防禦 + 人類雙簽    │

     └───────────┬────────────┘

                 │

                 ▼

     【確定性執行 / Merkle 密碼學證據鏈】

```



---



## 🔌 應用層的兩大根本邊界 (Two Fundamental Governance Boundaries)



對應用程式開發者（Application Developer）而言，治理責任被高度抽象為兩個基本的架構邊界，使業務邏輯與執行治理完全解耦：



```text

                 Application (Business Logic & Intent)

                                  │

                        ┌─────────┴─────────┐

                        │                   │

                     Ingress             Egress

                        │                   │

                        ▼                   ▼

                  ┌──────────────────────────────┐

                  │             DROS             │

                  │                              │

                  │ Identity (Principal)         │

                  │ Authorization (Capability)   │

                  │ Tool Boundary (In-Band Trap) │

                  │ Policy Gate (HITL 2FA)       │

                  │ Privacy & Data Minimization  │

                  │ Cryptographic Audit Log      │

                  │ O(1) Instant Revocation      │

                  └──────────────┬───────────────┘

                                 │

                             C-ABI Gate

                                 │

                                 ▼

                            OS Effect

```



1. **📥 Ingress 邊界（安全特徵輸入 / Data Ingest）**：確保餵給 AI Agent 的輸入資料，永遠是**經治理與資料最小化後、符合特定 Policy 的特徵資料**（如遮蔽 18 項 PHI、遮蔽 BOM 成本、去識別化圖特徵）。

2. **📤 Egress 邊界（確定性動作輸出 / Execution Sink）**：確保 AI Agent 發起的每一次 Tool Call / Action，**物理上必須通過 C-ABI 帶內策略閘門**，在 $26.1\,\mu\text{s}$ 內完成 6P 閉環校驗並生成具備法院採信力之 Merkle 存證，未授權動作瞬間硬熔斷。事後偽造與串供，產出法院採信收據」 |

| **6. 資源回收 (Revocation)** | `kill -9` / Process Terminate | **$O(1)$ RCU 原子指針秒級動態撤銷** | 解決「授權過期或被撤銷後，背景 Agent 偷跑」 |



---



## 🔌 DROS 的 2 大通用接口 (Two Universal Interfaces)



DROS 在底層完成了 6P 閉環，對外僅留下 2 個標準接口即可對接全世界所有的 AI 應用層：



1. **📥 接口 ①：Data Ingest（最小必要特徵安全輸入接口 / Safe Ingress）**：過濾機密與 PHI，僅向 AI 提供去識別化特徵向量與 ZKP 證明。

2. **📤 接口 ②：Execution Sink（確定性動作與工具執行接口 / Safe Egress）**：在 C-ABI 二進位層級於 $26.1\,\mu\text{s}$ 內完成 6P 帶內安全檢驗與 Merkle 密碼學存證。



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



不管大會公布何種新題目 (Track 01 ~ 06)，DROS-VEP Lite 均能以通用硬體與網關邊界實施鋼性防護：



1. **Principal (身份)**：DIT Token 帶內注入，強綁定團隊、企業與法人的加密 Key（法人 vLEI + 自然人 MyData/FIDO 雙軌）。

2. **Authorization (授權)**：Zero-Heap Capability Bitmaps 暫存器級精確鎖定 `PERMIT` 與 `PROHIBITED` 動作與欄位。

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

