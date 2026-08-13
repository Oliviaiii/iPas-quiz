"""Write draft explanations for 114-2 intermediate subject one, Q1-Q10.

This script only updates questions already present in ``questions.json``.  It
checks the official answer before writing and never overwrites reviewed work.

Usage::

    python scripts/write-explanations-114-2-m1-001-010.py
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
ARXIV = "https://arxiv.org/abs/"
SKLEARN = "https://scikit-learn.org/stable/"
DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def exam_ref(number: int) -> dict:
    return {
        "title": "114 年第二次中級 AI 應用規劃師－人工智慧技術應用與規劃公告試題",
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
    1: "B", 2: "A", 3: "B", 4: "C", 5: "A",
    6: "B", 7: "A", 8: "C", 9: "B", 10: "D",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[1] = {
    "summary": "正確答案是 B。情感分析的核心任務是判斷文字表達的正向、負向或其他情感傾向。",
    "concept": (
        "情感分析（Sentiment Analysis）是文字分類的一種，輸入可為商品評論、"
        "社群貼文或客服訊息，輸出通常是正向、負向、中立等極性，也可能細分"
        "情緒或對特定面向的態度。企業彙整不同時間的分類結果，才可觀察滿意度"
        "變化。它分析的是文本表達的態度，不等於辨識文體、翻譯語言或濃縮內容。"
    ),
    "answerReason": (
        "題幹要即時掌握顧客對產品的滿意度，必須先判定每則評論所表達的情感"
        "傾向，再彙整正負向比例或分數。B 正好描述此分類目標；其餘三項分別是"
        "風格分析、機器翻譯與摘要生成，產出不能直接代表顧客滿意或不滿意。"
    ),
    "optionAnalysis": {
        "A": (
            "語言風格與語氣分析關注正式程度、禮貌、用詞或寫作特徵，可用於"
            "客群溝通策略；但同一種口語風格可能表達稱讚或抱怨，風格本身不能"
            "替代正負向態度的判斷。"
        ),
        "B": (
            "正確。模型判斷評論呈現正向、負向或中立傾向，企業再依時間、商品"
            "或客群彙整結果，就能追蹤滿意度變化。這正是情感分析的典型分類用途。"
        ),
        "C": (
            "自動翻譯把來源語言的內容轉成指定目標語言，目標是維持原意與語言"
            "轉換品質。翻譯後仍需另一個分類器判斷情感，因此它是多語處理步驟，"
            "不是情感分析的主要目的。"
        ),
        "D": (
            "自動摘要將多句評論濃縮成較短內容，重點是保留主要資訊。摘要可以"
            "協助人工閱讀，但若沒有情感標籤或分數，仍無法直接量化滿意度的"
            "正負變化。"
        ),
    },
    "trap": (
        "先依輸出判斷 NLP 任務：情感分析輸出態度標籤或分數，翻譯輸出另一種"
        "語言，摘要輸出較短文本，風格分析輸出語體特徵；不要因它們都處理文字"
        "就視為同一任務。"
    ),
    "references": [
        exam_ref(1),
        {
            "title": "Hugging Face Transformers－Text classification 官方文件",
            "url": "https://huggingface.co/docs/transformers/tasks/sequence_classification",
            "locator": "Text classification：情感分析為文字分類的一種，將正向、負向或中立標籤指派給文字序列",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[2] = {
    "summary": "正確答案是 A。Transformer 的自注意力能直接連結序列中相距很遠的詞，建模長距離語境依賴。",
    "concept": (
        "自注意力（Self-Attention）會讓序列中的每個位置，依查詢與其他位置的"
        "鍵之相似度分配權重，再彙整相應的值。於是某個代名詞或專有名詞可直接"
        "參照長文前段的相關詞，不必像循環網路逐步傳遞狀態。Transformer 原始"
        "論文以注意力取代循環與卷積，並用位置編碼補入詞序資訊。"
    ),
    "answerReason": (
        "長篇金融文件的翻譯需要跨越多個詞甚至多句追蹤上下文。A 的自注意力"
        "使遠距位置直接互相計算關聯，能依整段語境選擇較合適的翻譯。這是"
        "Transformer 架構本身的關鍵；資料增強或強化學習可能是額外訓練策略，"
        "並非該架構改善長距語境建模的主要原因。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。自注意力為每個詞計算它對序列內其他詞的注意力權重，遠距詞"
            "可以直接互相影響表示，因此適合處理長文件中的指涉、術語與語境一致性。"
        ),
        "B": (
            "卷積能以局部濾波器擷取鄰近模式，也可平行運算；但 Transformer"
            "原始架構的核心是注意力，並非靠卷積加速。卷積若要連結很遠的位置，"
            "通常還需堆疊多層或擴大感受野。"
        ),
        "C": (
            "強化學習透過獎勵訊號調整策略，可用於後續偏好最佳化或特定生成目標；"
            "標準 Transformer 機器翻譯的序列建模不以強化學習為必要條件，"
            "也不是捕捉長距依賴的結構來源。"
        ),
        "D": (
            "資料增強可補充稀少語言或擴大訓練樣本，前提是增強資料品質良好；"
            "它改變的是資料組成，不是模型如何讓遠距詞互相參照，因此不能說明"
            "Transformer 架構本身的優勢。"
        ),
    },
    "trap": (
        "題目問的是模型架構的主要原因，而不是任何可能提升翻譯的措施。看到"
        "Transformer 與長篇語境，先鎖定自注意力；資料增強和強化學習屬訓練策略。"
    ),
    "references": [
        exam_ref(2),
        paper_ref(
            "1706.03762",
            "Vaswani et al., Attention Is All You Need（2017）",
            "摘要與第 3 節：Transformer 僅以注意力機制建構序列轉換模型；第 4 節比較長距依賴的路徑長度",
        ),
    ],
}

DRAFTS[3] = {
    "summary": "正確答案是 B。BERT 的 MLM 會遮住部分詞元，再利用左右兩側的雙向上下文預測原詞。",
    "concept": (
        "遮罩語言模型（Masked Language Model, MLM）先從輸入中選取一部分詞元，"
        "再將其中多數換成 [MASK]、少數改成隨機詞或保留原詞，模型則預測被選中"
        "位置的原始詞元。BERT 的 Transformer encoder 可同時看到遮罩位置左右"
        "兩側的內容，因此能預訓練深度雙向表示；它不是自回歸式的逐詞生成器。"
    ),
    "answerReason": (
        "B 同時包含 MLM 的兩個辨識點：先選取並遮罩部分詞，再根據雙向上下文"
        "還原。A 是只能使用左側內容的自回歸生成；C 是對抗式資料擾動；D 把"
        "BERT 的 encoder-only 預訓練誤說成以 decoder 重建整句。"
    ),
    "optionAnalysis": {
        "A": (
            "從左到右預測下一詞是因果式或自回歸語言模型的訓練方式，適合連續"
            "生成文本。BERT 的 MLM 不是固定遮罩句尾，也允許模型利用目標位置"
            "右側的詞，因此不符合雙向預訓練。"
        ),
        "B": (
            "正確。原始 BERT 論文從每個序列隨機選取部分 token 作為預測目標，"
            "讓模型利用左、右兩側語境預測原 token，藉此學得可供分類、問答等"
            "下游任務微調的雙向表示。"
        ),
        "C": (
            "對抗訓練會刻意產生使模型容易出錯的擾動樣本，以提升對擾動的穩健性。"
            "這是另一種正則化或穩健訓練方法，不是 BERT 原始 MLM 的遮罩與詞元"
            "預測目標。"
        ),
        "D": (
            "encoder-decoder 模型可用解碼器依編碼結果重建或生成序列，但原始 BERT"
            "僅使用 Transformer encoder，MLM 只預測被選取的位置，不要求以"
            "decoder 自回歸重建完整句子。"
        ),
    },
    "trap": (
        "MLM 的關鍵不是只看到遮罩，而是能同時利用左右文；另要區分 BERT 的"
        "encoder-only 表示學習與生成模型的 decoder 逐詞輸出，兩者訓練目標不同。"
    ),
    "references": [
        exam_ref(3),
        paper_ref(
            "1810.04805",
            "Devlin et al., BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding（2018）",
            "摘要與第 3.1 節：MLM 隨機遮罩輸入 token，利用左右上下文預測原 token；附 80% [MASK]、10% 隨機、10% 不變策略",
        ),
    ],
}

DRAFTS[4] = {
    "summary": "正確答案是 C。Word2Vec 以局部上下文預測目標學習向量，GloVe 則直接利用全語料的詞—詞共現統計。",
    "concept": (
        "Word2Vec 的 CBOW 與 Skip-gram 都屬預測式方法：前者由上下文預測中心詞，"
        "後者由中心詞預測附近詞，訓練過程逐一掃描局部視窗。GloVe 則先統計全"
        "語料的詞—詞共現矩陣，以加權最小平方法讓向量內積貼近共現次數的對數。"
        "兩者最後都產生靜態詞向量，差別主要在訓練目標使用局部預測或全域統計。"
    ),
    "answerReason": (
        "C 正確對照兩個方法：Word2Vec 透過上下文預測任務學向量，GloVe 明確"
        "使用語料庫的全域共現計數。A、B 把方法特性顛倒或誤配；D 所稱靜態文本"
        "與即時更新不是兩者的定義差異，兩者在更新語料後通常都需要再訓練或"
        "增量處理。"
    ),
    "optionAnalysis": {
        "A": (
            "Word2Vec 不以單純詞頻權重作為核心訓練目標，而是預測中心詞或上下文；"
            "GloVe 雖可從隨機初始化向量開始最佳化，但 Word2Vec 也可如此，"
            "初始化方式不能構成兩者主要差異。"
        ),
        "B": (
            "這個選項把兩者對調了。全域詞—詞共現矩陣是 GloVe 的直接輸入；"
            "Word2Vec 的 CBOW 與 Skip-gram 則以局部視窗中的預測任務更新向量。"
        ),
        "C": (
            "正確。Word2Vec 以神經式的上下文預測目標從局部視窗學習；GloVe"
            "建立並利用全語料共現計數，以加權迴歸結合全域統計與局部語境資訊。"
        ),
        "D": (
            "兩者一般都從既定語料訓練靜態詞向量，也都不會在新文字到達時自動"
            "即時更新。實務上能否增量更新取決於工具與訓練流程，不是 GloVe"
            "相對 Word2Vec 的理論特徵。"
        ),
    },
    "trap": (
        "記憶方式是「Word2Vec 做預測、GloVe 看共現」；不要把初始化方式、是否"
        "使用神經網路或能否即時更新當成核心差別。兩者都屬不依上下文改變的"
        "靜態詞向量。"
    ),
    "references": [
        exam_ref(4),
        paper_ref(
            "1301.3781",
            "Mikolov et al., Efficient Estimation of Word Representations in Vector Space（2013）",
            "第 2 節：CBOW 由上下文預測當前詞，Skip-gram 由當前詞預測上下文",
        ),
        {
            "title": "Pennington, Socher & Manning, GloVe: Global Vectors for Word Representation（2014）",
            "url": "https://nlp.stanford.edu/pubs/glove.pdf",
            "locator": "摘要與第 3 節：模型直接使用全域 word-word co-occurrence counts，並以加權最小平方法學習",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[5] = {
    "summary": "正確答案是 A。若 TF 直接採原始出現次數，長文本會使常見詞計數偏高，削弱權重對關鍵詞重要性的區辨。",
    "concept": (
        "TF-IDF 將詞頻 TF 與逆文件頻率 IDF 相乘：TF 描述某詞在單一文件內的"
        "出現量，IDF 則依該詞出現於多少文件來降低跨文件常見詞的權重。若 TF"
        "使用原始計數，篇幅越長就越有機會累積較大詞數，使文件長度混入權重；"
        "常見緩解方式包括除以文件詞數、L1/L2 正規化或 sublinear TF。"
    ),
    "answerReason": (
        "在四個選項中，只有 A 指向長文本與原始詞頻累積的直接關係：重複出現的"
        "常見詞可能因計數變大而占據較高權重，使真正關鍵但出現次數較少的詞不易"
        "凸顯。B、C 違反 TF-IDF 的基本計算方式；D 也錯把單篇文件長度說成會"
        "改變整體語料的文件頻率。"
    ),
    "optionAnalysis": {
        "A": (
            "正確（依官方題意）。使用未正規化的原始 TF 時，長文件讓常見詞累積"
            "較多次數，詞頻項便可能過度影響乘積。實務可採文件向量正規化、"
            "長度校正或 1 + log(tf) 的次線性詞頻降低影響。"
        ),
        "B": (
            "TF-IDF 以文件與詞的計數為單位，不需要先辨識句子邊界；只要完成"
            "斷詞或 tokenization 就能計算詞頻。句界可能影響其他語言模型，"
            "卻不是 TF-IDF 無法計算的原因。"
        ),
        "C": (
            "IDF 正是跨多份文件計算的量，公式中的文件總數與包含該詞的文件數"
            "都要求語料集合。TF-IDF 不但能同時處理多文件，還必須藉此判斷哪些"
            "詞在整個集合中稀有。"
        ),
        "D": (
            "IDF 取決於包含某詞的文件數相對於文件總數，而不是某一文件有多長。"
            "長文本可能包含更多不同詞，進而略影響語料統計，但不會必然使所有"
            "詞的 IDF 或最終權重趨於相近。"
        ),
    },
    "trap": (
        "分開看 TF 與 IDF：文件內重複次數影響 TF，跨文件出現範圍影響 IDF。"
        "此外，「長文本必然放大」只對某些未做長度正規化的實作成立，不能把它"
        "當成所有 TF-IDF 實作的絕對性質。"
    ),
    "editorialNote": (
        "本站依官方答案 A 撰寫，但選項敘述需加限定：TF-IDF 並非必然讓長文本"
        "的常見詞權重過度放大。scikit-learn 的 TfidfTransformer 預設使用 L2"
        "正規化，也可設定 sublinear_tf；不同 TF 定義與正規化會降低文件長度"
        "影響。待人工複核題目預設的 TF 計算方式。查核日期 2026-08-12。"
    ),
    "references": [
        exam_ref(5),
        sklearn_ref(
            "modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html",
            "TfidfTransformer",
            "公式與參數：tf-idf 為 tf × idf；norm 預設 L2，sublinear_tf 可用 1 + log(tf) 取代原始詞頻",
        ),
    ],
}

DRAFTS[6] = {
    "summary": "正確答案是 B。N-gram 只以固定長度的前序詞估計下一詞，因此難以捕捉超出視窗的長距離依賴。",
    "concept": (
        "N-gram 語言模型以馬可夫近似簡化完整歷史：預測下一詞時，只保留前面"
        "n−1 個詞。例如 trigram 僅看兩個前詞。這讓計數與估計可行，代價是"
        "視窗之外的主詞、指涉或篇章資訊完全不參與當次條件機率；增大 n 又會"
        "造成組合數激增與資料稀疏，許多序列在訓練語料中從未出現。"
    ),
    "answerReason": (
        "B 精確指出固定上下文視窗這個結構限制，所以長句中相距較遠的詞無法"
        "建立直接條件關係。A 把限制說成無法收斂；C 雖描述傳統 N-gram 沒有"
        "語意嵌入，但不是題目所問的長句脈絡主因；D 又過度說成所有詞彼此獨立，"
        "實際上模型仍建模視窗內的條件關係。"
    ),
    "optionAnalysis": {
        "A": (
            "N-gram 主要以頻率計數和條件機率估計，不涉及深度模型常說的梯度"
            "收斂問題。n 變大會增加儲存與資料稀疏困難，但不能說長句因此無法"
            "收斂。"
        ),
        "B": (
            "正確。固定 n 表示每次預測只保留 n−1 個前詞；若關鍵資訊離目標詞"
            "更遠，它就被馬可夫近似捨棄，故難以處理跨長距離的語法與語意依賴。"
        ),
        "C": (
            "傳統計數式 N-gram 確實不會學得稠密詞向量，因而難以把相似詞共享"
            "統計強度；這造成未見組合與語意泛化困難，但題幹問長句上下文，"
            "最直接原因仍是固定視窗。"
        ),
        "D": (
            "N-gram 並非假設所有詞完全獨立，而是假設下一詞在給定最近 n−1 個詞"
            "後，與更早歷史條件獨立。它仍會建立鄰近詞的條件機率，因此這個"
            "說法把有限依賴誤寫成零依賴。"
        ),
    },
    "trap": (
        "把「有限階馬可夫假設」與「詞彼此獨立」分清楚：N-gram 保留視窗內"
        "依賴，只忽略更早歷史。資料稀疏與沒有詞嵌入也是真限制，但題目問的是"
        "長距關係，應選固定視窗。"
    ),
    "references": [
        exam_ref(6),
        {
            "title": "Jurafsky & Martin, Speech and Language Processing（3rd ed. draft）－N-gram Language Models",
            "url": "https://web.stanford.edu/~jurafsky/slp3/3.pdf",
            "locator": "第 3.2 節：以 Markov assumption 將下一詞機率近似為只依賴固定數量的前詞；第 3.4 節討論稀疏與未知 n-gram",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[7] = {
    "summary": "正確答案是 A。IoU 閾值越高，預測框必須與真實框有更高重疊比例，才會被算作正確偵測。",
    "concept": (
        "IoU 是預測邊界框與真實框交集面積除以聯集面積，值介於 0 與 1。評估時"
        "會先設定 IoU 閾值：類別正確且 IoU 達標的預測才可配對為 true positive，"
        "未達標則不能視為正確定位。mAP 再由各類別在不同信心閾值下的"
        "precision-recall 曲線計算 AP 並平均。提高 IoU 閾值代表定位判定更嚴格。"
    ),
    "answerReason": (
        "A 最接近高 IoU 閾值的正確意義：預測框需要與真實框高度重疊，才能被"
        "認定為正確偵測，也就是要求更精準的定位。提高門檻不保證模型本身變好"
        "或 mAP 上升；同一組預測在更嚴格門檻下反而可能有較少 true positives。"
    ),
    "optionAnalysis": {
        "A": (
            "正確（就評估條件而言）。較高門檻要求交集占聯集的比例更高，表示"
            "只有位置與大小更貼近真實框的預測才通過，因此評量著重更精準的"
            "邊界框定位。"
        ),
        "B": (
            "預測框與真實框誤差越大通常會使 IoU 降低，更容易落在閾值以下而被"
            "計為 false positive 或漏失配對。這不會使 mAP 上升，通常會讓"
            "precision 或 recall 下降。"
        ),
        "C": (
            "提高 IoU 門檻可能使同一批預測中 true positives 減少、false positives"
            "增加，因此 recall 不會因門檻變嚴而自然上升。precision 的實際變化"
            "也需看預測排序，不能用此固定方向概括。"
        ),
        "D": (
            "IoU 的分子與分母都由預測框和真實框的面積決定，真實框的大小與位置"
            "會直接影響交集與聯集。它是比例指標但並非不受真實框尺寸影響，"
            "尤其小物件的少量像素偏移可造成明顯 IoU 變化。"
        ),
    },
    "trap": (
        "區分「門檻更嚴格」與「模型更精準」：提高 IoU 閾值只改變評估通過條件，"
        "不會改變既有預測框。也不要斷言 mAP 必然上升；相同預測在嚴格門檻下"
        "通常更難取得高分。"
    ),
    "editorialNote": (
        "本站依官方答案 A 判定，但其「模型偵測結果越精準」應解讀為高 IoU"
        "門檻要求通過者具更精準定位，而不是調高門檻會讓模型輸出本身改善。"
        "待人工複核是否需在前端用語中特別保留此限定。查核日期 2026-08-12。"
    ),
    "references": [
        exam_ref(7),
        {
            "title": "Torchvision－box_iou 官方文件",
            "url": "https://docs.pytorch.org/vision/stable/generated/torchvision.ops.box_iou.html",
            "locator": "box_iou 定義：intersection over union = area of intersection / area of union",
            "checkedAt": CHECKED_AT,
        },
        {
            "title": "COCO－Detection Evaluation 官方說明",
            "url": "https://cocodataset.org/#detection-eval",
            "locator": "Detection evaluation：AP 以 IoU=.50:.05:.95 等門檻回報，並區分 AP at IoU=.50 與 .75",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[8] = {
    "summary": "正確答案是 C。Softmax 將每個輸入轉成機率比例且全部保留；Max-Pooling 則只保留各局部視窗的最大值。",
    "concept": (
        "Softmax 對指定維度的每個輸入取指數並除以指數總和，輸出每項都介於 0"
        "與 1 且加總為 1，常用於互斥類別的分類輸出。Max-Pooling 則用滑動視窗"
        "掃過特徵圖，每個視窗只輸出最大元素，使空間尺寸縮小並保留最強局部"
        "反應。前者是整組分數的正規化，後者是局部選最大值的下採樣。"
    ),
    "answerReason": (
        "C 正確說出資訊處理差異：Softmax 為每個原輸入產生一個非零比例，維度"
        "通常不變；Max-Pooling 每個局部區域僅留下最大值，其他值被捨棄。A、B"
        "混淆兩種運算，D 更將其典型用途互換。"
    ),
    "optionAnalysis": {
        "A": (
            "Softmax 不會把整個張量壓成單一最大值，而是為指定維度中的每一項"
            "輸出機率比例。Max-Pooling 也通常為每個滑動視窗各輸出一個最大值，"
            "而不是必然把整張特徵圖變成單一數字。"
        ),
        "B": (
            "Max-Pooling 只比較局部數值並取最大值，輸出不保證介於 0 與 1，"
            "總和也不會是 1。將任意分數轉成機率分佈是 Softmax 的功能，"
            "不是池化運算。"
        ),
        "C": (
            "正確。Softmax 的每個輸出都由相應輸入轉換而來並以比例呈現，整組"
            "保有所有位置；Max-Pooling 對每個區域僅留下最大反應，其餘局部"
            "數值不再出現在輸出。"
        ),
        "D": (
            "用途顛倒。Softmax 常放在分類模型輸出端，把 logits 轉成機率；"
            "Max-Pooling 常用於卷積特徵圖的空間下採樣，減少寬高與後續計算量。"
        ),
    },
    "trap": (
        "Softmax 的 max 常出現在數值穩定技巧，但它不是「只取最大值」；"
        "Max-Pooling 才會丟掉區域內非最大元素。另注意一般池化會縮小空間尺寸，"
        "Softmax 通常維持形狀。"
    ),
    "references": [
        exam_ref(8),
        {
            "title": "PyTorch－Softmax 官方文件",
            "url": "https://docs.pytorch.org/docs/stable/generated/torch.nn.Softmax.html",
            "locator": "定義：以指數重新縮放指定維度元素，使其落在 [0,1] 且總和為 1",
            "checkedAt": CHECKED_AT,
        },
        {
            "title": "PyTorch－MaxPool2d 官方文件",
            "url": "https://docs.pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html",
            "locator": "定義與公式：對每個滑動 kernel 視窗取最大值",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[9] = {
    "summary": "正確答案是 B。資料增強若改變原有特徵分佈或語意，會製造不合任務的樣本，應檢查並收斂增強策略。",
    "concept": (
        "資料增強的目的，是以仍符合任務標籤與真實情境的轉換，增加資料變化並"
        "降低過擬合。有效增強必須近似標籤保持：影像翻轉、文字替換或合成樣本"
        "不能改掉本來要學的語意，也不能把訓練分佈推到部署時不會出現的區域。"
        "若增強產生分佈偏移或標籤失真，模型會學到錯誤規律，資料變多仍可能退步。"
    ),
    "answerReason": (
        "B 同時提出合理原因與對症策略：先比較增強前後分佈與樣本語意，移除"
        "破壞語意的轉換，並調整強度、機率或組合。A 把資料轉換誤連到參數"
        "初始化；C 已判定比例過高卻反而要求提高比例；D 的標籤問題可能存在，"
        "但半監督學習不是必然或最直接修正。"
    ),
    "optionAnalysis": {
        "A": (
            "隨機初始化通常是模型參數的訓練設定，不是每筆增強樣本需要執行的"
            "步驟。增強資料品質不佳不會靠重新初始化就消失，應直接檢查轉換後"
            "樣本是否仍合理。"
        ),
        "B": (
            "正確。若增強使影像物件、文字語意或資料統計偏離原任務，模型會把"
            "人工產生的偏差當成規律。檢視分佈、抽樣人工查核，並調低不合適"
            "轉換的強度或比例，才是直接改善。"
        ),
        "C": (
            "增強比例過高確實可能使模型偏向人工轉換樣本，但既已判斷此為原因，"
            "改善應是降低或重新平衡比例，而非再提高。學習率只能調整最佳化步幅，"
            "不能修復不合理的樣本分佈。"
        ),
        "D": (
            "增強操作若改變類別語意，原標籤確實可能失真；然而首要處理是修正、"
            "移除或重新標註這些樣本。半監督學習利用未標註資料與模型預測，"
            "並不保證能校正系統性錯標。"
        ),
    },
    "trap": (
        "評估「原因＋策略」題要兩半都正確，C 的前半可能成立但後半方向相反，"
        "D 也從標註問題跳到無法保證修復的半監督學習。資料增強的基本檢查是"
        "轉換後是否仍保留任務語意。"
    ),
    "references": [
        exam_ref(9),
        {
            "title": "TensorFlow－Data augmentation 官方教學",
            "url": "https://www.tensorflow.org/tutorials/images/data_augmentation",
            "locator": "Overview：以會產生可信影像的隨機轉換增加訓練資料多樣性，且增強層只應於訓練期間啟用",
            "checkedAt": CHECKED_AT,
        },
        paper_ref(
            "1909.13719",
            "Cubuk et al., RandAugment: Practical automated data augmentation with a reduced search space（2019）",
            "摘要與方法：增強策略的轉換種類、強度及數量會影響模型表現，需在目標資料集上選擇",
        ),
    ],
}

DRAFTS[10] = {
    "summary": "正確答案是 D。F1 分數是 Precision 與 Recall 的調和平均，可用單一數值綜合兩者。",
    "concept": (
        "Precision = TP/(TP+FP)，回答模型判為正例的樣本中有多少真的為正；"
        "Recall = TP/(TP+FN)，回答所有真實正例中找回多少。F1 = 2PR/(P+R)"
        "是兩者的調和平均，只要其中一項很低，F1 就會受到明顯拉低，因此適合"
        "要求二者均衡的分類情境。它不代表所有業務成本都相同，必要時仍可看"
        "混淆矩陣或使用不同權重的 F-beta。"
    ),
    "answerReason": (
        "題目明確要求同時兼顧 Precision 與 Recall，D 的 F1 正是將兩者合成的"
        "標準分類指標。Accuracy 只計算整體預測正確比例，在類別不平衡時可能"
        "掩蓋少數類漏判；RMSE 與 MSE 衡量連續值預測誤差，並不使用分類的"
        "true positive、false positive 與 false negative。"
    ),
    "optionAnalysis": {
        "A": (
            "Accuracy 是所有預測中答對的比例，適合類別相對平衡且錯誤成本近似"
            "的情境。若負例遠多於正例，全部猜負也可能有高準確率，卻有零召回率，"
            "所以它不直接平衡 Precision 與 Recall。"
        ),
        "B": (
            "RMSE 是均方誤差開根號，單位與預測目標相同，常用於房價、需求量等"
            "連續值迴歸。它衡量數值殘差大小，不是由分類的 Precision 與 Recall"
            "組成。"
        ),
        "C": (
            "MSE 將預測值與真值的差平方後取平均，會對較大殘差施以較重懲罰，"
            "同樣是迴歸損失或評估指標。它不描述誤報與漏報之間的平衡。"
        ),
        "D": (
            "正確。F1 使用調和平均 2PR/(P+R)，Precision 或 Recall 任一偏低都"
            "無法靠另一項很高完全補償，故能以單一數值評估兩者是否同時維持"
            "良好水準。"
        ),
    },
    "trap": (
        "先分任務：MSE、RMSE 是連續值迴歸；Accuracy 與 F1 是分類。再看題幹"
        "是否直接點名 Precision、Recall；若要等權綜合就是 F1，若業務偏重其中"
        "一方則考慮 F-beta 或分開檢視。"
    ),
    "references": [
        exam_ref(10),
        sklearn_ref(
            "modules/model_evaluation.html#precision-recall-f-measure-metrics",
            "Metrics and scoring－Precision, recall and F-measures",
            "第 3.4.4.9 節：precision、recall 定義；F-beta 為兩者加權調和平均，beta=1 即 F1",
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
