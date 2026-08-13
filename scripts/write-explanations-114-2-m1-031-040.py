"""Write draft explanations for 114-2 intermediate subject one, Q31-Q40.

The script verifies official answers and refuses to overwrite reviewed work.
Run the draft validator before applying it to the shared question bank.
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
    31: "B", 32: "D", 33: "C", 34: "D", 35: "A",
    36: "B", 37: "B", 38: "B", 39: "C", 40: "A",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[31] = {
    "summary": "正確答案是 B。將推論服務容器化並水平增加實例，可把約一萬個同時在途的請求分散處理；自動伸縮與多副本也能兼顧尖峰容量及單點故障。",
    "concept": (
        "依 Little's Law 粗估，若到達率是每秒 10,000 個請求、每請求平均停留一秒，"
        "穩態下約有 10,000 個請求同時在系統內。高流量推論因此需要多個無狀態服務"
        "副本，由負載平衡器分流，並依併發量、佇列長度或資源指標水平擴展。容器可"
        "固定依賴環境，多可用區副本、健康檢查及滾動更新則降低單點故障。自動伸縮"
        "仍需預留暖機時間與最小副本，不能只靠尖峰發生後才擴容。"
    ),
    "answerReason": (
        "B 同時處理容量與可用性：水平增加服務實例能將高併發分散到多台節點，"
        "Auto Scaling 可隨負載調整副本數，而任何單一副本失效時仍有其他副本服務。"
        "其餘方案不是形成單點，就是以拒絕需求或高延遲換取不過載。"
    ),
    "optionAnalysis": {
        "A": "垂直擴展可提高單機吞吐量，但硬體有上限且升級通常需要停機；所有流量集中於一台伺服器也形成單點故障，無法符合高可用性與尖峰彈性兩項要求。",
        "B": "正確。多個容器化服務副本可由負載平衡器平行處理請求，水平自動伸縮依觀測負載增加或縮減副本；配合健康檢查與跨節點部署，也能在個別實例故障時維持服務。",
        "C": "限制併發能保護後端免於資源耗盡，適合作為背壓或最後防線；但它會排隊或拒絕超過上限的請求，並未提供題目要求的 10,000 RPS 處理能力，也不增加可用副本。",
        "D": "批次推論可提高 GPU 吞吐量，但一次等待湊齊上千筆會增加單筆延遲與記憶體需求；動態批次可作輔助最佳化，卻不能單獨消除伺服器故障或取代水平容量規劃。",
    },
    "trap": "吞吐量、延遲與可用性要分開看：批次可能改善吞吐量但增加等待時間，限流只保護系統，單機升級仍有故障點；多副本水平伸縮才同時回應容量與可用性。",
    "references": [
        exam_ref(31),
        ref("Kubernetes Documentation－Horizontal Pod Autoscaling", "https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/", "HPA 依觀測指標調整 Deployment 等工作負載副本；水平擴展是增加 Pod 以配合需求"),
    ],
}

DRAFTS[32] = {
    "summary": "正確答案是 D。PSI 直接比較生產輸入特徵與訓練基準的分布差異，可在真實標籤與績效指標尚未回收前偵測資料漂移，是較前置的風險訊號。",
    "concept": (
        "模型效能衰退常來自生產資料分布偏離訓練資料。Population Stability Index "
        "（PSI）先把基準與目前樣本按相同區間分箱，再彙總各箱比例差與比例比值的"
        "對數，可量化特徵分布位移。它不需要真實標籤，所以能在標籤延遲的場景先"
        "發警報；但 PSI 只是資料漂移指標，不證明準確率必然下降，門檻也受樣本數、"
        "分箱與業務影響，警報後仍須查模型績效及資料品質。"
    ),
    "answerReason": (
        "題目要能「提早」預警模型效能下滑風險。D 監看模型實際輸入是否離開訓練"
        "分布，位於因果鏈較上游，且無須等正確答案標籤到齊；CPU、延遲主要反映"
        "服務健康，置信度變化則可能受校準影響，均不如輸入漂移直接。"
    ),
    "optionAnalysis": {
        "A": "CPU 與記憶體使用率能發現資源飽和、洩漏或容量不足，主要預警系統延遲與故障；即使資源完全正常，輸入族群改變仍可能使模型預測失準，因此不是模型效能衰退的最佳前置信號。",
        "B": "置信度分布變化可作 prediction drift 警訊，也可能反映輸入改變；但模型可能對錯誤答案仍高度自信，未校準分數也不等於正確率，故其診斷力通常不如逐特徵比對訓練基準。",
        "C": "平均延遲與百分位數是服務層級目標的重要指標，可發現網路、排程或資源問題；它衡量的是回應速度，不是預測是否正確，模型品質下降時 API 仍可能維持低延遲。",
        "D": "正確。對輸入特徵計算 PSI 可比較目前資料與開發／訓練基準的分布，資料族群或特徵來源改變時能在標籤回流前被偵測，作為進一步驗證效能的早期警報。",
    },
    "trap": "資料漂移、預測漂移、效能衰退與系統故障不是同一件事。PSI 能早期發現分布改變，但不能單獨斷言準確率下降；若有即時標籤，仍應直接監控任務指標。",
    "editorialNote": "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。PSI 是風險指標而非效能因果證明，且常見 0.1／0.25 門檻只是經驗值；本題依「提早發現風險」與官方答案 D 解讀。",
    "references": [
        exam_ref(32),
        ref("SAS Model Manager User's Guide－Population Stability", "https://documentation.sas.com/api/docsets/mdlmgrug/v_026/content/mdlmgrug.pdf?locale=en", "Performance Monitoring 章：PSI 衡量特徵分布相對基準隨時間改變的程度"),
        ref("The Population Accuracy Index: A New Measure of Population Stability for Model Monitoring", "https://www.mdpi.com/2227-9091/7/2/53", "第 1.2 節：PSI 用於監控目前資料相對模型開發資料的分布位移，並討論其限制"),
    ],
}

DRAFTS[33] = {
    "summary": "正確答案是 C。Skip-gram 以每次出現的中心詞預測周邊詞，會直接更新該中心詞的表示；相較把上下文平均後預測中心詞的 CBOW，通常更能學到罕見詞關係。",
    "concept": (
        "Word2Vec 有兩種主要架構。Continuous Bag-of-Words（CBOW）將多個上下文"
        "詞的表示合併，用來預測中心詞，計算較快且對高頻規律平滑；Skip-gram 則"
        "反過來以中心詞逐一預測窗口內的上下文詞，使低頻中心詞每次出現都產生多個"
        "訓練配對。原始 Word2Vec 延伸工作搭配 negative sampling 與高頻詞 subsampling，"
        "能在大型語料有效學習詞向量；罕見詞仍需有足夠上下文，方法不會憑空創造資訊。"
    ),
    "answerReason": (
        "題幹同時強調語料龐大與罕見詞語意。C 正確描述 Skip-gram 的方向：中心詞"
        "預測周圍詞，讓低頻詞有限的每次出現可貢獻多組上下文關係，是四個選項中"
        "最符合需求的策略。"
    ),
    "optionAnalysis": {
        "A": "Skip-gram 的架構方向雖適合，但神經詞向量本來通常就由隨機小值初始化；初始化不能特別加速高頻詞，也不是捕捉罕見詞的關鍵。真正有關的是中心詞產生多個上下文訓練配對。",
        "B": "CBOW 是以周圍詞預測中心詞，計算效率高，但把上下文表示合併會平滑掉部分細節；TF-IDF 是文件層級加權方法，並非標準 Word2Vec CBOW 目標的一部分，不能據此宣稱強化低頻詞表示。",
        "C": "正確。Skip-gram 對每個中心詞預測窗口內多個周圍詞，低頻詞只要出現，就能以其多組上下文更新向量；在大型語料下通常比 CBOW 更有利於學習少見詞的細緻關係。",
        "D": "CBOW 的確以周圍詞預測中心詞，且合併上下文有平滑效果；但它常偏重高頻模式，不能因此推論罕見詞表示更穩定。對題目指定的低頻詞關係，Skip-gram 更合適。",
    },
    "trap": "先記住預測方向：CBOW 是「上下文猜中心」，Skip-gram 是「中心猜上下文」。不要把 TF-IDF、初始化等其他技巧硬接成 Word2Vec 的核心低頻詞優勢。",
    "references": [
        exam_ref(33),
        ref("Efficient Estimation of Word Representations in Vector Space", "https://arxiv.org/abs/1301.3781", "第 3 節：CBOW 由上下文預測目前詞；Skip-gram 由目前詞預測前後詞"),
        ref("Distributed Representations of Words and Phrases and their Compositionality", "https://arxiv.org/abs/1310.4546", "方法：negative sampling 與高頻詞 subsampling 改善 Skip-gram 訓練效率與表示品質"),
    ],
}

DRAFTS[34] = {
    "summary": "正確答案是 D。全景分割同時對每個像素給予語義類別，並為可數物件標示不同實例身分，完整涵蓋道路、建築等背景與每一位行人。",
    "concept": (
        "語義分割為每個像素指派類別，但同類的多個物件共用同一標籤；實例分割"
        "則為每個可數物件產生獨立遮罩，通常著重人、車等 things，不要求把天空、"
        "道路等不可數背景 stuff 全部納入一致的像素分割。全景分割（Panoptic "
        "Segmentation）統一兩者：畫面每個像素都有類別，而 things 還有獨立 instance "
        "ID，因此輸出是一張完整且不重疊的場景解析圖。"
    ),
    "answerReason": (
        "題幹要求兩件事同時成立：每個像素都有物件類別，且同類物件彼此可區分。"
        "D 的全景分割正是語義分割與實例分割的統一任務，既涵蓋道路建築等背景，"
        "也把多位行人標成不同個體。"
    ),
    "optionAnalysis": {
        "A": "語義分割可做到每像素分類，適合標出道路、建築、行人類別；但所有行人像素通常都只是同一個「行人」類別，無法判斷哪一組像素屬於行人甲或行人乙。",
        "B": "物件偵測以邊界框定位並分類每個物件，可區分不同的行人實例；邊界框不是逐像素遮罩，也不會為整片道路、天空等背景提供完整像素標籤。",
        "C": "實例分割能為每位行人產生獨立像素遮罩，滿足同類個體區分；但其標準任務主要處理可數物件 instances，未必要求對道路、建築等所有背景像素提供統一且完整的語義結果。",
        "D": "正確。全景分割將 stuff 的每像素語義標籤與 things 的逐實例遮罩合併，讓每個像素都有類別，同時讓同類的行人、車輛各自具有不同實例識別。",
    },
    "trap": "題幹中的「每個像素」指向語義層次，「同類不同個體」指向實例層次；只滿足其中一半都不夠，兩者同時出現就要想到 panoptic segmentation。",
    "references": [
        exam_ref(34),
        ref("Panoptic Segmentation", "https://arxiv.org/abs/1801.00868", "Abstract 與任務定義：統一每像素類別的 semantic segmentation 與逐物件的 instance segmentation"),
    ],
}

DRAFTS[35] = {
    "summary": "正確答案是 A。CLIP 以大量圖文配對做對比式預訓練，使相符影像與文字在共同嵌入空間接近；把類別寫成文字提示後即可依相似度進行零樣本分類。",
    "concept": (
        "CLIP 分別以影像編碼器和文字編碼器產生向量，訓練時在一批圖文配對中提升"
        "正確配對的相似度、降低錯誤配對的相似度。推論時可把候選類別寫成提示句，"
        "比較影像向量與各文字向量的 cosine similarity，再選最相似類別；因此新"
        "任務不一定要再訓練專用分類頭。這是零樣本遷移，不等同自動生成自然語言"
        "標題；文字提示措辭與預訓練資料偏差仍會影響結果。"
    ),
    "answerReason": (
        "A 完整說出 CLIP 的訓練機制、表示空間與應用方式：圖文對比學習建立共同"
        "嵌入，文字提示成為類別描述，再以語意相似度識別影像，正好滿足不新增"
        "標註訓練資料的條件。"
    ),
    "optionAnalysis": {
        "A": "正確。CLIP 將影像與文字分別編碼到可比較的向量空間，以對比目標拉近正確圖文配對；分類時把類別名包成文字提示並比較相似度，即可執行零樣本影像分類與語意搜尋。",
        "B": "影像增強可提升視覺模型對裁切、顏色等變化的穩健性，擴散則通常指生成或去噪過程；這兩者不是 CLIP 以文字提示辨識新類別的關鍵，也沒有解釋圖文如何對齊。",
        "C": "傳統監督式影像分類會以標註類別訓練分類頭或 MLP，新增類別常需新增標註資料並再訓練；這與題目要求僅用文字提示進行無訓練資料的識別相反。",
        "D": "自迴歸影像字幕模型逐 token 生成描述，而 CLIP 是判別式雙編碼器，輸出圖文相似度而不是逐字生成標籤；它可用提示做分類，但不是 caption generator。",
    },
    "trap": "「以文字查圖」不代表模型會生成文字。CLIP 的核心是雙編碼器加相似度；零樣本分類是拿文字提示當候選類別，而非用自迴歸解碼器寫出影像描述。",
    "references": [
        exam_ref(35),
        ref("Learning Transferable Visual Models From Natural Language Supervision", "https://arxiv.org/abs/2103.00020", "Abstract、第 2.3 節與圖 1：圖文對比預訓練，利用文字類別提示進行零樣本預測"),
    ],
}

DRAFTS[36] = {
    "summary": "正確答案是 B。網格搜尋會列舉事先指定的學習率、樹深度與正則化係數組合，通常搭配交叉驗證逐組評分，符合題目所說的系統化測試多組設定。",
    "concept": (
        "超參數最佳化先定義搜尋空間，再以驗證程序估計每組設定的泛化表現。Grid "
        "Search 對離散網格做笛卡兒積並窮舉所有組合，流程完整、結果可重現，但維度"
        "或候選值增加時計算量呈乘法成長。Random Search 只抽樣部分組合，Bayesian "
        "Optimization 依歷次結果選下一點；Cross-Validation 則是評估候選設定的"
        "方法，不是決定要搜尋哪些組合的策略。"
    ),
    "answerReason": (
        "題幹用「多種模型設定」「多組超參數」「系統化測試」描述列舉式搜尋，"
        "B 的 Grid Search 正是對預先定義的參數網格逐組評估。實務上它常在每組"
        "內使用交叉驗證，所以 A 是配套評估法而非本題所問的搜尋法。"
    ),
    "optionAnalysis": {
        "A": "交叉驗證將資料輪流分成訓練折與驗證折，以較穩定地估計某個模型設定；它可以是 Grid Search 的內部評估機制，但單獨不規定或遍歷學習率、樹深度等候選組合。",
        "B": "正確。Grid Search 對 param_grid 中所有候選值做完整組合，逐一訓練並以指定評分及交叉驗證比較，正好對應題目的系統化測試與選出最穩定組合。",
        "C": "Random Search 從參數分布抽取固定數量組合，適合空間很大、希望以有限預算快速探索；它刻意不測完所有組合，與題幹強調的系統化多組列舉較不相符。",
        "D": "Bayesian Optimization 以代理模型利用過去試驗結果選擇下一組參數，通常能節省昂貴評估次數；題幹沒有提到動態、序列式或依歷次結果調整方向，因此不是最直接答案。",
    },
    "trap": "Grid Search 與 Cross-Validation 常一起出現在 `GridSearchCV`，但角色不同：前者產生候選參數組合，後者評估每組。題目若問「系統化搜尋參數組合」，答案是 Grid Search。",
    "references": [
        exam_ref(36),
        ref("scikit-learn API－GridSearchCV", "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html", "以交叉驗證對指定參數值進行 exhaustive search，最佳化 estimator 超參數"),
    ],
}

DRAFTS[37] = {
    "summary": "正確答案是 B。縮小每張 GPU 的本地 batch 會直接減少該卡需保存的輸入與中間 activation；再把不同資料 shard 分配給各 GPU，可維持多卡資料平行的整體吞吐量。",
    "concept": (
        "訓練 GPU 記憶體主要包含模型參數、梯度、optimizer state 與隨 batch size "
        "成長的中間 activation。模型架構固定時，降低每卡 micro-batch 是最直接的"
        "activation 降載方式；若要維持原本有效 batch，可搭配多 GPU 資料平行及"
        "gradient accumulation。Data sharding／DistributedSampler 讓各 rank 讀取不同"
        "樣本，避免重複訓練資料；它分散的是資料批次，不會自動把模型參數切片。"
    ),
    "answerReason": (
        "B 中真正直接降低單卡記憶體的是較小 batch，因為同一步要保留的樣本與"
        "activation 變少；資料分片則讓多張 GPU 各處理不同小批次，繼續利用多卡"
        "吞吐。其他選項不是改變單步記憶體，就是破壞訓練正確性。"
    ),
    "optionAnalysis": {
        "A": "減少資料集總筆數只縮短 epoch 或降低覆蓋，單一步驟仍用相同 batch 與模型時，GPU 同時保存的 tensor 大小不變；它還可能損失泛化能力，不能解決瞬時 OOM。",
        "B": "正確。較小的 per-GPU batch 減少每卡前向與反向傳播保存的 activation；以 DistributedSampler 等方式讓各 GPU 取得不同 shard，可平行處理資料並避免所有卡重複相同樣本。",
        "C": "學習率影響參數更新幅度與收斂穩定性，幾乎不改變參數、梯度或 activation tensor 的形狀；任意提高還可能造成發散，無法釋放 GPU 記憶體。",
        "D": "測試集必須留作訓練完成後的獨立泛化評估，拿來訓練會造成資料洩漏與偏樂觀成績；測試樣本的 tensor 大小也不比訓練資料小，並無省記憶體效果。",
    },
    "trap": "資料集大小與單步 batch size 不同：刪掉資料不會降低某一步的峰值記憶體。另要知道普通資料平行會在每張 GPU 複製模型；若連 batch=1 都 OOM，需模型／optimizer sharding 或 checkpointing，而非只做 data sharding。",
    "editorialNote": "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。B 的記憶體改善主要來自縮小每卡 batch；一般 data sharding 只分配輸入樣本，不會分片模型狀態。若模型本身放不進單卡，需另採 FSDP／ZeRO 等模型狀態分片。",
    "references": [
        exam_ref(37),
        ref("PyTorch Documentation－DistributedDataParallel", "https://docs.pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html", "DDP 同步多個模型副本；不會自動切分輸入，使用者需搭配 DistributedSampler 等方式分片資料"),
        ref("PyTorch Documentation－DistributedSampler", "https://docs.pytorch.org/docs/stable/data.html#torch.utils.data.distributed.DistributedSampler", "限制每個分散式程序只載入資料集的互斥子集"),
    ],
}

DRAFTS[38] = {
    "summary": "正確答案是 B。擴散模型需透過多步去噪逐漸還原影像；在合理範圍增加取樣步數並使用適合模型的高品質 scheduler，通常能減少欠去噪並改善細節。",
    "concept": (
        "Stable Diffusion 推論從噪聲潛在向量開始，scheduler 依一系列 timestep 重複"
        "呼叫去噪模型，最後由 VAE 解碼影像。步數太少時，數值近似較粗，可能留下"
        "顆粒或細節未收斂；較佳的 sampler／scheduler 能以同樣或較少步數取得更好的"
        "去噪軌跡。步數增加通常有邊際效益遞減，不能修復模型超出原生解析度、VAE "
        "壓縮或提示不足造成的所有模糊；4K 實務常還需分段高解析修復或超解析。"
    ),
    "answerReason": (
        "題目限制只能在生成階段調整，B 同時提高去噪迭代充分度並改善 timestep／"
        "solver 的品質，最直接針對顆粒與細節還原。A、D 犧牲品質，C 的 CFG 控制"
        "提示遵循程度，過高反而可能損害影像品質。"
    ),
    "optionAnalysis": {
        "A": "降低取樣步數可加快推論，但去噪更新更少，若目前已有顆粒與欠收斂細節，通常會使近似更粗而不是改善清晰度；只有專為少步推論蒸餾的模型才可能例外。",
        "B": "正確。在模型及計算預算允許下，增加 denoising steps 給取樣軌跡更多修正機會，搭配 DPM-Solver 等適合的 scheduler 可提升效率與細節，較符合清晰且不過度平滑的需求。",
        "C": "CFG 提高會讓結果更強烈遵循文字條件，不等於增加創意與多樣性；過高 guidance 可能造成過飽和、對比失真與品質下降，不能當作修復顆粒模糊的主要控制。",
        "D": "降低輸入或輸出解析度能節省運算與記憶體，但會直接減少空間取樣資訊；把低解析影像放大到 4K 通常更模糊，與保留紋理層次的目標相反。",
    },
    "trap": "取樣步數不是越多越好，而是太少時增加通常改善、之後收益遞減。CFG 也不是畫質旋鈕：它提高提示遵循，過高可能降低品質與多樣性。",
    "editorialNote": "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。B 是四個選項中最佳的一般作法，但無法保證直接原生生成 4K 紋理；結果仍受模型版本、原生解析度、VAE、scheduler 與步數區間影響。",
    "references": [
        exam_ref(38),
        ref("Hugging Face Diffusers－Stable Diffusion 3 Pipeline", "https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_3", "num_inference_steps 通常越多品質越高但推論更慢；guidance_scale 過高通常犧牲影像品質"),
        ref("Hugging Face Diffusers－Schedulers", "https://huggingface.co/docs/diffusers/main/using-diffusers/schedulers", "scheduler、timestep spacing 與 solver 設定會影響少步推論的品質與細節"),
    ],
}

DRAFTS[39] = {
    "summary": "正確答案是 C。良好 ARIMA 模型的殘差應近似無自相關白噪音；週期波動且多個 lag 的 ACF 顯著，表示尚有時間結構未被模型捕捉，屬配適不足。",
    "concept": (
        "ARIMA(p,d,q) 以 p 階自迴歸項捕捉過去觀測的依賴，以差分階數 d 處理非平穩"
        "趨勢，再以 q 階移動平均項捕捉過去誤差關係。模型配適後要診斷殘差：均值"
        "接近零、變異大致穩定，且 ACF 不應在系統性的多個 lag 超出信賴界線；"
        "Ljung-Box 檢定也可測試整組自相關是否為零。若殘差呈週期性，還可能需要"
        "季節性 SARIMA 項，而不只是盲目調整非季節 p、q。"
    ),
    "answerReason": (
        "題幹提供兩個一致證據：誤差隨時間週期波動，且殘差 ACF 多個時滯顯著。"
        "這否定白噪音假設，代表可預測的時間依賴仍留在殘差，因此 C 的 underfitting "
        "診斷最合理；需重新識別 AR／MA，並檢查季節項。"
    ),
    "optionAnalysis": {
        "A": "白噪音的核心是不同時間的誤差不具系統性相關；多個 lag 的 ACF 顯著且有週期波動，正是殘差不是白噪音的證據，不能據此宣稱模型穩定。",
        "B": "單一 lag 偶然超界或許要考量多重比較，但題目描述多個 lag 顯著且呈週期性，是結構化訊號而非輕微隨機異常；忽略會讓預測區間與未來預測失真。",
        "C": "正確。殘差仍保有自相關，表示 ARIMA 尚未吸收資料中的時間依賴；應重新檢查差分與 p、q，並依週期長度考慮季節性 P、D、Q，而後再次做殘差診斷。",
        "D": "殘差相關代表下一期誤差可由過去誤差部分預測，顯示模型漏掉資訊；它會影響點預測效率、標準誤與預測區間，不能視為與預測無關。",
    },
    "trap": "殘差 ACF 顯著不是「模型抓到自相關」，而是「模型抓完後還剩自相關」。題目出現週期波動時，除了 p、q，也應想到季節 ARIMA；官方 C 是最接近的選項但敘述未列季節項。",
    "editorialNote": "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。題目週期性殘差可能需要 SARIMA 的季節性 P／Q 或季節差分，而非僅調整非季節 p、q；本站仍依官方答案 C 的「配適不足」核心判定。",
    "references": [
        exam_ref(39),
        ref("statsmodels Documentation－STL Forecasting / ARIMA residual diagnostics", "https://www.statsmodels.org/stable/examples/notebooks/generated/stl_decomposition.html", "時間序列分解與季節成分；週期性結構需在模型中處理"),
        ref("NIST/SEMATECH e-Handbook－Autocorrelation", "https://www.itl.nist.gov/div898/handbook/eda/section3/eda35c.htm", "自相關圖用於檢查時間序列中不同 lag 的相關性及隨機性"),
    ],
}

DRAFTS[40] = {
    "summary": "正確答案是 A。VAE 以顯式潛在隨機變數與變分後驗建模，GAN 以生成器和鑑別器的對抗目標學習資料分布，擴散模型則以條件化逐步去噪生成；三者的目標與生成程序根本不同。",
    "concept": (
        "VAE 定義潛在變數生成模型 p(x|z)，用編碼器近似後驗 q(z|x)，以重建項與 KL "
        "正則的 evidence lower bound 訓練，潛在空間連續但像素似然常帶來平滑。GAN "
        "沒有顯式似然，由生成器與鑑別器進行 minimax 對抗訓練，可生成銳利樣本但"
        "可能不穩或模式崩潰。Diffusion 建立逐步加噪的 Markov 過程，再學習反向去噪；"
        "文字、影像等條件可透過 conditioning 或 cross-attention 引導。跨模態對齊"
        "不是任何一類模型自動保證，仍取決於配對資料、條件設計與對齊損失。"
    ),
    "answerReason": (
        "A 是唯一大致正確區分三種家族者：VAE 的變分潛在建模、GAN 的對抗分布"
        "學習、Diffusion 的條件反向去噪。B、C 顛倒其訓練機制，D 則錯把不同模型"
        "與模態都說成必然共用同一潛在空間。"
    ),
    "optionAnalysis": {
        "A": "正確。VAE 以近似後驗與顯式 latent variable objective 學習連續表示；GAN 以 adversarial loss 對齊生成與真實分布；條件 diffusion 從噪聲反覆去噪生成高品質樣本。選項對品質的描述是常見取捨而非絕對定律。",
        "B": "VAE 是顯式潛在變數模型並以變分推論最大化 ELBO，不依賴對抗訓練；diffusion 以已知前向加噪和學得的反向過程建模，也不是 GAN 式鑑別器對抗，因此前半整體錯置。",
        "C": "標準 GAN 直接把隨機向量一次送入生成器，不以逐步 Markov chain 轉換；VAE 的 KL 項用來約束近似後驗接近先驗，不代表 VAE 與 GAN 都用 Markov 鏈。Diffusion 才明確以逐步加噪／反向鏈生成。",
        "D": "多模態系統可以設計 shared latent space，但 VAE、GAN、diffusion 只規定生成目標與程序，不保證不同模態共享完全相同表示；三者差異也包含訓練損失、取樣步驟與機率建模，不只是解碼器。",
    },
    "trap": "要分清楚「模型家族的生成機制」與「多模態系統如何對齊」：VAE、GAN、Diffusion 都能被做成條件式或多模態版本，但共享空間與對齊效果不是架構名稱自動帶來。",
    "editorialNote": "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。A 的「VAE 生成解析度有限」「GAN 品質高但不穩」「Diffusion 兼具穩定與多樣」是常見概括而非必然；VAE 也不會僅靠顯式潛在變數自動完成跨模態對齊，仍需多模態訓練設計。",
    "references": [
        exam_ref(40),
        ref("Auto-Encoding Variational Bayes", "https://arxiv.org/abs/1312.6114", "變分下界、重參數化與潛在變數生成模型的訓練方法"),
        ref("Generative Adversarial Nets", "https://arxiv.org/abs/1406.2661", "以生成器與鑑別器進行 minimax 對抗訓練的生成模型框架"),
        ref("Denoising Diffusion Probabilistic Models", "https://arxiv.org/abs/2006.11239", "前向加噪 Markov chain 與學習反向去噪過程的生成方法"),
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
