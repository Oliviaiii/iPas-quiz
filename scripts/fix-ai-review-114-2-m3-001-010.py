"""Guarded draft explanation fixes from independent AI review, Q5 and Q6 references.

The cited PMLR URL returns 404 (the paper is not in PMLR v9). It is replaced by
the Deep Learning book chapter 9, whose §9.2 states the same claim verbatim.
This script preserves explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-114-intermediate-2-machine-learning"
TARGETS = {
    5: ("aiap-intermediate-114-02-machine-learning-005", ["A"], "89dc1ab174cfc4e2a48c6b8fa8144fa76b3753c58e75cfc2ed3e07611f58ebc4"),
    6: ("aiap-intermediate-114-02-machine-learning-006", ["C"], "e990b6000cba900a0f7886edfe864ef49ccfb313bc65173f589322d6c84ec31a"),
}

DEAD_URL = "https://proceedings.mlr.press/v9/le-cun10a.html"

NEW_REFERENCE_5 = {
    "title": "Deep Learning（Goodfellow, Bengio, Courville）－Chapter 9 Convolutional Networks",
    "url": "https://www.deeplearningbook.org/contents/convnets.html",
    "locator": "§9.2 Motivation：Convolution leverages three important ideas…sparse interactions, parameter sharing and equivariant representations；並說明 kernel 遠小於輸入時可偵測邊緣等有意義的小型特徵",
    "checkedAt": "2026-08-30",
}

NEW_REFERENCE_6 = {
    "title": "Deep Learning（Goodfellow, Bengio, Courville）－Chapter 9 Convolutional Networks",
    "url": "https://www.deeplearningbook.org/contents/convnets.html",
    "locator": "§9.2 Motivation：sparse interactions 使參數量與執行時間由 m×n 降為 k×n 與 O(k×n)，parameter sharing 讓同一組權重用於輸入的每個位置",
    "checkedAt": "2026-08-30",
}


def snapshot_hash(question: dict) -> str:
    snapshot = {key: question[key] for key in ("id", "officialAnswer", "explanationStatus", "explanation")}
    payload = json.dumps(snapshot, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    selected = {
        q["officialQuestionNumber"]: q
        for q in questions
        if q.get("sourceId") == SOURCE_ID and q.get("officialQuestionNumber") in TARGETS
    }
    if set(selected) != set(TARGETS):
        raise RuntimeError(f"Expected targets {sorted(TARGETS)}, found {sorted(selected)}")
    for number, (question_id, answer, digest) in TARGETS.items():
        question = selected[number]
        if question.get("id") != question_id or question.get("officialAnswer") != answer:
            raise RuntimeError(f"Guard failed for Q{number} identity or answer")
        if question.get("explanationStatus") != "draft" or snapshot_hash(question) != digest:
            raise RuntimeError(f"Guard failed for Q{number} status or reviewed snapshot")

    for number, replacement in ((5, NEW_REFERENCE_5), (6, NEW_REFERENCE_6)):
        references = selected[number]["explanation"]["references"]
        if len(references) != 2 or references[1]["url"] != DEAD_URL:
            raise RuntimeError(f"Guard failed for Q{number} reference snapshot")
        references[1] = replacement

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
