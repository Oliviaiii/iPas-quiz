"""Write draft explanations for 115-1 intermediate subject three, Q11-Q20.

The script verifies official answers, refuses to overwrite reviewed work, and
keeps every generated explanation in ``draft`` for independent review.

Usage::

    python scripts/write-explanations-115-1-m3-011-020.py
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
    "第三科_機器學習技術與應用_公告試題_20260615003428.pdf"
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
    11: "D", 12: "A", 13: "C", 14: "C", 15: "D",
    16: "A", 17: "B", 18: "A", 19: "D", 20: "C",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[11] = {
    "summary": "正確答案是 D。Mini-batch GD 用一批樣本估計梯度，既能降低單樣本梯度雜訊，又能把矩陣運算批次化以提高 GPU 吞吐量。",
    "concept": (
        "全批次梯度下降每次以完整訓練集計算精確梯度，方向穩定但更新頻率低，且大型資料可能"
        "受記憶體與單次計算時間限制。單樣本 SGD 更新很快，卻有高梯度變異，也難以用足 GPU 的"
        "大規模平行運算。Mini-batch 取兩者折衷：批內可用張量核心及向量化計算，提高每秒處理"
        "樣本數；批次平均又比單樣本梯度穩定。批次大小仍需依記憶體、序列長度、通訊與收斂調校。"
    ),
    "answerReason": (
        "題目同時要求梯度穩定與 GPU throughput，D 讓 256～2048 筆樣本共同形成一次更新，能"
        "攤提 GPU kernel 與同步成本，並降低單筆樣本造成的震盪，是四個選項中唯一直接兼顧兩者的策略。"
    ),
    "optionAnalysis": {
        "A": "全批次梯度使用所有樣本，雖能降低抽樣雜訊且題目觀察到 GPU 利用率 100%，但每次更新需 45 秒；高利用率不等於有足夠的參數更新頻率與最佳訓練時間。",
        "B": "單樣本 SGD 每次只花 0.01 秒，卻無法形成足夠大的矩陣運算來有效利用 GPU，且題目已觀察到梯度雜訊使訓練曲線劇烈震盪。",
        "C": "Newton 法要形成或近似 Hessian 並求解二階更新；大型語言模型參數極多，完整 Hessian 的儲存與計算遠超可行範圍，不能以減少更新次數抵銷成本。",
        "D": "正確。小批次把多筆樣本的梯度取平均，較單樣本穩定，並將運算組成 GPU 擅長的批次矩陣乘法；適當大小可在吞吐量、記憶體與泛化間取得平衡。",
    },
    "trap": "GPU utilization 100% 只表示裝置忙碌，不代表整體訓練最有效率。要同時看 samples/sec、每次更新時間、通訊成本與收斂所需步數。",
    "editorialNote": "本站依官方答案 D 判定。題目所列 256～2048 僅為示例，不是所有模型的最佳範圍；實務應依顯存、序列長度、資料平行規模與學習率調整，必要時用 gradient accumulation 形成較大有效批次。",
    "references": [
        exam_ref(11),
        ref(
            "NVIDIA Deep Learning Performance－Mini-batches",
            "https://docs.nvidia.com/deeplearning/performance/dl-performance-fully-connected/index.html#mini-batches",
            "Mini-batch 大小影響矩陣運算尺寸、GPU 平行效率與整體吞吐量",
        ),
        ref(
            "PyTorch－torch.utils.data.DataLoader",
            "https://docs.pytorch.org/docs/stable/data.html#torch.utils.data.DataLoader",
            "以 batch_size 組成訓練批次並支援批次資料載入",
        ),
    ],
}

DRAFTS[12] = {
    "summary": "正確答案是 A。正類僅 1% 時，即使幾乎全部預測正常也能得到接近 99% Accuracy，因此高準確率可能完全掩蓋肺癌陽性的漏診。",
    "concept": (
        "Accuracy=(TP+TN)/全部樣本，會由數量龐大的正常病例主導。若 10,000 人中只有 100 名陽性，"
        "全部預測正常仍有 99% Accuracy，但陽性 recall=0，表示所有肺癌都漏診。醫療篩檢應先依"
        "臨床成本檢查 sensitivity/recall、specificity、precision、混淆矩陣及適當閾值；PR curve"
        "能聚焦稀少正類的召回與誤報取捨，ROC-AUC 亦不應脫離具體工作點單獨解讀。"
    ),
    "answerReason": (
        "題幹的核心是 99% 正常與漏診風險。A 正確指出 Accuracy 沒有告訴醫師 1% 陽性中抓到"
        "多少人；99.1% 甚至可能只比全猜正常的 99% 基準多一點，無法證明具臨床篩檢價值。"
    ),
    "optionAnalysis": {
        "A": "正確。多數類的正確預測可把 Accuracy 拉高，即使少數肺癌幾乎全被漏掉；必須另看陽性 recall、false negative 數量與臨床可接受閾值。",
        "B": "Accuracy 計算所有樣本是否分類正確，邊界樣本若預測正確或錯誤都會納入；缺陷是它只彙總總體正確比例，沒有分別呈現少數類表現。",
        "C": "Accuracy 可用於二元與多類別問題，只是類別不平衡時容易誤導。AUC 不是二元分類的強制替代品，也不能單獨呈現選定閾值下的漏診數。",
        "D": "收斂速度是訓練過程的最佳化議題，Accuracy 是預測結果指標；題目關切的是上線後肺癌陽性的偵測，而不是模型每秒迭代或到達穩定所需時間。",
    },
    "trap": "遇到極端類別比例，先算『全猜多數類』的基準。本題基準已達 99%，所以 99.1% 不應直接被稱為優秀，還要看少數類召回與誤報。",
    "references": [
        exam_ref(12),
        ref(
            "scikit-learn－Classification metrics",
            "https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics",
            "Accuracy、precision、recall、confusion matrix 與分類指標定義",
        ),
        ref(
            "scikit-learn－Precision-Recall",
            "https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html",
            "高度不平衡分類中 precision-recall 用於衡量正類預測成功與漏判／誤報取捨",
        ),
    ],
}

DRAFTS[13] = {
    "summary": "正確答案是 C。L2 weight decay 會懲罰過大的 Embedding 與全連結層權重，限制模型有效複雜度，最直接從正則化角度縮小訓練與驗證落差。",
    "concept": (
        "訓練 F1 遠高於驗證 F1 是典型泛化落差。L2 regularization 在資料損失外加入與權重平方"
        "相關的懲罰，使最佳化不只追求記住訓練樣本，也偏好較小、較平滑的參數。實作上 optimizer"
        "的 weight_decay 常用來達到這個效果；對 Adam 而言，AdamW 將權重衰減與梯度更新解耦。"
        "正則強度過高會欠擬合，因此應以驗證集選擇係數，並可搭配 dropout、早停或更多代表性資料。"
    ),
    "answerReason": (
        "C 明確在目標／更新中加入參數懲罰，直接限制模型自由度，最符合題目『降低模型複雜度』。"
        "增加 Epoch 與無差別增加特徵可能強化記憶；移除驗證集則會失去泛化監測，不能解決問題。"
    ),
    "optionAnalysis": {
        "A": "模型目前已在訓練集達 F1=0.96，繼續訓練到 200 Epoch 通常會更貼合訓練細節，使驗證落差擴大；若採 early stopping，方向反而是及早停止。",
        "B": "新增 URL、HTML 標籤會增加輸入維度與可記憶的資料來源，其中還可能含網站或模板捷徑；未經篩選的更多特徵不等於降低模型複雜度。",
        "C": "正確。對權重施加 L2 懲罰會抑制大參數，降低模型對少數訓練模式的敏感度；係數應由保留的驗證資料調校，避免正則化過強。",
        "D": "把驗證集併入訓練集雖增加樣本，卻讓團隊無法獨立估計泛化或選超參數；它沒有直接限制模型複雜度，還可能隱藏既有過擬合。",
    },
    "trap": "題目限定『從降低模型複雜度』切入，因此要選正則化。更多資料有時能改善泛化，但把驗證集吞掉不是正確驗證流程，也不等於正則化。",
    "references": [
        exam_ref(13),
        ref(
            "PyTorch API－AdamW",
            "https://docs.pytorch.org/docs/stable/generated/torch.optim.AdamW.html",
            "Decoupled weight decay 與 weight_decay 參數的更新公式及介面",
        ),
        ref(
            "TensorFlow Keras－Regularizers",
            "https://www.tensorflow.org/api_docs/python/tf/keras/regularizers",
            "L2 regularizer 將權重平方懲罰加入 loss 的定義與用法",
        ),
    ],
}

DRAFTS[14] = {
    "summary": "正確答案是 C。Naive Bayes 的詞彙類別條件機率由訓練語料估計；若促銷詞幾乎只在垃圾信出現，模型就會錯把它們當成強垃圾訊號，應補足代表性資料並檢查先驗。",
    "concept": (
        "Multinomial Naive Bayes 依 P(class) 與各詞在類別下的 P(word|class) 組合後驗分數。當訓練"
        "資料缺少正常促銷郵件，『限時優惠』等詞的垃圾類條件機率會被高估，這是樣本分佈與"
        "representation bias 問題。改善重點是收集、標註或提高正常促銷郵件的代表性，重新估計"
        "詞彙統計；class prior 可校正垃圾信基準率，但不能單獨改寫已偏誤的詞彙條件機率。"
    ),
    "answerReason": (
        "C 唯一正確連結訓練語料分佈、類別條件機率與誤判，且提出資料平衡／先驗檢查方向。"
        "Naive Bayes 不需 Epoch 訓練，文字計數特徵也不因未標準化而造成分類邊界偏移。"
    ),
    "optionAnalysis": {
        "A": "Naive Bayes 對稀疏文字分類計算快速且常是有效基準；本題已找到資料中促銷詞分佈偏斜的具體原因，不需因單一失誤就斷定演算法一律不可用。",
        "B": "一般 Naive Bayes 由計數直接估計機率，不以反向傳播重複 Epoch 學習；增加 Epoch 沒有對應操作，也不會補進缺少的正常促銷語例。",
        "C": "正確。補充與重新取樣正常促銷信，可重新估計較合理的 P(word|normal)；若部署垃圾率不同，也應檢查 class prior，但兩種修正處理的機率項不同。",
        "D": "Multinomial NB 使用詞頻、計數或非負權重，不依靠歐氏距離或梯度尺度；Feature Scaling 不是修正促銷詞類別條件機率偏差的主要方法。",
    },
    "trap": "要分清 P(class) 與 P(word|class)：調整先驗只改類別基準率；題目描述的促銷詞偏誤主要要靠更具代表性的標註語料重估條件機率。",
    "editorialNote": "本站依官方答案 C 判定，但選項把『重新平衡資料』與『調整先驗機率』並列得較寬。題幹已明說問題是詞彙的類別條件機率偏高；單獨調整 class prior 只能改變類別基準率，不能修正 P(word|class)，較直接的改善是補入代表性的正常促銷郵件並重新估計條件機率。",
    "references": [
        exam_ref(14),
        ref(
            "scikit-learn－Naive Bayes",
            "https://scikit-learn.org/stable/modules/naive_bayes.html#multinomial-naive-bayes",
            "Multinomial Naive Bayes 的 class prior、類別條件詞彙分佈與平滑估計",
        ),
        ref(
            "scikit-learn API－MultinomialNB",
            "https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html",
            "fit_prior、class_prior、class_log_prior_ 與 feature_log_prob_ 的不同角色",
        ),
    ],
}

DRAFTS[15] = {
    "summary": "正確答案是 D。K-means 必須先指定 K，以到中心點的平方歐氏距離形成凸分區，對半月形群集、初始中心及會拉動平均值的離群點都敏感。",
    "concept": (
        "K-means 反覆執行兩步：把每點分配給最近 centroid，再以群內平均更新 centroid，目標是最小化"
        "群內平方距離 inertia。最近中心所形成的是 Voronoi 分區，適合近似凸且尺度相近的群集，"
        "無法沿半月形流形切出自然非凸群。均值與平方距離會放大遠端離群點影響；不同初始化還可能"
        "收斂到不同局部最小值，因此常用 k-means++、多次 n_init 與標準化後比較穩定性。"
    ),
    "answerReason": (
        "題幹一次提供 K=5、半月形、離群值與執行結果不同四個線索，D 分別對應預先指定群數、"
        "距離幾何限制、outlier sensitivity 與 initialization sensitivity，是唯一完整敘述。"
    ),
    "optionAnalysis": {
        "A": "K-means 沒有『超過 10 維就不能運作』的硬限制；高維會出現距離集中與計算負擔，需要特徵選擇或降維，但不能用固定維度門檻概括。",
        "B": "K-means 直接最小化到 centroid 的平方距離，並未假設資料由高斯分佈生成；它確實偏好凸、近球形群集，但『無法處理任何非球形』過度絕對。",
        "C": "K 值需事先選擇是限制，但 Lloyd 演算法只保證收斂到局部最小值；不同初始中心可得到不同 inertia 與分群，所以題目觀察到每次結果略異。",
        "D": "正確。K、距離形成的凸分區、初始中心與離群點分別解釋題目的所有現象；半月形資料可評估 DBSCAN、spectral clustering 等替代法。",
    },
    "trap": "K-means 的 K 與 k-nearest neighbors 的 K 無關。判斷限制時抓住 centroid、平方距離與局部最小值三件事，就能連到非凸、離群點與初始化。",
    "references": [
        exam_ref(15),
        ref(
            "scikit-learn－K-means",
            "https://scikit-learn.org/stable/modules/clustering.html#k-means",
            "K-means objective、初始化、局部最小值與高維 Euclidean distance 限制",
        ),
        ref(
            "scikit-learn－Comparing different clustering algorithms",
            "https://scikit-learn.org/stable/auto_examples/cluster/plot_cluster_comparison.html",
            "K-means 對非凸資料與不均勻群集的比較結果及演算法特性",
        ),
    ],
}

DRAFTS[16] = {
    "summary": "正確答案是 A。XGBoost 的目標函數除訓練損失外，還加入每棵樹的複雜度項，懲罰葉節點數與葉權重平方，抑制過度複雜的樹集合。",
    "concept": (
        "XGBoost 將第 t 棵樹的正則項寫成 Ω(f_t)=γT+(1/2)λΣw_j²，其中 T 是葉節點數、"
        "w_j 是葉分數，γ 控制新增葉的最低代價，λ 是葉權重 L2 正則化。配合 max_depth、"
        "min_child_weight、subsample 與 column subsampling 等限制，可降低模型追逐訓練噪聲。"
        "這項正則化是其核心目標的明確設計，但防過擬合仍需獨立驗證與 early stopping。"
    ),
    "answerReason": (
        "A 所稱樹複雜度懲罰與葉權重 L2 正是 XGBoost 原始目標函數的 Ω(f)。其他選項不是核心"
        "目標中的強制項：學習率不必動態衰減，卷積屬神經網路運算，也沒有強迫所有樹深度為 1。"
    ),
    "optionAnalysis": {
        "A": "正確。XGBoost 對葉節點數收取 γ 代價，並用 λ 懲罰葉權重平方；樹若不能帶來足夠損失改善，就不值得增加複雜度。",
        "B": "XGBoost 有固定 shrinkage/eta 參數降低每棵樹貢獻，也可由使用者排程調整，但核心目標函數並未強制學習率動態衰減。",
        "C": "卷積藉由共享局部濾波器處理影像等網格資料，屬 CNN 架構；XGBoost 是加法決策樹模型，不以卷積萃取空間特徵。",
        "D": "Decision stump 可降低單棵樹複雜度，某些 boosting 會選用，但 XGBoost 允許多種 max_depth，沒有把所有樹強制限制為深度 1。",
    },
    "trap": "不要把 XGBoost 名稱中的『gradient boosting』只理解為學習率。題目問核心 objective，關鍵公式是資料 loss 加上每棵樹的 Ω(f)。",
    "editorialNote": "本站依官方答案 A 判定。原始 XGBoost 正則式直接包含葉節點數 T 與葉權重 L2；樹深度通常由 max_depth 等結構參數間接限制，不宜把『深度』說成同一公式中的獨立懲罰項。",
    "references": [
        exam_ref(16),
        ref(
            "XGBoost: A Scalable Tree Boosting System",
            "https://arxiv.org/abs/1603.02754",
            "Section 2.1 regularized objective：Ω(f)=γT+1/2 λ||w||²",
        ),
        ref(
            "XGBoost 官方文件－Introduction to Boosted Trees",
            "https://xgboost.readthedocs.io/en/stable/tutorials/model.html",
            "Training loss 與 regularization term 組成 objective，並說明樹複雜度控制",
        ),
    ],
}

DRAFTS[17] = {
    "summary": "正確答案是 B。16 層 CNN 的訓練損失反而較高屬深度退化跡象；殘差捷徑讓梯度沿 identity path 傳遞，使深層網路較容易最佳化。",
    "concept": (
        "深層網路反向傳播時，梯度連乘可能變得很小，使靠近輸入的層更新困難；即使使用 ReLU 與"
        "正規化，增加深度也可能出現 optimization degradation：更深模型的訓練誤差反而更高。"
        "ResNet 讓區塊學習殘差 F(x)，輸出為 F(x)+x；identity skip connection 提供短路徑，讓"
        "訊號與梯度能跨越多層傳遞，且模型需要時可讓殘差接近零，較容易保留淺層解。"
    ),
    "answerReason": (
        "題目不是只說驗證表現差，而是深模型連訓練損失都較高且難收斂，指向最佳化／梯度傳遞。"
        "B 的殘差連接正是針對深度退化與梯度路徑的標準設計，其他選項未處理這個核心現象。"
    ),
    "optionAnalysis": {
        "A": "減少 filters 可降低參數與過擬合風險，但參數多通常首先表現為資源成本或泛化問題；題目是訓練損失比 3 層模型還高，較符合深層最佳化困難。",
        "B": "正確。Skip connection 將輸入直接加到區塊輸出，使梯度有較短的 identity path，緩解深層訊號衰減並讓殘差區塊較容易最佳化。",
        "C": "若現有 16 層已收斂困難，直接加深會延長梯度路徑與最佳化難度；應先改善架構、正規化、初始化及學習率，而不是假設深度越大越好。",
        "D": "Sigmoid 在飽和區導數接近零，深層連乘更容易造成梯度消失；由 ReLU 改成 Sigmoid 通常會惡化，而不是改善梯度傳遞。",
    },
    "trap": "訓練損失高與驗證損失高要分開判斷：更深模型連訓練集都學不好，是 optimization degradation，不是單純參數太多造成的過擬合。",
    "references": [
        exam_ref(17),
        ref(
            "Deep Residual Learning for Image Recognition",
            "https://arxiv.org/abs/1512.03385",
            "深層網路 degradation problem、residual mapping 與 identity shortcut 的設計及實驗",
        ),
    ],
}

DRAFTS[18] = {
    "summary": "正確答案是 A。池化會縮小特徵圖的高度與寬度，使後續全連結層接收的輸入數大幅下降，因而減少參數量與運算成本。",
    "concept": (
        "Pooling 在每個通道的局部視窗做 max 或 average 聚合，若使用 2×2、stride=2，特徵圖高寬"
        "各約減半，元素數降為約四分之一。池化層本身通常沒有可學習參數；真正大幅減少的是後續"
        "flatten 後全連結層的輸入連線數與計算量。它也帶來有限的局部平移穩健性，但會丟失空間"
        "細節，因此現代架構也可能用 strided convolution 或 global average pooling 取代部分池化。"
    ),
    "answerReason": (
        "題幹明確指出卷積後直接接全連結造成 5,000 萬參數，A 的空間下採樣會直接縮小 flatten"
        "向量，正面解決參數與計算瓶頸。非線性由 activation 提供，梯度消失也不是池化的主要用途。"
    ),
    "optionAnalysis": {
        "A": "正確。縮小 H×W 後，全連結層的輸入維度隨之降低；例如高寬各減半，若通道不變，連到 dense 層的權重數可約降到四分之一。",
        "B": "ReLU、GELU 等 activation 才是主要非線性來源；Max pooling 雖是非線性操作，但設計目的不是增加可學習表達能力，而是摘要與下採樣。",
        "C": "梯度消失主要與深度、激活飽和、初始化及正規化有關；池化縮短不了所有乘法梯度路徑，也不是專門強化反向傳播的機制。",
        "D": "池化可能藉由局部摘要提供一定平移穩健性並降低過擬合，但它必然改變空間維度或局部資訊；『不影響特徵維度』與題述加入池化不符。",
    },
    "trap": "池化通常沒有權重，但仍能間接大幅減少下一個 dense layer 的權重。計算參數時，要看池化前後 flatten 尺寸如何改變全連結輸入。",
    "references": [
        exam_ref(18),
        ref(
            "PyTorch API－MaxPool2d",
            "https://docs.pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html",
            "二維輸入在局部視窗取最大值及 stride 對輸出空間尺寸的公式",
        ),
        ref(
            "TensorFlow API－MaxPool2D",
            "https://www.tensorflow.org/api_docs/python/tf/keras/layers/MaxPool2D",
            "Max pooling 對二維空間資料進行下採樣及輸出 shape 計算",
        ),
    ],
}

DRAFTS[19] = {
    "summary": "正確答案是 D。Self-Attention 讓首頁與第 20 頁的 token 在一層內直接互相建立權重關聯，並可同時計算各位置，比 LSTM 的逐步傳遞更適合長距離依賴。",
    "concept": (
        "LSTM 按序列時間步遞迴，遠距資訊必須經過許多隱藏狀態傳遞，路徑長且各步有前後依賴，"
        "不易在單一序列內完全平行化。Transformer self-attention 以所有 token 的 query-key 相似度"
        "計算關聯，每一位置可在同一層直接關注其他位置，將長距依賴路徑縮短並讓訓練矩陣運算"
        "平行化。不過標準 attention 的時間與記憶體成本約隨序列長度平方增加，長文件仍需分段或長上下文設計。"
    ),
    "answerReason": (
        "首頁與第 20 頁條款的核心難題是相隔很遠的語義比對及遞迴運算瓶頸。D 同時指出 self-attention"
        "的直接全域連結與平行化，正好解釋改用 Transformer 後關聯捕捉及訓練效率改善。"
    ),
    "optionAnalysis": {
        "A": "Transformer 參數量不必然比 LSTM 少，取決於層數、hidden size、attention heads 與 FFN；訓練速度優勢主要來自序列位置可平行化，而不是固定較少參數。",
        "B": "位置編碼提供 token 的位置資訊，卻不會自動理解首頁、章節或責任條款等文件結構；章節語意仍要由資料、標記與 attention 學得。",
        "C": "LSTM 沒有 512 token 的架構硬上限，只是長序列難訓練且成本高；標準 Transformer 也受 context window 與平方 attention 成本限制，並非無限制。",
        "D": "正確。任意兩個 token 可透過 attention 在單層直接互動，跨頁資訊不必逐步經過 19 頁的隱藏狀態；各位置的 attention 也可用矩陣運算平行計算。",
    },
    "trap": "Transformer 的長距關聯優勢不是『無長度限制』。它縮短 token 間的網路路徑並支援平行運算，但上下文視窗和 O(n²) attention 仍是實際限制。",
    "references": [
        exam_ref(19),
        ref(
            "Attention Is All You Need",
            "https://arxiv.org/abs/1706.03762",
            "Table 1 比較 self-attention 與 recurrent layer 的序列運算、平行步驟及最大路徑長度",
        ),
    ],
}

DRAFTS[20] = {
    "summary": "正確答案是 C。PyTorch CrossEntropyLoss 直接接收每一類未正規化 logits；三分類輸出層應有 3 個單元，前向輸出不先套 Softmax。",
    "concept": (
        "對單一標籤的 C 類分類，模型輸出 shape 通常為 (batch, C)，每欄是任意實數 logit。"
        "CrossEntropyLoss 在數值穩定的實作中等價於 LogSoftmax 加 NLLLoss，因此訓練時若模型先"
        "Softmax，會把機率當成 logits 再正規化，改變損失與梯度且降低數值穩定性。貓、狗、鳥互斥"
        "三分類令 C=3，target 通常是 0、1、2 的 class index；推論展示機率時才對 logits 做 softmax。"
    ),
    "answerReason": (
        "C 同時滿足 CrossEntropyLoss 的輸入契約與三分類輸出維度。ReLU 單輸出不能表示三類；"
        "Sigmoid 適合獨立多標籤機率；訓練模型內先做 Softmax 則與損失內部運算重複。"
    ),
    "optionAnalysis": {
        "A": "ReLU 只保留非負值，單一輸出也無法為三個互斥類別各提供分數；CrossEntropyLoss 需要最後一維包含 C=3 個 class logits。",
        "B": "三個 Sigmoid 將各類視為獨立 Bernoulli，適合一張圖可同時有多個標籤的 multi-label 任務；貓狗鳥互斥單標籤分類應共同正規化。",
        "C": "正確。最後線性層輸出 3 個不受限 logits，直接交給 CrossEntropyLoss；推論時若要顯示機率，再沿類別維度套 Softmax。",
        "D": "輸出 3 維正確，但訓練前先 Softmax 會與 CrossEntropyLoss 內含的 LogSoftmax 重複；還可能因先轉機率而造成較差的數值與梯度行為。",
    },
    "trap": "記住 PyTorch 損失輸入契約：CrossEntropyLoss 吃 logits，不吃預先 Softmax 的機率；BCEWithLogitsLoss 同樣把 sigmoid 與 BCE 合併。",
    "references": [
        exam_ref(20),
        ref(
            "PyTorch API－CrossEntropyLoss",
            "https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html",
            "輸入為未正規化 logits，類別索引目標時等價於 LogSoftmax 後接 NLLLoss",
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
