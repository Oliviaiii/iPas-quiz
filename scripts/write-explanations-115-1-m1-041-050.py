"""Write draft explanations for 115-1 intermediate subject one, Q41-Q50.

The script validates the official answer for every question, refuses to
overwrite reviewed work, and leaves all generated content in ``draft``.

Usage::

    python scripts/write-explanations-115-1-m1-041-050.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-intermediate-1-ai-tech-planning"
AUTHOR = "Codex（AI 輔助初稿）"
AUTHORED_AT = "2026-08-12"
CHECKED_AT = "2026-08-12"

EXAM_PDF = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/115年第一次中級AI應用規劃師_"
    "第一科_人工智慧技術應用與規劃_公告試題_20260615003359.pdf"
)
DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def exam_ref(number: int) -> dict:
    return {
        "title": "115 年第一次中級 AI 應用規劃師－人工智慧技術應用與規劃公告試題",
        "url": EXAM_PDF,
        "locator": f"第 {number} 題題幹、選項與官方答案",
        "checkedAt": CHECKED_AT,
    }


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


EXPECTED_ANSWER = {
    41: "A", 42: "D", 43: "C", 44: "B", 45: "B",
    46: "C", 47: "D", 48: "C", 49: "A", 50: "D",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[41] = {
    "summary": "正確答案是 A。小批次推論與 kernel 間閒置會使 GPU 工作無法連續填滿，顯示批次聚合或 GPU 排程不佳，既壓低利用率，也可能在尖峰造成排隊延遲波動。",
    "concept": (
        "GPU 需要足夠且連續的平行工作才能有效使用大量運算單元。單筆或小批次"
        "請求常使每個 kernel 工作量不足，且多次啟動、資料搬移與請求排程會留下"
        "空檔；動態批次可在短暫佇列窗口內合併相容請求，提高吞吐與利用率。"
        "批次太大或等待窗口太久又會增加尾端延遲，因此需以實際流量調整最大"
        "batch、queue delay、模型 instance 數與優先序，而非只追求利用率。"
    ),
    "answerReason": (
        "題幹已給出 60% 利用率、小批次及 kernel 間明顯空檔，並排除 CPU、記憶體、"
        "網路、硬體與併發控制異常。A 直接解釋這些觀察：排程與 batch 設定使 GPU"
        "無法持續飽和，尖峰時等待佇列又放大延遲。"
    ),
    "optionAnalysis": {
        "A": "正確。小批次不足以填滿 GPU，kernel 啟動間隔又造成空轉；若排程器未適當聚合請求或配置模型 instances，尖峰佇列便可能形成不穩定的尾端延遲。",
        "B": "多請求爭用 GPU context 確實可能造成切換與延遲，但題幹明確說併發控制異常已排除；相反地，小批次與 kernel 空檔直接指向工作聚合不足。",
        "C": "若硬體算力根本不足，持續高負載時通常會看到 GPU 接近飽和；此處長期僅約 60% 且有空檔，顯示現有資源尚未被有效餵滿，而非單純效能不足。",
        "D": "量化可降低模型計算與記憶體成本，但未量化通常會增加每次 kernel 工作，不會自然造成低利用率與 kernel 間空檔；題幹也沒有提供精度或數值格式證據。",
    },
    "trap": "低 GPU 利用率不代表一定要換更快 GPU；先看時間軸是計算飽和、記憶體受限，還是 kernel 間空白。本題的小 batch 加空檔是排程與批次線索。",
    "references": [
        exam_ref(41),
        ref("NVIDIA Triton Inference Server－Batchers", "https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html", "Dynamic batcher 會合併推論請求以建立較大 batch、提高吞吐，並可設定最大排隊延遲與優先序"),
    ],
}

DRAFTS[42] = {
    "summary": "正確答案是 D。整體 RMSE 會由占 95% 的一般案件主導；若未依理賠金額區間切片監控，僅占 5% 的高額案件退化可能被總體平均掩蓋。",
    "concept": (
        "總體指標把不同族群的誤差聚合成一個數字。RMSE 雖會將大殘差平方而較"
        "重視極端誤差，但少數切片仍可能因樣本占比低、其他切片改善或尺度差異"
        "而在總體值中不明顯。模型監控應依業務風險建立資料切片，例如理賠金額"
        "分位區間、案件類型或客群，分別追蹤樣本量、RMSE、偏差及高分位誤差，"
        "並設定足以捕捉小族群的警示門檻。"
    ),
    "answerReason": (
        "D 指出監控設計的根本缺口是只看聚合 RMSE，未把高額理賠獨立切片。"
        "這正好解釋為何整體指標穩定而業務觀察到該 5% 族群惡化；提高更新頻率"
        "或改用 MAE 都不能替代分群觀測。"
    ),
    "optionAnalysis": {
        "A": "每日改成即時只能更快重算同一個總體指標；若聚合方式仍把高額案件稀釋，即時 RMSE 仍可能不觸發警示，因此頻率不是核心缺陷。",
        "B": "長尾族群不是無法監控；可按金額門檻或分位數切片，另設誤差、樣本量與信賴區間。樣本較少會提高不確定性，但不代表只能放棄偵測。",
        "C": "MAE 對大誤差的懲罰比 RMSE 更弱，改用 MAE 反而可能更不敏感；真正需求是把高額案件獨立切片，必要時再搭配加權或分位數指標。",
        "D": "正確。分群監控能讓高額案件自己的 RMSE、MAE、偏差與樣本數直接呈現，不再被大量一般案件平均，並能設定符合高額理賠風險的警示。",
    },
    "trap": "RMSE 會放大大殘差，但不保證少數族群一定在整體指標中顯著。問題若明確指出某 5% 子群退化，優先想到 slice-based monitoring，而不是單純換平均指標。",
    "references": [
        exam_ref(42),
        ref("TensorFlow Model Analysis－Metrics and plots", "https://www.tensorflow.org/tfx/model_analysis/metrics", "TFMA 可在完整資料與指定 slices 上計算模型指標，以檢視不同資料子群表現"),
        ref("scikit-learn－Mean squared error", "https://scikit-learn.org/stable/modules/model_evaluation.html#mean-squared-error", "MSE 對殘差平方後平均；RMSE 為其平方根，與 MAE 的誤差權重不同"),
    ],
}

DRAFTS[43] = {
    "summary": "正確答案是 C。Canary Release 將少量真實使用者流量導向新模型，直接量測 CTR、CVR 等線上指標，達標後再逐步擴量，能在控制曝險下驗證業務效果。",
    "concept": (
        "離線 AUC 與 NDCG 使用歷史標籤評估，無法完整反映推薦結果改變後的使用者"
        "回饋、介面互動與系統延遲。金絲雀發布讓新版本只服務少量流量，配合"
        "對照組、流量隨機化、統計檢定與 guardrails 觀察轉換、錯誤率及延遲；"
        "若指標健康再擴量，異常則停止或回滾。Shadow Mode 不把新結果呈現給"
        "使用者，因此適合驗證技術行為，卻不能量測新推薦造成的點擊與購買。"
    ),
    "answerReason": (
        "題目要求在全面上線前，以可控制風險量化真實業務指標。C 同時提供真實"
        "使用者曝險、少量起始流量、CTR／CVR 量測與逐步擴量，完全符合要求。"
    ),
    "optionAnalysis": {
        "A": "Shadow Mode 可比較輸出、延遲與錯誤，因使用者仍只看到舊模型，無法觀察他們對新推薦的點擊、購買或停留反應，不適合回答線上業務提升多少。",
        "B": "Backtesting 仍使用歷史日誌，可能受舊策略的曝光偏差影響，沒有新模型改變內容後的真實互動；可作上線前補充證據，但不是線上驗證。",
        "C": "正確。先讓 1–5% 流量實際使用新模型，與控制組比較 CTR、CVR、延遲和錯誤率；通過預設門檻再擴量，可限制故障與負面體驗的影響範圍。",
        "D": "Load Testing 驗證吞吐、資源與延遲，不會產生真實點擊或購買行為；壓測通過只表示系統能承載流量，不能證明推薦內容帶來業務改善。",
    },
    "trap": "Shadow、canary 與 load test 的觀察對象不同：Shadow 看新舊技術輸出，canary 看真實使用者與業務指標，load test 看容量。題目點名 CTR、CVR，應選真實小流量曝險。",
    "references": [
        exam_ref(43),
        ref("Google Cloud Deploy－Canary deployments", "https://cloud.google.com/deploy/docs/deployment-strategies/canary", "Canary deployment 先將部分流量導向新版本，經驗證後逐階段增加至全部流量"),
        ref("Kohavi et al., Online Controlled Experiments: Lessons from Running A/B/n Tests for 12 Years（2016）", "https://arxiv.org/abs/1606.07659", "以線上隨機對照實驗量測產品變更對使用者與業務指標的因果影響"),
    ],
}

DRAFTS[44] = {
    "summary": "正確答案是 B。影像分類是提交資料給伺服器處理，應用 POST 並把 5MB 二進位影像放在 Request Body，以 multipart/form-data 或 application/octet-stream 傳輸。",
    "concept": (
        "HTTP POST 適合讓伺服器依請求內容執行處理；Request Body 可承載大型二進位"
        "資料。只有一個原始檔時可用 application/octet-stream，多欄位或檔案連同"
        "metadata 時可用 multipart/form-data。把影像 Base64 放進 URL 會增加約三分"
        "之一大小，且 URL 受代理、伺服器與日誌長度限制，也可能讓敏感內容進入"
        "存取日誌。PUT 的語意主要是以指定 URI 建立或替換資源，不因資料是檔案"
        "就優於 POST；Content-Type 更必須描述實際內容。"
    ),
    "answerReason": (
        "B 的方法、位置與媒體類型皆正確：POST 表示提交分類工作，影像置於 body，"
        "multipart 或 octet-stream 可直接傳二進位。其他選項不是違反方法語意與"
        "傳輸限制，就是把需求改成客戶端推論。"
    ),
    "optionAnalysis": {
        "A": "GET 用於取得資源，內容不應依賴 request body；將 5MB 影像 Base64 放在 query 會膨脹、超過 URL 限制並可能被日誌記錄，不適合檔案上傳。",
        "B": "正確。POST 可提交待分類影像；multipart/form-data 能同時攜帶檔案與欄位，application/octet-stream 則適合單一原始二進位串流，都避免 URL 編碼負擔。",
        "C": "PUT 通常表示以目標 URI 建立或完整取代資源，而即時分類較像建立一次處理請求；application/xml 也無法正確描述原始影像二進位內容。",
        "D": "本地推論可用於離線或隱私情境，但會改變題目要求的服務部署、模型更新與客戶端資源邊界；它不是 REST API 接收高解析影像的傳輸設計。",
    },
    "trap": "方法語意與內容格式要分開判斷：POST 是提交處理，Content-Type 描述 body。Base64 不是加密或壓縮，放進 URL 還會增加體積與日誌曝露。",
    "references": [
        exam_ref(44),
        ref("RFC 9110－HTTP Semantics", "https://www.rfc-editor.org/rfc/rfc9110.html", "第 9.3.1、9.3.3、9.3.4 節：GET、POST 與 PUT 的方法語意；第 8.3 節定義 Content-Type"),
        ref("RFC 7578－multipart/form-data", "https://www.rfc-editor.org/rfc/rfc7578.html", "multipart/form-data 媒體類型與檔案欄位傳輸規則"),
    ],
}

DRAFTS[45] = {
    "summary": "正確答案是 B。Circuit Breaker 在外部服務持續失敗或逾時時暫停新呼叫並快速失敗或降級，避免執行緒、連線與佇列被拖垮而引發級聯故障。",
    "concept": (
        "斷路器以 Closed、Open、Half-Open 等狀態管理遠端呼叫。正常時允許請求並"
        "統計失敗；錯誤率或連續逾時達門檻後開路，在冷卻期間不再呼叫故障服務，"
        "而是立即回傳 fallback；稍後以少量探測判斷是否恢復。它通常搭配逾時、"
        "有限重試、bulkhead 與監控使用。單純擴大 thread pool 只延後資源耗盡，"
        "取消 timeout 更會使請求無限占用資源。"
    ),
    "answerReason": (
        "B 直接切斷故障外部服務造成的等待鏈，並提供替代回應，能防止局部逾時"
        "蔓延成平台中斷。其餘方案會增加阻塞、只擴大故障容器，或移除偵測訊號。"
    ),
    "optionAnalysis": {
        "A": "同步串行使每個下游延遲相加，取消 timeout 還會讓故障呼叫長時間占住連線與工作執行緒，最容易放大壅塞，不是可靠性設計。",
        "B": "正確。斷路器偵測持續錯誤後快速拒絕新呼叫，讓上游使用快取、預設值或部分結果；冷卻後再探測恢復，隔離故障並保護共享資源。",
        "C": "增加 thread pool 可能短暫容納更多等待，但外部服務仍慢時會產生更多同時卡住的呼叫、記憶體與連線壓力，甚至加重下游負載。",
        "D": "健康檢查提供故障偵測與流量摘除依據，停用後流量可能繼續送往異常實例；其負載通常應優化頻率與端點，而非完全取消。",
    },
    "trap": "Circuit Breaker 與 retry 方向不同：retry 再嘗試，breaker 在故障持續時停止嘗試。實務上重試要有限且退避，否則重試風暴也會造成 cascading failure。",
    "references": [
        exam_ref(45),
        ref("Microsoft Azure Architecture Center－Circuit Breaker pattern", "https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker", "以 Closed、Open、Half-Open 狀態處理遠端服務失敗，避免持續呼叫不可用服務並提供恢復探測"),
    ],
}

DRAFTS[46] = {
    "summary": "正確答案是 C。Federated Learning 將訓練工作移到院內資料所在處，只把模型更新送往雲端聚合，因此符合題目所設『原始影像不離院、仍利用雲端協調算力』的限制。",
    "concept": (
        "聯邦學習採 data stays local 的分散式訓練流程：中央端下發模型，各參與端"
        "在本地資料上計算更新，再回傳梯度或權重差異供聚合。原始病歷與影像不需"
        "集中到雲端，但模型更新仍可能洩漏資訊，實務需搭配安全聚合、傳輸加密、"
        "存取控制、差分隱私與治理。題目要求使用公有雲 GPU 訓練的用語略簡化："
        "若資料完全不出院，直接接觸資料的 forward／backward 計算需在院內，"
        "雲端主要負責模型協調、聚合或不接觸原始資料的工作。"
    ),
    "answerReason": (
        "C 是唯一沒有把原始資料或可解密資料傳往公有雲的方案。AES 與 VPN 只"
        "保護傳輸或靜態資料，雲端訓練時仍須取得明文；選項 B 又只處理加密推論，"
        "沒有建立題目要求的訓練流程。"
    ),
    "optionAnalysis": {
        "A": "AES-256 可保護傳輸與儲存中的影像，但選項明說在雲端解密後訓練，原始內容仍會離開院內並在雲端成為明文，不符合題目設定。",
        "B": "同態加密可讓特定運算在密文上進行，但選項只描述推論請求，未說明如何以院內訓練與雲端聚合完成模型訓練；也未對應題目的聯邦流程。",
        "C": "正確。影像留在醫院，院內節點以本地資料更新模型，雲端只聚合更新再下發新版；因此可協作訓練而不集中原始患者資料。",
        "D": "VPN 保護傳輸通道，卻不改變資料已被送到雲端的事實；雲端端點取得後仍可能處理原始影像，故不符合『不傳輸原始患者資料』。",
    },
    "trap": "加密傳輸不等於資料沒有離開院內；Federated Learning 也不等於自動具備隱私保證，模型更新仍須安全聚合與洩漏風險控制。",
    "editorialNote": "本站依題目明定的『原始資料不得離開院內』限制選 C。HIPAA 本身並非概括禁止受保護健康資訊使用合規雲端服務；是否可上雲仍涉及適用實體、Business Associate Agreement、風險分析與安全控制。另依標準聯邦學習流程，直接讀取原始影像的訓練計算發生在院內，公有雲主要負責協調與聚合。查核日期 2026-08-12。",
    "references": [
        exam_ref(46),
        ref("McMahan et al., Communication-Efficient Learning of Deep Networks from Decentralized Data（2016）", "https://arxiv.org/abs/1602.05629", "摘要與 FederatedAveraging 方法：資料保留於分散客戶端，本地計算模型更新後由中央聚合"),
        ref("HHS－Guidance on HIPAA & Cloud Computing", "https://www.hhs.gov/hipaa/for-professionals/special-topics/health-information-technology/cloud-computing/index.html", "受管制實體可使用符合 HIPAA 的雲端服務，但須與 CSP 建立適當 BAA 並遵守 Privacy、Security 與 Breach Notification Rules"),
    ],
}

DRAFTS[47] = {
    "summary": "正確答案是 D。30% 流量時延遲已明顯惡化，應先停止擴量、保留可控曝險並分析瓶頸；完成效能優化與驗證後，才繼續漸進部署。",
    "concept": (
        "Phased Rollout 的價值是每一階段都設置 success criteria 與 guardrails。"
        "轉換率是業務結果，延遲、錯誤率與資源飽和則是使用者體驗及可靠性護欄；"
        "任一關鍵護欄越界，就應暫停 promotion，診斷模型計算、特徵服務、快取、"
        "排程與容量，修復後再以同一階段驗證。是否立即 rollback 取決於嚴重度、"
        "錯誤預算與使用者影響；題目僅說部分體驗變差，D 保留調查與恢復路徑，"
        "比永久停止測試更合適。"
    ),
    "answerReason": (
        "D 同時避免把延遲問題擴大到全部使用者，又允許保留目前證據並完成效能"
        "修正。A 與 C 忽視 guardrail，B 則在尚可控制與修復時直接終止整個新模型"
        "流程，過度保守且失去已觀察到的轉換率收益。"
    ),
    "optionAnalysis": {
        "A": "延遲已在 30% 流量顯著上升，擴到 100% 可能使資源更飽和並影響所有使用者；漸進部署正是為了在這一步停止，而不是用全面曝險繼續觀察。",
        "B": "若延遲已超過嚴重門檻，可暫時 rollback；但選項還要求停止整個測試流程，沒有分析與修復後重試的路徑，無法利用新模型的轉換率改善。",
        "C": "維持 30% 可限制範圍，但在已知體驗惡化時只觀察而不調整，會持續傷害該群使用者，也無法找出容量或程式瓶頸。",
        "D": "正確。凍結 promotion，依必要程度降低或維持安全流量，針對 P95/P99 延遲、資源、依賴服務與模型耗時剖析；通過效能與業務門檻後再恢復擴量。",
    },
    "trap": "業務指標提升不能抵銷所有可靠性問題。漸進部署要同時看 primary metric 與 guardrails；『暫停擴量』也不等於永久放棄新模型。",
    "references": [
        exam_ref(47),
        ref("Google Cloud Deploy－Canary deployments", "https://cloud.google.com/deploy/docs/deployment-strategies/canary", "Canary 階段逐步增加流量；每階段可驗證版本後再 advance，亦可停止或 rollback"),
    ],
}

DRAFTS[48] = {
    "summary": "正確答案是 C。輸入特徵分布大致未變，但疫情後相同深夜交易型態所代表的盜刷風險改變，表示 P(y|x) 的特徵—標籤關係發生概念漂移。",
    "concept": (
        "Data Drift 通常指輸入分布 P(X) 改變；Concept Drift 則指目標與輸入的"
        "條件關係 P(Y|X) 隨時間變化。同樣的金額、地區、裝置與交易時段，在"
        "消費習慣改變後可能不再具有原本的風險意義，因此舊決策規則的攔截效果"
        "下降。整體 AUC 幾乎不變也不能排除特定時段、客群或既定 threshold 的"
        "業務表現退化，需做時間與族群切片並以延遲回收標籤監控。"
    ),
    "answerReason": (
        "題幹明說主要輸入特徵分布沒有明顯變化，卻指出原高風險型態逐漸成為"
        "一般消費，即同一 X 對 Y 的意義改變。C 的 Concept Drift 正確描述此"
        "現象；它不是特徵管線不一致，也不能只以調整 threshold 解釋根因。"
    ),
    "optionAnalysis": {
        "A": "Data Drift 要求輸入特徵分布改變，但題幹已說交易金額、地區與裝置等分布無明顯變化；即使可另查時段比例，已知關鍵線索是風險意義改變。",
        "B": "Training-Serving Skew 是訓練與線上採用不同轉換、程式或資料定義；題目說模型與特徵工程未調整，也沒有離線／線上值不一致證據。",
        "C": "正確。疫情後深夜電商成為一般行為，使相同特徵組合對盜刷標籤的條件機率改變；舊模型學到的關係因此不再完全適用。",
        "D": "重新校準 threshold 可能改善核准率與攔截率的取捨，但門檻沒有自行漂移；真正原因是資料生成概念改變，單純調門檻也未必恢復各族群排序。",
    },
    "trap": "先問『變的是 X，還是 X 與 Y 的關係』：P(X) 變是 data drift，P(Y|X) 變是 concept drift。AUC 穩定是整體排序訊號，不代表每個切片或固定門檻表現穩定。",
    "references": [
        exam_ref(48),
        ref("Gama et al., A Survey on Concept Drift Adaptation（2014）", "https://dl.acm.org/doi/10.1145/2523813", "第 2 節：concept drift 描述資料生成分布隨時間改變，並區分輸入分布與條件關係的變化"),
    ],
}

DRAFTS[49] = {
    "summary": "正確答案是 A。每個 epoch 的學習率與超參數軌跡描述離線訓練實驗，不是線上服務當下狀態，應由 experiment tracking 保存與比較。",
    "concept": (
        "Continuous Monitoring 關注已部署模型的服務健康、輸入、輸出與回收後"
        "品質，例如延遲、吞吐、錯誤率、特徵漂移、預測分布及標籤對照。Experiment"
        "Tracking 則記錄一次訓練 run 的參數、學習率、epoch metrics、程式版本與"
        "模型 artifacts，支援重現及選模。兩者可以在儀表板互相連結，但資料產生"
        "時機、告警目的與保留方式不同。"
    ),
    "answerReason": (
        "A 只在模型訓練期間產生，部署後不會隨每筆線上請求變動，因此最不適合"
        "放在線上即時監控。B 是系統 SLI，C 是輸入漂移，D 是線上行為與回收標籤"
        "品質，三者皆屬持續監控範疇。"
    ),
    "optionAnalysis": {
        "A": "正確。learning-rate schedule、超參數與 epoch 曲線屬特定訓練 run 的 provenance，適合存入 MLflow 等實驗追蹤系統，用於比較、重現與選模。",
        "B": "P50/P95/P99 latency、RPS 與錯誤率反映線上服務是否達成 SLO，會隨流量與負載即時變化，應持續監控並設告警。",
        "C": "PSI 以基準與當前特徵分布比較，可定期偵測輸入族群變化；不一定逐請求計算，但仍屬部署後持續監控，而非訓練實驗軌跡。",
        "D": "預測與 CTR 分布可較快觀察行為，人工標籤回收後則可估算真實品質；雖有時間延遲，仍是線上模型閉環監控的重要部分。",
    },
    "trap": "『持續監控』不代表每個指標都必須逐秒更新；延遲標籤與漂移可按小時或日計算。判斷重點是資料來自部署後運行，還是離線訓練 run。",
    "references": [
        exam_ref(49),
        ref("MLflow Tracking 官方文件", "https://mlflow.org/docs/latest/ml/tracking/", "Tracking runs 會記錄訓練參數、metrics、artifacts 與模型，支援實驗比較與重現"),
        ref("Google Cloud－Introduction to Vertex AI Model Monitoring", "https://cloud.google.com/vertex-ai/docs/model-monitoring/overview", "部署後監控輸入特徵偏移、預測偏移與特徵歸因偏移，並設定警示"),
    ],
}

DRAFTS[50] = {
    "summary": "正確答案是 D。Late Fusion 是各模態先獨立預測、最後才整合決策；D 卻說它在輸入階段整合特徵，這其實是 Early Fusion，因此最不可能解釋題述韌性。",
    "concept": (
        "Early Fusion 在特徵或輸入層先合併模態，再由共同模型學習；一個模態的"
        "噪音可能在共享特徵中影響後續表示。Late Fusion 讓影像模型與文字模型"
        "各自產生分數或預測，再用平均、加權、投票或次級模型整合。因分支隔離，"
        "文字品質下降不會直接破壞影像 encoder；若融合器能降低不可靠文字分支"
        "權重，整體效能便可能只小幅下降。"
    ),
    "answerReason": (
        "題目已明定影像與文字分別預測後再整合，這就是 decision-level 的 Late"
        "Fusion。A、B、C 都能由分支隔離或權重調整解釋穩健性；D 把流程顛倒成"
        "輸入階段融合，與前提直接矛盾。"
    ),
    "optionAnalysis": {
        "A": "可能。影像與文字各自推論，文字品質變差主要先影響文字分支；影像分支仍能提供獨立證據，因此整體不一定同比例惡化。",
        "B": "可能。融合器若有品質估計、門控或可學習權重，可在文字資訊不足時降低其分數權重，讓較可靠的影像預測主導結果。",
        "C": "可能。獨立模型使文字噪音不會在早期共享特徵層污染影像表示；錯誤仍可能在最終決策影響結果，但影響路徑較受隔離。",
        "D": "最不可能。輸入或特徵階段就整合是 Early Fusion，不是題目所述的『分別預測後再整合』；因此不能用它解釋此 Late Fusion 系統的表現。",
    },
    "trap": "題目問『最不可能』，且關鍵是融合時點：輸入／特徵層是 early fusion，個別模型輸出／決策層才是 late fusion。獨立分支降低耦合，但不保證差模態完全沒有影響。",
    "references": [
        exam_ref(50),
        ref("Baltrušaitis, Ahuja & Morency, Multimodal Machine Learning: A Survey and Taxonomy（2017）", "https://arxiv.org/abs/1705.09406", "第 5 節 Fusion：model-agnostic late fusion 對各模態分別預測後再以 averaging、voting 等方式整合"),
    ],
}


def main() -> None:
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    index = {
        q["officialQuestionNumber"]: q
        for q in questions
        if q["sourceId"] == SOURCE_ID
    }

    written = 0
    for number, draft in sorted(DRAFTS.items()):
        question = index.get(number)
        if question is None:
            raise SystemExit(f"Q{number} not found in {SOURCE_ID}")
        actual = question["officialAnswer"][0]
        if actual != EXPECTED_ANSWER[number]:
            raise SystemExit(
                f"Q{number}: official answer is {actual}, "
                f"but the draft was written for {EXPECTED_ANSWER[number]}"
            )
        if question["explanationStatus"] == "reviewed":
            raise SystemExit(f"Q{number} is already reviewed; refusing to overwrite")
        if sorted(draft["optionAnalysis"]) != ["A", "B", "C", "D"]:
            raise SystemExit(f"Q{number}: option analysis must cover A-D")
        if not draft["summary"].startswith(f"正確答案是 {actual}"):
            raise SystemExit(f"Q{number}: summary does not state the official answer")

        explanation = question["explanation"]
        explanation["summary"] = draft["summary"]
        explanation["concept"] = draft["concept"]
        explanation["answerReason"] = draft["answerReason"]
        explanation["optionAnalysis"] = {
            label: draft["optionAnalysis"][label] for label in "ABCD"
        }
        explanation["trap"] = draft["trap"]
        explanation["references"] = draft["references"]
        explanation["editorialNote"] = draft.get("editorialNote", DEFAULT_NOTE)
        explanation["author"] = AUTHOR
        explanation["authoredAt"] = AUTHORED_AT
        explanation.pop("reviewer", None)
        explanation.pop("reviewedAt", None)
        question["explanationStatus"] = "draft"
        written += 1

    QUESTIONS.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    drafts = sum(1 for q in questions if q["explanationStatus"] == "draft")
    print(f"Wrote {written} explanation drafts; {drafts} drafts in {QUESTIONS}")


if __name__ == "__main__":
    main()
