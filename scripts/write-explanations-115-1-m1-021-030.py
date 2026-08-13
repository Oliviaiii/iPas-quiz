"""Write explanation drafts for 115-1 intermediate subject one, Q21-Q30.

The script validates each official answer before writing, refuses to overwrite
reviewed content, and leaves every generated explanation in ``draft`` status.

Usage::

    python scripts/write-explanations-115-1-m1-021-030.py
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
    "bf93f438f7be48d295c1b40a34d79f3d/"
    "115年第一次中級AI應用規劃師_第一科_人工智慧技術應用與規劃_"
    "公告試題_20260615003359.pdf"
)
OPENAI_PROMPT_CACHING = "https://platform.openai.com/docs/guides/prompt-caching"
OPENAI_BATCH = "https://platform.openai.com/docs/guides/batch"
GOOGLE_MLOPS = (
    "https://cloud.google.com/architecture/mlops-continuous-delivery-and-"
    "automation-pipelines-in-machine-learning"
)
PYTORCH_TRANSFER = (
    "https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html"
)
PYTORCH_QUANTIZATION = "https://docs.pytorch.org/docs/stable/quantization.html"
GOOGLE_SRE_MONITORING = (
    "https://sre.google/sre-book/monitoring-distributed-systems/"
)
NIST_AI_RMF = "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf"
NIST_XAI = "https://nvlpubs.nist.gov/nistpubs/ir/2021/NIST.IR.8312.pdf"
FDA_GMLP = (
    "https://www.fda.gov/medical-devices/software-medical-device-samd/"
    "good-machine-learning-practice-medical-device-development-guiding-principles"
)
SHAP_TREE = "https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html"
GRAD_CAM = (
    "https://openaccess.thecvf.com/content_iccv_2017/html/"
    "Selvaraju_Grad-CAM_Visual_Explanations_ICCV_2017_paper.html"
)
SKLEARN_PCA = (
    "https://scikit-learn.org/stable/modules/decomposition.html#principal-"
    "component-analysis-pca"
)

DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


def exam_ref(number: int) -> dict:
    return ref(
        "115 年第一次中級 AI 應用規劃師－人工智慧技術應用與規劃公告試題",
        EXAM_PDF,
        f"第 {number} 題題幹、選項與官方答案",
    )


EXPECTED_ANSWER = {
    21: "B", 22: "C", 23: "B", 24: "D", 25: "B",
    26: "D", 27: "A", 28: "B", 29: "C", 30: "C",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[21] = {
    "summary": "正確答案是 B。成本主要來自重複且冗長的輸入，因此重用穩定前綴並摘要壓縮對話歷史，最能直接減少計費輸入又保留回答所需語意。",
    "concept": (
        "大型語言模型的請求成本取決於實際輸入與輸出 token；題目已指出主要成本集中於輸入，"
        "而完整歷史平均達 8,000 tokens。Prompt Caching 適合內容與順序一致的長前綴，可降低重複"
        "前綴的處理成本；對話摘要則把舊訊息濃縮為任務、事實、決策與未完成事項，減少每輪都"
        "重送全文。兩者分別處理重複前綴與持續膨脹的歷史，但摘要品質仍須以問答評測驗證。"
    ),
    "answerReason": (
        "B 對準最大的兩個輸入來源：穩定的系統說明可組成可快取前綴，8,000-token 對話歷史可"
        "用摘要保留必要語意。這能在不更換模型的前提下實質降低輸入成本；相較之下，A、D 只"
        "處理較少的輸出，C 的非同步批次模式也不適合需要立即回覆的互動式法律問答。"
    ),
    "optionAnalysis": {
        "A": (
            "max_tokens 是輸出上限，適合防止異常冗長回覆；但目前平均輸出僅 300 tokens，強制"
            "降至 200 可能截斷法律說明或引用。題目成本主因是上萬個輸入 tokens，僅壓輸出既未"
            "處理主要來源，也可能犧牲完整性。"
        ),
        "B": (
            "正確。把不變內容放在一致的提示前綴以提高快取命中率，並把舊對話壓縮成可驗證的"
            "語意摘要，可同時降低重複前綴與歷史訊息的輸入成本；實作後仍應以法律問答集檢查"
            "引用正確性與資訊遺失。"
        ),
        "C": (
            "Batch API 適合可等待的離線大量工作，能以非同步方式處理並降低費用；法律文件對話"
            "通常需要即時互動，不能接受批次完成窗口。它也不會縮短單次請求內的 8,000-token"
            "歷史或檢索內容，因此不是此即時系統的最佳組合。"
        ),
        "D": (
            "要求簡短回答可能降低部分輸出，適合控制文風，但模型仍會讀取全部檢索區塊、系統"
            "提示與完整歷史，輸入費用不變。且『盡量簡短』不是硬性 token 控制，法律回答若過度"
            "精簡還可能漏掉條件、例外或依據。"
        ),
    },
    "trap": (
        "先比較成本落在哪一側：題目明說輸入為主，就不能只縮輸出。Prompt Caching 也不是把"
        "任何文字自動免費化；前綴內容、排列與模型支援條件會影響命中，仍須查看實際 usage。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。題幹中的 GPT-4o 價格"
        "屬考題當時設定，實際費率、快取門檻與支援條件可能變動；部署時應查核當期官方文件。"
    ),
    "references": [
        exam_ref(21),
        ref(
            "OpenAI API Docs－Prompt caching",
            OPENAI_PROMPT_CACHING,
            "說明快取依賴相同提示前綴、快取命中與 cached_tokens usage 欄位",
        ),
        ref(
            "OpenAI API Docs－Batch API",
            OPENAI_BATCH,
            "說明 Batch API 的非同步處理、費用優惠與完成時間窗口",
        ),
    ],
}

DRAFTS[22] = {
    "summary": "正確答案是 C。MLOps 的核心是把資料、訓練、測試、部署、監控與再訓練串成可自動化、可版本化且可追溯的機器學習生命週期。",
    "concept": (
        "MLOps 將 DevOps 的自動化、持續整合與交付概念延伸到機器學習，額外管理資料、特徵、"
        "模型、實驗與線上效能。成熟流程會保存程式碼、資料與模型版本，經自動測試及審核後"
        "部署，並監測服務品質、資料漂移與模型表現；觸發條件成立時，再進入重新訓練與驗證。"
        "它是一套跨角色的流程與治理能力，不是單一訓練演算法或保證模型永不退化的工具。"
    ),
    "answerReason": (
        "題幹要求從訓練到再訓練的自動化串接及版本可追溯，C 同時涵蓋管線自動化、版本管理、"
        "部署、監控與持續更新，完整對應需求。資料標註與 AutoML 都可能是管線中的環節，但"
        "範圍不足；MLOps 也不會免除上線後的維運。"
    ),
    "optionAnalysis": {
        "A": (
            "資料標註與品質控管用來提高訓練資料可信度，是資料工程及資料治理的重要工作，"
            "也可納入 MLOps 管線；但它未涵蓋模型版本、部署、線上監控與再訓練，不能代表"
            "題目所問的完整生命週期角色。"
        ),
        "B": (
            "自動模型搜尋與超參數調整屬於 AutoML 或實驗最佳化，可降低部分建模工作量；它"
            "著重找模型，不負責從測試、核准、部署到線上監控及版本追蹤，因此只是 MLOps"
            "流程可能整合的一個元件。"
        ),
        "C": (
            "正確。MLOps 建立可重複的訓練與驗證管線、登錄模型與相關版本，並透過自動化部署"
            "和監控形成回饋迴路；發現漂移或效能未達門檻後，能依治理規則啟動更新與再驗證。"
        ),
        "D": (
            "監控確實有助於維持服務穩定，但資料與環境會改變，模型仍可能漂移並需要更新。"
            "MLOps 的價值是讓維運、回訓及發布更受控且可重現，而不是減少到不再需要後續"
            "維護；此選項把目標說成不切實際的保證。"
        ),
    },
    "trap": (
        "不要把 MLOps 縮成『自動調參』或『模型上線』。題目列出的箭頭是一整條生命週期，"
        "還特別要求版本可追溯，故答案必須同時涵蓋自動化、監控、版本與持續更新。"
    ),
    "references": [
        exam_ref(22),
        ref(
            "Google Cloud Architecture Center－MLOps: Continuous delivery and automation pipelines in machine learning",
            GOOGLE_MLOPS,
            "說明 ML 系統的 CI、CD、CT、自動化管線、部署與持續監控",
        ),
    ],
}

DRAFTS[23] = {
    "summary": "正確答案是 B。少量瑕疵樣本適合以預訓練視覺模型移轉學習，再以量化或蒸餾降低地端推論負擔，並用實機測試確認 100 毫秒需求。",
    "concept": (
        "移轉學習（Transfer Learning）利用模型在大型資料集已學到的通用邊緣、紋理與形狀表示，"
        "再針對目標瑕疵資料微調，通常比從零訓練大型網路更節省資料與運算。量化以較低精度"
        "表示權重或運算，知識蒸餾則讓較小學生模型模仿較大教師模型，兩者都可能降低模型大小"
        "與延遲。不過最終速度取決於硬體、前處理、模型與執行環境，必須在地端原型實測。"
    ),
    "answerReason": (
        "B 同時回應樣本有限、無 GPU、必須地端推論、100 毫秒延遲及中等預算。預訓練模型減少"
        "從零學習所需資料，微調適應瑕疵類別，再以量化或蒸餾建立較輕量版本，比採購大型 GPU、"
        "無期限等待資料或改成雲端傳輸更符合第一階段限制。"
    ),
    "optionAnalysis": {
        "A": (
            "大型 CNN 從零訓練通常需要更多資料、訓練時間與算力；現有瑕疵樣本僅 800 張，"
            "過度擬合風險較高。另採購高階 GPU 與題目的短期預算限制衝突，尚未先證明較小"
            "模型在現有 CPU 上無法達標。"
        ),
        "B": (
            "正確。預訓練權重可在有限標註下提供有效視覺表示，Fine-tuning 讓模型適應產線"
            "瑕疵；量化或蒸餾則可降低計算量與記憶體占用。完成後要以代表性影像在實際地端"
            "硬體做端到端延遲與準確率驗收。"
        ),
        "C": (
            "增加瑕疵樣本通常能改善涵蓋度，但『至少 10 萬筆』不是普遍成立的啟動門檻。"
            "在 800 張樣本可先分層切分、做資料增強與移轉學習原型，同時持續蒐集困難案例；"
            "直接暫緩會錯失低成本驗證可行性的機會。"
        ),
        "D": (
            "雲端 AutoML 可縮短部分訓練與部署工作，適合網路、資料治理和延遲皆允許的情境；"
            "本題明定必須地端即時推論，影像上傳還增加網路往返、斷線風險與資料外送議題，"
            "因此不符合關鍵部署邊界。"
        ),
    },
    "trap": (
        "『樣本少』不等於只能停案，也不等於移轉學習必然成功；應以分層驗證及新增資料評估。"
        "模型壓縮也不保證自動達到 100 毫秒，題目選的是最佳規劃，實作仍須在目標硬體量測。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。選項 B 是限制下最佳"
        "方向，但量化或蒸餾後的準確率與端到端延遲必須實測，不能僅憑技術名稱保證達標。"
    ),
    "references": [
        exam_ref(23),
        ref(
            "PyTorch Tutorials－Transfer Learning for Computer Vision",
            PYTORCH_TRANSFER,
            "示範以預訓練網路微調，或固定特徵抽取器後訓練分類層",
        ),
        ref(
            "PyTorch Documentation－Quantization",
            PYTORCH_QUANTIZATION,
            "說明量化以較低精度執行計算及其部署相關工作流程",
        ),
    ],
}

DRAFTS[24] = {
    "summary": "正確答案是 D。延遲測試量測的是請求從送入系統到取得預測結果所經過的時間，並確認其分布是否符合交易流程的回應門檻。",
    "concept": (
        "延遲（Latency）描述單次請求完成所需時間，應先界定量測邊界，例如只量模型運算，"
        "或包含驗證、特徵查詢、序列化、網路與後處理的端到端時間。即時詐欺偵測不能只看"
        "平均值，還要觀察 p95、p99 等尾端延遲，並在接近實際併發量、硬體及資料分布下測試。"
        "記憶體、穩健性與群體公平性也重要，但它們分別屬資源、安全及公平評估。"
    ),
    "answerReason": (
        "交易核准受回應時間限制，D 直接量測輸入抵達到預測產生的時間是否低於系統要求，"
        "正是 Latency Testing 的目標。其他選項雖可能影響上線品質，評估的卻不是時間，不能"
        "用來回答模型是否在交易時限內完成。"
    ),
    "optionAnalysis": {
        "A": (
            "記憶體量測用於容量規劃、避免記憶體不足及估算可同時載入的模型數量，屬資源"
            "使用測試。記憶體不足可能間接拖慢服務，但記憶體用量本身不是從輸入到輸出的"
            "經過時間，仍需另量 latency。"
        ),
        "B": (
            "對異常或攻擊輸入測試可評估魯棒性與安全性，例如輸入操弄是否造成錯判或服務"
            "失效；其主要輸出是攻擊成功率、效能退化或失敗模式，不是交易請求的回應時間"
            "是否達到服務等級。"
        ),
        "C": (
            "比較不同使用者族群的錯誤率或決策結果，是公平性與偏差評估，用於找出群體間"
            "不合理差距。即使各群結果一致，系統仍可能回應太慢；反之低延遲也不能證明模型"
            "對各族群公平。"
        ),
        "D": (
            "正確。延遲測試在定義好的量測起訖點記錄每筆請求完成時間，並以平均值與百分位"
            "延遲檢查是否符合交易核准門檻；若要求端到端，還應納入特徵取得、網路與後處理。"
        ),
    },
    "trap": (
        "不要把 latency 與 throughput 混淆：前者是單次請求等多久，後者是單位時間處理多少。"
        "也不能只看平均延遲，少數極慢請求可能正是即時交易最需要發現的風險。"
    ),
    "references": [
        exam_ref(24),
        ref(
            "Google Site Reliability Engineering－Monitoring Distributed Systems",
            GOOGLE_SRE_MONITORING,
            "The Four Golden Signals 的 latency 定義，以及區分成功與失敗請求延遲的說明",
        ),
    ],
}

DRAFTS[25] = {
    "summary": "正確答案是 B。保存可追溯的測試資料、流程、模型版本與關鍵設定，第三方才能在相同條件下重跑評估並核對結果。",
    "concept": (
        "可驗證性要求主張能由證據與重複執行來檢查，而不只是提供一個漂亮的準確率。外部稽核"
        "要能辨識用的是哪一版程式、模型、資料切分、前處理、評估指標、隨機種子與執行環境，"
        "並取得不可混淆的輸出紀錄。NIST AI RMF 的 MEASURE 功能要求採用客觀、可重複或可擴充"
        "的測試、評估、驗證與確認（TEVV）流程，且方法、指標與結果應被記錄。"
    ),
    "answerReason": (
        "B 建立從測試資料到評估結果的證據鏈，並記錄重現所需的訓練與評估設定，稽核者才能"
        "獨立執行及比較。單一高準確率、快速發布或大量資料都可能有其他價值，但若版本、"
        "切分與方法不可追溯，仍無法驗證當初宣稱的結果。"
    ),
    "optionAnalysis": {
        "A": (
            "99% 準確率只是特定資料與指標下的數值，且不存在適用所有 AI 系統的業界可靠"
            "門檻。若沒有測試集來源、切分、類別分布與評估程式，第三方無從判斷數字是否"
            "可重現，也可能被類別不平衡誤導。"
        ),
        "B": (
            "正確。版本化測試資料與流程，連同模型雜湊、程式版本、參數、環境和評估輸出"
            "留下紀錄，可讓第三方在界定條件下重跑並查明差異，最直接形成可驗證、可追溯"
            "且可重現的稽核證據。"
        ),
        "C": (
            "縮短發布週期有助於快速取得回饋，屬產品迭代與交付效率；版本發布得快並不代表"
            "每版使用的資料、設定與指標已被記錄。缺少重現材料時，更多外部結果仍無法核對"
            "某次模型評估主張。"
        ),
        "D": (
            "擴大資料量可能改善涵蓋度並降低部分抽樣誤差，但數百萬筆不是泛化能力的充分"
            "條件；資料若偏差、重複或切分洩漏，結果仍不可靠。它也沒有提供版本、流程及"
            "參數紀錄供第三方重跑。"
        ),
    },
    "trap": (
        "可驗證性問的是『別人能否依證據核對』，不是準確率是否很高。重現也必須限定資料、"
        "程式、環境與容許誤差；只留模型檔或報表，通常不足以還原完整評估。"
    ),
    "references": [
        exam_ref(25),
        ref(
            "NIST AI Risk Management Framework 1.0",
            NIST_AI_RMF,
            "MEASURE 2：客觀、可重複或可擴充的 TEVV 流程及其指標、方法與結果應被記錄",
        ),
    ],
}

DRAFTS[26] = {
    "summary": "正確答案是 D。要向每位被拒絕申請人說明該次決策的具體原因，系統必須能產生與個案輸入及模型輸出相連的可解釋資訊。",
    "concept": (
        "可解釋性（Explainability）關注系統如何形成特定輸出，以及哪些因素影響該筆決策。"
        "授信系統可依模型型態使用可讀規則、係數、特徵歸因或局部代理方法，但產生的理由必須"
        "忠實反映模型、讓目標受眾理解，並接受穩定性與正確性驗證。『特徵貢獻』是實作方式之一，"
        "不等於完整合規；還要把技術歸因轉成可理解、可申訴且不揭露不當資訊的理由。"
    ),
    "answerReason": (
        "題目要求的是逐筆拒絕理由，D 提供個案層級的特徵貢獻說明，能指出哪些輸入把該次"
        "預測推向拒絕，因此最直接對應核心能力。刪除個資、隨機決策及不可能的 100% 準確率"
        "都不能解釋某位申請人為何被拒絕。"
    ),
    "optionAnalysis": {
        "A": (
            "資料刪除時限屬個資保存與生命週期控制，可能因法規、同意或業務目的而有不同"
            "要求；即使在 10 秒內刪除，也不會產生本次拒絕的因素說明，反而可能破壞申訴與"
            "稽核所需的受控紀錄。"
        ),
        "B": (
            "隨機調整結果會讓相同條件可能得到不同決策，既不能說明原模型理由，也可能損害"
            "一致性與公平性。多元性或偏差管理應靠適當資料、評估與控制，而不是任意改變"
            "個別授信結果。"
        ),
        "C": (
            "準確率衡量模型在有標籤資料上的整體預測表現，不能解釋單一申請案；而真實資料"
            "存在雜訊與分布變化，要求所有決策 100% 正確也不切實際。高準確率與可解釋性是"
            "不同的可信任特性。"
        ),
        "D": (
            "正確。個案層級的特徵貢獻可說明收入、負債或信用紀錄等因素如何推動該次模型"
            "輸出，提供建立拒絕理由的技術基礎；仍應檢驗解釋忠實度，並依適用法規設計"
            "通知、人工覆核與申訴流程。"
        ),
    },
    "trap": (
        "不要把『模型整體準確』當成『單筆決策可說明』。也不要把 SHAP 等特徵歸因直接等同"
        "法律上已充分告知；技術解釋還需配合受眾、流程與實際監理要求。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非法律或金融合規意見，亦非官方詳解；尚待獨立人工"
        "複核。實際授信理由通知、資料保存、人工覆核與申訴義務應依適用法域及主管機關規範確認。"
    ),
    "references": [
        exam_ref(26),
        ref(
            "NIST IR 8312－Four Principles of Explainable Artificial Intelligence",
            NIST_XAI,
            "解釋應提供理由或證據、對個別使用者有意義、準確反映系統流程並在知識限制內運作",
        ),
        ref(
            "NIST AI Risk Management Framework 1.0",
            NIST_AI_RMF,
            "可信任 AI 的 explainable and interpretable 特性，以及治理與文件化脈絡",
        ),
    ],
}

DRAFTS[27] = {
    "summary": "正確答案是 A。人命攸關的影像輔助診斷應把 AI 定位為決策支援，保留醫師檢視、推翻與承擔最終臨床判斷的人機協作控制。",
    "concept": (
        "Human-in-the-Loop（HITL）把具權限與專業能力的人類安排在關鍵決策點，讓人能檢視模型"
        "輸出、原始影像、信心與限制，必要時拒絕建議或轉交其他流程。這不只是介面上多一個"
        "確認鍵；系統還要定義低信心、輸入品質不良與分布外案例的處置，避免自動化偏誤，並"
        "留下模型建議、醫師判斷與覆寫理由供監測。AI 可輔助，但不能模糊最終責任。"
    ),
    "answerReason": (
        "A 明確把 AI 輸出交由放射科醫師最終審核，使專業人員能結合病史、影像品質及臨床"
        "脈絡決定是否採納，直接滿足題目『最終決策責任由人類承擔』的架構要求。其餘選項"
        "不是把低信心案例安全轉交人類，就是加入與臨床責任無關的隨機性。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。HITL 保留醫師對每一關鍵診斷的審核與覆寫權，AI 作為輔助資訊而非最終"
            "裁決者；搭配輸入品質檢查、低信心升級、稽核紀錄及持續監測，能建立可操作的"
            "臨床安全邊界。"
        ),
        "B": (
            "信心閾值可用來識別模型不確定案例，但低於閾值就整個自動關機會中斷所有服務，"
            "也沒有把該案例安全轉交醫師。較合理的是標示不確定、停用該筆自動建議並觸發"
            "人工判讀，而非把關機當作最終責任機制。"
        ),
        "C": (
            "模型集成與多數決可在模型錯誤不完全相關時改善穩定性，但隨機切換缺乏可預期的"
            "選擇依據，多數模型也可能共享相同偏差。即使集成結果一致，仍沒有讓醫師保有"
            "最終臨床審核與責任。"
        ),
        "D": (
            "隨機擾動可用於資料增強、魯棒性測試或特定隱私方法，但在實際診斷輸入任意加噪"
            "可能遮蔽病灶或改變模型輸出。它沒有建立人工審核點，也不能確保醫師承擔最後"
            "決策。"
        ),
    },
    "trap": (
        "低信心閾值是『何時升級處理』的訊號，HITL 才回答『由誰做最後決策』。此外，人工"
        "簽核不會自動消除風險；介面必須提供足夠資訊，並防止醫師無條件照單全收。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非醫療器材法規或臨床建議，亦非官方詳解；尚待獨立"
        "人工複核。實際系統仍須依產品風險、預定用途與所在地法規完成臨床及安全驗證。"
    ),
    "references": [
        exam_ref(27),
        ref(
            "FDA, Health Canada and MHRA－Good Machine Learning Practice Guiding Principles",
            FDA_GMLP,
            "Human-AI team performance 原則：在預定使用環境重視人因與人機團隊整體表現",
        ),
        ref(
            "NIST AI Risk Management Framework 1.0",
            NIST_AI_RMF,
            "GOVERN 與 MANAGE 對角色責任、人類監督及風險處置的框架要求",
        ),
    ],
}

DRAFTS[28] = {
    "summary": "正確答案是 B。SHAP 值表示個別特徵相對於基準值把該樣本的模型輸出往哪個方向推動多少；-2.3 是負向 2.3 個模型輸出單位。",
    "concept": (
        "SHAP 以 Shapley value 將單筆預測相對於基準輸出的差額分配給各特徵，概念上滿足"
        "f(x) = base value + 各特徵 SHAP 值總和。正負號代表推動模型輸出的方向，絕對值才"
        "反映該特徵對這一筆預測的影響幅度。單位取決於解釋器設定：XGBoost 二元分類若解釋"
        "raw output，通常是 margin 或 log-odds；只有明確解釋 probability output 才能以機率尺度理解。"
    ),
    "answerReason": (
        "B 保留 SHAP 的相對基準與模型輸出尺度：月收入的 -2.3 表示它使這一筆的輸出往負"
        "方向移動，依題目把正向定義為較高違約風險時，便是降低風險的貢獻。它沒有像 A"
        "直接把未說明尺度的 2.3 當百分比，也沒有把局部方向誤當全域重要性。"
    ),
    "optionAnalysis": {
        "A": (
            "SHAP 值的單位跟被解釋的模型輸出一致，不會因數值是 -2.3 就自動代表機率降低"
            "2.3%。XGBoost 二元分類的預設 raw output 常是 margin 或 log-odds；若要解釋機率，"
            "須明確選用 probability output 並按該尺度解讀。"
        ),
        "B": (
            "正確。-2.3 表示相對 base value，月收入對此申請人的模型輸出貢獻為負 2.3 個"
            "輸出單位；在輸出越高代表違約風險越高的設定下，它把本筆預測往較低風險方向"
            "推動，仍須配合模型實際輸出尺度說明。"
        ),
        "C": (
            "負號只表示這個特徵在該筆樣本把輸出往負方向推，不表示影響小；-2.3 的絕對值"
            "反而可能相當大。全域重要性通常彙整許多樣本的 SHAP 絕對值，不能用單一樣本的"
            "正負號決定是否刪除特徵。"
        ),
        "D": (
            "+1.8 說明負債比率對這一筆預測的局部正向貢獻，不能推出它在整個訓練集最大。"
            "比較全域重要性要彙整代表性資料上各特徵的影響，例如平均絕對 SHAP 值，且還要"
            "考慮特徵相關性與資料分布。"
        ),
    },
    "trap": (
        "SHAP 的符號是方向，不是重要或不重要；數值單位也不是固定百分比。先確認模型輸出"
        "是 raw margin、log-odds 還是 probability，再區分單筆局部解釋與整體特徵重要性。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。選項 B 的『2.3 個"
        "單位』必須依 TreeExplainer 的 model_output 解讀；若為 XGBoost 二元分類預設 raw output，"
        "通常是 margin／log-odds，不應直接視為違約機率百分點。"
    ),
    "references": [
        exam_ref(28),
        ref(
            "SHAP Documentation－shap.TreeExplainer",
            SHAP_TREE,
            "model_output 說明：XGBoost 二元分類 raw output 為 log-odds；probability 模式才加總到機率輸出",
        ),
    ],
}

DRAFTS[29] = {
    "summary": "正確答案是 C。Grad-CAM 利用目標類別對卷積特徵圖的梯度產生類別辨識熱區，不需像 LIME 或 Kernel SHAP 進行大量擾動採樣，最符合近即時 CNN 影像解釋。",
    "concept": (
        "Grad-CAM 將目標類別分數對最後卷積層特徵圖的梯度做全域平均，取得每張特徵圖的"
        "重要性權重，再加權組合並經 ReLU 形成粗略的類別關注圖，最後放大疊回原影像。它"
        "使用模型的一次前向與梯度反向傳播即可產生類別相關區域，通常比需要建立大量擾動"
        "樣本的模型無關方法更適合低延遲；但 200 毫秒能否達標仍取決於模型與硬體實測。"
    ),
    "answerReason": (
        "C 專為 CNN 類別決策提供梯度式空間定位，輸出可直接呈現影像中的代表性關注區域，"
        "且不必大量重複採樣，三項需求都能對應。LIME 與 KernelExplainer 需要多次擾動和"
        "推論，TreeExplainer 則是針對樹模型，與 CNN 架構不相符。"
    ),
    "optionAnalysis": {
        "A": (
            "影像 LIME 把影像切成超像素，反覆開關區塊並對擾動樣本推論，再擬合局部代理模型；"
            "它能提供局部區塊解釋且不依賴 CNN 內部梯度，但大量採樣使延遲與結果穩定性較難"
            "符合本題 200 毫秒限制。"
        ),
        "B": (
            "Kernel SHAP 是模型無關的 Shapley 值近似，可用於無法存取模型內部結構的情境；"
            "若把大量像素當特徵，組合空間極大，需要許多遮罩樣本與重複推論，運算成本和"
            "視覺連貫性均不利於近即時需求。"
        ),
        "C": (
            "正確。Grad-CAM 利用目標類別梯度對卷積特徵圖加權，形成類別相關的粗略定位圖，"
            "能疊回 CT 影像顯示模型關注區域；它避開大量擾動採樣，較適合以一次梯度計算"
            "提供近即時視覺解釋。"
        ),
        "D": (
            "TreeExplainer 利用樹集成結構高效計算 SHAP 值，適合 XGBoost、LightGBM 等樹模型；"
            "CNN 的卷積層不是決策樹路徑，因此不能用 TreeExplainer 直接產生其影像類別關注圖。"
            "即使另訓練樹代理模型，也不是原 CNN 的梯度式定位。"
        ),
    },
    "trap": (
        "方法都能叫『可解釋』，但計算機制與模型相依性不同：LIME、Kernel SHAP 靠擾動採樣，"
        "TreeExplainer 對應樹模型，Grad-CAM 才直接利用 CNN 卷積特徵與類別梯度。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非醫療判讀建議或官方詳解；尚待獨立人工複核。Grad-CAM"
        " 產生的是粗略關注區域，不能單獨證明因果或臨床正確性；200 毫秒也須在目標硬體實測。"
    ),
    "references": [
        exam_ref(29),
        ref(
            "Selvaraju et al.－Grad-CAM: Visual Explanations From Deep Networks via Gradient-Based Localization (ICCV 2017)",
            GRAD_CAM,
            "原始論文摘要與方法：以流入最後卷積層的目標概念梯度產生粗略定位圖",
        ),
    ],
}

DRAFTS[30] = {
    "summary": "正確答案是 C。PCA 可對中心化資料的協方差矩陣做特徵值分解，取最大特徵值所對應的特徵向量作為最大變異方向。",
    "concept": (
        "主成分分析（PCA）是在不使用目標標籤的情況下，找出彼此正交且依序解釋最大資料變異"
        "的方向。對中心化資料建立協方差矩陣後，特徵向量給出候選方向，對應特徵值表示沿該"
        "方向的變異量；依特徵值由大到小選取，即得到主成分。實作上也常直接對中心化資料矩陣"
        "做奇異值分解（SVD），其右奇異向量與協方差矩陣特徵向量具有對應關係。"
    ),
    "answerReason": (
        "C 描述 PCA 的典型線性代數推導：協方差矩陣的最大特徵值對應方向具有最大投影變異，"
        "後續特徵向量依序給出互相正交的次要方向。題目先標準化 200 個感測器特徵，也符合"
        "避免原始尺度使大數值特徵主導變異的處理脈絡。"
    ),
    "optionAnalysis": {
        "A": (
            "梯度下降是一般最佳化方法，某些大型或線上 PCA 變體可用迭代方法近似主成分；"
            "但標準 PCA 的核心閉式關係是協方差矩陣的特徵值問題，或等價的 SVD，不需要把"
            "梯度下降當作主要數學操作。"
        ),
        "B": (
            "依特徵與目標的相關性排序屬監督式特徵選擇，會保留部分原始欄位；PCA 不使用"
            "目標變數，而是把原特徵線性組合成新的主成分，最佳化的是資料投影變異，不是"
            "與標籤的相關程度。"
        ),
        "C": (
            "正確。協方差矩陣是對稱矩陣，其特徵向量形成正交方向，特徵值表示各方向的變異量；"
            "選取最大特徵值對應向量即可取得第一主成分，依序選取則保留主要變異資訊。"
        ),
        "D": (
            "卷積利用局部共享權重擷取鄰近結構，常見於影像、聲音或序列模型；一般表格中 200"
            "個感測器欄位未必有可平移的局部鄰接關係。標準 PCA 是全域線性投影，不靠卷積"
            "建立主成分。"
        ),
    },
    "trap": (
        "PCA 是特徵萃取，不是依目標挑原始特徵；它保留的是最大變異，也不保證最有預測力。"
        "看到實作使用 SVD 不代表 C 錯，SVD 與協方差矩陣特徵值分解是相互對應的求解方式。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。實務 PCA 常直接對"
        "中心化資料矩陣做 SVD，以避免明確形成協方差矩陣；本題選項 C 是標準數學原理的描述。"
    ),
    "references": [
        exam_ref(30),
        ref(
            "scikit-learn User Guide－Principal component analysis (PCA)",
            SKLEARN_PCA,
            "說明 PCA 以 SVD 投影到最大變異方向，以及與協方差矩陣特徵向量的關係",
        ),
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
