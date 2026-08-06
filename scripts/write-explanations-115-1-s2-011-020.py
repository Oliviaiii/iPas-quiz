"""Write the phase-two explanation drafts for 115-1 elementary subject two, Q11-Q20.

Same guarantees as the earlier batches: the script only fills ``explanation`` on
questions that already exist, aborts if an official answer no longer matches the
answer a draft was written against, and refuses to overwrite anything already
marked reviewed.

Every cited URL was opened and checked on the date recorded in ``checkedAt``:
the exam PDF was retrieved and verified page by page on 2026-07-29 (see
sources.json), study-guide locators and other reused references were opened on
2026-07-31 while drafting earlier batches and are carried over verbatim, and the
remaining references were opened and verified on 2026-08-03 while drafting this
batch.

Usage::

    python scripts/write-explanations-115-1-s2-011-020.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-elementary-1-genai-planning"
AUTHOR = "Claude Code（AI 輔助初稿）"
AUTHORED_AT = "2026-08-03"
EXAM_CHECKED_AT = "2026-07-29"
REUSED_CHECKED_AT = "2026-07-31"
TODAY_CHECKED_AT = "2026-08-03"

EXAM_PDF = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/115年第一次初級AI應用規劃師_第二科_"
    "生成式AI應用與規劃_公告試題_20260410164328.pdf"
)
GUIDE_PDF = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/AI應用規劃師(初級)-學習指引-科目2_"
    "生成式AI應用與規劃114123_20251222172159.pdf"
)
DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def exam_ref(number: int) -> dict:
    return {
        "title": "115 年第一次初級 AI 應用規劃師－生成式 AI 應用與規劃公告試題",
        "url": EXAM_PDF,
        "locator": f"第 {number} 題題幹、選項與官方答案",
        "checkedAt": EXAM_CHECKED_AT,
    }


def guide_ref(locator: str) -> dict:
    return {
        "title": "iPAS AI 應用規劃師（初級）學習指引－科目二 生成式 AI 應用與規劃",
        "url": GUIDE_PDF,
        "locator": locator,
        "checkedAt": REUSED_CHECKED_AT,
    }


def ref(title: str, url: str, locator: str, checked_at: str) -> dict:
    return {
        "title": title,
        "url": url,
        "locator": locator,
        "checkedAt": checked_at,
    }


EXPECTED_ANSWER = {
    11: "B", 12: "B", 13: "B", 14: "A", 15: "D",
    16: "D", 17: "B", 18: "A", 19: "C", 20: "C",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[11] = {
    "summary": "正確答案是 B。No-Code 平台的功能定位是讓非技術人員以視覺化方式組裝分析畫面，AutoML 的定位是自動化模型訓練，兩者分工正好承接題目的兩項需求。",
    "concept": (
        "這題考的是兩類工具的主要功能定位。No-Code 平台透過視覺化介面與拖放"
        "操作，讓使用者無需編寫程式碼就能組裝應用畫面與操作流程；官方學習指引"
        "並指出它降低技術門檻，使非技術人員也能參與開發。門市主管要自行調整"
        "分析畫面、檢視指標呈現，需要的正是這種人人可上手的介面組裝能力。\n"
        "AutoML（Automated Machine Learning）則把建模流程中的演算法挑選、"
        "特徵處理與超參數搜尋自動化：使用者備妥資料並指定預測目標，平台就能"
        "自動訓練並比較多個候選模型。行銷部門要建立銷售預測模型卻未必有"
        "資料科學團隊，AutoML 正是為此設計。題目明說以「主要功能定位與典型"
        "用途」作為評估依據，選型時就應讓兩類工具各守本業。"
    ),
    "answerReason": (
        "把兩項需求各自配對到定位相符的工具：門市主管的分析畫面與指標呈現"
        "調整，交給以視覺化介面見長的 No-Code 平台；行銷部門的銷售預測模型，"
        "交給把訓練流程自動化的 AutoML。B 的分工讓每項需求都由該類工具的核心"
        "能力承接，是唯一與兩者定位一致的規劃。"
    ),
    "optionAnalysis": {
        "A": (
            "把兩類工具的角色對調了。AutoML 的操作介面是用來設定資料來源、"
            "預測目標與訓練流程，不是給門市主管日常拖曳調整報表畫面的儀表板"
            "工具；反過來要 No-Code 平台負責模型訓練，又超出它以介面與流程"
            "組裝為主的典型用途，兩項需求都會被放錯位置。"
        ),
        "B": (
            "正確。門市主管透過 No-Code 平台的視覺化介面自行調整分析畫面與"
            "指標呈現，不必排隊等資訊部門支援；行銷部門把整理好的銷售資料交給"
            "AutoML 自動完成演算法挑選與調參，不需深厚的演算法背景也能產出"
            "預測模型，兩邊需求各得其所。"
        ),
        "C": (
            "只導入 No-Code 平台會缺一角。這類平台的強項是畫面與流程組裝，"
            "部分產品雖內建簡單的分析元件，但銷售預測這種需要演算法比較與"
            "超參數搜尋的高階模型建立，並不是它的主要功能定位；題目又要求依"
            "定位選型，硬要單一平台包辦，等於把建模需求交給不擅長的工具。"
        ),
        "D": (
            "只導入 AutoML 同樣缺一角。AutoML 專注於把模型開發流程自動化，"
            "並不提供讓業務主管自由組裝儀表板、切換檢視指標的介面設計能力；"
            "門市端的分析畫面調整需求會落空，主管仍得回頭仰賴技術人員支援，"
            "與題目希望門市自助的目標不符。"
        ),
    },
    "trap": (
        "第一，記住兩個定位關鍵字：No-Code 是「不寫程式組裝介面與流程」，"
        "AutoML 是「自動化模型訓練」，題目把需求寫成兩句，就分別配對。"
        "第二，出現「僅導入單一工具」的選項時，先檢查另一半需求是否被犧牲。"
    ),
    "references": [
        exam_ref(11),
        guide_ref("第三章 3-1：No Code 平台透過視覺化介面和拖放操作，讓使用者無需編寫程式碼即可快速開發"),
        guide_ref("第三章 3-9：No Code 平台降低了技術門檻，使非技術人員也能參與應用開發，促進跨部門協作"),
        ref(
            "Microsoft Learn－What is automated ML? AutoML（Azure Machine Learning）",
            "https://learn.microsoft.com/en-us/azure/machine-learning/concept-automated-ml",
            "What is automated ML?：AutoML 自動化模型開發中耗時且重複的步驟，讓不具資料科學專長者也能建立端到端機器學習流程",
            REUSED_CHECKED_AT,
        ),
    ],
}

DRAFTS[12] = {
    "summary": "正確答案是 B。MCP 是讓模型與外部工具、系統互動的標準化協定，RAG 則是檢索外部文件來補充模型的知識來源，一個補動作、一個補知識。",
    "concept": (
        "兩者都在替大型語言模型補上外部能力，但方向不同。Model Context "
        "Protocol（MCP）是一套主從式的開放協定，定義 AI 應用（Host）、連線"
        "元件（Client）與能力提供方（Server）之間的溝通方式；Server 對外提供"
        "工具（可執行的函式，如查資料庫、呼叫 API）、資源與提示範本，讓模型能"
        "以同一套介面接上各種外部系統並執行動作。\n"
        "檢索增強生成（Retrieval-Augmented Generation, RAG）走另一條路：把"
        "外部文件切塊、向量化建立索引，回答前先檢索出相關片段放進提示，讓模型"
        "依據取回的內容作答。它擴充的是模型讀得到的知識，重點在檢索品質與內容"
        "時效。判斷這類題目，抓住「MCP 補的是能做什麼動作、RAG 補的是知道什麼"
        "內容」即可。"
    ),
    "answerReason": (
        "B 用一句話分別說中兩者的定位：MCP 著重模型與外部工具或系統的互動，"
        "這是協定層的整合能力；RAG 著重補充模型的知識來源，這是內容層的檢索"
        "增強。兩個描述都與官方規格及原始論文的定義一致，也沒有把任一方的特性"
        "安到對方頭上，因此是正確答案。"
    ),
    "optionAnalysis": {
        "A": (
            "MCP 作用在推論階段，讓已訓練完成的模型連上外部系統，並不介入模型"
            "訓練，談不上降低訓練成本；RAG 在生成前多了一道檢索流程，通常反而"
            "增加回應延遲，它的目的是讓答案有依據，而不是提升推論速度。這個"
            "選項替兩者安排的目標都與實際設計不符。"
        ),
        "B": (
            "正確。MCP 以標準化協定串接模型與外部工具、資料來源，解決的是"
            "「模型如何呼叫外部系統執行動作」；RAG 以檢索補充模型參數以外的"
            "知識，解決的是「模型依據什麼內容回答」。兩者路線不同而互補，"
            "也常在同一個系統中並用。"
        ),
        "C": (
            "前半句過強、後半句說反。RAG 常搭配向量資料庫做語意檢索，但這不是"
            "必要條件，關鍵字檢索、BM25 或混合檢索同樣能實作 RAG；MCP 的存在"
            "目的正是標準化模型與外部系統的整合，說它「不需任何外部整合」，"
            "與這個協定的定義恰好相反。"
        ),
        "D": (
            "把兩者的身分整組對調。RAG 是把檢索與生成串接起來的技術作法，"
            "並沒有一份統一的通訊協議規格；MCP 才是以規格文件定義訊息格式與"
            "角色分工的標準化協定，而且它處理的是工具與系統整合，不是資料檢索"
            "技術，主詞與屬性都配錯了。"
        ),
    },
    "trap": (
        "第一，用「補知識還是補動作」區分：RAG 讓模型讀到更多內容，MCP 讓模型"
        "接上更多系統。第二，選項若把「標準化協議」、「向量資料庫」這類關鍵詞"
        "掛到另一方頭上，通常就是刻意調換主詞的陷阱。"
    ),
    "references": [
        exam_ref(12),
        ref(
            "Model Context Protocol－Architecture overview",
            "https://modelcontextprotocol.io/docs/learn/architecture",
            "MCP 採主從式架構，Server 對外提供 Tools（可執行動作，如 API 呼叫、資料庫查詢）、Resources 與 Prompts 三類基本能力",
            REUSED_CHECKED_AT,
        ),
        ref(
            "arXiv－Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
            "https://arxiv.org/abs/2005.11401",
            "以外部非參數化記憶補充模型參數知識，使知識可更新且生成結果有出處可追溯",
            REUSED_CHECKED_AT,
        ),
    ],
}

DRAFTS[13] = {
    "summary": "正確答案是 B。把長文件切成主題集中的片段後，向量比對更能對準問題語意，檢索也不再夾帶整份文件的無關內容。",
    "concept": (
        "在檢索增強生成（RAG）流程中，文件會先被切塊（Chunking），逐塊轉成"
        "向量建立索引，查詢時依語意相似度取回最相關的片段。切分粒度直接決定"
        "檢索品質：整份長文件當一個單位時，一個向量要代表數十個主題的平均"
        "語意，與提問的相似度被稀釋，取回的內容自然夾帶大量無關段落。\n"
        "切塊後每個片段聚焦單一主題，相似度計算更銳利，引用也能精準落在相關"
        "段落上。另一個好處在生成端：研究顯示語言模型在長上下文中，對位於中段"
        "的關鍵資訊利用效果明顯下降，把無關內容擋在提示之外，本身就是在保護"
        "回答品質。題幹描述的「回覆常包含無關內容、引用段落不夠精準」，"
        "正是切分粒度過大的典型症狀。"
    ),
    "answerReason": (
        "題目已把症狀寫明：以整份文件檢索時，回覆混入無關內容、引用不精準，"
        "這是檢索對齊與上下文純度的問題。Chunking 把長文件拆成語意集中的"
        "片段，讓向量檢索能對準提問、取回真正相關的段落，同時避免整份文件的"
        "雜訊擠進提示干擾生成，B 同時說中這兩層效果，正是導入的主要目的。"
    ),
    "optionAnalysis": {
        "A": (
            "縮短輸入確實可能讓單次推理快一點，但那是切塊的附帶效果。團隊觀察"
            "到的問題是回覆含無關內容、引用不精準，屬於檢索品質而非速度；"
            "若目標真是加速推理，優先手段會是模型量化、快取或改用較小的模型，"
            "而不是重整文件的切分方式。"
        ),
        "B": (
            "正確。片段主題單一之後，向量更能代表該段語意，與問題的相似度比對"
            "更準確，檢索結果的語意對齊程度隨之提升；同時只有相關片段進入"
            "提示，長文件夾帶的無關內容被擋在外面，生成端受到的干擾也跟著"
            "下降，題幹的兩個症狀一次處理。"
        ),
        "C": (
            "記憶體用量與系統穩定性屬於部署資源層面的議題，通常靠模型壓縮、"
            "調整批次大小或擴充硬體處理。切塊反而會讓索引筆數增加、整體儲存量"
            "上升，把 Chunking 當成節省記憶體、提升穩定性的手段，方向並不"
            "成立。"
        ),
        "D": (
            "生成內容的創意空間由取樣策略控制，例如溫度參數調高會讓輸出更"
            "發散，那是生成端的設定。知識查詢系統要求的是引用精準、有憑有據，"
            "與「更高創意」的方向相反；切塊處理的是檢索端的材料品質，"
            "與創意發揮無關。"
        ),
    },
    "trap": (
        "第一，分清作用階段：Chunking 屬於檢索前的資料處理，溫度與取樣屬於"
        "生成階段，壓縮與量化屬於部署層，三者解決的問題不同。第二，題幹把痛點"
        "寫成「無關內容、引用不精準」時，要挑直接改善檢索品質的選項，"
        "而不是速度或資源的附帶效益。"
    ),
    "references": [
        exam_ref(13),
        ref(
            "arXiv－Lost in the Middle: How Language Models Use Long Contexts",
            "https://arxiv.org/abs/2307.03172",
            "關鍵資訊位於長上下文中段時，模型表現顯著下降，顯示長上下文噪音會影響回答品質",
            REUSED_CHECKED_AT,
        ),
        guide_ref("第三章 3-18：標記化處理將文本拆分為基本單元、向量化表示將文本轉換為數值形式以適應深度學習模型"),
    ],
}

DRAFTS[14] = {
    "summary": "正確答案是 A。把表格轉成 JSON 或 Markdown table，欄位與數值的對應關係被明確標示，模型解析不再依賴容易錯亂的視覺對齊。",
    "concept": (
        "上下文工程（Context Engineering）處理的是「餵給模型的內容要用什麼"
        "形式呈現」。Excel 表格直接貼進提示時，欄列結構常在轉換中流失：欄位以"
        "不定數量的空白或換行分隔、跨欄儲存格錯位，模型只能靠猜測還原行列"
        "對應，解析自然不穩定。\n"
        "結構化格式解決的正是這個歧義：JSON 把每個值掛在明確的欄位名稱下，"
        "Markdown table 以分隔符號清楚界定欄與列，模型讀到的是「欄名對值」的"
        "明確配對，不必再猜哪個數字屬於哪一欄。針對表格理解的實證研究顯示，"
        "大型語言模型在結構化表格任務上的表現，會隨表格輸入格式、內容順序等"
        "輸入設計顯著變動，格式選擇本身就是影響理解品質的關鍵變因。"
    ),
    "answerReason": (
        "題幹的痛點是「模型對原始表格解析效果不穩定」，也就是輸入格式造成的"
        "理解歧義。四個選項中只有 A 動手改變資料的呈現結構：轉成 JSON 或 "
        "Markdown table 之後，欄位名稱與數值的對應寫得明明白白，行列邊界不再"
        "依賴排版，正面消除了解析不穩的根源，因此是最適當的上下文工程作法。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。結構化轉換把表格的隱含結構顯性化：JSON 以鍵值配對標明每個"
            "數值屬於哪個欄位，Markdown table 以豎線與分隔列標出行列邊界。"
            "模型不必再從錯亂的空白與換行中猜測結構，解析穩定度與後續統計、"
            "比較的正確率都會提升。"
        ),
        "B": (
            "補充欄位與數據說明是有價值的輔助手段，能幫模型理解欄位的業務"
            "意義，實務上常與格式轉換並用。但題幹指出問題出在「原始表格的"
            "解析」本身：維持原有呈現方式，欄列錯位與分隔歧義依然存在，"
            "再多的文字說明也無法替模型還原哪個數字屬於哪一欄。"
        ),
        "C": (
            "分段輸入是處理超長內容的常見手段，但關鍵在「隨機切割」：表格的"
            "同一列資料彼此關聯，隨機切割會把同一筆紀錄拆進不同段落，欄位標題"
            "與數值分家，行列對應徹底毀壞，解析只會比原始表格更不穩定，"
            "與改善目標背道而馳。"
        ),
        "D": (
            "保留原貌不等於保留資訊可用性。題幹已經實測出原始表格解析不穩，"
            "繼續原樣輸入等於放棄改善；「完整資訊」應該靠無損的結構化轉換保留"
            "下來，JSON 與 Markdown table 都能承載原表的全部欄位與數值，"
            "並非只有原始排版才算完整。"
        ),
    },
    "trap": (
        "第一，區分「格式問題」與「語意問題」：解析不穩定要靠結構化格式解決，"
        "欄位含義不清才靠補充說明。第二，看到「保留完整資訊」這類說法，"
        "先想想原始格式是否真的能被模型正確讀取，讀不懂的完整等於不完整。"
    ),
    "references": [
        exam_ref(14),
        ref(
            "arXiv－Table Meets LLM: Can Large Language Models Understand Structured Table Data?",
            "https://arxiv.org/abs/2305.13062",
            "摘要：GPT-3.5 與 GPT-4 在結構化表格任務的表現，隨表格輸入格式、內容順序、角色提示與分隔標記等輸入設計而顯著變動",
            TODAY_CHECKED_AT,
        ),
        guide_ref("第三章 3-18：生成式 AI 具備上下文理解能力，並可透過提示詞進行可控生成"),
    ],
}

DRAFTS[15] = {
    "summary": "正確答案是 D。情境感知代理的核心是維護對話歷史與任務狀態，並在後續決策時據以調整行為，而不是只看當下這一句指令。",
    "concept": (
        "情境感知代理（Context-aware Agent）與單純的指令執行器，差別在於"
        "有沒有「狀態」。無狀態的作法是每次只看當前輸入，回答完就忘；情境感知"
        "代理則持續維護對話歷史、任務進度與環境回饋，決策時把這些脈絡納入"
        "考量：使用者先前提過的偏好會被沿用，已完成的子任務不會重做，"
        "上一步工具呼叫失敗會改變下一步的選擇。\n"
        "代理研究中的經典作法即是如此：Generative Agents 論文讓代理以自然語言"
        "儲存完整的經驗紀錄，隨時間把記憶綜合成更高層的反思，並在規劃行為時"
        "動態檢索取用，代理因此能表現出前後連貫、隨情境調整的行為。這正是"
        "「情境感知」一詞的技術內涵。"
    ),
    "answerReason": (
        "題目問核心特性，要挑最能把「情境感知」與一般代理區隔開來的敘述。"
        "D 指出代理能利用對話歷史與任務狀態調整行為與決策，點中了狀態維護與"
        "脈絡運用這個定義核心；其餘選項不是描述相反的無狀態行為，就是把訓練"
        "機制或多模態能力誤當成情境感知，因此選 D。"
    ),
    "optionAnalysis": {
        "A": (
            "即時重新訓練模型參數屬於線上學習或持續學習的範疇，成本高且有"
            "災難性遺忘風險；實務上代理多在推論階段運作，模型權重固定不動，"
            "情境資訊是放進上下文視窗或外部記憶供檢索，不是寫回權重。把情境"
            "感知說成即時改參數，混淆了推論與訓練兩個階段。"
        ),
        "B": (
            "只依當前輸入執行、不保留歷程，描述的是無狀態的單輪執行器，例如"
            "一問一答的簡單查詢介面。這種型態正是情境感知代理要克服的限制："
            "沒有歷程就無法沿用先前脈絡、無法追蹤任務進度，敘述與題目要問的"
            "特性恰好相反。"
        ),
        "C": (
            "跨模態處理指的是同時理解文字、影像等多種輸入型態，屬於模型輸入"
            "能力的擴充，與是否利用歷史脈絡是兩個獨立面向：純文字代理可以充分"
            "情境感知，具備多模態能力的系統也可能完全無狀態。把輸入模態的廣度"
            "當成情境感知的核心，答錯了維度。"
        ),
        "D": (
            "正確。維護對話歷史與任務狀態，並在決策時據以調整行為，正是情境"
            "感知的定義性特徵：先前的偏好與結論被沿用、任務進行到哪一步有跡"
            "可循、環境回饋會改變後續選擇，代理的行為因此能隨情境演變而連貫地"
            "調整。"
        ),
    },
    "trap": (
        "第一，用「有沒有維護狀態」判斷情境感知，別被重新訓練、跨模態這些"
        "聽起來更進階的能力吸走注意力，它們屬於不同維度。第二，看到「僅依當前"
        "輸入」、「不保留歷程」這類敘述，在情境感知題型中就是定義的反面。"
    ),
    "references": [
        exam_ref(15),
        ref(
            "arXiv－Generative Agents: Interactive Simulacra of Human Behavior",
            "https://arxiv.org/abs/2304.03442",
            "摘要：代理以自然語言儲存完整經驗紀錄，隨時間將記憶綜合為更高層的反思，並動態檢索取用以規劃行為",
            TODAY_CHECKED_AT,
        ),
        guide_ref("第三章 3-18：生成式 AI 具備上下文理解能力，並可透過提示詞進行可控生成"),
    ],
}

DRAFTS[16] = {
    "summary": "正確答案是 D。Solution Graph 的功能是把任務分解與可行的決策路徑組織成圖狀結構，供代理在執行時參考，而不是取代或鎖死代理的推理。",
    "concept": (
        "處理跨部門複雜任務時，Agentic AI 需要一個結構來回答「任務可以拆成"
        "哪些步驟、步驟之間如何銜接、走不通時還有哪些路」。解決方案圖譜"
        "（Solution Graph）扮演的正是這個角色：節點代表子任務或中間狀態，"
        "邊代表步驟間的先後與依賴關係，代理執行時據以判斷下一步該做什麼、"
        "目前推進到哪個環節。\n"
        "要注意它的定位是「可參考的結構」：實際的語意理解、工具結果判讀與"
        "臨場決策仍由語言模型負責，圖譜提供的是組織骨架，讓代理的探索有跡"
        "可循。這與思維樹（Tree of Thoughts）一類研究的精神一致——把推理展開"
        "成可分支的節點結構，供模型評估、選擇與回溯，結構輔助推理而非取代"
        "推理。"
    ),
    "answerReason": (
        "題目問 Solution Graph 的主要功能。D 說它定義代理可參考的任務分解與"
        "決策路徑結構，同時保住兩個關鍵：一是它提供圖狀的組織結構（任務怎麼"
        "拆、路徑怎麼走），二是它的角色是「可參考」的框架，代理仍保有依情境"
        "選擇與回溯的空間。其餘選項不是把它誇大成取代模型，就是把它矮化成"
        "案例倉庫或鎖死成固定流程，因此選 D。"
    ),
    "optionAnalysis": {
        "A": (
            "圖形搜尋演算法擅長路徑展開、代價比較與回溯，但它無法理解自然語言"
            "需求、判讀工具回傳的內容，也處理不了圖上沒有預先定義的情況。"
            "Agentic 系統的分工是模型負責語意判斷、結構負責組織路徑，Solution "
            "Graph 屬於後者，說它取代語言模型推理，是把輔助角色誇大成了"
            "替代品。"
        ),
        "B": (
            "儲存已完成案例供日後檢索的，是案例庫或經驗記憶這類機制，常搭配"
            "檢索增強使用，價值在事後重用過往成果。Solution Graph 則是在任務"
            "執行當下被參照的結構，內容是任務分解與路徑選項而非歷史成品，"
            "兩者作用的時間點與存放的內容都不一樣。"
        ),
        "C": (
            "把代理限制在固定流程內，描述的是硬性的流程編排或護欄設計，好處是"
            "行為可預測，代價是放棄依中間結果調整的彈性。Solution Graph 的"
            "定位是「可參考」的路徑結構：代理可以在分支之間選擇、必要時回溯"
            "換路，圖譜引導探索而不是禁止偏離，方向與這個選項相反。"
        ),
        "D": (
            "正確。圖譜以節點與邊把任務分解結果與可行的決策路徑組織起來，"
            "代理執行時據以掌握全局、選擇下一步，走不通時還能沿結構回溯改道；"
            "組織與引導由圖譜負責，臨場的語意判斷仍由模型完成，這正是它作為"
            "規劃框架的主要功能。"
        ),
    },
    "trap": (
        "第一，分清三種角色：參考框架（引導但可調整）、固定流程（鎖死不可"
        "偏離）、案例知識庫（事後重用），Solution Graph 屬於第一種。第二，"
        "選項出現「取代模型推理」或「僅能依固定流程」這類極端定位時，"
        "在代理規劃題中通常都是要排除的敘述。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
        "待查項目：Solution Graph（解決方案圖譜）並非業界有統一定義的標準"
        "術語，官方學習指引科目二亦未收錄，本題解析依題幹用語與圖狀推理框架"
        "（如 Tree of Thoughts）的一般用法推得，建議複核者查證命題是否另有"
        "指定出處。查核日期 2026-08-03。"
    ),
    "references": [
        exam_ref(16),
        ref(
            "arXiv－Tree of Thoughts: Deliberate Problem Solving with Large Language Models",
            "https://arxiv.org/abs/2305.10601",
            "ToT 原始論文：以想法為節點探索多條推理路徑，並自我評估、前瞻與回溯，適用需要規劃或搜尋的問題",
            REUSED_CHECKED_AT,
        ),
    ],
}

DRAFTS[17] = {
    "summary": "正確答案是 B。多個服務實例搭配負載分散，單一實例故障時其餘實例接手、流量上升時可增加實例，同時滿足高可用與可擴展。",
    "concept": (
        "高可用性（High Availability）的核心是消除單點故障：任何一個元件"
        "失效，服務整體仍能繼續運作；可擴展性（Scalability）則要求容量能隨"
        "流量增減。雲端架構的標準作法是水平擴展——AWS Well-Architected "
        "可靠性支柱把它列為設計原則：以多個小型資源取代單一大型資源，"
        "降低單一故障對整體工作負載的影響，並把請求分散到多個資源上，"
        "避免共用同一個故障點。\n"
        "落到 LLM API 服務，就是部署多個模型服務實例，前面放負載平衡器把請求"
        "分配出去：某個實例故障，健康檢查會把它移出流量池，其餘實例繼續承接；"
        "尖峰流量來時，自動擴展機制增加實例數量消化負載。這套組合正是"
        "「不中斷、耐故障、可伸縮」的標準解法。"
    ),
    "answerReason": (
        "題幹列出的要求——高併發、流量波動、服務不中斷、故障容忍——每一項都"
        "指向水平擴展架構：多實例讓單一故障不再是全局故障，負載分散讓高併發"
        "請求被攤平到各實例，實例數量又能隨流量波動增減。B 是唯一同時回應"
        "全部四項要求的部署方式，因此正確。"
    ),
    "optionAnalysis": {
        "A": (
            "單一高效能 VM 是垂直擴展思路，把資源集中在一台機器上，管理簡單、"
            "資源使用率也可能不錯，適合流量穩定的小型內部服務。但整個服務繫於"
            "一台機器，VM 故障、重開或維護時服務就全面中斷，正是高可用設計要"
            "消除的單點故障；容量上限也被單機規格鎖死，難以因應流量波動。"
        ),
        "B": (
            "正確。多個模型服務實例分散部署，負載分散機制把請求分配到健康的"
            "實例上：單一實例故障時被移出流量池、其餘實例繼續承接，服務不"
            "中斷；流量上升時增加實例、回落時縮減，高併發與波動都有對策，"
            "完整落實水平擴展的可靠性原則。"
        ),
        "C": (
            "把推論移到用戶端裝置，適合離線使用、隱私敏感或模型極小的場景，"
            "例如手機上的輸入預測。但大型語言模型的參數量與算力需求遠超一般"
            "用戶裝置的負荷，模型版本分發、更新與回應品質也難以統一管理；"
            "企業要對外提供穩定的 API 服務，服務品質不能繫於每個客戶端的"
            "硬體。"
        ),
        "D": (
            "FTP 是檔案傳輸協定，設計目的為批次上傳下載檔案，沒有低延遲請求"
            "回應互動的概念，也缺乏現代 API 常用的加密與串流能力；LLM API "
            "一般以 HTTPS 或 gRPC 提供服務。更關鍵的是，更換傳輸協定完全不會"
            "帶來故障容忍或擴展能力，與題目指定的設計原則無關。"
        ),
    },
    "trap": (
        "第一，看到「不中斷、故障容忍」就先找「有沒有備援」：任何單一機器"
        "方案都過不了單點故障這一關。第二，別被「減少負擔」的字眼帶走——"
        "把運算推給用戶端或更換傳輸協定都沒有處理可用性與擴展性，"
        "答題時要對準題目指定的設計原則。"
    ),
    "references": [
        exam_ref(17),
        ref(
            "AWS Well-Architected Framework－Reliability Pillar: Design principles",
            "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/design-principles.html",
            "設計原則 Scale horizontally to increase aggregate workload availability：以多個小型資源取代單一大型資源，降低單一故障對整體工作負載的影響，並將請求分散至多個資源以避免共同故障點",
            TODAY_CHECKED_AT,
        ),
        ref(
            "AWS－Amazon SageMaker AI 開發者指南：Real-time inference",
            "https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints.html",
            "Real-time inference：即時推論適用於具有即時、互動、低延遲需求的工作負載，端點支援自動擴展（autoscaling）",
            REUSED_CHECKED_AT,
        ),
    ],
}

DRAFTS[18] = {
    "summary": "正確答案是 A。這類工具都以大型語言模型為核心，從大量程式碼與文本學到統計規律，逐一預測下一個符號來生成程式碼，因此無法保證輸出必然正確。",
    "concept": (
        "ChatGPT、Claude、GitHub Copilot 背後都是大型語言模型：以海量文本與"
        "程式碼訓練，學習「給定前文，下一個符號（token）最可能是什麼」，"
        "生成程式碼時就是把這個預測一步步接下去。Codex 論文說明了這條技術"
        "路線——它是在 GitHub 公開程式碼上微調的 GPT 語言模型，其產品版本即為"
        " GitHub Copilot 提供技術支援；論文同時揭示了能力邊界，模型在 "
        "HumanEval 基準單次取樣僅解出約三成題目，顯示生成內容並沒有正確性"
        "保證。\n"
        "GitHub 官方的使用建議也印證這一點：Copilot 是可能出錯的工具，"
        "使用者應理解並仔細審查建議的程式碼，並以自動化測試、linting 與程式碼"
        "掃描把關。生成靠機率、驗證靠流程，是理解這類工具的正確框架。"
    ),
    "answerReason": (
        "A 同時說對三件事：技術基礎是大型語言模型、訓練材料是大量程式碼與"
        "文本、生成方式是預測下一個符號；最後補上「不保證正確性」，與原始論文"
        "揭示的解題率及官方文件要求人工審查的立場一致。其餘三項分別替工具"
        "虛構了執行驗證、資料庫檢索與內建編譯器等並不存在的機制，因此選 A。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。這些工具的建議由語言模型依上下文逐符號生成，能產出訓練資料"
            "中不存在的組合，也因此可能寫出語法正確但邏輯錯誤、或引用不存在"
            "函式庫的程式碼；正確性必須由開發者透過審查、測試與掃描工具驗證，"
            "模型本身不提供保證。"
        ),
        "B": (
            "Copilot 的定位是編輯器內的即時補全，建議在使用者輸入的瞬間由模型"
            "生成，並不會先把程式碼放進沙箱執行驗證後才顯示。GitHub 官方最佳"
            "實務反而提醒使用者以自動化測試、linting 與程式碼掃描檢查 Copilot "
            "的產出——若工具已自行執行並保證正確，就不需要這些人工把關的"
            "建議。"
        ),
        "C": (
            "Claude 是生成式大型語言模型，回覆在對話當下由模型即時生成，"
            "可以組合出資料庫裡從未存在的新程式；「從既有解答資料庫檢索回傳」"
            "描述的是檢索式系統（如 FAQ 對照或程式碼搜尋引擎）的運作方式，"
            "這個敘述把生成講成了查表，與其原理不符。"
        ),
        "D": (
            "語言模型輸出文字時並不經過編譯器；部分產品雖提供沙箱執行環境"
            "（例如資料分析情境），那是模型之外的附加設施，而且也只能發現"
            "執行期錯誤。宣稱能「自動編譯並更正所有語法與邏輯錯誤」更不成立"
            "——邏輯錯誤連編譯器都偵測不出來，只能靠測試與人工驗證。"
        ),
    },
    "trap": (
        "第一，抓住「生成靠機率預測、正確性靠外部驗證」這組原理，凡是宣稱"
        "工具會先執行、先驗證、先編譯再給建議的敘述都可先存疑。第二，區分"
        "生成式補全與檢索式查詢：前者即時產生新內容且可能出錯，後者只回傳"
        "既有內容。"
    ),
    "references": [
        exam_ref(18),
        ref(
            "arXiv－Evaluating Large Language Models Trained on Code",
            "https://arxiv.org/abs/2107.03374",
            "摘要：Codex 為在 GitHub 公開程式碼上微調的 GPT 語言模型，其產品版本為 GitHub Copilot 提供技術支援；HumanEval 單次取樣解題率為 28.8%",
            TODAY_CHECKED_AT,
        ),
        ref(
            "GitHub Docs－Best practices for using GitHub Copilot",
            "https://docs.github.com/en/copilot/get-started/best-practices",
            "官方最佳實務：Copilot 可能犯錯，應先理解並仔細審查建議的程式碼（含功能與安全性），並以自動化測試、linting 與 code scanning 驗證其產出",
            TODAY_CHECKED_AT,
        ),
    ],
}

DRAFTS[19] = {
    "summary": "正確答案是 C。AI 生成的程式碼一樣要過品質關：納入程式碼審查、重構與安全測試流程，才能把看不見的錯誤與弱點擋在正式環境之外。",
    "concept": (
        "Vibe Coding 指的是以自然語言描述需求、讓 AI 生成大部分程式碼的開發"
        "方式，此詞由 Andrej Karpathy 於 2025 年提出；它與 MVP 策略同樣以速度"
        "優先，適合快速做出可運作的原型。代價是開發者可能沒有逐行理解生成的"
        "程式碼，未察覺的錯誤與安全弱點會一路帶進系統。\n"
        "因此正式上線前的把關不能省：程式碼審查讓人真正理解並檢視邏輯，"
        "重構清理倉促生成累積的技術債，安全測試搭配掃描工具找出弱點。GitHub "
        "官方最佳實務對 AI 生成程式碼的要求正是如此——理解建議的程式碼、"
        "仔細審查其功能與安全性，並以自動化測試、linting 與程式碼掃描補上"
        "額外的檢查層。速度靠 AI，品質靠流程，兩者缺一不可。"
    ),
    "answerReason": (
        "技術主管點名的風險是「程式碼品質與安全」，對症的措施必須真的檢驗與"
        "改善程式碼本身。審查、重構與安全測試三件事分別處理理解與正確性、"
        "結構品質、安全弱點，是業界對 AI 生成程式碼一致建議的把關流程；"
        "其餘選項不是跳過驗證，就是只在生成前調整提示、或反過來禁止人為"
        "修正，都無法降低已生成程式碼中的實際風險，因此選 C。"
    ),
    "optionAnalysis": {
        "A": (
            "直接沿用生成程式碼上正式環境，等於把未經驗證的程式直接暴露給"
            "真實使用者與攻擊者。AI 生成程式碼的錯誤與弱點並不少見，省下的"
            "審查時間會以線上事故、資安事件與返工加倍償還；MVP 求快指的是縮小"
            "功能範圍，從來不是省略品質驗證。"
        ),
        "B": (
            "優化提示詞確實能讓生成方向更貼近需求、減少明顯偏差，是值得持續做"
            "的前置工作。但提示詞作用在「生成之前」，無法保證輸出正確——模型"
            "仍可能寫出看似合理的錯誤邏輯或不安全寫法，而且問題要等執行或被"
            "攻擊才暴露；品質保證必須靠生成之後的審查與測試補上，提示詞取代"
            "不了驗證。"
        ),
        "C": (
            "正確。審查讓團隊真正理解並檢視 AI 生成的邏輯，錯誤在合併前被"
            "挑出；重構清理快速生成階段累積的重複與混亂結構，讓系統可長期"
            "維護；安全測試與掃描工具針對注入、越權這類弱點把關。三道流程"
            "直接處理題幹點名的品質與安全風險。"
        ),
        "D": (
            "為了維持一致性而限制開發者修改 AI 生成的架構，是把方向弄反了："
            "架構有缺陷或存在安全疑慮時，團隊反而被制度綁住不能修正，技術債與"
            "風險被永久鎖進系統。一致性應該靠編碼規範與審查標準達成，而不是靠"
            "禁止人類修改；最終為系統負責的是團隊，不是生成工具。"
        ),
    },
    "trap": (
        "第一，速度與品質的分工要抓對：AI 與 MVP 負責把東西快速做出來，"
        "審查、重構與測試負責讓它能安全上線，兩段不能互相取代。第二，"
        "凡是主張「跳過驗證」或「不准人工介入」的選項，在軟體品質題型中"
        "幾乎都是要排除的方向。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
        "待查項目：Vibe Coding 為 2025 年才普及的新詞，官方學習指引未收錄；"
        "本題以 GitHub 官方最佳實務佐證審查與測試主張，術語起源暫以維基百科"
        "詞條佐證，建議複核者確認是否有更權威的一手出處可替換。"
        "查核日期 2026-08-03。"
    ),
    "references": [
        exam_ref(19),
        ref(
            "GitHub Docs－Best practices for using GitHub Copilot",
            "https://docs.github.com/en/copilot/get-started/best-practices",
            "官方最佳實務：Copilot 可能犯錯，應先理解並仔細審查建議的程式碼（含功能與安全性），並以自動化測試、linting 與 code scanning 驗證其產出",
            TODAY_CHECKED_AT,
        ),
        ref(
            "Wikipedia－Vibe coding",
            "https://en.wikipedia.org/wiki/Vibe_coding",
            "詞條：Andrej Karpathy 於 2025 年 2 月提出此詞；開發者可能在未理解程式碼的情況下提交 AI 生成內容，帶入未察覺的錯誤與安全弱點",
            TODAY_CHECKED_AT,
        ),
    ],
}

DRAFTS[20] = {
    "summary": "正確答案是 C。GPT-Realtime 類型模型的設計目的是低延遲的「語音進、語音出」即時互動，即時語音客服與互動式代理正是官方文件點名的典型用例。",
    "concept": (
        "GPT-Realtime 類型模型主打即時語音對話：支援低延遲的語音輸入與語音"
        "輸出，使用者說話、模型近乎即時地以語音回應，並支援打斷與輪替。"
        "Microsoft Learn 的官方文件寫得直接：GPT Realtime API 為即時、低延遲"
        "的對話互動而設計，適合使用者與模型即時互動的用例，例如客服代理"
        "（customer support agents）、語音助理與即時翻譯；語音代理型會話還能"
        "邊聽、邊推理、邊說並呼叫工具。\n"
        "選型的判準因此是「互動即時性」：只有當使用者正在線上等著一來一往，"
        "毫秒級延遲才有價值。批次報表、結構化檢索、高一致性摘要這些場景要的"
        "分別是吞吐量、查詢正確性與輸出穩定，即時語音能力派不上用場。"
    ),
    "answerReason": (
        "題目要找最適合的應用場景。即時語音客服與互動式 AI 代理需要的能力——"
        "低延遲語音串流、對話輪替、即時打斷、邊對話邊呼叫工具——正是 Realtime "
        "類型模型的設計核心，與官方文件列出的客服代理與語音助理用例一致。"
        "其餘三個場景分別以吞吐、檢索正確性或輸出一致性為重，都用不上即時"
        "語音互動這項賣點，因此選 C。"
    ),
    "optionAnalysis": {
        "A": (
            "長時間批次報表生成重視的是吞吐量與單位成本：任務可以排程、可以"
            "離線跑，沒有使用者在線上等待，毫秒級延遲毫無價值。這類工作適合"
            "批次推論或一般文字模型搭配排程系統；用即時語音模型來跑批次，"
            "等於為用不到的即時性付出額外成本。"
        ),
        "B": (
            "即時資料查詢與結構化資訊檢索的核心是資料庫與搜尋引擎：靠索引、"
            "查詢語言與排序取得正確結果，這裡的「即時」指的是資料新鮮度與查詢"
            "回應，靠檢索架構就能達成。它不需要語音串流與對話輪替能力，"
            "一般語言模型搭配檢索增強即可勝任，語音即時模型的專長使不上力。"
        ),
        "C": (
            "正確。語音客服與互動式代理的體驗取決於反應速度：使用者開口後要"
            "立刻聽到回應、講到一半可以打斷、代理還要能在對話中呼叫查詢工具。"
            "Realtime 類型模型的低延遲語音進出與語音代理會話設計正是為此而"
            "生，官方文件也把客服代理與語音助理列為典型用例。"
        ),
        "D": (
            "法規文件自動摘要把「高一致性」列為優先：同一份文件每次摘要應得到"
            "穩定結果，靠的是低溫度設定、固定提示範本與人工複核，而且完全可以"
            "批次處理。它不存在語音互動需求，也不在乎毫秒級延遲；以一致性為先"
            "的任務，反而應避開為即時反應最佳化的模型組態。"
        ),
    },
    "trap": (
        "第一，選型先問「有沒有人在線上等著一來一往」：有，才輪得到 Realtime "
        "類型模型；沒有，就回到批次或一般文字模型。第二，別把三種「即時」混為"
        "一談——語音互動的低延遲、檢索資料的新鮮度、系統回應的速度是不同層面"
        "的需求，題目考的是第一種。"
    ),
    "references": [
        exam_ref(20),
        ref(
            "Microsoft Learn－Use the GPT Realtime API for speech and audio（Azure OpenAI）",
            "https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/realtime-audio",
            "GPT Realtime API 為即時、低延遲的對話互動而設計，支援 speech in, speech out，典型用例包含客服代理、語音助理與即時翻譯；voice-agent session 可聽、推理、說並呼叫工具",
            TODAY_CHECKED_AT,
        ),
        guide_ref("第三章 3-22 多模態整合與協同生成：語音與文字轉換，如 Whisper 與 ChatGPT 語音模式，實現語音與文字的無縫轉換"),
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
