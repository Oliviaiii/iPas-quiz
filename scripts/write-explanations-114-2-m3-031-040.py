"""Write explanation drafts for 114-2 intermediate subject three, Q31-Q40.

The script validates official answers, refuses to overwrite reviewed content,
and leaves every generated explanation in ``draft`` status.

Usage::

    python scripts/write-explanations-114-2-m3-031-040.py
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
    "bf93f438f7be48d295c1b40a34d79f3d/"
    "114年第二梯次中級AI應用規劃師第三科機器學習技術與應用"
    "(當次試題公告114_20251226000650.pdf"
)
KERAS_EARLY_STOPPING = "https://keras.io/api/callbacks/early_stopping/"
SKLEARN_LASSO = (
    "https://scikit-learn.org/stable/modules/generated/"
    "sklearn.linear_model.Lasso.html"
)
SKLEARN_COSINE = (
    "https://scikit-learn.org/stable/modules/generated/"
    "sklearn.metrics.pairwise.cosine_similarity.html"
)
SKLEARN_STRATIFIED = (
    "https://scikit-learn.org/stable/modules/generated/"
    "sklearn.model_selection.StratifiedKFold.html"
)
SKLEARN_LOO = (
    "https://scikit-learn.org/stable/modules/generated/"
    "sklearn.model_selection.LeaveOneOut.html"
)
SKLEARN_PCA = (
    "https://scikit-learn.org/stable/modules/generated/"
    "sklearn.decomposition.PCA.html"
)
HOMOMORPHIC_INTRO = "https://homomorphicencryption.org/introduction/"
NIST_GCM = "https://csrc.nist.gov/pubs/sp/800/38/d/final"
SKLEARN_MSE = (
    "https://scikit-learn.org/stable/modules/generated/"
    "sklearn.metrics.mean_squared_error.html"
)
PYTORCH_DROPOUT = "https://docs.pytorch.org/docs/stable/generated/torch.nn.Dropout.html"
NUMPY_DOT = "https://numpy.org/doc/stable/reference/generated/numpy.dot.html"
NUMPY_INV = "https://numpy.org/doc/stable/reference/generated/numpy.linalg.inv.html"
NUMPY_EIG = "https://numpy.org/doc/stable/reference/generated/numpy.linalg.eig.html"

DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


def exam_ref(number: int) -> dict:
    return ref(
        "114 年第二次中級 AI 應用規劃師－機器學習技術與應用公告試題",
        EXAM_PDF,
        f"第 {number} 題題幹、選項、附圖與官方答案",
    )


EXPECTED_ANSWER = {
    31: "B", 32: "D", 33: "B", 34: "D", 35: "A",
    36: "D", 37: "B", 38: "B", 39: "C", 40: "C",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[31] = {
    "summary": "正確答案是 B。早停應監控驗證損失，並以適度 patience 容許短期波動，連續多輪未改善才停止。",
    "concept": (
        "Early Stopping 是用未參與權重更新的驗證指標判斷泛化能力，而不是追求訓練損失最低。"
        "`patience` 表示指標停止改善後仍允許訓練的輪數，可避免季節性或隨機噪音造成單輪反彈就"
        "誤停；通常還會保存或還原驗證表現最佳輪次的權重。測試集應保留到模型選擇完成後，否則"
        "反覆據其決策會讓最終評估產生資訊洩漏。"
    ),
    "answerReason": (
        "題目已指出驗證損失在第 80 輪後週期起伏，單看一輪無法判斷是否真正惡化。B 同時選對"
        "監控資料（驗證集）並加入耐心值，能跨過暫時波動，只有連續多輪沒有更佳驗證損失才停止，"
        "最符合泛化目標。"
    ),
    "optionAnalysis": {
        "A": "訓練損失持續降低可能正是模型愈來愈貼合訓練噪音；其最低點不能代表未見資料的表現最佳。",
        "B": "正確。驗證損失反映泛化，patience 可容忍題幹所述的週期波動，避免因單輪噪音過早停止。",
        "C": "測試集應用於模型與超參數固定後的最終評估；拿它控制停止輪次等同用測試資訊選模型。",
        "D": "合併全部資料便失去獨立驗證訊號；訓練至收斂也不能辨識何時已開始過擬合。",
    },
    "trap": "不要把訓練損失最低誤認為泛化最佳，也不要把測試集當成可反覆查看的驗證集。題幹強調波動時，關鍵字是 patience。",
    "references": [
        exam_ref(31),
        ref(
            "Keras API－EarlyStopping",
            KERAS_EARLY_STOPPING,
            "monitor、patience 與 restore_best_weights 參數定義",
        ),
    ],
}

DRAFTS[32] = {
    "summary": "正確答案是 D。L1 正則化會把部分係數壓到恰為 0，因而同時抑制複雜度並產生稀疏特徵選擇。",
    "concept": (
        "Lasso 在線性模型的損失函數加入 L1 範數懲罰。當懲罰強度提高時，較不重要特徵的係數"
        "可縮成 0，留下稀疏模型；Ridge 的 L2 懲罰通常只把係數向 0 縮小而不會自動剔除。高度相關"
        "特徵下，Lasso 可能從一組替代特徵中選出部分代表，因此選擇結果仍應用交叉驗證與穩定性"
        "分析確認。"
    ),
    "answerReason": (
        "需求不只要減少過擬合，還明確要求『自動篩選』代表特徵。D 所述 L1 會讓部分係數成為 0，"
        "可直接排除有限貢獻特徵；這是其他只控制輪數或保留全部係數的方法沒有的性質。"
    ),
    "optionAnalysis": {
        "A": "早停控制最佳化輪數，但本身不會把不重要輸入特徵的係數系統性設為 0，不能直接完成特徵篩選。",
        "B": "先人工移除共線特徵再用 Ridge 可改善穩定性，但不是模型自動產生稀疏選擇，且移除規則另需決定。",
        "C": "Ridge 能縮小所有權重並降低變異，通常仍保留每個特徵，與題目要求的自動篩選不符。",
        "D": "正確。L1 懲罰可使某些係數恰為 0，兼具正則化與嵌入式特徵選擇效果。",
    },
    "trap": "L1 與 L2 都能正則化，但『係數縮為 0／稀疏』才是 L1 的辨識點；高度相關時也不代表被選中的特徵必然是唯一因果因素。",
    "references": [
        exam_ref(32),
        ref(
            "scikit-learn API－Lasso",
            SKLEARN_LASSO,
            "L1 正則化目標函數與 sparse coefficients 說明",
        ),
    ],
}

DRAFTS[33] = {
    "summary": "正確答案是 B。n 位客戶彼此逐一比較約需 n(n−1)/2 次配對，主導項為 n²，因此是 O(n²)。",
    "concept": (
        "若每對無序客戶只比較一次，配對數為組合數 C(n,2)=n(n−1)/2；若方向也分開算，則是"
        "n(n−1)。兩者省略常數與低階項後皆為 O(n²)。同樣地，全成對相似度函式對 n 筆輸入"
        "會形成 n×n 的相似度矩陣；單次相似度若另與特徵維度 d 成正比，完整成本可寫成 O(n²d)，"
        "但本題只問相對於客戶數 n 的成長。"
    ),
    "answerReason": (
        "每位客戶都要與其餘客戶比較，隨 n 增加一倍，配對數約增加四倍。n(n−1)/2 的最高次項"
        "是 n²，Big-O 不計 1/2 常數與 −n 低階項，所以選 B。"
    ),
    "optionAnalysis": {
        "A": "O(n) 只適合每位客戶做固定次數工作的單次掃描；此處每位還要對照其餘約 n 位。",
        "B": "正確。所有客戶的不重複配對數為 n(n−1)/2，忽略常數及低階項後是 O(n²)，執行時間隨資料量平方成長。",
        "C": "O(1) 表示工作量不隨客戶數變化，顯然無法涵蓋新增客戶帶來的大量新配對。",
        "D": "O(log n) 常見於每步縮小固定比例的搜尋；全配對沒有這種縮減，而要枚舉各對。",
    },
    "trap": "去除重複對稱配對只把 n² 次降成約 n²/2 次，改變的是常數，不會把複雜度變成 O(n)。",
    "references": [
        exam_ref(33),
        ref(
            "scikit-learn API－cosine_similarity",
            SKLEARN_COSINE,
            "成對相似度輸出形狀為 (n_samples_X, n_samples_Y)",
        ),
    ],
}

DRAFTS[34] = {
    "summary": "正確答案是 D。依官方命題意圖，分層要維持類別代表性，留一法則讓每輪以 149 筆訓練，兼顧稀少資料利用率。",
    "concept": (
        "標準 Leave-One-Out（LOO）以每一筆樣本各當一次測試資料，等同 n folds，每折測試集只有"
        "一筆；StratifiedKFold 則讓每一折盡量保留原始類別比例。兩者目的不同：前者最大化每輪"
        "訓練量，後者降低不平衡資料在各折分布差異。然而單筆驗證折不可能同時包含正、負類，"
        "因此『Stratified Leave-One-Out』不是 scikit-learn 的標準 splitter 名稱，也無法在每個"
        "單筆驗證折內維持約 8% 的陽性比例。"
    ),
    "answerReason": (
        "在四個選項中，官方以 D 表達『分層』與『留一』的兩項需求：分層對應類別不平衡，留一"
        "對應有限樣本下每輪幾乎使用全部資料訓練。因此本站依公告答案選 D；但若按標準交叉驗證"
        "定義實作，應改用可行的 StratifiedKFold（或 repeated stratified CV），而不是宣稱單筆"
        "驗證折仍能維持類別比例。"
    ),
    "optionAnalysis": {
        "A": "一般 5-Fold 未明說分層，極少數陽性可能分配不均；若改成 Stratified 5-Fold 才能直接照顧比例。",
        "B": "LOO 每輪保留最多訓練資料，但單筆驗證樣本只能屬於一類，沒有每折類別比例一致的性質。",
        "C": "隨機切分若不加分層約束，可能讓部分驗證集沒有或只有極少陽性，評估不穩定。",
        "D": "依官方答案與命題意圖為正確：名稱意在結合分層的類別代表性與留一的高資料利用率；惟其標準性與可實作定義有疑義。",
    },
    "trap": "應試時可由『比例一致性＝分層』『資料利用率＝留一』鎖定官方 D；實務上切勿忽略每折只有一筆便不可能呈現兩類比例的矛盾。",
    "editorialNote": (
        "官方答案為 D，但『Stratified Leave-One-Out Cross Validation』不是 scikit-learn 所列的"
        "標準切分器；LOO 每個驗證折僅一筆，無法在單折內維持正負類比例。實務建議依陽性樣本數"
        "選擇 StratifiedKFold 或 repeated stratified CV，並報告適合不平衡分類的指標。本站依"
        "官方答案撰寫應試解析，待命題單位或人工審校確認術語。"
    ),
    "references": [
        exam_ref(34),
        ref(
            "scikit-learn API－StratifiedKFold",
            SKLEARN_STRATIFIED,
            "各 fold 保留各類別樣本比例的定義",
        ),
        ref(
            "scikit-learn API－LeaveOneOut",
            SKLEARN_LOO,
            "每次以一筆樣本作測試、n 筆資料形成 n 個 splits 的定義",
        ),
    ],
}

DRAFTS[35] = {
    "summary": "正確答案是 A。總特徵值為 10，前兩主成分解釋 (6+3)/10=90%，已超過 80% 門檻。",
    "concept": (
        "PCA 中某主成分的 explained variance ratio 是其特徵值除以所有保留候選特徵值總和。"
        "本題總變異為 6+3+1=10，所以三者比例依序是 60%、30%、10%；累積解釋率為 60%、90%、"
        "100%。若規則是保留至少 80%，應選使累積比例首次達標的前兩個主成分。"
    ),
    "answerReason": (
        "一個主成分只有 6/10=60%，未達 80%；加入第二個後為 9/10=90%，已達標，第三個僅再提供"
        "10%。因此可依題設由三維降到二維並保留 90% 總變異，A 的計算與結論均正確。"
    ),
    "optionAnalysis": {
        "A": "正確。前兩主成分的累積解釋率是 90%，超過至少 80% 的保留標準。",
        "B": "第一主成分只有 60%，未達題設門檻；60% 也不能單獨證明資料呈線性或保證一維能避免過擬合。",
        "C": "第二主成分的 30% 已被保留；是否捨棄第三主成分應看其 10% 與既定門檻，而非誤把第二主成分當作被捨棄。",
        "D": "6、3、1 的相對差距明顯，變異並不均衡；前兩者已涵蓋九成，正提供合理降維依據。",
    },
    "trap": "先算總和再算『累積』比例；不要把單一主成分比例、線性關係與是否過擬合混為一談。",
    "references": [
        exam_ref(35),
        ref(
            "scikit-learn API－PCA",
            SKLEARN_PCA,
            "explained_variance_ 與 explained_variance_ratio_ 定義",
        ),
    ],
}

DRAFTS[36] = {
    "summary": "正確答案是 D。同態加密允許直接對密文運算，解密運算結果後可得到與明文相應運算一致的結果。",
    "concept": (
        "一般加密通常要先解密才能計算；同態加密的核心是讓未持有祕密金鑰的計算方也能在密文上"
        "執行受支援的加法、乘法等運算，輸出仍是密文，再由有權者解密。實際機器學習會受方案支援"
        "的運算、近似誤差、密文噪音與效能成本限制，並非任意既有訓練程式加密後即可原樣執行。"
    ),
    "answerReason": (
        "題目要求避免資料在傳輸及平台計算時暴露。D 正好描述同態加密的識別特性：平台不需先取得"
        "明文即可進行數值運算。其他選項分別是差分隱私、危險的私鑰交換或壓縮，均非同態性。"
    ),
    "optionAnalysis": {
        "A": "在查詢或模型輸出加入隨機噪音是差分隱私的典型概念，不是密文可計算的同態性。",
        "B": "私鑰不應在各銀行間交換；同態運算的價值之一正是計算方無須持有解密祕密。",
        "C": "壓縮可能是獨立效能技術，但同態加密不以壓縮資料量為核心，而且密文往往比明文更大。",
        "D": "正確。可在加密資料上執行受方案支援的運算，過程無須把客戶原始資料解密給平台。",
    },
    "trap": "看到『加噪音』要想到差分隱私；看到『密文上直接運算』才是同態加密。D 是能力描述，不代表所有模型都能零成本完整訓練。",
    "references": [
        exam_ref(36),
        ref(
            "HomomorphicEncryption.org－Introduction to Homomorphic Encryption",
            HOMOMORPHIC_INTRO,
            "在加密資料上直接計算且不需 secret key 的核心定義",
        ),
    ],
}

DRAFTS[37] = {
    "summary": "正確答案是 B。依官方命題對應，同態加密負責密文運算，非對稱與對稱加密支援金鑰／通道機密性，雜湊用來檢查完整性。",
    "concept": (
        "需求可拆成兩層：資料處理層需讓平台在不解密下運算，對應同態加密；通訊層通常以非對稱"
        "機制完成身分認證或協商金鑰，再以高效率對稱加密保護大量資料。雜湊可產生內容摘要，但"
        "未加金鑰的 hash 本身不能阻止攻擊者竄改後重算摘要，也不能辨識舊封包重放。實務協議應用"
        "AEAD（如 GCM）或 MAC／數位簽章驗證來源與完整性，並加 nonce、序號或時間戳防重放。"
    ),
    "answerReason": (
        "B 是唯一依官方分類同時列出同態加密，以及非對稱、雜湊、對稱三種安全通訊基礎元件的"
        "選項，故依公告答案選 B。它能對應題目想考的密文計算、金鑰交換／認證、完整性摘要與傳輸"
        "機密性；不過要完整達到『未被竄改或重放』仍需採用經認證的協議組合。"
    ),
    "optionAnalysis": {
        "A": "缺少讓平台直接處理密文的同態加密；差分隱私限制個體對輸出的影響，不能取代密文運算。",
        "B": "依官方答案為正確。四項技術涵蓋命題所指的密文計算、非對稱金鑰機制、摘要完整性與對稱通道加密。",
        "C": "雖含同態加密與簽章，但差分隱私不是建立機密通訊或防重放所必需的元件；官方未採此組。",
        "D": "MPC 也是隱私協同計算方法，但此選項缺少明確的非對稱身分／金鑰機制；且堆疊 HE 與 MPC 並非題意要求的通訊配置。",
    },
    "trap": "題庫答案把每項技術做概念配對；工程上則不能把 plain hash 當成完整防竄改或防重放措施，必須看是否有金鑰認證與訊息新鮮度機制。",
    "editorialNote": (
        "官方答案為 B，本站依命題意圖解析。然而 B 僅列『單向雜湊』，未明列 MAC、數位簽章、"
        "AEAD 或 nonce／序號；單純 hash 無法自行驗證來源，也無法防止有效舊封包被重放。因此"
        "『最能完整對應』在嚴格資安語意下仍不充分，實作時應使用經標準化的認證加密與防重放協議。"
    ),
    "references": [
        exam_ref(37),
        ref(
            "HomomorphicEncryption.org－Introduction to Homomorphic Encryption",
            HOMOMORPHIC_INTRO,
            "密文上運算且計算方無須 secret key",
        ),
        ref(
            "NIST SP 800-38D－GCM and GMAC",
            NIST_GCM,
            "authenticated encryption 提供資料機密性與真實性／完整性保證",
        ),
    ],
}

DRAFTS[38] = {
    "summary": "正確答案是 B。附圖先將每個誤差平方，再把平方誤差加總除以樣本數，正是均方誤差 MSE。",
    "concept": (
        "均方誤差定義為 MSE=(1/n)Σ(yᵢ−ŷᵢ)²。平方使正負誤差不會互相抵銷，也會加重較大誤差的"
        "影響。MAE 是平均絕對誤差；RMSE 還要對 MSE 開平方根；R² 則比較殘差平方和與相對於"
        "真值平均數的總平方和，四者公式不能只靠『都是回歸指標』混用。"
    ),
    "answerReason": (
        "已目視核對附圖函式：`(y_true - y_pred) ** 2` 計算逐項平方誤差，`sum(...) / len(y_true)`"
        "再求其平均，完整對應 MSE 公式；程式沒有 `abs`、平方根或 R² 的基準項，所以選 B。"
    ),
    "optionAnalysis": {
        "A": "MAE 應計算 `abs(y_true-y_pred)` 的平均，附圖使用平方而非絕對值。",
        "B": "正確。平方誤差總和除以樣本數就是 mean squared error。",
        "C": "RMSE 是 MSE 再開平方根；附圖回傳前沒有 `sqrt`，因此仍是 MSE。",
        "D": "R² 還需以真值相對平均數的總平方和正規化，通常為 1−SSres/SStot；附圖沒有此步驟。",
    },
    "trap": "看到 `** 2` 不足以直接選 RMSE；一定要檢查最後是否再開平方根。本站已目視確認題圖完整回傳式沒有平方根。",
    "editorialNote": "本站已於 2026-08-12 目視核對第 38 題官方附圖程式碼；內容仍為 AI 輔助詳解初稿，尚待獨立人工複核。",
    "references": [
        exam_ref(38),
        ref(
            "scikit-learn API－mean_squared_error",
            SKLEARN_MSE,
            "均方誤差回歸損失的定義與範例",
        ),
    ],
}

DRAFTS[39] = {
    "summary": "正確答案是 C。附圖於訓練時抽取 Bernoulli mask、遮蔽部分輸入並除以保留率 p，實作的是 inverted Dropout。",
    "concept": (
        "Dropout 訓練時以獨立 Bernoulli 隨機遮罩將部分元素設為 0，降低單元彼此共適應；常見的"
        "inverted dropout 會把留下的元素除以保留機率，使訓練時輸出的期望尺度維持不變，因此"
        "推論時可直接原樣輸出。附圖的 p 是『保留機率』，不同框架 API 有時用 p 表示『丟棄率』，"
        "讀程式時應由 mask 分布與縮放式判斷。"
    ),
    "answerReason": (
        "已目視核對題圖：training=True 時以 `np.random.binomial(1,p,size=x.shape)` 產生 0/1 mask，"
        "回傳 `x*mask/p`；非訓練時回傳 x。隨機置零、只在訓練啟用及保留率補償縮放三項特徵"
        "共同指向 Dropout，故選 C。"
    ),
    "optionAnalysis": {
        "A": "L1 是在目標函數加入權重絕對值懲罰，不會每次 forward 隨機產生 0/1 activation mask。",
        "B": "L2 是在目標函數懲罰權重平方大小，以連續方式縮小權重；它不會在每次 forward 對輸入或神經元輸出做隨機遮蔽。",
        "C": "正確。訓練期 Bernoulli 遮罩加上 1/p 縮放，就是 inverted Dropout。",
        "D": "Batch Normalization 會用批次均值、變異數正規化並學習縮放／位移；附圖沒有統計量計算。",
    },
    "trap": "不要只看到『正則化』就選 L1/L2；隨機 mask 是 Dropout 的關鍵。另注意題圖 p 是 keep probability，與 PyTorch `Dropout(p)` 的 drop probability 命名相反。",
    "editorialNote": "本站已於 2026-08-12 目視核對第 39 題完整官方附圖及 training 分支；內容仍為 AI 輔助詳解初稿。",
    "references": [
        exam_ref(39),
        ref(
            "PyTorch API－Dropout",
            PYTORCH_DROPOUT,
            "訓練時 Bernoulli 隨機置零、縮放及 evaluation identity 的行為",
        ),
    ],
}

DRAFTS[40] = {
    "summary": "正確答案是 C。附圖的 v1·v2=1×4+2×5+3×6=32，`np.dot(v1,v2)` 回傳 NumPy 整數純量。",
    "concept": (
        "對兩個一維陣列，`np.dot` 計算內積；`v1*v2` 則做逐元素乘法。`np.linalg.inv(A)` 求方陣"
        "反矩陣，行列式應用 `np.linalg.det(A)`；`np.linalg.eig(A)` 回傳特徵值與右特徵向量，並不"
        "求反矩陣。題圖用 Python 整數建立 NumPy 陣列，在題目所採常見 64 位環境中其內積純量"
        "型別顯示為 `np.int64`。"
    ),
    "answerReason": (
        "已目視核對附圖：`v1=[1,2,3]`、`v2=[4,5,6]`，所以內積是 4+10+18=32，C 的函式、數值"
        "與題設執行環境型別相符。A、D 把反矩陣／特徵分解函式張冠李戴；B 又把逐元素乘法誤算"
        "成向量相加 `[5,7,9]`。"
    ),
    "optionAnalysis": {
        "A": "`np.linalg.inv(A)` 回傳 A 的反矩陣，不是行列式；行列式應用 `np.linalg.det(A)`。",
        "B": "`v1*v2` 是逐元素相乘，結果為 `[4,10,18]`；`[5,7,9]` 其實是 `v1+v2`。",
        "C": "正確。一維陣列的 `np.dot` 是內積，計算結果為 32；題設常見 NumPy 環境顯示為 `np.int64(32)`。",
        "D": "`np.linalg.eig(A)` 回傳特徵值陣列及特徵向量矩陣的 tuple，不會回傳 A 的反矩陣。",
    },
    "trap": "分清 `*` 的逐元素運算與 `dot` 的一維向量內積，也要分清 inv、det、eig 三個線性代數 API；型別名稱則可能受平台與輸入 dtype 影響。",
    "editorialNote": (
        "本站已於 2026-08-12 目視核對第 40 題完整官方附圖。C 的數學結果 32 不受平台影響；"
        "`np.int64` 顯示依 NumPy／平台與輸入 dtype 而定，常見 64 位環境符合題目敘述。內容仍為"
        "AI 輔助詳解初稿，尚待獨立人工複核。"
    ),
    "references": [
        exam_ref(40),
        ref("NumPy API－numpy.dot", NUMPY_DOT, "兩個一維陣列時為向量內積"),
        ref("NumPy API－numpy.linalg.inv", NUMPY_INV, "計算方陣反矩陣"),
        ref("NumPy API－numpy.linalg.eig", NUMPY_EIG, "回傳特徵值與右特徵向量"),
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
