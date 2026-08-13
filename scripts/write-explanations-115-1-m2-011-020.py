"""Write draft explanations for 115-1 intermediate subject two, Q11-Q20."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-intermediate-1-big-data"
AUTHOR = "Codex（AI 輔助初稿）"
AUTHORED_AT = "2026-08-12"
CHECKED_AT = "2026-08-12"
EXAM_PDF = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/115年第一次中級AI應用規劃師_"
    "第二科_大數據處理分析與應用_公告試題_20260615003426.pdf"
)
DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def exam_ref(number: int) -> dict:
    return {
        "title": "115 年第一次中級 AI 應用規劃師－大數據處理分析與應用公告試題",
        "url": EXAM_PDF,
        "locator": f"第 {number} 題題幹、選項與官方答案",
        "checkedAt": CHECKED_AT,
    }


def ref(title: str, url: str, locator: str) -> dict:
    return {"title": title, "url": url, "locator": locator, "checkedAt": CHECKED_AT}


EXPECTED_ANSWER = {
    11: "C", 12: "C", 13: "B", 14: "C", 15: "C",
    16: "A", 17: "D", 18: "D", 19: "D", 20: "B",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[11] = {
    "summary": "正確答案是 C。有序評價適合序數編碼；無序縣市在羅吉斯迴歸中宜做 One-Hot，而 XGBoost 可使用原生類別特徵。",
    "concept": (
        "有序類別具有可排列等級，例如非常不滿意到非常滿意，可映射為遞增整數；"
        "無序類別如縣市沒有合理大小順序。線性模型若把縣市直接編成整數，會錯誤"
        "引入線性距離，因此常用 One-Hot；含截距模型可 drop first 避免完全共線。"
        "新版 XGBoost 可將 pandas category 欄位搭配 enable_categorical 交給樹模型"
        "使用其類別切分，而不需虛構順序。"
    ),
    "answerReason": (
        "C 同時尊重兩項特徵的量尺與兩種模型的處理能力。A 遺失客服評價的順序"
        "效率；B 在切分前用答案衍生續約率造成 target leakage，還替縣市製造順序；"
        "D 也有目標編碼洩漏風險且 PCA 不適合拿來解釋無序類別。"
    ),
    "optionAnalysis": {
        "A": (
            "One-Hot 能安全表示兩項類別，並非完全不能用；但客服評價的五級順序"
            "會被拆成互不相關欄位，線性模型無法直接利用等級結構，XGBoost 也會"
            "產生較多稀疏欄位，因此不是最適方案。"
        ),
        "B": (
            "客服評價做 Ordinal 合理，但縣市的歷史續約率是由目標計算；若在資料"
            "切分前使用全部樣本，驗證目標會滲入特徵。XGBoost 對無序縣市直接"
            "Ordinal 也會加入不存在的大小關係。"
        ),
        "C": (
            "正確。Logistic Regression 以序數值保留評價順序、以 One-Hot 表示"
            "無序縣市；XGBoost 可保留評價序數，並以 category dtype 與"
            "enable_categorical 對縣市做原生類別切分。"
        ),
        "D": (
            "平均續約率編碼同樣必須只由訓練折計算並做平滑，選項沒有此防漏設計。"
            "對 One-Hot 後欄位做 PCA 會形成難解釋的連續組合，也非 22 類縣市"
            "的必要處理。"
        ),
    },
    "trap": (
        "先判斷類別是否有順序，再看模型能力。任何利用續約結果的 target encoding"
        "都必須在訓練資料內、交叉驗證每一折內估計，不能在切分前計算。"
    ),
    "references": [
        exam_ref(11),
        ref(
            "scikit-learn－Encoding categorical features",
            "https://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features",
            "OrdinalEncoder 將類別轉為整數；OneHotEncoder 建立無序類別的二元欄位",
        ),
        ref(
            "XGBoost－Categorical Data 官方教學",
            "https://xgboost.readthedocs.io/en/stable/tutorials/categorical.html",
            "DataFrame category dtype、enable_categorical=True 與類別切分使用方式",
        ),
    ],
}

DRAFTS[12] = {
    "summary": "正確答案是 C。chunksize 會回傳可逐批迭代的資料區塊，避免一次把 50GB CSV 全部載入記憶體。",
    "concept": (
        "pandas.read_csv 設定 chunksize=N 後會建立 TextFileReader，每次迭代讀取約"
        "N 列 DataFrame。工程師可對每批進行清理、聚合或輸出，再釋放該批記憶體，"
        "使峰值用量受 chunk 大小控制。這與只讀取資料子集不同：妥善迭代仍能"
        "處理完整 50GB 檔案。"
    ),
    "answerReason": (
        "C 直接將完整資料的處理改為串流式分批載入，是不換框架下最通用的 OOM"
        "解法。A 會漏掉其餘資料；B 的 usecols 不接受 0.5 隨機比例；D 合理指定"
        "較小 dtype 可降低用量，但未必足以容納 50GB，且仍試圖一次載入。"
    ),
    "optionAnalysis": {
        "A": (
            "nrows=10000 只讀取開頭一萬列，適合試讀 schema 或抽查，卻沒有處理"
            "剩餘資料。它避免 OOM 的代價是捨棄絕大多數訓練資料，不符合完整"
            "前處理需求。"
        ),
        "B": (
            "usecols 要求欄名、欄索引清單或可呼叫函式，不是 0.5 這種抽樣比例，"
            "也不會隨機選一半欄位。即使挑選必要欄位可省記憶體，此參數寫法仍無效。"
        ),
        "C": (
            "正確。chunksize=10000 讓程式逐批取得 DataFrame；每批完成轉換或"
            "彙總後再讀下一批，可遍歷全部檔案而不保留完整資料於 RAM。"
        ),
        "D": (
            "指定 dtype 能避免自動推斷出過寬型別，例如把可用 int32 的欄位存成"
            "int64，確實是輔助最佳化；但檔案遠超 RAM 時，僅縮小每列通常仍無法"
            "保證一次載入成功。"
        ),
    },
    "trap": (
        "要區分『少讀資料』與『分批讀完整資料』。chunksize 解決峰值記憶體，"
        "但跨批次排序、去重或全域標準化仍需設計累積統計或外部中間結果。"
    ),
    "references": [
        exam_ref(12),
        ref(
            "pandas－read_csv 官方文件",
            "https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html",
            "chunksize 回傳 TextFileReader 供迭代；nrows、usecols 與 dtype 參數定義",
        ),
        ref(
            "pandas－Scaling to large datasets 官方指南",
            "https://pandas.pydata.org/docs/user_guide/scale.html",
            "使用 chunking 處理大於記憶體的資料，並說明可分塊演算法的限制",
        ),
    ],
}

DRAFTS[13] = {
    "summary": "正確答案是 B。依工作負載分別使用文件、向量與關聯式資料庫，最能同時滿足彈性商品結構、向量搜尋及低延遲 ACID 庫存。",
    "concept": (
        "Polyglot persistence 是依不同資料模型與一致性需求選擇儲存引擎。文件型"
        "資料庫適合欄位可變、巢狀的商品文件；向量資料庫針對高維向量建立近似"
        "最近鄰索引並提供相似度查詢；關聯式資料庫則以交易、約束及鎖定維護"
        "庫存一致性。代價是需設計資料同步、權威來源與跨系統失敗處理。"
    ),
    "answerReason": (
        "B 讓每個服務使用最符合其主要需求的資料庫，避免單一引擎同時承擔三種"
        "截然不同的工作負載。A 技術上可能透過擴充實現，但在題目指定高 QPS"
        "專用向量搜尋下不如專用架構；C、D 無法可靠保證庫存交易一致性。"
    ),
    "optionAnalysis": {
        "A": (
            "現代關聯式資料庫可支援 JSON、向量擴充與列鎖，規模合適時確實可簡化"
            "維運；但將 PB 級彈性文件、高 QPS 1,536 維 ANN 與低延遲交易都集中"
            "在同一系統，資源競爭與專用索引能力較難最佳化。"
        ),
        "B": (
            "正確。文件庫保留商品 schema 彈性，向量庫提供專用索引與相似度查詢，"
            "關聯庫用交易與鎖確保庫存扣減；這是依存取模式拆分的合理架構。"
        ),
        "C": (
            "文件庫很適合商品資料，但不是所有產品都能提供專用向量引擎的高 QPS"
            "能力；更重要的是，僅為統一技術棧就把嚴格庫存交易交給不合適的一致性"
            "模型，會提高超賣風險。"
        ),
        "D": (
            "搜尋引擎適合全文檢索與部分向量搜尋，卻通常不是庫存扣減的交易權威"
            "來源。文件更新與索引刷新不能取代關聯式交易的原子條件更新與一致性保證。"
        ),
    },
    "trap": (
        "不要因單一產品『也能做』某功能就忽略主要工作負載。選 B 仍需承認其"
        "代價：跨庫同步、最終一致性、備援與監控都必須明確設計。"
    ),
    "references": [
        exam_ref(13),
        ref(
            "MongoDB－Data Modeling 官方文件",
            "https://www.mongodb.com/docs/manual/data-modeling/",
            "文件資料模型可嵌入相關資料並支援彈性 schema 的設計原則",
        ),
        ref(
            "PostgreSQL－Transactions 官方文件",
            "https://www.postgresql.org/docs/current/tutorial-transactions.html",
            "交易將多個步驟形成 all-or-nothing 操作，並在並行更新下維持一致狀態",
        ),
        ref(
            "Milvus－Index Explained 官方文件",
            "https://milvus.io/docs/index-explained.md",
            "向量索引用於加速高維向量相似度搜尋，並比較精確與近似搜尋取捨",
        ),
    ],
}

DRAFTS[14] = {
    "summary": "正確答案是 C。Sharding 將資料列按分片鍵水平分散到多個節點，以擴充容量與分攤查詢、寫入負載。",
    "concept": (
        "水平分割保留相同 schema，將不同資料列分派到不同 shard；例如依客戶 ID"
        "雜湊或範圍決定節點。當資料與請求超出單機能力時，可增加 shard 擴充"
        "儲存和計算。良好分片鍵應分布均勻並貼合查詢模式，否則會出現熱點、"
        "跨 shard 查詢與重新平衡成本。"
    ),
    "answerReason": (
        "C 正是分片的定義與主要目的。A 描述 replication，B 描述快取或物化"
        "檢視，D 描述 compression；這些技術可和分片並用，但不等於把資料水平"
        "分配到多台機器。"
    ),
    "optionAnalysis": {
        "A": (
            "增加相同資料副本是複寫，可提高可用性與讀取容錯，但每個副本仍可能"
            "保存全部資料。Sharding 的各節點主要持有不同資料子集，解決容量與"
            "負載的水平擴展。"
        ),
        "B": (
            "預先計算結果屬物化檢視、彙總表或快取，可降低特定重複查詢延遲。"
            "它不會把原始 PB 級資料依分片鍵拆到多個節點。"
        ),
        "C": (
            "正確。每個 shard 保存部分資料列並承擔相應讀寫，新增節點可提高"
            "總容量與吞吐量；路由層依 shard key 將請求送往正確節點。"
        ),
        "D": (
            "壓縮用較少位元保存相同資訊，可節省空間與 I/O，但資料仍可能集中"
            "在單一節點。它不提供跨節點負載均衡，也不是 sharding 的定義。"
        ),
    },
    "trap": (
        "分片與複寫常一起部署但目的不同：分片分散『不同資料』以擴展；複寫保留"
        "『相同資料』副本以提高可用性與讀取能力。"
    ),
    "references": [
        exam_ref(14),
        ref(
            "MongoDB－Sharding 官方文件",
            "https://www.mongodb.com/docs/manual/sharding/",
            "Sharding 將資料分散到多台機器，以支援大型資料集及高吞吐量操作",
        ),
    ],
}

DRAFTS[15] = {
    "summary": "正確答案是 C。固定特徵快取並反覆使用完全相同樣本只提升吞吐量，不增加訓練變化，可能讓模型更容易記憶資料。",
    "concept": (
        "過度擬合是模型對訓練資料表現極佳，卻無法泛化到未見資料。資料層面可"
        "透過標籤保持的隨機增強、擴充真實場景及清除錯標來改善訊號與涵蓋範圍。"
        "若把增強前的固定特徵永久快取，之後每個 epoch 只重播相同表示，計算"
        "雖快卻沒有新資訊；持續訓練反而可能加深記憶。"
    ),
    "answerReason": (
        "題目問最無法改善甚至惡化的資料處理調整，C 只優化 throughput，並讓"
        "相同資料重複曝光。A、B 增加有效變化，D 降低標註噪音，三者在方法正確"
        "時都可能縮小訓練與驗證落差。"
    ),
    "optionAnalysis": {
        "A": (
            "動態裁切、翻轉、色彩擾動等若保留瑕疵標籤，每個 epoch 可看到不同"
            "版本，等同加入合理不變性並降低記住單一像素配置的機會，通常能改善泛化。"
        ),
        "B": (
            "增加不同產線、光照、相機與瑕疵型態的真實影像，可擴大訓練分布並"
            "減少取樣偏差。新資料需維持品質與標註一致，但方向能直接改善泛化。"
        ),
        "C": (
            "正確。固定快取可省去重複特徵計算，卻不創造新場景；若因此停用動態"
            "增強並增加重播次數，模型更容易記住同一組特徵，過擬合可能惡化。"
        ),
        "D": (
            "錯標或低品質影像會提供矛盾訊號，清理後可讓訓練目標更一致。不過"
            "應先訂定品質標準並避免只刪難例，否則可能縮窄真實資料分布。"
        ),
    },
    "trap": (
        "訓練管線更快不代表模型泛化更好。快取本身不是錯，關鍵是快取後是否仍"
        "有隨機增強，以及反覆訓練是否只讓模型更熟悉同一組固定表示。"
    ),
    "references": [
        exam_ref(15),
        ref(
            "TensorFlow－Data augmentation 官方教學",
            "https://www.tensorflow.org/tutorials/images/data_augmentation",
            "以會產生可信影像的隨機轉換增加訓練資料多樣性，且增強只於訓練期啟用",
        ),
        ref(
            "TensorFlow－Better performance with tf.data 官方指南",
            "https://www.tensorflow.org/guide/data_performance",
            "cache 會在第一個 epoch 後重用元素；若要隨機變換每次迭代，cache 與 map 的順序會影響結果",
        ),
    ],
}

DRAFTS[16] = {
    "summary": "正確答案是 A。SVD 可分解任意 m×n 矩陣，不限於行列數相等的方陣。",
    "concept": (
        "對任意實數矩陣 A∈R^(m×n)，SVD 可寫為 A=UΣVᵀ；U、V 的欄向量分別"
        "是左右奇異向量，Σ 含非負奇異值。保留最大的 k 個奇異值與相應向量可"
        "得到最佳的秩 k 近似之一。LSA 將此方法套到詞—文件矩陣，PCA 也可透過"
        "對中心化資料矩陣做 SVD 來計算主成分。"
    ),
    "answerReason": (
        "A 把 SVD 錯誤限制為方陣，因此是不正確敘述。使用者—商品、詞—文件"
        "矩陣通常正是長方形，仍可分解。B 是截斷 SVD，D 是 LSA 的典型方法；"
        "C 所要表達的是 SVD 適用矩陣更一般，PCA 可由中心化資料的 SVD 求得。"
    ),
    "optionAnalysis": {
        "A": (
            "正確選項（題目問不正確）。SVD 對 m×n 長方形矩陣同樣存在；完整或"
            "縮減形式只會改變 U、Σ、V 的尺寸，不要求 m=n。"
        ),
        "B": (
            "正確敘述。將奇異值由大到小排列，只保留前 k 組奇異向量，可形成"
            "低秩近似，常用於壓縮、去噪與降維。"
        ),
        "C": (
            "就矩陣分解適用範圍而言可成立：SVD 直接作用於一般矩陣；PCA 對"
            "中心化資料尋找最大變異方向，可由資料矩陣的 SVD 或共變異數矩陣"
            "特徵分解求得。"
        ),
        "D": (
            "正確敘述。LSA 對詞—文件矩陣做截斷 SVD，把詞與文件投影到較低維"
            "潛在空間，使共現模式相似的詞或文件獲得相近表示。"
        ),
    },
    "trap": (
        "特徵分解通常針對方陣，SVD 則可直接處理長方形矩陣。另注意 PCA 要先"
        "依定義中心化資料；不能把未中心化的任意 SVD 結果一律稱為 PCA。"
    ),
    "editorialNote": (
        "官方答案 A 明確錯誤。C 的『PCA 可視為對共變異數矩陣進行特殊 SVD』"
        "是簡化說法：對稱共變異數矩陣可做特徵分解，也可做 SVD；實務 PCA"
        "常直接對中心化資料矩陣做 SVD，避免顯式形成共變異數矩陣。"
    ),
    "references": [
        exam_ref(16),
        ref(
            "NumPy－numpy.linalg.svd 官方文件",
            "https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html",
            "對形狀 (..., M, N) 的一般矩陣進行奇異值分解，並說明 full/reduced 形式尺寸",
        ),
        ref(
            "scikit-learn－TruncatedSVD 官方文件",
            "https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html",
            "截斷 SVD 用於降維；套於 term count 或 TF-IDF 矩陣時稱為 latent semantic analysis",
        ),
    ],
}

DRAFTS[17] = {
    "summary": "正確答案是 D。此 ICU 時序問題需同時處理缺失模式、感測器漂移、標註誤差、病患基準差異、病患分組驗證與少數類指標。",
    "concept": (
        "臨床時序資料的缺失本身可能含資訊，短缺口可前向填補並加入 missingness"
        " indicator；長缺口則需限制填補跨度。感測器漂移要依時間與裝置校正，"
        "而非只做全域縮放。多次觀測屬同一病患，若隨機切分會讓病患特徵外洩到"
        "測試集。敗血症僅 3.2% 時，PR-AUC 與 recall 比 accuracy 更能反映少數類。"
    ),
    "answerReason": (
        "D 是唯一同時針對題幹每項問題提出相符處理的方案：保留缺失訊號、以"
        "滾動穩健統計校正漂移、處理時間標註雜訊、按病患建模與分組驗證，並用"
        "PR-AUC/Recall 評估。A、B、C 各自留下嚴重偏差或資料洩漏。"
    ),
    "optionAnalysis": {
        "A": (
            "整體平均會抹去個別病患與時序變化，且未處理系統性漂移；任意擴大"
            "標註區間可能增加錯標。ROC-AUC 可報告，但在 3.2% 盛行率下不能單獨"
            "反映陽性預測品質。"
        ),
        "B": (
            "線性插值可處理短且變化平滑的缺口，但 10–30 分鐘未必都合理；Z-score"
            "只重新縮放，不能修正隨時間偏高的漂移。最嚴重的是隨機切分讓同病患"
            "資料同時出現在訓練與測試，造成洩漏。"
        ),
        "C": (
            "刪除所有缺失列可能系統性排除病況較重或監測中斷的時段；Min-Max"
            "不處理漂移與病患基準差異。Accuracy 在 3.2% 陽性下可能被一律預測"
            "陰性的模型灌高，分層 K-Fold 也未保證病患隔離。"
        ),
        "D": (
            "正確。前向填補搭配缺失指標保留觀測狀態，滾動中位數對極端值較穩健"
            "並追蹤基線；病患分組避免洩漏，PR-AUC 與 recall 則聚焦稀少敗血症。"
        ),
    },
    "trap": (
        "這是組合題，不能只看其中一項合理措施。尤其要抓出兩個硬傷：隨機切分"
        "重複病患會洩漏；高度不平衡時只看 accuracy 或 ROC-AUC 可能過度樂觀。"
    ),
    "editorialNote": (
        "本站依官方答案 D 撰寫，但 D 仍是原則性方案。前向填補須設定最大允許"
        "缺口，72 小時滾動中位數的窗口也應依感測器校正紀錄與臨床變化驗證；"
        "標註誤差不可僅靠任意擴窗，宜做敏感度分析或弱標籤建模。"
    ),
    "references": [
        exam_ref(17),
        ref(
            "scikit-learn－GroupKFold 官方文件",
            "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html",
            "同一 group 不會同時出現在訓練與測試折，適合以病患 ID 分組",
        ),
        ref(
            "scikit-learn－Precision-Recall 官方文件",
            "https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html",
            "在類別高度不平衡時，precision-recall 可反映正例預測成功程度",
        ),
        ref(
            "Lipton et al., Learning to Diagnose with LSTM Recurrent Neural Networks（2016）",
            "https://arxiv.org/abs/1511.03677",
            "臨床多變量時序建模及缺失值處理背景，說明 ICU 訊號具有時間依賴與缺失問題",
        ),
    ],
}

DRAFTS[18] = {
    "summary": "正確答案是 D。Lift 等於聯合機率除以邊際機率乘積；1 表示獨立，小於 1 為負關聯，大於 1 為正關聯。",
    "concept": (
        "對規則 A→B，support(A∪B)=P(A∩B)，confidence=P(B|A)=P(A∩B)/P(A)，"
        "lift=confidence/P(B)=P(A∩B)/(P(A)P(B))。Lift 用 B 的基準發生率校正"
        "confidence，因此能判斷共同購買是否超過獨立情況的預期；其下限為 0，"
        "上限不固定為 1。"
    ),
    "answerReason": (
        "D 的 lift 閾值解讀正確，是四項中唯一可選者。A 把 support 說成 confidence，"
        "B 又把 confidence 說成 support；C 的公式正確但錯誤限制範圍為 [0,1]，"
        "lift 可以大於 1。"
    ),
    "optionAnalysis": {
        "A": (
            "P(A∩B) 是項目集 {A,B} 的 support，不是規則 A→B 的 confidence。"
            "Confidence 要以 A 出現的交易為分母，即 P(B|A)。"
        ),
        "B": (
            "P(B|A) 是 confidence，表示買 A 的交易中有多少也買 B。Support 則以"
            "全部交易為分母，計算 A 與 B 同時出現的比例。"
        ),
        "C": (
            "公式正確，但範圍敘述錯誤。若 A、B 的共同出現遠高於獨立預期，分子"
            "可大於 P(A)P(B)，lift 就會超過 1，且沒有固定上限 1。"
        ),
        "D": (
            "正確。Lift=1 代表觀察到的共現率等於獨立預期；小於 1 表示互相抑制，"
            "大於 1 表示正向關聯。比較規則時仍須同看 support、樣本量與業務意義。"
        ),
    },
    "trap": (
        "三個公式要分清：support 看全體共現，confidence 看 A 發生後 B 的比例，"
        "lift 再除以 B 的基準率。Lift 大於 1 不代表存在因果關係。"
    ),
    "editorialNote": (
        "官方答案 D 的最後一句『提升度並非數值愈大即代表關聯愈強』需限定解讀。"
        "在固定方向與可靠樣本量下，較大的 lift 確實代表相對獨立基準更強的正向"
        "關聯；但稀有項目可產生高 lift 卻 support 很低，且 lift 不代表因果或"
        "商業價值，所以不可脫離 support 與樣本數單獨排序。"
    ),
    "references": [
        exam_ref(18),
        ref(
            "mlxtend－Association Rules 官方文件",
            "https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/association_rules/",
            "support、confidence、lift 的公式；lift=1 為獨立，<1 與 >1 的解讀",
        ),
    ],
}

DRAFTS[19] = {
    "summary": "正確答案是 D。附圖 8 筆訂單中，{B,E} 同時出現 4 次，是達最低支援計數 3 的最大頻繁項目集。",
    "concept": (
        "Apriori 先找支援計數達門檻的 1-itemsets，再組合候選 2-itemsets；若某"
        "項目集不頻繁，其所有超集合依 Apriori 性質也不可能頻繁。『最大頻繁"
        "項目集』在本題指無法再加入其他項目仍保持支援計數至少 3 的頻繁集合，"
        "不是單看元素最多的候選或最高頻率單項。"
    ),
    "answerReason": (
        "目視附圖交易為 ABE、CD、BDE、ABE、BCE、AD、A、AD。{B,E} 出現在"
        "第 1、3、4、5 筆，共 4 次；{A,D} 只出現第 6、8 筆共 2 次，{A,B,E}"
        "只出現第 1、4 筆共 2 次。故達門檻且最大的選項是 D。"
    ),
    "optionAnalysis": {
        "A": (
            "{A} 出現在第 1、4、6、7、8 筆，支援計數 5，確實頻繁；但它還可"
            "擴展嗎要看候選。選項中另有包含兩項且達門檻的 {B,E}，所以只選"
            "單項 {A} 不是本題最大頻繁項目集。"
        ),
        "B": (
            "{A,D} 只在第 6 與第 8 筆同時出現，支援計數為 2，低於最低支援度"
            "（計數）3，因此在 2-itemset 階段就會被剪除。"
        ),
        "C": (
            "{A,B,E} 僅出現在第 1、4 筆，支援計數為 2；雖然其中子集 {B,E}"
            "頻繁，但三項合併後未達門檻，不能保留。"
        ),
        "D": (
            "正確。{B,E} 同時出現在第 1、3、4、5 筆，支援計數 4≥3；將 A、C"
            "或 D 加入後都不到 3 次，因此它是無法再擴展的最大頻繁項目集。"
        ),
    },
    "trap": (
        "題目寫最低支援度為 3，實際是支援『計數』門檻，不是 3%。逐筆交集計數"
        "後還要區分 frequent、maximal frequent 與單純項目數最多的候選。"
    ),
    "editorialNote": (
        "已於 2026-08-12 目視官方附圖：8 筆訂單依序為 {A,B,E}、{C,D}、"
        "{B,D,E}、{A,B,E}、{B,C,E}、{A,D}、{A}、{A,D}。圖表與題庫文字"
        "及官方答案 D 一致；本站仍維持 draft，待獨立人工複核。"
    ),
    "references": [
        exam_ref(19),
        ref(
            "scikit-learn User Guide－Frequent Itemsets via the Apriori Algorithm",
            "https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/apriori/",
            "Apriori 依 min_support 產生頻繁項目集，並回傳 itemsets 與 support",
        ),
        ref(
            "Agrawal & Srikant, Fast Algorithms for Mining Association Rules（1994）",
            "https://www.vldb.org/conf/1994/P487.PDF",
            "第 2 節：Apriori 利用頻繁項目集的子集性質產生與剪除候選集合",
        ),
    ],
}

DRAFTS[20] = {
    "summary": "正確答案是 B。若模型永遠猜正常仍有 99.5% Accuracy，卻完全找不到詐欺，顯示整體準確率會被多數類主導。",
    "concept": (
        "Accuracy=(TP+TN)/全部樣本，在類別極度不平衡時，大量正常交易的 TN"
        "會壓過少數詐欺的 FN。若全部預測正常，10,000 筆中約 9,950 筆仍答對，"
        "Accuracy 為 99.5%，但詐欺 recall=TP/(TP+FN)=0。模型選擇應至少搭配"
        "混淆矩陣、詐欺類 precision/recall、PR-AUC 與業務成本。"
    ),
    "answerReason": (
        "B 用數字精確呈現 accuracy paradox，是本題最嚴重且最直接的風險。類別"
        "不平衡本身不必然使訓練變慢、梯度爆炸或直接造成過擬合；A、C、D 都把"
        "可能與其他因素相關的現象說成必然因果。"
    ),
    "optionAnalysis": {
        "A": (
            "訓練時間主要由樣本量、模型複雜度、特徵及硬體決定；比例不平衡可能"
            "需要重採樣或調參，但不會單憑 99.5:0.5 就必然大幅增加每步運算。"
        ),
        "B": (
            "正確。一律預測正常可答對所有 99.5% 正常交易，卻把 0.5% 詐欺全部"
            "漏掉，使詐欺 TP=0、FN 為全部詐欺，因此 recall 為 0。"
        ),
        "C": (
            "梯度爆炸常與深網路、循環連乘、初始化或學習率有關。類別不平衡會"
            "讓損失由多數類主導，但不等同數值梯度必然爆炸。"
        ),
        "D": (
            "不平衡可能使模型偏向多數類，但過擬合是訓練表現與未見資料泛化的"
            "落差，兩者不是同義。即使測試集同樣不平衡，一律猜正常仍可能有高"
            "accuracy，問題在少數類失效而非必然整體下降。"
        ),
    },
    "trap": (
        "看到極端基準率先計算『全猜多數類』的 accuracy，再檢查少數類 recall。"
        "高 accuracy 不保證模型有偵測能力，也不能只換成 ROC-AUC 就忽略業務門檻。"
    ),
    "references": [
        exam_ref(20),
        ref(
            "scikit-learn－Classification metrics 官方文件",
            "https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics",
            "accuracy 與 precision、recall 公式及分類評估指標使用方式",
        ),
        ref(
            "scikit-learn－Precision-Recall 官方範例",
            "https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html",
            "高度不平衡分類中 precision-recall 衡量少數正類預測成功的方式",
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
