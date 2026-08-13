"""Write draft explanations for 114-2 intermediate subject one, Q41-Q50.

The script verifies official answers, refuses to overwrite reviewed questions,
and only writes when explicitly executed.

Usage::

    python scripts/write-explanations-114-2-m1-041-050.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-114-intermediate-2-ai-tech-planning"
AUTHOR = "Codex（AI 輔助初稿）"
AUTHORED_AT = "2026-08-12"
CHECKED_AT = "2026-08-12"

EXAM_PDF = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/114年第二梯次中級AI應用規劃師"
    "第一科人工智慧技術應用與規劃(當次試題公告114_20251226000616.pdf"
)
ARXIV = "https://arxiv.org/abs/"
SKLEARN = "https://scikit-learn.org/stable/"
DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def exam_ref(number: int) -> dict:
    return {
        "title": "114 年第二次中級 AI 應用規劃師－人工智慧技術應用與規劃公告試題",
        "url": EXAM_PDF,
        "locator": f"第 {number} 題題幹、選項與官方答案",
        "checkedAt": CHECKED_AT,
    }


def paper_ref(paper_id: str, title: str, locator: str) -> dict:
    return {
        "title": title,
        "url": f"{ARXIV}{paper_id}",
        "locator": locator,
        "checkedAt": CHECKED_AT,
    }


def sklearn_ref(path: str, title: str, locator: str) -> dict:
    return {
        "title": f"scikit-learn－{title}",
        "url": f"{SKLEARN}{path}",
        "locator": locator,
        "checkedAt": CHECKED_AT,
    }


EXPECTED_ANSWER = {
    41: "A", 42: "D", 43: "B", 44: "C", 45: "D",
    46: "A", 47: "C", 48: "B", 49: "A", 50: "C",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[41] = {
    "summary": "正確答案是 A。同一組交叉驗證結果同時用於挑選超參數與回報效能，會產生選擇偏差，使分數過度樂觀。",
    "concept": (
        "交叉驗證可用來選模型，也可用來估計泛化效能，但同一批驗證摺不應同時"
        "承擔兩個角色。反覆嘗試超參數並挑出該批資料分數最高者，等於模型選擇"
        "流程逐漸配合驗證資料的偶然特徵；此時再把最高分當成未見資料表現，"
        "就低估了泛化誤差。巢狀交叉驗證以內圈選參數、外圈獨立估計效能。"
    ),
    "answerReason": (
        "題幹明說在同一 K-Fold 資料上調參並評估，因此測試摺的分數已間接左右"
        "超參數選擇，不能再視為完全獨立的測試證據。A 所述的資料洩漏與過度"
        "樂觀偏差正是主要風險；其餘選項把問題錯歸為正則化、方差必然上升或"
        "K-Fold 與調參原理不相容。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。每次比較候選參數都讀取驗證摺表現，最後選中的組合已對這批"
            "資料發生選擇性過擬合；若仍回報同一分數，便會高估未見資料表現。"
        ),
        "B": (
            "各摺反覆擬合不同參數本來就是搜尋流程的一部分，不會自動造成過度"
            "正則化。正則化強度取決於候選超參數，真正問題是缺少獨立外層資料"
            "評估已完成的選模程序。"
        ),
        "C": (
            "交叉驗證重複使用訓練樣本是其設計特性，可減少單次切分的偶然性；"
            "估計方差可能受資料量與模型穩定度影響，但這不是同資料調參再評估"
            "最具代表性的問題。"
        ),
        "D": (
            "K-Fold 可合法用於超參數搜尋，兩者並不衝突。應把搜尋放在巢狀 CV"
            "內圈，外圈保留給泛化評估；問題在角色未隔離，不是驗證方法失效。"
        ),
    },
    "trap": (
        "分清楚『用 CV 選參數』本身並沒有錯，錯的是選完後仍用同一 CV 分數"
        "宣稱泛化效能。公平估計整個選模流程時，需使用外層 CV 或完全獨立測試集。"
    ),
    "references": [
        exam_ref(41),
        sklearn_ref(
            "auto_examples/model_selection/plot_nested_cross_validation_iris.html",
            "Nested versus non-nested cross-validation",
            "說明：非巢狀 CV 用同一資料調參與評估會洩漏資訊、對資料過擬合並產生 overly optimistic score；巢狀 CV 以內圈選參數、外圈估計誤差",
        ),
    ],
}

DRAFTS[42] = {
    "summary": "正確答案是 D。四個選項中，以 VAE 建模輸入的潛在表示並監控分佈變化，最直接對應已知的輸入資料偏移。",
    "concept": (
        "資料漂移是上線輸入分佈 P(X) 相對訓練資料改變；它可能使鑑別式模型遇到"
        "未熟悉區域而增加錯誤。生成模型可學習訓練輸入的表示或密度，再以潛在"
        "向量分佈、重建誤差等訊號偵測偏離。不過漂移監控不必限定 VAE，也不能"
        "只靠單一生成分數；實務還需特徵統計、切片效能與人工門檻驗證。"
    ),
    "answerReason": (
        "題幹已定位原因為輸入分佈改變，D 是唯一直接監測該現象的方案：比較"
        "新資料與訓練資料在 VAE 潛在表示中的分佈，觸發調查或再訓練流程。A"
        "未先驗證就生成資料可能放大偏差，B 換成簡單模型不消除漂移，C 增加容量"
        "也無法讓模型自動認識新的資料分佈。"
    ),
    "optionAnalysis": {
        "A": (
            "GAN 可合成樣本，但生成內容受原訓練分佈與條件設計限制。若尚未弄清"
            "新分佈與標籤關係，直接混入合成資料可能無法覆蓋真實漂移，甚至加入"
            "新的偽影與偏差。"
        ),
        "B": (
            "邏輯迴歸較簡單、可解釋，但資料分佈轉移同樣會使其訓練假設失效。"
            "替換模型不等於監測或修復漂移，應先量測新舊資料差異與上線效能。"
        ),
        "C": (
            "較大容量能擬合更複雜的訓練關係，也提高過擬合與成本風險；它不會"
            "憑空取得新分佈資料，更不能保證對分佈外樣本穩健。"
        ),
        "D": (
            "正確（就選項比較而言）。VAE 可把輸入編碼到潛在空間，團隊再比較"
            "線上與基準資料的潛在分佈或重建訊號，以較直接地發現輸入偏移並預警。"
        ),
    },
    "trap": (
        "先回應已知根因：題目已證實資料分佈偏移，優先選監控偏移而非盲目換模、"
        "加容量或合成資料。另不要把『可作為漂移訊號』誤讀成 VAE 一定能可靠"
        "辨識所有分佈外資料。"
    ),
    "editorialNote": (
        "本站依官方答案 D 撰寫，僅將其視為四個選項中的相對最佳方案。研究顯示"
        "VAE 等深度生成模型的似然可能反而給分佈外資料較高分，不能單憑潛在空間"
        "或似然保證可靠 OOD 偵測；實務需以真實漂移案例校準並搭配特徵統計與"
        "效能監控。待人工複核是否需調整題目對『最適合』的表述。查核日期 2026-08-12。"
    ),
    "references": [
        exam_ref(42),
        paper_ref(
            "1810.09136",
            "Nalisnick et al., Do Deep Generative Models Know What They Don't Know?（ICLR 2019）",
            "摘要：VAE、flow 與 PixelCNN 的密度估計可能無法區分訓練分佈與分佈外影像，提醒不可未驗證即用於 OOD 偵測",
        ),
    ],
}

DRAFTS[43] = {
    "summary": "正確答案是 B。逐步降低標註比例並比較 F1，能直接觀察生成式表示與監督式分類器在低資源下的資料效率與泛化差異。",
    "concept": (
        "資料利用效率要用學習曲線比較：固定測試集、資料切分、前處理與評估"
        "程序，只改變可用標註資料量，再觀察模型表現下降速度。VAE 路徑可透過"
        "建模輸入分佈或使用未標註資料學表示，BERT Classifier 則直接最佳化"
        "標籤條件分類。標註比例越低，兩者如何利用未標註結構與預訓練知識的差異"
        "更容易呈現。"
    ),
    "answerReason": (
        "B 同時控制標註資源並使用適合三類分類的 F1，正面測量題目要求的資料"
        "利用效率與泛化能力。完整資料只測單一資源點，推論時間不是資料效率；"
        "GAN 增強加入第三個變因；只調參數量也不能隔離生成式與鑑別式訓練目標。"
    ),
    "optionAnalysis": {
        "A": (
            "完整 2,000 筆資料的準確率可比較最終效能，推論時間可比較部署成本，"
            "但只有一個標註量，無法看出模型隨標註減少的表現曲線，因此不能"
            "直接回答資料利用效率。"
        ),
        "B": (
            "正確。以 100%、50%、10% 標註量建立受控學習曲線，可比較少量標註時"
            "哪條路徑維持較高 F1；相同固定測試集又能評估未見資料泛化。"
        ),
        "C": (
            "GAN 生成資料會把合成品質、標籤方式與增強比例引入實驗，結果難以"
            "歸因於原本的 VAE 與 BERT 路徑。Precision 也只看誤報，未完整反映"
            "各類召回。"
        ),
        "D": (
            "固定輸入維度與調整參數量是在研究容量和過擬合，不是直接操弄標註"
            "資源。兩種架構的參數效率也不等於資料效率，且任意改參數量可能"
            "破壞各自合理設定。"
        ),
    },
    "trap": (
        "看到『資料利用效率』就要改變資料量，而非只比較模型大小或速度。公平"
        "實驗還要固定每個標註比例的抽樣、測試集與調參預算，並多次重抽樣回報"
        "變異，避免單次切分誤導。"
    ),
    "references": [
        exam_ref(43),
        paper_ref(
            "1406.5298",
            "Kingma et al., Semi-Supervised Learning with Deep Generative Models（NeurIPS 2014）",
            "摘要：深度生成模型與變分推論可利用少量標註及大量未標註資料，改善半監督泛化",
        ),
        paper_ref(
            "1810.04805",
            "Devlin et al., BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding（2018）",
            "摘要：預訓練 BERT 可加入輸出層後針對多種 NLP 任務微調",
        ),
    ],
}

DRAFTS[44] = {
    "summary": "正確答案是 C。VAE 或 GAN 能學習資料分佈並產生多樣樣本，較能支援題目所要求的虛擬資料生成。",
    "concept": (
        "鑑別式分類模型學習由顧客特徵到流失標籤的決策邊界，擅長預測但不直接"
        "描述如何生成一筆完整顧客資料。VAE 與 GAN 屬生成模型：VAE 以潛在"
        "變數建模資料並解碼樣本；GAN 讓生成器與鑑別器對抗訓練，產生近似真實"
        "分佈的樣本。若要模擬指定促銷條件，還需採條件式模型並驗證反事實假設。"
    ),
    "answerReason": (
        "題目除了流失預測，也明確要求產生多樣虛擬樣本。C 是唯一含有資料生成"
        "機制的選項，可由生成表示再搭配分類頭或以生成樣本供下游流失模型評估。"
        "隨機森林與邏輯迴歸只能輸出預測；強化學習可選策略，但不以生成符合"
        "顧客聯合分佈的資料為基本功能。"
    ),
    "optionAnalysis": {
        "A": (
            "隨機森林以多棵決策樹投票或平均，能處理非線性流失預測並提供特徵"
            "重要度，但輸出是類別或機率，不會生成具有完整欄位與一致關係的"
            "虛擬顧客樣本。"
        ),
        "B": (
            "邏輯迴歸可估計顧客流失機率，模型簡單且易解釋；它學的是條件機率"
            "P(y|x)，並未學習顧客特徵的聯合分佈 P(x)，因此不能獨立合成資料。"
        ),
        "C": (
            "正確。VAE 可從連續潛在空間取樣並解碼，GAN 可由噪聲經生成器產生"
            "近似訓練分佈的樣本；條件式版本還能納入促銷或服務條件，再搭配"
            "分類器評估流失預測。"
        ),
        "D": (
            "強化學習代理透過環境回饋學習行動策略，適合決定何時提供何種優惠；"
            "但必須先有可信的環境或使用者反應模型。代理本身不等於建立可供"
            "A/B 測試的顧客資料生成器。"
        ),
    },
    "trap": (
        "題目說『同時兼顧』不代表單一 VAE 或 GAN 天然完成因果模擬與分類。"
        "考題層次是辨認生成能力；實務仍要結合條件生成、預測模型及反事實驗證，"
        "不能把合成相關性當成促銷的因果效果。"
    ),
    "editorialNote": (
        "本站依官方答案 C 撰寫。VAE／GAN 可生成近似訓練分佈的樣本，但僅靠"
        "觀察性資料生成不同促銷條件，不能保證得到可信的顧客因果反應；『兼顧"
        "預測』也通常需分類頭或下游模型。待人工複核是否需進一步標示 A/B 測試"
        "與離線模擬的差別。查核日期 2026-08-12。"
    ),
    "references": [
        exam_ref(44),
        paper_ref(
            "1312.6114",
            "Kingma & Welling, Auto-Encoding Variational Bayes（2013）",
            "摘要與方法：以變分推論學習連續潛在變數的生成模型並進行取樣",
        ),
        paper_ref(
            "1406.2661",
            "Goodfellow et al., Generative Adversarial Nets（2014）",
            "摘要與第 1 節：生成器捕捉資料分佈，鑑別器估計樣本來自訓練資料而非生成器的機率",
        ),
    ],
}

DRAFTS[45] = {
    "summary": "正確答案是 D。PCA 降低輸入維度可減少 SVM 計算量，並可能移除低變異雜訊而降低過擬合風險。",
    "concept": (
        "PCA 是線性、非監督式降維：先將資料置中，再找出依解釋變異量排序的"
        "正交方向，將 1024 維投影到前 100 個主成分。特徵變少通常降低儲存、"
        "距離或核計算成本，也可能減少雜訊維度；但 PCA 最大化的是輸入變異，"
        "不是分類可分性，所以準確率可能提高、持平或下降，必須用驗證資料確認。"
    ),
    "answerReason": (
        "D 使用『可』而非『必然』，合理描述降維的常見效益：SVM 面對較少特徵"
        "時訓練計算較低，模型也較少機會利用高維雜訊過擬合。A 過度保證準確率；"
        "B 忽略高維成本與冗餘；C 則把 PCA 誤當成會自動建立非線性決策邊界。"
    ),
    "optionAnalysis": {
        "A": (
            "主成分依輸入變異排序，沒有使用類別標籤；高變異方向不一定最能"
            "區分類別，低變異方向也可能含關鍵訊號。因此 PCA 不能保證 SVM"
            "準確率提高，維度數應以交叉驗證選擇。"
        ),
        "B": (
            "原始高維特徵確實保留全部資訊，但也可能含冗餘、噪聲並增加時間與"
            "記憶體成本。PCA 可在可接受資訊損失下壓縮特徵，對高維影像表示"
            "具有實際用途。"
        ),
        "C": (
            "PCA 本身只做線性投影，不會使線性 SVM 自動學得非線性邊界。若資料"
            "需要非線性分隔，仍須選擇 RBF 等核函數、非線性降維或不同模型。"
        ),
        "D": (
            "正確。由 1024 維減為 100 維會降低後續 SVM 的特徵計算與儲存需求；"
            "若被移除方向主要是噪聲或冗餘，還可能降低過擬合，但最終效果仍需"
            "驗證。"
        ),
    },
    "trap": (
        "看到『必然』通常要警覺：非監督 PCA 不知道分類標籤，不能保證提升"
        "準確率。另區分降維與非線性化，PCA 只改表示維度，SVM 是否非線性仍"
        "由核函數等設定決定。"
    ),
    "references": [
        exam_ref(45),
        sklearn_ref(
            "modules/generated/sklearn.decomposition.PCA.html",
            "PCA",
            "定義：以 SVD 將置中資料投影到較低維空間；components 依 explained variance 排序",
        ),
        sklearn_ref(
            "auto_examples/applications/plot_face_recognition.html",
            "Faces recognition example using eigenfaces and SVMs",
            "範例：以 PCA 將高維人臉資料降維後，再用 SVM 分類並以交叉驗證搜尋參數",
        ),
    ],
}

DRAFTS[46] = {
    "summary": "正確答案是 A。應持續監測資料漂移與概念漂移，才能在服務未報錯但資料或關係已改變時主動預警。",
    "concept": (
        "線上系統健康可分為軟體與模型兩層：服務可正常回應，預測品質仍可能因"
        "世界改變而退化。資料漂移通常指輸入分佈 P(X) 改變；概念漂移指輸入與"
        "目標的關係 P(Y|X) 改變。MLOps 應保存訓練基準，監測特徵分佈、缺失率、"
        "預測分佈與取得標籤後的切片效能，超過門檻時通知調查或觸發再訓練。"
    ),
    "answerReason": (
        "題幹已發現近期輸入分佈偏移，A 直接建立可提前觀察該風險的監控機制，"
        "也涵蓋日後輸入—標籤關係改變。量化只改善延遲或資源；多做超參數搜尋"
        "不等於能適應新資料；固定隨機種子只提升實驗可重現性。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。以訓練或近期穩定期間作基準，持續比較特徵與預測分佈，並在"
            "標籤延遲到達後追蹤效能與概念關係，可在服務仍運作時發現品質風險。"
        ),
        "B": (
            "模型量化降低權重或啟動值精度，主要目的是縮小模型、降低記憶體與"
            "推論延遲。它不會檢查輸入分佈，也無法修復新資料造成的準確率下降。"
        ),
        "C": (
            "增加調參次數只會在既定訓練與驗證資料上搜尋更多組合；若沒有收集"
            "並驗證近期資料，搜尋仍看不到漂移後的模式，也可能增加選擇性過擬合。"
        ),
        "D": (
            "固定隨機種子可讓資料切分、初始化等隨機步驟較易重現，方便除錯與"
            "比較實驗；它不會讓上線輸入維持不變，也不會產生漂移告警。"
        ),
    },
    "trap": (
        "『系統正常』只代表沒有技術錯誤，不代表模型品質正常。漂移監控與效能"
        "監控也不同：沒有即時標籤時先看資料／預測分佈，有標籤後才能確認模型"
        "效能及概念是否真的退化。"
    ),
    "references": [
        exam_ref(46),
        {
            "title": "NIST AI RMF Playbook－MEASURE 2.4、MANAGE 4.1",
            "url": "https://airc.nist.gov/airmf-resources/playbook/",
            "locator": "MEASURE 2.4 建議在部署與運作中監測效能與風險；MANAGE 4.1 要求部署後持續監測、處理新風險與回應機制",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[47] = {
    "summary": "正確答案是 C。多任務損失若未適當加權，一個任務可能主導共享參數更新，造成任務間競爭與負遷移。",
    "concept": (
        "多任務模型通常共享 Transformer encoder，再由文件分類頭與 NER 序列"
        "標註頭各自輸出。總損失常寫成 L = w1·L分類 + w2·LNER；若損失尺度、"
        "樣本數或學習速度不同，未平衡的梯度可能把共享表示推向只利於其中一個"
        "任務的方向。NER 提升而分類下降就是負遷移的典型訊號，可調整權重、"
        "動態平衡梯度或減少共享層。"
    ),
    "answerReason": (
        "題幹已排除架構錯誤與資料品質問題，C 最能解釋一升一降的取捨：NER"
        "損失或梯度占優，使共享 encoder 更偏向 token-level 訊號而犧牲文件級"
        "分類。A、D 錯稱 Transformer／BERT 不能支援多輸出；B 則否定分類實際"
        "需要的上下文表示。"
    ),
    "optionAnalysis": {
        "A": (
            "共享 encoder 配不同任務頭可以同時支援句／文件分類與 token 級"
            "序列標註，這是常見多任務設計。題幹也已明說架構正確，因此不能將"
            "此現象歸因為根本不支援。"
        ),
        "B": (
            "文件分類同樣需要上下文化表示來理解詞義、否定與跨句關係，並非"
            "不需要語意。真正問題是共享表示被哪個損失方向主導，而不是分類"
            "不使用語意特徵。"
        ),
        "C": (
            "正確。若直接相加不同尺度的分類與 NER 損失，梯度較大或收斂較快的"
            "任務可能支配共享層更新。調整固定權重或使用 GradNorm 等動態方法，"
            "可嘗試平衡訓練速率。"
        ),
        "D": (
            "BERT encoder 可接多個輸出頭，例如序列分類頭使用整體表示、NER 頭"
            "對每個 token 分類。能否多頭是模型組裝方式，不是 BERT 表示本身"
            "無法做到。"
        ),
    },
    "trap": (
        "多任務不保證所有任務一起變好；共享參數可能帶來正遷移，也可能因梯度"
        "方向或尺度衝突造成負遷移。看到一個任務提升、另一個下降，先檢查各損失"
        "權重、梯度大小與學習速度。"
    ),
    "references": [
        exam_ref(47),
        paper_ref(
            "1711.02257",
            "Chen et al., GradNorm: Gradient Normalization for Adaptive Loss Balancing in Deep Multitask Networks（ICML 2018）",
            "摘要與第 2 節：多任務損失權重影響共享網路訓練；GradNorm 以梯度大小動態平衡各任務訓練速率",
        ),
    ],
}

DRAFTS[48] = {
    "summary": "正確答案是 B。KD-Tree 或 Ball Tree 可加速 DBSCAN 所需的鄰域查詢，且不改變其密度聚類核心邏輯。",
    "concept": (
        "DBSCAN 對每個點查找半徑 ε 內的鄰居，再依 min_samples 判斷核心點並"
        "擴張密度連通群集。暴力計算所有點對距離在數百萬筆資料上極昂貴，且"
        "鄰域結果可能耗用大量記憶體。空間索引可剪枝不可能位於半徑內的點，"
        "降低查詢成本；scikit-learn 也提供 ball_tree、kd_tree 等鄰居搜尋後端。"
    ),
    "answerReason": (
        "B 只替換鄰域搜尋的執行方式，DBSCAN 的 ε、核心點與密度連通定義不變，"
        "最符合『不改核心邏輯』。A 直接更換演算法；C 以極小 ε 扭曲聚類結果；"
        "D 增加維度會加重距離計算，且使樹索引在高維更難有效剪枝。"
    ),
    "optionAnalysis": {
        "A": (
            "平均連結階層式聚類以群集間平均距離逐步合併，群集定義與 DBSCAN"
            "的密度連通完全不同；大規模階層聚類本身也可能需要昂貴距離或連結"
            "計算，不符合保留核心邏輯。"
        ),
        "B": (
            "正確。KD-Tree 或 Ball Tree 可支援半徑鄰居查詢，避免每次都掃描"
            "所有點；若距離度量與資料維度適合，就能在保留 DBSCAN 判定規則下"
            "降低運算量。"
        ),
        "C": (
            "ε 決定何種距離算鄰居，調得極小雖可能減少每點鄰居，卻會把原本"
            "群集拆散並將大量樣本判為噪聲。這是改變模型結果來換速度，不是"
            "純粹的效率最佳化。"
        ),
        "D": (
            "標準化可避免量綱支配距離，但增加特徵維度會提高每次距離計算成本，"
            "並加劇高維空間的距離集中與索引退化。若要改善高維問題，方向通常"
            "是選特徵或降維。"
        ),
    },
    "trap": (
        "區分參數偷改與計算最佳化：把 ε 調小會改變群集，使用索引則只加速"
        "同一鄰域查詢。也要記得 KD-Tree／Ball Tree 並非高維萬靈丹，維度很高"
        "時可能退化，需實測或搭配降維。"
    ),
    "editorialNote": (
        "本站依官方答案 B 撰寫，但題幹同時強調『高維』；KD-Tree／Ball Tree"
        "在高維可能因維度災難而接近暴力搜尋，且鄰域過密時仍有高記憶體成本。"
        "B 是四個選項中唯一保留 DBSCAN 邏輯的合理最佳化，並非保證對所有"
        "數百萬筆高維資料都最有效。查核日期 2026-08-12。"
    ),
    "references": [
        exam_ref(48),
        sklearn_ref(
            "modules/generated/sklearn.cluster.DBSCAN.html",
            "DBSCAN",
            "參數 algorithm 支援 ball_tree、kd_tree、brute；文件並提醒某些 eps/min_samples 情況可達 O(n²) 記憶體複雜度",
        ),
        sklearn_ref(
            "modules/neighbors.html#nearest-neighbor-algorithms",
            "Nearest Neighbors－algorithm selection",
            "說明 KD tree、Ball tree 與 brute force 的選擇受樣本數、維度、資料結構及鄰居數影響，高維時樹方法效率可能降低",
        ),
    ],
}

DRAFTS[49] = {
    "summary": "正確答案是 A。未做詞嵌入正規化不是跨語言與族群情感偏誤的主要或必然成因，因此此敘述不正確。",
    "concept": (
        "本題問『不正確』。跨語言、文化與書寫風格的落差，優先檢查資料代表性、"
        "標註規則與各群體切片表現：若訓練語料集中於特定語言或語氣，模型會把"
        "該分佈中的相關性學成判斷規則。嵌入正規化只是將向量尺度調整成一致，"
        "常用於餘弦相似度或數值處理；它不會補入缺失文化語境，也不是所有"
        "Transformer 情感分類器的必要開關。"
    ),
    "answerReason": (
        "A 把群體間錯誤不一致歸因於未啟用單一嵌入正規化，缺少必然機制，"
        "正規化也無法修復語料與標註偏差，故為不正確敘述。B、C 都指出資料"
        "代表性不足會造成偏誤；D 則正確提醒架構能理解上下文，仍會從有偏"
        "訓練資料學到有偏規律。"
    ),
    "optionAnalysis": {
        "A": (
            "正確（本題要選的不正確敘述）。向量正規化可控制尺度、便於相似度"
            "比較，但不同語言／族群誤判更直接源於語料覆蓋、標註與分佈差異。"
            "許多分類模型也可在未單獨正規化詞嵌入時正常訓練。"
        ),
        "B": (
            "訓練語料偏向單一文化的情緒表達，會使模型把語氣強度、禮貌詞或"
            "俚語與標籤建立片面的相關性；部署到其他群體時，這些捷徑便可能"
            "形成系統性誤判，敘述正確。"
        ),
        "C": (
            "若某些語言或書寫風格樣本太少，模型沒有足夠例子學習其反諷、委婉"
            "批評與強烈讚美等模式。資料來源不平衡會使整體平均分數掩蓋弱勢"
            "切片表現，敘述正確。"
        ),
        "D": (
            "Transformer 的自注意力可形成上下文化表示，但學到什麼仍取決於"
            "訓練資料與目標函數。架構能力不會自動消除樣本、標註或社會歷史"
            "偏差，因此敘述正確。"
        ),
    },
    "trap": (
        "先圈出『不正確』，避免把三個合理風險選走。技術控制與治理原因也要"
        "分層：正規化處理向量尺度，代表性抽樣、標註一致性與切片評估才直接"
        "處理跨群體偏誤。"
    ),
    "references": [
        exam_ref(49),
        {
            "title": "NIST SP 1270－Towards a Standard for Identifying and Managing Bias in Artificial Intelligence",
            "url": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1270.pdf",
            "locator": "Executive Summary 與第 3、4 節：資料集代表性、測試評估及人類與系統因素都是 AI 偏誤來源；治理需超越單一計算修正",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[50] = {
    "summary": "正確答案是 C。四個選項中，文字與影像表示未能充分對齊最能解釋提示條件只被部分落實的跨模態偏差。",
    "concept": (
        "文字到影像系統需把提示中的物件、屬性與關係轉成可引導生成器的條件"
        "表示。CLIP 類模型以對比學習讓配對文字與影像在嵌入空間靠近，提供跨"
        "模態語意對齊；但全局語意相近不代表能精確保留品牌色碼、字樣或複雜"
        "手部幾何。實際缺陷也可能來自訓練資料覆蓋、文字編碼、條件注入、"
        "生成器空間能力與隨機採樣，不宜只歸因單一元件。"
    ),
    "answerReason": (
        "題幹的主題與場景正確、細部屬性與姿勢失真，C 在四項中最接近合理"
        "機制：跨模態表示若只捕捉粗略語意，文字指定的細節就可能未被生成過程"
        "忠實實現。A 所稱隨機梯度漂移不是推論去噪的標準原因；B 的短提示未超出"
        "上下文；D 又與 CLIP 通常正是用對比學習建立對齊的事實相悖。"
    ),
    "optionAnalysis": {
        "A": (
            "擴散模型推論會從隨機噪聲逐步去噪，但通常不做訓練用的隨機梯度"
            "更新，因此『隨機梯度漂移』不是標準推論機制。取樣隨機性可造成"
            "輸出差異，卻不能以此術語直接解釋品牌色與手部問題。"
        ),
        "B": (
            "題示提示僅包含主體、物件與場景，遠低於一般文字編碼器的上下文"
            "長度；沒有證據顯示位置編碼溢出。若真的截斷，通常是超長提示後段"
            "未被採用，不符合此情境。"
        ),
        "C": (
            "正確（依官方選項比較）。文字與影像表示的對齊若不足以精確編碼"
            "顏色、品牌視覺或空間關係，生成器可能只符合『飲料、模特兒、海邊』"
            "等粗粒度概念，而在細節上偏離。"
        ),
        "D": (
            "CLIP 的核心訓練方式本來就是對比學習：提高正確圖文配對的相似度，"
            "降低錯誤配對的相似度。因此不能直接說未使用對比損失，且就算已用"
            "對比學習，也不保證所有細節與幾何都能完美生成。"
        ),
    },
    "trap": (
        "先排除不合機制的術語：擴散推論不是靠梯度訓練更新，短提示也沒有超長"
        "問題，CLIP 更不是未用對比學習。剩下 C 是相對最佳，但要記得圖文嵌入"
        "對齊只是整個生成管線的一環。"
    ),
    "editorialNote": (
        "本站依官方答案 C 撰寫，但題目將品牌顏色與手部失真統一歸因於 CLIP"
        "文字／影像編碼器未充分對齊，屬過度簡化。CLIP 原始用途是學習全局圖文"
        "表示；實際文字到影像擴散模型的細節失真還可能來自訓練資料、條件注入、"
        "生成器表示能力與取樣。且並非所有生成管線都直接以 CLIP 影像編碼器"
        "參與生成。待人工複核是否需標示為『四個選項中的相對最佳解』。查核日期 2026-08-12。"
    ),
    "references": [
        exam_ref(50),
        paper_ref(
            "2103.00020",
            "Radford et al., Learning Transferable Visual Models From Natural Language Supervision（CLIP, 2021）",
            "摘要與第 2.2 節：CLIP 以自然語言監督及對比目標，預測批次中哪個文字與哪張影像配對",
        ),
        paper_ref(
            "2112.10752",
            "Rombach et al., High-Resolution Image Synthesis with Latent Diffusion Models（2022）",
            "摘要與第 3.3 節：以 cross-attention 將文字等條件注入潛在擴散模型，說明文字到影像管線不只是單一 CLIP 對齊步驟",
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
