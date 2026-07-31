"""Write the phase-two explanation drafts for 114-4 elementary subject two, Q1-Q10.

Same guarantees as the subject-one batches: only fills ``explanation`` on
questions that already exist, aborts if an official answer no longer matches
the answer a draft was written against, and refuses to overwrite reviewed work.

Every cited URL was opened and checked on the date recorded in ``checkedAt``.

Usage::

    python scripts/write-explanations-114-4-s2-001-010.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-114-elementary-4-genai-planning"
AUTHOR = "Claude Code（AI 輔助初稿）"
AUTHORED_AT = "2026-07-31"
CHECKED_AT = "2026-07-31"

EXAM_PDF = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/114年第四梯次初級AI應用規劃師第二科"
    "生成式AI應用與規劃(當次試題公告114_20251226000507.pdf"
)
GUIDE_PDF = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/AI應用規劃師(初級)-學習指引-科目2_"
    "生成式AI應用與規劃114123_20251222172159.pdf"
)
DEFAULT_NOTE = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"


def exam_ref(number: int) -> dict:
    return {
        "title": "114 年第四次初級 AI 應用規劃師－生成式 AI 應用與規劃公告試題",
        "url": EXAM_PDF,
        "locator": f"第 {number} 題題幹、選項與官方答案",
        "checkedAt": CHECKED_AT,
    }


def guide_ref(locator: str) -> dict:
    return {
        "title": "iPAS AI 應用規劃師（初級）學習指引－科目二 生成式 AI 應用與規劃",
        "url": GUIDE_PDF,
        "locator": locator,
        "checkedAt": CHECKED_AT,
    }


EXPECTED_ANSWER = {
    1: "B", 2: "D", 3: "B", 4: "A", 5: "D",
    6: "B", 7: "C", 8: "C", 9: "B", 10: "B",
}

DRAFTS: dict[int, dict] = {}

DRAFTS[1] = {
    "summary": "正確答案是 B。模型是抽象描述資料結構、業務流程與介面邏輯的核心元素。",
    "concept": (
        "官方學習指引說明，No Code 平台透過拖曳元件設計介面並設定邏輯與流程，"
        "Low Code 平台則在視覺化開發的基礎上，讓開發者以少量程式碼實現深度整合"
        "與複雜邏輯。\n"
        "在這類平台上，「模型」不是畫面上的裝飾，而是整個應用的骨架：它定義了"
        "資料有哪些欄位與關聯、業務流程如何流轉、介面元件綁定到哪些資料。"
        "因為視覺化操作最終都要落到模型上，模型設計得好不好，會直接決定應用"
        "後續好不好維護、能不能擴充。"
    ),
    "answerReason": (
        "題目問哪個敘述「最符合實際情況」。B 指出模型用來抽象描述資料結構、"
        "業務流程與介面邏輯，並影響應用的設計與維護，準確描述了模型在 Low Code"
        "平台中的核心地位，因此選 B。"
    ),
    "optionAnalysis": {
        "A": (
            "把模型窄化成視覺化的輔助工具，低估了它的角色。模型定義的資料結構"
            "與流程會被整個應用引用，一旦設計不當，後續新增功能或修改流程都會"
            "受制於它，影響絕不只限於畫面呈現。"
        ),
        "B": (
            "正確。模型抽象描述資料結構、業務流程與介面邏輯，是平台上各種視覺化"
            "設定最終依附的基礎；模型設計的品質直接反映在應用的可維護性與"
            "可擴充性上。"
        ),
        "C": (
            "UML 是傳統軟體工程常用的建模語言，但 Low Code 平台的模型通常是"
            "平台自訂的中繼資料格式，可直接驅動介面生成與流程執行，並支援"
            "拖曳設定與即時預覽。說它缺乏針對 Low Code 環境的延展性，與這類"
            "平台以模型驅動開發的實際運作方式不符。"
        ),
        "D": (
            "自動程式碼生成是把模型轉換成可執行成品的手段，前提是先有模型可"
            "依循，兩者是上下游關係而非取代關係。若模型描述有誤，生成出來的"
            "程式碼同樣會是錯的，因此模型的價值並未被削弱。"
        ),
    },
    "trap": (
        "第一，Low Code 平台的核心是模型驅動開發，視覺化與程式碼生成都是圍繞"
        "模型展開的手段。第二，看到「僅」、「已被全面取代」、「價值有限」這類"
        "弱化語氣的敘述，通常是要被排除的選項。"
    ),
    "references": [
        exam_ref(1),
        guide_ref("第三章 3-2：No Code 以拖曳元件設計介面與流程；Low Code 結合視覺化開發與程式碼擴充"),
    ],
}

DRAFTS[2] = {
    "summary": "正確答案是 D。聯邦學習讓分散的敏感資料留在原處，模型仍能持續優化。",
    "concept": (
        "題目的條件有三個：資料分散在不同部門或機構、資料屬於敏感文本、"
        "而且模型要能「持續優化」。能同時滿足這三點的，是改變訓練架構而非"
        "只加強資料保護。\n"
        "聯邦學習的作法是讓各方在本地用自己的資料訓練，只把模型參數或梯度更新"
        "送出彙整成全域模型，再下發繼續訓練。原始文本自始至終不離開持有方，"
        "但每一方的知識都反映在同一個模型裡，因此可以持續迭代優化。"
    ),
    "answerReason": (
        "四個選項都是隱私相關技術，但只有聯邦學習直接回答了「資料不集中要如何"
        "共同訓練並持續優化模型」這個問題，其餘三者著重在運算或驗證過程中的"
        "保密，因此選 D。"
    ),
    "optionAnalysis": {
        "A": (
            "同態加密允許在密文狀態下直接進行運算，運算結果解密後與明文運算"
            "相同，適合把運算外包給不可信環境。但完全同態運算的計算成本極高，"
            "用於大型模型的反覆訓練並不實際，它處理的也是「運算過程保密」"
            "而非「資料分散如何協同訓練」。"
        ),
        "B": (
            "安全多方計算讓多方在不揭露各自輸入的前提下共同計算出一個結果，"
            "適合聯合統計或聯合查詢這類明確定義的計算任務。它常被拿來與聯邦"
            "學習搭配以強化聚合階段的保密性，但本身並未提供模型持續迭代訓練"
            "的整體架構。"
        ),
        "C": (
            "零知識證明讓證明方在不透露內容的情況下，使驗證方相信某個陳述為真，"
            "典型用途是身分或資格驗證、區塊鏈交易驗證。它解決的是「如何證明」，"
            "與讓模型從分散資料中學習無關。"
        ),
        "D": (
            "正確。各部門或機構在本地訓練、只上傳模型更新，中央彙整為全域模型"
            "後再下發，原始敏感文本不外流，模型卻能持續吸收各方資料而優化，"
            "完全對應題目的三個條件。"
        ),
    },
    "trap": (
        "第一，區分「保護運算或驗證過程」（同態加密、安全多方計算、零知識證明）"
        "與「改變訓練架構讓資料不必集中」（聯邦學習）。第二，題目若強調模型要"
        "持續優化，就要找能支撐反覆訓練的方案，而不是單次計算的保密技術。"
    ),
    "references": [
        exam_ref(2),
        {
            "title": "arXiv－Communication-Efficient Learning of Deep Networks from Decentralized Data",
            "url": "https://arxiv.org/abs/1602.05629",
            "locator": "聯邦學習原始論文：資料保留在裝置端，僅交換模型更新",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[3] = {
    "summary": "正確答案是 B。導入可重複執行的自動化測試，並以 API 或服務虛擬化做模組化驗證。",
    "concept": (
        "可測試性指的是系統能否被有效、可重複地驗證。當系統牽涉跨部門流程與"
        "外部服務整合時，兩個困難會浮現：一是流程長、分支多，靠人工點按無法"
        "窮盡；二是外部服務可能不穩定、有額度限制或無法在測試環境呼叫。\n"
        "自動化測試解決第一個問題：測試可重複執行，每次改動都能回歸驗證。"
        "服務虛擬化（以模擬的服務替身回應請求）解決第二個問題：讓測試不必"
        "依賴真實外部系統，也能穩定重現各種回應情境，包括錯誤與逾時。"
    ),
    "answerReason": (
        "B 同時處理了題目點出的兩個難處：可重複執行的自動化測試對應跨部門的"
        "長流程，API 與服務虛擬化對應外部服務整合，且是模組化驗證而非只看表面，"
        "因此選 B。"
    ),
    "optionAnalysis": {
        "A": (
            "平台內建的即時預覽與基本單元測試適合開發途中快速確認單一元件，"
            "屬於必要但不充分的手段。它通常無法涵蓋跨部門的完整流程，也難以"
            "模擬外部服務的各種回應，對題目描述的整合情境覆蓋不足。"
        ),
        "B": (
            "正確。可重複執行的自動化測試讓每次改動都能回歸驗證；透過 API 測試"
            "與服務虛擬化，可在不依賴真實外部系統的情況下穩定重現各種情境，"
            "並以模組為單位定位問題，是提升可測試性的正規作法。"
        ),
        "C": (
            "只驗證使用者介面互動與操作流程，測的是系統表面。介面測試容易因"
            "版面調整而失效，且無法檢查資料在跨部門流程中是否正確流轉，"
            "更看不到與外部服務往來的細節，覆蓋深度不足。"
        ),
        "D": (
            "依靠使用者回饋與上線後監控屬於事後偵錯。監控在正式環境確實必要，"
            "但把它當成主要驗證手段，等於讓使用者承擔缺陷風險，缺陷發現得晚、"
            "修復成本也高，與「確保可測試性」的目標背道而馳。"
        ),
    },
    "trap": (
        "第一，可測試性強調的是「可重複、可自動、可定位」，凡是仰賴人工或事後"
        "才發現問題的作法都不符合。第二，外部服務整合的測試關鍵在於能不能"
        "脫離真實服務仍穩定重現情境，這正是服務虛擬化的用途。"
    ),
    "references": [
        exam_ref(3),
        guide_ref("第三章 3-2：Low Code 平台適合需要深度整合與複雜邏輯的中大型企業應用"),
    ],
}

DRAFTS[4] = {
    "summary": "正確答案是 A。把圖結構轉成文字提示時，部分關聯資訊可能在轉換中遺失。",
    "concept": (
        "社交互動資料的本質是圖：節點是使用者，邊是互動關係，還帶有方向、"
        "強度與時間等屬性。語言模型的輸入卻是線性的文字序列。\n"
        "圖提示要把圖結構描述成文字，這個轉換必然要做取捨：先寫哪個節點、"
        "如何表達環狀或多重路徑、要不要保留所有邊的權重。序列化過程中，"
        "全域的拓撲結構（例如某個節點是否為關鍵樞紐）往往最容易被稀釋，"
        "這正是這類方法最典型的挑戰。"
    ),
    "answerReason": (
        "A 指出圖結構轉換為文字提示時可能導致部分關聯資訊遺失，這是圖與序列"
        "兩種資料型態之間本就存在的落差，也是實務上最常遇到的問題，因此選 A。"
    ),
    "optionAnalysis": {
        "A": (
            "正確。圖是非線性的結構，文字提示是線性序列；序列化時必須決定順序"
            "與取捨，節點間的多重路徑、環狀關係與全域拓撲特徵容易在描述過程中"
            "被壓縮或遺漏，導致模型推理時缺少關鍵脈絡。"
        ),
        "B": (
            "自動提示工程的作法是讓模型產生候選提示、依評分挑選較佳者，"
            "只要能把圖資料描述成文字，它就能產生提示內容。說它在圖資料上"
            "完全無法產生提示，與其運作方式不符。"
        ),
        "C": (
            "說法過於樂觀，也與選項 A 直接矛盾。實務上正因為轉換無法完整保留"
            "所有上下文，才需要設計描述方式（例如挑選子圖、加入節點摘要）"
            "來緩解資訊損失，這個選項等於否定了問題的存在。"
        ),
        "D": (
            "圖提示可以描述樹狀或多分支結構，並非只能處理線性路徑；許多應用"
            "正是用它來表達複雜的多跳關係。真正的限制不在於能不能表達分支，"
            "而在於表達得夠不夠完整。"
        ),
    },
    "trap": (
        "第一，凡是把非線性結構（圖、表格、程式）轉成文字餵給語言模型，"
        "都要先想到「轉換過程會遺失什麼」。第二，選項中出現「完整保留所有」、"
        "「無法產生任何」這類絕對敘述時，通常可以優先排除。"
    ),
    "references": [
        exam_ref(4),
        {
            "title": "arXiv－Large Language Models Are Human-Level Prompt Engineers",
            "url": "https://arxiv.org/abs/2211.01910",
            "locator": "自動提示工程（APE）以模型產生並評分候選提示的方法",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[5] = {
    "summary": "正確答案是 D。回饋機制多半只針對局部片段，難以全面評估超長輸出的整體品質。",
    "concept": (
        "自動提示工程的運作邏輯是：產生候選提示、用某個評分機制衡量效果、"
        "依分數挑選並反覆迭代。整套流程的品質，取決於那個評分機制是否可靠。\n"
        "在超長上下文任務中，輸出可能長達數千字，評估往往只能抽取片段或用"
        "局部指標計分。這會造成優化目標與真正想要的品質脫節：提示被調整成"
        "在被評估的片段上表現良好，但整體的一致性、結構完整度與跨段落的"
        "邏輯連貫卻沒有被衡量，也因此無法被有效優化。"
    ),
    "answerReason": (
        "題目問「最大限制」。D 指出回饋機制通常僅針對局部片段，難以全面評估"
        "最終輸出品質，直指自動提示工程賴以運作的評分環節在超長任務下失準，"
        "是最根本的限制，因此選 D。"
    ),
    "optionAnalysis": {
        "A": (
            "上下文變動確實會使既有提示需要重新調整，但這比較接近應用情境的"
            "動態性問題，可透過重新迭代來因應。它並未觸及自動提示工程本身"
            "賴以運作的評分環節，不是最根本的限制。"
        ),
        "B": (
            "模型的上下文長度限制是語言模型本身的屬性，會影響所有長文本任務，"
            "並非自動提示工程特有的問題。題目問的是使用 APE 時面臨的限制，"
            "這個選項描述的是承載模型的共通條件。"
        ),
        "C": (
            "提示分解與任務拆解是可行的技術方向，實務上也常以分段處理搭配"
            "結果彙整來因應長任務。說提示內容難以有效分解、無法支援複雜任務"
            "拆解，低估了現行作法的彈性。"
        ),
        "D": (
            "正確。自動提示工程依賴回饋分數來挑選與迭代提示；當輸出過長而評估"
            "只能覆蓋局部片段時，優化方向會偏離整體品質，導致提示看似改善、"
            "全篇表現卻未提升，這是它在超長上下文任務中最核心的限制。"
        ),
    },
    "trap": (
        "第一，判斷自動化優化方法的限制時，先問「它的評分依據可靠嗎」，"
        "評估失準會使整個迭代失去意義。第二，要區分語言模型本身的限制"
        "（上下文長度）與特定方法的限制（回饋覆蓋不足）。"
    ),
    "references": [
        exam_ref(5),
        {
            "title": "arXiv－Large Language Models Are Human-Level Prompt Engineers",
            "url": "https://arxiv.org/abs/2211.01910",
            "locator": "APE 以評分函數挑選候選提示並迭代優化的流程",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[6] = {
    "summary": "正確答案是 B。以生成式 AI 自動建立介面模板，並結合使用者數據即時產生個人化功能與行銷內容。",
    "concept": (
        "官方學習指引列出生成式 AI 強化 No Code 與 Low Code 平台的具體方式，"
        "其中包含模板設計優化（AI 提供設計建議，快速完成介面設計與互動流程）、"
        "自動化行銷文案生成（輸入產品資訊即時產出行銷內容），以及個人化 App"
        "快速開發（透過用戶數據分析生成符合需求的應用，實現個人化體驗與快速"
        "部署）。\n"
        "題目的三個需求——高度個人化體驗、快速生成介面、行銷內容自動產出——"
        "正好對應上述三項，因此要找的是能同時涵蓋這三者的整合策略。"
    ),
    "answerReason": (
        "B 一次涵蓋三個需求：自動建立介面模板對應快速生成介面，結合使用者數據"
        "生成個人化功能對應個人化體驗，即時產生行銷推播對應行銷內容自動產出，"
        "且仍在 No Code 平台的框架內運作，因此選 B。"
    ),
    "optionAnalysis": {
        "A": (
            "以 AI 產生 API 呼叫與元件配置、再由開發者手動整合，確實可行，"
            "但手動整合這一步會成為瓶頸，與題目「短時間內完成」的前提衝突；"
            "而且這個作法沒有提到個人化體驗與行銷內容產出，只覆蓋了部分需求。"
        ),
        "B": (
            "正確。自動建立介面模板加快了開發，結合使用者數據即時生成個人化"
            "功能與行銷推播內容則同時滿足個人化與行銷需求，三個目標一次到位，"
            "與學習指引所列的模板設計優化、個人化 App 快速開發及自動化行銷"
            "文案生成三項應用相符。"
        ),
        "C": (
            "建立跨專案可重用的通用模組有助於長期的開發效率，是良好的工程實務，"
            "但重點放在「通用」與「重用」，與本題要求的高度個人化方向相反，"
            "也沒有處理行銷內容自動產出的需求。"
        ),
        "D": (
            "完全依賴 AI 產生所有功能與流程且不經人工設計或驗證，風險過高。"
            "生成內容可能有錯誤、遺漏或不符合業務規則，缺少人為把關等於把"
            "品質完全交給機率，任何正式上線的應用都不應採取這種作法。"
        ),
    },
    "trap": (
        "第一，題目列出多個需求時，要挑能同時覆蓋所有需求的選項，只滿足其中"
        "一項的通常不是答案。第二，凡是主張「完全依賴 AI、不經人工驗證」的"
        "選項，在應用規劃題中幾乎都是錯的。"
    ),
    "references": [
        exam_ref(6),
        guide_ref("第三章 3-2：生成式 AI 強化 No Code / Low Code 的應用，含模板設計優化、自動化行銷文案生成與個人化 App 快速開發"),
    ],
}

DRAFTS[7] = {
    "summary": "正確答案是 C。流程為 AI Host 發起、經 MCP Client 連到 MCP Server 查詢，再把結果回傳 Host。",
    "concept": (
        "Model Context Protocol 採用主從式架構，三個角色的關係是固定的：\n"
        "AI Host 是使用模型的應用程式本體，需要外部資料或工具時由它發動；"
        "MCP Client 存在於 Host 之中，負責與伺服器建立並維持連線，"
        "一個 Client 對應一個 Server；MCP Server 則是實際提供資料或工具能力的"
        "一方，例如連接 GitHub 程式碼庫的伺服器。\n"
        "因此請求一定是由內而外：Host 發起，Client 傳遞，Server 執行，"
        "結果再沿原路回到 Host 交給模型使用。"
    ),
    "answerReason": (
        "題目描述 AI 先發出請求、再經 MCP 架構逐步完成查詢與回傳。依照上述"
        "角色關係，順序是 AI Host → MCP Client → MCP Server → 資料查詢 →"
        "結果回傳 AI Host，與 C 完全一致。"
    ),
    "optionAnalysis": {
        "A": (
            "以 MCP Server 作為起點並不成立。Server 是被動提供能力的一方，"
            "等待來自 Client 的請求，不會主動去驅動 Host；而且此順序把 Host"
            "排在 Client 之前之外，也顛倒了 Client 內嵌於 Host 的從屬關係。"
        ),
        "B": (
            "把 MCP Client 排在 AI Host 之前，顛倒了兩者的包含關係。Client 是"
            "由 Host 建立並管理的連線元件，不會先於 Host 存在或自行發起流程。"
        ),
        "C": (
            "正確。Host 因任務需要而發起請求，交由其內部的 MCP Client 送往"
            "對應的 MCP Server，Server 完成資料查詢後將結果沿原路回傳給 Host，"
            "再由模型據以生成摘要。"
        ),
        "D": (
            "順序中把 MCP Server 排在 MCP Client 之前，等於讓 Host 先接觸"
            "Server 再經過 Client，與架構定義不符。Client 的角色正是 Host 與"
            "Server 之間的連線代理，不能被跳過或後置。"
        ),
    },
    "trap": (
        "第一，記住從屬關係：Client 內嵌於 Host，Server 在外部；請求永遠"
        "由內而外，回應原路返回。第二，Server 是被動提供能力者，任何以 Server"
        "為起點的流程都可以先排除。"
    ),
    "references": [
        exam_ref(7),
        {
            "title": "Model Context Protocol－Architecture overview",
            "url": "https://modelcontextprotocol.io/specification/2025-06-18/architecture",
            "locator": "Host、Client 與 Server 的角色定義與主從式連線關係",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[8] = {
    "summary": "正確答案是 C。Client Agent 發起任務，Remote Agent 執行後把結果回傳。",
    "concept": (
        "Agent-to-Agent 架構處理的是多個代理人如何互相委派工作。角色分工以"
        "「誰發起」為判準：Client Agent 是需求方，負責把任務描述出來並送出；"
        "Remote Agent 是能力提供方，接到任務後在自己的環境中執行，"
        "再把結果回傳給發起者。\n"
        "這種設計讓各代理人可以專精不同能力，需求方不必知道對方內部如何實作，"
        "只需依約定的介面提出任務與接收結果，因此能跨系統、跨組織組合能力。"
    ),
    "answerReason": (
        "C 描述 Client Agent 發起任務、Remote Agent 執行並回傳結果，"
        "符合這套架構中需求方與能力提供方的基本分工，因此選 C。"
    ),
    "optionAnalysis": {
        "A": (
            "方向相反。Remote Agent 是被委派的一方，等待任務上門；由它主動"
            "分派任務給 Client Agent，等於把需求方與執行方的角色對調，"
            "不符合架構中以發起者定義 Client 的原則。"
        ),
        "B": (
            "由人工事先設定處理順序，等於回到固定流程的編排，失去了代理人之間"
            "動態協商與委派的意義。這套架構的價值正在於任務可依需要即時發起，"
            "而不是預先寫死執行次序。"
        ),
        "C": (
            "正確。Client Agent 作為需求方提出任務，Remote Agent 作為能力提供方"
            "接手執行並回傳結果，雙方透過約定的介面互動，需求方不需了解對方的"
            "內部實作。"
        ),
        "D": (
            "同時處理並同步結果描述的是平行運算的協調模式。此架構的基本互動是"
            "委派與回覆，具有明確的先後關係；雖然一個 Client 可以同時委派多個"
            "任務，但那是多組委派並行，不是雙方同步處理同一件任務。"
        ),
    },
    "trap": (
        "第一，以「誰發起」判斷角色：發起者是 Client，執行者是 Remote，"
        "名稱中的 Client 與 Server 概念一致。第二，代理人架構強調動態委派，"
        "凡是強調人工預先排定順序的選項通常不符合。"
    ),
    "references": [
        exam_ref(8),
        {
            "title": "A2A Protocol－官方文件",
            "url": "https://a2a-protocol.org/latest/",
            "locator": "Client Agent 與 Remote Agent 的角色定義與任務委派流程",
            "checkedAt": CHECKED_AT,
        },
    ],
}

DRAFTS[9] = {
    "summary": "正確答案是 B。上下文工程的核心目的是優化提示與上下文。",
    "concept": (
        "上下文工程處理的問題是：在模型權重固定的前提下，要餵給模型什麼內容、"
        "以什麼順序與結構呈現，才能得到最好的輸出。\n"
        "它涵蓋的範圍比單純寫提示詞更廣，包括系統指令的設計、對話歷史要保留"
        "多少、檢索到的文件如何篩選與排序、範例要放幾個放在哪裡、以及在有限的"
        "上下文長度內如何取捨。共同點是：全部作用在「輸入」這一側，不改動"
        "模型參數，因此成本低、迭代快。"
    ),
    "answerReason": (
        "四個選項中，只有 B 描述的是對輸入端的提示與上下文進行優化；"
        "其餘三項分別指向訓練時間、模型規模與微調，都涉及模型本身而非輸入內容，"
        "因此選 B。"
    ),
    "optionAnalysis": {
        "A": (
            "縮短模型訓練時間屬於訓練階段的效率課題，作法包括調整批量大小、"
            "使用混合精度或分散式訓練。上下文工程是在模型訓練完成後才介入，"
            "不影響訓練所需的時間。"
        ),
        "B": (
            "正確。上下文工程透過設計系統指令、篩選與排序檢索內容、安排範例與"
            "對話歷史，在不改動模型參數的前提下提升輸出品質，重點正是優化提示"
            "與上下文本身。"
        ),
        "C": (
            "增加模型參數數量是改變模型架構與規模的決定，屬於模型設計與訓練的"
            "範疇，需要重新訓練並付出可觀的運算成本。上下文工程恰好是在不動"
            "模型的前提下改善效果的手段。"
        ),
        "D": (
            "優化微調正確率涉及以特定資料再訓練模型並更新權重，屬於模型調整。"
            "它與上下文工程是兩條互補但不同的路徑：一條改模型，一條改輸入；"
            "上下文工程的優勢正在於不必動到權重。"
        ),
    },
    "trap": (
        "第一，用「有沒有改動模型權重」來區分：改權重的是訓練或微調，"
        "不改權重而調整輸入的是上下文工程。第二，上下文工程不只是寫提示詞，"
        "還包含檢索內容的篩選、排序與長度取捨。"
    ),
    "references": [
        exam_ref(9),
        guide_ref("第三章 3-18：生成式 AI 具備上下文理解能力，並可透過提示詞進行可控生成"),
    ],
}

DRAFTS[10] = {
    "summary": "正確答案是 B。面對互相矛盾的上下文，模型最常見的行為是產生幻覺或隨機採信其中一方。",
    "concept": (
        "生成式模型的運作方式是依據前文，在訓練所建立的文字機率分布中選出最"
        "可能接續的內容。它並不具備獨立的事實查核能力，也沒有可靠的機制判斷"
        "兩段互相矛盾的敘述誰才正確。\n"
        "因此當上下文自相矛盾時，模型仍會照常生成流暢的回應：可能採用其中一"
        "方、可能在不同段落前後不一致，也可能把兩者折衷成一個根本不存在於輸入"
        "中的說法。官方學習指引把 AI 幻覺列為生成式 AI 實際應用時必須防範的"
        "主要挑戰之一。"
    ),
    "answerReason": (
        "模型沒有事實判斷能力，卻仍傾向產生完整流暢的輸出，結果就是在矛盾"
        "資訊中隨機採信一方，或生成輸入中並不存在的內容。B 準確描述了這個"
        "行為，因此選 B。"
    ),
    "optionAnalysis": {
        "A": (
            "模型並沒有「一律採用第一段」這樣的固定規則。位置確實可能影響"
            "注意力分配，但那是傾向而非保證，也會隨提示寫法、上下文長度與"
            "模型版本而變。把它說成永遠如此過於絕對。"
        ),
        "B": (
            "正確。模型缺乏事實查核能力，面對矛盾輸入時仍會生成流暢回應，"
            "可能任選一方、前後不一致，或折衷出輸入中沒有的說法，也就是幻覺。"
            "這正是學習指引所列的生成式 AI 主要挑戰之一。"
        ),
        "C": (
            "拒絕回答並要求釐清是理想中的謹慎行為，但預設情況下模型傾向完成"
            "任務而非中止。除非在系統指令中明確要求遇到矛盾時必須提出釐清，"
            "否則不能期待它主動這麼做。"
        ),
        "D": (
            "自動判斷哪一方正確需要外部事實依據。模型只能看到輸入中的兩段"
            "矛盾敘述，兩者在文本層面都同樣「合理」，它沒有任何依據能可靠地"
            "分辨真偽，因此無法保證選到正確的那一個。"
        ),
    },
    "trap": (
        "第一，模型輸出流暢不代表內容正確；矛盾輸入通常換來看似合理卻不可靠的"
        "回應。第二，若希望模型遇到矛盾時提出釐清，必須在提示或系統指令中"
        "明確要求，並在流程上加入人工複核，不能仰賴預設行為。"
    ),
    "references": [
        exam_ref(10),
        guide_ref("第三章 3-18：生成式 AI 的挑戰包含輸出內容準確性保證與 AI 幻覺問題的防範"),
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
