"""Write draft explanations for 115-1 intermediate subject three, Q1-Q10.

The script verifies official answers and refuses to overwrite reviewed work.
Run the draft validator before applying it to the shared question bank.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-intermediate-1-machine-learning"
AUTHOR = "Codex（AI 輔助初稿）"
AUTHORED_AT = "2026-08-13"
CHECKED_AT = "2026-08-13"

EXAM_PDF = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/"
    "115年第一次中級AI應用規劃師_第三科_機器學習技術與應用_公告試題_20260615003428.pdf"
)
DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def exam_ref(number: int) -> dict:
    return {
        "title": "115 年第一次中級 AI 應用規劃師－機器學習技術與應用公告試題",
        "url": EXAM_PDF,
        "locator": f"第 {number} 題題幹、選項與官方答案",
        "checkedAt": CHECKED_AT,
    }


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


EXPECTED_ANSWER = {
    1: "C", 2: "C", 3: "A", 4: "C", 5: "C",
    6: "B", 7: "B", 8: "B", 9: "A", 10: "A",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[1] = {
    "summary": "正確答案是 C。蒙地卡羅方法以大量隨機抽樣建立可能的市場情境，再由模擬損失的經驗分布近似投資組合風險。",
    "concept": (
        "蒙地卡羅方法（Monte Carlo Method）用重複隨機抽樣近似難以解析求得的機率、期望值或分布。"
        "在風險值情境中，可先依市場因子的假設分布產生大量未來路徑，逐一重估投資組合損益，再從損失分布分位數估計 VaR。"
        "模擬品質取決於定價模型、相關結構、樣本數與隨機數設計；樣本增加通常降低抽樣誤差，但不會修正錯誤的市場假設。"
    ),
    "answerReason": "題幹的關鍵是『無解析解、產生大量隨機市場情境、近似損失分布』，這正是蒙地卡羅模擬的工作方式，因此選 C。",
    "optionAnalysis": {
        "A": "馬可夫鏈以狀態與轉移機率描述下一狀態只依賴目前狀態的隨機過程，可作為某些模擬的取樣工具；但題幹未描述狀態轉移，核心是大量隨機情境的數值近似。",
        "B": "梯度下降根據目標函數梯度反覆更新模型參數，目的在尋找較小損失的參數；它處理最佳化問題，不是從隨機市場路徑建立損失分布的風險模擬框架。",
        "C": "正確。蒙地卡羅方法反覆抽取市場因子、計算各情境下的投資組合損益，最後用模擬得到的經驗分布近似無法直接解析求出的風險量。",
        "D": "貝氏推論以似然與先驗分布更新後驗分布，適合在觀測資料加入後修正參數不確定性；題幹沒有先驗與後驗更新，而是在既定假設下做大量隨機模擬。",
    },
    "trap": "蒙地卡羅是廣泛的隨機數值方法；馬可夫鏈只是特定隨機過程，MCMC 才是兩者的組合。不要看到『隨機』就直接選馬可夫鏈。",
    "references": [
        exam_ref(1),
        ref("NIST－New Tool to Account for Uncertainty", "https://www.nist.gov/news-events/news/2020/01/new-tool-account-uncertainty", "Monte Carlo analysis 對輸入變數反覆隨機取樣並彙整模型結果，以評估不確定性"),
    ],
}

DRAFTS[2] = {
    "summary": "正確答案是 C。MSE 將殘差平方，因此豪宅造成的大誤差會被放大，其梯度大小也隨誤差絕對值增加。",
    "concept": (
        "均方誤差（MSE）計算殘差平方的平均；單筆損失為 (y−ŷ)²，對預測值的梯度大小與 |y−ŷ| 成正比。"
        "因此極端高價物件若預測偏差很大，會比一般物件產生更大的損失與更新影響。MAE 對誤差採線性懲罰，Huber 則在大誤差區轉為線性，兩者通常用來降低離群值支配訓練的程度。"
        "本題明確要求『更敏感』，所以應選 MSE；實務上仍要先判斷豪宅是有效樣本還是資料錯誤。"
    ),
    "answerReason": "C 的平方懲罰會讓十倍量級價格所造成的大殘差快速放大，且其梯度不固定，最符合題目希望極端物件對參數更新影響更大的要求。",
    "optionAnalysis": {
        "A": "MAE 對殘差取絕對值，大誤差的損失只線性增加，除零點外梯度幅度近似固定；它較穩健，但不符合題目要讓極端誤差產生更大梯度的目的。",
        "B": "Huber 在小殘差使用平方項、大殘差改用線性項，設計目的正是兼顧平滑最佳化與降低離群值影響；豪宅的大殘差會落在線性區，敏感度低於純 MSE。",
        "C": "正確。MSE 對殘差平方，單筆梯度與殘差成比例；極端高價物件若預測錯很多，對總損失與梯度更新的貢獻都會顯著增加。",
        "D": "交叉熵比較分類標籤與預測類別機率，適合二元或多類分類；房價是連續值迴歸，不能因為想放大誤差就改用分類損失。",
    },
    "trap": "題目不是問『如何降低離群值影響』，而是反過來要求對極端值更敏感。MSE 放大大誤差；MAE 與 Huber 則較具穩健性。",
    "references": [
        exam_ref(2),
        ref("scikit-learn User Guide－Metrics and scoring: regression metrics", "https://scikit-learn.org/stable/modules/model_evaluation.html#mean-squared-error", "MSE、MAE 與 Huber 類損失對迴歸殘差的不同處理"),
    ],
}

DRAFTS[3] = {
    "summary": "正確答案是 A。矩陣乘法 (1, 10) × (10, 64) 的內維度 10 相同，輸出保留外維度而成為 (1, 64)。",
    "concept": (
        "二維矩陣相乘遵循 (m, n) × (n, p) → (m, p)：左矩陣的欄數必須等於右矩陣的列數，結果的形狀由左矩陣列數與右矩陣欄數決定。"
        "此處一筆 Query 有 10 個輸入特徵，WQ 將每個 10 維向量線性投影到 64 維，所以結果是一筆 64 維 Query 表示。"
        "這個規則只判斷線性投影的形狀；實際 Transformer 常另有 batch、序列長度與多頭維度。"
    ),
    "answerReason": "Q 的最後一維 10 與 WQ 的第一維 10 可收縮相乘，剩餘外維度依序是 1 與 64，因此 QWQ 的形狀是 (1, 64)。",
    "optionAnalysis": {
        "A": "正確。依 (m,n)×(n,p)=(m,p)，令 m=1、n=10、p=64，乘積包含一列且每列有 64 個投影後的特徵。",
        "B": "(10,10) 可能來自把兩個十維方向做外積，但本題是列向量乘上 10×64 權重；收縮掉共同的 10 後，不會留下兩個 10 維。",
        "C": "(64,1) 是結果轉置後的形狀；若採欄向量慣例，會以 WQ 的轉置或不同乘法順序表示，但題目已明確指定 (1,10)×(10,64)。",
        "D": "矩陣相乘只要求左側欄數等於右側列數，本題兩者都是 10，所以維度相容；若是 (1,10)×(64,10) 才不能直接相乘。",
    },
    "trap": "只比對相乘處的『內維度』，相同就能乘；輸出寫『外維度』。不要把數字倒過來，也不要套用逐元素相乘的同形狀規則。",
    "references": [
        exam_ref(3),
        ref("NumPy Reference－numpy.matmul", "https://numpy.org/doc/stable/reference/generated/numpy.matmul.html", "二維矩陣乘法的核心維度相容與輸出形狀規則"),
    ],
}

DRAFTS[4] = {
    "summary": "正確答案是 C。手寫數字的左右方向可能是類別語意的一部分，水平鏡像後卻沿用原標籤，會產生不合理甚至近似其他字形的訓練樣本。",
    "concept": (
        "資料擴增只有在轉換後標籤仍成立時才是 label-preserving transformation。水平翻轉常適合一般物體，因為貓、狗或行人面向左右通常不改類別；"
        "但文字、數字、交通號誌方向與醫療影像左右側等任務可能具有方向語意，鏡像後不能無條件保留標籤。"
        "若轉換破壞標籤一致性，模型會收到同一輸入模式對應錯誤類別的監督訊號，泛化反而下降。"
    ),
    "answerReason": "手寫數字的筆畫方向與形狀定義類別，鏡像數字可能不是合法數字或接近另一字形；仍保留原標籤會引入語意不一致，因此 C 最可能受害。",
    "optionAnalysis": {
        "A": "貓與狗的物種標籤通常不因面向左或右而改變，所以水平翻轉多半仍保留類別；若任務判斷身體左右側病灶才需另行限制。",
        "B": "多數車型分類辨識品牌或車種，左右鏡像通常不會把轎車變成另一類車；但若類別取決於駕駛座位置、文字標誌或不對稱細節，才可能不適用。",
        "C": "正確。手寫數字的方向具有語意，鏡像後的筆畫可能不再是原數字或與別的字形混淆；若標籤不跟著改，就會製造錯誤監督資料。",
        "D": "行人偵測的目標是定位是否有人，人物朝左或朝右仍是行人，因此水平翻轉通常是可用的幾何增強，且邊界框可同步轉換。",
    },
    "trap": "不是所有影像都可套相同增強。先問轉換後『答案是否仍相同』；若方向本身承載標籤語意，水平翻轉就不是安全的標籤保留操作。",
    "references": [
        exam_ref(4),
        ref("PyTorch Vision－RandomHorizontalFlip", "https://docs.pytorch.org/vision/stable/generated/torchvision.transforms.RandomHorizontalFlip.html", "水平翻轉的影像轉換定義與機率參數"),
        ref("TensorFlow Image－Data augmentation", "https://www.tensorflow.org/tutorials/images/data_augmentation", "資料擴增應只套用對資料有意義且能保留標籤的轉換"),
    ],
}

DRAFTS[5] = {
    "summary": "正確答案是 C。殘差的散布寬度隨預測值增加而擴大，是變異數不恆定（heteroscedasticity）的典型漏斗形訊號。",
    "concept": (
        "線性迴歸常假設在給定解釋變數下，誤差項具有固定變異數。殘差圖若在整個擬合值範圍呈大致等寬的隨機帶狀，較符合等變異；"
        "若越往右越分散，表示條件變異數隨預測水準改變，稱異質變異或變異數不一致。"
        "它可能使傳統標準誤、信賴區間與檢定失真，可考慮轉換目標、加入遺漏結構、加權最小平方法或異質變異穩健標準誤。"
    ),
    "answerReason": "題幹直接描述殘差呈右側擴散的漏斗形，而非沿時間連續成串、單一殘差分布偏斜或特徵彼此相關，因此最直接診斷是 C。",
    "optionAnalysis": {
        "A": "殘差相關通常要依時間或觀測順序畫殘差、查看 ACF 或使用 Durbin-Watson 等方法；單看殘差隨擬合值的垂直散布擴大，主要反映變異數改變。",
        "B": "特徵高度相關是多重共線性，常造成係數不穩、標準誤增大，可用相關矩陣或 VIF 檢查；它不以殘差圖的漏斗形作為直接特徵。",
        "C": "正確。預測值愈大，殘差的條件散布愈寬，表示誤差變異數不是常數，違反同方差假設，這正是 heteroscedasticity 的典型圖像。",
        "D": "常態性關注殘差整體分布形狀，通常以 Q-Q plot 或直方圖檢查；漏斗形可以與非常態同時存在，但不能單憑它把主要問題判成非常態。",
    },
    "trap": "殘差圖的『寬度隨擬合值改變』看變異數；殘差隨順序呈週期看自相關；Q-Q 圖偏離直線才主要看常態性。",
    "references": [
        exam_ref(5),
        ref("NIST Engineering Statistics Handbook－Residual Plots", "https://www.itl.nist.gov/div898/handbook/pri/section2/pri24.htm", "殘差圖用於檢查固定變異數、獨立性與模型形式等假設"),
    ],
}

DRAFTS[6] = {
    "summary": "正確答案是 B。t-SNE 著重保存局部鄰域並主要用於低維視覺化；它不可靠地保存全局距離，也不像 PCA 提供固定線性投影供模型前處理與新資料轉換。",
    "concept": (
        "t-SNE 以高維與低維鄰近機率的差異為目標，擅長把局部相似樣本放在附近，常用於二維或三維探索。"
        "群集間距離、大小與全局排列會受 perplexity、初始化與隨機最佳化影響，不應直接當成原空間全局幾何。"
        "PCA 則以正交線性成分最大化保留變異，能把同一個已擬合投影套到新資料，較適合作為 XGBoost 前的固定降維步驟；是否值得降維仍應以驗證結果決定。"
    ),
    "answerReason": "題目一邊需要詞嵌入群集視覺化、一邊需要穩定的模型輸入。B 正確區分 t-SNE 的局部視覺化用途與其全局結構及新資料轉換限制。",
    "optionAnalysis": {
        "A": "t-SNE 的目標是保留局部鄰域機率，不保證群集間全局距離與方向；把其低維座標當作穩定的 XGBoost 生產特徵，會受隨機性與重新擬合影響。",
        "B": "正確。t-SNE 適合把十萬筆嵌入的局部鄰近關係投影供探索，但圖上的遠距與群集大小不代表可靠全局結構，也沒有 PCA 那種天然固定線性映射。",
        "C": "PCA 是線性降維：以資料協方差的主方向建立正交線性組合；若要刻畫彎曲流形，通常需 kernel PCA、Isomap、UMAP 或 t-SNE 等非線性方法。",
        "D": "PCA 擬合後可用同一組主成分對新資料做線性 transform；標準 t-SNE 通常需與既有資料重新最佳化，並非可直接外推的線性映射。",
    },
    "trap": "t-SNE 圖上『群內近』較可解讀，『群間多遠、群多大』不可直接當成原資料的全局結構；PCA 才有明確線性投影與新資料 transform。",
    "references": [
        exam_ref(6),
        ref("Visualizing Data using t-SNE", "https://www.jmlr.org/papers/v9/vandermaaten08a.html", "t-SNE 以鄰近機率保存局部結構並用於高維資料視覺化"),
        ref("scikit-learn API－PCA", "https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html", "PCA 的線性降維、主成分與 transform 介面"),
    ],
}

DRAFTS[7] = {
    "summary": "正確答案是 B。L1 會產生稀疏解；多個高度相關特徵提供近似重複訊息時，最佳化可能只留下其中一個，使不同重訓的入選特徵不穩定。",
    "concept": (
        "Lasso／L1 正則化在損失中加入係數絕對值總和，能把部分係數精確壓到零，因此具有特徵選擇效果。"
        "月、季、年收入高度相關時，數個特徵能互相替代；資料抽樣、交叉驗證切分或最佳化細節的微小差異，就可能讓 L1 在等效候選中保留不同一個。"
        "這不代表模型預測一定不穩，而是個別係數與重要性歸屬不穩。可先合併重複語意、使用 Elastic Net／群組方法，並報告穩定性分析。"
    ),
    "answerReason": "題幹同時指出高度相關、重要特徵在重訓間輪替，正符合 L1 稀疏選擇在可互相替代特徵間不穩定的現象，因此選 B。",
    "optionAnalysis": {
        "A": "L2 通常把相關特徵的係數共同縮小而非全部精確壓成零；它可能讓重要性分散，但題目描述的是在相關特徵間反覆『選一個留下』，更符合 L1。",
        "B": "正確。L1 鼓勵稀疏解；月、季、年收入承載重疊資訊時，保留任一者都能相近地降低損失，因此小幅資料差異可能改變哪個係數非零。",
        "C": "沒有正則化確實可能使共線特徵係數不穩，但選項把原因說成過擬合與不同局部極值並不精確；線性凸模型的共線問題不是由每次落入不同極值來解釋。",
        "D": "梯度消失多見於深層網路反向傳播，並非因表格資料有 200 個特徵就自然發生；PCA 也可能降低可解釋性，應先處理語意重複與正則化選型。",
    },
    "trap": "預測表現穩定不等於特徵重要性穩定。當特徵高度相關，L1 的『稀疏』可能只是任選代表，不可把被歸零者解讀成毫無業務影響。",
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
        "官方答案 B 的『隨機保留』宜理解為重訓時受抽樣、資料切分或最佳化細節影響而可能改選代表特徵；"
        "L1 正則化本身並不必然採用隨機座標更新，確定性設定與完全相同資料也可能得到相同解。"
    ),
    "references": [
        exam_ref(7),
        ref("scikit-learn User Guide－Lasso", "https://scikit-learn.org/stable/modules/linear_model.html#lasso", "Lasso 使用 L1 penalty 估計 sparse coefficients 並可作特徵選擇"),
        ref("scikit-learn API－Lasso", "https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html", "高度相關特徵與不同 selection 設定下的係數更新行為"),
    ],
}

DRAFTS[8] = {
    "summary": "正確答案是 B。學習率過大會讓參數更新跨過低損失區，在最優點兩側來回跳動；更嚴重時損失持續增大而發散。",
    "concept": (
        "梯度式最佳化每一步大致為參數減去學習率乘梯度。學習率控制步幅：太小會收斂緩慢，太大則可能跨越谷底，造成 loss oscillation，甚至離開可穩定區域而 divergence。"
        "題幹前段的訓練損失下降、驗證損失上升表示原先已出現過擬合；但調高學習率後『訓練損失震盪』是另一個直接現象。"
        "診斷時應分清學習動態與泛化落差，並用 learning-rate schedule、warmup 或較小步幅處理。"
    ),
    "answerReason": "題目問學習率過大的直接結果；更新步幅太大會越過最佳區域，使損失反覆震盪或直接發散，正是 B 的描述。",
    "optionAnalysis": {
        "A": "梯度消失源於深層連鎖導數反覆乘上小量、飽和啟用函數或長序列等因素，使前層梯度接近零；它不是把全域學習率調大最直接造成的現象。",
        "B": "正確。學習率放大每次參數更新，若步幅大於損失谷底的穩定範圍，參數會跨過最佳點來回跳動，訓練損失因而震盪，嚴重時數值發散。",
        "C": "訓練損失持續下降但驗證損失上升才是過擬合訊號；學習率太大反而可能連訓練集都無法穩定擬合，不能把兩段症狀視為同一原因。",
        "D": "死亡 ReLU 是神經元長期落在 ReLU 負半軸、輸出與梯度皆為零；大更新有時可增加風險，但它不是題幹所見整體 loss 震盪的最直接通用解釋。",
    },
    "trap": "本題同時放了兩個症狀：第 15 epoch 後的 train／validation 分岔是過擬合；調高學習率後的 training loss 震盪才是步幅過大的結果。",
    "references": [
        exam_ref(8),
        ref("Dive into Deep Learning－Learning Rate", "https://d2l.ai/chapter_optimization/gd.html", "學習率過小造成進展慢，過大可能越過最佳點並使最佳化發散"),
    ],
}

DRAFTS[9] = {
    "summary": "正確答案是 A。Adam 同時使用梯度的一階矩估計形成動量，並以二階矩估計為各參數調整有效步長，因此能減少震盪並加快訓練。",
    "concept": (
        "Adam（Adaptive Moment Estimation）維護梯度的一階矩與未中心化二階矩指數移動平均，並對初始化偏差作校正。"
        "一階矩平滑短期梯度方向，作用類似 momentum；二階矩依近期梯度平方尺度正規化更新，讓不同參數具有自適應有效學習率。"
        "兩者常使含噪或不同尺度梯度的訓練較穩定，但 Adam 不保證永遠優於 SGD，仍需設定基礎學習率、正則化並驗證泛化。"
    ),
    "answerReason": "A 同時指出 Adam 名稱與演算法的兩個核心：moment estimate 平滑方向，以及逐參數 adaptive step size；其他選項都不是 Adam 本身必然執行的機制。",
    "optionAnalysis": {
        "A": "正確。Adam 以一階矩估計累積梯度方向、以二階矩估計縮放各參數更新，再進行偏差校正，因此能在不同梯度尺度下調整步長並降低震盪。",
        "B": "Adam 並非強制每個參數使用相同有效學習率；恰恰相反，它以各參數各自的二階矩估計縮放更新，基礎 learning rate 相同但實際步長可不同。",
        "C": "Batch Normalization 是網路層，利用 mini-batch 統計量正規化中間 activation；Adam 是 optimizer，不會自動插入批次正規化或重新分布輸入資料。",
        "D": "梯度裁剪將梯度值或範數限制在門檻內，需另外設定與呼叫；Adam 的二階矩縮放可緩和大梯度更新，但不等於把梯度裁成固定範圍。",
    },
    "trap": "Adam 的 adaptive learning rate 來自梯度矩估計，不是 BatchNorm，也不是 gradient clipping。這些技術可以同時使用，但作用層次不同。",
    "references": [
        exam_ref(9),
        ref("Adam: A Method for Stochastic Optimization", "https://arxiv.org/abs/1412.6980", "原始論文第 2 節：一階、二階矩估計、偏差校正與逐參數更新公式"),
    ],
}

DRAFTS[10] = {
    "summary": "正確答案是 A。隔日使用分鐘數是連續值迴歸，可用 MSE；隔日是否流失是二元分類，應以二元交叉熵衡量標籤與預測機率。",
    "concept": (
        "損失函數要先依目標變數與任務決定。使用時長以分鐘表示，是連續數值預測，MSE 會衡量預測分鐘數與實際分鐘數的平方差；"
        "流失標籤只有是／否，是 Bernoulli 二元分類，模型常輸出流失機率並用 Binary Cross-Entropy（log loss）訓練。"
        "『輸出具有不確定性』不是選交叉熵的充分理由；關鍵是要預測連續量，還是類別機率。"
    ),
    "answerReason": "第一個輸出是分鐘數，對應迴歸誤差；第二個輸出是二元標籤，對應二元機率的交叉熵。A 唯一把兩種任務與常用損失正確配對。",
    "optionAnalysis": {
        "A": "正確。MSE 適合衡量連續分鐘數的數值差；Binary Cross-Entropy 對流失與否的 0／1 標籤及預測機率計算對數損失，與二元分類輸出相符。",
        "B": "它把兩種損失對調：一般交叉熵用於類別機率，不直接衡量分鐘差；MSE 雖可數值上套到 0／1，但不如二元交叉熵符合 Bernoulli 機率模型。",
        "C": "Hinge loss 常用於最大間隔分類，不適合直接預測連續使用分鐘；MAE 是連續值迴歸損失，也不是二元機率分類的標準選擇。",
        "D": "交叉熵衡量類別機率分布，不是因為所有預測都有不確定性就能通用；連續時長若要做機率建模也需指定適當連續分布，不能直接套一般分類交叉熵。",
    },
    "trap": "先看標籤型態：連續數值是 regression，類別是 classification。MSE 與 BCE 的分界不是『有沒有不確定性』，而是輸出空間與機率模型。",
    "references": [
        exam_ref(10),
        ref("TensorFlow Keras－Regression losses", "https://www.tensorflow.org/api_docs/python/tf/keras/losses/MeanSquaredError", "MeanSquaredError 對真實值與預測值的平方差取平均"),
        ref("TensorFlow Keras－BinaryCrossentropy", "https://www.tensorflow.org/api_docs/python/tf/keras/losses/BinaryCrossentropy", "Binary cross-entropy 用於 0／1 二元分類任務"),
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
