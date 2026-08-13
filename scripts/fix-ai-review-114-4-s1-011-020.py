"""Draft guarded citation fixes from independent AI review, Q11-Q20.

This script is intentionally not run by the reviewer. It only repairs the
reference evidence for Q13, Q18, and Q19, and refuses to proceed if the current
drafts no longer match the reviewed snapshots.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-114-elementary-4-ai-foundation"
CHECKED_AT = "2026-08-13"

GUIDE_TITLE = "iPAS AI 應用規劃師（初級）學習指引－科目一 人工智慧基礎概論"
GUIDE_URL = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/"
    "bf93f438f7be48d295c1b40a34d79f3d/AI應用規劃師(初級)-學習指引-科目1_"
    "人工智慧基礎概論1141203_20251222172144.pdf"
)

EXPECTED = {
    13: {
        "id": "aiap-elementary-114-04-ai-foundation-013",
        "answer": ["D"],
        "reference_count": 2,
        "guide_locator": (
            "第三章 3-13 至 3-14：監督式學習、非監督式學習與強化學習的定義；"
            "強化學習適用於試錯學習與長期規劃，例如自動駕駛"
        ),
    },
    18: {
        "id": "aiap-elementary-114-04-ai-foundation-018",
        "answer": ["C"],
        "reference_count": 2,
        "guide_locator": "第三章 3-13 至 3-14：強化學習的回饋機制與策略最佳化",
    },
    19: {
        "id": "aiap-elementary-114-04-ai-foundation-019",
        "answer": ["A"],
        "reference_count": 2,
        "guide_locator": (
            "第三章 3-11：迴歸模型用於預測房地產價格等連續數值；"
            "3-18 損失函數的作用"
        ),
    },
}


def guide_ref(locator: str) -> dict:
    return {
        "title": GUIDE_TITLE,
        "url": GUIDE_URL,
        "locator": locator,
        "checkedAt": CHECKED_AT,
    }


def find_guide_reference(references: list[dict], expected_locator: str) -> int:
    matches = [
        index
        for index, reference in enumerate(references)
        if reference.get("title") == GUIDE_TITLE
        and reference.get("url") == GUIDE_URL
        and reference.get("locator") == expected_locator
    ]
    if len(matches) != 1:
        raise RuntimeError(
            "Expected exactly one unchanged learning-guide reference with locator "
            f"{expected_locator!r}, found {len(matches)}"
        )
    return matches[0]


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
        if question.get("id") != guard["id"]:
            raise RuntimeError(f"Q{number}: question id changed")
        if question.get("officialAnswer") != guard["answer"]:
            raise RuntimeError(f"Q{number}: official answer changed")
        if question.get("explanationStatus") != "draft":
            raise RuntimeError(f"Q{number}: explanation is no longer draft")

        explanation = question.get("explanation")
        if not isinstance(explanation, dict):
            raise RuntimeError(f"Q{number}: explanation is missing")
        references = explanation.get("references")
        if not isinstance(references, list):
            raise RuntimeError(f"Q{number}: references are missing")
        if len(references) != guard["reference_count"]:
            raise RuntimeError(f"Q{number}: reference count changed")

        guide_index = find_guide_reference(references, guard["guide_locator"])

        if number == 13:
            references.append(
                {
                    "title": "scikit-learn－sklearn.semi_supervised",
                    "url": "https://scikit-learn.org/stable/api/sklearn.semi_supervised.html",
                    "locator": (
                        "Semi-supervised learning algorithms：使用少量有標記資料及"
                        "大量未標記資料進行分類"
                    ),
                    "checkedAt": CHECKED_AT,
                }
            )
        elif number == 18:
            references[guide_index] = guide_ref(
                "第三章 3-38：Q 表的高維限制、DNN 近似 Q 值、Experience Replay "
                "與 Target Network"
            )
            references.append(
                {
                    "title": "Google DeepMind－Deep Reinforcement Learning",
                    "url": "https://deepmind.google/blog/deep-reinforcement-learning/",
                    "locator": (
                        "DQN 以深度神經網路表示 Q-network，並隨機抽樣回放經驗，"
                        "取得多樣且低相關的訓練資料"
                    ),
                    "checkedAt": CHECKED_AT,
                }
            )
        elif number == 19:
            references[guide_index] = guide_ref(
                "第三章 3-11、3-41：房價是連續值迴歸；MSE 用於迴歸並計算"
                "預測值與真實值平方誤差的平均"
            )

        # Independent AI corrections remain AI drafts pending human review.
        question["explanationStatus"] = "draft"

    QUESTIONS.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
