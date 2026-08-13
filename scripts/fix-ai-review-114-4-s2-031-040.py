"""Guarded draft explanation fixes from independent AI review, Q31 and Q37.

This script is intentionally not run by the reviewer. It removes an absolute
privacy guarantee from Q31 and distinguishes data drift from its possible
performance impact in Q37. Exact text guards keep the edits narrow and retain
explanationStatus draft.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-114-elementary-4-genai-planning"
CHECKED_AT = "2026-08-13"

EXPECTED = {
    31: {
        "id": "aiap-elementary-114-04-genai-planning-031",
        "answer": ["B"],
        "concept": (
            "個人資料保護法第 5 條要求，蒐集、處理或利用個人資料不得逾越特定目的之必要"
            "範圍。落到技術面就是兩個動作：資料最小化，只提供完成客服任務真正需要的欄位；"
            "去識別化，把姓名、身分證號、聯絡方式等識別資訊移除或替換。\n官方學習指引也"
            "把資料隱私與安全性列為生成式 AI 的主要挑戰，指出敏感資料洩漏風險與個資法"
            "（GDPR、CCPA）的合規風險，解方包含資料加密、匿名化與權限控管。這些手段的"
            "效果強弱不同：模型手上根本沒有敏感個資，就沒有在回覆中洩漏的可能，這是最"
            "徹底的一層。"
        ),
        "reference_count": 3,
    },
    37: {
        "id": "aiap-elementary-114-04-genai-planning-037",
        "answer": ["A"],
        "concept": (
            "官方學習指引在模型監控與重新訓練的段落指出，應定期檢查數據漂移（Data Drift），"
            "分析輸入數據的分佈變化；當業務場景或用戶行為改變時，數據漂移可能導致模型預測"
            "準確性降低，企業須及時更新訓練資料集。\n由此可整理出資料漂移的三個要素：發生"
            "在部署之後、比較的對象是輸入資料的統計分布、後果是效能隨時間衰退。要注意的是，"
            "模型本身沒有變，改變的是它所面對的真實世界。"
        ),
        "answer_reason": (
            "A 明確寫出訓練時的資料分佈與部署後實際輸入資料的統計特徵隨時間逐漸出現差異，"
            "並導致模型表現衰退，三個要素齊備，與學習指引對數據漂移的描述一致，因此選 A。"
        ),
        "option_a": (
            "正確。訓練分布與線上輸入分布之間隨時間拉開差距，模型仍以舊分布的規律推論，"
            "準確度便逐步下滑；因應方式是持續監控輸入分布並在觸發警戒值時重新訓練，正是"
            "學習指引所述的處理流程。"
        ),
        "trap": (
            "第一，用「什麼在變」來分辨：資料漂移是外界輸入分布在變，過擬合是模型從一開始"
            "就學偏，結構變更是上游欄位定義在變。第二，資料漂移是上線後才顯現的漸進現象，"
            "訓練階段的驗證分數看不出來。"
        ),
        "reference_count": 3,
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
            raise RuntimeError(f"Q{number} explanation is missing")

        if number == 31:
            require(explanation.get("concept"), guard["concept"], "Q31 concept")
            explanation["concept"] = (
                "個人資料保護法第 5 條要求，蒐集、處理或利用個人資料不得逾越特定目的之必要"
                "範圍。技術上應先做資料最小化，只提供完成客服任務真正需要的欄位；再依資料"
                "型態採適當去識別化，處理直接識別碼與可能組合識別個人的準識別碼。\n官方學習"
                "指引也把資料隱私與安全性列為生成式 AI 的主要挑戰，解方包含加密、匿名化與"
                "權限控管。資料最小化與去識別化能從源頭降低暴露面，所以 B 是最佳選項；但"
                "去除姓名或遮罩欄位不等於風險歸零。NIST 指引要求評估再識別風險，並指出"
                "即使資料已去識別化仍可能殘留隱私風險，因此仍須搭配存取控管、輸出審核與"
                "持續監測。"
            )
            add_reference(
                explanation,
                {
                    "title": "NIST SP 800-188－De-Identifying Government Datasets",
                    "url": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-188.pdf",
                    "locator": (
                        "摘要、3.2 與 4.3.12：去識別化用於降低揭露風險，但須評估再識別可能，"
                        "且去識別化資料仍可能殘留隱私風險或發生失敗"
                    ),
                    "checkedAt": CHECKED_AT,
                },
                guard["reference_count"],
            )
        elif number == 37:
            require(explanation.get("concept"), guard["concept"], "Q37 concept")
            require(
                explanation.get("answerReason"),
                guard["answer_reason"],
                "Q37 answer reason",
            )
            options = explanation.get("optionAnalysis")
            if not isinstance(options, dict):
                raise RuntimeError("Q37 option analysis is missing")
            require(options.get("A"), guard["option_a"], "Q37 option A")
            require(explanation.get("trap"), guard["trap"], "Q37 trap")
            explanation["concept"] = (
                "資料漂移描述資料分布的變化。Google Model Monitoring 進一步區分："
                "training-serving skew 是正式環境特徵分布偏離訓練資料；inference drift 是"
                "正式環境的特徵分布隨時間顯著改變。兩者都可透過比較統計分布及距離分數監測。\n"
                "漂移可能造成模型表現衰退，因此應同步監測輸入分布與業務效能；但效能下降不是"
                "漂移成立的必要條件。有些分布變化未必影響模型使用的決策邊界，反之概念漂移也"
                "可能在輸入邊際分布不明顯改變時傷害效能。"
            )
            explanation["answerReason"] = (
                "A 是四個選項中唯一描述訓練資料與部署後輸入資料統計分布產生差異的選項，"
                "因此符合本題所稱資料漂移；題目附帶的模型表現衰退是可能後果，不是定義資料"
                "漂移不可缺少的判準。"
            )
            options["A"] = (
                "正確。訓練分布與部署後輸入分布出現差距符合本題的資料漂移描述。這種差距"
                "可能使準確度下降，所以實務上需同時監測特徵分布與模型效能，再依影響決定"
                "是否更新資料或重新訓練；不能只由漂移指標推定效能必然下降。"
            )
            explanation["trap"] = (
                "第一，用「什麼在變」來分辨：資料漂移是輸入分布改變，過擬合是模型從訓練"
                "階段就泛化不足，結構變更是資料管線契約不一致。第二，漂移可漸進也可突然"
                "發生，且分布改變與效能下降應分別量測，不能把後者當成前者的必要定義。"
            )
            add_reference(
                explanation,
                {
                    "title": "Google Cloud－Introduction to Model Monitoring",
                    "url": "https://cloud.google.com/vertex-ai/docs/model-monitoring/overview",
                    "locator": (
                        "Model Monitoring v1：training-serving skew 為正式環境分布偏離訓練"
                        "分布；inference drift 為正式環境特徵分布隨時間顯著改變"
                    ),
                    "checkedAt": CHECKED_AT,
                },
                guard["reference_count"],
            )

        question["explanationStatus"] = "draft"

    QUESTIONS.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
