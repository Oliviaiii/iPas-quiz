"""Guarded draft explanation fixes from independent AI review, Q4 and Q10.

This script is intentionally not run by the reviewer. It distinguishes
trimming from winsorization and avoids denying the sampling capability of
Bayesian networks. Exact guards keep edits narrow and statuses draft.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-elementary-1-ai-foundation"
CHECKED_AT = "2026-08-13"

EXPECTED = {
    4: {
        "id": "aiap-elementary-115-01-ai-foundation-004",
        "answer": ["C"],
        "option_b": (
            "截尾（Trimming）針對連續型極端值設計，把超出設定分位數的觀測值截斷或剔除，"
            "以降低少數極端點對模型參數的拉扯。它確實會改變尾端的分佈，使用時須控制比例，"
            "但屬於統計上公認的極端值處理手段，與 C 的工具誤用不同層次。"
        ),
        "reference_count": 4,
    },
    10: {
        "id": "aiap-elementary-115-01-ai-foundation-010",
        "answer": ["A"],
        "option_d": (
            "貝氏網路以有向圖描述變數之間的條件依賴關係，用於機率推論與不確定性分析。"
            "官方學習指引在檢核題解析中明確指出，決策樹、線性迴歸與貝氏分類雖是重要的"
            "機器學習方法，但並不擅長生成新的內容；產生高品質圖像仍以 GAN、VAE、擴散"
            "模型等深度生成模型為主。"
        ),
        "reference_count": 5,
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
        options = explanation.get("optionAnalysis")
        if not isinstance(options, dict):
            raise RuntimeError(f"Q{number} option analysis is missing")

        if number == 4:
            require(options.get("B"), guard["option_b"], "Q4 option B")
            options["B"] = (
                "截尾（Trimming）是移除排序後兩端一定比例的觀測值，以降低極端點的影響；"
                "若把尾端值改設為分位數界限，則稱為縮尾或溫莎化（Winsorization），兩者不應"
                "混稱。Trimming 確實會改變樣本與尾端分布，應先驗證極端案件是否真為錯誤並"
                "控制移除比例，但仍是可用的統計處理方式；C 則把類別編碼工具誤用於連續數值"
                "離群值，因而是最不適當選項。"
            )
            add_reference(
                explanation,
                {
                    "title": "NIST/SEMATECH e-Handbook－Measures of Location",
                    "url": "https://itl.nist.gov/div898/handbook/eda/section3/eda351.htm",
                    "locator": (
                        "Trimmed mean 移除兩端一定比例資料；Winsorized mean 不移除，而將"
                        "尾端值設為最低或最高保留界限"
                    ),
                    "checkedAt": CHECKED_AT,
                },
                guard["reference_count"],
            )
        elif number == 10:
            require(options.get("D"), guard["option_d"], "Q10 option D")
            options["D"] = (
                "貝氏網路以有向圖分解變數的聯合機率分布，除了條件推論，也可依該分布進行"
                "前向取樣，因此不能概括說它沒有生成樣本的能力。不過，傳統貝氏網路需要明確"
                "設計節點與條件機率，並非為高維像素及平滑隱空間所設計；在本題要從既有圖像"
                "產生具變化且風格一致的新圖像時，VAE 仍是四個選項中直接且適合的技術。"
            )
            add_reference(
                explanation,
                {
                    "title": "pgmpy Documentation－Bayesian Model Sampling",
                    "url": "https://pgmpy.org/exact_infer/bn_sampling.html",
                    "locator": "BayesianModelSampling.forward_sample：依貝氏網路的聯合分布產生樣本",
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
