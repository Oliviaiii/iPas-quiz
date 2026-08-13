"""Write draft explanations for 115-1 intermediate subject two, Q31-Q40.

The script verifies official answers, refuses to overwrite reviewed work, and
keeps every generated explanation in ``draft`` for independent review.

Usage::

    python scripts/write-explanations-115-1-m2-031-040.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-intermediate-1-big-data"
AUTHOR = "Codex（AI 輔助初稿）"
AUTHORED_AT = "2026-08-13"
CHECKED_AT = "2026-08-13"

EXAM_PDF = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/115年第一次中級AI應用規劃師_"
    "第二科_大數據處理分析與應用_公告試題_20260615003417.pdf"
)
DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def exam_ref(number: int) -> dict:
    return {
        "title": "115 年第一次中級 AI 應用規劃師－大數據處理分析與應用公告試題",
        "url": EXAM_PDF,
        "locator": f"第 {number} 題題幹、選項與官方答案",
        "checkedAt": CHECKED_AT,
    }


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


EXPECTED_ANSWER = {
    31: "B", 32: "B", 33: "A", 34: "C", 35: "D",
    36: "D", 37: "A", 38: "B", 39: "C", 40: "A",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[31] = {
    "summary": "正確答案是 B。統一管理並共用『過去 30 天交易行為』特徵，可避免兩個團隊各自重做相同轉換與維護工作，降低跨團隊重複開發成本。",
    "concept": (
        "特徵平台或 Feature Store 會集中定義特徵的來源、轉換邏輯與中繼資料，讓多個模型重用"
        "同一份經驗證的特徵定義。當信用評分與詐欺偵測都需要相同交易窗口時，若各自建立管線，"
        "欄位定義、時間邊界、修正與監控都要維護兩次，也容易產生口徑不一致。共用特徵的直接"
        "治理價值是減少重工並提高一致性；線上延遲、儲存容量與模型版本則屬其他系統層面的問題。"
    ),
    "answerReason": (
        "題幹明確指出兩團隊需要同一基礎資料、但各自做特徵工程，因此公司層級最直接的痛點是"
        "重複定義與維護。B 所述的跨團隊維護成本正是統一註冊、共享與治理特徵要解決的核心問題。"
    ),
    "optionAnalysis": {
        "A": "推論延遲取決於線上儲存、網路、模型計算與服務架構；Feature Store 可提供低延遲取用能力，但題幹只描述兩團隊重複使用相同資料，未指出服務回應過慢。",
        "B": "正確。共用同一個經驗證的 30 天交易特徵定義與轉換管線，可避免兩團隊重複撰寫、測試、修正與監控相同邏輯，也降低口徑分歧。",
        "C": "資料儲存空間不足應從保留政策、壓縮、分區與儲存架構處理；統一特徵可能減少部分重複產物，但題目的主要目的不是解決原始訓練資料容量。",
        "D": "模型版本管理追蹤的是模型成品、參數與部署生命週期；特徵統一管理著重特徵定義、血緣與取用，兩者可整合但不能以特徵共用取代模型登錄。",
    },
    "trap": "不要看到『統一管理』就把所有 MLOps 問題都歸入同一答案；先找題幹的重複物件。本題重複的是特徵工程，所以主要收益是重用與一致性。",
    "references": [
        exam_ref(31),
        ref(
            "Feast 官方文件－Introduction",
            "https://docs.feast.dev/",
            "Feature Store 定義、管理、驗證及提供特徵，並支援團隊協作與一致的訓練／服務特徵取用",
        ),
    ],
}

DRAFTS[32] = {
    "summary": "正確答案是 B。在切分前對全體資料執行 SMOTE，會讓測試資料參與合成樣本的近鄰計算，造成資料洩漏，使測試 AUC-ROC 過度樂觀。",
    "concept": (
        "測試集必須模擬完全未見資料。SMOTE 會依少數類樣本及其近鄰插值產生合成點；若先對"
        "完整資料 SMOTE 再切分，原本應隔離的測試樣本已影響合成資料，且高度相似的原始／合成"
        "樣本可能分散在訓練與測試兩側。正確流程是先保留測試集，再只對訓練資料重採樣；進行"
        "交叉驗證時，SMOTE 也必須放入 pipeline，僅在每一折的訓練部分 fit_resample。"
    ),
    "answerReason": (
        "B 指出評估失真的因果來源：測試資訊在模型訓練前已透過 SMOTE 進入資料處理。這使 0.91"
        "不能視為獨立泛化證據。PR-AUC 雖值得補充，但更換指標無法修復已發生的資料洩漏。"
    ),
    "optionAnalysis": {
        "A": "SMOTE 並非金融場景一律禁用；是否適合要看特徵距離、合成樣本合理性與驗證結果。class_weight 是另一種可選方法，但不能由業務類型推導出唯一處理方式。",
        "B": "正確。SMOTE 在全資料上尋找近鄰，讓測試樣本資訊影響合成點；切分後訓練資料因此不再獨立於測試資料，測試分數可能虛高。",
        "C": "1.6% 正類時 PR-AUC 能更聚焦正類 precision-recall，ROC-AUC 也可能掩蓋實務誤報量；但選項稱其餘流程均正確，忽略切分前 SMOTE 的根本洩漏。",
        "D": "LightGBM 提供 class_weight、is_unbalance 等參數，但不是自動且無條件處理所有不平衡問題；與 SMOTE 併用可能過度補償，卻不是本題測試分數失真的主要原因。",
    },
    "trap": "任何會從多筆樣本學習參數或鄰近關係的步驟，都要在切分後只對訓練集 fit。指標選擇與資料切分是兩道不同檢查，不能用 PR-AUC 掩蓋洩漏。",
    "references": [
        exam_ref(32),
        ref(
            "imbalanced-learn－Common pitfalls and recommended practices",
            "https://imbalanced-learn.org/stable/common_pitfalls.html",
            "Data leakage：在切分前重採樣會讓模型看見本應留在測試集的資訊，建議使用 pipeline",
        ),
        ref(
            "imbalanced-learn API－SMOTE",
            "https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html",
            "SMOTE 依 k-nearest neighbors 對少數類執行過採樣的參數與介面",
        ),
    ],
}

DRAFTS[33] = {
    "summary": "正確答案是 A。多類別羅吉斯迴歸可直接利用完整標註資料預測 8 類機率，訓練與推論效率高，也容易封裝成線上分類服務。",
    "concept": (
        "Multinomial Logistic Regression 是監督式多類別分類器，以 softmax 將各類別線性分數轉成"
        "總和為 1 的類別機率，並共同最佳化多類別損失。數十萬筆結構化資料在特徵妥善編碼後，"
        "線性模型通常能以成熟的數值最佳化器有效訓練，模型大小及線上推論成本也相對可控。SVM"
        "的 One-vs-One 對 8 類需訓練 8×7/2=28 個二元分類器；K-means 與 PCA 本身不利用類別標籤。"
    ),
    "answerReason": (
        "四個選項中只有 A 同時是直接支援多類別標註的監督式分類方法，且能兼顧大樣本訓練、"
        "擴充與快速推論。它不保證一定具有最高準確率，但在題目列出的候選方法中最符合完整需求。"
    ),
    "optionAnalysis": {
        "A": "正確。Multinomial loss 共同估計 8 類機率，能使用現有標籤訓練；線性決策的參數量與推論計算較小，適合做效率良好的基準及線上部署。",
        "B": "One-vs-One SVM 會為每對類別訓練分類器，8 類需 28 個模型；核心 SVM 在數十萬筆資料上通常訓練成本較高，線上還要彙整多模型決策。",
        "C": "K-means 是依特徵距離分群的非監督式方法，不使用書籍主題標籤；群集編號沒有必然對應 8 個主題，也不能取代已標註的多類別分類。",
        "D": "PCA 是保留最大變異方向的無監督降維，不會尋找最能區分類別的方向；最大主成分是連續座標，也不是 8 類預測標籤。",
    },
    "trap": "先分辨監督式分類、非監督式分群與降維。題目說資料已完整標註，就應選直接學習類別的模型；還要比較 8 類下 One-vs-One 的模型數量。",
    "editorialNote": "本站依官方答案 A 判定。實務上準確率與擴充性仍取決於特徵型態、稀疏度與資料分佈，梯度提升樹等未列入選項的方法也可能更合適；本題結論限定於四個候選選項。",
    "references": [
        exam_ref(33),
        ref(
            "scikit-learn API－LogisticRegression",
            "https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html",
            "multinomial loss、各 solver 的多類別支援與大資料集選擇說明",
        ),
        ref(
            "scikit-learn－Multiclass classification",
            "https://scikit-learn.org/stable/modules/multiclass.html",
            "One-vs-One 需建立 n_classes*(n_classes-1)/2 個分類器及其計算特性",
        ),
    ],
}

DRAFTS[34] = {
    "summary": "正確答案是 C。羅吉斯迴歸是二元監督式分類方法，使用 sigmoid 將線性分數轉成 0 到 1 的估計機率，可輸出商品為高銷量的機率。",
    "concept": (
        "二元羅吉斯迴歸建模的是 log-odds 與特徵的線性關係，經 sigmoid 後得到 P(y=1|x)。品牌、"
        "顏色與材質等無序類別通常先做 One-Hot Encoding，價格區間則依是否具有可信順序選擇"
        "編碼。輸出 0.73 可解讀為模型估計的高銷量機率，但若要讓機率在部署資料中真正對應約"
        "73% 發生率，仍應以獨立驗證資料檢查 calibration，必要時再做機率校準。"
    ),
    "answerReason": (
        "C 同時符合二元分類與機率輸出兩個條件。K-means 沒有類別標籤，決策樹迴歸與線性迴歸"
        "主要預測連續值，輸出也不天然受限於 0 到 1，因此都不是題目描述下的標準選擇。"
    ),
    "optionAnalysis": {
        "A": "K-means 依距離將未標註樣本分群，不會直接學習高銷量 1／低銷量 0 的既有標籤；群集編號也不是經校準的類別機率。",
        "B": "決策樹迴歸以連續目標的平方誤差等準則切分；雖葉節點平均值可能落在 0 到 1，題目已有二元標籤，應使用分類模型而非迴歸版本。",
        "C": "正確。羅吉斯迴歸直接估計二元類別的條件機率，並可用係數方向解釋編碼後特徵如何影響高銷量的 log-odds。",
        "D": "線性迴歸的預測值沒有 0 到 1 邊界，誤差假設也不符合二元結果；它可能產生負值或大於 1 的輸出，不能直接當作合法機率。",
    },
    "trap": "『輸出在 0～1』與『機率已校準』不是同一件事。羅吉斯迴歸提供機率形式，但仍要在部署代表性資料上用校準曲線或 Brier score 檢查可靠度。",
    "editorialNote": "本站依官方答案 C 判定。題目所稱『P=0.73 表示 73% 機率』是模型條件機率輸出的語意；是否具有良好校準需另行驗證，不能只因使用 Logistic Regression 就保證。",
    "references": [
        exam_ref(34),
        ref(
            "scikit-learn－Logistic regression 官方使用指南",
            "https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression",
            "二元 Logistic Regression 的機率模型與 multiclass 延伸",
        ),
        ref(
            "scikit-learn－Probability calibration",
            "https://scikit-learn.org/stable/modules/calibration.html",
            "良好校準分類器的 predict_proba 應與實際正類比例一致及校準檢查方法",
        ),
    ],
}

DRAFTS[35] = {
    "summary": "正確答案是 D。自注意力本身不含詞序，位置編碼把每個 token 的序列位置加入向量表示，讓 Transformer 能區分相同詞出現在不同位置的語意差異。",
    "concept": (
        "Self-attention 對輸入集合計算查詢、鍵和值之間的關聯；若沒有額外位置訊號，交換 token"
        "順序會相應交換輸出，模型本身無從知道第一、第二或相對先後。原始 Transformer 將正弦／"
        "餘弦 positional encoding 與 token embedding 相加，使不同位置具有可辨識表示，也讓模型"
        "能學習相對距離。後續架構也可能使用可學習位置嵌入、相對位置偏置或旋轉位置編碼，但目的相同。"
    ),
    "answerReason": (
        "工程師遇到的是詞序不敏感，D 正面補入序列位置資訊。隨機擾動屬正則化思路，mask 控制"
        "可見範圍，而平行向量運算是 Transformer 的計算特性，都不能單獨讓模型辨認詞語先後。"
    ),
    "optionAnalysis": {
        "A": "在 embedding 加隨機擾動可作資料增強或正則化，可能改善泛化，但隨機值沒有穩定表示第幾個位置，模型仍無法可靠分辨詞序。",
        "B": "Attention mask 用來遮住 padding 或禁止解碼器看到未來 token，控制哪些位置可以互相關注；它不是為每個可見 token 提供位置身分。",
        "C": "把 token 轉為向量是 embedding 的作用，自注意力可平行處理整段序列；若只有這些向量而沒有位置訊號，同樣詞彙換序後仍缺少順序標記。",
        "D": "正確。位置編碼與詞向量結合後，每個 token 同時帶有內容和位置，使注意力能依絕對或相對位置學習語序關係。",
    },
    "trap": "不要把位置編碼與 causal mask 混為一談：位置編碼回答『token 在哪裡』，遮罩回答『這個位置可以看哪些位置』，兩者功能互補。",
    "references": [
        exam_ref(35),
        ref(
            "Attention Is All You Need",
            "https://arxiv.org/abs/1706.03762",
            "Section 3.5 Positional Encoding：因模型沒有 recurrence 或 convolution，必須注入序列順序資訊",
        ),
    ],
}

DRAFTS[36] = {
    "summary": "正確答案是 D。Text-to-SQL Agent 可把自然語言轉成 SQL，再由具權限、審計與分散式執行能力的資料庫引擎完成精確聚合，最符合題目需求。",
    "concept": (
        "Text-to-SQL 的職責是把使用者問題對應到資料庫 schema、欄位與聚合語意，產生可驗證的 SQL；"
        "真正掃描數百億筆資料、執行篩選與統計的是分散式查詢引擎。這個分工讓非技術使用者保留"
        "自然語言介面，同時沿用資料庫的列／欄權限、工作負載控制與查詢日誌。實務上仍須限制只讀"
        "帳號、允許的 schema 與 SQL 類型，檢查生成語句並防止 prompt injection，不能讓 Agent 無限制執行。"
    ),
    "answerReason": (
        "D 是唯一把語言理解交給 LLM、確定性聚合交給資料庫的架構，能在資料留在湖倉／資料庫時"
        "執行新問題。其他方法分別在做推薦、文字檢索生成或合成資料，均不適合精確即時計算任意統計。"
    ),
    "optionAnalysis": {
        "A": "協同過濾依相似使用者或項目推薦，適合商品與內容推薦；重用歷史問題答案無法解析新的篩選條件，也不會對最新資料執行精確 SQL 聚合。",
        "B": "RAG 擅長從文件或小段資料檢索證據供 LLM 生成文字，但不能靠提示上下文掃描數百億筆紀錄並保證精確 GROUP BY、比例與權限語意。",
        "C": "GAN 可學習資料分佈並生成合成樣本，適合資料擴增或模擬；合成資料不是即時查詢真實交易資料的引擎，統計也可能因模型近似而偏差。",
        "D": "正確。Agent 依 schema 將問題轉成 SQL，資料庫以既有權限與審計執行聚合；搭配查詢驗證、只讀角色及資源限制後，可兼顧介面彈性與計算精確性。",
    },
    "trap": "自然語言回答流暢不等於數值正確。看到『數百億筆、精確聚合、資料庫權限與審計』，應讓資料庫執行 SQL，而非把原始資料塞入 LLM 上下文。",
    "editorialNote": "本站依官方答案 D 判定。Text-to-SQL 並不自動保證正確或安全；正式系統仍需 schema grounding、SQL allowlist／parser、最小權限只讀帳號、查詢成本限制、結果驗證與完整審計。",
    "references": [
        exam_ref(36),
        ref(
            "AWS Prescriptive Guidance－Natural language query generation using LLMs and Amazon Redshift",
            "https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/generate-sql-queries-for-amazon-redshift-by-using-generative-ai.html",
            "以 LLM 將自然語言轉為 SQL、由資料倉儲執行查詢的 Text-to-SQL 架構與流程",
        ),
        ref(
            "PostgreSQL 官方文件－Privileges",
            "https://www.postgresql.org/docs/current/ddl-priv.html",
            "以資料庫角色及 SELECT 等權限限制物件存取的機制",
        ),
    ],
}

DRAFTS[37] = {
    "summary": "正確答案是 A。成員推斷利用模型對訓練樣本與未見樣本輸出行為的差異，推測某人的資料是否參與訓練；差分隱私訓練可限制單筆資料對模型的影響。",
    "concept": (
        "Membership Inference Attack 的目標不是還原敏感屬性，而是判斷特定紀錄是否屬於訓練集。"
        "過擬合模型常對訓練樣本給出較高信心或較低 loss，攻擊者可利用機率向量、損失或反覆查詢"
        "建立成員判別器。防禦應從降低訓練與非訓練行為差距著手，例如正則化、早停、只回傳必要"
        "輸出；具正式保證的方法是以裁切梯度與加入雜訊的差分隱私訓練限制單筆樣本影響。"
    ),
    "answerReason": (
        "A 同時正確描述『是否在訓練集』的攻擊目標、以高信心差異推斷的常見訊號，以及差分隱私"
        "等防禦方向。B、C、D 分別混入頻率側通道、屬性推斷與模型竊取，都是不同威脅。"
    ),
    "optionAnalysis": {
        "A": "正確。攻擊者比較目標模型對候選紀錄的信心或損失，判定其是否更像模型見過的樣本；差分隱私可限制個別樣本影響，減少過度暴露輸出也能降低攻擊訊號。",
        "B": "限制查詢頻率可提高大量探測成本，也是 API 防護的一環；但成員推斷的核心不是回應頻率差異，單次機率輸出也可能洩露成員訊號。",
        "C": "由輸出推測輸入缺失或敏感屬性屬 attribute inference；它問的是某人的屬性值，而 membership inference 問的是該筆紀錄是否被用於訓練。",
        "D": "大量查詢蒐集輸入輸出對並訓練替代模型屬 model extraction／model stealing；它企圖複製決策行為，與判斷特定資料是否在訓練集不同。",
    },
    "trap": "先鎖定攻擊者想知道什麼：『有沒有參與訓練』是成員推斷，『敏感欄位是什麼』是屬性推斷，『複製模型』則是模型竊取。",
    "editorialNote": "本站依官方答案 A 判定。『降低輸出信心』若只是任意壓低或四捨五入機率，未必能可靠防禦，攻擊者仍可能利用標籤、loss 或多次查詢；較完整做法是降低過擬合、限制回傳資訊與查詢，並採具隱私會計的差分隱私訓練。",
    "references": [
        exam_ref(37),
        ref(
            "Membership Inference Attacks Against Machine Learning Models",
            "https://arxiv.org/abs/1610.05820",
            "Shokri 等人的成員推斷威脅模型、shadow models 與利用目標模型輸出的攻擊方法",
        ),
        ref(
            "Deep Learning with Differential Privacy",
            "https://arxiv.org/abs/1607.00133",
            "以 per-example gradient clipping、noise 與 privacy accounting 訓練差分隱私深度模型",
        ),
    ],
}

DRAFTS[38] = {
    "summary": "正確答案是 B。差分隱私合成資料的發布物是經差分隱私機制建立的合成資料集；B 描述的是對統計查詢或模型訓練加入雜訊的一般差分隱私作法，並非合成資料的定義。",
    "concept": (
        "K 匿名要求每個準識別符組合至少出現 K 次，但不提供對所有背景知識的正式機率保證。"
        "差分隱私要求相鄰資料集（增減一個人的資料）產生任一輸出的機率相近，並以 epsilon、delta"
        "量化隱私損失；合成資料作法會先用具 DP 保證的統計或生成模型學習分佈，再抽樣出不存在的"
        "合成個體。Randomized Response 則在資料收集端以已知機率擾動敏感回答，讓單次回答可否認。"
    ),
    "answerReason": (
        "B 把『差分隱私合成資料』錯說成直接發布加噪查詢結果或加噪訓練模型；後兩者是差分隱私"
        "機制的其他輸出形式，沒有產生可供後續分析的合成資料集，因此是題目預期的不正確敘述。"
    ),
    "optionAnalysis": {
        "A": "正確描述 K 匿名的基本條件：以泛化或抑制讓每個準識別符等價類至少有 K 筆，降低紀錄被準識別符唯一連結的風險，但仍可能遭同質性或背景知識攻擊。",
        "B": "不正確。對查詢答案加噪或以 DP 訓練模型可滿足差分隱私，卻不等於發布 DP 合成資料；後者還要由私有化統計／模型生成與原資料同 schema 的合成紀錄。",
        "C": "正確。亂數回應讓受訪者依已知機率回答真值或隨機答案，因此觀察者不能由單次回答確定真實狀態；群體比例可在已知機率下做統計校正。",
        "D": "依本題分類，差分隱私以隱私預算量化並具有組合規則；K 匿名缺乏同等背景知識保證，重複詢問未妥善控管的亂數回應也會累積證據。不過 randomized response 可構成 local DP，需見編輯註記。",
    },
    "trap": "要區分『DP 保護的查詢答案／模型』與『DP 合成資料集』：它們都可能符合差分隱私，但發布物不同。看到『合成資料』必須真的產生新紀錄。",
    "editorialNote": "本站依官方答案 B 判定，但 D 的措辭有概念重疊：經適當參數化的 randomized response 本身可滿足 local differential privacy，也具有可量化與可組合的保證；若 D 把它視為完全不屬於差分隱私，則『只有差分隱私』並不嚴謹。D 後半段可理解為未納入隱私預算的傳統重複詢問會削弱保護，待獨立人工複核。",
    "references": [
        exam_ref(38),
        ref(
            "NIST SP 800-226－Guidelines for Evaluating Differential Privacy Guarantees",
            "https://doi.org/10.6028/NIST.SP.800-226",
            "Section 2 differential privacy guarantee、composition；Section 3.6 differentially private synthetic data",
        ),
        ref(
            "NIST－Differentially Private Synthetic Data",
            "https://www.nist.gov/blogs/cybersecurity-insights/differentially-private-synthetic-data",
            "DP 合成資料以私有化分佈或模型產生 fake individuals，且與加噪回答特定查詢的流程有別",
        ),
        ref(
            "NIST SP 800-226－Randomized response",
            "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-226.pdf",
            "Local model 與 randomized response 的差分隱私保證、隱私參數及重複操作的 composition",
        ),
    ],
}

DRAFTS[39] = {
    "summary": "正確答案是 C。附圖函式的預設參數 tags=[] 只在函式定義時建立一次；兩次呼叫共用同一串列並各 append 一次，所以 row2['tags'] 是 ['checked', 'checked']。",
    "concept": (
        "Python 的預設參數值在執行 def、建立函式物件時求值一次，不是每次呼叫都重新求值。"
        "list 是可變物件，因此第一次 process_record({\"id\": 1}) 對預設串列 append 後，該串列保留"
        "一個 checked；第二次未傳 tags，仍取得同一串列，再 append 一次。record['tags'] 是直接指定"
        "該串列參照，不會複製它。避免此陷阱應用 tags=None，並在函式內建立新串列。"
    ),
    "answerReason": (
        "本站目視附圖確認函式簽名為 process_record(record, tags=[])，且每次都先 tags.append(\"checked\")"
        "再指定 record['tags']=tags。第二次呼叫沿用第一次已變更的預設串列，故 row2 看到兩個 checked。"
    ),
    "optionAnalysis": {
        "A": "程式只把字串 checked 加入串列，從未 append 字串 tags；record['tags'] 中的 tags 是字典鍵名稱，不會自動成為串列元素。",
        "B": "如果每次呼叫都建立新空串列，第二次執行後也至少會有一個 checked；實際上可變預設值還會沿用第一次結果，因此不可能是空串列。",
        "C": "正確。第一次呼叫把共用預設串列改為 ['checked']，第二次再改為 ['checked', 'checked']，並把同一串列指定給 row2['tags']。",
        "D": "record['tags'] = tags 是賦值操作，字典原本沒有 tags 鍵也會直接建立，不會拋出 KeyError；通常只有讀取不存在的 record['tags'] 才會發生該錯誤。",
    },
    "trap": "關鍵不是字典是否獨立，而是預設 list 是否共用。可變預設參數會跨呼叫保留狀態；安全寫法是預設 None，函式內再建立 tags=[]。",
    "editorialNote": "本站已於 2026-08-13 目視核對 `/images/questions/aiap-115-intermediate-1-big-data-p12-1.png`：程式確為 `tags=[]`、每次 append `checked`，row1 與 row2 呼叫都未傳 tags。本站內容仍為 AI 輔助詳解初稿，尚待獨立人工複核。",
    "references": [
        exam_ref(39),
        ref(
            "Python 官方教學－Default Argument Values",
            "https://docs.python.org/3/tutorial/controlflow.html#default-argument-values",
            "預設值只求值一次；可變 list 會在後續呼叫累積，建議以 None 建立新物件",
        ),
    ],
}

DRAFTS[40] = {
    "summary": "正確答案是 A。附圖先計算測試點到每筆訓練樣本的距離，排序後取最近 X 個標籤並以多數決預測，正是 K-近鄰分類。",
    "concept": (
        "K-Nearest Neighbors（KNN）是 instance-based learning：預測時才計算新點與訓練樣本的"
        "距離，選出距離最小的 K 個鄰居，再以多數決或距離加權投票得到分類標籤。演算法沒有先"
        "學習明確參數模型，因此訓練成本低，但推論要搜尋鄰居，會受資料量、維度、距離度量與特徵"
        "尺度影響。附圖把鄰居數寫為 X，角色就是常見符號 K。"
    ),
    "answerReason": (
        "本站目視附圖確認流程依序是計算所有 sample 與 test_point 的距離、升冪排序、取前 X 個"
        "最小距離項目並統計其標籤多數，這六步完整符合 KNN 分類器，其他候選演算法沒有此預測流程。"
    ),
    "optionAnalysis": {
        "A": "正確。KNN 對待測點找出 K（圖中 X）個最近訓練樣本，並由鄰居標籤投票；附圖的距離、排序、取最近項目與多數標籤完全吻合。",
        "B": "K-means 也使用距離，但會反覆把資料指派給最近群中心並更新 centroid，輸出是未標註群集；附圖使用已知標籤投票，沒有更新中心。",
        "C": "SVM 在訓練時尋找最大間隔超平面，預測時依決策函數判斷位於哪一側；不需對每個測試點排序全部訓練樣本並投票。",
        "D": "隨機森林先訓練多棵決策樹，每棵樹沿特徵切分走到葉節點，再對樹的預測投票；它不以樣本間距離挑選最近 X 筆。",
    },
    "trap": "KNN 與 K-means 都有 K 且都可能計算距離，但 KNN 使用有標籤鄰居投票做監督式分類；K-means 使用 centroid 做非監督式分群。",
    "editorialNote": "本站已於 2026-08-13 目視核對 `/images/questions/aiap-115-intermediate-1-big-data-p12-2.png`：輸入含已標註 train_data 與 test_point，流程為距離排序、取前 X 個並以標籤眾數預測。本站內容仍為 AI 輔助詳解初稿，尚待獨立人工複核。",
    "references": [
        exam_ref(40),
        ref(
            "scikit-learn－Nearest Neighbors Classification",
            "https://scikit-learn.org/stable/modules/neighbors.html#nearest-neighbors-classification",
            "KNeighborsClassifier 以每個查詢點最近鄰的多數決或距離加權投票分類",
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
