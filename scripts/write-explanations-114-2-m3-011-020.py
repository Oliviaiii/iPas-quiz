"""Write draft explanations for 114-2 intermediate subject three, Q11-Q20.

The script verifies official answers, refuses to overwrite reviewed questions,
and only writes when explicitly executed.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-114-intermediate-2-machine-learning"
AUTHOR = "Codex（AI 輔助初稿）"
AUTHORED_AT = "2026-08-12"
CHECKED_AT = "2026-08-12"

EXAM_PDF = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/114年第二梯次中級AI應用規劃師"
    "第三科機器學習技術與應用(當次試題公告114_20251226000650.pdf"
)
DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


def exam_ref(number: int) -> dict:
    return ref(
        "114 年第二次中級 AI 應用規劃師－機器學習技術與應用公告試題",
        EXAM_PDF,
        f"第 {number} 題題幹、選項與官方答案",
    )


EXPECTED_ANSWER = {
    11: "D", 12: "C", 13: "B", 14: "C", 15: "B",
    16: "A", 17: "B", 18: "A", 19: "C", 20: "C",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[11] = {
    "summary": "正確答案是 D。Random Search 不必枚舉完整笛卡兒網格，在高維空間中可把固定試驗預算分散到更多不同參數值。",
    "concept": (
        "Grid Search 對每個超參數列出候選值後枚舉所有組合，維度增加時組合數呈乘法成長。"
        "Random Search 則由指定分布抽樣組合；當真正影響結果的參數只有少數時，每次試驗通常能探索更多有效維度上的不同值，"
        "因此在相同運算預算下較有機會找到良好區域，但仍不保證全域最佳解。"
    ),
    "answerReason": "D 正確描述隨機搜尋相對網格搜尋在高維超參數空間的主要效率優勢。它改變的是候選組合的取樣方式，不會自動設計模型、增加訓練資料或消除過擬合。",
    "optionAnalysis": {
        "A": "Random Search 只抽樣既定超參數空間，除非搜尋空間本身含架構選項，否則不會自動產生神經網路或其他模型架構。",
        "B": "搜尋方法不會讓原始訓練集變大；每次試驗能使用多少資料由資料管線與資源限制決定，並非 Random Search 的固有優勢。",
        "C": "超參數搜尋仍可能依驗證集反覆選擇而過擬合；需靠獨立測試集、巢狀交叉驗證與正則化控制，不能說隨機搜尋會避免過擬合。",
        "D": "正確。固定試驗次數下，隨機抽樣避免把預算耗在所有網格組合，尤其當高維空間只有部分參數真正重要時，探索通常更有效率。",
    },
    "trap": "不要把『通常較有效率』誤解成必然找到最佳值；結論是在相同搜尋預算與合理抽樣分布下的比較，而非品質保證。",
    "references": [
        exam_ref(11),
        ref("Bergstra & Bengio, Random Search for Hyper-Parameter Optimization", "https://jmlr.org/papers/v13/bergstra12a.html", "摘要與第 1 至 2 節：比較 grid search 與 random search，說明只有少數超參數重要時隨機搜尋更有效率"),
    ],
}

DRAFTS[12] = {
    "summary": "正確答案是 C。學習率直接縮放每一步的權重更新幅度，是調整神經網路收斂速度與穩定性的核心超參數。",
    "concept": (
        "梯度式最佳化會依損失函數對權重的梯度更新參數，學習率決定沿該方向移動多大一步。"
        "過大可能跨過良好解、震盪甚至發散；過小則收斂緩慢或在有限訓練時間內無法到達較佳區域。"
        "實務可配合學習率排程、早停與驗證曲線，但學習率本身不等同於防止過擬合。"
    ),
    "answerReason": "C 是四項中可由開發者在訓練前設定、且直接控制權重更新速度的超參數。其餘選項是前向輸出、由資料與目前權重算出的梯度，或訓練結果，不是此處要調整的控制量。",
    "optionAnalysis": {
        "A": "神經元輸出由輸入、權重、偏差與活化函數計算而來，是模型運算結果，不是用來直接控制整體收斂速度的超參數。",
        "B": "梯度是對目前損失與權重求導得到的訊號；演算法會利用梯度，但不能把每一步實際梯度值當作人工預先指定的超參數。",
        "C": "正確。學習率乘上梯度形成更新步幅，調低可減少震盪，調高可加速進展，但必須以驗證結果與穩定性共同選擇。",
        "D": "訓練後權重是最佳化過程產生的已學習參數，不是事前設定的超參數；任意手動更改也無法系統性改善收斂。",
    },
    "trap": "題幹把過快與過擬合並列，但過擬合還受模型容量、訓練輪數與正則化影響；學習率主要控制更新與收斂，仍須搭配驗證監控。",
    "references": [
        exam_ref(12),
        ref("Keras－SGD optimizer", "https://keras.io/api/optimizers/sgd/", "參數與更新式：learning_rate 乘上 gradient，momentum 另為獨立設定"),
    ],
}

DRAFTS[13] = {
    "summary": "正確答案是 B。若標註者的主觀判斷或既有社會偏見進入標籤，模型便會把這些系統性差異當成學習目標。",
    "concept": (
        "監督式學習把標籤視為目標真值，因此標註規則、標註者背景、模糊案例處理方式及歷史決策都會影響模型。"
        "若某些族群或案例被系統性地錯標，而非單純隨機雜訊，模型可能重現甚至放大該偏差。"
        "治理上應制定操作化標準、量測標註者一致性、抽樣稽核並分析不同群體的錯誤分布。"
    ),
    "answerReason": "B 直接對應標籤偏差的來源：標記資料本身帶有系統性的主觀偏見。資料量、模型結構與特徵數量會影響訓練，但不會單獨構成『標籤中的偏差』。",
    "optionAnalysis": {
        "A": "資料量過大可能增加成本，卻不會自然造成標籤偏差；若標註流程本來有偏差，增加同類資料甚至可能更穩定地複製該偏差。",
        "B": "正確。標註者的價值判斷、歷史制度或不一致準則若系統性影響標籤，模型就會把主觀偏差視為應預測的真值。",
        "C": "模型結構不當可能造成欠擬合、過擬合或特定誤差，但標籤偏差特指目標資料生成或標記過程的問題，兩者層級不同。",
        "D": "特徵太多可能帶來維度災難與過擬合風險，卻不會因此改變既有標籤的內容；這是輸入設計而非標註偏差。",
    },
    "trap": "不要把所有模型偏差都叫作 label bias；本題語境指標籤生成或人工標記的系統性偏差，需回頭檢查標註定義與流程。",
    "references": [
        exam_ref(13),
        ref("NIST SP 1270－Towards a Standard for Identifying and Managing Bias in Artificial Intelligence", "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1270.pdf", "第 3 至 4 節：人類、系統與統計偏差可在資料生命週期與人工決策中進入 AI 系統"),
    ],
}

DRAFTS[14] = {
    "summary": "正確答案是 C。腫瘤惡性機率會影響臨床判斷與病人安全，醫師必須能理解模型輸出的依據、限制與風險。",
    "concept": (
        "可解釋性是讓人能理解輸出如何或基於何種資訊形成，屬於 AI 醫材透明度的一部分。"
        "當模型支援高風險醫療決策時，錯誤可能延誤診斷或導致不必要處置，使用者需要知道適用族群、效能、失效模式、"
        "不確定性與輸出依據，以便批判性評估，而不是把分數當成不可質疑的結論。"
    ),
    "answerReason": "四個情境都可受益於解釋，但 C 直接關係疾病診斷與病人結果，錯誤代價最高，也要求臨床人員判斷模型是否適用於個案，因此可解釋性最關鍵。",
    "optionAnalysis": {
        "A": "購買時間預測的解釋可改善行銷與除錯，但錯誤通常造成推播時機不佳，對人身安全與重大權益的直接影響低於臨床診斷。",
        "B": "廣告出價需要成本歸因與策略監控，解釋仍有商業價值；然而主要後果通常是預算與轉換效率，不及醫療誤判的風險。",
        "C": "正確。腫瘤惡性可能性會支持臨床診斷，醫師須理解依據、限制、偏差與不確定性，才能安全整合模型輸出與專業判斷。",
        "D": "客戶流失預測影響優惠分配，仍應檢查公平性與理由；但就題目四項比較，通常不如可能改變病人診療的醫療情境關鍵。",
    },
    "trap": "『最為關鍵』是風險比較，不代表其他商業模型不需要透明度；應看錯誤後果、受影響權益，以及人類是否需據此做重大決策。",
    "references": [
        exam_ref(14),
        ref("FDA／Health Canada／MHRA－Transparency for Machine Learning-Enabled Medical Devices", "https://www.fda.gov/medical-devices/software-medical-device-samd/transparency-machine-learning-enabled-medical-devices-guiding-principles", "Why 與 What：透明度支援安全、風險管理與知情決策；輸出邏輯有助臨床照護時批判性評估"),
    ],
}

DRAFTS[15] = {
    "summary": "正確答案是 B。R² 為 0.85 表示相對於以目標平均值預測的基準，模型解釋了觀測目標變異的 85%。",
    "concept": (
        "決定係數常寫成 R² = 1 − SSE/SST，其中 SSE 是殘差平方和，SST 是目標相對平均值的總平方和。"
        "值為 0.85 表示在本資料與評估設定下，殘差變異相對基準減少 85%。R² 不是分類準確率、單筆誤差百分比或統計信心水準，"
        "也不能單獨證明因果、無偏或可泛化。"
    ),
    "answerReason": "B 符合決定係數的標準解讀。A 把回歸指標當分類準確率，C 將剩餘未解釋變異誤當預測誤差百分比，D 則混淆配適度與信賴區間。",
    "optionAnalysis": {
        "A": "R² 衡量回歸模型相對平均值基準所解釋的變異比例，不是預測命中次數除以總數，因此不能表述為 85% 準確率。",
        "B": "正確。在一般含截距且以同一資料脈絡解讀時，R²=0.85 表示模型可解釋目標總變異的 85%，仍有約 15% 未被解釋。",
        "C": "1−R² 等於殘差平方和占總平方和的比例，不代表每次預測誤差都是 15%，也不是 MAE、RMSE 或相對百分比誤差。",
        "D": "信心水準是區間估計程序的涵蓋率設定，需要抽樣分布與標準誤等資訊；R²=0.85 本身不能推出 85% 信心水準。",
    },
    "trap": "看到 0.85 不要把所有比例概念混在一起；先辨認 R² 的分子分母是平方和，再排除 accuracy、error rate 與 confidence level。",
    "references": [
        exam_ref(15),
        ref("scikit-learn－r2_score", "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html", "定義與 Notes：最佳值為 1，常數平均預測可得 0，且 R² 可能為負"),
    ],
}

DRAFTS[16] = {
    "summary": "正確答案是 A。F1 是 Precision 與 Recall 的調和平均，代入 0.8 與 0.6 得 0.96/1.4，約為 0.686。",
    "concept": (
        "Precision = TP/(TP+FP)，著重被判為正類者有多少真的為正；Recall = TP/(TP+FN)，著重真實正類有多少被找出。"
        "F1 = 2PR/(P+R) 是兩者的調和平均，任一項偏低都會拉低結果。它適合需要兼顧假陽性與假陰性的情境，"
        "但不同錯誤成本或極端不平衡時仍可能需 PR 曲線、Fβ 或成本指標。"
    ),
    "answerReason": "代入 P=0.8、R=0.6：F1=2×0.8×0.6÷(0.8+0.6)=0.96÷1.4=0.685714…，四捨五入至三位小數為 0.686，因此選 A。",
    "optionAnalysis": {
        "A": "正確。完整計算為 0.685714…，依選項取三位小數就是 0.686，且介於 precision 與 recall 之間並更靠近較小值。",
        "B": "0.700 是兩者的算術平均 (0.8+0.6)/2；F1 使用調和平均而非算術平均，所以在兩值不同時會稍低於 0.700。",
        "C": "0.720 不符合 2PR/(P+R)；可能源於誤乘或錯誤分母。應先算分子 0.96，再除以 1.4，而非任意平均。",
        "D": "0.750 高於 precision 與 recall 的調和平均合理範圍，無法由給定數值依 F1 公式算得，亦未反映 recall 僅 0.6。",
    },
    "trap": "常見錯誤是直接算算術平均得到 0.7；記住 F1 的分子是 2PR、分母是 P+R，最後才依題目精度四捨五入。",
    "references": [
        exam_ref(16),
        ref("scikit-learn－Precision, recall and F-measures", "https://scikit-learn.org/stable/modules/model_evaluation.html#precision-recall-f-measure-metrics", "分類指標章節：precision、recall 與 F-beta/F1 的定義及公式"),
    ],
}

DRAFTS[17] = {
    "summary": "正確答案是 B。依官方答案，Adam 會維持梯度的一階動差指數移動平均，形成類似動量的內建機制。",
    "concept": (
        "傳統 momentum 對過往更新或梯度做指數累積，使更新方向具有慣性。Adam 同時追蹤梯度的一階動差與平方梯度的二階動差，"
        "並進行偏差校正；其中一階動差常被理解為 momentum-like 機制。不過『SGD+Momentum』按名稱與公式也明確包含 momentum，"
        "因此本題若未限定『無須另外加掛 momentum 的演算法』便不是唯一答案。"
    ),
    "answerReason": "官方答案選 B，合理意圖應是辨認 Adam 原生追蹤梯度一階動差，不需另以附加模組命名。但 A 的 SGD+Momentum 也明確使用動量，故只能依官方答案作答並保留題意歧義。",
    "optionAnalysis": {
        "A": "就技術事實而言也含動量：SGD+Momentum 正是替 SGD 加入速度累積項。若題目問『哪一個使用 momentum』，A 無法被合理排除。",
        "B": "依官方答案為正確。Adam 內建梯度一階動差的指數移動平均，以及平方梯度二階動差，前者具有動量式平滑與方向累積效果。",
        "C": "標準 RMSProp 主要以平方梯度的移動平均調整各參數步幅；某些實作可另設 momentum，但單寫 RMSProp 並不必然表示啟用動量。",
        "D": "Adagrad 累積歷史平方梯度以縮放學習率，常使有效步幅持續下降；它不是以一階速度項累積更新方向的典型 momentum 方法。",
    },
    "trap": "考試可能把『Adam 原生具有一階動差』當命題點，但不能因此說 SGD+Momentum 沒有動量；正式審題應要求題幹增加排他條件。",
    "editorialNote": (
        "本站依官方答案 B 撰寫，但本題存在明確複選歧義。Keras 官方 SGD 文件直接將其描述為 gradient descent (with momentum)，"
        "且公式在 momentum>0 時使用 velocity；Adam 原論文與官方文件則說明其使用一階、二階動差估計。因此 A『SGD+Momentum』與 B『Adam』"
        "都具動量或動量式機制。建議人工複核並將題幹改為『下列何者在演算法中同時內建一階與二階動差估計』或排除 A。查核日期 2026-08-12。"
    ),
    "references": [
        exam_ref(17),
        ref("Keras－SGD optimizer", "https://keras.io/api/optimizers/sgd/", "頁首與更新式：SGD 支援 momentum，momentum>0 時使用 velocity"),
        ref("Keras－Adam optimizer", "https://keras.io/api/optimizers/adam/", "說明：Adam 基於梯度一階與二階動差的自適應估計"),
        ref("Kingma & Ba, Adam: A Method for Stochastic Optimization", "https://arxiv.org/abs/1412.6980", "摘要與演算法 1：計算梯度的一階、二階動差指數移動平均並做偏差校正"),
    ],
}

DRAFTS[18] = {
    "summary": "正確答案是 A。XGBoost 的核心改進包括正則化學習目標、稀疏感知的缺失值處理，以及可擴展的平行化建樹。",
    "concept": (
        "XGBoost 仍是梯度提升樹，不是改換成隨機森林或神經網路。它在提升目標加入樹複雜度正則化，利用二階近似推導分裂增益，"
        "並以 sparsity-aware 演算法為缺失值學習預設分支方向。系統層面另採欄位區塊、平行掃描、快取與分散式設計來擴充訓練效率。"
    ),
    "answerReason": "A 同時涵蓋統計面與系統面的代表性改進：以正則化抑制複雜度、原生處理稀疏或缺失輸入，並支援平行化。B 至 D 都把 XGBoost 說成不同模型家族或不相關技術。",
    "optionAnalysis": {
        "A": "正確。XGBoost 論文的 regularized objective、sparsity-aware split finding 與 scalable parallel tree learning，正好對應題列三項改進。",
        "B": "XGBoost 的基學習器仍是加法式建立的決策樹；Random Forest 採 bagging 與隨機特徵抽樣，並未取代 XGBoost 的 boosting 架構。",
        "C": "XGBoost 沒有以神經網路取代弱學習器，名稱中的 tree boosting 即表示以樹作為基學習器，逐輪修正目前模型的目標。",
        "D": "Batch Normalization 是神經網路常見的批次統計正規化層，不是 XGBoost 相對傳統 GBDT 的代表性機制，也不作用於樹節點。",
    },
    "trap": "『正則化』與『正規化』字面相近但不同；XGBoost 的 regularization 是限制樹複雜度，並不是神經網路的 Batch Normalization。",
    "references": [
        exam_ref(18),
        ref("Chen & Guestrin, XGBoost: A Scalable Tree Boosting System", "https://arxiv.org/abs/1603.02754", "摘要、第 2 節與第 3 節：regularized objective、sparsity-aware algorithm、parallel and distributed computation"),
    ],
}

DRAFTS[19] = {
    "summary": "正確答案是 C。在正類僅 3% 時，單看 Accuracy 可能讓全猜陰性的模型得到約 97%，卻完全找不到確診病例。",
    "concept": (
        "類別極度不平衡時，多數類可主宰整體準確率，因此評估應呈現少數類的 recall、precision、F1、PR-AUC 或依臨床成本選定的指標。"
        "SMOTE、類別權重與欠採樣則是訓練端常見策略，各自有合成雜訊、機率校準或資訊損失等代價。"
        "任何重採樣都應只在交叉驗證的訓練摺內執行，避免測試資訊洩漏。"
    ),
    "answerReason": "本題問『最不適合』。C 不會提升模型對少數類的學習能力，而且作為主要指標會掩蓋漏診；A、B、D 雖各有風險，都是可用來增加少數類影響力的常見方法。",
    "optionAnalysis": {
        "A": "SMOTE 在特徵空間插值合成少數類樣本，可減少模型忽略正類，但需在訓練摺內使用並檢查合成樣本是否跨越類別邊界。",
        "B": "提高正類權重會讓漏判確診病例在損失函數中付出更大代價，常能改善少數類 recall；仍需驗證 precision 與機率校準。",
        "C": "正確（最不適合）。若模型一律預測陰性即可有約 97% accuracy，這個高分仍對正類 recall 為 0，會嚴重誤導早期偵測成效。",
        "D": "欠採樣可降低多數類支配程度並平衡訓練，但會丟掉部分陰性資訊；若資料足夠且採樣合理，仍是可考慮的訓練策略。",
    },
    "trap": "先注意題目有否定詞『最不適合』；Accuracy 不是永遠錯，而是在 3% 正類且關心漏診時，不能作為唯一或主要效能依據。",
    "references": [
        exam_ref(19),
        ref("scikit-learn－Classification metrics", "https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics", "分類指標章節：accuracy、balanced accuracy、precision、recall、F-measures 與 precision-recall curve"),
        ref("imbalanced-learn－SMOTE", "https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html", "API 說明：SMOTE 是少數類過採樣方法，sampling_strategy 控制重採樣後類別分布"),
    ],
}

DRAFTS[20] = {
    "summary": "正確答案是 C。把價格與滿意度等兩個以上特徵相乘或交互組合，可建立代表共同作用的 interaction feature。",
    "concept": (
        "互動效果表示一個特徵對預測的影響會隨另一特徵而改變。對數值特徵加入 x1×x2，可讓線性模型估計兩者共同作用；"
        "類別特徵則可交叉組合成聯合類別。平方項 x1² 描述單一變數的非線性，對數轉換改變尺度，標準化只改變中心與量綱，"
        "三者都不會自行創造兩個不同特徵之間的交互項。"
    ),
    "answerReason": "C 直接把兩個或多個原始特徵組合成新欄位，符合互動特徵的定義。A 只有單一特徵自乘，B 與 D 只是逐欄轉換，沒有表示價格與滿意度的共同效果。",
    "optionAnalysis": {
        "A": "單一特徵平方是 polynomial feature，可表示該變數的曲線關係，但沒有結合另一個不同特徵，因此不是題示的價格×滿意度互動。",
        "B": "對每個特徵取對數可降低偏態或把乘法關係轉成加法尺度，但若只是逐欄轉換，並未直接建立特徵之間的交互組合。",
        "C": "正確。建立價格×滿意度或其他交叉組合，讓模型取得兩者共同出現時的額外訊號，正是 interaction feature 的典型做法。",
        "D": "標準化把特徵調整為相近尺度，有助某些模型最佳化與正則化，卻仍保留各欄獨立形式，不會自動產生交互項。",
    },
    "trap": "Polynomial features 包含平方項與交互項，但兩者不要混稱；本題明示『不同特徵之間』，所以應選 x1×x2 等交叉組合。",
    "references": [
        exam_ref(20),
        ref("scikit-learn－PolynomialFeatures", "https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PolynomialFeatures.html", "類別與 interaction_only 參數：產生輸入特徵的多項式與 interaction terms，例如 x1*x2"),
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
