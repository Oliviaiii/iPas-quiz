"""Write draft explanations for 115-1 intermediate subject one, Q31-Q40.

This script updates only existing questions, verifies official answers, and
refuses to overwrite reviewed explanations.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-intermediate-1-ai-tech-planning"
AUTHOR = "Codex（AI 輔助初稿）"
AUTHORED_AT = "2026-08-12"
CHECKED_AT = "2026-08-12"
EXAM_PDF = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/115年第一次中級AI應用規劃師_"
    "第一科_人工智慧技術應用與規劃_公告試題_20260615003359.pdf"
)
DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def exam_ref(number: int) -> dict:
    return {
        "title": "115 年第一次中級 AI 應用規劃師－人工智慧技術應用與規劃公告試題",
        "url": EXAM_PDF,
        "locator": f"第 {number} 題題幹、選項與官方答案",
        "checkedAt": CHECKED_AT,
    }


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


EXPECTED_ANSWER = {
    31: "A", 32: "B", 33: "D", 34: "B", 35: "B",
    36: "A", 37: "A", 38: "D", 39: "A", 40: "D",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[31] = {
    "summary": "正確答案是 A。高維空間中的距離容易失去區辨力，使依鄰域半徑判斷密度的 DBSCAN 難以形成穩定群集。",
    "concept": (
        "DBSCAN 以半徑 ε 內的鄰居數判定核心點，再將密度相連的點擴展成群集。"
        "維度增加時，資料空間體積快速膨脹；若樣本量未同步增加，局部鄰域會變得"
        "稀疏，而且最近與較遠距離的差距可能縮小。此時單一 ε 很難同時區分群內"
        "與群外距離，許多點便可能達不到 MinPts 而被標為雜訊。"
    ),
    "answerReason": (
        "題目有 300 個特徵，且反覆調整 ε、MinPts 仍失效，最典型原因是 A 所述"
        "的維度詛咒與距離集中。B 把實務限制誤寫為完全不能處理，C、D 則把"
        "可能結果說成數學必然，均無法成立。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。高維會使固定半徑鄰域非常稀疏，且距離的相對差異變小；DBSCAN"
            "依距離與鄰居數估計密度，因此 ε 不易選定，核心點可能大量消失。"
        ),
        "B": (
            "DBSCAN 的定義沒有禁止高維輸入，軟體也可接受多維特徵。問題是常用"
            "距離度量在高維可能失去意義、索引效率下降，而不是演算法在維度超過"
            "某值後絕對無法執行。"
        ),
        "C": (
            "特徵數多不代表資料必然沒有群集；若資料位於低維流形、只有少數相關"
            "特徵，或經合適的特徵選擇與降維，仍可能存在清楚結構。此選項把風險"
            "誤寫成必然結論。"
        ),
        "D": (
            "核心點數由 ε、MinPts 與實際鄰域分布決定，沒有高維下必須少於某個"
            "數量的通用數學限制。高維造成的是距離與密度估計困難，不是直接限制"
            "核心點個數。"
        ),
    },
    "trap": (
        "『高維下效果常變差』不等於『DBSCAN 只能用於低維』。先指出距離集中與"
        "鄰域稀疏的機制，再考慮標準化、特徵選擇、降維或改用適合的距離。"
    ),
    "references": [
        exam_ref(31),
        ref(
            "scikit-learn－DBSCAN 官方文件",
            "https://scikit-learn.org/stable/modules/clustering.html#dbscan",
            "DBSCAN 以 eps 鄰域及 min_samples 定義核心樣本與密度相連群集",
        ),
        ref(
            "Beyer et al., When Is Nearest Neighbor Meaningful?（1999）",
            "https://doi.org/10.1007/3-540-49257-7_15",
            "高維資料中最近與最遠鄰居距離對比可能趨於消失，削弱距離式方法的區辨力",
        ),
    ],
}

DRAFTS[32] = {
    "summary": "正確答案是 B。一般全連結層接收形如（批次大小、特徵數）的輸入，因此需先用 Flatten 展平卷積特徵圖。",
    "concept": (
        "卷積層通常輸出 N×C×H×W 張量，保留批次、通道與空間維度；線性層則對"
        "最後一維的特徵向量做矩陣乘法。若架構要直接從卷積輸出銜接固定大小的"
        "全連結分類器，需保留 N，將 C、H、W 合併成 C×H×W。PyTorch 可使用"
        "torch.flatten(x, 1) 或 nn.Flatten() 完成。"
    ),
    "answerReason": (
        "B 是題目所問的標準維度轉換。A 的全域平均池化也能設計出另一種有效架構，"
        "但它會先把每個通道的空間資訊取平均，不等同單純展平；C 不會自動改維，"
        "D 的 Softmax 則應用於分類分數而非卷積特徵銜接。"
    ),
    "optionAnalysis": {
        "A": (
            "全域平均池化把每個通道的 H×W 值平均成一個數，可大幅減少參數，"
            "某些 CNN 架構確實採用；但若題目要求卷積輸出與一般全連結層之間的"
            "直接形狀轉換，標準操作是 Flatten。"
        ),
        "B": (
            "正確。Flatten 保留批次維度，將 C×H×W 攤平成單一特徵維度，使資料"
            "形狀符合 nn.Linear 的 in_features，之後才能計算分類 logits。"
        ),
        "C": (
            "nn.Linear 只對輸入最後一維做線性轉換，並不會自動把通道、高、寬合併"
            "為預期向量。若直接傳入四維張量，通常會出現維度不符，或得到不是"
            "預期的逐位置線性運算。"
        ),
        "D": (
            "Softmax 將一組 logits 正規化為機率分布，通常放在分類輸出端或交由"
            "損失函式處理。它不改變 C×H×W 為全連結層需要的特徵向量，也會過早"
            "壓縮特徵差異。"
        ),
    },
    "trap": (
        "Flatten 與全域平均池化都可能出現在 CNN，但用途不同：Flatten 只重排"
        "形狀並保留所有元素；全域平均池化會彙整空間資訊並減少元素數。"
    ),
    "editorialNote": (
        "本站依官方答案 B 撰寫。A 不是無效架構：若分類頭按通道數設計，全域平均"
        "池化後也可接全連結層；本題應理解為保留卷積輸出全部元素、銜接一般"
        "Fully Connected Layer 時的必要形狀轉換。待人工複核題意限定。"
    ),
    "references": [
        exam_ref(32),
        ref(
            "PyTorch－nn.Flatten 官方文件",
            "https://docs.pytorch.org/docs/stable/generated/torch.nn.Flatten.html",
            "將連續維度展平；預設保留第 0 維 batch，將其餘維度相乘",
        ),
        ref(
            "PyTorch－nn.Linear 官方文件",
            "https://docs.pytorch.org/docs/stable/generated/torch.nn.Linear.html",
            "輸入最後一維必須等於 in_features，輸出最後一維為 out_features",
        ),
    ],
}

DRAFTS[33] = {
    "summary": "正確答案是 D。合成資料能在可控條件下產生稀有且多樣的場景，補充真實訓練資料並改善模型泛化。",
    "concept": (
        "合成資料由模擬器、圖形引擎或生成模型製造，可精確控制天候、照明、物件"
        "位置及感測器條件，並自動取得標籤。它特別適合補足昂貴、危險或少見的"
        "情境，例如濃霧與大雨駕駛。但模擬與真實世界仍可能有 domain gap，通常"
        "需要搭配真實資料驗證、域隨機化或域適應，而非假設可無條件完全取代。"
    ),
    "answerReason": (
        "D 正確描述合成資料的角色：增加訓練分布中少見條件的覆蓋，讓模型接觸"
        "更多變化。A 錯誤限制於文字，B 忽略模擬落差與真實驗證，C 則把資料來源"
        "與推論計算量混為一談。"
    ),
    "optionAnalysis": {
        "A": (
            "合成資料廣泛用於影像、3D 感知、機器人與自駕模擬，不只文字任務。"
            "圖形引擎可產生具有深度、分割遮罩與邊界框標註的天候場景，正適合"
            "補足昂貴影像資料。"
        ),
        "B": (
            "特定任務可能大量使用合成資料，但『可完全取代』不是一般保證。材質、"
            "光學、天候與感測器雜訊若模擬不準，模型可能只適應合成分布，因此"
            "仍需真實資料校準與測試。"
        ),
        "C": (
            "推論成本主要受模型架構、輸入解析度、數值精度與硬體最佳化影響。"
            "合成資料改變的是訓練資料涵蓋範圍，不會直接縮短已部署模型的運算路徑。"
        ),
        "D": (
            "正確。工程師可系統性調整雨量、霧濃度、光照及道路物件，產生少見"
            "情境並取得一致標籤；與真實資料合理混合後，可提升模型對變化的泛化。"
        ),
    },
    "trap": (
        "合成資料的優勢是『可控制、可擴充』，不是『必然等同真實』。評估時要"
        "同時考慮覆蓋稀有情境與 synthetic-to-real domain gap。"
    ),
    "references": [
        exam_ref(33),
        ref(
            "NVIDIA Omniverse Replicator－Synthetic Data Generation 官方文件",
            "https://docs.omniverse.nvidia.com/extensions/latest/ext_replicator.html",
            "以 domain randomization 產生多樣化合成資料與標註，供電腦視覺模型訓練",
        ),
        ref(
            "Tremblay et al., Training Deep Networks with Synthetic Data（2018）",
            "https://arxiv.org/abs/1804.06516",
            "摘要與方法：以模擬及 domain randomization 產生影像，並結合真實資料改善真實場景偵測",
        ),
    ],
}

DRAFTS[34] = {
    "summary": "正確答案是 B。支援增量學習的模型可隨資料流更新參數，減少等待週期性全量重訓造成的模型過期。",
    "concept": (
        "增量學習（Incremental Learning）將新批次或單筆資料持續納入模型更新，"
        "不必每次從全部歷史資料重新訓練。CTR 等快速變動場景可用線上線性模型、"
        "特徵雜湊或其他串流模型，讓新廣告與設備行為較快反映在權重中。不過，"
        "更新模型參數與擴張輸入 schema 是兩件事；實作仍須採可處理新類別或"
        "固定雜湊空間的特徵表示。"
    ),
    "answerReason": (
        "B 是唯一同時符合即時更新與避免全量重訓的方向。A 仍受批次更新延遲，"
        "C 每次改輸入層並全量訓練更昂貴，D 的圖結構不會自動解決新增特徵與"
        "概念漂移；增量式架構才直接回應模型過期問題。"
    ),
    "optionAnalysis": {
        "A": (
            "把週更改成日更可縮短過期時間，卻仍是定期全量批次訓練；每天內的"
            "新行為仍無法即時反映，資料量增加後訓練成本也會持續上升。羅吉斯"
            "迴歸若改採線上最佳化可增量更新，但選項明確限定傳統靜態方式。"
        ),
        "B": (
            "正確。支援 partial fit 或逐筆更新的模型能保留既有狀態並吸收新資料，"
            "搭配可擴展編碼後可較快學到新廣告位與設備行為，避免每次從零全量訓練。"
        ),
        "C": (
            "固定 DNN 的輸入層通常要求固定維度；每增加特徵就修改網路並全量"
            "重訓，會增加部署與訓練延遲，正好延續題目要避免的靜態流程。"
        ),
        "D": (
            "GNN 適合資料本身有節點與邊關係的任務，但預訓練 GNN 不會自動理解"
            "任意新增欄位，也仍需定義特徵表示與線上更新機制，不能僅靠圖結構"
            "解決動態特徵。"
        ),
    },
    "trap": (
        "不要把『縮短批次週期』當成真正線上學習。另需分清概念漂移、參數增量"
        "更新與 schema 擴張：B 是架構方向，但仍要設計動態特徵表示。"
    ),
    "editorialNote": (
        "本站依官方答案 B 撰寫，但『適應新增特徵』需有實作前提。以 scikit-learn"
        "為例，partial_fit 通常仍要求固定輸入維度；可搭配 FeatureHasher 將新特徵"
        "映射到固定維度，或選用支援動態特徵的線上學習系統。待人工複核是否需"
        "補充題目所假設的特徵編碼。查核日期 2026-08-12。"
    ),
    "references": [
        exam_ref(34),
        ref(
            "scikit-learn－Strategies to scale computationally: incremental learning",
            "https://scikit-learn.org/stable/computing/scaling_strategies.html#incremental-learning",
            "支援 partial_fit 的估計器可從小批次資料增量更新，避免一次載入完整資料集",
        ),
        ref(
            "scikit-learn－FeatureHasher 官方文件",
            "https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.FeatureHasher.html",
            "以 hashing trick 將符號特徵映射到固定維度，適合線上或記憶體受限情境",
        ),
    ],
}

DRAFTS[35] = {
    "summary": "正確答案是 B。異質資料應先用各自合適的方法取得表示，再進行特徵融合，而非先粗略混成同一矩陣。",
    "concept": (
        "基因資料是高維數值或類別訊號，常需依統計關聯、正則化或領域知識篩選；"
        "病歷文本則需要斷詞、語意嵌入或語言模型編碼。多模態建模應先尊重各模態"
        "的尺度、結構與噪音特性，再於 early、intermediate 或 late fusion 階段"
        "結合。若一開始用同一種轉換處理所有欄位，容易破壞模態特有結構。"
    ),
    "answerReason": (
        "B 先對基因與文本採專屬處理，再融合兩類表示，完整回應題幹所說的性質"
        "差異。A、C 在合併後用單一方法處理，忽略不同尺度與語意；D 僅用詞頻"
        "會損失病歷中的語境與詞序資訊。"
    ),
    "optionAnalysis": {
        "A": (
            "PCA 可對同尺度的數值矩陣找最大變異方向，但把基因值與未適當編碼的"
            "文本直接合併，主成分可能被量綱或高變異模態主導；PCA 也不會自行"
            "理解文本語意。"
        ),
        "B": (
            "正確。先為基因特徵去除冗餘與噪音，再以適合的文本模型取得語意表示，"
            "最後在對齊樣本與尺度後融合，可保留兩模態互補資訊。"
        ),
        "C": (
            "隨機森林重要性可用於特定表格模型的特徵選擇，但一次合併與排序仍"
            "假設所有輸入已是可比較的固定數值；高基數、相關特徵與文本表示還可能"
            "造成重要性偏差，並非最佳的異質處理策略。"
        ),
        "D": (
            "詞頻可作為簡單文本基線，卻忽略否定、上下文與臨床詞彙語意；降低"
            "複雜度不等於最合適。題目明示語意文本特徵，應採能保留語意的表示"
            "再與基因資料融合。"
        ),
    },
    "trap": (
        "多模態的『融合』不是先把原始欄位拼起來。先分別抽取可靠表示，再選擇"
        "融合層次；也要避免單一模態因維度或尺度較大而主導模型。"
    ),
    "references": [
        exam_ref(35),
        ref(
            "Baltrušaitis, Ahuja & Morency, Multimodal Machine Learning: A Survey and Taxonomy（2018）",
            "https://doi.org/10.1109/TPAMI.2018.2798607",
            "多模態 representation 與 fusion 分類：各模態表示後可在不同階段整合互補資訊",
        ),
        ref(
            "Lee et al., BioBERT: a pre-trained biomedical language representation model（2020）",
            "https://doi.org/10.1093/bioinformatics/btz682",
            "摘要與方法：以生醫語料預訓練語言表示，改善生醫文本探勘任務",
        ),
    ],
}

DRAFTS[36] = {
    "summary": "正確答案是 A。標註影像很少時，使用大型資料集預訓練的 CNN 再微調，通常比從頭訓練大型模型更有效。",
    "concept": (
        "遷移學習利用來源任務已學得的視覺特徵，例如邊緣、紋理與形狀，作為"
        "目標任務起點。小資料情境可先凍結大部分 backbone，只訓練分類頭，再以"
        "較小學習率微調部分或全部層；搭配合理資料增強與驗證，可降低從隨機"
        "初始化訓練所需樣本量及過擬合風險。"
    ),
    "answerReason": (
        "每類只有約 50 張影像，A 能重用預訓練表示並將有限標註集中於瑕疵類別"
        "適配。B 從頭訓練大型 ViT 對資料量要求高，C 的無監督群集不等同十類"
        "監督分類，D 只複製相同影像不增加資訊。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。預訓練 CNN 已從大規模影像學到可轉移特徵；替換最後分類層並"
            "用 500 張標註影像微調，可降低參數估計難度，通常是小型影像資料集"
            "的實用起點。"
        ),
        "B": (
            "大型 ViT 從隨機初始化訓練通常需要大量資料或強正則化；500 張影像"
            "難以穩定估計眾多參數，容易記住訓練集。若使用預訓練 ViT 再微調才"
            "可能是合理替代，但選項明確說從頭訓練。"
        ),
        "C": (
            "K-means 依特徵距離分群，不知道人工定義的十種瑕疵標籤，也不保證"
            "每個群正好對應一個類別。它可用於探索資料，不能直接替代監督分類器。"
        ),
        "D": (
            "重複複製影像只增加檔案與抽樣次數，不增加新的視角、光照或瑕疵"
            "變化，模型仍可記住相同樣本。應採具標籤保持性的資料增強，而不是"
            "原樣複製後從頭訓練。"
        ),
    },
    "trap": (
        "題目限制的是標註量，不是完全沒有外部知識。遷移學習重用預訓練權重；"
        "不要把『複製資料』誤認為產生新資訊，也別把分群當成分類。"
    ),
    "references": [
        exam_ref(36),
        ref(
            "PyTorch－Transfer Learning for Computer Vision Tutorial",
            "https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html",
            "小型影像資料集下，以 ImageNet 預訓練網路進行 fine-tuning 或固定特徵抽取",
        ),
        ref(
            "Yosinski et al., How transferable are features in deep neural networks?（2014）",
            "https://arxiv.org/abs/1411.1792",
            "實驗分析深度網路各層特徵的通用性與遷移後微調效果",
        ),
    ],
}

DRAFTS[37] = {
    "summary": "正確答案是 A。SMOTE 可在訓練資料層級合成少數類別樣本，緩解 99:1 的類別不平衡。",
    "concept": (
        "SMOTE（Synthetic Minority Over-sampling Technique）在少數類別樣本與其"
        "近鄰之間插值，產生新的少數類別特徵，而不是只原樣複製。它屬資料前"
        "處理，能提高模型在訓練時看到瑕疵類的機會。必須只在訓練折內執行以"
        "避免資料洩漏，且影像資料通常需在合適特徵空間使用或改採影像增強。"
    ),
    "answerReason": (
        "題目明確限定不改模型與學習演算法，只透過資料前處理，A 正好符合。B、C"
        "分別改正則化與架構，超出限制；D 增加多數類別會讓 99:1 更嚴重，即使"
        "表面 accuracy 上升也會犧牲瑕疵辨識。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。SMOTE 以少數類鄰近樣本插值，重新平衡訓練資料，使分類器在"
            "參數更新時更重視瑕疵類；後續仍應用 recall、precision 或 PR AUC"
            "評估，而非只看 accuracy。"
        ),
        "B": (
            "L1/L2 正則化限制權重複雜度以減少過擬合，屬模型訓練設定；它不改變"
            "良品與瑕疵樣本的比例，也不保證少數類獲得足夠學習訊號。"
        ),
        "C": (
            "增加網路層數會改動模型架構並提高容量與過擬合風險，沒有增加少數類"
            "資料。類別比例不平衡不會單靠更深特徵抽取而消失。"
        ),
        "D": (
            "複製更多良品會進一步放大多數類優勢，模型更容易一律預測良品。"
            "Accuracy 可能因類別基準率而看似很高，卻使瑕疵 recall 更差，與需求相反。"
        ),
    },
    "trap": (
        "先遵守『只改資料』的限制，再判斷重採樣方向。少數類要過採樣或多數類"
        "適度欠採樣；不能為追求整體 accuracy 繼續增加良品。"
    ),
    "editorialNote": (
        "本站依官方答案 A 撰寫。原始像素上的 SMOTE 插值未必產生自然影像；實務"
        "應在驗證過的表徵空間使用，或採旋轉、裁切、生成式資料等影像適用增強。"
        "任何重採樣只可套用訓練資料，不得在切分資料前執行。"
    ),
    "references": [
        exam_ref(37),
        ref(
            "Chawla et al., SMOTE: Synthetic Minority Over-sampling Technique（2002）",
            "https://doi.org/10.1613/jair.953",
            "第 4 節：在少數類樣本與其近鄰之間插值產生合成樣本",
        ),
        ref(
            "imbalanced-learn－SMOTE 官方文件",
            "https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html",
            "SMOTE 參數、fit_resample 介面及支援的重採樣策略",
        ),
    ],
}

DRAFTS[38] = {
    "summary": "正確答案是 D。已確認 999°C 是不可能的通訊錯誤時，應刪除該筆或以中位數等穩健值填補。",
    "concept": (
        "離群值處理要先判斷成因：真實極端事件可能含重要訊息，資料錯誤則不應"
        "當成有效溫度餵給模型。本題已提供常態範圍、物理不可能性與通訊溢位原因，"
        "可將該值標為遺失後刪除，或依時間、設備與缺失比例使用中位數等穩健方法"
        "填補。中位數不易被極端值拉動。"
    ),
    "answerReason": (
        "D 直接排除已知錯誤觀測，或用不受 999 強烈影響的中位數替代。A 會讓"
        "平均數受到污染；B 只改尺度且極端值仍存在；C 把連續溫度錯誤變成類別，"
        "都沒有清除不可能的測量。"
    ),
    "optionAnalysis": {
        "A": (
            "平均數對極端值敏感，少數 999°C 就可能明顯拉高中心位置，保留後"
            "直接輸入還會讓模型學到錯誤關係。保存原始資料供稽核可以，但建模"
            "資料應另行清理。"
        ),
        "B": (
            "Z-score 是減去平均再除以標準差，理論上不會把所有值裁切在 [-3,3]；"
            "999°C 仍會是極端標準分數，還可能扭曲樣本平均與標準差，因此不是"
            "錯誤值修復。"
        ),
        "C": (
            "One-Hot 適合無序類別，不適合把單一錯誤溫度當成合法的新類別。這會"
            "保留通訊故障訊號而非還原溫度；若故障狀態有價值，應另建品質旗標。"
        ),
        "D": (
            "正確。若異常筆數極少且可安全捨棄，可刪除；若需保留時間序列位置，"
            "可先標記缺失，再用中位數或更符合時序的插補法處理。"
        ),
    },
    "trap": (
        "標準化不等於離群值移除，也不會自動把資料限制在三個標準差內。先判斷"
        "是真實事件還是已知錯誤；只有後者才適合直接刪除或填補。"
    ),
    "references": [
        exam_ref(38),
        ref(
            "scikit-learn－StandardScaler 官方文件",
            "https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html",
            "標準化公式 z=(x-u)/s，並明示 StandardScaler 對 outliers 敏感；不包含裁切",
        ),
        ref(
            "scikit-learn－SimpleImputer 官方文件",
            "https://scikit-learn.org/stable/modules/generated/sklearn.impute.SimpleImputer.html",
            "strategy='median' 可用各欄訓練資料中位數填補缺失值",
        ),
    ],
}

DRAFTS[39] = {
    "summary": "正確答案是 A。原始影像與非結構化文本適合存放資料湖，整理後的結構化特徵則適合資料倉儲。",
    "concept": (
        "資料湖通常以原生格式保存大量結構化、半結構化與非結構化資料，採"
        "schema-on-read，便於後續用不同工具重處理原始影像與文本。資料倉儲採"
        "較明確的 schema-on-write，保存清理、整合後的結構化資料，適合穩定的"
        "SQL 查詢、報表與治理。兩者可在同一平台架構中互補，不必二選一。"
    ),
    "answerReason": (
        "A 依資料型態與用途分工：保留原始多模態素材於 lake，將可直接分析的"
        "結構化特徵放入 warehouse。B 讓倉儲承擔大量原始物件不經濟；C 放棄"
        "結構化查詢優勢；D 又把非結構化文本錯放到只適合整理後資料的倉儲。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。影像檔與原始文本可低成本保留在資料湖，供模型反覆抽取特徵；"
            "已清理且 schema 穩定的特徵表放入倉儲，便於 SQL 查詢、版本與品質管理。"
        ),
        "B": (
            "資料倉儲能處理結構化分析，但將所有原始影像與長文本轉入倉儲格式"
            "會增加載入、轉換與儲存成本，也失去保留原始格式供不同模型重處理的彈性。"
        ),
        "C": (
            "資料湖技術也能查詢結構化資料，並非必然犧牲效率；但穩定的特徵表"
            "若有高頻 SQL、BI 與治理需求，倉儲通常提供較成熟的結構、索引與"
            "工作負載最佳化。"
        ),
        "D": (
            "非結構化文本與原始影像同樣適合先保留於資料湖，因為未來可能更換"
            "tokenizer 或 embedding 模型。把所有文本直接放倉儲會混淆原始語料"
            "與整理後結構化特徵。"
        ),
    },
    "trap": (
        "不要只按檔案副檔名選系統，要看資料成熟度與存取模式：原始、多樣、待"
        "探索資料進 lake；整理後、schema 穩定且需高效分析的資料進 warehouse。"
    ),
    "references": [
        exam_ref(39),
        ref(
            "AWS－What is a Data Lake? 官方說明",
            "https://aws.amazon.com/what-is/data-lake/",
            "資料湖以原生格式集中儲存結構化與非結構化資料，供分析與機器學習使用",
        ),
        ref(
            "Google Cloud－Data lake vs. data warehouse 官方說明",
            "https://cloud.google.com/learn/what-is-a-data-lake",
            "比較資料湖的原始多型態資料與資料倉儲的已處理結構化資料及查詢用途",
        ),
    ],
}

DRAFTS[40] = {
    "summary": "正確答案是 D。將 FP32 模型量化為 INT8 並使用裝置相容的推論加速，可減少記憶體流量與整數運算成本。",
    "concept": (
        "量化把權重與／或 activation 從 32 位元浮點表示轉成 8 位元整數表示，"
        "可縮小模型與記憶體頻寬需求；若邊緣硬體與推論引擎有 INT8 加速單元，"
        "還能降低單張推論延遲。部署前需用代表性資料校正或量化感知訓練，並"
        "比較精度下降、算子支援與端到端 latency，不能只看模型檔大小。"
    ),
    "answerReason": (
        "D 同時針對既有硬體的模型計算與執行引擎最佳化，最符合低於 200ms 且"
        "維持合理準確率的要求。A 改訓練資料不保證模型變快；B 增加等待以湊批次，"
        "不利單張即時延遲；C 同時跑多模型反而增加運算。"
    ),
    "optionAnalysis": {
        "A": (
            "訓練樣本數影響訓練時間與泛化，部署後每張影像要執行的模型算子與"
            "參數量通常不變。減少資料還可能降低瑕疵涵蓋率，不能作為推論加速方法。"
        ),
        "B": (
            "批次推論可提高吞吐量，但即時串流需等待累積一批影像，且較大 batch"
            "占用更多記憶體；對單張端到端延遲低於 200ms 的目標未必有利。"
        ),
        "C": (
            "模型集成可降低單一模型誤差，但必須執行多個模型並彙整結果，通常"
            "增加計算量、記憶體與延遲，與不換硬體的加速目標相反。"
        ),
        "D": (
            "正確。INT8 將每個值的儲存量降至 FP32 的四分之一，支援整數加速的"
            "引擎可減少記憶體搬移與運算時間；經校正或量化感知訓練可控制精度損失。"
        ),
    },
    "trap": (
        "吞吐量與延遲不是同一指標：batch 可能讓每秒處理張數上升，卻增加單張"
        "等待時間。INT8 也不是必然加速，仍須確認硬體、算子與推論引擎支援。"
    ),
    "editorialNote": (
        "本站依官方答案 D 撰寫。INT8 的實際延遲收益取決於邊緣硬體是否具有效率"
        "的 INT8 kernel、模型算子覆蓋率與資料搬移瓶頸；部署前應以目標裝置實測"
        "端到端 P95 latency 與準確率。查核日期 2026-08-12。"
    ),
    "references": [
        exam_ref(40),
        ref(
            "NVIDIA TensorRT－Working with Quantized Types 官方文件",
            "https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/work-quantized-types.html",
            "INT8 顯式與隱式量化、scale、校正與量化算子執行方式",
        ),
        ref(
            "PyTorch－Quantization 官方文件",
            "https://docs.pytorch.org/docs/stable/quantization.html",
            "量化將模型計算與儲存由浮點轉為較低精度，並提供 post-training 與 quantization-aware training 流程",
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
