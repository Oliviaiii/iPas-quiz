"""Write the phase-two explanation drafts for 115-1 elementary subject two, Q21-Q30.

Same guarantees as the earlier batches: the script only fills ``explanation`` on
questions that already exist, aborts if an official answer no longer matches the
answer a draft was written against, and refuses to overwrite anything already
marked reviewed.

Every cited URL was opened and checked on the date recorded in ``checkedAt``.
Study-guide locators are reused verbatim from the 114-4 subject-two batches,
which verified them against the guide PDF on 2026-07-31; the exam PDF itself was
retrieved and page-checked on 2026-07-29 (see sources.json retrievedAt).

Usage::

    python scripts/write-explanations-115-1-s2-021-030.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-elementary-1-genai-planning"
AUTHOR = "Claude Code（AI 輔助初稿）"
AUTHORED_AT = "2026-08-03"
# 三種查核日期：考題 PDF 於 2026-07-29 取得並逐頁核對；學習指引與 arXiv/A2A
# 參考沿用 114-4 科目二批次於 2026-07-31 的驗證；其餘網址於 2026-08-03 開啟確認。
EXAM_CHECKED_AT = "2026-07-29"
REUSED_CHECKED_AT = "2026-07-31"
CHECKED_AT = "2026-08-03"

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


EXPECTED_ANSWER = {
    21: "D", 22: "D", 23: "A", 24: "D", 25: "A",
    26: "C", 27: "A", 28: "C", 29: "C", 30: "B",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[21] = {
    "summary": "正確答案是 D。AgentKit 是 OpenAI 推出的代理開發工具組，核心用途是支援 AI 代理的建構、工具整合與任務流程開發。",
    "concept": (
        "AI 代理（Agent）是能規劃步驟、呼叫外部工具並保持狀態以完成多步驟任務"
        "的應用程式。OpenAI 於 2025 年發表的 AgentKit，就是把建構這類代理所需的"
        "元件打包成一套開發工具組：開發者可在視覺化畫布（Agent Builder）上以"
        "拖放節點串接代理、工具與控制流程來設計任務工作流程，再透過可嵌入的"
        "聊天介面（ChatKit）或 SDK 程式碼部署到自家產品之中。\n"
        "作答時要把「應用層的代理開發工具」與其他層次的東西分開：訓練框架負責"
        "模型的預訓練與權重更新；模擬環境服務強化學習的訓練迴圈；通訊協議規範"
        "代理之間如何互相溝通。AgentKit 不做這三件事，它假設模型能力已經存在，"
        "聚焦在把模型組裝成會用工具、能跑流程的代理應用。"
    ),
    "answerReason": (
        "OpenAI 開發者文件對代理的定義是能規劃、呼叫工具並完成多步驟工作的"
        "應用，而 AgentKit 相關工具（如 Agent Builder）讓開發者以節點組合代理、"
        "工具與控制流程邏輯來建構並部署工作流程。D 所述「支援 Agents 的建構、"
        "工具整合與任務流程開發」正是這個定位，因此為正確答案。"
    ),
    "optionAnalysis": {
        "A": (
            "建立強化式學習訓練用的互動式模擬環境，是 OpenAI Gym（後續為 "
            "Gymnasium）這類強化學習工具庫的角色，提供代理人與環境試錯互動的"
            "介面。AgentKit 服務的是以現成大型語言模型組裝代理應用的開發者，"
            "並不提供強化學習訓練所需的模擬環境。"
        ),
        "B": (
            "大規模預訓練與權重優化屬於模型訓練基礎設施的工作，需要訓練框架、"
            "龐大算力與資料管線，由模型供應商在建模階段完成。AgentKit 位在"
            "應用層，假設模型能力已經存在，讓開發者專注於流程與工具的組裝，"
            "不涉及模型權重的訓練或更新。"
        ),
        "C": (
            "「Agent-to-Agent」（A2A）是一套開放的代理間通訊協議，規範 Client "
            "Agent 與 Remote Agent 之間如何委派任務與回傳結果，讓不同系統的"
            "代理能互通。AgentKit 則是單一廠商的開發工具組，兩者一個是跨系統"
            "的互通規範、一個是產品層的建構工具，性質不同。"
        ),
        "D": (
            "正確。AgentKit 的定位是代理開發工具組：以視覺化建構器把代理、"
            "工具與控制流程節點組成任務工作流程，支援把外部工具與資料介接進"
            "代理，再部署成可用的應用，涵蓋建構、工具整合與任務流程開發，"
            "與題目問的主要用途一致。"
        ),
    },
    "trap": (
        "第一，區分「開發工具組」與「通訊協議」：AgentKit 幫你把代理做出來，"
        "A2A 規範代理之間怎麼講話，選項 C 借用相似詞彙混淆兩者。第二，看到 "
        "Agent 一詞別直覺聯想到強化學習：本題脈絡是大型語言模型的代理應用"
        "開發，與強化學習的模擬環境無關。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
        "待查項目：OpenAI AgentKit 官方公告頁（openai.com/index/introducing-agentkit）"
        "本日回應 HTTP 403 無法開啟，AgentKit 完整元件清單（如 Connector "
        "Registry、Evals）未能逐項核對，僅以可開啟的 OpenAI 開發者文件"
        "（Agents 指南與 Agent Builder 頁）佐證代理建構與工作流程開發功能；"
        "Agent Builder 文件頁另標示該工具已排定停用時程，產品組成變動快，"
        "宜由複核者確認最新狀態。查核日期 2026-08-03。"
    ),
    "references": [
        exam_ref(21),
        {
            "title": "OpenAI 開發者文件－Agents",
            "url": "https://developers.openai.com/api/docs/guides/agents",
            "locator": "Agents 指南：代理是能規劃、呼叫工具、跨專家協作並保持狀態以完成多步驟工作的應用程式；SDK 負責執行工具迴圈與代理交接",
            "checkedAt": CHECKED_AT,
        },
        {
            "title": "OpenAI 開發者文件－Agent Builder",
            "url": "https://developers.openai.com/api/docs/guides/agent-builder",
            "locator": "Agent Builder：以拖放節點的視覺化畫布建構多步驟代理工作流程，工作流程由代理、工具與控制流程邏輯組成，可經 ChatKit 或 SDK 程式碼部署",
            "checkedAt": CHECKED_AT,
        },
        {
            "title": "A2A Protocol－官方文件",
            "url": "https://a2a-protocol.org/latest/",
            "locator": "Client Agent 與 Remote Agent 的角色定義與任務委派流程",
            "checkedAt": REUSED_CHECKED_AT,
        },
    ],
}

DRAFTS[22] = {
    "summary": "正確答案是 D。Google 對 Veo 生成的影片以 SynthID 技術嵌入人眼不可見的數位浮水印，讓內容可被偵測為 AI 生成，以因應不實資訊風險。",
    "concept": (
        "生成式 AI 讓影片可以被大量合成，平台因此需要一種不影響觀看體驗、又"
        "難以移除的機制，來標記「這段內容是 AI 生成的」。SynthID 是 Google "
        "DeepMind 開發的浮水印技術，把數位浮水印直接嵌入 AI 生成的圖像、音訊、"
        "文字與影片之中；浮水印對人眼不可察覺，不改變影像或影片品質，但可由"
        "對應的偵測工具讀出，用來判斷內容是否出自 Google 的生成式模型。\n"
        "依 DeepMind 的說明，這種浮水印設計上能抵抗裁切、加濾鏡、變更影格率與"
        "失真壓縮等常見修改，因此比外加的可見標示更難被去除；Google 也明確"
        "表示以 Veo 生成的影片會以 SynthID 標記，作為偵測 AI 生成內容、支撐"
        "透明性與信任的依據。"
    ),
    "answerReason": (
        "題目問 Veo 生成影片採用哪種「技術措施」協助企業用戶因應 AI 生成內容"
        "的不實資訊風險。Google 的作法正是以 SynthID 在生成影片中嵌入不可見的"
        "數位浮水印，讓內容即使被轉傳、剪輯後仍可被偵測為 AI 生成，D 的敘述"
        "與此一致；其餘選項描述的用量限制與可見警語，都不是 Veo 實際採用的"
        "浮水印機制。"
    ),
    "optionAnalysis": {
        "A": (
            "限制每日生成次數與使用時間屬於用量管制，目的通常是控管資源成本"
            "或濫用頻率。它無法讓已經產出的影片被辨識為 AI 生成，影片一旦流出"
            "平台便失去追蹤依據，因此解決不了不實資訊被散播後的辨識問題。"
        ),
        "B": (
            "在影片開頭與結尾加入可見的 AI 標示警語是一種揭露手段，部分平台"
            "確實會搭配使用；但可見標示只出現在特定位置，經剪輯、裁切就能輕易"
            "移除。SynthID 的特點恰好相反：浮水印不可見且嵌入內容本身，能在"
            "後續修改中留存。"
        ),
        "C": (
            "強制附帶至少 10 秒的免責聲明片段同樣屬於外加的可見內容，除了"
            "嚴重干擾影片的實際使用，也和可見警語一樣能被剪掉。Google 並未對 "
            "Veo 影片採取此種作法，題目所述的技術措施是嵌入式浮水印而非附加"
            "聲明片段。"
        ),
        "D": (
            "正確。Veo 生成的影片以 SynthID 嵌入人眼不可察覺的數位浮水印，"
            "浮水印不影響影片品質，且設計上能抵抗變更影格率、壓縮等修改，"
            "使企業與平台之後仍能以偵測工具驗證內容是否為 AI 生成，直接支撐"
            "不實資訊的辨識與治理。"
        ),
    },
    "trap": (
        "第一，區分「可見標示」與「不可見浮水印」：警語與聲明片段可被剪除，"
        "嵌入內容本身的浮水印才能在轉傳與修改後留存。第二，別把「限制使用量」"
        "當成內容治理手段，用量管制影響的是產出多少，不影響產出內容能否被"
        "辨識為 AI 生成。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
        "待查項目：已驗證的 DeepMind SynthID 與 Veo 頁面確認「Veo 影片以 "
        "SynthID 嵌入不可見浮水印、不影響品質、可抵抗變更影格率等修改」，"
        "但頁面未逐字寫出題幹選項所稱『每一幀（frame）』的嵌入粒度，該細節"
        "依官方公告試題選項文字保留，宜由複核者向 Google 官方說明補查。"
        "查核日期 2026-08-03。"
    ),
    "references": [
        exam_ref(22),
        {
            "title": "Google DeepMind－SynthID",
            "url": "https://deepmind.google/science/synthid/",
            "locator": "SynthID 將數位浮水印直接嵌入 AI 生成的圖像、音訊、文字或影片，浮水印人眼不可察覺、不改變影像或影片品質，並設計為可抵抗裁切、濾鏡、變更影格率與失真壓縮等修改",
            "checkedAt": CHECKED_AT,
        },
        {
            "title": "Google DeepMind－Veo",
            "url": "https://deepmind.google/models/veo/",
            "locator": "以 Veo 生成的影片會以 SynthID 標記，作為浮水印與偵測 AI 生成內容的技術",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[23] = {
    "summary": "正確答案是 A。判斷理賠案件是否為詐欺是分類判別任務，屬鑑別式 AI；自動產出調查報告是生成新內容，屬生成式 AI。",
    "concept": (
        "鑑別式 AI（Discriminative AI）與生成式 AI（Generative AI）的分工可以"
        "用「輸出是什麼」來判斷。鑑別式模型學習輸入特徵與類別之間的判斷邊界，"
        "輸出是一個標籤或分數，典型任務是分類與辨識，例如判斷交易是否異常、"
        "郵件是否為垃圾郵件。生成式 AI 則透過深度學習與大數據集的訓練來生成"
        "新的內容，而非僅僅分析或辨識現有數據，輸出是一段原本不存在的文字、"
        "圖像或音訊。\n"
        "回到題目：功能 (1) 要回答「這件理賠案是不是詐欺」，輸出是二元判斷，"
        "屬於鑑別式的分類任務；功能 (2) 要把調查內容寫成一份新的報告文件，"
        "輸出是整段新生成的文字，屬於生成式任務。"
    ),
    "answerReason": (
        "功能 (1) 的產出是「詐欺／非詐欺」的類別標籤，模型的工作是在既有資料"
        "上劃出判斷邊界，這是鑑別式 AI 的核心用途；功能 (2) 的產出是一份先前"
        "不存在的調查報告全文，模型的工作是生成新內容，這是生成式 AI 的定義。"
        "兩個功能一判別、一生成，正好與 A 的配對相符。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。詐欺判斷輸出類別標籤，以判斷邊界區分正常與詐欺案件，是"
            "鑑別式 AI 的分類任務；調查報告生成輸出新的文字內容，需要語言生成"
            "能力，是生成式 AI 的應用，配對方向與兩類技術的定義一致。"
        ),
        "B": (
            "把兩者對調了。詐欺判斷要的是判別結果，交給「生成式」的歸類等於"
            "期待模型產生內容而非給出類別；把報告生成歸為「鑑別式」更說不通，"
            "因為鑑別式模型的輸出是標籤或分數，無法產出整份報告文字。順序"
            "顛倒是本選項唯一但致命的錯誤。"
        ),
        "C": (
            "兩者都算鑑別式只說對了一半。詐欺判斷確實是鑑別式任務，但調查"
            "報告生成要求模型逐字產出新文件，超出鑑別式模型「在既有類別中做"
            "判斷」的能力範圍，因此第二個功能的歸類錯誤。"
        ),
        "D": (
            "兩者都算生成式同樣只對一半。報告生成確實是生成式應用，但詐欺"
            "判斷要的是明確的類別結論，以鑑別式分類模型處理最直接；本題考的"
            "是兩種 AI 技術類型的定義歸屬，判別任務仍應歸於鑑別式而非生成式。"
        ),
    },
    "trap": (
        "第一，用「輸出型態」快速分流：輸出標籤或分數是鑑別式，輸出新文字、"
        "新圖像是生成式。第二，留意配對題的順序陷阱：選項 A 與 B 內容相同、"
        "只是順序對調，審題時要把 (1)(2) 與選項逐一對位再作答。"
    ),
    "references": [
        exam_ref(23),
        guide_ref("第三章 3-17：生成式 AI 專注於透過深度學習和大數據集的訓練來生成新的內容，而非僅僅分析或辨識現有數據"),
    ],
}

DRAFTS[24] = {
    "summary": "正確答案是 D。總體擁有成本要涵蓋直接成本之外的訓練、系統整合與資安合規等間接支出，D 的範圍最完整。",
    "concept": (
        "總體擁有成本（Total Cost of Ownership, TCO）是協助買方與擁有者估算"
        "一項產品或服務「直接與間接成本」的財務估算方法，重點在於擁有成本"
        "往往遠高於採購價格本身。對導入生成式 AI 系統而言，直接成本包括 API "
        "調用費、維護人力與基礎設施；間接成本則涵蓋人員訓練、與既有系統的"
        "整合開發、資安與法規遵循，乃至後續升級與汰換等生命週期支出。\n"
        "評估哪一項 TCO 分析「最完整」時，判斷標準不是把看得到的帳單加總，"
        "而是有沒有把上述隱藏成本一併納入。題目給的三筆月費（API 15 萬、人力 "
        "8 萬、基建 5 萬）只是直接成本的部分，完整分析必須再加上間接項目。"
    ),
    "answerReason": (
        "題目問哪一項 TCO 分析「最完整」。A、B、C 都停留在直接成本的不同"
        "子集：A 只看 API 費用，B 加上人力，C 把三項直接成本加齊為 28 萬元；"
        "只有 D 在直接成本之外進一步納入人員訓練、系統整合與資安合規等相關"
        "支出，符合 TCO 同時估算直接與間接成本、著眼整個生命週期的定義，"
        "因此為正確答案。"
    ),
    "optionAnalysis": {
        "A": (
            "只以 API 調用成本 15 萬元為評估基礎，等於把 TCO 化約為單一帳單"
            "項目，連題目已明列的維護人力 8 萬元與基礎設施 5 萬元都被排除，"
            "是四個選項中涵蓋面最窄的估算，會嚴重低估導入的真實成本。"
        ),
        "B": (
            "納入 API 費用與維護人力共 23 萬元，比 A 完整，但仍漏掉題目明列"
            "的基礎設施成本 5 萬元，更未觸及任何間接成本。既然題目資訊中就有"
            "被遺漏的直接項目，這個估算稱不上完整。"
        ),
        "C": (
            "把 API 調用、維護人力與基礎設施加總為約 28 萬元，是「直接成本」"
            "層次上正確的計算；但 TCO 的定義本來就要求同時估算直接與間接"
            "成本，訓練、整合與合規支出都未納入，因此在「最完整」的比較下"
            "仍不如 D。"
        ),
        "D": (
            "正確。除了三項直接成本外，再納入人員訓練、系統整合與資安合規等"
            "相關支出，正是 TCO 強調「擁有成本高於採購成本、需涵蓋生命週期中"
            "直接與間接支出」的精神，是四個選項中涵蓋面最完整的分析。"
        ),
    },
    "trap": (
        "第一，看到數字加總正確就急著選 C 是本題主要陷阱：C 只完成了直接成本"
        "的加總，而題目問的是 TCO 分析的完整性。第二，記住 TCO 與單純預算"
        "編列的差別：前者包含訓練、整合、合規、汰換等隱藏成本，後者往往只列"
        "看得見的帳單。"
    ),
    "editorialNote": (
        "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
        "待查項目：TCO 的一手定義來源（Gartner 詞彙表與 IBM 主題頁）本日均"
        "回應 HTTP 403 無法開啟，暫以維基百科條目作為輔助參考；官方學習指引"
        "既有已驗證段落中亦未見 TCO 專節，宜由複核者補查更權威的一手出處。"
        "查核日期 2026-08-03。"
    ),
    "references": [
        exam_ref(24),
        {
            "title": "Wikipedia－Total cost of ownership",
            "url": "https://en.wikipedia.org/wiki/Total_cost_of_ownership",
            "locator": "TCO 定義：協助買方與擁有者估算產品或服務直接與間接成本的財務估算，涵蓋採購、安裝與訓練、整合、資安、維運乃至汰換升級等生命週期成本",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[25] = {
    "summary": "正確答案是 A。改用 API 後每月成本僅 960 元，較人工翻譯 30,000 元淨節省 29,040 元，20 萬元整合費約 7 個月回收。",
    "concept": (
        "本題把投資報酬率（Return on Investment, ROI）評估化成兩步計算：先算"
        "「每月淨節省」，再算「一次性投入的回收期」。每月淨節省 = 原人工成本 "
        "− 新方案變動成本；回收期 = 一次性整合費用 ÷ 每月淨節省。\n"
        "代入題目數字：人工翻譯每月 600 則 × 50 元 = 30,000 元。改用 API 後，"
        "每月 token 用量為 600 則 × 2,000 tokens = 1,200,000 tokens，費用為 "
        "1,200,000 ÷ 1,000 × 0.8 元 = 960 元。每月淨節省 30,000 − 960 = "
        "29,040 元；系統整合費 200,000 元 ÷ 29,040 元 ≈ 6.9 個月，約 7 個月"
        "回收。API 服務以 token 用量計價，變動成本要以「則數 × 每則 token 數 "
        "× 單價」逐步換算，不能省略。"
    ),
    "answerReason": (
        "依題目條件逐步計算：每月 API 成本 960 元、人工成本 30,000 元，淨節省 "
        "30,000 − 960 = 29,040 元；一次性整合費 200,000 元除以每月淨節省 "
        "29,040 元約為 6.9 個月，即約 7 個月回收。A 的兩個數字（29,040 元、"
        "約 7 個月）皆與計算相符，是唯一計算正確的選項。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。API 月費為 600 則 × 2,000 tokens ÷ 1,000 × 0.8 元 = 960 元，"
            "每月淨節省 30,000 − 960 = 29,040 元；回收期 200,000 ÷ 29,040 ≈ "
            "6.9 個月，約 7 個月，節省金額與回收期兩個數字都正確。"
        ),
        "B": (
            "每月節省 30,000 元是把人工成本全額當成節省，漏扣了改用 API 之後"
            "仍要支付的 960 元變動成本。ROI 評估比較的是兩方案的成本差額，"
            "新方案自身的使用費必須扣除，因此 30,000 元高估了每月效益。"
        ),
        "C": (
            "28,040 元相當於把 API 月費多算成 1,960 元（正確為 960 元）；而且"
            "此選項內部並不一致：若每月真能節省 28,040 元，回收期為 200,000 ÷ "
            "28,040 ≈ 7.1 個月，仍約 7 個月而非 8 個月，金額與回收期兩者都站"
            "不住。"
        ),
        "D": (
            "每月節省 25,000 元找不到可由題目數字推得的計算路徑；雖然 200,000 "
            "÷ 25,000 = 8 個月讓金額與回收期內部一致，但起點的節省金額本身"
            "錯誤，內部一致並不能取代正確的成本計算。"
        ),
    },
    "trap": (
        "第一，最常見的錯誤是忘記扣除新方案自身的變動成本，直接把人工費用 "
        "30,000 元當成每月節省（選項 B 的陷阱）。第二，token 費用要按「每 "
        "1,000 tokens 0.8 元」的單價換算：600 則 × 2,000 tokens 是 120 萬 "
        "tokens，換算後僅 960 元，數量級一旦估錯就會落入其他選項的數字。"
    ),
    "references": [
        exam_ref(25),
        {
            "title": "Anthropic Claude 平台文件－Pricing",
            "url": "https://platform.claude.com/docs/en/docs/about-claude/pricing",
            "locator": "模型定價表：API 依輸入與輸出 token 分別以每百萬 token 計價，為商用生成式 AI 服務以 token 用量計費的實例",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[26] = {
    "summary": "正確答案是 C。平台已擁有大量歷史案例資料，RAG 能在生成報告前先檢索這些內部案例，讓特徵描述有依據可循。",
    "concept": (
        "檢索增強生成（Retrieval-Augmented Generation, RAG）把外部知識庫接進"
        "生成流程：撰寫回覆或報告之前，先從資料庫檢索出相關文件片段，再讓"
        "語言模型以檢索結果為依據生成內容。它以外部的非參數化記憶補充模型"
        "參數中的知識，使知識可以隨資料庫更新，生成結果也有出處可追溯。\n"
        "本題情境正符合 RAG 的適用條件：支付平台已累積大量歷史交易紀錄與已知"
        "洗錢案例，需求是自動生成「可疑交易的特徵描述報告」。把案例資料庫"
        "作為檢索來源，模型生成的每段特徵描述都能對應到實際案例，既利用了"
        "既有的資料資產，也降低模型憑空編造特徵的風險。"
    ),
    "answerReason": (
        "題目的兩個關鍵條件是「擁有大量歷史交易紀錄和已知洗錢案例資料」與"
        "「自動生成特徵描述報告」。RAG 正是為此設計：以歷史案例資料庫為檢索"
        "來源，生成報告時先取回相關案例，再據以描述可疑交易的特徵，輸出有"
        "依據、可追溯，也能隨新案例入庫而更新，因此 C 最適合本題需求。"
    ),
    "optionAnalysis": {
        "A": (
            "Midjourney 是文字生成圖像的工具，產出的是視覺影像。本題要的是"
            "文字形式的特徵描述報告，交易流程「圖像」無法承載可疑特徵的細節"
            "描述，也用不上平台累積的歷史案例文字資料，工具型態與任務需求"
            "並不相合。"
        ),
        "B": (
            "Few-shot Learning 是以少量示例讓模型適應新任務的技術，圖像識別"
            "模型處理的則是影像輸入。本題的交易紀錄與案例屬於結構化與文字"
            "資料，不是影像；且平台明明擁有大量歷史資料，不存在「僅有少量"
            "樣本」的前提，兩個設定都對不上題目。"
        ),
        "C": (
            "正確。RAG 將歷史交易紀錄與已知洗錢案例建成檢索資料庫，生成報告"
            "時先檢索相關案例再撰寫特徵描述，輸出內容有實際案例支撐、來源可"
            "追溯，並能隨案例庫更新而反映新的洗錢型態，完整發揮平台的資料"
            "優勢。"
        ),
        "D": (
            "直接使用 ChatGPT 基礎模型，模型只具備訓練語料中的一般性知識，"
            "接觸不到平台內部的交易紀錄與案例資料，描述可疑特徵時缺乏依據，"
            "容易產出籠統甚至憑空推測的內容。與 C 的關鍵差異就在於有沒有把"
            "內部案例庫接進生成流程。"
        ),
    },
    "trap": (
        "第一，題幹強調「擁有大量內部資料」時，優先考慮把資料接進生成流程的 "
        "RAG，而不是換一個更大的通用模型。第二，檢查選項的模態與任務是否"
        "對得上題目：影像生成、圖像識別與文字報告生成是三種不同任務，關鍵詞"
        "再熟悉也要回到題目需求核對。"
    ),
    "references": [
        exam_ref(26),
        {
            "title": "arXiv－Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
            "url": "https://arxiv.org/abs/2005.11401",
            "locator": "以外部非參數化記憶補充模型參數知識，使知識可更新且生成結果有出處可追溯",
            "checkedAt": REUSED_CHECKED_AT,
        },
    ],
}

DRAFTS[27] = {
    "summary": "正確答案是 A。以 n8n 這類工作流程自動化工具串接既有 AI 檢測 API、檔案系統與通訊軟體，建置快，又保留調整彈性。",
    "concept": (
        "題目的需求是把「AI 檢測到瑕疵」這個事件，接到「自動拍照存檔」與"
        "「通知品管人員」兩個後續動作，本質上是一條跨系統的自動化工作流程"
        "（Workflow）。n8n 是一套工作流程自動化工具，結合 AI 能力與商業流程"
        "自動化，讓使用者以節點串接不同服務：一個節點介接 AI 檢測 API 接收"
        "事件，一個節點把影像寫入檔案系統，再一個節點透過通訊軟體發送通知，"
        "必要時還能插入自訂程式碼節點處理特殊邏輯。\n"
        "這類工具的價值正對應題目的三個條件：公司已有 AI 檢測系統（只需整合，"
        "不必重造）、具有一定開發人力（能維護流程與少量程式碼）、希望快速"
        "建置且保有彈性（拖放節點即可修改流程，不必更動整套系統）。"
    ),
    "answerReason": (
        "逐一檢查題目條件：既有 AI 系統要「整合」而非重寫，n8n 以 API 節點"
        "直接介接；「快速建置」靠現成節點組裝，不需從零開發；「保有彈性調整"
        "空間」靠視覺化流程隨時增改節點，並可加入程式碼擴充；「具一定開發"
        "人力」正好能駕馭這種工具。A 同時滿足全部條件，因此最適合。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。以 n8n 建立工作流，AI 檢測 API、檔案系統與通訊軟體各以節點"
            "介接，檢測事件觸發後自動完成拍照存檔與通知；流程以視覺化方式"
            "維護，公司的開發人力可自行調整或擴充節點，兼顧建置速度、整合"
            "能力與後續彈性。"
        ),
        "B": (
            "委外開發客製化程式確實能完全符合需求規格，適合流程極複雜、內部"
            "無人力維護的場景。但開發週期長、費用高，與「快速建置」相違；"
            "日後每次流程調整都得回頭找廠商，彈性掌握在外部而非自己手上，"
            "公司既有的開發人力反而閒置。"
        ),
        "C": (
            "採購現成品質管理軟體導入最快，但套裝功能由廠商決定，未必能介接"
            "公司「既有的」AI 檢測系統與特定通知管道；遇到流程變更只能等待"
            "廠商支援或加購模組，客製彈性最小，與「保有彈性調整空間」的要求"
            "不符。"
        ),
        "D": (
            "Excel 巨集擅長表格資料的批次處理，搭配人工作業則代表瑕疵發生後"
            "仍要有人手動介入，無法在檢測事件發生的當下自動拍照存檔並即時"
            "通知品管人員。這與題目「自動化品質檢測流程」的目標相反，只是把"
            "原本的人工流程換個工具執行。"
        ),
    },
    "trap": (
        "第一，題目同時給了「快速」與「彈性」兩個條件：委外客製犧牲速度、"
        "套裝軟體犧牲彈性，只有工作流程自動化工具能兩者兼顧。第二，判斷"
        "自動化方案時，注意流程中是否仍殘留人工步驟，凡是需要人手動觸發的"
        "選項都不符合事件驅動的自動化需求。"
    ),
    "references": [
        exam_ref(27),
        {
            "title": "n8n 官方文件",
            "url": "https://docs.n8n.io/",
            "locator": "n8n 為 fair-code 授權的工作流程自動化工具，結合 AI 能力與商業流程自動化",
            "checkedAt": CHECKED_AT,
        },
        guide_ref("第三章 3-23 AI 即服務（AIaaS）：API 介接與外掛程式讓企業能輕鬆整合 AI 工具至現有流程中"),
    ],
}

DRAFTS[28] = {
    "summary": "正確答案是 C。Token Economics 只涵蓋推理與生成階段的 token 用量與費用，訓練階段的 GPU 記憶體成本屬模型建置支出，不在其範圍。",
    "concept": (
        "題幹已給出定義：Token Economics 指「模型推理與生成過程中，Token "
        "使用量及其費用」。商用大型語言模型 API 以 token 為計價單位，帳單由"
        "兩部分構成：送進模型的輸入（input）token 與模型產出的輸出（output）"
        "token，兩者分別計價。因此估算「每日處理 50 萬筆資料、生成 1,000 份"
        "報告」的成本，就是估算每次呼叫的輸入 token 數、生成內容的輸出 token "
        "費用，以及整體推理過程的 token 用量統計。\n"
        "與此相對，模型「訓練階段」的成本屬於另一個帳本：GPU 算力與記憶體、"
        "訓練資料處理等支出發生在模型建置期，由模型供應商承擔。採用現成 API "
        "的導入團隊按用量付費，不需負擔訓練成本，自然不會把它放進 Token "
        "Economics 分析。"
    ),
    "answerReason": (
        "本題是「何者不屬於」的反向題。A（每次呼叫的輸入 token 數）、B（生成"
        "內容的輸出 token 費用）、D（推理過程的 token 用量統計）都落在題幹"
        "定義的「推理與生成過程中的 token 用量及其費用」範圍內；只有 C 講的"
        "是模型訓練階段的 GPU 記憶體成本，屬於建模期的基礎設施支出而非推理"
        "計價項目，因此選 C。"
    ),
    "optionAnalysis": {
        "A": (
            "每次 API 呼叫所需的輸入 token 數量是 Token Economics 的基本變數："
            "50 萬筆交通資料整理成提示後有多少 token 進入模型，直接決定輸入端"
            "費用，屬於推理階段的用量估算，在分析範圍之內，不是本題要挑的"
            "項目。"
        ),
        "B": (
            "生成報告內容所消耗的輸出 token 費用是核心項目：每日 1,000 份報告"
            "的長度換算成輸出 token 數，乘上輸出單價就是生成端成本。商用 API "
            "的輸出單價通常高於輸入單價，更是成本估算的重點，因此在考量範圍"
            "之內。"
        ),
        "C": (
            "正確（即不屬於考量範圍）。訓練階段使用 token 數量所需的 GPU 記憶"
            "體成本，是模型開發者在建置模型時的算力與硬體支出，發生在訓練期"
            "而非推理期。題幹已把 Token Economics 限定於推理與生成過程，採用 "
            "API 服務的交通局也不需承擔供應商的訓練成本，故此項超出分析範圍。"
        ),
        "D": (
            "模型推理過程中的 token 使用量統計是成本監控的基礎：持續記錄各"
            "批次呼叫實際消耗的輸入與輸出 token，才能核對帳單、預估月成本並"
            "找出可壓縮的環節，明確屬於題幹定義的推理階段 token 用量分析。"
        ),
    },
    "trap": (
        "第一，本題問「不屬於」，先依題幹定義畫出邊界（推理與生成階段），再"
        "逐項檢查；別被 C 裡出現的「Token」字樣拉回範圍內，它的主詞其實是"
        "訓練期的 GPU 記憶體成本。第二，區分「訓練成本」與「推理成本」：前者"
        "是建模期的一次性投入，後者才是按用量持續發生的營運費用。"
    ),
    "references": [
        exam_ref(28),
        {
            "title": "Anthropic Claude 平台文件－Pricing",
            "url": "https://platform.claude.com/docs/en/docs/about-claude/pricing",
            "locator": "模型定價表：API 依輸入與輸出 token 分別以每百萬 token 計價，輸出 token 單價高於輸入 token 單價",
            "checkedAt": CHECKED_AT,
        },
        guide_ref("第三章 3-18：標記化處理將文本拆分為基本單元、向量化表示將文本轉換為數值形式以適應深度學習模型"),
    ],
}

DRAFTS[29] = {
    "summary": "正確答案是 C。合作社僅有一位具基礎程式概念的人員，Low-Code 平台以視覺化拖拉為主、少量程式碼為輔，最能配合此人力條件完成客製流程。",
    "concept": (
        "No-Code 與 Low-Code 是降低開發門檻的兩種取徑。No-Code 以拖曳元件"
        "設計介面與流程，完全不寫程式，適合流程單純、標準化的應用；Low-Code "
        "則結合視覺化開發與程式碼擴充，大部分功能以拖拉組裝，遇到平台內建"
        "元件不夠用的環節，再以少量程式碼補強，適合需要一定整合深度與客製"
        "邏輯的應用。\n"
        "題目的流程橫跨多個系統：手機 APP 回報照片、自動通知專家、建立案件"
        "紀錄、排程現場訪查，彼此之間有觸發與資料傳遞的客製邏輯；人力條件"
        "則是「僅一位具備基礎程式概念的人員」。這個組合正好落在 Low-Code 的"
        "適用區間——視覺化開發扛起大部分工作，少量程式碼處理客製環節，一個"
        "人也維護得動。"
    ),
    "answerReason": (
        "把需求與人力放在一起看：流程需要跨系統整合與客製邏輯，純視覺化平台"
        "可能不敷使用，全程式開發又超出人力負荷；唯一具備基礎程式概念的人員，"
        "恰好能在 Low-Code 平台上以拖拉完成主流程，再用少量程式碼處理通知、"
        "建檔與排程的銜接細節。C 在開發門檻與客製彈性之間的平衡最符合題目"
        "條件。"
    ),
    "optionAnalysis": {
        "A": (
            "傳統程式開發從零撰寫完整系統，自由度最高，適合有完整工程團隊、"
            "需求高度特殊的組織。但合作社只有一位具基礎程式概念的人員，獨力"
            "開發並長期維護整套含 APP 介接、通知與排程的系統並不實際，開發"
            "週期與失敗風險都過高。"
        ),
        "B": (
            "純 No-Code 平台完全不需程式技能，對零技術背景的團隊是合理起點；"
            "但本題流程涉及照片回報觸發、專家通知、案件建檔與訪查排程等多"
            "系統銜接，客製邏輯一旦超出平台內建元件的範圍，No-Code 就難以"
            "擴充。既有具程式概念的人力不加利用，等於放棄了擴充空間。"
        ),
        "C": (
            "正確。Low-Code 結合視覺化拖拉與少量程式碼：主流程以拖放快速"
            "組裝，特殊銜接邏輯以簡短程式補強，正好匹配「IT 人力有限、但有"
            "一位具基礎程式概念人員」的條件，也保留流程日後調整與擴充的"
            "彈性。"
        ),
        "D": (
            "直接購買現成農業管理軟體且不做客製，導入負擔最小，但套裝功能"
            "未必涵蓋病蟲害照片回報、指定專家通知與現場訪查排程這一整條特定"
            "流程；不客製就只能遷就軟體既有設計，需求缺口將由人工作業填補，"
            "自動化目標無法達成。"
        ),
    },
    "trap": (
        "第一，區分 No-Code 與 Low-Code 的適用邊界：前者零程式門檻但擴充"
        "受限，後者以少量程式碼換取整合深度；題目給的人力線索（具基礎程式"
        "概念）就是指向後者的訊號。第二，讀清楚題幹的資源條件：人力極少時"
        "排除傳統開發，需求高度客製時排除不可調整的套裝軟體。"
    ),
    "references": [
        exam_ref(29),
        guide_ref("第三章 3-2：No Code 以拖曳元件設計介面與流程；Low Code 結合視覺化開發與程式碼擴充"),
        guide_ref("第三章 3-2：Low Code 平台適合需要深度整合與複雜邏輯的中大型企業應用"),
    ],
}

DRAFTS[30] = {
    "summary": "正確答案是 B。少樣本學習的主要特徵是以少量任務示例引導模型適應新情境或新分類，而不需重新蒐集大規模標註資料。",
    "concept": (
        "少樣本學習（Few-shot Learning）要解決的正是「每類範例有限」的困境："
        "讓模型憑少量示例就能適應新任務或新類別。在大型語言模型的脈絡中，"
        "GPT-3 論文把它具體化為提示中的示範——把幾組輸入輸出範例直接放進"
        "提示，模型不需梯度更新或微調，就能從示範歸納出任務形式並套用到新的"
        "輸入上。\n"
        "以本題的垃圾分類查詢系統為例：每種分類只要準備少量「物品名稱 → "
        "分類」的示例，模型便能依樣判斷新物品的歸屬；日後新增分類時，補上"
        "該類的幾個示例即可適應，不必為每一類蒐集大規模標註資料重新訓練。"
        "相對的概念是零樣本（Zero-shot，完全不給示例）與傳統監督式學習"
        "（依賴大量標註資料）。"
    ),
    "answerReason": (
        "題幹點明「每種分類的訓練範例有限」，工程師因此選用少樣本學習。B 所述"
        "「透過少量任務示例，引導模型適應新情境或新分類需求」正是這項技術的"
        "定義與價值：以極少的示例定錨任務，讓模型把既有能力遷移到新分類上，"
        "與題目情境一一對應，因此為正確答案。"
    ),
    "optionAnalysis": {
        "A": (
            "需重新蒐集大規模標註資料是傳統監督式訓練的路徑，用於從頭訓練或"
            "大幅更新模型。少樣本學習的立足點恰好相反——正因大規模標註昂貴"
            "或不可得，才以少量示例引導模型，本敘述與該技術要解決的問題背道"
            "而馳。"
        ),
        "B": (
            "正確。少樣本學習以少量任務示例讓模型掌握新任務的形式與判斷依據，"
            "在提示式用法中甚至不需更新模型權重；垃圾分類系統只要為每類準備"
            "幾個示例，即可引導模型適應新增的分類需求，正是其主要特徵。"
        ),
        "C": (
            "不需任何範例即可完成新任務推論，描述的是零樣本學習（Zero-shot "
            "Learning）：只憑任務指令作答。它與少樣本學習的差別就在示例的"
            "有無，把「少量示例」說成「零示例」，等於把兩個相鄰但不同的設定"
            "混為一談。"
        ),
        "D": (
            "少樣本學習並非僅適用於自然語言處理。少樣本影像分類長期是機器"
            "學習的研究主題，早期元學習方法多以影像資料集為實驗場景；多模態"
            "模型也能以少量圖文示例適應新任務，因此「對其他模態效果有限」的"
            "限定並不成立。"
        ),
    },
    "trap": (
        "第一，分清 Zero-shot、Few-shot 與傳統監督式學習的差別：零示例、少量"
        "示例、大量標註是三個不同的資料需求層級，選項 A 與 C 各站在 Few-shot "
        "的兩個反面。第二，別把技術與單一領域綁死：少樣本學習廣泛應用於影像"
        "等多種模態，不是自然語言處理專屬。"
    ),
    "references": [
        exam_ref(30),
        {
            "title": "arXiv－Language Models are Few-Shot Learners",
            "url": "https://arxiv.org/abs/2005.14165",
            "locator": "以提示中的少量示範讓模型執行新任務，不需梯度更新或微調",
            "checkedAt": REUSED_CHECKED_AT,
        },
        guide_ref("第三章 3-21 預訓練與模型微調技術：少樣本學習和提示工程提升了模型的適應性與精準度"),
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
