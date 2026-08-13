"""Draft guarded explanation fixes from independent AI review, Q2/Q5/Q6/Q8/Q10.

This script is intentionally not run by the reviewer. It qualifies unsupported
generalizations, repairs one contradictory option analysis, adds the missing
exam-time OpenAI source, and preserves explanationStatus as draft.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-elementary-1-genai-planning"
CHECKED_AT = "2026-08-13"

EXPECTED = {
    2: {
        "id": "aiap-elementary-115-01-genai-planning-002",
        "answer": ["D"],
        "option_c": (
            "梯度凍結（Gradient Freezing）是把部分層整層凍結、不回傳梯度，常見於遷移學習"
            "的分層凍結策略，確實能減少更新量；但未凍結的層仍是整層全量更新，粒度粗、"
            "彈性低，降低參數量的幅度與維持效能的能力都遠不及以極少量新增參數逼近全微調"
            "效果的 LoRA。"
        ),
        "reference_count": 3,
    },
    5: {
        "id": "aiap-elementary-115-01-genai-planning-005",
        "answer": ["C"],
        "option_c": (
            "正確。自注意力讓模型同時看見整段輸入的所有位置，長距離依賴不隨距離衰減；"
            "自迴歸生成每一步都以完整前文為條件，回覆得以連貫一致。客服自動回覆與內部"
            "文件摘要正是這類模型的典型應用。"
        ),
        "reference_count": 3,
    },
    6: {
        "id": "aiap-elementary-115-01-genai-planning-006",
        "answer": ["D"],
        "editorial_note": (
            "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目："
            "OpenAI 官方 Sora 系統卡與說明中心頁面（openai.com、help.openai.com）於本日"
            "以 WebFetch 嘗試開啟均回應 403，Sora 出處工具三項細節與「未提供對外實時驗證"
            "介面」的判斷僅依官方公告試題題幹與 C2PA 公開資訊撰寫，尚缺 OpenAI 一手出處，"
            "待複核補查。查核日期 2026-08-03。"
        ),
        "reference_count": 2,
    },
    8: {
        "id": "aiap-elementary-115-01-genai-planning-008",
        "answer": ["D"],
        "option_c": (
            "雲端部署的延遲主要來自用戶端與資料中心之間的網路往返，就地執行的邊緣部署"
            "正是為了縮短這段距離；說「雲端通常比邊緣更容易出現延遲」把兩者的相對關係"
            "講反，也解釋不了題幹中雲端反而順暢的觀察。"
        ),
        "reference_count": 3,
    },
    10: {
        "id": "aiap-elementary-115-01-genai-planning-010",
        "answer": ["D"],
        "concept": (
            "知識蒸餾（Knowledge Distillation）由大型教師模型先產生輸出（例如各類別的機率"
            "分布或生成內容），再訓練參數量較小的學生模型模仿這些輸出。原始論文提出這個"
            "方法，正是為了把準確但笨重、部署成本高的模型壓縮成可大量部署的輕量模型。\n"
            "在檢索增強生成（RAG）系統中，成本與延遲的大宗通常是負責閱讀檢索片段並生成"
            "回覆的大型模型，檢索索引本身相對便宜。把生成端蒸餾成小模型後，推論算力與"
            "記憶體需求下降、延遲縮短；學生模型因為模仿教師行為，在內部知識查詢這類範圍"
            "明確的任務上仍能維持可接受的品質。學習指引也把模型壓縮與量化列為降低生成式"
            " AI 計算與儲存需求的方向，知識蒸餾屬於同一類輕量化思路。"
        ),
        "trap": (
            "第一，分清 RAG 各環節的成本來源：檢索相對便宜、生成昂貴，優化推論成本要對"
            "生成端下手。第二，知識蒸餾的「知識」指教師模型的行為分布，不是把文件知識"
            "改寫成規則，兩者不能混為一談。"
        ),
        "reference_count": 4,
    },
}


def require(value: object, expected: object, label: str) -> None:
    if value != expected:
        raise RuntimeError(f"Guard failed for {label}")


def add_reference(explanation: dict, reference: dict, expected_count: int) -> None:
    references = explanation.get("references")
    if not isinstance(references, list) or len(references) != expected_count:
        raise RuntimeError("Reference list changed from the reviewed snapshot")
    if any(item.get("url") == reference["url"] for item in references):
        raise RuntimeError(f"Reference already exists: {reference['url']}")
    references.append(reference)


def main() -> None:
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    targets = {
        question["officialQuestionNumber"]: question
        for question in questions
        if question.get("sourceId") == SOURCE_ID
        and question.get("officialQuestionNumber") in EXPECTED
    }
    if set(targets) != set(EXPECTED):
        raise RuntimeError(f"Target question set changed: {sorted(targets)}")

    for number, guard in EXPECTED.items():
        question = targets[number]
        require(question.get("id"), guard["id"], f"Q{number} id")
        require(question.get("officialAnswer"), guard["answer"], f"Q{number} answer")
        require(question.get("explanationStatus"), "draft", f"Q{number} status")
        explanation = question.get("explanation")
        if not isinstance(explanation, dict):
            raise RuntimeError(f"Q{number}: explanation is missing")
        options = explanation.get("optionAnalysis")
        if not isinstance(options, dict):
            raise RuntimeError(f"Q{number}: option analysis is missing")
        references = explanation.get("references")
        if not isinstance(references, list) or len(references) != guard["reference_count"]:
            raise RuntimeError(f"Q{number}: reference list changed")

        if number == 2:
            require(options.get("C"), guard["option_c"], "Q2 option C")
            options["C"] = (
                "梯度凍結可減少更新參數與反向傳播成本，成效取決於凍結哪些層、任務與模型；"
                "不能普遍斷言其效能一定遠低於 LoRA。本題仍選 D，因 LoRA 是題目所列選項中"
                "明確以低秩更新大幅縮減可訓練參數、且專為參數高效微調設計的方法。"
            )
        elif number == 5:
            require(options.get("C"), guard["option_c"], "Q5 option C")
            options["C"] = (
                "正確。自注意力可讓脈絡視窗內各位置直接建立關聯，縮短長距離資訊傳遞的"
                "路徑；自迴歸生成則依已生成前文逐詞預測，使回覆具連貫性。這些能力不等於"
                "長距離資訊永不衰減，實際表現仍受脈絡長度、注意力分配與模型能力影響。"
            )
        elif number == 6:
            require(
                explanation.get("editorialNote"),
                guard["editorial_note"],
                "Q6 editorial note",
            )
            add_reference(
                explanation,
                {
                    "title": "OpenAI－Sora 2 System Card: Provenance and Transparency Initiatives",
                    "url": (
                        "https://deploymentsafety.openai.com/sora-2/"
                        "provenance-and-transparency-initiatives"
                    ),
                    "locator": (
                        "考試時點前已列出所有資產的 C2PA、可見移動浮水印，以及辨識產品所生"
                        "影片或音訊的內部工具；未列對外即時驗證介面"
                    ),
                    "checkedAt": CHECKED_AT,
                },
                guard["reference_count"],
            )
            explanation["editorialNote"] = (
                "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。OpenAI 於"
                "考試時點前發布的 Sora 2 System Card 已支持 A～C 所述三層機制，故官方答案"
                " D 可由一手來源確認。現況註記：OpenAI 後續頁面標示 Sora 產品已於 2026-04-26"
                " 停止提供；本題仍依 2026-03-21 考試時點判讀。查核日期 2026-08-13。"
            )
        elif number == 8:
            require(options.get("C"), guard["option_c"], "Q8 option C")
            options["C"] = (
                "雲端因網路往返而可能比就近處理的邊緣部署有更高傳輸延遲，所以此句在一般"
                "網路情境下可能成立，不能說它把相對關係講反；但它無法解釋本題實際觀察到的"
                "「雲端順暢、邊緣變慢」。題目要找的是邊緣端資源受限造成的運算延遲，故 C"
                " 不是本題答案。"
            )
        elif number == 10:
            require(explanation.get("concept"), guard["concept"], "Q10 concept")
            require(explanation.get("trap"), guard["trap"], "Q10 trap")
            explanation["concept"] = (
                "知識蒸餾（Knowledge Distillation）由大型教師模型提供輸出訊號，再訓練較小"
                "的學生模型模仿教師行為，目標是以較輕量的模型保留所需能力。\n在 RAG 系統"
                "中，檢索、重排序、提示長度與生成模型都可能影響成本及延遲，不能普遍認定"
                "檢索一定便宜、生成一定是主要瓶頸。若量測確認生成模型是本題情境的優化目標，"
                "將其蒸餾為較小學生模型可降低該環節的推論資源需求；品質是否維持仍須以任務"
                "評估驗證。"
            )
            explanation["trap"] = (
                "第一，知識蒸餾是讓學生模型學習教師模型行為，不是把文件改寫成規則。第二，"
                "RAG 各環節的成本占比須經量測判定；本題已指定採用蒸餾，因此重點是辨識 D"
                " 對蒸餾方法的正確描述，而非假設所有系統都由生成端主導成本。"
            )

        question["explanationStatus"] = "draft"

    QUESTIONS.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
