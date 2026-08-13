"""Write draft explanations for 115-1 intermediate subject one, Q1-Q10.

This script only updates questions already present in ``questions.json``. It
checks the official answer before writing and never overwrites reviewed work.

Usage::

    python scripts/write-explanations-115-1-m1-001-010.py
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
ARXIV = "https://arxiv.org/abs/"
SKLEARN = "https://scikit-learn.org/stable/"
DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def exam_ref(number: int) -> dict:
    return {
        "title": "115 年第一次中級 AI 應用規劃師－人工智慧技術應用與規劃公告試題",
        "url": EXAM_PDF,
        "locator": f"第 {number} 題題幹、選項與官方答案",
        "checkedAt": CHECKED_AT,
    }


def paper_ref(paper_id: str, title: str, locator: str) -> dict:
    return {
        "title": title,
        "url": f"{ARXIV}{paper_id}",
        "locator": locator,
        "checkedAt": CHECKED_AT,
    }


def sklearn_ref(path: str, title: str, locator: str) -> dict:
    return {
        "title": f"scikit-learn－{title}",
        "url": f"{SKLEARN}{path}",
        "locator": locator,
        "checkedAt": CHECKED_AT,
    }


EXPECTED_ANSWER = {
    1: "D", 2: "C", 3: "B", 4: "C", 5: "C",
    6: "C", 7: "C", 8: "B", 9: "D", 10: "A",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[1] = {
    "summary": "正確答案是 D。詞性標註的目的，是為序列中的每個詞彙指派名詞、動詞、形容詞等語法類別。",
    "concept": (
        "詞性標註（Part-of-Speech Tagging）是一種序列標註任務，會依詞本身與"
        "上下文，為每個 token 指派詞性標籤。同一個詞在不同句子中可能具有"
        "不同詞性，因此不能只查字典。詞性可協助後續的句法分析、命名實體辨識"
        "與關係擷取，但它本身不負責翻譯、斷詞或情感判斷。"
    ),
    "answerReason": (
        "D 直接描述 POS Tagging 的輸出：每個詞彙都得到名詞、動詞、形容詞等"
        "語法類別。法律文件解析可利用這些標籤判斷實體與動作之間的語法角色。"
        "A、B、C 分別是機器翻譯、斷詞與情感分析，任務目標均不同。"
    ),
    "optionAnalysis": {
        "A": (
            "機器翻譯將來源語言的文本轉成目標語言，重點是保留語意並產生另一"
            "語言的句子；它可能使用詞性特徵，但為詞語標記語法類別並不會完成翻譯。"
        ),
        "B": (
            "斷詞或 tokenization 是把字串切成字、詞或子詞單位，通常是詞性標註"
            "之前的處理。它只決定單位邊界，不會告訴系統每個單位是名詞或動詞。"
        ),
        "C": (
            "情感分析判斷文本、句子或面向所表達的正向、負向或中立傾向，屬於"
            "語意或分類任務；詞性標註輸出的是語法類別，不能直接代表情感。"
        ),
        "D": (
            "正確。模型依詞彙及其上下文，為序列中每個 token 指派名詞、動詞、"
            "形容詞等標籤，提供後續句法與資訊擷取所需的語法線索。"
        ),
    },
    "trap": (
        "不要把前處理流程中的相鄰步驟混為一談：先斷詞取得 token，再做 POS"
        "標註取得語法類別；情感分析與翻譯則各有不同的輸出目標。"
    ),
    "references": [
        exam_ref(1),
        {
            "title": "spaCy－Linguistic Features 官方文件",
            "url": "https://spacy.io/usage/linguistic-features",
            "locator": "Part-of-speech tagging：Token.pos_ 與細粒度 Token.tag_ 為依上下文預測的詞性標籤",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[2] = {
    "summary": "正確答案是 C。LoRA 凍結預訓練權重，只訓練低秩更新矩陣，因而大幅減少可訓練參數與訓練記憶體。",
    "concept": (
        "低秩調適（Low-Rank Adaptation, LoRA）假設微調造成的權重更新可用較低"
        "秩表示。它不直接更新大型權重矩陣 W，而以兩個較小矩陣的乘積 BA 表示"
        "增量，訓練時凍結 W、只更新 A 與 B。這會減少需要保存的梯度與最佳化器"
        "狀態；它是參數高效率微調，不等於把模型蒸餾、剪枝或改造注意力型態。"
    ),
    "answerReason": (
        "題幹已限定凍結原模型且只訓練少量額外參數，這正是 C 所述的 LoRA"
        "做法。低秩矩陣的參數量遠小於完整權重矩陣，因此能降低微調所需的 GPU"
        "記憶體。其他選項分別會建立學生模型、刪除既有權重或改變注意力計算，"
        "都不是 LoRA 的核心機制。"
    ),
    "optionAnalysis": {
        "A": (
            "知識蒸餾用教師模型的輸出或中間表示訓練較小的學生模型，目標通常是"
            "模型壓縮與推論加速。LoRA 仍在原預訓練模型上加入低秩更新，並不建立"
            "一個較小的 70B 學生模型。"
        ),
        "B": (
            "剪枝移除或遮蔽低重要性權重，使模型稀疏化；它會改變原模型參數結構"
            "或有效參數集合。LoRA 保留並凍結原權重，另加可訓練的低秩分支。"
        ),
        "C": (
            "正確。將權重更新限制為低秩矩陣乘積，只需為少量參數保存梯度與"
            "最佳化器狀態，能在保持基礎模型權重不變的情況下進行領域適配。"
        ),
        "D": (
            "稀疏注意力限制每個 token 參照的位置，可降低長序列注意力的計算或"
            "記憶體成本；LoRA 不要求把密集注意力換成稀疏注意力，兩者解決的瓶頸不同。"
        ),
    },
    "trap": (
        "看到『減少資源』不能立刻選任何壓縮技術：LoRA 減少的是微調時的可訓練"
        "參數；蒸餾、剪枝通常改變部署模型，稀疏注意力則處理長序列計算。"
    ),
    "references": [
        exam_ref(2),
        paper_ref(
            "2106.09685",
            "Hu et al., LoRA: Low-Rank Adaptation of Large Language Models（2021）",
            "摘要與第 2、4 節：凍結預訓練權重，將可訓練的秩分解矩陣注入 Transformer 層，以降低可訓練參數與記憶體需求",
        ),
    ],
}

DRAFTS[3] = {
    "summary": "正確答案是 B。CBOW 通常訓練較快，而 Skip-gram 逐一預測周邊詞，對低頻詞表示通常較有利。",
    "concept": (
        "CBOW 由一個上下文視窗的詞表示共同預測中心詞，每個視窗形成一次中心詞"
        "預測；Skip-gram 則由中心詞分別預測視窗內多個上下文詞。因此 Skip-gram"
        "每個中心詞可產生多個訓練配對，成本較高，卻能讓低頻中心詞獲得多次"
        "更新訊號。原始 Word2Vec 論文也指出 CBOW 較快，Skip-gram 對罕見詞較好。"
    ),
    "answerReason": (
        "B 完整呈現題目要求的效率與長尾品質取捨：超大語料可偏好 CBOW 的速度，"
        "重視長尾詞則可採 Skip-gram。A、C 分別把低頻詞優勢和速度優勢顛倒；"
        "D 忽略兩種不同預測方向所造成的訓練訊號差異。"
    ),
    "optionAnalysis": {
        "A": (
            "CBOW 將多個上下文表示合併後預測中心詞，確實可平滑常見語意並提高"
            "效率；但長尾詞作為目標出現次數仍少，平均上下文不會憑空增加它的"
            "出現次數，因此不能據此說 CBOW 對低頻詞較好。"
        ),
        "B": (
            "正確。CBOW 每個上下文視窗預測一個中心詞，通常計算較省；Skip-gram"
            "讓中心詞分別預測多個周邊詞，對罕見中心詞形成多個訓練配對，通常"
            "能學得較好的低頻詞表示，但訓練較慢。"
        ),
        "C": (
            "Skip-gram 不是每次只做一次單一目標預測就結束；一個中心詞通常要與"
            "視窗內多個上下文詞建立配對。相較 CBOW 合併上下文預測中心詞，它"
            "通常需要更多訓練工作，不能以此宣稱更快。"
        ),
        "D": (
            "兩者的差異不是 batch 排列而已，而是條件預測方向不同：CBOW 由上下文"
            "預測中心詞，Skip-gram 由中心詞預測上下文。這會改變訓練樣本數與"
            "低頻詞的學習效果。"
        ),
    },
    "trap": (
        "記住『CBOW 快、Skip-gram 顧罕見詞』是通常的經驗取捨，不是所有資料與"
        "超參數下的絕對保證；本題問的是在十億 token 與大量長尾詞下最準確的概括。"
    ),
    "references": [
        exam_ref(3),
        paper_ref(
            "1301.3781",
            "Mikolov et al., Efficient Estimation of Word Representations in Vector Space（2013）",
            "第 2 節：CBOW 由上下文預測當前詞，Skip-gram 由當前詞預測上下文",
        ),
        paper_ref(
            "1310.4546",
            "Mikolov et al., Distributed Representations of Words and Phrases and their Compositionality（2013）",
            "第 2 節：Skip-gram 的訓練目標與負採樣，說明中心詞對上下文詞的預測配對",
        ),
    ],
}

DRAFTS[4] = {
    "summary": "正確答案是 C。MLM 隨機選取並遮蔽部分 token，利用左右兩側的雙向上下文預測原始內容。",
    "concept": (
        "遮蔽語言建模（Masked Language Model, MLM）從輸入中選取部分 token 作為"
        "預測目標，訓練模型還原原 token。BERT 的 Transformer encoder 可同時"
        "利用目標位置左、右兩側的上下文，因此學到深度雙向表示。原始 BERT"
        "做法並非所有選中 token 都換成 [MASK]，但學習目標仍是預測其原始詞。"
    ),
    "answerReason": (
        "C 同時說出 MLM 的操作與目標：隨機遮蔽部分輸入，依雙向語境預測原內容。"
        "A 是自回歸語言建模；B 是對抗訓練；D 把遮蔽誤說成壓縮詞彙表，三者都"
        "不能描述 BERT 的 MLM 預訓練。"
    ),
    "optionAnalysis": {
        "A": (
            "自左至右預測下一 token 是因果式自回歸語言模型的目標，適合連續生成。"
            "MLM 並非依固定方向逐詞生成，而能使用被選位置左右兩側的內容。"
        ),
        "B": (
            "對抗訓練透過擾動或生成對手樣本提高穩健性，也可用判別器比較資料；"
            "原始 BERT 的 MLM 不以縮小真實句與生成句差異作為訓練目標。"
        ),
        "C": (
            "正確。模型針對被選取的位置預測原始 token，且 encoder 可同時讀取"
            "左右上下文，藉此預訓練可供分類、問答等任務使用的雙向表示。"
        ),
        "D": (
            "遮蔽的是某次輸入中的 token 位置，不會從 tokenizer 的詞彙表刪除"
            "低頻詞，也不會縮小 embedding 矩陣。詞彙表大小是 tokenization 與"
            "模型設計決策，不是 MLM 的目的。"
        ),
    },
    "trap": (
        "MLM 的 mask 是訓練訊號，不是模型壓縮。另需區分雙向 encoder 的填空式"
        "預測與自回歸 decoder 的下一詞預測，兩者能使用的上下文方向不同。"
    ),
    "references": [
        exam_ref(4),
        paper_ref(
            "1810.04805",
            "Devlin et al., BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding（2018）",
            "摘要與第 3.1 節：MLM 隨機選取輸入 token，利用左右上下文預測原 token，並說明 80/10/10 替換策略",
        ),
    ],
}

DRAFTS[5] = {
    "summary": "正確答案是 C。Word2Vec 以低維稠密向量表示詞彙，並從上下文學得語意結構，改善 One-Hot 的高維稀疏與無語意距離問題。",
    "concept": (
        "One-Hot 向量的維度等於詞彙表大小，每個詞只有一個位置為 1；任意兩個"
        "不同詞彼此正交，無法用距離表示語意相似性。Word2Vec 透過 CBOW 或"
        "Skip-gram 預測任務，把每個詞映射到事先設定維度的稠密向量。出現在"
        "相似上下文的詞會形成相近表示，同時維度通常遠小於詞彙表大小。"
    ),
    "answerReason": (
        "C 同時對應題幹的兩個痛點：稠密詞向量降低表示維度，訓練目標又使"
        "向量保有語意與句法結構。A 要求真正建模長距序列，超出 Word2Vec 的"
        "固定局部視窗；B 是詞頻權重；D 則誤稱必須有人工標註。"
    ),
    "optionAnalysis": {
        "A": (
            "序列模型或注意力模型可針對詞序與長距依賴建立上下文表示；Word2Vec"
            "主要從固定大小的局部視窗學靜態詞向量，同一個詞在不同句子仍使用"
            "同一向量，並非長距序列建模的根本解法。"
        ),
        "B": (
            "TF-IDF 等方法會依詞頻與文件頻率調整特徵權重。Word2Vec 雖會利用"
            "語料出現事件訓練，核心目標卻是上下文預測，不是讓模型更重視高頻詞；"
            "實作還常下採樣極高頻詞。"
        ),
        "C": (
            "正確。每個詞以數百維等固定長度的稠密向量表示，不必配置詞彙表大小"
            "的稀疏向量；預測式訓練使語意或句法相似的詞在向量空間保有結構。"
        ),
        "D": (
            "Word2Vec 的訓練標籤直接由原始文字的中心詞與上下文位置產生，不需要"
            "人工標註詞語類別。它屬自監督式表示學習，而不是依賴標註語料的"
            "監督分類。"
        ),
    },
    "trap": (
        "低維不代表只做壓縮：Word2Vec 還藉由上下文預測學得可比較的稠密表示。"
        "但它仍是局部視窗下的靜態詞向量，不要延伸成能理解所有長距語境。"
    ),
    "references": [
        exam_ref(5),
        paper_ref(
            "1301.3781",
            "Mikolov et al., Efficient Estimation of Word Representations in Vector Space（2013）",
            "摘要與第 2 節：以 CBOW、Skip-gram 從大規模語料學習連續詞向量，並比較 one-hot 輸入與低維投影層",
        ),
    ],
}

DRAFTS[6] = {
    "summary": "正確答案是 C。語義分割只分像素類別，實例分割還會把同類別的不同物件分成各自獨立的遮罩。",
    "concept": (
        "語義分割為每個像素指派類別，例如所有行人像素都標為『行人』；兩名"
        "相鄰行人的類別相同，因此結果不要求區分個體。實例分割則同時辨識類別"
        "與個體身分，為每個可數物件輸出獨立遮罩。實務上實例分割模型可能也"
        "輸出 bounding box，但根本差異是是否區分同類別的各個實例。"
    ),
    "answerReason": (
        "題幹同時要求道路、建築、行人的逐像素分類，又特別要求把行人 #1 與"
        "行人 #2 分開。C 正確指出語義分割無法表達同類個體身分，而實例分割"
        "可建立獨立 mask。其餘選項否定或顛倒了像素級標記與個體區分。"
    ),
    "optionAnalysis": {
        "A": (
            "兩種任務都涉及像素級遮罩；bounding box 不是語義分割的主要輸出。"
            "Mask R-CNN 類實例分割器可能先偵測框再預測遮罩，但『不產生框』"
            "並非所有實例分割方法的定義。"
        ),
        "B": (
            "影像層級分類只判斷整張圖有哪些類別，不定位各像素。實例分割則比"
            "影像分類更細，必須為每個物件實例產生像素級遮罩，因此此說法錯置任務。"
        ),
        "C": (
            "正確。語義分割可把所有行人像素歸入同一類；實例分割還會為兩名"
            "相鄰行人配置不同實例識別與獨立遮罩，符合題幹『行人 #1/#2』需求。"
        ),
        "D": (
            "兩者確實都能提供像素級資訊，但是否區分同類別個體正是核心差異。"
            "否定此差異會使語義分割無法表達的實例身分被忽略。"
        ),
    },
    "trap": (
        "判斷關鍵不是有沒有逐像素標記，而是同一類別的兩個物件是否需要分開。"
        "只需『哪些像素是行人』用語義分割；需要『每一名行人』則用實例分割。"
    ),
    "references": [
        exam_ref(6),
        paper_ref(
            "1703.06870",
            "He et al., Mask R-CNN（2017）",
            "摘要與第 1 節：instance segmentation 同時辨識物件實例並為每個實例產生高品質分割遮罩",
        ),
        paper_ref(
            "1505.04597",
            "Ronneberger et al., U-Net: Convolutional Networks for Biomedical Image Segmentation（2015）",
            "摘要與架構：以 encoder-decoder 產生像素級分割圖，代表語義分割的典型輸出",
        ),
    ],
}

DRAFTS[7] = {
    "summary": "正確答案是 C。實例分割同時提供每個物件的像素級遮罩與個體身分，符合精確區域標記及同類個體分離需求。",
    "concept": (
        "電腦視覺任務的輸出粒度依序可區分為：影像分類輸出整張圖的類別；目標"
        "檢測輸出每個物件的類別與邊界框；語義分割輸出每個像素的類別；實例"
        "分割則為每個物件實例輸出獨立像素遮罩。因此，需求同時出現 pixel-level"
        " mask 與區分同類個體時，應選實例分割。"
    ),
    "answerReason": (
        "C 同時滿足題目兩個不可缺少的條件：購物籃、手機、商品需精確到像素，"
        "且相同商品也要按不同個體分開。分類缺少定位，檢測只有框而非精確遮罩，"
        "語義分割又會把同類物件合併，均不完整。"
    ),
    "optionAnalysis": {
        "A": (
            "影像分類可判斷畫面是否包含手機或商品，輸出通常是整張影像的類別"
            "機率。它不提供物件位置、邊界框或像素遮罩，無法標記每位顧客手中"
            "的各個物件。"
        ),
        "B": (
            "目標檢測會為每個物件輸出類別與 bounding box，也能區分多個實例；"
            "但矩形框包含背景且不貼合物件輪廓，未達題目要求的 pixel-level mask。"
        ),
        "C": (
            "正確。實例分割對每個偵測到的購物籃、手機或商品建立各自遮罩，既能"
            "精確標出區域，也能把兩個同類商品或不同顧客分配為不同實例。"
        ),
        "D": (
            "語義分割可將像素分為顧客、商品等類別，適合道路或背景等區域理解；"
            "但同類別的多個商品通常共用一個類別標籤，不能提供題目要求的個體身分。"
        ),
    },
    "trap": (
        "目標檢測能分個體但只有矩形框；語義分割有像素遮罩但不分同類個體。"
        "題幹同時要求這兩項能力時，才鎖定實例分割。"
    ),
    "references": [
        exam_ref(7),
        paper_ref(
            "1703.06870",
            "He et al., Mask R-CNN（2017）",
            "摘要與第 1 節：在物件偵測分支之外，為每個物件實例預測分割遮罩",
        ),
    ],
}

DRAFTS[8] = {
    "summary": "正確答案是 B。ROC 橫軸為假陽率 FPR，縱軸為真陽率 TPR，分別對應健康者被誤判與病患被檢出的比例。",
    "concept": (
        "ROC 曲線在不同分類閾值下繪製 FPR 與 TPR。TPR = TP/(TP+FN)，也就是"
        "敏感度或 recall，表示真實陽性中被正確找出的比例；FPR = FP/(FP+TN)，"
        "表示真實陰性中被誤判為陽性的比例。每個閾值形成一個點，曲線呈現提高"
        "偵測率時可能伴隨的誤報取捨。"
    ),
    "answerReason": (
        "B 的軸向、公式意義及醫療解讀均正確：橫軸是健康個體被錯判惡性的"
        "風險，縱軸是惡性病患被正確識別的能力。A 與 C 描述其他分類指標組合，"
        "D 則是物件偵測評估，均不是 ROC 的座標。"
    ),
    "optionAnalysis": {
        "A": (
            "Accuracy 是全部樣本中預測正確的比例，並不是 ROC 的橫軸。Recall"
            "在二元陽性定義下等於 TPR，可作縱軸，但選項要求兩軸都正確，故 A"
            "仍不成立。"
        ),
        "B": (
            "正確。橫軸 FPR 衡量健康者被誤判為惡性的比例；縱軸 TPR 衡量惡性"
            "病患被檢出的比例。改變判定閾值可觀察兩者的取捨。"
        ),
        "C": (
            "Precision 與 Recall 的關係形成 Precision-Recall 曲線，特別常用於"
            "類別不平衡資料。ROC 的橫軸分母限定真實陰性，並非預測陽性的 precision。"
        ),
        "D": (
            "IoU 與 mAP 是物件偵測中評估邊界框重疊及跨類別平均精確度的概念。"
            "皮膚病變二元分類的 ROC 不以邊界框或 IoU 作為座標。"
        ),
    },
    "trap": (
        "先固定 ROC 軸向：X 是 FPR，Y 是 TPR。醫療上 TPR 常稱 sensitivity；"
        "specificity = 1−FPR，別把 precision 或 accuracy 填入橫軸。"
    ),
    "references": [
        exam_ref(8),
        sklearn_ref(
            "modules/model_evaluation.html#roc-metrics",
            "Metrics and scoring－ROC metrics",
            "ROC curve 定義：在不同門檻下，以 false positive rate 為橫軸、true positive rate 為縱軸",
        ),
        {
            "title": "NIST－Sensitivity and Specificity 官方手冊",
            "url": "https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/sensitiv.htm",
            "locator": "Sensitivity = true positive rate；specificity = true negative rate，並列出混淆矩陣公式",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[9] = {
    "summary": "正確答案是 D。單一混淆矩陣只記錄某一判定閾值下的計數，無法直接得到跨多個閾值的 ROC AUC。",
    "concept": (
        "二元混淆矩陣包含 TP、FP、TN、FN 四種計數，因此可用代數公式直接算出"
        "precision、accuracy 與 recall。ROC 曲線則需改變分數閾值，對每個閾值"
        "計算一組 FPR、TPR，再對曲線求面積。若只保留一個閾值的類別預測與"
        "混淆矩陣，原始連續分數的排序資訊已遺失，不能重建整條曲線。"
    ),
    "answerReason": (
        "D 是唯一無法由一張混淆矩陣直接計算的項目。A、B、C 分別可由"
        "TP/(TP+FP)、(TP+TN)/總數、TP/(TP+FN) 算出；AUC 則需要多個閾值或"
        "所有樣本的預測分數，超出單一矩陣提供的資訊。"
    ),
    "optionAnalysis": {
        "A": (
            "Precision 的分子是 TP，分母是所有預測陽性 TP+FP；這兩個數都在"
            "混淆矩陣內，因此可直接計算。它回答『被模型判陽性的樣本有多少是真的』。"
        ),
        "B": (
            "Accuracy 將對角線上的正確預測 TP+TN 除以全部四格總數，所有項目"
            "都可從混淆矩陣取得，因此可直接計算。"
        ),
        "C": (
            "Recall 或 TPR 將 TP 除以真實陽性總數 TP+FN，混淆矩陣已提供所需"
            "計數，所以能直接計算某一閾值下的召回率。"
        ),
        "D": (
            "正確。ROC AUC 彙整分類器在多個閾值下的 FPR-TPR 表現；單一混淆"
            "矩陣只對應一個操作點，沒有預測分數排序，無法直接計出整條曲線面積。"
        ),
    },
    "trap": (
        "區分『一個閾值的指標』與『跨閾值的曲線』。混淆矩陣足以算 precision、"
        "recall、accuracy 等操作點指標；ROC AUC 必須保留預測分數或多個閾值結果。"
    ),
    "references": [
        exam_ref(9),
        sklearn_ref(
            "modules/generated/sklearn.metrics.confusion_matrix.html",
            "confusion_matrix",
            "定義：C(i,j) 為真實類別 i 被預測成類別 j 的樣本數；二元情況對應 TN、FP、FN、TP",
        ),
        sklearn_ref(
            "modules/model_evaluation.html#roc-metrics",
            "Metrics and scoring－ROC metrics",
            "ROC curve 由不同 decision threshold 的 FPR 與 TPR 組成；roc_auc_score 由 prediction scores 計算",
        ),
    ],
}

DRAFTS[10] = {
    "summary": "正確答案是 A。YOLO 是單階段偵測器，直接從整張影像預測框與類別；Faster R-CNN 則先產生候選區域，再分類與微調框。",
    "concept": (
        "單階段偵測器把物件定位與分類整合為一次密集預測，不先建立獨立候選"
        "區域清單；YOLO 原始設計以單一網路從完整影像直接回歸邊界框與類別機率。"
        "Faster R-CNN 是兩階段偵測器，先由 Region Proposal Network（RPN）產生"
        "候選區域，再以共享特徵對候選區域分類並進行 bounding-box regression。"
    ),
    "answerReason": (
        "A 準確描述兩者的流程差異，也解釋工廠為何會比較速度與偵測品質。B、D"
        "把 Faster R-CNN 或兩者的階段數說反；C 則把 YOLO 誤述為依賴候選區域，"
        "違反其直接密集預測的單階段設計。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。YOLO 對整張影像一次產生位置與類別預測；Faster R-CNN 先以"
            "RPN 提出可能含物件的區域，再針對這些 proposals 做分類與框回歸。"
        ),
        "B": (
            "Faster R-CNN 是典型兩階段架構，但 YOLO 的主要特徵正是將偵測視為"
            "單一回歸問題，不先進行候選區域分類。因此不能說兩者都是兩階段。"
        ),
        "C": (
            "YOLO 雖是單階段架構，但不以增加 region proposals 為運作核心；它"
            "直接在影像的網格或特徵位置密集預測。候選區域數量是兩階段偵測器"
            "較直接的流程參數。"
        ),
        "D": (
            "Faster R-CNN 的 RPN 與後續分類/框回歸構成兩個階段，雖然可端到端"
            "訓練且共享卷積特徵，仍不能因此稱為單階段偵測。"
        ),
    },
    "trap": (
        "『同一模型端到端訓練』不等於『單階段』。判斷點是有沒有先產生候選"
        "區域，再對候選區域分類：Faster R-CNN 有，YOLO 沒有。"
    ),
    "references": [
        exam_ref(10),
        paper_ref(
            "1506.02640",
            "Redmon et al., You Only Look Once: Unified, Real-Time Object Detection（2015）",
            "摘要與第 1 節：以單一神經網路從完整影像直接預測 bounding boxes 與 class probabilities",
        ),
        paper_ref(
            "1506.01497",
            "Ren et al., Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks（2015）",
            "摘要與第 3 節：RPN 產生 region proposals，再由 Fast R-CNN detector 分類與回歸邊界框",
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
