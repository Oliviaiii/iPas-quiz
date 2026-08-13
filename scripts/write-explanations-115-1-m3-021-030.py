"""Write draft explanations for 115-1 intermediate subject three, Q21-Q30.

The script verifies official answers, refuses to overwrite reviewed work, and
keeps every generated explanation in ``draft`` for independent review.

Usage::

    python scripts/write-explanations-115-1-m3-021-030.py
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
    "bf93f438f7be48d295c1b40a34d79f3d/115年第一次中級AI應用規劃師_"
    "第三科_機器學習技術與應用_公告試題_20260615003417.pdf"
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
    21: "D", 22: "C", 23: "D", 24: "D", 25: "A",
    26: "D", 27: "C", 28: "B", 29: "B", 30: "B",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[21] = {
    "summary": "正確答案是 D。把既有模型的 FP32 權重直接轉成 INT8，以縮小儲存量並加速推論，屬於不重新訓練的模型量化，具體可稱訓練後量化。",
    "concept": (
        "量化（quantization）以較低位元數表示權重或啟用值，例如由 32-bit 浮點轉為 8-bit 整數，"
        "藉此降低模型記憶體、傳輸與部分硬體上的運算成本。若完成訓練後才校正或直接轉換，稱"
        "post-training quantization；若訓練時模擬量化誤差，則是 quantization-aware training。位元"
        "縮減會引入捨入與飽和誤差，實作後仍須量測準確度、延遲與裝置算子支援。"
    ),
    "answerReason": "題幹的決定性線索是 FP32 轉 INT8，且不重新訓練；這正是訓練後量化。蒸餾要訓練學生模型，剪枝移除權重或結構，張量分解則以低秩因子近似原張量，都不是改變數值表示精度。",
    "optionAnalysis": {
        "A": "知識蒸餾以教師模型的輸出或中間表徵監督較小學生模型，通常需要新的訓練流程；題幹沒有學生模型，也明示不重新訓練。",
        "B": "剪枝將部分權重設為零或移除通道、神經元，以增加稀疏性或縮小結構；它改的是保留哪些參數，不是把每個 FP32 權重改用 INT8 表示。",
        "C": "張量分解以低秩矩陣或多個小張量近似大型權重張量，降低參數或計算；題述沒有做秩分解，只降低每個數值的位元精度。",
        "D": "正確。FP32 權重轉為 INT8 是典型量化；因轉換發生在預訓練模型之後且不重訓，更精確地屬於 post-training quantization。",
    },
    "trap": "模型壓縮方法都可能縮小體積，但辨識動作即可：降位元是量化、設零或刪結構是剪枝、訓練小模型模仿大模型是蒸餾、低秩近似是分解。",
    "editorialNote": "題目只寫權重由 FP32 轉 INT8，因此解析不宣稱啟用值也必然量化；實際加速幅度取決於行動裝置硬體、算子覆蓋率與量化方案。",
    "references": [
        exam_ref(21),
        ref("PyTorch－Quantization Recipe", "https://docs.pytorch.org/tutorials/recipes/quantization.html", "Dynamic quantization 將模型權重由 32-bit 浮點轉為 8-bit 整數的範例"),
        ref("PyTorch－INT8 Quantization for x86 CPU", "https://pytorch.org/blog/int8-quantization/", "FP32 至 INT8 量化對推論速度與記憶體需求的影響"),
    ],
}

DRAFTS[22] = {
    "summary": "正確答案是 C。混合搜尋同時利用向量的語意相近性與 BM25 的字詞精確匹配，再由 RRF 依排名融合，可直接補足單一向量檢索的盲點。",
    "concept": (
        "向量搜尋擅長同義改寫與概念相近，但可能漏掉產品代碼、法條編號、專有名詞等精確 token；"
        "BM25 依詞項出現與稀有程度排序，擅長字面匹配但不一定理解改寫。Hybrid search 平行取得"
        "兩份候選，再以 Reciprocal Rank Fusion 對每份清單中的名次給分並加總，不需直接比較尺度"
        "不同的原始分數。因此它能直接改善候選召回與排序的互補性。"
    ),
    "answerReason": "題目已定位為向量語意匹配不準，C 引入獨立的 BM25 訊號並融合兩種排序，是最直接且完整的檢索改善。縮小 chunk 或調 threshold 可能有幫助，但只調整單一向量流程；隨機洗牌更會破壞相關性排序。",
    "optionAnalysis": {
        "A": "縮小 chunk 可讓片段更聚焦，但也可能切斷必要上下文並增加候選數；它不會修正 embedding 對關鍵字、編號或領域詞彙匹配不足的根本限制。",
        "B": "提高相似度閾值能刪除低分結果，改善 precision，卻不能找回向量搜尋原本漏掉的相關文件；閾值過高還可能降低 recall。",
        "C": "正確。向量檢索補語意、BM25 補字面精確匹配，RRF 依兩份排名融合；在企業術語、錯誤碼或法條與自然語意並存時特別有用。",
        "D": "Shuffle 不會新增相關文件或提高相似度，只會打亂已計算的排序；處理位置偏誤應在 reranking、提示編排或生成評估階段設計，而不是隨機破壞檢索品質。",
    },
    "trap": "Threshold 只能過濾已有候選，不能補回漏檢；chunk size 影響索引單位，也不保證更小更好。題目明示向量匹配不足時，加入互補的詞彙檢索最直接。",
    "references": [
        exam_ref(22),
        ref("Azure AI Search－Hybrid search overview", "https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview", "混合查詢平行執行全文與向量搜尋並以 RRF 合併結果"),
        ref("Azure AI Search－RRF ranking", "https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking", "RRF 依多個排名清單的 reciprocal rank 合併分數"),
    ],
}

DRAFTS[23] = {
    "summary": "正確答案是 D。原始 BERT 是雙向編碼器與遮罩語言模型，沒有 GPT-2 那種依左側前文逐 token 自回歸生成後文的解碼機制，因此不適合直接做合約續寫。",
    "concept": (
        "BERT 預訓練時同時利用被遮罩 token 左右兩側的上下文，主要產生語境表徵，適合分類、"
        "抽取與理解任務；它不是原生左到右生成器。GPT-2 則以 causal language modeling 學習"
        "P(x_t|x_<t)，推論時把已生成 token 接回輸入，逐步產生下一 token。要讓 BERT 參與生成，"
        "通常需另接自回歸 decoder 或採 encoder-decoder 架構，不能只靠增加微調資料改變注意力遮罩與架構。"
    ),
    "answerReason": "任務要求以合約前半段作條件、連續生成後半段。D 指出 BERT 缺少原生自回歸續寫能力，是架構與預訓練目標的不匹配；法律知識、分詞與模型大小都可能影響品質，但無法解釋為何 GPT-2 對續寫更合適。",
    "optionAnalysis": {
        "A": "領域知識不足可用法律語料持續預訓練或微調改善，GPT-2 也不天然保證法律知識；它不是 BERT 無法有效續寫的最主要架構原因。",
        "B": "分詞會影響法律術語的切分與序列長度，但 BERT 與 GPT 系模型都使用子詞切分；即使換 tokenizer，也不會自動讓雙向 encoder 成為左到右 decoder。",
        "C": "模型容量會影響品質，但模型較小不等於不能生成；題目關鍵是 BERT 的預訓練目標與解碼形式，而非單純參數量比較。",
        "D": "正確。GPT-2 以 causal mask 預測下一 token，天然能以前文為 prefix 反覆續寫；原始 BERT 的 masked-token encoder 沒有這套自回歸生成流程。",
    },
    "trap": "『理解模型』不是完全不能參與生成，而是原始 BERT 缺少自回歸 decoder。若加入 decoder 或改成 BART、T5 等 seq2seq 架構，便是不同模型設計。",
    "editorialNote": "本站將題目中的 BERT 解讀為原始 encoder-only BERT，而非以 BERT 初始化 encoder-decoder 的衍生架構；後者可執行生成，但已超出選項語境。",
    "references": [
        exam_ref(23),
        ref("Devlin et al.－BERT", "https://aclanthology.org/N19-1423/", "BERT 的雙向 Transformer encoder 與 masked language model 預訓練目標"),
        ref("Radford et al.－Language Models are Unsupervised Multitask Learners", "https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf", "GPT-2 使用前文 token 預測下一 token 的自回歸語言模型"),
    ],
}

DRAFTS[24] = {
    "summary": "正確答案是 D。One-Hot 對約 3,000 個類別各建立一個二元欄位，輸出維度會隨類別數近似線性增加，最容易造成高維稀疏矩陣。",
    "concept": (
        "One-hot encoding 對每個類別配置獨立指示欄，因此一個含 K 個類別的特徵通常展開為 K 個"
        "輸出欄位；高基數會增加記憶體、計算與模型複雜度，俗稱維度爆炸。稀疏矩陣能節省大量零值"
        "的儲存，但沒有消除特徵空間維度。Target encoding 以目標統計壓成少數欄，label encoding"
        "只輸出一欄整數，embedding 則把類別映射到固定的低維稠密向量。"
    ),
    "answerReason": "商品項目約 3,000 類且互相獨立，D 會建立約 3,000 個 dummy columns，是四種方法中輸出維度增長最直接者。其餘方法分別維持單一數值、固定統計欄或可設定的 embedding 維度。",
    "optionAnalysis": {
        "A": "Target encoding 常將類別替換為該類目標平均等少數統計量，輸出維度低；其主要風險是目標洩漏、稀有類估計不穩與過擬合，而不是 one-hot 式欄位爆炸。",
        "B": "Label encoding 每個類別映射成一個整數，仍只有一個輸出欄；它避免維度膨脹，但若類別無序，數字大小可能被模型誤解為次序或距離。",
        "C": "Embedding 為每類學習固定長度向量；雖然 embedding table 的參數量隨類別數增加，單筆樣本輸出的特徵維度仍由 embedding dimension 控制。",
        "D": "正確。OneHotEncoder 為每個唯一商品類別建立一個二元特徵，約 3,000 類便形成約 3,000 維的稀疏表示，最符合題目所稱維度爆炸。",
    },
    "trap": "稀疏儲存降低記憶體，不等於降低維度；embedding table 參數也會隨類別數增加，但題目問的是編碼後特徵維度，答案仍是 one-hot。",
    "references": [
        exam_ref(24),
        ref("scikit-learn－OneHotEncoder", "https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html", "每個類別建立一個 one-of-K 二元欄位並可輸出稀疏矩陣"),
        ref("scikit-learn－TargetEncoder", "https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.TargetEncoder.html", "以目標條件平均編碼類別並使用交叉擬合降低洩漏"),
    ],
}

DRAFTS[25] = {
    "summary": "正確答案是 A。距離的嚴重右偏可因 Log 壓縮長尾而改善關係；若屋齡與房價原本近似線性，Log 屋齡會彎曲該關係，反而增加模型偏差。",
    "concept": (
        "Log 是單調的非線性轉換，會強烈拉開靠近零的差異、壓縮大值間距，常用於正值且右偏、"
        "乘法關係或邊際效果遞減的變數。它不是每個連續特徵都必須採用的標準化方法。特徵工程應"
        "依該特徵與目標的關係、模型假設與交叉驗證決定；不同特徵可以採不同轉換，之後若模型"
        "對尺度敏感，再另做 StandardScaler。含零或負值時也不能直接套自然對數。"
    ),
    "answerReason": "距離右偏且 Log 後改善，代表壓縮長尾或線性化關係有益；屋齡若原本與房價呈線性，套 Log 會把等量屋齡差異變成不等距，破壞線性模型可直接利用的結構。因此 A 是最符合兩特徵結果不同的解釋。",
    "optionAnalysis": {
        "A": "正確。若每增加一年對房價的影響近似固定，原始屋齡已符合線性斜率；改成 log(age) 會強調低屋齡、壓縮高屋齡，使關係彎曲並可能降低預測。",
        "B": "Log 通常壓縮大值，但不是把所有資料的變異數按同一比例縮小，也不必然失去鑑別力；題目已證明它對右偏距離反而提升模型。",
        "C": "有公尺、年等單位並不禁止 Log；關鍵是變數正值、分布與關係形式。Box-Cox 本身也是帶參數的冪轉換，lambda=0 時即對應對數。",
        "D": "不同特徵可使用不同轉換；梯度穩定可在轉換後另行縮放。強迫屋齡與距離採同一函數，反而忽略兩者分布與房價關係不同。",
    },
    "trap": "分布右偏只是考慮 Log 的線索，不是命令。應看轉換是否使特徵與目標更符合模型假設；Log 也不同於 StandardScaler，前者改變關係形狀，後者主要改尺度。",
    "editorialNote": "題目未指明屋齡是否含 0；若有 0，直接 log(age) 尚有未定義問題，常需 log1p 或其他轉換。本題依官方答案 A 的『原關係近似線性』條件判定。",
    "references": [
        exam_ref(25),
        ref("SciPy－boxcox", "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.boxcox.html", "Box-Cox 僅適用正值資料，lambda=0 時為 log(x)"),
        ref("scikit-learn－PowerTransformer", "https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PowerTransformer.html", "冪轉換用於使資料更接近常態並穩定變異，轉換參數由資料估計"),
    ],
}

DRAFTS[26] = {
    "summary": "正確答案是 D。滑動窗口把 t-1、t-2 等過去觀測排列成目前樣本的輸入欄位，本質上是在建立滯後特徵，讓模型利用時間依賴預測未來。",
    "concept": (
        "一般監督式模型每列需要固定長度特徵。時間序列滑動窗口以過去 L 個時間點形成 X_t，"
        "再以當期或未來值形成 y_t，例如 [sales(t-3), sales(t-2), sales(t-1)] 預測 sales(t)。這些"
        "欄位稱 lags。窗口長度決定可見歷史範圍，步長決定相鄰樣本重疊程度；建立後仍要按時間"
        "切分，避免未來值或以全資料計算的 rolling statistics 洩漏到訓練。"
    ),
    "answerReason": "題幹明說把過去多個時間點組合為模型輸入，正是將歷史觀測轉成 lag features，所以選 D。重疊窗口可能增加訓練樣本，但主要目的不是創造新標籤；它也不會自動去噪或降維，反而通常增加欄位。",
    "optionAnalysis": {
        "A": "窗口重疊確實可形成更多監督樣本，但這些不是經隨機變形產生的新資料；核心功能是把歷史順序顯式編碼，不能概括為一般資料增強。",
        "B": "把多點輸入模型不等於濾除雜訊；若要去噪需移動平均、濾波或其他平滑方法。窗口甚至會把每個含雜訊的歷史值都保留下來。",
        "C": "若窗口含 L 個過去值，單一序列通常展開成 L 個特徵，維度反而增加；降維需要 PCA、特徵選擇或壓縮表示等額外步驟。",
        "D": "正確。每個窗口將過去觀測對齊到目前樣本，建立 lag-1、lag-2 等滯後特徵，使迴歸或分類模型能學習自相關與時間型態。",
    },
    "trap": "『窗口』有時用於平滑，有時用於造 lag；本題明確說把過去多點組成模型輸入，因此是 supervised lag features，而不是把窗口取平均來去噪。",
    "references": [
        exam_ref(26),
        ref("scikit-learn－Lagged features for time series forecasting", "https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html", "以 shift 建立過去觀測的 lagged features 並預測下一時間點"),
    ],
}

DRAFTS[27] = {
    "summary": "正確答案是 C。Rolling Window／Time Series Split 維持時間先後，逐次把驗證區間向前推進，並可限制訓練集只保留最近窗口，以模擬用最新資料預測未來。",
    "concept": (
        "時間序列驗證不能隨機把未來資料放入訓練、過去資料放入驗證。Expanding window 逐次累積"
        "所有歷史；rolling window 則固定或限制訓練長度，隨時間移除最舊資料並加入較新資料。題目"
        "要求每次基於最新時間區間，應採後者，或用 TimeSeriesSplit 設 max_train_size。這能觀察"
        "模型跨時間的穩定性與概念漂移，但仍需依重訓頻率、季節週期選窗口長度。"
    ),
    "answerReason": "C 同時滿足時間順序與更新訓練區間，能模擬第 52、60、70 週等不同切點的真實部署。一般 K-fold、分層 K-fold 與 LOO 忽略時間先後，可能把較新行為洩漏到較早預測，且不保證只用最近資料。",
    "optionAnalysis": {
        "A": "一般 K-fold 假設樣本可交換，隨機折可能用第 80 週訓練、第 40 週驗證，造成未來資訊洩漏；也不會固定只保留最新時間窗口。",
        "B": "Stratified K-fold 只維持各折類別比例，仍可能打亂時間；銷量預測是連續目標，分層也不是解決模式隨時間改變的核心方法。",
        "C": "正確。驗證集沿時間向前移，訓練集位於其之前；使用固定 max_train_size 時，每折都捨棄過舊週次並以最近窗口訓練，直接符合題目要求。",
        "D": "Leave-One-Out 每次留一筆，其他所有時間點都可進訓練，會讓被留出的早期樣本看到未來資料；計算昂貴且無法模擬連續部署。",
    },
    "trap": "TimeSeriesSplit 預設常是 expanding window；題目特別要求『最新時間區間』，實作時要再設定固定窗口或 max_train_size，才是真正 rolling window。",
    "editorialNote": "官方選項把 Rolling Window Validation 與 Time Series Split 並列，但兩者不完全同義：scikit-learn TimeSeriesSplit 預設累積歷史，需設定 max_train_size 才符合固定長度滾動窗口。",
    "references": [
        exam_ref(27),
        ref("scikit-learn－TimeSeriesSplit", "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html", "依時間順序建立訓練／測試折，並以 max_train_size 限制訓練窗口"),
        ref("scikit-learn－Time-related feature engineering", "https://scikit-learn.org/stable/auto_examples/applications/plot_cyclical_feature_engineering.html#time-based-cross-validation", "時間式交叉驗證避免用未來資料評估過去"),
    ],
}

DRAFTS[28] = {
    "summary": "正確答案是 B。RandomForestRegressor 可透過多棵樹的分裂捕捉非線性與特徵交互作用，並提供整體 feature_importances_，最符合預測連續房價與稽核需求。",
    "concept": (
        "隨機森林迴歸對 bootstrap 樣本訓練多棵決策樹，並在分裂時抽取部分特徵，最後平均樹的"
        "預測以降低單樹變異。樹的分段切分能表示非線性與交互作用，不需先指定函數形狀。整體"
        "重要性可用 impurity-based feature_importances_，但對高基數特徵可能偏誤；稽核時宜再以"
        "獨立驗證集 permutation importance、穩定性與方向性分析補強，重要性不等於因果影響。"
    ),
    "answerReason": "B 是唯一同時對應連續房價、非線性關係與全域重要性輸出的選項。Logistic Regression 是分類器；K-means 加回歸沒有自然提升解釋性的保證；SVR 雖可非線性，但支持向量不是每個原始特徵的全域重要性。",
    "optionAnalysis": {
        "A": "Logistic Regression 預測類別機率，不適用連續成交價；即使改成線性迴歸，單一係數也只能直接描述預先指定的線性效果，無法自然捕捉題述非線性。",
        "B": "正確。RandomForestRegressor 適合連續目標，樹分裂可建立非線性與交互作用，並提供所有資料／所有樹彙總的特徵重要性供整體檢視。",
        "C": "K-means 是無監督分群，分群後各建迴歸會增加流程與分段決策；沒有證據保證提升準確率，也讓整體特徵影響更難統一解釋。",
        "D": "核 SVR 能捕捉非線性，但支持向量是具代表性的訓練樣本，不是原始 50 個特徵的重要性；非線性 kernel 也難直接產生可稽核的全域特徵排名。",
    },
    "trap": "能列 feature importance 不等於完整可解釋或因果。隨機森林符合題目選擇，但稽核應交代 importance 方法、資料切分、相關特徵分攤與重抽樣穩定性。",
    "editorialNote": "題目 B 原文把 Random Forest Regression 斷字成 `Regress ion`，本站保留題目資料而在解析使用正確拼法。Impurity importance 對高基數特徵有偏誤，不能單獨當成稽核結論。",
    "references": [
        exam_ref(28),
        ref("scikit-learn－RandomForestRegressor", "https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html", "多棵迴歸樹平均預測與 feature_importances_ 屬性"),
        ref("scikit-learn－Permutation feature importance", "https://scikit-learn.org/stable/modules/permutation_importance.html", "Permutation importance 的定義，以及 impurity importance 對高基數特徵的偏誤"),
    ],
}

DRAFTS[29] = {
    "summary": "正確答案是 B。只有大量正常資料、沒有已確認故障標籤時，無法訓練一般二元分類器；可先學習正常模式，再把明顯偏離者視為異常，屬非監督或半監督異常偵測。",
    "concept": (
        "異常偵測依訓練資料可分 outlier detection 與 novelty detection。若訓練資料混有未知異常，"
        "可用 Isolation Forest、Local Outlier Factor 等非監督方法找稀少偏離點；若訓練集可信為"
        "正常，可學正常分布或邊界，再把新樣本偏離判為 novelty，常稱 one-class 或半監督異常偵測。"
        "時序振動還需以不重疊設備／時間區間驗證，並由工程師確認告警是否真是故障。"
    ),
    "answerReason": "題幹沒有任何故障標註，卻有大量正常運作資料，因此 B 最符合以正常模式為基準找偏離的設定。監督二元分類需要正負標籤；強化學習處理互動決策；自監督可學表示，但本身不是四項中最直接的任務範疇。",
    "optionAnalysis": {
        "A": "二元分類要有正常與故障兩類標籤供 loss 比較；目前完全沒有已確認故障樣本，無法可靠學得故障類決策邊界或評估故障 recall。",
        "B": "正確。可用正常資料建立基線、密度或 one-class 邊界，將低機率或遠離正常結構的新振動視為異常；若資料可能混有未知故障則採穩健非監督方法。",
        "C": "強化學習需要 agent、環境、動作與 reward，以互動學決策策略；單純從感測時序判斷是否偏離正常，不具這種序列決策回饋設定。",
        "D": "自監督可透過遮罩重建、對比學習等預任務學振動表示，之後協助異常偵測；但它是表示學習訓練方式，不直接等同本題最終的異常偵測任務類型。",
    },
    "trap": "『只有正常標註』常稱 novelty detection 或 one-class／半監督異常偵測；『連正常標籤也沒有、資料混雜』更接近非監督 outlier detection。題目把兩者合併為 B。",
    "editorialNote": "異常不必然等於故障；轉速、負載或感測器更換也可能造成分布偏移。上線前仍需取得部分專家確認事件，校準 threshold、誤報率與實際提前預警價值。",
    "references": [
        exam_ref(29),
        ref("scikit-learn－Novelty and Outlier Detection", "https://scikit-learn.org/stable/modules/outlier_detection.html", "區分 outlier detection、novelty detection，並列出 one-class 與非監督方法"),
        ref("scikit-learn－IsolationForest", "https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html", "以隨機切分隔離樣本並產生異常分數"),
    ],
}

DRAFTS[30] = {
    "summary": "正確答案是 B。訓練 AUC 很高但驗證大幅下降，少數類預測與不同折結果又明顯波動，表示模型對抽樣資料非常敏感，屬高變異問題。",
    "concept": (
        "高變異模型能緊貼訓練樣本，換一批資料後決策函數與表現卻大幅改變，常呈現訓練分數高、"
        "驗證分數低及 cross-validation 各折分散大的現象。少數違約樣本少時，各折包含的案例"
        "數與難度稍變就會使 AUC 波動，進一步放大方差。過擬合是高變異常見的觀察結果；可用更"
        "簡單模型、正則化、更多代表性資料、重複分層交叉驗證與信賴區間診斷改善。"
    ),
    "answerReason": "0.97 對 0.72 的泛化落差支持過度貼合訓練資料，而『少數樣本預測波動極大、不同 K-fold 差異明顯』更直接指向對資料切分敏感的高變異，所以官方選 B。高偏差通常訓練與驗證都差；資料漂移需有時間／來源分布改變證據。",
    "optionAnalysis": {
        "A": "高偏差表示模型太簡單或假設不合，連訓練資料都擬合不好；本題訓練 AUC 0.97 很高，與典型 underfitting 不符。",
        "B": "正確。模型換一個 K-fold 切分就明顯改變結果，且稀少違約案例的預測不穩，都是估計對抽樣擾動敏感、variance 偏高的直接證據。",
        "C": "訓練遠高於驗證確實可描述為過擬合，但它是表現現象；題目另給跨折與少數類波動，意在辨識更具體的高變異來源。四選一依官方答案選 B。",
        "D": "資料漂移指訓練與部署期間的輸入分布或條件關係改變；題目只描述同一資料上的驗證與 K-fold 差異，沒有時間、族群或來源分布改變的比較證據。",
    },
    "trap": "高變異與過擬合高度相關：前者強調換資料就不穩，後者強調訓練好但泛化差。題目同時出現兩者線索時，用 K-fold 波動辨認官方想問的更具體問題。",
    "editorialNote": "官方答案 B，但 C『過擬合』也能合理描述訓練 AUC 0.97、驗證 AUC 0.72 的現象；本站把 B 解讀為其統計機制，C 解讀為外顯結果。人工複核宜保留此選項重疊疑義。另 AUC 的折間差異須搭配各折違約數與信賴區間判讀。",
    "references": [
        exam_ref(30),
        ref("scikit-learn－Underfitting vs. Overfitting", "https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html", "模型複雜度增加後訓練誤差下降而驗證誤差上升的過擬合現象"),
        ref("scikit-learn－Learning curve", "https://scikit-learn.org/stable/modules/learning_curve.html", "以交叉驗證訓練／驗證分數與其變異診斷模型泛化"),
        ref("scikit-learn－StratifiedKFold", "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedKFold.html", "在各折維持類別比例的分層交叉驗證"),
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
