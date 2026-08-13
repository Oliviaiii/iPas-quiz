"""Write draft explanations for 114-2 intermediate subject one, Q11-Q20.

This script refuses to overwrite reviewed explanations and verifies every
official answer before changing ``questions.json``.  All content remains a
draft until a separate reviewer completes the authoring-guide checklist.

Usage::

    python scripts/write-explanations-114-2-m1-011-020.py
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
SK = "https://scikit-learn.org/stable/modules/"
DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def exam_ref(number: int) -> dict:
    return {
        "title": "114 年第二次中級 AI 應用規劃師－人工智慧技術應用與規劃公告試題",
        "url": EXAM_PDF,
        "locator": f"第 {number} 題題幹、選項與官方答案",
        "checkedAt": CHECKED_AT,
    }


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


EXPECTED_ANSWER = {
    11: "C", 12: "B", 13: "B", 14: "A", 15: "C",
    16: "D", 17: "D", 18: "D", 19: "B", 20: "B",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[11] = {
    "summary": "正確答案是 C。DBSCAN 以鄰域半徑 ε 決定哪些點互為鄰居，再以 MinPts 判斷該鄰域是否足以形成高密度區域，兩者共同決定群集與雜訊。",
    "concept": (
        "DBSCAN 是密度式分群：對每個樣本建立半徑為 ε（eps）的鄰域，若鄰域內"
        "樣本數至少達 MinPts（scikit-learn 參數名為 min_samples），該點便可成為"
        "核心點；相連的核心點及其可達邊界點形成群集，無法由任何核心點密度可達"
        "的樣本則標為雜訊。ε 太大容易合併群集，太小則會產生較多雜訊；MinPts "
        "提高會要求更高的局部密度。DBSCAN 不需要事先指定群集數 K。"
    ),
    "answerReason": (
        "題幹問的是決定 DBSCAN 聚類結果的兩個主要超參數。C 同時列出鄰域尺度"
        "ε 與形成核心點所需的最小樣本數 MinPts，正好對應演算法的密度定義，"
        "也直接控制主要群集與雜訊的分界。"
    ),
    "optionAnalysis": {
        "A": "特徵數是輸入資料的維度，通常由特徵工程決定；學習率用於梯度式最佳化。DBSCAN 依鄰域與密度擴張群集，不以梯度更新參數，因此這兩者不是其核心超參數。",
        "B": "K 值常見於 K-means 或 K-nearest neighbors，用來指定群集數或鄰居數；DBSCAN 的優點之一正是不必預先指定群集數。雖然它使用距離，但正式搭配的是 ε 與 MinPts，而不是 K 與距離閾值。",
        "C": "正確。ε 界定一個點周圍的鄰域範圍，MinPts 界定該鄰域達到何種點數才算高密度；核心點、密度可達關係與雜訊標記都由這兩項設定衍生。",
        "D": "交叉熵是分類模型常見的損失函數，權重初始化是神經網路開始梯度訓練前的設定。DBSCAN 沒有需以反向傳播學習的權重，也不最小化交叉熵，故兩者不適用。",
    },
    "trap": "不要把所有分群都想成要指定 K；K-means 先指定群集數，DBSCAN 則以 ε 與 MinPts 定義局部密度，最後由資料密度自行長出群集數並留下雜訊。",
    "references": [
        exam_ref(11),
        ref("scikit-learn User Guide－DBSCAN", SK + "clustering.html#dbscan", "DBSCAN 的 eps、min_samples、核心樣本、群集與雜訊定義"),
    ],
}

DRAFTS[12] = {
    "summary": "正確答案是 B。PCA 會把彼此相關的原始特徵旋轉成互相正交的主成分，可減少多重共線性造成的線性迴歸係數不穩定。",
    "concept": (
        "多重共線性表示迴歸的解釋變數高度線性相關，使設計矩陣接近奇異；即使"
        "整體預測未必完全失效，個別係數也可能因資料小幅變動而大幅改變。主成分"
        "分析（PCA）先將資料中心化，再以奇異值分解找出依解釋變異量排序、彼此"
        "正交的新座標。選取部分主成分可同時去除線性相關與降維，但成分是原始"
        "特徵的線性組合，因此會犧牲個別原始變數係數的直接可解釋性。"
    ),
    "answerReason": (
        "題幹已明說問題來源是多個特徵高度相關。B 直接將相關變數轉換為正交的"
        "主成分，再用這些成分建立迴歸，可消除主成分彼此間的線性共線性，是四個"
        "選項中唯一針對根因的處理方式。"
    ),
    "optionAnalysis": {
        "A": "原樣保留高度相關特徵會留下近似重複的資訊，設計矩陣的條件數仍可能很差，係數的不確定性與對樣本擾動的敏感性不會自行消失，未處理題幹指出的根因。",
        "B": "正確。PCA 將中心化資料投影到互相正交的主軸，主成分之間不再線性相關；挑選能保留主要變異的成分後做迴歸，可緩解多重共線性與冗餘維度。",
        "C": "新增更多原始變數只有在帶來獨立且有用訊息時才可能改善模型；若仍與既有變數高度相關，反而增加冗餘、估計變異與過擬合風險，不能當作共線性的通用解法。",
        "D": "房價是連續數值，線性迴歸的任務型態正確；分類模型輸出離散類別，除非先把房價任意分箱而改變問題，否則不適合預測總價，也沒有處理特徵相關性。",
    },
    "trap": "PCA 解決的是特徵空間的線性相關與維度問題，不等於保證預測一定更準；還要用驗證資料選主成分數。另要分清楚房價預測是迴歸，不因係數不穩就改成分類。",
    "references": [
        exam_ref(12),
        ref("scikit-learn User Guide－PCA", SK + "decomposition.html#pca", "PCA 以 SVD 將中心化輸入投影到正交成分，並可依成分數降維"),
    ],
}

DRAFTS[13] = {
    "summary": "正確答案是 B。Kubernetes 的核心角色是協調容器化工作負載，讓模型服務可宣告式部署、維持運行、擴展副本並管理其執行環境。",
    "concept": (
        "Kubernetes 是容器協調平台。部署 AI 模型時，模型伺服器通常被封裝成"
        "容器，再以 Deployment 等工作負載資源宣告映像、Pod 副本數與更新策略；"
        "控制平面持續讓實際狀態逼近期望狀態，並可配合 Service、水平 Pod 自動"
        "擴展與自我修復維持推論服務。它管理的是執行與調度層，不會自動取代"
        "訓練框架、實驗追蹤、資料版本庫或 GPU 本身的數值運算。"
    ),
    "answerReason": (
        "B 所述部署、擴展與運行環境，逐項對應 Kubernetes 對容器化工作負載的"
        "編排功能。其餘選項分別屬於訓練調參、資料與模型資產管理、硬體加速，"
        "可能與 Kubernetes 整合，但不是 Kubernetes 自身的核心功能。"
    ),
    "optionAnalysis": {
        "A": "訓練流程與超參數搜尋通常由 Kubeflow、Ray、Optuna 或訓練框架負責；它們可以把工作提交到 Kubernetes，但 Kubernetes 原生控制器只負責排程與維持工作負載，不理解模型參數優劣。",
        "B": "正確。Kubernetes 能以 Deployment 管理模型服務 Pod 的版本與副本，透過排程、滾動更新、自我修復及自動擴展，協調服務在叢集中的部署和持續運行。",
        "C": "持久資料、特徵與模型版本通常由物件儲存、資料版本工具或 Model Registry 管理。Kubernetes 可掛載 PersistentVolume，但提供儲存介面不等於替使用者完成資料內容與版本治理。",
        "D": "GPU 的矩陣計算由硬體、驅動與深度學習函式庫執行；Kubernetes 可透過 device plugin 把 GPU 資源排程給 Pod，卻不負責推論算子的加速運算本身。",
    },
    "trap": "要區分「平台負責協調資源」與「應用工具完成工作」：Kubernetes 可排程有 GPU 的訓練或推論容器，但不會自己訓練模型、管理模型內容或執行 GPU 核心運算。",
    "references": [
        exam_ref(13),
        ref("Kubernetes Documentation－Overview", "https://kubernetes.io/docs/concepts/overview/", "Kubernetes 為管理容器化工作負載與服務的可攜、可擴展平台"),
        ref("Kubernetes Documentation－Deployments", "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/", "Deployment 管理 Pod 與 ReplicaSet，提供宣告式更新"),
    ],
}

DRAFTS[14] = {
    "summary": "正確答案是 A。交叉驗證讓每組超參數在多個不同資料切分上接受評估，較能排除偶然切分造成的高分，選出表現穩定且可泛化的設定。",
    "concept": (
        "超參數選擇本身也是學習過程：若反覆看同一份驗證集並依其分數調整，"
        "設定可能逐漸過度貼合該驗證集。K 折交叉驗證輪流以不同折作驗證，其餘"
        "折訓練，使用多次外樣本分數的平均與變異比較候選設定，比單次切分更穩定。"
        "完成選擇後仍應保留未參與調參的測試集；若要對調參後泛化誤差做較無偏"
        "估計，可使用巢狀交叉驗證，由內層選參數、外層評估。"
    ),
    "answerReason": (
        "題幹聚焦「因過度調整超參數而過擬合」。A 讓多組候選參數在多個驗證折"
        "反覆比較，選擇跨切分都穩定的設定，直接降低對單一驗證切分的偶然適配；"
        "在四個選項中最符合超參數選擇的泛化控制。"
    ),
    "optionAnalysis": {
        "A": "正確。交叉驗證讓每組候選設定接受多次外樣本評估，平均分數反映整體表現，折間波動則顯示穩定性；搭配獨立測試集或巢狀交叉驗證，可避免把調參結果誤當最終泛化成績。",
        "B": "早期停止可以抑制單次模型訓練過久，但應監控驗證指標而非題目寫的訓練誤差；若只看持續下降的訓練誤差，通常無法判斷泛化何時惡化，也沒有解決跨多組超參數反覆挑選的偏差。",
        "C": "標準化使不同量綱的特徵具有可比較尺度，對距離法與帶正則化或梯度最佳化的模型很重要；但它不是用來偵測候選超參數是否只適合某一次驗證切分的評估設計。",
        "D": "提高複雜度與擴大搜尋範圍會增加可供挑選的設定；若驗證流程不嚴謹，選中偶然高分設定的機會反而上升，與降低超參數過擬合的目的相反。",
    },
    "trap": "早期停止確實是正則化手段，但本選項錯在只監控訓練誤差，且題目問的是多組超參數的選擇。交叉驗證用來選參數，最終測試集則不可再拿回來調參。",
    "references": [
        exam_ref(14),
        ref("scikit-learn User Guide－Cross-validation", SK + "cross_validation.html", "交叉驗證以多次訓練／驗證切分評估泛化能力，測試資料應保留到最後"),
        ref("scikit-learn Example－Nested versus non-nested cross-validation", "https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html", "以同一資料調參與評估會造成偏樂觀，巢狀交叉驗證可分離選參與估計"),
    ],
}

DRAFTS[15] = {
    "summary": "正確答案是 C。Model Registry 是模型生命週期的集中目錄，用來登錄模型版本、連回產生模型的訓練執行紀錄，並以狀態、別名或標籤支援部署治理。",
    "concept": (
        "MLOps 將資料、訓練、模型封裝、部署與監控串成可追溯流程。Model Registry "
        "位在模型產出後、部署前後的治理樞紐：同一個註冊模型下保留多個版本，"
        "記錄來源執行、簽章、描述與標籤，並用 alias 或生命週期狀態指出候選版"
        "與目前服務版。它可提供部署端查找正確模型的依據，但運算環境配置、"
        "Feature Store 與線上漂移監控仍是不同元件。"
    ),
    "answerReason": (
        "C 的版本、訓練紀錄關聯與部署狀態正是 Registry 要集中治理的模型中繼"
        "資料。其他選項分別描述基礎設施、Feature Store／資料版本及 Monitoring，"
        "雖都屬 MLOps，卻不是 Model Registry 最常負責的階段。"
    ),
    "optionAnalysis": {
        "A": "CPU、GPU、記憶體、映像與依賴環境通常由雲端平台、容器及叢集排程器設定；Registry 可以記錄模型相依資訊，卻不會替訓練工作配置或執行運算資源。",
        "B": "可重複使用的特徵定義、離線／線上特徵值及其版本通常由 Feature Store 或資料版本系統管理。Model Registry 管的是訓練完成的模型物件與中繼資料，資產層級不同。",
        "C": "正確。Registry 以註冊模型和模型版本為核心，連結產生版本的實驗執行與成品，並用描述、標籤、alias 或狀態協助審核、部署與回滾。",
        "D": "上線後的準確率、延遲、資料漂移與概念漂移需要監控服務持續蒐集實際流量和標籤；Registry 可保存監控結果所觸發的新版本或標籤，但本身不是即時監控引擎。",
    },
    "trap": "MLOps 名詞容易混在一起：Feature Store 管特徵、Experiment Tracking 管訓練執行、Model Registry 管可部署模型版本、Monitoring 管上線後指標；可互相連結但不能視為同一元件。",
    "references": [
        exam_ref(15),
        ref("MLflow Documentation－Model Registry Workflows", "https://mlflow.org/docs/latest/ml/model-registry/workflow", "註冊模型、模型版本、來源 run、alias、tags 與部署組織流程"),
    ],
}

DRAFTS[16] = {
    "summary": "正確答案是 D。Seq2Seq 將一個可變長度序列編碼後，再逐步產生另一個可變長度序列，翻譯與生成式摘要正是典型的文字序列轉文字序列任務。",
    "concept": (
        "序列到序列（Sequence-to-Sequence, Seq2Seq）模型包含處理輸入序列的"
        "編碼器與產生輸出序列的解碼器，輸入與輸出長度可以不同。原始神經機器"
        "翻譯工作即用一個深層 LSTM 將句子映射成向量，再由另一個 LSTM 生成目標"
        "句；後續注意力機制與 Transformer 改良了長距依賴，但輸入序列轉輸出序列"
        "的任務定義不變。抽取實體與詞頻統計不需生成新序列。"
    ),
    "answerReason": (
        "D 的翻譯把來源語句轉成目標語句，摘要把長文本轉成較短且語意相關的"
        "文本，兩者都需要依輸入條件逐 token 生成另一段序列，完整符合 Seq2Seq。"
        "其餘任務不是此模型最典型、最直接的適用情境。"
    ),
    "optionAnalysis": {
        "A": "時間序列模型確實可能一次輸出多個未來值，也能採 encoder-decoder 架構；但題目問最適合的典型 Seq2Seq 情境，原始概念主要指可變長度符號序列的條件生成，D 的翻譯與摘要更直接。",
        "B": "命名實體辨識通常是序列標註：對輸入中的每個 token 指派人名、地名、組織或非實體標籤，輸出與輸入位置對齊，不需要解碼器自由生成另一段文字。",
        "C": "關鍵字頻率統計是計數與彙總，只需 tokenize 後計算出現次數再視覺化；它不學習輸入到輸出的條件序列分布，也無需逐步解碼。",
        "D": "正確。翻譯需要依來源句生成不同長度的目標語句，生成式摘要需要依長文產生較短敘述；兩者都是編碼輸入序列、再解碼輸出序列的代表性應用。",
    },
    "trap": "看到「序列」不代表都要用 Seq2Seq；NER 是逐 token 標註，詞頻是統計，只有需要依輸入生成另一個可變長度序列時，encoder-decoder 的 Seq2Seq 特性才最突出。",
    "references": [
        exam_ref(16),
        ref("Sequence to Sequence Learning with Neural Networks", "https://arxiv.org/abs/1409.3215", "Abstract 與方法：以多層 LSTM 將輸入序列映射成固定維向量，再由另一 LSTM 解碼目標序列；應用於機器翻譯"),
    ],
}

DRAFTS[17] = {
    "summary": "正確答案是 D。檢索階段的首要品質門檻是相關性：若向量近鄰只在字面或主題上相似、卻沒有回答查詢意圖，後續生成就會被錯誤證據帶偏。",
    "concept": (
        "RAG 以檢索器從外部知識庫挑選文件，再把文件交給生成器作答。向量檢索"
        "通常把查詢與文件嵌入同一空間，以近鄰分數找候選，但嵌入相似度只是代理"
        "訊號：文件可能共享術語或主題，卻不包含問題需要的時間、實體、條件或"
        "答案證據。因此檢索品質的核心是意圖相關性與證據充分性，實務上可透過"
        "較合適的切塊、混合檢索、metadata filter、reranker 與檢索評估改善。"
    ),
    "answerReason": (
        "D 指出語意相似不等於實質相關，這是檢索器能否把正確證據送進生成器的"
        "根本挑戰。A 屬於檢索後的上下文組裝，B 是工具選型，C 是效率工程；"
        "它們重要但都不能替代相關文件本身的品質。"
    ),
    "optionAnalysis": {
        "A": "上下文視窗限制發生在候選文件已取回之後，通常以切塊選取、壓縮或排序處理；把所有文件完整塞入既不必要也可能稀釋證據，這是生成前的 context construction，不是檢索相關性的核心判準。",
        "B": "Faiss 與 ScaNN 都是近似最近鄰搜尋實作，選型會影響延遲、召回率與維運；但無論採何種函式庫，若 embedding 或排序無法理解查詢意圖，仍會快速取回不相關文件。",
        "C": "高維向量的計算與記憶體成本會影響吞吐量，可用量化、索引結構或較小嵌入模型改善；這屬效能與資源限制，不等於檢索到的內容能支持問題答案。",
        "D": "正確。向量距離高可能只代表用詞或主題相近，未必符合查詢中的實體、時間與關係限制；若候選缺乏真正答案證據，語言模型仍可能據錯誤上下文作答。",
    },
    "trap": "不要把「速度最快的向量資料庫」當成「最佳檢索」；RAG 要先確保取回的片段能回答問題，再優化延遲。另要區分 retrieval、context assembly 與 generation 三個階段。",
    "editorialNote": "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。題目以「最關鍵」比較品質與效率，D 為官方答案；不同服務等級下索引成本也可能成為工程瓶頸，但不改變檢索相關性是作答品質前提。",
    "references": [
        exam_ref(17),
        ref("Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", "https://arxiv.org/abs/2005.11401", "Abstract 與方法：RAG 結合預訓練 seq2seq 的參數記憶及由 dense retriever 存取的非參數文件索引"),
        ref("Dense Passage Retrieval for Open-Domain Question Answering", "https://arxiv.org/abs/2004.04906", "方法與實驗：以雙編碼器進行 passage retrieval，檢索器目標是為問題找出包含答案的相關段落"),
    ],
}

DRAFTS[18] = {
    "summary": "正確答案是 D。對注意力權重加入稀疏化約束會迫使多數位置的權重趨近零，讓有限權重集中於少數關鍵位置，直接對治過度平均的分布。",
    "concept": (
        "標準注意力先計算 Query 與 Key 的相似分數，再以 softmax 正規化；softmax "
        "會為所有位置給出正值，分數差異不足時分布便可能接近平均，使 Value 的"
        "加權和缺乏焦點。稀疏注意力透過遮罩、正則項，或 sparsemax／entmax 等"
        "可產生零權重的轉換，限制真正參與聚合的位置，因而提升選擇性。這與單純"
        "增加隨機噪音或把 softmax 換成未正規化的 ReLU 有本質差異。"
    ),
    "answerReason": (
        "題幹指定問題是注意力權重過於平均。D 直接約束權重分布變得稀疏，讓模型"
        "把機率質量集中到少數關鍵 token，與問題及改善方向一一對應；其他方法"
        "沒有提供穩定、正規化且可控的聚焦機制。"
    ),
    "optionAnalysis": {
        "A": "縮放點積注意力原本是除以 √d_k，避免維度增大時點積方差過大、softmax 落入極端小梯度區。若「提高縮放常數」指分母變大，分數會更接近零，softmax 反而更平均，會加劇題幹問題。",
        "B": "在 logits 加高斯雜訊可造成暫時擾動，或在特定正則化設計中增加探索，但噪音不保證總是強化真正關鍵位置；推論時移除後也可能恢復平均，並非直接且穩定的解法。",
        "C": "ReLU 只截掉負分數，輸出既不自動總和為一，也可能出現全部為零或尺度不穩；若要以稀疏轉換取代 softmax，通常需使用 sparsemax／entmax 等有明確正規化定義的方法，而非直接換 ReLU。",
        "D": "正確。稀疏化約束懲罰分散權重或限制可被關注的位置，使非關鍵位置成為零或近零，剩餘權重集中在較少 token 上，直接改善無法聚焦的過度平均現象。",
    },
    "trap": "縮放常數的方向最容易看反：分母越大，logits 越平，softmax 越接近平均。另要注意「直接用 ReLU」不等於具有機率單純形約束的 sparsemax 或 entmax。",
    "editorialNote": "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。「Attention Collapse」在研究文獻中有多種用法，本題已由題幹明確限定為權重過於平均，故依此定義解讀；待複核確認官方學習材料是否採相同術語。",
    "references": [
        exam_ref(18),
        ref("Attention Is All You Need", "https://arxiv.org/abs/1706.03762", "第 3.2.1 節：scaled dot-product attention 除以 √d_k，避免大點積將 softmax 推入極小梯度區"),
        ref("Sparse Sequence-to-Sequence Models", "https://arxiv.org/abs/1905.05702", "Abstract 與方法：softmax 形成稠密 alignment；entmax 系列可產生稀疏注意力"),
    ],
}

DRAFTS[19] = {
    "summary": "正確答案是 B。反向翻譯可利用既有翻譯模型把單語句子轉成偽來源句，形成額外偽平行語料，等同在不蒐集新真實配對資料下進行資料增強。",
    "concept": (
        "低資源語言模型只有少量訓練樣本時，容量相對資料量過大便容易記住訓練"
        "資料。反向翻譯（Back-Translation）是半監督式資料增強：先用反方向翻譯"
        "模型把目標語言單語句翻回來源語言，再將合成來源句與原目標句組成偽平行"
        "語料，加入訓練以擴充表達與句型覆蓋。本題「不新增真實語料」可理解為"
        "不再蒐集人工配對資料，仍允許從既有語料生成合成樣本。"
    ),
    "answerReason": (
        "B 唯一直接增加訓練樣本的多樣性而不要求新增人工真實平行語料，能降低"
        "模型只記住一萬筆資料的傾向。A 擴大容量通常更易過擬合，C 只壓縮部分"
        "參數且破壞性較高，D 全凍結則限制目標語言適應能力。"
    ),
    "optionAnalysis": {
        "A": "把隱藏層擴至 1024 會增加參數與表徵容量；在資料已不足且明顯過擬合的條件下，更大模型通常更容易記憶訓練集，除非另有強正則化或大規模預訓練，方向與題意相反。",
        "B": "正確。反向翻譯用模型產生合成來源句，再與既有目標句配成偽平行樣本，擴增語句變化與監督訊號；這是低資源機器翻譯中利用單語或既有資料改善泛化的經典方法。",
        "C": "L1 正則化能促使權重稀疏，可能降低容量，但只對 embedding matrix 強力壓縮未必處理 Transformer 其他層的過擬合，且可能直接損傷稀有詞表徵；相較資料增強不是最適選擇。",
        "D": "凍結部分預訓練層可減少可訓練參數並保留通用知識，但把所有 Transformer 層全部凍結會使模型難以適應該少數語言的詞法與句法；它是極端限制，不如合成資料增強直接。",
    },
    "trap": "題目要同時滿足「不新增真實語料」與「提升泛化」；合成偽語料並未違反前者。擴大模型容量、壓縮單一矩陣或全部凍結，都不能像資料增強一樣直接增加訓練變化。",
    "editorialNote": "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。反向翻譯通常仍需目標語言單語資料或既有句子；本題依「不新增真實語料」解作不新增人工蒐集／標註資料，而非禁止使用題內既有語料產生合成樣本。",
    "references": [
        exam_ref(19),
        ref("Improving Neural Machine Translation Models with Monolingual Data", "https://arxiv.org/abs/1511.06709", "Abstract 與方法：以反向翻譯將單語目標句轉成合成來源句，加入平行訓練資料"),
    ],
}

DRAFTS[20] = {
    "summary": "正確答案是 B。WGAN 以 Wasserstein 距離導出的目標取代原始 GAN 的分類式損失，提供較平滑且有意義的訓練訊號，是緩解模式崩潰的代表性方法。",
    "concept": (
        "模式崩潰（Mode Collapse）是生成器把許多不同潛在向量映射成少數相似"
        "輸出，雖能騙過鑑別器卻未涵蓋真實分布的多種模式。原始 GAN 在鑑別器"
        "過強或兩分布支撐幾乎不重疊時，生成器梯度可能不穩。Wasserstein GAN "
        "以 Earth-Mover／Wasserstein-1 距離對應的 critic 目標提供較連續的品質"
        "訊號，改善訓練穩定與模式覆蓋；實作還必須滿足 critic 的 Lipschitz 約束。"
    ),
    "answerReason": (
        "B 是針對原始 GAN 目標函數與梯度品質的經典替代方案，WGAN 論文也報告"
        "更穩定訓練並減輕模式崩潰，因此是本題官方答案。其他方法可能在特定架構"
        "有幫助，但不是選項中最具代表性的完整解法。"
    ),
    "optionAnalysis": {
        "A": "梯度懲罰可用來滿足 WGAN critic 的 Lipschitz 約束，WGAN-GP 確實能提升穩定性；但若只說在一般鑑別器加入懲罰，未交代 Wasserstein critic 目標，主要是在限制梯度，並不如 B 直接指出完整的 WGAN 損失替代。",
        "B": "正確。WGAN 將二元真假分類目標改為估計 Wasserstein-1 距離的 critic 差異，使真實與生成分布即使支撐不重疊仍可獲得較有用梯度，常用來改善訓練不穩與模式崩潰。",
        "C": "GAN 本來就從隨機潛在向量取樣；額外加入無結構噪音只會改變取樣擾動，若生成器已把大範圍輸入映射到同一模式，噪音仍可能得到相似臉孔，沒有直接約束模式覆蓋。",
        "D": "多尺度鑑別器能同時檢查局部細節與全域結構，常用於提升不同解析尺度的影像品質；它未必要求生成器覆蓋資料分布中不同身份、姿態等模式，故不是模式崩潰的通用首選。",
    },
    "trap": "WGAN 與 gradient penalty 不是互斥概念：WGAN-GP 正是用梯度懲罰實作 Lipschitz 約束。考題要比較選項完整性時，B 指出核心損失；A 若未限定 WGAN critic，只是較局部的穩定化描述。",
    "editorialNote": "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。A 的梯度懲罰若特指 WGAN-GP，也屬常見且有效的訓練穩定方法，因此題目存在解釋空間；本站仍依官方答案 B 判定，待人工複核題目所依教材的用語與層級。",
    "references": [
        exam_ref(20),
        ref("Wasserstein GAN", "https://arxiv.org/abs/1701.07875", "Abstract 與理論：以較有意義且平滑的距離改善 GAN 學習穩定，並討論 mode collapse"),
        ref("Improved Training of Wasserstein GANs", "https://arxiv.org/abs/1704.00028", "Abstract 與第 4 節：以 gradient penalty 取代 weight clipping 來施加 Lipschitz 約束，改善多種 GAN 架構訓練"),
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
