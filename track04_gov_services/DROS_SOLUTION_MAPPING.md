# Track 04 專屬：DROS-VEP 解決方案對應說明書 (Gov Services & Identity Proxy)

> **主題**：政府服務 ── 解決憑證碎片化背後的資料孤島與跨機關可信代理  
> **核心技術內核**：DROS-VEP Lite (Dual-Track Identity Proxy: Natural Person MyData/Wallet + Legal Entity vLEI, & $O(1)$ RCU Instant Revocation)

---

## 零、 DROS 整體機制導讀

### 🔍 DROS 是什麼？它解決的根本問題是什麼？

傳統 AI Agent 的最大安全缺口，不是 AI 模型本身，而是 **「AI Agent 被授權後，誰來管控它實際執行期的行為？」**

在政府服務場景中，台灣政府已推動 **MyData（解決資料取得）** 與 **數位憑證皮夾（解決個人出示）**，但始終存在一塊關鍵空白：**「AI Agent 代理代辦（人不在現場）」**！當民眾或企業委託 Agent 跨機關申辦育兒津貼、長照補助或稅務登記時，現有系統無法回答「誰授權的？授權範圍多大？多久失效？出錯誰負責？」。DROS-6P 提供了專為 Agent 執行期設計的微秒級確定性治理內核。

---

## 一、 題目缺口與現實產業痛點 (Governance Gap & Industry Context)

### 🏛️ 產業背景：跨機關憑證碎片化與「申請制」的荒謬

依據個資法第 5 條，公務機關只能在法定職務範圍內利用個資（如戶政資料不能由社會局隨意調閱），導致政府雖然早就掌握民眾的出生與稅籍資料，民眾仍被迫在不同部會網站之間來回重填（「你不申請就不給」）。

```
現行數位身分工具的演進與斷鏈：

  STEP 1: MyData (2019起)         STEP 2: 數位憑證皮夾 (2025起)      STEP 3: AI Agent 代辦 (當前缺口)
      ✓ 民眾自主同意繞開法規          ✓ W3C 國際標準 / 選擇性揭露         ❌ 缺乏執行期可信代理治理
         │                               │                                   │
  ─────────────────────────────────────────────────────────────────────────────────→ 
         │                               │                                   │
      ✗ 缺點：一根管子、單次使用     ✗ 缺點：解決出示，但人必須在現場     💥 痛點：Agent 越權、無法撤銷
```

### 🔴 跨機關代理代辦的四大核心問題

1. **誰授權的？ (Principal)**：Agent 代表民眾本人還是整個家戶？多人合併申辦時如何防偽？
2. **授權範圍多大？ (Authorization)**：「代查資格」與「代送件簽署」是否混在一起？能否防範查所得時順便偷查病歷？
3. **高風險動作如何把關？ (Policy Gate)**：具有法律效力的最終簽署，如何強制懸停由本人確認？
4. **授權如何即時撤銷？ (Revocation)**：民眾撤銷委託後，Agent 會不會在背景繼續偷跑？

---

## 二、 DROS-VEP 解法：自然人與法人「身分雙軌對接」與三層代理邊界

DROS 在政府端部署 C-ABI 帶內治理微內核，原生支援**「自然人（MyData/皮夾）+ 法人（vLEI）」雙軌身分**，並劃分嚴格的三層授權邊界：

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   DROS-VEP GovProxy 雙軌身分與三層授權架構                       │
│                                                                                  │
│  【軌道 1：自然人身分 (Natural Person)】                                         │
│   • 起點：MyData 授權包 / 數位憑證皮夾 (W3C VC)                                  │
│   • 注入：DROS DIT Token (綁定身分證號密碼學 Hash、有效期限、委託範圍)           │
│                                                                                  │
│  【軌道 2：法人身分 (Legal Entity)】                                             │
│   • 起點：GLEIF vLEI 法人憑證 (LE) + 業務角色憑證 (ECR/OOR)                      │
│   • 注入：DROS DIT Token (綁定公司 LEI 碼、ISO 5009 官方角色、經辦權限)          │
│                                                                                  │
│  【三層代理授權邊界 (Three-Tier Capability Boundary)】                           │
│   1. LEVEL 1: 代查資格 (Query)   ──► 【PERMIT (26.1 μs 放行)】                   │
│      • 自動比對跨部會條件（如戶政出生證明 + 綜所稅率），民眾免重填               │
│   2. LEVEL 2: 代送件 (Submit)    ──► 【SUSPENDED (HITL 懸停)】                   │
│      • 備妥申辦草稿，推送手機 2FA 請民眾確認，300 秒逾時保護                     │
│   3. LEVEL 3: 法律簽署 (Sign)     ──► 【DENY (硬性阻斷)】                         │
│      • 涉及法律責任之最終印鑑/簽章，嚴禁 Agent 擅自代理                          │
│                                                                                  │
│  【秒級動態撤銷 (Instant Revocation)】                                           │
│   • 民眾於 App 點擊「終止代辦」 ──► $O(1)$ RCU 原子指針在 <1 μs 內覆寫           │
│   • Agent 後續任何請求瞬間回傳 HTTP 403 FORBIDDEN，零延遲物理停止               │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 三、 6 大信任要點閉環對照表 (6-Pillar Enforcement)

| 信任要點 (Pillar) | 政府服務場景面臨之挑戰 | DROS-VEP 實體微內核解法 | 實測性能指標 |
| :--- | :--- | :--- | :--- |
| **1. Principal (代表誰)** | 自然人與法人身分混淆、代辦身分遭冒用 | 雙軌 DIT Token 帶內注入（自然人 MyData/皮夾 + 法人 vLEI ECR） | $0.0008\text{s}$ 驗證通過 |
| **2. Authorization (授權)** | 代查與代送件權限邊界不清 | Zero-Heap Capability Bitmaps 實施三層角色方法硬性映射 | 暫存器位元比對零延遲 |
| **3. Tool Bound (邊界)** | Agent 跨部會橫向移動偷讀其他機關資料庫 | C-ABI / eBPF 外國函式介面帶內攔截，未授權 API 瞬間 Drop | $26.1\ \mu\text{s}$ 帶內熔斷 |
| **4. Policy Gate (門閥)** | 涉及法律效力之送件與簽署缺乏把關 | HITL 狀態懸停機制，向民眾手機推送 2FA 二次確認 | 300s 逾時防禦 |
| **5. Audit Log (稽核)** | 申辦遭駁回或資料外洩時責任無從追溯 | SHA-256 Merkle Hash Chain，產出具備法院採信力之申辦收據 | 獨立離線驗證通過 |
| **6. Revocation (撤銷)** | 民眾撤銷委託後背景 Agent 依然偷跑 | $O(1)$ RCU (Read-Copy-Update) 原子指針切換 | $< 1\ \mu\text{s}$ 即時撤銷 (HTTP 403) |

---

## 四、 10 秒可重現驗證指令

```bash
# 1. 執行政府服務與雙軌身分自動化測試
python test_verification_suite.py

# 2. 啟動展示台檢視 GovProxy 控制台
python server.py
# 瀏覽: http://localhost:8000/track04_gov_services/index.html
```

---
*專利聲明：DROS 執行治理與安全技術已申請美國臨時專利保護（U.S. Provisional Patent Application No. 64/111,973）。*  
*© 2026 OpenShip Ecosystem & Top-Celestial Company Ltd. All Rights Reserved.*
