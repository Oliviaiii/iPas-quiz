"""Write draft explanations for 114-2 intermediate big-data subject, Q11-Q20.

The script verifies official answers and refuses to overwrite reviewed work.
Run the draft validator before applying it to the shared question bank.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-114-intermediate-2-big-data"
AUTHOR = "Codex（AI 輔助初稿）"
AUTHORED_AT = "2026-08-12"
CHECKED_AT = "2026-08-12"

EXAM_PDF = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/114年第二梯次中級AI應用規劃師"
    "第二科大數據處理分析與應用(當次試題公告114_20251226000634.pdf"
)
DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def exam_ref(number: int) -> dict:
    return {
        "title": "114 年第二次中級 AI 應用規劃師－大數據處理分析與應用公告試題",
        "url": EXAM_PDF,
        "locator": f"第 {number} 題題幹、選項與官方答案",
        "checkedAt": CHECKED_AT,
    }


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


EXPECTED_ANSWER = {
    11: "C", 12: "A", 13: "D", 14: "D", 15: "C",
    16: "A", 17: "B", 18: "A", 19: "C", 20: "D",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[11] = {
    "summary": "正確答案是 C。大量 IoT 裝置會持續產生高速事件流，需要可水平擴展的大數據平台承接資料，再以流式即時分析在事件抵達時偵測異常。",
    "concept": (
        "IoT 異常監控同時具有資料量大、產生速度快與低延遲要求。合適架構會以訊息"
        "佇列或事件匯流排解耦裝置與下游，再由分散式 stream processing engine 對"
        "無界資料流做視窗聚合、狀態計算與規則／模型推論。大數據平台負責分散式"
        "儲存與運算伸縮；即時分析則在事件到達時持續處理。批次工作適合歷史報表"
        "或模型再訓練，不能單獨滿足即時告警。"
    ),
    "answerReason": (
        "C 同時滿足兩個核心條件：大數據平台可承接大量裝置與資料規模，即時分析"
        "可在資料流進入時迅速偵測異常。其他組合要不是只能離線處理，就是缺乏"
        "自動化與水平擴展能力。"
    ),
    "optionAnalysis": {
        "A": "關聯式資料庫適合結構化交易與查詢，圖形視覺化可呈現結果；但僅有這兩項沒有事件流處理、窗口狀態與告警引擎，面對大量裝置高速寫入時也容易形成擴展瓶頸。",
        "B": "批次處理會累積一段時間後才運算，適合離線統計；雲端備份保障資料留存，但不會在事件抵達時判斷異常，因此無法達成即時監控。",
        "C": "正確。分散式大數據平台可水平擴展資料接收、儲存與運算，流式分析框架則能對持續事件做低延遲計算並觸發異常警報，兩者完整對應題意。",
        "D": "Word 文件與人工標註是人工離線流程，既無法自動接收感測器事件，也無法在大量資料下維持毫秒或秒級反應，吞吐量與即時性都不符合需求。",
    },
    "trap": "儀表板只是顯示結果，不等於即時分析；備份只是保存資料，也不等於監控。題目同時出現『大量』與『即時』時，要選可分散擴展且能處理無界事件流的組合。",
    "references": [
        exam_ref(11),
        ref("Apache Flink Documentation－Stateful Stream Processing", "https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/stateful-stream-processing/", "事件驅動應用與資料管線對無界資料流持續進行具狀態、可擴展處理"),
    ],
}

DRAFTS[12] = {
    "summary": "正確答案是 A。隨機過採樣會重複抽取少數類既有樣本；若模型反覆看到相同案例，可能記住個別噪音與細節，增加對少數類訓練資料過擬合的風險。",
    "concept": (
        "Random Oversampling 從少數類有放回抽樣，將其複製到較平衡的數量。它能讓"
        "學習器在損失中更重視少數類，但沒有新增資訊：重複樣本使決策樹或高容量"
        "模型可能把少數類的噪音與離群點也當成穩定模式。這與 SMOTE 在鄰近少數"
        "樣本間合成新點不同；後者增加變化但也可能跨越類別邊界。重採樣應只在每個"
        "訓練折內做，驗證／測試資料保持原分布，並以 recall、precision 等指標評估。"
    ),
    "answerReason": (
        "A 指出 Random Oversampling 最典型的代價：複製相同少數類樣本可能使模型"
        "過度貼合。此方法會增加而非減少資料列，也不會自然製造欄位缺失；收斂速度"
        "可能因資料量改變，但不是其最常見的核心問題。"
    ),
    "optionAnalysis": {
        "A": "正確。有放回重複少數類樣本不會增加新資訊，卻提高這些樣本及其噪音在訓練中的權重；模型容量較大時可能形成過於特化的決策邊界，導致泛化下降。",
        "B": "資料列增加可能讓每個 epoch 計算時間變長，但梯度收斂快慢取決於模型、最佳化器與批次設計；『降低收斂速度』不是隨機過採樣最具代表性的統計風險。",
        "C": "隨機過採樣是複製少數類資料，使訓練集總筆數增加；減少總筆數是對多數類做 undersampling 的效果，方向正好相反。",
        "D": "過採樣只選取並複製既有完整資料列，不會把欄位值刪除或改成缺失。若來源樣本原本有缺值，複製會保留缺值，但不是方法本身造成。",
    },
    "trap": "Oversampling 與 undersampling 的方向容易看反：前者增加少數類列，後者刪減多數類列。隨機過採樣的問題不是資料變少，而是重複資訊可能讓模型記憶樣本。",
    "references": [
        exam_ref(12),
        ref("imbalanced-learn User Guide－Random over-sampling", "https://imbalanced-learn.org/stable/over_sampling.html#naive-random-over-sampling", "RandomOverSampler 以有放回抽樣方式複製少數類樣本，並討論 smoothed bootstrap 變體"),
    ],
}

DRAFTS[13] = {
    "summary": "正確答案是 D。同態加密允許運算者在沒有私鑰、看不到明文的情況下直接計算密文，資料擁有者解密運算結果後可得到對應的明文計算結果。",
    "concept": (
        "一般加密保護儲存與傳輸資料，但伺服器計算前通常要解密；Homomorphic "
        "Encryption 的同態性則讓特定加法、乘法或可表示的電路在密文上執行，輸出"
        "仍是密文，最後由持有私鑰者解密。部分同態只支援有限運算，leveled HE 支援"
        "有限深度電路，fully homomorphic encryption 理論上可評估任意電路，但噪音"
        "管理、數值編碼、速度與模型相容性仍是實務限制。它不是去識別、資料清理"
        "或標準化。"
    ),
    "answerReason": (
        "D 直接描述同態加密的定義性能力：資料保持加密仍可被運算。A 是匿名化／"
        "代碼化，B 是資料前處理，C 是異常偵測，三者都沒有讓密文可計算的密碼"
        "學性質。"
    ),
    "optionAnalysis": {
        "A": "把身分欄位替換成代碼屬假名化或 tokenization；若對照表仍存在，資料仍可能重新連結個人，而且一般代碼本身不提供在密文上執行算術的能力。",
        "B": "標準化將數值轉成共同尺度，例如減平均再除標準差，目的是改善數值條件或模型訓練；它不是保密機制，轉換後的值仍可能直接被服務商讀取。",
        "C": "異常值偵測用統計或模型找出偏離常態的資料點，屬資料品質與分析；它不會加密資料，也不讓第三方在不知道明文時完成運算。",
        "D": "正確。同態方案保留加密資料的代數結構，雲端可在無私鑰下評估支援的運算並回傳密文結果，再由資料擁有者解密取得對應答案。",
    },
    "trap": "匿名化保護身分、雜湊做單向摘要、一般加密保護靜態資料；只有同態加密的關鍵字是『不解密仍能運算』，且運算後結果仍需由私鑰持有者解密。",
    "references": [
        exam_ref(13),
        ref("Homomorphic Encryption Standardization－Introduction", "https://homomorphicencryption.org/introduction/", "同態加密允許無私鑰者直接對加密資料運算，結果維持加密並由私鑰持有者解密"),
    ],
}

DRAFTS[14] = {
    "summary": "正確答案是 D。A、B 各占一半，原始 Gini impurity 為 1−0.5²−0.5²=0.5；二元分類最大值也是 0.5，除以最大值正規化後為 1。",
    "concept": (
        "Gini impurity 定義為 G=1−Σp_k²，也可寫成 Σp_k(1−p_k)。節點全部同類時"
        "G=0；K 類完全平均時達最大值 1−1/K。題目有 5 個 A、5 個 B，所以 p_A=p_B=0.5，"
        "原始 G=1−0.25−0.25=0.5。若『Normalized Gini impurity』指將原始值除以"
        "該類別數的最大可能值，二元最大值 1−1/2=0.5，故 G_norm=0.5/0.5=1。"
        "不同資料源對 normalized 名稱可能另有定義，計算時要先確認尺度。"
    ),
    "answerReason": (
        "此資料是二元類別最均勻、也最不純的狀態。原始 Gini 是 0.5，題目問正規化"
        "值，需以二元最大值 0.5 縮放，因此得到 1，對應 D。"
    ),
    "optionAnalysis": {
        "A": "0 代表節點完全純，例如 10 筆全是 A；本題 A、B 各半，隨機抽取兩筆屬不同類別的機率最高，不能判為零不純度。",
        "B": "0.42 不是依 5/10、5/10 代入 Gini 公式的結果；若類別比例為 0.7 與 0.3，原始 Gini 才是 1−0.49−0.09=0.42，但本題並非此比例。",
        "C": "0.84 同樣不符合二元各半的原始或最大值正規化結果；原始值為 0.5，除以 0.5 後是 1，沒有得到 0.84 的計算步驟。",
        "D": "正確。二元各半使 Gini impurity 達到最大 0.5；正規化以最大可能不純度為 1，因此 0.5÷0.5=1，表示相對尺度上的最高不純度。",
    },
    "trap": "先算原始 Gini，再看題目是否寫『正規化』。二元各半的原始值是 0.5，不是 1；只有再除以二元最大值 0.5 後才得到 normalized value 1。",
    "editorialNote": "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。「Normalized Gini impurity」並非所有教材都採同一命名；本題依官方答案 D，解作以 K 類最大值 1−1/K 正規化。待複核官方學習材料的明確公式。",
    "references": [
        exam_ref(14),
        ref("scikit-learn User Guide－Mathematical formulation of decision trees", "https://scikit-learn.org/stable/modules/tree.html#mathematical-formulation", "Gini impurity 定義為 Σ p_mk(1−p_mk)，等價於 1−Σp²"),
    ],
}

DRAFTS[15] = {
    "summary": "正確答案是 C。卜瓦松分布描述固定時間區間內獨立事件的發生次數，其參數 λ 就是該區間的平均事件數；本題每分鐘來電數符合此計數情境。",
    "concept": (
        "Poisson distribution 用於固定區間中的非負整數事件計數，典型假設是事件"
        "獨立、平均發生率在考察期間大致固定，且極短區間發生機率約與區間長度成正比。"
        "其機率質量 P(X=k)=e^(−λ)λ^k/k!，平均與變異數皆為 λ。本題每小時平均 20 通，"
        "若率固定，換算每分鐘 λ=20/60=1/3。Exponential distribution 與同一 Poisson "
        "process 有關，但描述的是相鄰事件等待時間，不是每分鐘的來電筆數。"
    ),
    "answerReason": (
        "題目問『每分鐘接到幾通』，輸出是 0、1、2…的事件數，並明示獨立與短時間"
        "機率成比例，正是 Poisson process 的計數分布條件，因此選 C。"
    ),
    "optionAnalysis": {
        "A": "均勻分布要求所有可能值有相同機率；來電數沒有固定有限上限，而且 0、1、2 通的機率由平均率決定並不相等，不符合均勻假設。",
        "B": "指數分布描述連續的等待時間，例如『下一通電話還要等幾分鐘』；題目問固定一分鐘內的離散來電次數，因此應用 Poisson 而不是 Exponential。",
        "C": "正確。Poisson 分布以 λ 表示固定區間的平均事件數，事件獨立且穩定發生率時可計算該分鐘出現 0、1、2…通電話的機率；此處 λ=1/3 通／分鐘。",
        "D": "常態分布是連續且可取任意實數，雖在 λ 很大時可近似 Poisson，但每分鐘平均僅 1/3 通且資料是非負整數，直接使用 Poisson 更合適。",
    },
    "trap": "Poisson 問『固定時間內幾次』，Exponential 問『等到下一次多久』。兩者可來自同一事件過程，但隨機變數型態一個是離散計數、一個是連續等待時間。",
    "references": [
        exam_ref(15),
        ref("NIST/SEMATECH e-Handbook－Poisson Distribution", "https://itl.nist.gov/div898/handbook/eda/section3/eda366j.htm", "Poisson 分布用於固定時間區間內的事件次數，λ 為該區間平均事件數"),
    ],
}

DRAFTS[16] = {
    "summary": "正確答案是 A。Z=(3,200−2,000)/400=3；公司規則是 |Z|≥3 即異常，等號也包含在門檻內，因此此交易應標記。",
    "concept": (
        "Z-score 將觀測值相對平均數的距離換算成標準差單位，公式 z=(x−μ)/σ。正值"
        "代表高於平均、負值代表低於平均，絕對值越大表示離中心越遠。本題差額 1,200 "
        "元，除以 400 元得到 z=3，即高於平均三個標準差。以固定 |z| 門檻偵測離群值"
        "是假設式規則，若交易分布高度偏態、厚尾或隨客群改變，應改用 robust z-score、"
        "分群基準或分位數，而非把 z=3 當普遍事實。"
    ),
    "answerReason": (
        "計算結果恰好是 3，且判定條件寫的是大於或等於 3，因此臨界點必須納入"
        "異常，只有 A 同時給出正確數值與正確門檻判斷。"
    ),
    "optionAnalysis": {
        "A": "正確。3,200 減 2,000 等於 1,200，除以標準差 400 得 3；由於規則使用 |Z|≥3 而不是 >3，Z=3 已符合異常條件。",
        "B": "Z=2.5 對應的交易金額應是 2,000+2.5×400=3,000 元；題目金額為 3,200 元，所以數值計算與合理範圍判斷皆錯。",
        "C": "Z=2 對應 2,800 元，不是 3,200 元；單一觀測的 z-score 也不能證明標準差估計過高，需檢查整體樣本與估計方法。",
        "D": "Z=1.5 對應 2,600 元；本題實際為三個標準差。是否納入異常檢測應依既定 |Z|≥3 規則，不能在算錯數值後排除。",
    },
    "trap": "先做差再除以標準差，並注意門檻有沒有等號。|Z|≥3 包含正三與負三；若寫 |Z|>3，恰好等於三才不會被標記。",
    "references": [
        exam_ref(16),
        ref("NIST/SEMATECH e-Handbook－Location and Scale", "https://www.itl.nist.gov/div898/handbook/eda/section3/eda353.htm", "標準化以觀測值減去位置參數再除以尺度參數，標準分數以標準差單位表示距離"),
    ],
}

DRAFTS[17] = {
    "summary": "正確答案是 B。把類別任意編成 0、1、2 後，樹會用數值閾值切割，可能把代碼大小與相鄰關係誤當成有意義順序，進而扭曲分裂與重要性。",
    "concept": (
        "Label Encoding 為每個類別指定整數。一般數值型樹會測試 x≤t，因此一個"
        "三類編碼只能形成依代碼順序相鄰的集合；若類別本來是 nominal，編碼次序"
        "只是人工決定，模型卻可能當成 ordinal。One-Hot Encoding 為每類建立指示欄，"
        "避免任意大小關係，但增加欄數與記憶體。Target Encoding 用目標統計表示類別，"
        "必須以 out-of-fold、平滑等方式防止洩漏與過擬合。部分現代 GBDT 有原生"
        "categorical split，應依具體實作選擇。"
    ),
    "answerReason": (
        "B 點出類別整數編碼交給一般梯度提升樹的主要陷阱：模型可能依人為代碼做"
        "有序閾值切分並產生偏誤。A 誤稱 one-hot 會降低記憶體，C 把 target encoding "
        "說成自動無過擬合，D 則把 PCA 錯用到少量類別。"
    ),
    "optionAnalysis": {
        "A": "One-hot 常能避免 nominal 類別的任意順序，但每個類別新增欄位，通常增加而非減少維度與記憶體；而『會員等級』是否具真實順序仍應依業務語意決定，不能一律優先。",
        "B": "正確。一般樹把整數編碼視為可比較數值，使用閾值切分；若代碼順序沒有業務意義，可能限制可形成的類別組合並影響分裂增益與衍生的重要性。",
        "C": "Target encoding 使用各類別的目標平均，若直接用全訓練資料計算會把標籤資訊洩漏進特徵，稀有類別尤其容易過擬合；需 out-of-fold 計算與 smoothing，不能自動消除風險。",
        "D": "PCA 適用於數值特徵的線性投影，不直接接受『一般、白金、黑卡』這類原始字串；僅三類也沒有維度災難，先做 PCA 不是合理的類別編碼方案。",
    },
    "trap": "One-hot 不會減少記憶體，target encoding 也不會自動防洩漏。另要先問類別是否真的有序：會員等級可能具業務順序，因此 B 的風險要依模型與語意判斷。",
    "editorialNote": "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。題目中的一般、白金、黑卡可能本來就有等級順序，且部分 GBDT 支援原生 categorical features；B 應理解為未確認語意便任意 label encode 給一般數值切分樹的風險。",
    "references": [
        exam_ref(17),
        ref("scikit-learn User Guide－Categorical Feature Support in Gradient Boosting", "https://scikit-learn.org/stable/auto_examples/ensemble/plot_gradient_boosting_categorical.html", "比較 dropping、one-hot、ordinal 與原生 categorical encoding；原生類別處理避免任意排序限制"),
        ref("scikit-learn User Guide－Target Encoder's Internal Cross fitting", "https://scikit-learn.org/stable/auto_examples/preprocessing/plot_target_encoder_cross_val.html", "Target encoding 若不交叉擬合容易資料洩漏與過擬合"),
    ],
}

DRAFTS[18] = {
    "summary": "正確答案是 A。交易中任一節點出錯時，所有更新要嘛一起提交、要嘛全部回復，避免留下部分結果，這正是 ACID 的原子性。",
    "concept": (
        "資料庫交易的 ACID 包含 Atomicity、Consistency、Isolation、Durability。"
        "Atomicity 把多個操作視為不可分割單位，失敗時 rollback，使外部只看到全部"
        "完成或完全沒發生。Consistency 指交易從一個符合完整性規則的狀態帶到另一個"
        "合法狀態；Isolation 管理並行交易彼此可見性；Durability 保證已 commit 的"
        "結果在故障後仍保存。分散式多節點通常還需協調協定來達成原子提交，但題目"
        "描述的是性質而不是指定協定。"
    ),
    "answerReason": (
        "題幹關鍵詞是『一個節點錯誤』『不會部分更新』『全部成功或回復』，逐字"
        "對應原子性的 all-or-nothing 保證，因此 A 最精確。最終狀態一致是原子回復"
        "的結果之一，但 B 的 consistency 著重完整性規則，不是此描述主體。"
    ),
    "optionAnalysis": {
        "A": "正確。原子性把跨節點更新視為單一交易單位；只要其中一步不能完成，先前步驟也不能留下永久效果，必須整筆 abort／rollback，避免部分套用。",
        "B": "一致性要求提交前後都符合主鍵、餘額守恆等資料庫與應用規則；題目沒有描述違反約束，而是強調失敗時所有操作一併撤回，應歸原子性。",
        "C": "隔離性規範多個並行交易如何看到彼此未提交或已提交的修改，避免 dirty read、lost update 等並行異常；題目只有單筆交易跨節點失敗，沒有交易競爭情境。",
        "D": "持久性保證交易成功 commit 並回覆後，即使系統當機結果仍不遺失；題目描述的是尚在交易中發生錯誤並回復，尚未進入已提交結果的保存問題。",
    },
    "trap": "ACID 題先抓動詞：失敗全回復是 Atomicity、符合規則是 Consistency、並行互不干擾是 Isolation、提交後不遺失是 Durability。不要因題目出現『一致』兩字就直接選 Consistency。",
    "references": [
        exam_ref(18),
        ref("PostgreSQL Documentation－Transactions", "https://www.postgresql.org/docs/current/tutorial-transactions.html", "交易將多步驟綁成 all-or-nothing；失敗時已執行步驟不影響資料庫，稱為 atomic"),
    ],
}

DRAFTS[19] = {
    "summary": "正確答案是 C。邊緣節點就近偵測異常以取得低延遲，流式框架持續處理大量事件，雲端資料湖保留原始完整資料並可水平擴展供後續訓練。",
    "concept": (
        "同時滿足即時與歷史分析可採 edge-stream-lake 分層。邊緣運算把需要毫秒反應"
        "的前處理與初步推論放近感測器，降低網路往返並可在斷線時維持局部決策；"
        "stream processing framework 對事件做過濾、視窗與狀態運算；完整原始事件"
        "則非同步寫入可擴展的雲端 object storage／data lake，供批次特徵工程、稽核"
        "與模型再訓練。生產上還需事件 ID、checkpoint、重試與 exactly-once／冪等"
        "設計，避免即時與保存支線不一致。"
    ),
    "answerReason": (
        "C 是唯一把低延遲邊緣運算、可擴展流式處理及完整雲端資料湖三者串起來的"
        "流程，對應題目的即時性、資料完整性與可擴展性。其餘方案把關鍵判斷放在"
        "雲端批次、資料倉儲或報表端，無法穩定達到毫秒級。"
    ),
    "optionAnalysis": {
        "A": "所有感測器事件先跨網路進 API Gateway 與資料庫，再做批次特徵工程，路徑長且批次增加等待時間；它可保存資料，但模型推論排在批次之後，難以毫秒告警。",
        "B": "MQTT Broker 適合裝置訊息傳遞，但直接寫雲端資料倉儲後才顯示儀表板，缺少就近運算與明確流式分析層；倉儲通常偏分析查詢，並非毫秒事件處理的核心。",
        "C": "正確。Edge node 就近快速反應，stream framework 以分散式狀態運算承接上萬感測器，data lake 低成本保存原始與處理後資料，三層可各自水平擴展。",
        "D": "本地快取可短暫緩衝，但 REST API、雲端報表與批次更新主要面向查詢與離線流程；沒有持續流式處理與完整資料湖設計，難兼顧毫秒告警及長期訓練資料。",
    },
    "trap": "低延遲不等於只用快取，完整保存也不等於直接進資料庫。把需求拆成三條：邊緣負責快、stream 負責持續算、lake 負責完整留存與後續擴展。",
    "references": [
        exam_ref(19),
        ref("Apache Flink Documentation－Stateful Stream Processing", "https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/stateful-stream-processing/", "分散式 stream processor 對無界事件流執行具狀態、可容錯且可擴展的即時計算"),
        ref("AWS IoT Greengrass－What is AWS IoT Greengrass?", "https://docs.aws.amazon.com/greengrass/v2/developerguide/what-is-iot-greengrass.html", "Edge runtime 可在裝置端處理、管理與回應資料，並與雲端安全通訊"),
    ],
}

DRAFTS[20] = {
    "summary": "正確答案是 D。同態加密讓銀行先加密敏感特徵，雲端在不知道明文與私鑰的情況下評估支援的模型運算，銀行解密結果後取得對應預測。",
    "concept": (
        "雲端機密運算的核心需求是 data in use protection：一般傳輸／靜態加密在計算"
        "前仍需解密，而 homomorphic encryption 允許直接評估密文，結果仍是密文。"
        "銀行持有私鑰，雲端只取得 evaluation key 與密文，可降低服務商看見原始交易"
        "的風險。實務要把模型轉成方案支援的加法、乘法或近似多項式，管理乘法深度、"
        "噪音與精度；效能通常遠慢於明文推論。這能減少明文暴露，但不取代存取控制、"
        "金鑰管理、輸出隱私與法規治理。"
    ),
    "answerReason": (
        "D 唯一同時滿足『不解密原始資料』與『仍能執行模型運算』。匿名化與雜湊"
        "會移除或不可逆改變模型需要的資訊，資料本地化則乾脆不在雲端運算，均不"
        "符合題目設定。"
    ),
    "optionAnalysis": {
        "A": "匿名化目標是降低資料與個人的可連結性，但若只保留可識別代碼更接近假名化，仍可能透過對照表回復身分；此外它沒有讓雲端對加密數值執行模型算術。",
        "B": "密碼雜湊是單向摘要，適合密碼驗證或完整性比對；交易金額一旦雜湊就失去大小與加總等數值關係，模型無法在摘要上完成原本風險運算。",
        "C": "資料本地化把訓練與推論留在銀行內部，可避免原始資料上雲，但題目明確要將模型部署雲端並讓服務商處理；此方案改變部署目標而非實現在雲端密文運算。",
        "D": "正確。同態加密保留所支援運算的代數關係，雲端可在無私鑰下對密文評估模型並回傳密文預測；銀行解密後得到與相應明文運算一致或編碼精度內近似的結果。",
    },
    "trap": "Hash 與 encryption 不同：雜湊不可逆，也不保留一般模型運算所需關係；同態加密可解密且可對密文計算。匿名化也不能自動提供 data-in-use confidentiality。",
    "editorialNote": "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。題目稱解密後與原始資料運算『一致』；採 CKKS 等近似同態方案時會有編碼與數值近似誤差，應依實際方案、模型與風險門檻驗證。",
    "references": [
        exam_ref(20),
        ref("Homomorphic Encryption Standardization－Introduction", "https://homomorphicencryption.org/introduction/", "雲端可直接操作加密資料並只回傳加密結果，由私鑰持有者解密"),
        ref("Homomorphic Encryption Standardization－Security Guidelines", "https://homomorphicencryption.org/security-guidelines/", "同態加密方案的安全參數與實作指引，涵蓋常見 FHE schemes"),
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
