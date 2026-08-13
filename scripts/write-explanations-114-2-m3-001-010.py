"""Write draft explanations for 114-2 intermediate subject three, Q1-Q10.

The script verifies official answers and refuses to overwrite reviewed work.
Run the draft validator before applying it to the shared question bank.
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


def exam_ref(number: int) -> dict:
    return {
        "title": "114 年第二次中級 AI 應用規劃師－機器學習技術與應用公告試題",
        "url": EXAM_PDF,
        "locator": f"第 {number} 題題幹、選項與官方答案",
        "checkedAt": CHECKED_AT,
    }


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


EXPECTED_ANSWER = {
    1: "B", 2: "C", 3: "C", 4: "B", 5: "A",
    6: "C", 7: "A", 8: "D", 9: "A", 10: "C",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[1] = {
    "summary": "正確答案是 B。交叉驗證以多次訓練／驗證切分模擬模型面對未觀察資料的表現，可估計泛化誤差及不同切分下的穩定性。",
    "concept": (
        "模型在訓練資料表現好不代表能泛化。Cross-Validation 將資料輪流分成訓練折"
        "與驗證折，每次只用訓練折擬合，再以未參與擬合的驗證折計算指標，最後彙整"
        "平均與變異。題目特別提到不同月份，資料有時間順序時不能隨機打散，否則會"
        "用未來月份訓練、過去月份驗證而洩漏；應採 rolling／TimeSeriesSplit，讓每折"
        "只用過去預測未來。F、t、卡方檢定回答特定統計假設，不是一般模型泛化評估流程。"
    ),
    "answerReason": (
        "B 唯一以重複的外樣本驗證直接估計模型對未觀察資料的預測表現。透過各折"
        "分數可觀察平均效能及月份間波動；若資料依月份排序，應使用保留時間順序的"
        "交叉驗證版本。"
    ),
    "optionAnalysis": {
        "A": "F 檢定可比較變異數、迴歸模型或巢狀模型的特定假設，但它不會自動建立多個未觀察月份的訓練／驗證流程，也無法單獨估計部署後泛化表現。",
        "B": "正確。交叉驗證在多個資料切分上反覆擬合與評估，驗證樣本每次未參與訓練，可估計外樣本分數與穩定性；月份資料應採時間序列切分避免未來資訊洩漏。",
        "C": "配對 t 檢定比較同一受試單位兩次量測或配對差值的平均是否為零，可用於後續比較兩模型分數，但本身不是訓練與評估模型泛化能力的方法。",
        "D": "卡方檢定常檢驗類別變數獨立性或觀察次數是否符合期望分布；它不直接衡量銷售預測模型在未見月份的誤差與穩定性。",
    },
    "trap": "看到『不同月份』不能直接使用隨機 K-fold；仍選交叉驗證，但要用 time-aware split。統計顯著性檢定可輔助比較，不能取代外樣本預測評估。",
    "editorialNote": "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。題幹具月份順序，B 應具體落實為 rolling／TimeSeriesSplit，而非隨機 K-fold，否則可能發生未來資料洩漏。",
    "references": [
        exam_ref(1),
        ref("scikit-learn User Guide－Cross-validation", "https://scikit-learn.org/stable/modules/cross_validation.html", "以未參與擬合的資料評估模型泛化能力及交叉驗證基本流程"),
        ref("scikit-learn API－TimeSeriesSplit", "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html", "時間排序資料需避免用未來訓練、過去評估；每折以前段訓練、後段測試"),
    ],
}

DRAFTS[2] = {
    "summary": "正確答案是 C。L1 正則化在損失中加入參數絕對值總和，菱角狀約束常使部分最佳係數精確成為零，得到稀疏模型並兼具特徵選擇效果。",
    "concept": (
        "Lasso 解的是資料配適損失加 αΣ|w_j|。α 越大，非零係數付出的懲罰越高；"
        "L1 在零點不可微且其約束幾何有軸向尖角，最佳解容易落在座標軸上，使部分"
        "權重恰為零。相較之下，L2／Ridge 通常連續縮小係數但不精確歸零。稀疏性可"
        "簡化模型與選特徵，但高度相關特徵間 Lasso 可能任選其一，α 過大也會欠擬合；"
        "應以交叉驗證選正則強度並先處理特徵尺度。"
    ),
    "answerReason": (
        "C 描述 L1 最具代表性的效果：把部分參數壓到零，留下較少非零權重。其他"
        "選項不是正則化目標；增加參數與提高學習率甚至可能提高複雜度或使訓練不穩。"
    ),
    "optionAnalysis": {
        "A": "L1 懲罰不會新增模型參數，而是限制既有參數的絕對值總和；許多係數歸零後，有效使用的特徵與自由度通常減少，方向與選項相反。",
        "B": "梯度穩定與震盪主要由學習率、最佳化器、梯度裁剪與損失曲面影響；L1 的核心是複雜度懲罰與稀疏化，零點不可微反而需次梯度或專用 solver 處理。",
        "C": "正確。Lasso 對係數絕對值加總施加懲罰，使不重要特徵的係數可精確收斂為零，形成 sparse model，兼具變數選擇與降低複雜度的效果。",
        "D": "Learning rate 是最佳化步幅，與 L1 正則強度 α 是不同超參數；加入 L1 不會自動提高學習率，也不能以加快收斂作為其主要效果。",
    },
    "trap": "L1 對應『稀疏、可歸零』，L2 對應『平滑縮小、通常不歸零』。正則化強度與學習率也不能混為同一個參數。",
    "references": [
        exam_ref(2),
        ref("scikit-learn User Guide－Lasso", "https://scikit-learn.org/stable/modules/linear_model.html#lasso", "Lasso 估計 sparse coefficients，使用 L1 penalty，並可用於特徵選擇"),
    ],
}

DRAFTS[3] = {
    "summary": "正確答案是 C。非凸目標可能有多個局部極小值或鞍點，梯度式演算法的終點會受初始化與更新路徑影響，可能停在局部最優而非全域最優。",
    "concept": (
        "凸函數的任一局部極小值都是全域極小值；非凸函數沒有這項保證，其損失曲面"
        "可能包含多個 basin、local minima、saddle points 與平坦區。梯度下降只使用"
        "目前位置附近斜率，落入某個吸引區後可能收斂到該區的局部解，不同初始化可"
        "得到不同結果。動量、隨機 mini-batch、學習率排程與多次重新啟動可改善探索，"
        "但一般不能保證找到 global optimum。梯度消失、資料不足、過擬合都可能同時"
        "發生，卻不是『多個極值』最直接推出的情況。"
    ),
    "answerReason": (
        "題幹已指出非凸且存在多個極值點，這正是局部最佳化解不唯一、結果依初始"
        "位置而變的原因，因此 C 最直接。其餘選項需要網路深度、資料量或訓練與"
        "泛化落差等額外條件。"
    ),
    "optionAnalysis": {
        "A": "梯度消失通常來自深層連鎖導數、飽和啟用函數或長序列，使梯度接近零；非凸曲面可有梯度消失區，但『多個極值』本身不必然造成典型的 vanishing gradient。",
        "B": "資料過少是資料蒐集與樣本量問題，與目標函數是否凸沒有必然關係；相同資料量可形成凸或非凸最佳化問題。",
        "C": "正確。非凸目標存在多個局部極小值時，沿局部梯度更新可能在其中一個 basin 收斂，不同初始化與隨機訓練順序因此得到不同最佳化結果。",
        "D": "過擬合是訓練表現好、未見資料表現差的泛化問題，取決於模型容量、正則化與資料；找到局部或全域訓練損失解不等於必然過擬合。",
    },
    "trap": "Optimization 問『有沒有把訓練目標降好』，generalization 問『新資料表現好不好』。局部最優是前者；過擬合是後者，不能因都出現在訓練過程就混用。",
    "references": [
        exam_ref(3),
        ref("Deep Learning（Goodfellow, Bengio, Courville）－Optimization for Training Deep Models", "https://www.deeplearningbook.org/contents/optimization.html", "第 8 章討論非凸神經網路最佳化中的 local minima、saddle points 與初始化影響"),
    ],
}

DRAFTS[4] = {
    "summary": "正確答案是 B。該點既未達核心點的 MinPts 門檻，也不落在任何核心點的 ε 鄰域、無法密度可達，因此不屬任何群集，DBSCAN 會標為雜訊。",
    "concept": (
        "DBSCAN 以 ε 鄰域與 min_samples／MinPts 定義密度。核心點的鄰域樣本數達"
        "門檻；非核心點若位於核心點鄰域，可作為 border point 加入群集；剩餘無法"
        "由核心點密度可達的點標為 noise，常用標籤 −1。『自身鄰域不足』本身還不能"
        "立即判 noise，因為它仍可能是邊界點；必須再確認是否被任何核心點包含。"
        "題幹已明確排除這種情況，所以結論唯一。"
    ),
    "answerReason": (
        "題目完整給了 Noise 的兩項條件：不是核心點，也不是任一群集的邊界／密度"
        "可達點。因此 B 正確；A 與 D 不是 DBSCAN 的正式分類，C 則缺少被核心點"
        "鄰域涵蓋的必要條件。"
    ),
    "optionAnalysis": {
        "A": "鄰近點不是 DBSCAN 結果中的標準點型；所有 ε 範圍內的樣本都可口語稱鄰居，但演算法最終關心 core、border 與 noise，不能用此詞取代分類。",
        "B": "正確。鄰域點數不足且不屬任何核心點鄰域，表示它無法從群集核心密度可達，DBSCAN 會把它排除於群集並標記為 noise／outlier。",
        "C": "邊界點自身不是核心點，但必須落在某個核心點的 ε 鄰域，因此仍屬該群集；題幹特別說未被任何核心點鄰域包含，已排除此可能。",
        "D": "潛在點不是 DBSCAN 定義的正式結果類型，也沒有對應的判定規則；演算法完成後，不能成為 core 或 border 的點就是 noise。",
    },
    "trap": "『不是核心點』不等於一定是雜訊，還要再問是否在核心點鄰域內；在就是 border，不在才是 noise。這是本題最重要的判斷順序。",
    "references": [
        exam_ref(4),
        ref("scikit-learn User Guide－DBSCAN", "https://scikit-learn.org/stable/modules/clustering.html#dbscan", "核心樣本、非核心樣本、群集擴張及無法歸入群集的 noise 定義"),
    ],
}

DRAFTS[5] = {
    "summary": "正確答案是 A。第一層卷積核在影像局部視野上滑動，自動學得邊緣、方向與簡單紋理等低階局部特徵，供後續層逐步組合成瑕疵模式。",
    "concept": (
        "Convolutional layer 使用一組可學習 kernel，在影像各位置的 local receptive "
        "field 做加權和並產生 feature maps。相同 kernel 在所有位置共享參數，因此能"
        "偵測某種局部模式不論它出現在哪裡。靠近輸入的卷積層通常學到邊緣、角點、"
        "色彩與紋理，深層再組合成零件形狀與瑕疵。降低空間尺寸主要由 stride>1 或"
        "pooling 達成，並非每個第一卷積層的必然功能；最終分類則通常由後段聚合與"
        "輸出層負責。"
    ),
    "answerReason": (
        "A 正確描述第一卷積層的核心工作：從原始像素局部區域學得 feature detector。"
        "其他選項把可選的下採樣、模型容量或最後分類頭的角色誤當成第一層卷積的"
        "主要職責。"
    ),
    "optionAnalysis": {
        "A": "正確。第一層 kernel 對小範圍像素做卷積，訓練後會對特定邊緣方向、顏色差與紋理產生反應，形成可供後續層組合的局部 feature maps。",
        "B": "卷積若使用 stride=1 與適當 padding，可以保持影像寬高；降維常由 pooling 或 stride convolution 負責。因此卷積層可能下採樣，但不是第一層最主要且必然的功能。",
        "C": "卷積的參數共享恰好比同尺寸全連接層少很多參數；增加 filter 數會增加容量，但設計目的不是為了單純增加神經元與參數。",
        "D": "整合高階特徵並輸出最終類別通常在 CNN 後端以 global pooling、fully connected 與 softmax 等完成；第一層只建立初步局部表示，不會直接完成瑕疵分類。",
    },
    "trap": "卷積與 pooling 不同：卷積主要『學特徵』，pooling 主要『彙整／降採樣』。若卷積 stride 大於一也會降維，但那是設定效果，不是第一層的定義。",
    "references": [
        exam_ref(5),
        ref("Convolutional Networks and Applications in Vision", "https://proceedings.mlr.press/v9/le-cun10a.html", "卷積網路以 local connections 與 shared weights 擷取多層次影像特徵"),
    ],
}

DRAFTS[6] = {
    "summary": "正確答案是 C。CNN 只連接局部感受野，並在不同位置重用同一組卷積核；相較把每個像素連到每個神經元的 FCNN，大幅減少參數與乘加運算。",
    "concept": (
        "影像具有局部相關與平移結構。Local receptive field 讓一個輸出只看鄰近像素，"
        "parameter sharing 讓同一 filter 掃描整張圖；例如 3×3×C 的 kernel 參數量不"
        "隨影像位置數成長。FCNN 若把 H×W×C 像素全部連到下一層每個單元，權重矩陣"
        "會非常大，忽略空間鄰近關係。CNN 因參數少而更節省記憶體與運算，也常有較好"
        "樣本效率。它能學一定程度的平移等變性，但旋轉、尺度不變性通常需資料增強"
        "或特殊架構，並非自動完整具備。"
    ),
    "answerReason": (
        "C 精確指出 CNN 相對全連接網路的結構性效率來源：稀疏局部連接加權重共享。"
        "B 雖描述端到端學習優點，但 FCNN 也能直接吃像素；A 過度宣稱不變性，D 則"
        "錯稱 CNN 不使用啟用函數。"
    ),
    "optionAnalysis": {
        "A": "標準 CNN 對平移較有等變性，配合 pooling 可取得有限穩健性，但不會自動對任意旋轉與縮放不變；通常仍需旋轉／尺度增強、spatial transformer 或特定等變架構。",
        "B": "CNN 可端到端學特徵，確實減少手工 feature engineering；但 FCNN 也能直接以像素訓練，真正造成參數與運算差距的是連接型態，不只是省略人工步驟。",
        "C": "正確。局部感受野避免每個單元連到全圖，參數共享讓同一 filter 在所有空間位置使用；兩者使參數量遠低於展平影像後的 fully connected layer。",
        "D": "CNN 通常在卷積後使用 ReLU、GELU 等 activation 以建立非線性；若完全捨棄啟用函數，多層線性卷積仍等價於單一線性轉換，表達能力反而受限。",
    },
    "trap": "端到端學特徵是 CNN 的優點，但題目問『效率主要原因』，要回答 local connectivity 與 weight sharing。也不要把平移等變性誤寫成完整旋轉尺度不變。",
    "references": [
        exam_ref(6),
        ref("Convolutional Networks and Applications in Vision", "https://proceedings.mlr.press/v9/le-cun10a.html", "卷積架構利用局部連接、共享權重與 pooling 建立高效率階層式影像表示"),
    ],
}

DRAFTS[7] = {
    "summary": "正確答案是 A。電力需求是有時間順序的序列，未來七天會受先前負載、週期與長期趨勢影響；LSTM 的記憶單元與閘門適合建模跨時間依賴。",
    "concept": (
        "LSTM 是 recurrent neural network 的一種，透過 cell state、input gate、forget "
        "gate 與 output gate 控制資訊寫入、保留與讀出，以緩解普通 RNN 在長序列的"
        "梯度消失問題。它適用於負載、需求、語音與文字等有順序且目前狀態依賴過去"
        "的資料。多步電力預測可用過去負載及天氣等序列輸出未來七天；仍需使用依"
        "時間切分的驗證避免洩漏。影像物件辨識通常用 CNN／Vision Transformer，"
        "分群用 clustering，降維用 PCA 或 autoencoder。"
    ),
    "answerReason": (
        "A 是四項中唯一明確的時間序列預測，近期與較久以前的負載模式都可能影響"
        "未來需求，符合 LSTM 設計目的。其他選項的核心分別是空間視覺、無監督分群"
        "與表示壓縮，不需要循環記憶。"
    ),
    "optionAnalysis": {
        "A": "正確。七天電力需求具有小時、日與週期依賴，LSTM 可逐時讀入歷史序列並以 gated memory 保留有用狀態，再用於單步或多步未來負載預測。",
        "B": "單張監視影像中的物件類別與位置主要取決於空間局部特徵，CNN、object detector 或 Vision Transformer 更合適；除非題目要求跨影片影格追蹤，否則不需 LSTM。",
        "C": "依相似特徵自動分群是無標註 clustering 任務，常用 K-means、DBSCAN 或階層分群；LSTM 是序列表示模型，本身不直接決定群集歸屬。",
        "D": "高維感測器壓縮屬降維／表示學習，可用 PCA 或 autoencoder；若是壓縮一段時間序列可加入 LSTM encoder，但選項沒有序列依賴，並非最典型用途。",
    },
    "trap": "不要看到感測器就選 LSTM，關鍵是資料是否有『順序與跨時間依賴』。同樣地，影片才可能同時需要 CNN 與 LSTM，單張影像辨識不必。",
    "references": [
        exam_ref(7),
        ref("Long Short-Term Memory", "https://www.bioinf.jku.at/publications/older/2604.pdf", "原始 LSTM 論文：以記憶單元與乘法閘門處理長時間延遲及梯度衰減"),
    ],
}

DRAFTS[8] = {
    "summary": "正確答案是 D。決策樹在每個節點比較候選特徵分裂後的不確定性下降量；以熵作 impurity 時，父節點熵減去子節點加權熵就是資訊增益。",
    "concept": (
        "Entropy H(Y)=−Σp_k log p_k 衡量類別混雜程度。候選分裂的 Information Gain "
        "是 H(parent) 減去各 child entropy 的樣本數加權平均；增益越大，代表分裂後"
        "子節點越純、該特徵更能降低分類不確定性。分類決策樹遞迴選擇高增益分裂，"
        "直到停止條件，再以葉節點做預測。實作也常用 Gini impurity；高基數類別可能"
        "使未校正資訊增益偏好過多切分，需要 gain ratio、正則限制或驗證。"
    ),
    "answerReason": (
        "D 描述的遞迴分裂正是資訊增益作為 split criterion 的使用位置。A 用係數"
        "懲罰篩選，B 以梯度學神經表示，C 以 margin 與 kernel 決策，三者的訓練目標"
        "都不是節點熵下降。"
    ),
    "optionAnalysis": {
        "A": "L1 線性模型以損失加係數絕對值懲罰，使部分係數歸零；它不建立樹節點，也不在每一步計算父子類別熵，因此不是資訊增益的主要架構。",
        "B": "深度神經網路以 activation 建立非線性表示，再以反向傳播最佳化損失；雖可用資訊論損失，但一般不靠逐特徵 entropy gain 遞迴建立分類規則。",
        "C": "SVM 尋找最大 margin 超平面，kernel 用內積隱式映射高維空間；特徵選擇與決策邊界來自 margin objective，而非節點分裂的 information gain。",
        "D": "正確。分類樹對每個候選特徵與閾值計算分裂後子節點 impurity，使用 entropy criterion 時選擇 information gain 最大者，再對子節點遞迴重複。",
    },
    "trap": "Cross-entropy 名稱也含 entropy，但資訊增益題的關鍵詞是『特徵分裂、父節點、子節點』，對應 decision tree，不是所有使用熵概念的分類模型。",
    "references": [
        exam_ref(8),
        ref("scikit-learn User Guide－Decision Trees mathematical formulation", "https://scikit-learn.org/stable/modules/tree.html#mathematical-formulation", "分類樹以 entropy 或 log loss 衡量節點 impurity，選擇使子節點加權 impurity 最小的分裂"),
    ],
}

DRAFTS[9] = {
    "summary": "正確答案是 A。KNN 直接比較樣本距離，SVM 的 margin 與 RBF kernel 也受特徵尺度影響；若量綱差異大，數值較大的特徵會不成比例地主導模型。",
    "concept": (
        "假設年收入以百萬元、年齡以數十計，未縮放的 Euclidean distance 幾乎只反映"
        "收入差。Standardization 將各特徵轉為近似零平均、單位變異，Min-Max scaling "
        "則映射到固定範圍，使各維對距離有可比較貢獻。KNN 的鄰居完全由距離決定；"
        "SVM 的最佳化與 RBF kernel exp(−γ||x−x'||²) 同樣受尺度影響。Scaler 必須只在"
        "訓練折 fit，再 transform 驗證／測試，最好放進 Pipeline 防止資料洩漏。樹模型"
        "依單一特徵排序切分，通常較不敏感。"
    ),
    "answerReason": (
        "A 直接處理距離式模型的核心假設：各特徵尺度需可比較，避免大數值範圍遮蔽"
        "其他訊號。缺失值補齊與抽樣可能在特定資料需要，但不如縮放對 KNN、SVM "
        "普遍且直接；把連續特徵類別化還會損失資訊。"
    ),
    "optionAnalysis": {
        "A": "正確。標準化或其他適當縮放可防止量綱較大的特徵主導距離、RBF kernel 與 SVM regularization，讓模型依資訊而非單位大小決定鄰居或邊界。",
        "B": "離散化可處理非線性區間或增加可解釋性，但會丟失連續變化與引入人為切點；距離模型不要求所有連續特徵先改成類別，且類別距離需另行定義。",
        "C": "KNN 與多數 SVM 不能直接接受缺值，所以資料有 missing 時確實需補齊；但題目未說存在缺值，而所有具不同量綱的距離特徵都普遍需要縮放。",
        "D": "抽樣平衡針對類別不平衡，可能改善少數類學習；它不會改變各特徵的數值範圍，因此大尺度特徵仍會主導距離。",
    },
    "trap": "缺失值處理是『有缺值才做』，類別平衡是『分布不均才做』；feature scaling 則是距離式模型遇到不同量綱時的核心前處理。記得 scaler 不能先看完整資料。",
    "references": [
        exam_ref(9),
        ref("scikit-learn API－StandardScaler", "https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html", "若某特徵變異數量級遠大於其他特徵，可能主導 estimator objective；常見 RBF SVM 與線性模型假設尺度相近"),
        ref("scikit-learn User Guide－Importance of Feature Scaling", "https://scikit-learn.org/stable/auto_examples/preprocessing/plot_scaling_importance.html", "示例說明未縮放特徵如何主導 KNN 距離及影響模型結果"),
    ],
}

DRAFTS[10] = {
    "summary": "正確答案是 C。AutoML 適合在時間與專業人力有限時，自動化資料前處理、候選演算法與超參數比較，快速建立顧客流失模型基線。",
    "concept": (
        "AutoML 將重複性模型開發步驟自動化，例如資料切分、特徵轉換、模型家族與"
        "超參數搜尋、評估及產出可部署成品。它最有價值的情境是任務標準化、資料已"
        "有標籤、需要快速比較多個 baseline，且團隊缺乏足夠 ML 工程時間。AutoML "
        "不免除問題定義、資料品質、洩漏檢查、公平與部署監控；高度客製損失、特殊"
        "約束或法規模型通常需 custom training。已成熟固定的流程也未必值得更換。"
    ),
    "answerReason": (
        "C 同時具備 AutoML 的典型適用條件：標準的表格二元分類、急需比較多種模型、"
        "缺少專職工程師與時間。A、B 已有成熟流程或穩定模型，增益有限；D 需要精細"
        "控制，與 AutoML 的抽象化取向衝突。"
    ),
    "optionAnalysis": {
        "A": "已有資深團隊、完整 MLOps 與固定更新流程時，仍可用 AutoML 做基準或搜尋，但導入效益較小，還可能與既有治理及客製 pipeline 重複，不是最迫切情境。",
        "B": "長期穩定模型只需定期調參，可直接在既有流程做有限 hyperparameter tuning；重新用 AutoML 搜尋整套 pipeline 可能增加驗證與遷移成本，未必提升效率。",
        "C": "正確。顧客流失是常見 tabular classification，AutoML 可在有限時間自動試驗多種處理與模型並比較驗證指標，讓缺乏專職工程師的團隊快速取得可用 baseline。",
        "D": "信用風險模型若要求客製特徵、約束、可解釋性與細緻演算法控制，通常需 custom training 與專家治理；全自動搜尋可能無法滿足法規及業務限制。",
    },
    "trap": "AutoML 是加速器，不是『不用懂資料』。最適合標準任務的快速 baseline；需求越客製、風險越高、控制越細，越需要人工設計與獨立驗證。",
    "references": [
        exam_ref(10),
        ref("Google Cloud－Introduction to Vertex AI", "https://cloud.google.com/vertex-ai/docs/start/introduction-unified-platform", "AutoML 可在不寫訓練程式下訓練 tabular、image、video 模型；custom training 提供完整流程控制"),
        ref("Google Cloud－Choose a training method", "https://cloud.google.com/vertex-ai/docs/start/training-methods", "AutoML 適合以較少技術投入快速建立原型與探索資料；custom training 適合完整客製控制"),
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
