"""Write draft explanations for 115-1 intermediate subject three, Q41-Q50.

The script verifies official answers, refuses to overwrite reviewed work, and
keeps every generated explanation in ``draft`` for independent review.

Usage::

    python scripts/write-explanations-115-1-m3-041-050.py
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


def exam_ref(number: int, locator: str | None = None) -> dict:
    return {
        "title": "115 年第一次中級 AI 應用規劃師－機器學習技術與應用公告試題",
        "url": EXAM_PDF,
        "locator": locator or f"第 {number} 題題幹、選項與官方答案",
        "checkedAt": CHECKED_AT,
    }


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


EXPECTED_ANSWER = {
    41: "B", 42: "C", 43: "D", 44: "B", 45: "A",
    46: "B", 47: "B", 48: "D", 49: "C", 50: "B",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[41] = {
    "summary": "正確答案是 B。附圖以 p=0.5 隨機水平翻轉手寫字母，會把 b、d 或 p、q 等具有方向語義的形狀變成另一類外觀，卻仍保留原標籤，造成標籤污染。",
    "concept": (
        "資料增強必須保持類別語義不變。對一般物體，水平翻轉可能是合理不變性；對文字與數字，"
        "方向本身常決定類別，鏡像後不再屬於原標籤。已目視核對附圖 Compose 順序為"
        " RandomHorizontalFlip(p=0.5)、RandomRotation(15)、ColorJitter(brightness=0.3)、ToTensor。"
        "若訓練與驗證都套用相同有害規則，驗證 loss 仍可能下降，卻與部署的正常書寫分布不一致。"
    ),
    "answerReason": "b/d/p/q 正是翻轉或旋轉後容易混淆的方向性字母，而圖中水平翻轉有 50% 機率且不會同步改標籤，最能解釋部署錯誤。15 度旋轉與亮度變化通常仍保留字母，ToTensor 放在 PIL 幾何與色彩變換之後也合理。",
    "optionAnalysis": {
        "A": "小角度旋轉可模擬手寫傾斜，15 度未必破壞類別；它可能增加 p/q 等混淆，但不如 50% 鏡像直接把 b 外觀變得接近 d 的標籤矛盾。",
        "B": "正確。HorizontalFlip 改變左右方向，卻沿用原字母標籤；模型因此反覆看到鏡像 d 樣外觀標成 b 等錯誤監督，部署在正常方向文字時容易混淆。",
        "C": "Brightness ColorJitter 改的是整體明暗，通常不會改變筆畫拓撲或字母身分；幅度是否過大需看影像，但它不能特別解釋 b/d/p/q 的方向性錯誤。",
        "D": "圖中幾何與亮度轉換可先處理 PIL image，最後 ToTensor 轉成張量，屬常見順序；先 ToTensor 並不是維持座標對應的必要條件。",
    },
    "trap": "不是所有常見增強都適合所有領域。先問轉換是否真的 label-preserving；文字、交通方向、醫學左右側等任務尤其不能照搬自然影像的水平翻轉。",
    "editorialNote": "本站已於 2026-08-13 目視核對 Q41 附圖全部四個 transforms。驗證 loss 持續下降不代表部署分布正確；仍需確認 validation transform 是否誤用了隨機增強，正式驗證通常只做確定性必要前處理。",
    "references": [
        exam_ref(41, "第 41 題 Transform 附圖、題幹、選項與官方答案"),
        ref("torchvision－RandomHorizontalFlip", "https://docs.pytorch.org/vision/stable/generated/torchvision.transforms.RandomHorizontalFlip.html", "以指定機率水平翻轉影像"),
        ref("PyTorch－Transforms v2 end-to-end example", "https://docs.pytorch.org/vision/stable/auto_examples/transforms/plot_transforms_e2e.html", "訓練增強與驗證確定性前處理分開配置的官方範例"),
    ],
}

DRAFTS[42] = {
    "summary": "正確答案是 C。附圖行 A 將預訓練 ResNet50 全部既有參數設為 `requires_grad=False`，凍結 backbone，只訓練新換上的全連接層，屬特徵萃取策略。",
    "concept": (
        "遷移學習的 feature extraction 把預訓練網路視為固定特徵轉換器，凍結其參數，再替換並"
        "訓練任務專用分類頭。已目視核對圖中 `for param in model.parameters(): param.requires_grad = False`，"
        "之後 `model.fc = nn.Linear(2048, 2)`；新 fc 是凍結迴圈後才建立，預設仍需梯度，optimizer"
        "也只接收 `model.fc.parameters()`。全面 fine-tuning 則會讓部分或全部 backbone 權重更新。"
    ),
    "answerReason": "行 A 明確關閉所有當時既有模型權重的梯度，配合只訓練新 fc，完全符合 C。它不是更新所有層的全面微調，也沒有不經訓練直接推論的 zero-shot，且沒有教師／學生模型的蒸餾流程。",
    "optionAnalysis": {
        "A": "Full fine-tuning 會讓預訓練層參與反向傳播並更新，通常搭配較小學習率；圖中反而將所有既有 parameters 凍結，所以不屬全面微調。",
        "B": "Zero-shot 是模型不以該任務標註樣本更新便處理新類別；圖中建立二類 fc 並以 optimizer 訓練它，仍是有訓練的遷移學習。",
        "C": "正確。凍結 ResNet backbone 後，其輸出作為固定的高階影像特徵，只學習新 `Linear(2048,2)` 分類頭，就是 feature extraction。",
        "D": "知識蒸餾需教師模型提供 soft targets 或表徵，訓練學生模型模仿；圖中只有單一 ResNet 與替換分類頭，沒有師生架構。",
    },
    "trap": "凍結 backbone、只訓練 head 是 feature extraction；解凍部分或全部層再小步更新才是 fine-tuning。要注意新 fc 在凍結迴圈之後建立，所以沒有被一起凍結。",
    "editorialNote": "附圖使用 `resnet50(pretrained=True)`，新版 torchvision 已改以 `weights=ResNet50_Weights.DEFAULT` 表達；不影響本題行 A 的策略判斷。",
    "references": [
        exam_ref(42, "第 42～43 題 ResNet 程式附圖、行 A、選項與官方答案"),
        ref("PyTorch－Transfer Learning for Computer Vision Tutorial", "https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html", "區分 fine-tuning 與固定特徵萃取器，並以 requires_grad=False 凍結參數"),
    ],
}

DRAFTS[43] = {
    "summary": "正確答案是 D。微調時使用較小學習率，可讓預訓練參數逐步適應新任務，避免一次更新過大而快速破壞原本已有用的特徵表示。",
    "concept": (
        "預訓練權重已位於能表達一般模式的參數區域，fine-tuning 的目標是溫和調整而非從隨機"
        "初始化重新搜尋。學習率控制每一步沿梯度更新的幅度；過大可能造成 catastrophic forgetting、"
        "loss 震盪或離開有用解。分類頭若為新初始化，常可用比 backbone 更大的學習率。需注意"
        "Q42 圖實際凍結 backbone、optimizer 只含 fc，嚴格說是 feature extraction；本題改問一般微調原則。"
    ),
    "answerReason": "D 正確連結小學習率與保護預訓練表示。OOM 主要取決於模型、activation、batch 與精度；小學習率不保證更快收斂，更不可能強制 loss 變成零。",
    "optionAnalysis": {
        "A": "學習率是 optimizer 更新係數，通常不顯著改變 forward/backward 所需 activation 記憶體；OOM 更常以縮小 batch、影像或模型及混合精度處理。",
        "B": "較小步幅常需要更多更新才能收斂，不能說主要目的在加快整體時間；它換取的是微調穩定性與較低的預訓練知識破壞風險。",
        "C": "學習率不能強制 loss 歸零；資料噪聲、正則化與不可約誤差都可能使 loss 非零，刻意追求訓練 loss 為零反而可能過擬合。",
        "D": "正確。小 learning rate 限制每次參數位移，使 backbone 在新任務梯度下逐步調整，較不易突然抹除預訓練形成的可泛化特徵。",
    },
    "trap": "先分清圖中『只訓練新 head』與題目問的『fine-tuning』。若 backbone 被凍結，其學習率沒有作用；只有解凍的參數才會被 optimizer 更新。",
    "editorialNote": "圖中 optimizer 僅包含 `model.fc.parameters()`，所以 1e-4 實際只作用於新分類頭，並未微調凍結的 ResNet backbone。本題應視為脫離該程式細節的一般 fine-tuning 原理題；已保留此語境差異供人工複核。",
    "references": [
        exam_ref(43, "第 42～43 題 ResNet 程式附圖、第 43 題選項與官方答案"),
        ref("PyTorch－Transfer Learning for Computer Vision Tutorial", "https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html", "預訓練 ConvNet 微調與固定特徵萃取兩種情境"),
    ],
}

DRAFTS[44] = {
    "summary": "正確答案是 B。附圖先在全部 X、y 上執行監督式 LDA `fit_transform`，再對轉換結果交叉驗證 KNN；驗證折的標籤已參與降維，造成資料洩漏。",
    "concept": (
        "交叉驗證要模擬未見資料：所有會從資料估計參數的前處理，都必須只在每折 training fold"
        "上 fit，再用該折的轉換器 transform validation fold。LDA 是監督式降維，會利用 X 與 y"
        "尋找類別分離方向，洩漏尤其直接。已目視圖中 `X_new = lda.fit_transform(X,y)` 發生在"
        "`cross_val_score(model, X_new, y, cv=5)` 之前；應以 Pipeline 串接 LDA 與 KNN 後整體 CV。"
    ),
    "answerReason": "B 精確指出洩漏及修正方式。附圖得到 0.9733 不能視為無偏泛化估計，因每個 validation fold 的標籤已影響 LDA 投影；跳過 LDA 則變成另一模型流程，不能回答原本要評估 LDA+KNN 的問題。",
    "optionAnalysis": {
        "A": "錯誤。先用完整 y 擬合 LDA，等於讓驗證折的類別資訊參與特徵建立，再測 KNN；交叉驗證只包住分類器並不足以隔離資料。",
        "B": "正確。把 `LinearDiscriminantAnalysis()` 與 `KNeighborsClassifier()` 放入 sklearn Pipeline，再將 Pipeline 傳給 cross_val_score，每折才會獨立 fit LDA。",
        "C": "流程雖能產生分數，但因 validation fold 參與降維，結果通常偏樂觀，不能宣稱代表模型部署到真正新資料的泛化能力。",
        "D": "不做 LDA 可以另行評估原始四特徵的 KNN，但不再是題目要比較的 LDA 降維後 KNN；簡化流程不能修正對原流程的不公平估計。",
    },
    "trap": "資料洩漏不只發生在 scaling。特徵選擇、補值、PCA，以及本題使用標籤的 LDA，都必須放進每個 fold 裡 fit；可用 Pipeline 自動維持邊界。",
    "editorialNote": "本站已目視核對 Q44 圖的完整程式與輸出 0.9733333333333334，以及題組四張 Iris 載入／head 圖；解析不把該數字視為可信泛化分數。",
    "references": [
        exam_ref(44, "第 44～45 題 Iris 題組四圖、Q44 LDA/KNN 程式與輸出圖、選項及答案"),
        ref("scikit-learn－Common pitfalls: data leakage", "https://scikit-learn.org/stable/common_pitfalls.html#data-leakage", "前處理只以訓練資料 fit，並使用 Pipeline 避免交叉驗證洩漏"),
        ref("scikit-learn－Pipeline", "https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html", "將 transformers 與 final predictor 串成可交叉驗證的單一 estimator"),
    ],
}

DRAFTS[45] = {
    "summary": "正確答案是 A。程式碼 B 的 StratifiedKFold、程式碼 C 的整數 `cv=5`（分類器預設分層），以及程式碼 D 的 RepeatedStratifiedKFold 都會維持各折類別比例。",
    "concept": (
        "分層交叉驗證讓每折的各類比例近似完整資料，對三類各 50 筆的 Iris 可避免某折類別組成"
        "偏斜。已目視核對候選圖：A=`KFold(n_splits=5, shuffle=True)`；B=`StratifiedKFold(...)`；"
        "C=`cv=5`；D=`RepeatedStratifiedKFold(n_splits=5,n_repeats=2)`。cross_val_score 對 classifier"
        "且 y 為 multiclass 時，傳整數會採 StratifiedKFold；KFold 則不使用 y 做類別分層。"
    ),
    "answerReason": "B 與 D 名稱和行為都明確分層；C 在本題 KNeighborsClassifier 的 cross_val_score 中會由 `check_cv` 選 StratifiedKFold。因此合適的是 B、C、D，對應選項 A。",
    "optionAnalysis": {
        "A": "正確。它列出候選 B、C、D：B 與 D 明確 stratified；C 的整數 cv 在分類器加 multiclass y 的情況下也會使用 StratifiedKFold。",
        "B": "此組合包含候選 A 的普通 KFold，後者只分索引而不依 y 維持比例；即使 shuffle，也不能保證每折三類比例與原資料一致。",
        "C": "它同樣誤納候選 A。B 與 D 是合理分層策略，但普通 KFold 不能因資料原本平衡就視為具分層保證。",
        "D": "候選 C、D 都合適，但漏掉同樣直接適用的候選 B `StratifiedKFold(n_splits=5, shuffle=True)`，所以組合不完整。",
    },
    "trap": "`cv=5` 的具體 splitter 取決於 estimator 與 y：分類器搭配 binary/multiclass 會分層；迴歸器則使用 KFold。不能脫離 cross_val_score 語境死背整數 cv。",
    "editorialNote": "本站已目視核對 Q45 兩張圖的原始 cross_val_score 插入位置與 A～D 候選程式。B 使用 shuffle=True 卻未設 random_state，重跑折分可能不同，但不影響其分層性。",
    "references": [
        exam_ref(45, "第 44～45 題題組圖、Q45 原始程式與 A～D 候選程式圖、選項及答案"),
        ref("scikit-learn－cross_val_score", "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html", "cv 為整數時分類器與 binary/multiclass y 使用 StratifiedKFold"),
        ref("scikit-learn－StratifiedKFold", "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedKFold.html", "建立近似維持各類樣本比例的 folds"),
        ref("scikit-learn－RepeatedStratifiedKFold", "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.RepeatedStratifiedKFold.html", "以不同隨機化重複 Stratified K-fold"),
    ],
}

DRAFTS[46] = {
    "summary": "正確答案是 B。圖中除以 255 將像素縮放至 0～1，可改善數值尺度與訓練穩定性；to_categorical 把標籤轉為 10 維 one-hot，適合搭配 10 類 softmax。",
    "concept": (
        "已目視題組圖：CIFAR-10 以 `datasets.cifar10.load_data()` 載入，`x_train[0]` 是每像素"
        "三個 0～255 RGB 整數，`y_train[0]` 為 `array([6], dtype=uint8)`。處理圖將 train/test"
        "影像都除以 255.0，並以 `to_categorical(...,10)` 轉換兩組標籤。輸入縮放不等於 z-score；"
        "one-hot 目標通常配合 10-unit softmax 與 categorical cross-entropy。"
    ),
    "answerReason": "描述 B、D、E、F 分別對應改善泛化／訓練穩定、降低梯度數值不穩、one-hot 標籤與 softmax 相容。A 把 0～1 錯寫成 0～31；C 把 min-max 式縮放錯稱 z-score。因此選 B。",
    "optionAnalysis": {
        "A": "此組合包含描述 A 與 C；除以 255 後原 0～255 像素落在 0～1，不是 0～31，也沒有減平均除標準差，所以 A、C 都不成立。",
        "B": "正確。描述 B、D、E、F 與圖中尺度縮放、one-hot 及 10 類輸出用途相符；縮放使數值條件較穩定，標籤表示則配合 categorical softmax 分類。",
        "C": "描述 B、E、F 可成立，但描述 C 不成立；z-score 必須減去平均值再除以標準差，單純除以 255 是固定範圍縮放。",
        "D": "它多納入描述 A；影像值除以 255.0 的明確範圍是 [0,1]，並非 [0,31]，所以整組不能選。",
    },
    "trap": "除以 255 是 rescaling，不是 z-score。另 one-hot 是否必要取決於 loss：categorical_crossentropy 用 one-hot；sparse_categorical_crossentropy 可直接用整數標籤。",
    "editorialNote": "本站已目視核對 Q46 題組五張圖，包括原始 RGB 陣列、label 6、除以 255 與 A～F 描述。描述 B、D 使用『增加泛化』『避免梯度爆炸或消失』語氣偏強；縮放主要改善數值條件與訓練穩定性，並不單獨保證泛化或避免所有梯度問題。本站仍依官方答案 B。",
    "references": [
        exam_ref(46, "第 46～48 題 CIFAR-10 載入與資料圖、Q46 處理程式與 A～F 描述圖、選項及答案"),
        ref("Keras－CIFAR10 small images classification dataset", "https://keras.io/api/datasets/cifar10/", "CIFAR-10 的 50,000/10,000 張 32x32 RGB 影像與整數標籤形狀"),
        ref("TensorFlow－to_categorical", "https://www.tensorflow.org/api_docs/python/tf/keras/utils/to_categorical", "將整數類別向量轉成 binary class matrix"),
        ref("Keras－Rescaling layer", "https://keras.io/api/layers/preprocessing_layers/image_preprocessing/rescaling/", "以 scale=1./255 將 [0,255] 輸入縮放至 [0,1]"),
    ],
}

DRAFTS[47] = {
    "summary": "正確答案是 B。描述 C、E、F 正確：Conv2D 後的 BatchNormalization 有助穩定深層訓練，Dropout 可降低過擬合，Flatten 將空間×通道特徵攤平成一維向量。",
    "concept": (
        "已目視模型圖：輸入 32×32×3；區塊 1 兩個 32-filter same Conv2D，區塊 2 為 64 filters，"
        "區塊 3 為 128 filters，各含 BN、2×2 max pooling、Dropout(0.25)；區塊 4 Flatten、Dense(256)、"
        "BN、Dropout(0.5)、Dense(10,softmax)。same padding 與 stride 1 保持高寬，但第一個 Conv2D"
        "輸出通道數由 filters=32 決定，所以輸出是 32×32×32，不是描述 B 所寫 32×32×3。"
    ),
    "answerReason": "A 錯把 Input 當標準化；B 錯寫 Conv2D 輸出通道；D 錯稱 Dropout 把輸出設為 1，實際訓練時是隨機設為 0。C、E、F 分別正確描述 BN、Dropout 正則化與 Flatten，因此對應選項 B。",
    "optionAnalysis": {
        "A": "選項 A 含描述 A，然而 `layers.Input(shape=(32,32,3))` 只宣告輸入形狀，不做像素縮放或標準化；即使描述 C 正確，組合仍錯。",
        "B": "正確。描述 C、E、F 均符合圖中層的作用：BN 穩定 activation／gradient，Dropout(0.25) 正則化，Flatten 將三維特徵圖展成給 Dense 使用的向量。",
        "C": "描述 A 錯把 Input 視為標準化，描述 D 又錯稱 Dropout 將 25% 輸出設為 1；訓練時被抽中的 units 輸出會設為 0，再對其餘值縮放。",
        "D": "描述 E、F 成立，但描述 D 的 Dropout 行為錯誤；它不是隨機開啟為 1，而是隨機丟棄為 0，因此此組合不能選。",
    },
    "trap": "卷積輸出 shape 看四件事：batch、高寬、filters。same 只保持高寬，不保持 channels；Dropout 是設零，不是設一；Input 只聲明形狀。",
    "editorialNote": "本站已目視核對 Q47 兩張圖的完整 Sequential 模型與 A～F 描述。描述 C 的『減少梯度消失或爆炸』是概括性效果，BatchNormalization 能改善訓練穩定但不保證完全避免。",
    "references": [
        exam_ref(47, "第 46～48 題共用資料圖、Q47 CNN 模型與 A～F 描述圖、選項及答案"),
        ref("Keras－Conv2D", "https://keras.io/api/layers/convolution_layers/convolution2d/", "filters 決定輸出通道，same padding 在 stride=1 時保持空間尺寸"),
        ref("Keras－Dropout", "https://keras.io/api/layers/regularization_layers/dropout/", "訓練時隨機將輸入 units 設為 0 並縮放其餘值"),
        ref("Keras－Flatten", "https://keras.io/api/layers/reshaping_layers/flatten/", "將非 batch 維度攤平成向量"),
        ref("Keras－BatchNormalization", "https://keras.io/api/layers/normalization_layers/batch_normalization/", "以 batch 統計正規化 activation，推論時使用 moving statistics"),
    ],
}

DRAFTS[48] = {
    "summary": "正確答案是 D。圖中第 6 個 epoch 附近訓練 accuracy 約 0.81，驗證 accuracy 卻跌至約 0.72，顯示模型持續貼合訓練資料但對未見資料的泛化變差，最像過擬合。",
    "concept": (
        "Overfitting 的典型訊號是 training metric 持續改善，而 validation metric 停滯、惡化或與"
        "訓練差距擴大。已目視圖中藍線從約 0.47 持續升至 0.84，紅線大致上升但在 x=6 明顯由"
        "約 0.80 跌到 0.72，之後回升。單一 epoch 的震盪也可能來自驗證樣本量、隨機性或學習率；"
        "應觀察多次重跑與 validation loss，再用 early stopping、資料增強或正則化處理。"
    ),
    "answerReason": "四個選項中 D 最能解釋訓練高、驗證低的泛化差距。Underfitting 通常兩者都偏低且訓練也無法改善；低 learning rate 或大 batch 可能影響收斂，但不能僅由這組曲線直接推定。",
    "optionAnalysis": {
        "A": "學習率太低通常表現為訓練進展緩慢；圖中 training accuracy 仍穩定上升，無法由第 6 epoch 的 train/validation 差距直接判定 learning rate 太低。",
        "B": "大 batch 會改變梯度噪聲與泛化，但題目未提供 batch 對照；它不是看到訓練優於驗證時最直接的診斷名稱。",
        "C": "Underfitting 表示模型連訓練資料規律都沒學好，training 與 validation 通常一起偏低；此處訓練表現持續較好而驗證落後，方向相反。",
        "D": "正確。訓練 accuracy 上升至約 0.81，同時驗證跌至約 0.72，形成明顯 generalization gap，符合模型過度適應訓練資料的現象。",
    },
    "trap": "圖的 y 軸是 Accuracy，雖題幹前文稱『曲線值』，不是 validation loss。還要注意單點下跌不足以證明長期過擬合，應看後續趨勢與多次實驗。",
    "editorialNote": "本站已目視核對 Q48 圖：橫軸標示 0～9，題目所稱 Epochs=6 對應 x=6，約為 train 0.81、validation 0.72；紅線在 x=7、8 又回升。因此 D 是四選一的最可能原因，但單一谷值也可能是隨機波動，不能據此獨立確診。",
    "references": [
        exam_ref(48, "第 46～48 題共用 CIFAR-10 圖、Q48 train/validation accuracy 曲線、選項與答案"),
        ref("TensorFlow－Overfit and underfit", "https://www.tensorflow.org/tutorials/keras/overfit_and_underfit", "以訓練與驗證指標分歧辨識過擬合，並示範正則化方法"),
        ref("Keras－EarlyStopping", "https://keras.io/api/callbacks/early_stopping/", "監控驗證指標並在停止改善時終止訓練"),
    ],
}

DRAFTS[49] = {
    "summary": "正確答案是 C。ResNet 的 identity skip connection 讓訊號與梯度能繞過多個權重層，緩解極深網路的退化與最佳化困難，適合超過 50 層的 CNN。",
    "concept": (
        "Residual block 不直接只學 H(x)，而令堆疊層學殘差 F(x)，輸出為 F(x)+x。加法中的 identity"
        " path 提供較短的資訊與梯度路徑，使多層若暫時無益也較容易近似 identity mapping。原始"
        "ResNet 論文展示 50、101、152 層網路可有效訓練。這不代表梯度永不消失，也仍需初始化、"
        "正規化與適當 optimizer；但它是題目所問經典、直接針對深度訓練困難的架構。"
    ),
    "answerReason": "C 明確以 residual/skip connection 回應超過 50 層與梯度傳遞問題。VGG 單純堆疊；GoogLeNet 的 Inception 主要做多尺度與計算配置；ViT 仍是深層網路，也可能有最佳化與資料需求問題，不能宣稱沒有訓練問題。",
    "optionAnalysis": {
        "A": "VGG 的重複 3×3 卷積能增加深度與感受野，但沒有跨層 identity shortcut；單純堆疊不能保證超過 50 層時梯度穩定。",
        "B": "Inception 並行不同卷積核可擷取多尺度特徵並控制計算量，GoogLeNet 亦使用輔助分類器；但選項所述模組本身不是最直接的殘差梯度通道。",
        "C": "正確。輸出 F(x)+x 的 skip connection 允許梯度沿 identity path 跨越權重層，降低深網路退化與最佳化障礙，ResNet-50 也直接符合深度需求。",
        "D": "ViT 捨棄卷積改用 self-attention，不等於消除深層最佳化、梯度、過擬合或資料需求；『不會出現任何問題』是過度絕對的說法。",
    },
    "trap": "ResNet 的經典貢獻常描述為解決 degradation／optimization problem，不應誇張成完全消除 vanishing gradient。題目四選一仍以 skip connection 最直接。",
    "editorialNote": "題幹把 ResNet 作用集中描述為梯度消失；原始論文更直接討論深度增加後的 degradation problem，且指出不是單純 overfitting。殘差連接改善梯度路徑，但不能保證任何設定下都不消失。",
    "references": [
        exam_ref(49),
        ref("He et al.－Deep Residual Learning for Image Recognition", "https://openaccess.thecvf.com/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html", "以 residual learning 與 identity shortcut 訓練 50、101、152 層網路"),
    ],
}

DRAFTS[50] = {
    "summary": "正確答案是 B。梯度必須在 `loss.backward()` 產生後、`optimizer.step()` 使用前裁剪，因此應放在位置 4 與 5 之間，以限制總梯度範數及參數更新失控。",
    "concept": (
        "已目視圖中順序：位置 1 `optimizer.zero_grad()`、位置 2 forward、位置 3 計算 loss、位置 4"
        " `loss.backward()`、位置 5 `optimizer.step()`。`clip_grad_norm_` 讀取 parameters 的 `.grad`，"
        "計算整體範數，若超過 max_norm 就按比例縮放。backward 前尚無本輪梯度，step 後權重已更新，"
        "所以正確窗口只有兩者之間。它防的是 exploding gradients，不直接限制 loss 或輸入。"
    ),
    "answerReason": "B 的位置與機制都正確：backward 先建立梯度，clipping 再限制範數，step 最後依裁剪後梯度更新。其餘選項不是放在梯度存在且尚未更新的時機，就是把 clipping 誤解為 loss、權重或影像正規化。",
    "optionAnalysis": {
        "A": "位置 3～4 是計算 loss 後、backward 前，參數尚未取得本輪 `.grad`，無法裁剪；clip_grad_norm_ 也不會限制 loss 數值，更不是處理梯度消失。",
        "B": "正確。`loss.backward()` 後 gradients 已累積，`optimizer.step()` 前呼叫 `clip_grad_norm_(model.parameters(), max_norm)`，更新便會使用縮放後梯度。",
        "C": "step 後本輪權重已按未裁剪梯度更新，才裁剪太晚；函式操作的是 `.grad`，不是把更新後 weights 強制壓進某個數值範圍。",
        "D": "位置 1～2 位於清梯度與 forward 之間，尚無本輪梯度；輸入影像標準化應在 dataset transform／preprocessing 完成，不由 gradient clipping 處理。",
    },
    "trap": "順序固定為 zero_grad → forward → loss → backward → clip → step。若使用自動混合精度，還要先 unscale gradients 再 clip，否則裁的是放大後梯度。",
    "editorialNote": "本站已目視核對 Q50 圖中位置 1～5。Gradient clipping 可降低 exploding-gradient 導致的 NaN 風險，但 NaN 也可能來自資料、除零、非法 log、過高 learning rate 或 mixed-precision overflow，不能只靠 clipping 當成完整根因修復。",
    "references": [
        exam_ref(50, "第 49～50 題 AOI 情境、Q50 訓練迴圈位置圖、選項與官方答案"),
        ref("PyTorch－clip_grad_norm_", "https://docs.pytorch.org/docs/stable/generated/torch.nn.utils.clip_grad_norm_.html", "將參數梯度視為單一向量計算總範數並原地裁剪"),
        ref("PyTorch－Automatic Mixed Precision examples", "https://docs.pytorch.org/docs/stable/notes/amp_examples.html#gradient-clipping", "AMP 下在 backward 後先 unscale，再 clip，最後 step 的官方流程"),
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
