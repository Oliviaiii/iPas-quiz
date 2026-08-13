"""Write draft explanations for 114-2 intermediate subject three, Q41-Q50.

The official PDF pages 10-19 were rendered and visually checked because the
question JSON does not retain the referenced code listings, tables, or plots.
The script verifies official answers and refuses to overwrite reviewed work.
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


def exam_ref(number: int, pages: str) -> dict:
    return {
        "title": "114 年第二次中級 AI 應用規劃師－機器學習技術與應用公告試題",
        "url": EXAM_PDF,
        "locator": f"試卷第 {pages} 頁：第 {number} 題題幹、附圖／程式碼、選項與官方答案",
        "checkedAt": CHECKED_AT,
    }


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


EXPECTED_ANSWER = {
    41: "D", 42: "B", 43: "A", 44: "D", 45: "B",
    46: "B", 47: "B", 48: "C", 49: "C", 50: "C",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[41] = {
    "summary": "正確答案是 D。條件機率 P(A|B)=P(A∩B)/P(B)；Monte Carlo 以樣本次數近似時，就是同時滿足 A、B 的次數除以滿足 B 的次數。",
    "concept": (
        "官方附圖程式先以 `np.random.randint(1, 7, size=100000)` 模擬骰子，再建立"
        "布林陣列 A（偶數）、B（大於 3）與 `A_and_B = A & B`。NumPy 對布林陣列"
        "呼叫 sum 會把 True 當 1，因此 `A_and_B.sum()` 是交集次數，`B.sum()` 是條件"
        "事件次數。由定義 P(A|B)=P(A∩B)/P(B)，共同除以總模擬數 n 後 n 會約掉。"
        "理論上 B={4,5,6}，其中 A∩B={4,6}，所以機率為 2/3；模擬比值應接近而非"
        "必然精確等於 2/3。"
    ),
    "answerReason": (
        "D 的分子、分母分別正確對應交集與條件事件樣本數。這不是除以 A 的次數，"
        "也不能把兩個事件次數相乘或相加當分母。"
    ),
    "optionAnalysis": {
        "A": "A.sum()×B.sum() 是兩個計數相乘，量級約為 n²，既沒有除回 n，也不是任何條件機率分母；即使 A、B 獨立也不能如此估計 P(A|B)。",
        "B": "A.sum()+B.sum() 會重複計入交集，且它既不是聯集次數（聯集應扣交集），也不是條件事件 B 的次數，無法對應條件機率定義。",
        "C": "以 A.sum() 作分母計算的是 P(B|A) 的樣本估計，即已知擲出偶數時又大於 3 的比例；題目條件方向是已知 B 求 A，不能顛倒。",
        "D": "正確。B.sum() 限定所有大於 3 的模擬樣本，A_and_B.sum() 計算其中同時為偶數者，兩者相除即 Monte Carlo 估計 P(A|B)。",
    },
    "trap": "條件機率最容易把方向看反：P(A|B) 的分母一定是 B。先口語讀成『在 B 發生的樣本裡，有多少也發生 A』，再寫程式。",
    "references": [
        exam_ref(41, "10-11"),
        ref("NIST/SEMATECH e-Handbook－Conditional Probability", "https://www.itl.nist.gov/div898/handbook/eda/section3/eda361.htm", "機率概念與以事件相對頻率估計機率的基礎"),
    ],
}

DRAFTS[42] = {
    "summary": "正確答案是 B。附表中三個 Linear 層合計約 123.64M 參數，遠高於 13 個卷積層約 14.71M；ReLU 與池化層則沒有可學習參數。",
    "concept": (
        "官方附圖使用 torchvision VGG16 並以輸入 3×150×150 產生 summary。最後"
        "AdaptiveAvgPool2d 固定輸出 512×7×7=25,088 個值，第一個 Linear 將其連到"
        "4,096 單元，參數為 25,088×4,096+4,096=102,764,544；第二與第三 Linear "
        "又分別有 16,781,312 與 4,097,000。全連接層因每個輸入連到每個輸出，儲存"
        "大量權重；卷積核則在空間位置共享。參數量與 FLOPs 要分開：參數多不代表"
        "運算量必然最大。"
    ),
    "answerReason": (
        "由附表直接相加即可看出 Linear 類別占 VGG16 約 138.36M 總參數中的絕大多數，"
        "因此 B 正確；ReLU、MaxPool、AdaptiveAvgPool 的表列 Param # 都是 0。"
    ),
    "optionAnalysis": {
        "A": "VGG16 的 13 個 Conv2d 雖有多組 3×3 kernel，但空間位置共享同一權重；合計約 14.7M，遠少於第一個 Linear 單層約 102.8M。",
        "B": "正確。三個 Linear 參數約為 102.76M、16.78M、4.10M，合計約 123.64M，約占總參數 89%，是四類中最多。",
        "C": "ReLU 逐元素套用 max(0,x)，沒有 kernel、weight 或 bias；附表每個 ReLU 的 Param # 都為 0，因此不可能最多。",
        "D": "MaxPool 與 AdaptiveAvgPool 依固定規則彙整局部或目標尺寸，不學習權重；附表亦顯示 Param # 為 0。",
    },
    "trap": "參數量主要影響模型檔與權重記憶體，運算量還要乘上每個權重被使用的空間位置次數。VGG16 是『FC 參數多、Conv FLOPs 多』的典型。",
    "references": [
        exam_ref(42, "11-13"),
        ref("torchvision source－VGG", "https://docs.pytorch.org/vision/stable/_modules/torchvision/models/vgg.html", "VGG features、AdaptiveAvgPool2d((7,7)) 與三層 classifier Linear 的官方實作"),
        ref("Very Deep Convolutional Networks for Large-Scale Image Recognition", "https://arxiv.org/abs/1409.1556", "VGG16 架構：13 個卷積層加 3 個全連接層"),
    ],
}

DRAFTS[43] = {
    "summary": "正確答案是 A。卷積核參數雖被共享，但會在大量空間位置反覆執行乘加；VGG16 的主要 FLOPs 因而集中在多層高解析度 Conv2d。",
    "concept": (
        "卷積層計算量約與 H_out×W_out×C_out×K_h×K_w×C_in 成正比；同一個 kernel "
        "在每個輸出位置都要做 dot product。早期 VGG feature maps 可達 150×150、"
        "75×75 等尺寸，所以少量共享參數會被重用成大量 operations。Linear 的 FLOPs "
        "大致等於輸入×輸出，只執行一次矩陣向量乘法；它的權重多、記憶體大，但在"
        "此架構的總運算仍低於所有卷積。ReLU 和 pooling 主要是逐元素比較／彙整，"
        "計算量也較小。FLOP 工具可能把一次 multiply-add 計為一或兩 FLOPs，排名不受影響。"
    ),
    "answerReason": (
        "A 正確區分『權重被儲存幾次』與『權重被使用幾次』：Conv 權重在每個空間"
        "位置重複使用，累積 FLOPs 最大；Linear 則是參數量最大。"
    ),
    "optionAnalysis": {
        "A": "正確。每層卷積要在整張 feature map 的大量位置，對每個輸出通道執行 kernel dot product；13 層累積後占 VGG16 大部分乘加運算。",
        "B": "Linear 權重多且占模型檔大部分，但每次前向只執行一個矩陣乘法，沒有 H×W 空間位置的重複套用，因此參數最多不等於 FLOPs 最多。",
        "C": "ReLU 對每個 activation 做一次簡單比較／截斷，操作數隨元素數成長，但每元素成本遠低於卷積的多通道 kernel 乘加。",
        "D": "Pooling 在局部窗口取最大或平均，不包含跨所有輸入／輸出通道的乘加；其計算通常遠少於相鄰卷積層。",
    },
    "trap": "別用 Param # 表格直接猜 FLOPs。卷積的每個參數會跨空間重用很多次，因此可呈現『參數較少、運算較多』。",
    "references": [
        exam_ref(43, "11-13"),
        ref("Very Deep Convolutional Networks for Large-Scale Image Recognition", "https://arxiv.org/abs/1409.1556", "VGG16 由多個 3×3 卷積堆疊構成，卷積特徵抽取占主要計算"),
    ],
}

DRAFTS[44] = {
    "summary": "正確答案是 D。官方 summary 顯示 VGG16 共有 13 個 Conv2d 與 3 個 Linear，總參數 138,357,544，與經典 VGG16 架構一致。",
    "concept": (
        "官方附表把 VGG16 features、avgpool 與 classifier 完整列出：Conv2d 編號 1、3、"
        "6、8、11、13、15、18、20、22、25、27、29，共 13 層；Linear-33、36、39 共"
        "3 層，所以名稱中的 16 指這 16 個有可學習權重的層。MaxPool 後雖為 512×4×4，"
        "AdaptiveAvgPool2d 接著輸出 512×7×7，第一 Linear 輸入是 25,088。Param # 已"
        "包含 bias，例如 25,088×4,096+4,096=102,764,544。summary 的 estimated size "
        "只是特定前向／反向與權重估算，未完整涵蓋 optimizer state、所有 framework "
        "workspace 及不同 batch，不能當訓練 GPU 下限。"
    ),
    "answerReason": (
        "D 可由附表逐層計數及 Total params 行直接驗證。A 忽略 adaptive pooling 把 4×4"
        "改為 7×7，B 的參數公式漏看 bias 已計入，C 則過度解讀估算記憶體。"
    ),
    "optionAnalysis": {
        "A": "MaxPool2d-31 先得到 512×4×4，但下一個 AdaptiveAvgPool2d-32 明確輸出 512×7×7；攤平後是 25,088，不是 8,192。",
        "B": "102,764,544 正好等於 25,088×4,096 個 weights 加 4,096 個 bias，故附表 Param # 已含偏差，不是只列權重。",
        "C": "624.98 MB 沒有完整計入 optimizer moments、所有 gradients、allocator overhead、temporary workspace 與不同 batch activations；1 GB GPU 不能據此保證可訓練。",
        "D": "正確。附表可數得 13 個 Conv2d、3 個 Linear，Total params 行為 138,357,544，約 138.36M，完整符合 VGG16。",
    },
    "trap": "閱讀 summary 要沿資料流看，不可跳過 AdaptiveAvgPool。另記得 Param # 通常是 weight+bias；estimated total size 也不是 optimizer 完整訓練記憶體。",
    "references": [
        exam_ref(44, "11-13"),
        ref("torchvision source－VGG", "https://docs.pytorch.org/vision/stable/_modules/torchvision/models/vgg.html", "VGG 的 AdaptiveAvgPool2d((7,7))、classifier Linear(512×7×7,4096) 及 vgg16 configuration"),
    ],
}

DRAFTS[45] = {
    "summary": "正確答案是 B。程式碼 B 只將 `model.features.parameters()` 設為不需梯度，保留整個 classifier 可訓練，並把最後 `classifier[6]` 換成 10 類輸出層。",
    "concept": (
        "torchvision VGG 將卷積 backbone 放在 `model.features`，三層全連接分類器放在"
        "`model.classifier`，最後一層索引為 6。凍結參數需逐一設定 `param.requires_grad=False`；"
        "之後 optimizer 只傳入仍 requires_grad 的參數。若目標是凍結卷積、微調 classifier，"
        "就迭代 `model.features.parameters()`，再替換最後 Linear 的 out_features。只寫"
        "`model.requires_grad=False` 不會遞迴設定各 Parameter；而凍結整個 model 再換最後"
        "層則是另一種『只訓練最末層』策略，不等於讓整個 classifier 重新訓練。"
    ),
    "answerReason": (
        "依題目用語『凍結卷積層、只訓練最後全連接層（classifier）』及官方答案，B "
        "精確鎖定 features 並保留 classifier trainable，最後將 1,000 類換為 10 類。"
    ),
    "optionAnalysis": {
        "A": "它迭代 model.parameters() 凍結所有既有 features 與 classifier，再新建的 classifier[6] 會預設可訓練；此法只訓練新末層，並非題目／官方答案所指凍結卷積而微調 classifier 整體。",
        "B": "正確。只遍歷 model.features.parameters() 並關閉梯度，卷積 backbone 被凍結；classifier 前兩個 Linear 仍可訓練，新建 classifier[6] 也可訓練且輸出 10 類。",
        "C": "它凍結 `model.classifier.parameters()`，正好把題目要訓練的全連接分類器關閉；雖新替換最後層可訓練，但卷積 features 仍全部更新，方向與要求相反。",
        "D": "將 `model.requires_grad=False` 只是替 Module 物件新增／修改普通屬性，不會遞迴改變其中每個 Parameter 的 requires_grad；卷積仍會產生梯度，因此不正確。",
    },
    "trap": "PyTorch 要凍結的是每個 Parameter 的 `requires_grad`，不是 Module 上同名屬性。也要先辨認 `features` 是卷積 backbone、`classifier` 是 FC head。",
    "editorialNote": "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。A 先凍結所有舊參數再替換末層，確實可達成『只訓練新最後一層』；B 則是凍結卷積、訓練整個 classifier。題幹將『最後全連接層(classifier)』用語混在一起，本站依官方 B 解作訓練 classifier 模組。",
    "references": [
        exam_ref(45, "13-14"),
        ref("PyTorch Tutorial－Transfer Learning for Computer Vision", "https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html", "凍結 pretrained network 的 requires_grad 並替換最後 fully connected layer 的 transfer learning 流程"),
        ref("torchvision source－VGG", "https://docs.pytorch.org/vision/stable/_modules/torchvision/models/vgg.html", "VGG `features` 與 `classifier` Sequential 結構，末層索引與輸入維度"),
    ],
}

DRAFTS[46] = {
    "summary": "正確答案是 B。附圖的 `pca = PCA()` 保留全部主成分，transform 後再 inverse_transform 幾乎重建原含噪資料；需在程式碼 B 設較小 `n_components` 才會丟棄低變異噪聲方向。",
    "concept": (
        "官方題組先用 `np.random.normal(digits.data, 4)` 在 64 維手寫數字加入噪聲，"
        "再依序執行 `PCA()`、fit、transform、inverse_transform。PCA 降噪的假設是信號"
        "集中在前幾個高變異 principal components，雜訊較分散在後段；只有保留部分"
        "成分，inverse transform 才會以低秩近似重建。`PCA()` 預設 n_components=None，"
        "保留 min(n_samples,n_features) 全部成分，沒有資訊瓶頸，因而也沒有預期降噪。"
        "成分數應以解釋變異、交叉驗證與視覺品質選擇，太少會抹掉筆畫。"
    ),
    "answerReason": (
        "需要修改的是建立 PCA 物件的程式碼 B，例如 `PCA(n_components=20)` 或合理"
        "變異比例。A 只是 import，C/D/E 的 fit-transform-inverse 流程本身正確。"
    ),
    "optionAnalysis": {
        "A": "`from sklearn.decomposition import PCA` 正確匯入類別，與是否保留全部成分無關；修改 import 不能建立降維資訊瓶頸。",
        "B": "正確。應將 `pca = PCA()` 改為指定較小 `n_components`；只保留主要 directions 後，低變異成分在 inverse transform 時不會被重建，才形成降噪。",
        "C": "`pca.fit(noisy)` 以 noisy 資料估計平均與 principal axes，是標準流程；若有乾淨訓練基準可改以其 fit，但題目程式失效的直接原因不是此行。",
        "D": "`pca.transform(noisy)` 將影像投影到主成分座標，正是降維步驟；是否真的降維由建立 PCA 時的 n_components 決定。",
    },
    "trap": "PCA 不是呼叫 fit 就自動降噪；若所有 components 都保留，正反轉換近似 identity。降噪來自捨棄部分成分，而不是 inverse_transform 本身。",
    "references": [
        exam_ref(46, "14-15"),
        ref("scikit-learn API－PCA", "https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html", "n_components=None 保留 min(n_samples,n_features) 個成分；transform 與 inverse_transform 的低維投影及重建"),
        ref("scikit-learn Example－Faces recognition using eigenfaces and SVMs", "https://scikit-learn.org/stable/auto_examples/applications/plot_face_recognition.html", "以有限 principal components 建立影像低維表示的官方示例"),
    ],
}

DRAFTS[47] = {
    "summary": "正確答案是 B。程式碼 A 與 C 都以 KNN、digits 全資料及合法的 multiclass accuracy scoring 執行交叉驗證；B、D 使用預設 binary F1，對十類目標會報錯。",
    "concept": (
        "附圖四段都建立 `KNeighborsClassifier(n_neighbors=3)`。A 使用顯式"
        "`StratifiedKFold(n_splits=5, shuffle=True)` 與 `scoring='accuracy'`；C 以 `cv=5`，"
        "對 classifier 會採 stratified folds，亦用 accuracy，兩者都可輸出平均準確率。"
        "B、D 將 scoring 設為 `'f1'`；scikit-learn 的 f1 scorer 預設 average='binary'，"
        "digits 目標有 0-9 十類，會出現 multiclass target 不支援 binary average 的錯誤。"
        "若改成 `'f1_macro'` 或 `'f1_weighted'` 才可執行，但那輸出的是 F1 不是題目要求的 accuracy。"
    ),
    "answerReason": (
        "A、C 的 API 參數與評分指標均能正確完成五折 KNN accuracy；因此包含這兩段"
        "且不含 B、D 的組合是選項 B。"
    ),
    "optionAnalysis": {
        "A": "把四段全選會包含程式 B、D；兩者的 `scoring='f1'` 是二元 F1 scorer，digits 為多類，執行時各 fold scoring 失敗，不能算全部正確。",
        "B": "正確。程式 A 明確使用 StratifiedKFold+accuracy，程式 C 用 cv=5+accuracy；兩者都會讓 cross_val_score 完成並讓 `scores.mean()` 輸出平均準確率。",
        "C": "程式 B 與 A 的差別是 scoring 改成 `'f1'`；對多類 digits 未指定 macro/weighted averaging 會報錯，且即使修正也不是輸出 accuracy，因此 A+B 不成立。",
        "D": "程式 C 可行，但 D 同樣使用不適用多類預設的 `'f1'`，所以 C+D 不是兩段皆正確的組合。",
    },
    "trap": "`f1`、`f1_macro`、`f1_weighted` 是不同 scorer。多類問題不能直接用預設 binary `f1`；題目又明確要求『準確率』，最直接應用 accuracy。",
    "references": [
        exam_ref(47, "15-16"),
        ref("scikit-learn API－cross_val_score", "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html", "cv 為整數時 classifier 使用 StratifiedKFold；scoring 可指定 estimator 評估指標"),
        ref("scikit-learn User Guide－String name scorers", "https://scikit-learn.org/stable/modules/model_evaluation.html#string-name-scorers", "accuracy、f1、f1_macro、f1_weighted 等 scorer 名稱及多類平均方式"),
    ],
}

DRAFTS[48] = {
    "summary": "正確答案是 C。敘述 A 正確：減去各欄平均會使訓練特徵均值為 0；敘述 D 也符合題意：尺度標準化可改善最佳化數值條件，降低梯度尺度極端的風險。",
    "concept": (
        "附圖先做 `X_train -= X_train.mean(axis=0)`，使每欄中心化；再除以中心化後的"
        "`X_train.std(axis=0)`，使非零變異欄的標準差成為 1，不是 0。這是 z-score "
        "standardization，結果不限制在 [0,1]；那是 MinMax scaling。標準化讓不同量綱"
        "特徵對 loss landscape 與梯度貢獻較可比，可提升訓練穩定，但不是 feature selection。"
        "附圖另把 X_test 用自身平均與標準差處理，實務上不理想：應保存 train mean/std "
        "並套到 test，否則前處理映射不一致且使用測試分布資訊。"
    ),
    "answerReason": (
        "六個敘述中 A 正確、B 把標準差誤寫成 0、C 混同 min-max、E 混同 feature selection、"
        "F 把整個矩陣錯誤替換成標準差向量。官方把 D 視為正確，因此正確組合 A+D 是 C。"
    ),
    "optionAnalysis": {
        "A": "A 選項組合含 A、B、C、D，但 B、C 錯：除以標準差後標準差為 1，且 z-score 不會把所有值限制在 0 到 1，因此不能選。",
        "B": "A 雖正確，E 錯誤；標準化保留所有原特徵，只改中心與尺度，沒有篩除任何欄位，屬 preprocessing／feature scaling 而非 selection。",
        "C": "正確。A 的中心化使每個訓練特徵平均為 0；D 在題目脈絡下指標準化改善尺度與梯度數值條件，減少極端梯度造成不穩的風險。",
        "D": "A 正確但 C、F 都錯；F 的指定會把 X_train 直接變成一列標準差而丟掉樣本資料，正確作法是 `(X-mean_train)/std_train`，測試集也用 train statistics。",
    },
    "trap": "標準化是 mean 0、std 1；正規化到 [0,1] 是另一種縮放。最重要的實務陷阱是 test 不能自行 fit scaler，必須沿用 training statistics。",
    "editorialNote": "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。D『防止梯度爆炸或消失』語氣過強：輸入標準化可改善數值條件與降低風險，但不能保證防止深層網路的 exploding／vanishing gradients。附圖對 X_test 使用自身統計亦非最佳實務。",
    "references": [
        exam_ref(48, "16-17"),
        ref("scikit-learn API－StandardScaler", "https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html", "z=(x-u)/s；在訓練集估計 mean/std，後續 transform 沿用相同統計"),
        ref("scikit-learn User Guide－Data leakage", "https://scikit-learn.org/stable/common_pitfalls.html#data-leakage", "前處理只應以訓練資料 fit，再對測試資料 transform"),
    ],
}

DRAFTS[49] = {
    "summary": "正確答案是 C。輸入有 9 個特徵，第一個 Dense(10) 參數為 9×10+10=100；第二個 Dense(10) 接收 10 維，參數為 10×10+10=110。",
    "concept": (
        "官方 Titanic 題組把九個欄位切成 `X_train = dataset_train[:, 0:9]`，所以"
        "`Input(shape=(X_train.shape[1],))` 是 9 維。Keras Dense 的 kernel shape 為"
        "(input_dim, units)，另有每個 unit 一個 bias，因此 Param #=(input_dim+1)×units。"
        "第一層 (9+1)×10=100，第二層 (10+1)×10=110，最後 Dense(1) 為 (10+1)×1=11，"
        "與附圖 summary 的 11 一致。ReLU 是 max(0,x)，題目 A 顯示的 1/(1+e^-x) 是"
        "sigmoid；單一 sigmoid 配 binary crossentropy 用於二元分類，多類互斥通常用 softmax。"
    ),
    "answerReason": (
        "C 的兩個空格數值都能由 Dense 公式及附圖九特徵直接算出。B 對調兩層，A 把"
        "sigmoid 公式標成 ReLU，D 則把二元輸出用途說成一般多類分類。"
    ),
    "optionAnalysis": {
        "A": "選項畫出的 f(x)=1/(1+e^-x) 是 logistic sigmoid；ReLU 的定義是 max(0,x)，負值輸出 0、正值保持原值，因此公式辨識錯誤。",
        "B": "它把參數量順序顛倒。第一 Dense 的 input_dim 是九個 Titanic 特徵，所以是 100；只有第二 Dense 的 input_dim 才是前層 10 units，得到 110。",
        "C": "正確。第一層含 90 個 kernel weights 加 10 bias=100；第二層含 100 個 weights 加 10 bias=110，與 Keras Dense 參數計算一致。",
        "D": "單一 sigmoid 通常輸出二元事件機率或多標籤中每一類獨立機率；互斥多類分類通常以 units=類別數的 softmax，不是單一 sigmoid。",
    },
    "trap": "Dense 參數別忘 bias：`input_dim×units + units`。Activation 公式也要分清：sigmoid 是 S 曲線，ReLU 是 max(0,x)，softmax 才常用於互斥多類輸出。",
    "references": [
        exam_ref(49, "16-18"),
        ref("Keras API－Dense layer", "https://keras.io/api/layers/core_layers/dense/", "Dense 計算 activation(dot(input,kernel)+bias)，kernel 形狀由 input dimension 與 units 決定"),
        ref("Keras API－Layer activation functions", "https://keras.io/api/layers/activations/", "ReLU、sigmoid 與 softmax 的定義及輸出行為"),
    ],
}

DRAFTS[50] = {
    "summary": "正確答案是 C。附圖訓練損失為藍色實線，所以空格 1 是 `b-`；驗證損失為紅色虛線，所以空格 2 是 `r--`，正確敘述為 A、D。",
    "concept": (
        "Matplotlib 的 format string 可組合 color 與 linestyle：`b` 是 blue、`r` 是 red，"
        "`-` 是 solid、`--` 是 dashed。附圖 legend 與曲線顯示 Training Loss 藍色實線、"
        "Validation Loss 紅色虛線，因此兩個 fmt 分別是 `b-` 與 `r--`。曲線趨勢上，"
        "training loss 從約 0.66 持續降到 0.40；validation loss 先降到約 0.46 後波動"
        "停滯，兩者 gap 擴大，呈現 overfitting。E 說驗證損失下降更明顯，與圖完全相反。"
    ),
    "answerReason": (
        "A、D 分別精確對應兩條曲線的顏色與線型，組合成選項 C。B 把驗證畫成藍色"
        "虛線，C 把訓練畫成紅色實線，E 又誤讀損失趨勢。"
    ),
    "optionAnalysis": {
        "A": "選項 A 組合為 B、C：`b--` 會畫藍色虛線，不是圖中的紅色驗證線；`r-` 又會把訓練線畫成紅色實線，兩者都對不上。",
        "B": "此組雖含正確的 A、D，卻多含 C；空格 1 若用 `r-`，Training Loss 會成紅色，與附圖藍色實線及 legend 不符，所以整組不能選。",
        "C": "正確。`b-` 產生藍色實線對應 Training Loss，`r--` 產生紅色虛線對應 Validation Loss，因此正確敘述恰為 A、D。",
        "D": "C、D、E 中只有 D 正確；C 顏色錯，E 也錯，因為圖中訓練損失持續下降且總降幅更大，驗證損失約在 0.45 附近停滯。",
    },
    "trap": "fmt 字串先讀顏色再讀線型：b-=藍實線、r--=紅虛線。判讀 loss curve 時要看數值方向，validation 趨平而 training 繼續降是過擬合，不是驗證改善更多。",
    "references": [
        exam_ref(50, "18-19"),
        ref("Matplotlib Documentation－plot format strings", "https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html", "fmt `[marker][line][color]` 的顏色字碼 b/r 與線型 -/-- 定義"),
        ref("Keras Guide－Training & evaluation with the built-in methods", "https://keras.io/guides/training_with_built_in_methods/", "fit 的 validation_split 與 History 中 training／validation metrics 的使用"),
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
