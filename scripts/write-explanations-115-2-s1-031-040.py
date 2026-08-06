"""Write the phase-two explanation drafts for 115-2 elementary subject one, Q31-Q40.

Same guarantees as the earlier batches: the script only fills ``explanation`` on
questions that already exist, aborts if an official answer no longer matches the
answer a draft was written against, and refuses to overwrite anything already
marked reviewed.

Every cited URL was opened and checked on the date recorded in ``checkedAt``.
Guide page numbers use the study guide's own section numbering (3-N), which is
the PDF page minus six.

Usage::

    python scripts/write-explanations-115-2-s1-031-040.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-elementary-2-ai-foundation"
AUTHOR = "Claude Code（AI 輔助初稿）"
AUTHORED_AT = "2026-08-06"
EXAM_CHECKED_AT = "2026-07-29"
REUSED_CHECKED_AT = "2026-07-31"
TODAY_CHECKED_AT = "2026-08-06"

EXAM_PDF = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/115年第二次初級AI應用規劃師_第一科_"
    "人工智慧基礎概論_公告試題_20260604212644.pdf"
)
GUIDE_PDF = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/AI應用規劃師(初級)-學習指引-科目1_"
    "人工智慧基礎概論1141203_20251222172144.pdf"
)
SK = "https://scikit-learn.org/stable/modules/"
DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def exam_ref(number: int) -> dict:
    return {
        "title": "115 年第二次初級 AI 應用規劃師－人工智慧基礎概論公告試題",
        "url": EXAM_PDF,
        "locator": f"第 {number} 題題幹、選項與官方答案",
        "checkedAt": EXAM_CHECKED_AT,
    }


def guide_ref(locator: str) -> dict:
    return {
        "title": "iPAS AI 應用規劃師（初級）學習指引－科目一 人工智慧基礎概論",
        "url": GUIDE_PDF,
        "locator": locator,
        "checkedAt": REUSED_CHECKED_AT,
    }


def sk_ref(page: str, locator: str, title: str) -> dict:
    return {
        "title": f"scikit-learn－{title}",
        "url": f"{SK}{page}",
        "locator": locator,
        "checkedAt": REUSED_CHECKED_AT,
    }


def arxiv_ref(arxiv_id: str, title: str, locator: str) -> dict:
    return {
        "title": title,
        "url": f"https://arxiv.org/abs/{arxiv_id}",
        "locator": locator,
        "checkedAt": REUSED_CHECKED_AT,
    }


EXPECTED_ANSWER = {
    31: "D", 32: "D", 33: "B", 34: "C", 35: "A",
    36: "A", 37: "D", 38: "C", 39: "C", 40: "C",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[31] = {
    "summary": "正確答案是 D。PDP 呈現的是特徵對預測的平均整體趨勢，無法回答單一批次資料的個別歸因問題。",
    "concept": (
        "部分依賴圖（Partial Dependence Plots, PDP）是模型層級的全域解釋工具："
        "固定我們關注的特徵（如溫度），把其他特徵的值邊際化（平均掉）之後，"
        "畫出模型預測值隨該特徵變動的曲線。scikit-learn 文件說明，PDP 顯示"
        "目標回應與所關注輸入特徵之間的依賴關係，呈現的是該特徵的「平均效果」。\n"
        "正因為是對整個資料集取平均，PDP 回答的是「整體而言，溫度升高時良品率"
        "如何變化」這類全域趨勢問題，不會告訴你「這一筆樣本的預測被哪個特徵"
        "推動了多少」。要看單一樣本層級的關係，得改用逐筆各畫一條線的個體條件"
        "期望圖（ICE），或 SHAP、LIME 這類局部歸因方法；文件也提醒，PDP 的"
        "平均可能掩蓋特徵交互作用造成的異質關係。"
    ),
    "answerReason": (
        "主管想問的是「某一筆瑕疵批次中，溫度是不是主要原因」，這是單一樣本的"
        "局部歸因問題。PDP 在計算時已把其他特徵邊際化、對所有樣本取平均，"
        "產出的只有溫度對良品率的整體趨勢曲線；平均的過程也可能掩蓋批次之間的"
        "異質差異，因此無法據以判斷特定批次的成因，D 正確指出了這個限制。"
    ),
    "optionAnalysis": {
        "A": (
            "PDP 確實不顯示預測準確率——準確率要在測試集上以評估指標另行計算，"
            "這句話本身沒有說錯。但它沒有點中本題的癥結：主管的問題卡在"
            "「能不能做單一批次的歸因」，就算 PDP 附上準確率資訊，仍然回答不了"
            "個別批次的原因，所以 A 不是最能說明此情境的限制。"
        ),
        "B": (
            "說 PDP 僅能反映模型輸出結果、無法提供任何特徵影響資訊，把它的本職"
            "功能整個抹掉了。PDP 存在的目的正是呈現特徵對預測輸出的邊際影響"
            "趨勢，例如溫度上升時良品率平均如何變化；它的限制在於只到「平均、"
            "全域」的層級，而不是完全沒有特徵資訊。"
        ),
        "C": (
            "PDP 並非只能分析單一特徵：常見實作支援兩個特徵的二維 PDP，"
            "以等高線呈現交互影響，只是超過兩個特徵便難以視覺化。更重要的是，"
            "本題的困難出在「全域平均」與「單筆歸因」的落差，而不是可分析的"
            "特徵數量，C 說的限制既不精確也不是此情境的重點。"
        ),
        "D": (
            "正確。PDP 把其他特徵邊際化後對全體樣本取平均，輸出的是溫度對"
            "良品率的整體趨勢；單一瑕疵批次的預測是多個特徵在該筆數值組合下"
            "共同作用的結果，平均曲線無法回推這一筆的成因。想做逐筆診斷，"
            "應改用 ICE、SHAP、LIME 這類局部解釋工具。"
        ),
    },
    "trap": (
        "第一，先分清全域解釋與局部解釋：PDP、排列重要性看整體平均，ICE、"
        "SHAP、LIME 看單筆樣本；題目一問到「某一筆資料的原因」，就要想到局部"
        "工具。第二，別把「PDP 有限制」擴大成「PDP 沒有用」，選項 B 這種全盤"
        "否定的敘述通常是干擾項。"
    ),
    "references": [
        exam_ref(31),
        {
            "title": "scikit-learn－5.1. Partial Dependence and Individual Conditional Expectation plots",
            "url": "https://scikit-learn.org/stable/modules/partial_dependence.html",
            "locator": "第 5.1.1 節：PDP 顯示目標回應與所關注輸入特徵間的依賴關係，對其餘特徵邊際化，呈現特徵的平均效果；第 5.1.2 節：ICE 逐樣本各畫一條線，PDP 的平均可能掩蓋交互作用造成的異質關係",
            "checkedAt": TODAY_CHECKED_AT,
        },
    ],
}

DRAFTS[32] = {
    "summary": "正確答案是 D。LIME 的代理模型是用來擬合原黑箱模型在目標實例附近預測行為的簡單可解釋模型。",
    "concept": (
        "LIME（Local Interpretable Model-agnostic Explanations）解釋單一預測的"
        "流程是：在要解釋的樣本附近產生大量擾動樣本，拿原黑箱模型對這些擾動"
        "樣本評分，再以距離加權訓練一個簡單的可解釋模型（例如稀疏線性模型）"
        "去逼近黑箱模型在該鄰域內的輸出，這個簡單模型就是代理模型"
        "（Surrogate model）。\n"
        "Ribeiro 等人的原始論文把這個設計描述為「以在預測附近學習可解釋模型的"
        "方式，對任何分類器的預測提供可解釋且忠實的說明」。理解代理模型的兩個"
        "關鍵字是「局部」與「近似」：它只需要在目標樣本的鄰域內貼近黑箱模型的"
        "行為，離開鄰域就不保證有效；它的用途是解釋，實際的預測仍由原黑箱模型"
        "負責。"
    ),
    "answerReason": (
        "題幹說系統「建立了一個簡化模型來近似原模型在該筆資料附近的行為」，"
        "這句話就是代理模型的定義：在目標實例（該筆信貸申請）附近，以可解釋的"
        "簡單模型擬合原黑箱模型的預測行為，再從簡單模型的權重讀出各特徵在這筆"
        "決策中的影響方向與大小，因此選 D。"
    ),
    "optionAnalysis": {
        "A": (
            "全局代理模型確實是一種存在的解釋手法——以單一簡單模型逼近黑箱模型"
            "在整個輸入空間的行為。但 LIME 名稱裡的 Local 表明它刻意只做局部"
            "近似：單筆資料附近的行為用線性模型就貼得住，整個決策面卻往往複雜到"
            "簡單模型裝不下；把 LIME 的代理模型說成全局解釋所有預測，方向正好"
            "相反。"
        ),
        "B": (
            "產生擾動資料是 LIME 流程中的取樣步驟，用來探測黑箱模型在鄰域內的"
            "反應，它本身不是代理模型。代理模型是拿這些擾動樣本與黑箱模型的"
            "輸出訓練出來的簡單模型，是流程的最終產物；選項把前置的資料生成"
            "機制與代理模型混為一談。"
        ),
        "C": (
            "LIME 的代理模型不是獨立訓練的生成式模型，也不負責輔助預測："
            "它以黑箱模型的輸出為擬合目標，存在目的只有解釋這一筆決策。"
            "信貸審核結果仍由原模型做成；若拿代理模型參與預測，一離開該筆資料"
            "的鄰域，它與原模型的行為就可能明顯偏離。"
        ),
        "D": (
            "正確。代理模型的意義正是在目標實例附近，用一個人看得懂的簡單模型"
            "擬合原黑箱模型的預測行為；因為只要求局部貼合，簡單模型的權重就能"
            "忠實反映黑箱模型在這筆申請上如何看待各特徵，達成不改動原模型又能"
            "解釋個案的目標。"
        ),
    },
    "trap": (
        "第一，抓住 LIME 的 L（Local）：代理模型只在單筆樣本附近有效，選項"
        "寫成「全局解釋所有預測」就是陷阱。第二，分清代理模型的角色是「解釋」"
        "而不是「預測」：它不會取代原模型上線，也不是用來生成資料或輔助推論的"
        "模型。"
    ),
    "references": [
        exam_ref(32),
        arxiv_ref(
            "1602.04938",
            "Ribeiro, Singh & Guestrin, \"Why Should I Trust You?\": Explaining the Predictions of Any Classifier (arXiv)",
            "摘要：LIME 以在預測附近學習可解釋模型的方式，對任何分類器的預測提供可解釋且忠實的說明",
        ),
    ],
}

DRAFTS[33] = {
    "summary": "正確答案是 B。稀疏專家混合每次推論只啟用部分專家子網路，讓模型總參數規模很大時仍能控制單次運算成本。",
    "concept": (
        "要同時做到「模型規模大」與「運算有效率」，關鍵技術之一是條件計算"
        "（Conditional Computation）：不讓每個輸入都動用全部參數，而是依輸入"
        "內容挑選網路的一部分來計算。稀疏專家混合（Sparse Mixture-of-Experts, "
        "MoE）是其代表：模型在部分層放入多個並列的專家子網路（Experts），"
        "再由可訓練的閘控網路（Gating Network）替每個輸入選出少數幾個專家參與"
        "計算，其餘專家閒置。\n"
        "Shazeer 等人的論文說明，稀疏閘控 MoE 層可由上千個前饋子網路組成，"
        "閘控網路為每個樣本決定稀疏的專家組合，在計算效率僅小幅損失的情況下，"
        "把模型容量提升超過一千倍。換句話說，「總參數量」與「單次前向實際啟用"
        "的參數量」被拆開了：規模可以持續擴大以維持生成品質，單次推論的成本"
        "卻只隨被選中的專家數成長。"
    ),
    "answerReason": (
        "題幹的條件是模型規模較大，同時要兼顧運算效率。稠密模型的運算量與"
        "總參數同步成長，兩者難以同時成立；稀疏 MoE 以閘控路由讓每次推論只"
        "啟用部分專家，總參數大幅擴增時單次計算量仍受控，正是 B 所述「每次僅"
        "使用部分模型來提升效率」的設計，因此選 B。"
    ),
    "optionAnalysis": {
        "A": (
            "單一稠密（Dense）Transformer 的特徵是每個輸入的前向計算都用到全部"
            "模型參數，品質可以靠加大參數堆出來，但運算成本也隨參數量等比上升。"
            "題幹強調規模較大時仍要兼顧效率，稠密架構恰好是效率隨規模惡化的"
            "類型，與需求方向相反。"
        ),
        "B": (
            "正確。稀疏專家混合在每層放置多個專家子網路，由閘控網路依輸入選出"
            "少數專家計算、其餘不參與；總參數可以擴充到極大以維持生成品質，"
            "單次推論只付出被啟用那部分的成本，同時滿足「規模大」與「有效率」"
            "兩個要求。"
        ),
        "C": (
            "生成對抗網路（GAN）由生成器與鑑別器對抗訓練，長於產生逼真影像，"
            "早期影像風格轉換確實常用它。但選項描述的是「兩個模型互相比較以"
            "提升品質」的訓練機制，沒有觸及「每次只啟用部分參數」的設計，"
            "無法說明大規模模型如何兼顧運算效率，而後者才是題幹點名的重點。"
        ),
        "D": (
            "卷積神經網路（CNN）以卷積核擷取影像局部特徵，是視覺任務的基礎"
            "架構，也能用於影像轉換。但 CNN 的每次前向仍會用到全部權重，"
            "「直接進行影像轉換」的敘述同樣沒有回應題幹「模型規模較大仍兼顧"
            "運算效率」的設計問題，說明力不如稀疏啟用的專家混合。"
        ),
    },
    "trap": (
        "第一，看到「規模大」與「效率」同時出現，先想條件計算與稀疏啟用"
        "（MoE），而不是先想模型家族（GAN、CNN）本身。第二，分清「總參數量」"
        "與「單次啟用參數量」：MoE 的關鍵是兩者脫鉤，稠密模型則兩者綁在一起，"
        "這是 A 與 B 的分水嶺。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
        "待查項目：題幹以 2025 年照片轉公仔風格影像服務為背景，未指名特定產品；"
        "商用模型是否採 MoE 屬未公開的內部實作，本詳解僅依選項文字的架構特性"
        "作答，未認定特定產品的實作方式。查核日期 2026-08-06。"
    ),
    "references": [
        exam_ref(33),
        {
            "title": "Shazeer et al., Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer（arXiv:1701.06538）",
            "url": "https://arxiv.org/abs/1701.06538",
            "locator": "摘要：稀疏閘控 MoE 層由可達數千個前饋子網路組成，可訓練的閘控網路為每個樣本選出稀疏的專家組合；以條件計算在計算效率僅小幅損失下實現逾千倍的模型容量提升",
            "checkedAt": TODAY_CHECKED_AT,
        },
    ],
}

DRAFTS[34] = {
    "summary": "正確答案是 C。CLIP 以網路蒐集的圖文配對資料訓練，DINO 只用未標註影像做自蒸餾，兩者的資料型態不同。",
    "concept": (
        "兩個模型都不依賴人工逐張標註的類別標籤，但取得監督訊號的來源不同。"
        "CLIP（Contrastive Language-Image Pre-training）的訓練資料是從網路蒐集"
        "的 4 億對（影像，文字）配對，預訓練任務是判斷哪段文字說明與哪張影像"
        "相配，等於把自然語言當成影像表示的監督訊號。\n"
        "DINO 則是純影像的自監督方法，論文自述為「無標籤的自蒸餾"
        "（self-distillation with no labels）」：同一張未標註影像經過不同裁切"
        "與增強後，分別送進學生網路與教師網路，訓練學生的輸出貼近教師，"
        "全程不使用文字或人工標籤。因此本題的考點就落在資料型態：CLIP 需要"
        "圖文成對資料，DINO 只需要未標註影像。"
    ),
    "answerReason": (
        "題目問訓練資料型態的差異。CLIP 的每筆訓練樣本是一張影像加上一段對應"
        "文字，靠配對關係學到圖文對齊的表示；DINO 的訓練樣本只有影像本身，"
        "監督訊號由同一影像的不同視角自行產生。C 正確描述「CLIP 用圖像與文字"
        "配對資料、DINO 用未標註圖像資料」的對比，因此選 C。"
    ),
    "optionAnalysis": {
        "A": (
            "監督式學習指使用人工標註的類別標籤（例如 ImageNet 的分類標記）"
            "訓練，而 CLIP 與 DINO 的共同賣點正是避開人工逐張標註：CLIP 用網路"
            "上天然成對的圖文資料，DINO 完全不用標籤。這個選項對兩個模型的資料"
            "型態都描述錯誤。"
        ),
        "B": (
            "「皆使用未標註圖像資料」只對 DINO 成立。CLIP 的訓練資料除了影像"
            "還必須有成對的文字說明，否則無法定義「哪段文字配哪張圖」的對比"
            "學習任務；把 CLIP 說成只用未標註圖像，抹掉了它賴以運作的語言監督"
            "訊號，與論文設定不符。"
        ),
        "C": (
            "正確。CLIP 以 4 億對取自網路的圖文配對做對比學習，文字是它的監督"
            "來源；DINO 以未標註影像做無標籤自蒸餾，監督訊號來自同一影像的"
            "不同增強視角。兩者對資料的需求一個是「圖加文」、一個是「只有圖」，"
            "正是題目要辨別的差異。"
        ),
        "D": (
            "把兩個模型的資料來源互換了：CLIP 並非只用未標註影像，DINO 也不"
            "使用圖文配對，敘述與兩篇論文的設定完全相反。記憶時可抓名稱線索"
            "——CLIP 的 Language 說明它離不開文字，DINO 論文強調 no labels，"
            "只吃未標註影像。"
        ),
    },
    "trap": (
        "第一，「自監督」不等於「資料只有影像」：CLIP 的監督訊號來自天然成對"
        "的文字，DINO 來自影像自身的增強視角，兩者都不需人工標註但資料型態"
        "不同。第二，這類對照題最常見的陷阱是 D 這種左右互換，先記死"
        "「CLIP＝圖文配對、DINO＝純影像」再核對選項。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
        "待查項目：題幹將 CLIP 歸為自監督學習；CLIP 論文自述為以自然語言為"
        "監督訊號（natural language supervision），學界亦有將其歸為弱監督或"
        "圖文對比學習者。本題依官方答案聚焦兩者訓練資料型態的差異，分類名稱的"
        "歧義不影響作答。查核日期 2026-08-06。"
    ),
    "references": [
        exam_ref(34),
        {
            "title": "Radford et al., Learning Transferable Visual Models From Natural Language Supervision（arXiv:2103.00020）",
            "url": "https://arxiv.org/abs/2103.00020",
            "locator": "摘要：以 4 億對取自網路的（影像，文字）配對資料預訓練，任務為預測哪段文字說明與哪張影像相配",
            "checkedAt": TODAY_CHECKED_AT,
        },
        {
            "title": "Caron et al., Emerging Properties in Self-Supervised Vision Transformers（arXiv:2104.14294）",
            "url": "https://arxiv.org/abs/2104.14294",
            "locator": "摘要：DINO 為無標籤自蒸餾（self-distillation with no labels）方法，以自監督方式訓練 Vision Transformer，不使用人工標籤",
            "checkedAt": TODAY_CHECKED_AT,
        },
    ],
}

DRAFTS[35] = {
    "summary": "正確答案是 A。傳統 Transformer 推理時受固定長度上下文窗口限制，難以一次整合散落在長文件各處的資訊。",
    "concept": (
        "Transformer 以自注意力讓序列中任意兩個位置直接互相參照，但一次能處理"
        "的內容受上下文窗口（Context Window）限制：模型生成回應時所能參照的"
        "全部文本（含輸入與輸出）必須落在固定的 token 上限內，可視為模型的"
        "工作記憶。長篇法規文件常超過窗口，必須截斷或分段餵入，散落在不同段落"
        "的條文因此無法在同一次推理中同時被看到。\n"
        "即使文件塞得進窗口，長上下文的利用品質也會退化：研究顯示，當關鍵資訊"
        "位於長上下文中段時，模型表現明顯下滑；隨著 token 數增加，準確率與"
        "召回率也逐步下降。這兩層限制加起來，正好解釋題幹「需整合文件中彼此"
        "距離較遠、較不相關的資訊時，連貫性與準確性下降」的現象。"
    ),
    "answerReason": (
        "題幹症狀是：問題需要整合散落在長文件各處、彼此關聯較弱的資訊時，"
        "回答品質明顯變差。這對應傳統 Transformer 的限制——推理時只能在固定"
        "長度的上下文窗口內作業，超出窗口的內容進不了模型；即便同在窗口內，"
        "距離遙遠的分散資訊實際被利用的效率也隨長度下降。A 同時點出固定窗口與"
        "難以整合分散資訊兩個要素，最能說明此情境。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。傳統 Transformer 的可處理長度在推理時有固定上限，長篇法規"
            "必須截斷或分段；需要跨段整合的資訊若不在同一個窗口內，模型無法"
            "同時參照，即使同在窗口內，分散於前後兩端的關鍵內容也常被利用得"
            "不完整，與使用者反映的症狀一致。"
        ),
        "B": (
            "「能記住的內容取決於訓練語料」說的是模型參數化知識的範圍——訓練時"
            "沒學過的知識，推理時答不出來，通常靠檢索或微調補足。但題幹的法規"
            "文件已經以輸入的形式提供給模型，問題出在讀入與整合長輸入的能力，"
            "而非模型先前學過什麼，把症狀歸給訓練語料對不上情境。"
        ),
        "C": (
            "前半句符合事實：自注意力的計算量約隨序列長度平方成長，長序列的"
            "處理效率確實下降。錯在後半句「仍可完整處理所有輸入內容」——"
            "上下文窗口有固定的 token 上限，超長文件必須截斷或分段，模型無法"
            "完整處理任意長度的輸入，這半句與事實相反，整條敘述因此不成立。"
        ),
        "D": (
            "Transformer 的權重在推理階段是固定的，不需要也不會在每次推理後"
            "重新訓練；新資訊可以直接放進上下文或透過檢索當場提供給模型使用，"
            "只是受窗口長度限制。把「記住新資訊」說成必須重新訓練，混淆了參數"
            "更新（訓練）與上下文提供（推理）兩種機制。"
        ),
    },
    "trap": (
        "第一，分清兩種「記不住」：訓練語料沒涵蓋是知識缺口，靠檢索或微調補；"
        "文件塞不進窗口、分散資訊整合不佳，是架構層的上下文限制，靠加長窗口、"
        "分段與檢索（RAG）緩解。第二，遇到半對半錯的選項要整句檢查：C 的效率"
        "下降是真的，「仍可完整處理」才是致命錯誤。"
    ),
    "references": [
        exam_ref(35),
        {
            "title": "Claude Developer Platform 文件－Context windows",
            "url": "https://platform.claude.com/docs/en/docs/build-with-claude/context-windows",
            "locator": "How the context window works：上下文窗口指模型生成回應時所能參照的全部文本，相當於模型的工作記憶；隨 token 數增加，準確率與召回率會逐步下降（context rot）",
            "checkedAt": TODAY_CHECKED_AT,
        },
        arxiv_ref(
            "2307.03172",
            "arXiv－Lost in the Middle: How Language Models Use Long Contexts",
            "關鍵資訊位於長上下文中段時，模型表現顯著下降，顯示長上下文噪音會影響回答品質",
        ),
    ],
}

DRAFTS[36] = {
    "summary": "正確答案是 A。持續比對預測值與實際值的差距，並依梯度逐步更新模型內部參數，正是優化器在訓練迴圈中的職責。",
    "concept": (
        "深度學習的訓練迴圈可以拆成幾個分工明確的元件：模型架構決定資料如何"
        "一層層被轉換；損失函數把預測值與實際值的差距量化成一個數字；接著以"
        "反向傳播算出損失對每個參數的梯度；最後由優化器（Optimizer）依據這些"
        "梯度更新模型內部參數，常見演算法包括 SGD、Adam、RMSprop 等。\n"
        "PyTorch 官方文件的描述是：優化器物件會保存當前狀態，並依據計算出的"
        "梯度更新參數；訓練時每一步先以 loss.backward() 算出梯度，再呼叫 "
        "optimizer.step() 完成一次參數更新。這個「算差距、求梯度、更新參數」"
        "的循環反覆進行，直到損失收斂、預測趨於穩定，正是題幹工程師描述的"
        "機制。"
    ),
    "answerReason": (
        "工程師的敘述有三個要素：比對預測值與實際值的差距、透過一套機制逐步"
        "調整內部參數、直到結果趨於穩定。差距的量化由損失函數負責，但「依據"
        "差距逐步調整參數直到收斂」這個執行更新的機制，對應的元件是優化器——"
        "它拿到梯度後決定每個參數往哪個方向、移動多少，四個選項中只有 A 承擔"
        "這個角色。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。優化器是訓練迴圈中依梯度更新參數的元件：每一輪以損失函數"
            "量化預測與實際值的差距，反向傳播求出梯度後，由優化器（如 SGD、"
            "Adam）按學習率與各自的更新規則調整權重，迭代到損失不再明顯下降，"
            "與題幹「逐步調整參數直到趨於穩定」的描述一致。"
        ),
        "B": (
            "資料前處理模組在訓練開始前運作，負責清理缺失值、標準化數值、編碼"
            "類別等，讓資料變成模型能讀取的格式；它不參與訓練中的參數更新，"
            "也不會比對預測值與實際值。題幹描述的是訓練迴圈內反覆迭代的機制，"
            "發生時點與職責都對不上。"
        ),
        "C": (
            "模型架構指網路的層數、每層型態與連接方式（如卷積層、注意力層的"
            "堆疊），決定參數擺在哪裡、資料怎麼流動；它是「被調整對象」的骨架，"
            "本身不是執行調整的機制。工程師說的是那套持續更新參數的流程，"
            "而不是網路長什麼樣子。"
        ),
        "D": (
            "激活函數（如 ReLU、Sigmoid）為神經元輸出加入非線性，讓網路能逼近"
            "複雜函數；它在前向傳播時逐點運算，不比對預測與實際值，也不主動"
            "更新任何參數。它影響的是梯度傳遞的品質，真正拿梯度去改參數的仍是"
            "優化器。"
        ),
    },
    "trap": (
        "第一，把訓練迴圈的分工背清楚：損失函數「量差距」、反向傳播「算梯度」、"
        "優化器「改參數」，題目描述哪個動作就選哪個元件。第二，別看到「調整」"
        "就想到架構或激活函數：前者是被更新的結構，後者是前向的非線性轉換，"
        "都不是執行更新的機制。"
    ),
    "references": [
        exam_ref(36),
        {
            "title": "PyTorch 官方文件－torch.optim",
            "url": "https://docs.pytorch.org/docs/2.13/optim.html",
            "locator": "套件說明：torch.optim 實作各種最佳化演算法；優化器物件保存當前狀態並依據計算出的梯度更新參數，以 loss.backward() 計算梯度後呼叫 optimizer.step() 執行更新，提供 SGD、Adam 等演算法",
            "checkedAt": TODAY_CHECKED_AT,
        },
        {
            "title": "Keras 官方文件－Optimizers",
            "url": "https://keras.io/api/optimizers/",
            "locator": "優化器為編譯 Keras 模型的兩個必要引數之一（另一為損失函數），文件列出 SGD、Adam、RMSprop 等優化器與學習率排程用法",
            "checkedAt": TODAY_CHECKED_AT,
        },
    ],
}

DRAFTS[37] = {
    "summary": "正確答案是 D。顯著性圖以梯度直接算出影像中每個像素對本次預測的影響力，天生就是標示關鍵區域的工具。",
    "concept": (
        "醫院的需求是：對「這一張」X 光的「這一次」判讀，標出影像中影響最大的"
        "區域。這屬於影像上的局部解釋，而且要求輸出本身就是與影像對齊的重要性"
        "熱圖。\n"
        "顯著性圖（Saliency Map）正是為此設計：Simonyan 等人的論文以「類別"
        "分數對輸入影像的梯度」計算類別顯著性圖，梯度大的像素代表稍微改動就會"
        "明顯影響該類別的分數，即為模型判讀時最敏感的區域；結果以熱度圖疊在"
        "原影像上，放射科醫師可以直接對照病灶位置，檢視模型是否看對地方。"
        "它針對給定的影像與類別逐筆產生，粒度直達像素，不需要先把影像轉成"
        "表格特徵。"
    ),
    "answerReason": (
        "四個選項中，LIME、SHAP 與 PDP 都是與資料型態無關的通用歸因框架，"
        "要用在影像上得先做超像素分割或遮蔽取樣，產出的是區塊或特徵層級的近似"
        "歸因；顯著性圖則是針對影像模型的原生方法，直接以梯度產生與原圖逐像素"
        "對齊的重要性熱圖，「標示影像中對預測結果影響最大的區域」就是它的定義"
        "輸出，最直接滿足評估委員會的需求，因此選 D。"
    ),
    "optionAnalysis": {
        "A": (
            "LIME 的作法是在目標樣本附近產生擾動樣本，再以簡單模型做局部近似；"
            "用於影像時需先切成超像素、反覆遮蔽採樣，得到的是區塊層級的近似"
            "解釋，計算成本高且結果受分割方式影響。它可以間接標出重要區塊，"
            "但不如以梯度直接產生像素級熱圖的方法來得直接。"
        ),
        "B": (
            "SHAP 以 Shapley 值把單筆預測拆解成各特徵的貢獻，理論性質完整，"
            "常用於表格資料的逐筆歸因；用在影像上同樣要透過遮蔽或近似取樣把"
            "像素群當成特徵處理，運算負擔大。本題只要求標示影響最大的影像區域，"
            "SHAP 的特徵貢獻框架不是為影像區域標示而生的最直接工具。"
        ),
        "C": (
            "部分依賴圖（PDP）呈現的是某個特徵在整個資料集上對預測的平均影響"
            "趨勢，屬於全域解釋，輸入通常是表格化特徵。本題要的是「單一病患、"
            "單一次診斷」的區域標示，PDP 既不逐筆解釋，也不輸出影像熱圖，"
            "層級與輸出形式都對不上需求。"
        ),
        "D": (
            "正確。顯著性圖以類別分數對輸入影像逐像素求梯度，直接得到「哪些"
            "像素最影響本次判讀」的熱圖，針對給定影像與類別逐筆產生，可疊在 "
            "X 光片上供醫師比對病灶，正是「標示影像中影響最大區域」需求的原生"
            "解法。"
        ),
    },
    "trap": (
        "第一，先分層級再選工具：PDP 是全域平均，LIME、SHAP、顯著性圖才做單筆"
        "解釋；題目問單一影像的判讀依據，就先刪掉 PDP。第二，同屬局部解釋時再"
        "比「直接程度」：顯著性圖是影像原生方法、輸出像素級熱圖，LIME 與 SHAP "
        "是通用框架，需先分割或遮蔽才能套到影像上。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
        "待查項目：LIME 與 SHAP 經超像素分割或遮蔽取樣後亦能產生影像區域級"
        "解釋，本題判 D 的依據是題幹強調「最能直接」標示影像區域，而顯著性圖"
        "以梯度原生輸出像素級熱圖，屬程度比較而非絕對排除，建議複核者確認此"
        "判準。查核日期 2026-08-06。"
    ),
    "references": [
        exam_ref(37),
        arxiv_ref(
            "1312.6034",
            "Simonyan, Vedaldi & Zisserman, Deep Inside Convolutional Networks: Visualising Image Classification Models and Saliency Maps (arXiv)",
            "摘要：以類別分數對輸入影像的梯度計算類別顯著性圖，該圖針對給定的影像與類別而產生",
        ),
        arxiv_ref(
            "1602.04938",
            "Ribeiro, Singh & Guestrin, \"Why Should I Trust You?\": Explaining the Predictions of Any Classifier (arXiv)",
            "摘要：LIME 以在預測附近學習可解釋模型的方式，對任何分類器的預測提供可解釋且忠實的說明",
        ),
        arxiv_ref(
            "1705.07874",
            "Lundberg & Lee, A Unified Approach to Interpreting Model Predictions (arXiv)",
            "摘要：SHAP 為每個特徵指派對應於特定預測的重要性數值，屬於加法式特徵歸因",
        ),
    ],
}

DRAFTS[38] = {
    "summary": "正確答案是 C。異常樣本難以事先完整標記、只能以大量正常評論的分布找偏離，對應半監督式設定下的異常偵測。",
    "concept": (
        "異常偵測的資料現實是：正常樣本極多，異常樣本稀少、樣態多變且難以事先"
        "窮舉標記。常見做法是主要以正常資料學習「正常長什麼樣」，再把明顯偏離"
        "正常分布的新樣本判為異常；scikit-learn 文件把這種「以未被異常污染的"
        "資料建模、再對新觀測值偵測異常」的設定稱為新奇偵測（Novelty "
        "Detection），文獻上也常稱為半監督式異常偵測——它介於兩端之間："
        "不像監督式需要兩類標註齊備，也不是毫無先驗的探索，而是利用「訓練資料"
        "幾乎都是正常」這個已知條件。\n"
        "題幹的系統正是這個設定：平台握有大量正常評論，要偵測的是大量重複貼文、"
        "機器人生成內容這類難以事先完整標記的異常行為，因此以正常分布為基準、"
        "對偏離者示警是最合適的框架。"
    ),
    "answerReason": (
        "題幹給了兩個條件：異常樣本難以事先完整標記（排除需要兩類標註齊備的"
        "作法），以及系統主要依據大量正常評論的分布來識別偏離行為（以正常資料"
        "建模、對偏離示警）。這正是半監督式異常偵測的定義——用幾乎都是正常的"
        "資料學習正常分布，新評論若明顯偏離該分布即視為異常，連未曾見過的新型"
        "灌水手法也能因偏離而被抓到，因此選 C。"
    ),
    "optionAnalysis": {
        "A": (
            "關聯規則挖掘從交易式資料中找「哪些項目經常一起出現」的規律，典型"
            "應用是購物籃分析；用在評論上找出常見字詞組合，產出的是共現規則，"
            "而不是「偏離正常分布」的判定。它沒有把正常行為建成可比對的基準，"
            "無法對新型異常評論示警，與題幹的偵測目標不合。"
        ),
        "B": (
            "監督式二元分類要同時有足量且具代表性的正常與異常標註樣本，才能學出"
            "兩類的邊界；題幹已言明異常樣本難以事先完整標記，而且機器人手法會"
            "不斷翻新，分類器只認得訓練時看過的異常型態，新手法會直接漏接。"
            "標註前提不成立，是它在本題出局的原因。"
        ),
        "C": (
            "正確。以大量正常評論學習正常行為的分布，再把明顯偏離的評論行為"
            "（如異常密集的重複貼文、非人類的發文節奏）標記出來；這種只需正常"
            "資料、不必窮舉異常型態的設定，正是半監督式異常偵測的用法，"
            "scikit-learn 稱之為新奇偵測。"
        ),
        "D": (
            "強化學習讓代理人與環境互動，依獎勵訊號逐步調整行動策略，適合下棋、"
            "機器人控制、廣告出價這類序列決策問題。評論異常偵測是對既有資料做"
            "判定，沒有可互動的環境，也沒有現成的獎勵函數可回饋，套用強化學習"
            "缺乏成立的前提。"
        ),
    },
    "trap": (
        "第一，用「標註狀況」決定框架：兩類標註齊備用監督式分類，幾乎只有正常"
        "資料就走半監督式（新奇偵測）路線，完全沒有先驗才輪到純非監督探索。"
        "第二，別把「找出常見字詞組合」與「找出偏離正常的行為」混為一談："
        "前者是共現規律，後者才是異常偵測的目標。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
        "待查項目：「以純正常資料訓練的異常偵測」在文獻中有半監督式異常偵測、"
        "新奇偵測（novelty detection）、單類分類等不同稱呼，scikit-learn 文件"
        "歸於 novelty detection；本題依官方答案採半監督式的說法，名詞使用待"
        "複核者確認。查核日期 2026-08-06。"
    ),
    "references": [
        exam_ref(38),
        sk_ref("outlier_detection.html", "新奇偵測以正常資料建模，異常樣本偏離該模型", "Novelty and Outlier Detection"),
        sk_ref(
            "semi_supervised.html",
            "1.14 節：半監督式學習指訓練資料中僅部分樣本有標註，估計器會利用額外的未標註資料改善泛化",
            "1.14. Semi-supervised learning",
        ),
        guide_ref(
            "第三章 3-35～3-38：機器學習分為監督式（以有標記數據學習輸入與輸出的映射）、"
            "非監督式（不依賴標記，分析資料內在結構做聚類與降維）與強化學習"
            "（代理與環境互動、依獎勵回饋更新策略）"
        ),
    ],
}

DRAFTS[39] = {
    "summary": "正確答案是 C。CRF 直接對標籤序列給定輸入的條件機率 P(y|x) 建模，屬於鑑別式模型。",
    "concept": (
        "生成式與鑑別式模型的分界在於建模對象。生成式模型學習輸入與輸出的聯合"
        "分佈 P(x,y)（或資料本身的分佈），可以由分佈生成新樣本，序列標註中的"
        "代表是隱馬可夫模型（HMM）；鑑別式模型則直接學習給定輸入下輸出的條件"
        "分佈 P(y|x)，把全部力氣放在「怎麼判對」，不花成本描述輸入資料如何"
        "生成。\n"
        "Sutton 與 McCallum 的 CRF 導論說明：CRF 就是直接對條件分佈 p(y|x) "
        "建模的方法，是 HMM 的鑑別式對應版本，兩者的關係如同 naive Bayes"
        "（生成式）之於 logistic regression（鑑別式）；由於不必對輸入建模，"
        "CRF 能自由使用大量重疊的輸入特徵（如大小寫、詞綴、前後文），並在 "
        "NER、詞性標註等序列標註任務中同時考慮相鄰標籤的相依性。"
    ),
    "answerReason": (
        "題幹點名 NER 這種要為整句每個詞指派標籤、並考慮詞與詞關聯的序列標註"
        "任務，並指定以 CRF 作為模型。CRF 的定義就是直接對「給定整句輸入時，"
        "整條標籤序列的條件機率」建模，訓練與推論都圍繞 P(y|x) 進行，"
        "不建模輸入句子本身的生成過程，因此在模型類型上屬於鑑別式模型，選 C。"
    ),
    "optionAnalysis": {
        "A": (
            "生成式模型學的是聯合分佈 P(x,y)，能夠描述資料如何生成，序列標註中"
            "的代表是 HMM：先假設標籤序列生成，再由標籤生成觀測詞。CRF 恰好是"
            "把這個方向反過來的設計——只對 P(y|x) 建模、不描述 x 的生成，"
            "把 CRF 歸為生成式，正好選到它刻意避開的那一類。"
        ),
        "B": (
            "無監督模型指不使用標註資料、從資料自身結構學習的方法，如分群與"
            "降維。CRF 的訓練恰恰需要逐詞標好標籤的語料（如人名、地名、組織的 "
            "BIO 標記），是典型的監督式訓練；NER 資料集的標籤就是它的學習目標，"
            "說它無監督與其訓練方式相反。"
        ),
        "C": (
            "正確。CRF 直接對條件分佈 P(y|x) 建模，屬於鑑別式模型；它以特徵"
            "函數同時看整句輸入與相鄰標籤，推論時找出整條序列的最佳標籤組合，"
            "既保留鑑別式可用豐富特徵的優點，又能處理標籤之間的相依性，"
            "正適合 NER 這類序列標註任務。"
        ),
        "D": (
            "自迴歸模型把序列機率拆成「逐步以前文預測下一個元素」，如 GPT 這類"
            "語言模型逐 token 生成。CRF 不是逐步生成輸出，而是對整條標籤序列做"
            "全域正規化，一次性求條件機率最大的序列；兩者處理序列的方式不同，"
            "自迴歸也不是 CRF 的分類歸屬。"
        ),
    },
    "trap": (
        "第一，分類看「建模對象」：學 P(x,y) 或能生成資料的是生成式，直接學 "
        "P(y|x) 的是鑑別式；CRF、logistic regression 屬後者，HMM、naive "
        "Bayes 屬前者。第二，別把「處理序列」與「自迴歸」畫上等號：CRF 靠標籤"
        "間的相依結構與全域正規化處理序列，不是逐步生成。"
    ),
    "references": [
        exam_ref(39),
        {
            "title": "Sutton & McCallum, An Introduction to Conditional Random Fields（arXiv:1011.4088）",
            "url": "https://ar5iv.labs.arxiv.org/html/1011.4088",
            "locator": "第 2.3 節：CRF 直接對條件分佈 p(y|x) 建模，是 HMM 的鑑別式對應，關係如同 naive Bayes 之於 logistic regression；第 5 節列出 NER、詞性標註等序列標註應用",
            "checkedAt": TODAY_CHECKED_AT,
        },
        guide_ref("第三章 3-48：生成式 AI 學習資料的聯合分佈或邊際分佈並生成新樣本，典型模型包括 GAN、VAE 與擴散模型"),
    ],
}

DRAFTS[40] = {
    "summary": "正確答案是 C。GAN 以生成器與鑑別器對抗學習資料分佈，能創作訓練集中未曾出現的新旋律，而非重播或重建既有內容。",
    "concept": (
        "題幹的三個要求把答案範圍限定得很清楚：要能「生成全新旋律」（必須是"
        "生成式模型）、不能「拼接既有片段」（排除靠既有樣本作答的實例式方法）、"
        "也不能「僅進行資料的重建」（排除以重建輸入為目標的模型）。\n"
        "生成對抗網路（GAN）由兩個網路對抗訓練：生成模型 G 捕捉資料分佈、"
        "負責產生樣本，鑑別模型 D 估計樣本來自真實訓練資料的機率，G 的訓練"
        "目標是讓 D 分不出真假。訓練收斂後，G 學到的是音樂資料的整體分佈，"
        "可以從隨機雜訊取樣，生成訓練集中不存在、卻符合學到的結構與風格的"
        "新樣本。官方學習指引也把 GAN 與 VAE、擴散模型並列為學習資料分佈並"
        "生成新樣本的生成式模型代表。"
    ),
    "answerReason": (
        "技術長的要求是真正學習音樂的結構與風格、創作從未出現過的新旋律。"
        "四個選項中，KNN 與隨機森林是判別與預測用途，無法生成內容；自編碼器的"
        "訓練目標是把輸入壓縮後重建回原樣，對應題幹明文排除的「僅進行資料的"
        "重建」；只有 GAN 以對抗訓練學習資料分佈，從分佈中取樣產生全新樣本，"
        "同時滿足「學結構風格」與「生成新旋律」兩個要求，因此選 C。"
    ),
    "optionAnalysis": {
        "A": (
            "K-近鄰演算法是基於實例的方法：預測時找出訓練集中最相近的 K 筆"
            "樣本，以多數決或平均作答，本身不學習資料分佈，也不產生新內容。"
            "硬要拿它「生成」音樂，結果只能是檢索並重複既有歌曲片段，正好落入"
            "題幹禁止的「播放或拼接既有歌曲」情況。"
        ),
        "B": (
            "自編碼器由編碼器把輸入壓縮成低維表示、解碼器再重建回原輸入，訓練"
            "目標是重建誤差最小，常用於降維、去噪與異常偵測。題幹明文排除"
            "「僅進行資料的重建」，而標準自編碼器缺乏可供取樣的分佈假設，"
            "難以直接生成新旋律；要具備生成能力需改造成 VAE 等變形，"
            "那已不是本選項所稱的自編碼器。"
        ),
        "C": (
            "正確。GAN 的生成器從隨機雜訊產生樣本，鑑別器判斷樣本是真是假，"
            "兩者對抗迭代後，生成器學到訓練資料的分佈，能生成符合音樂結構與"
            "風格、卻未曾在訓練集中出現的新旋律；調整取樣位置還能帶出風格"
            "變化，符合平台提供多樣靈感素材的需求。"
        ),
        "D": (
            "隨機森林是多棵決策樹的集成，以投票或平均輸出類別或數值，強項是"
            "結構化資料的分類與迴歸，例如判斷一首歌屬於哪種曲風。它的輸出是"
            "標籤或分數，不是可播放的旋律序列，也不建模資料分佈，無從生成新的"
            "音樂內容。"
        ),
    },
    "trap": (
        "第一，先分「判別」與「生成」：KNN、隨機森林輸出類別或數值，生成新內容"
        "要找 GAN、VAE、擴散模型這一族。第二，再用題幹的排除條件收斂答案："
        "「不能只重建」踢掉自編碼器，「不能拼接既有片段」踢掉實例式方法，"
        "剩下的生成式模型才是答案。"
    ),
    "references": [
        exam_ref(40),
        {
            "title": "Goodfellow et al., Generative Adversarial Networks（arXiv:1406.2661）",
            "url": "https://arxiv.org/abs/1406.2661",
            "locator": "摘要：生成模型 G 捕捉資料分佈，鑑別模型 D 估計樣本來自訓練資料的機率；G 的訓練目標是最大化 D 犯錯的機率，兩者構成極小極大雙人賽局",
            "checkedAt": TODAY_CHECKED_AT,
        },
        guide_ref("第三章 3-48：生成式 AI 學習資料的聯合分佈或邊際分佈並生成新樣本，典型模型包括 GAN、VAE 與擴散模型"),
        guide_ref("第三章 3-23：檢核題第 8 題解析指出決策樹、線性迴歸和貝氏分類雖是重要的機器學習方法，但並不擅長生成新的內容"),
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
