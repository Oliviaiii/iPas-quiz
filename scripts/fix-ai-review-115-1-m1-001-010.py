"""Guarded draft reference fix from independent AI review, Q8.

The cited NIST Dataplot page now 301-redirects to the NIST ITL landing page,
so the locator no longer resolves to any sensitivity/specificity text. It is
replaced by the scikit-learn roc_curve API page, which states the same claim.
This script preserves explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-intermediate-1-ai-tech-planning"
TARGETS = {
    8: ("aiap-intermediate-115-01-ai-tech-planning-008", ["B"], "e33120014b49fbde76d5582d057ff2207ce46c4a349106e98b723516d296e02d"),
}

DEAD_URL = "https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/sensitiv.htm"

NEW_REFERENCE_8 = {
    "title": "scikit-learn API－sklearn.metrics.roc_curve",
    "url": "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html",
    "locator": "Returns 段：fpr 為 Increasing false positive rates…、tpr 為 Increasing true positive rates…，各元素對應 thresholds[i]，說明 ROC 由多個判定門檻的 FPR／TPR 組成",
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

    references = selected[8]["explanation"]["references"]
    if len(references) != 3 or references[2]["url"] != DEAD_URL:
        raise RuntimeError("Guard failed for Q8 reference snapshot")
    references[2] = NEW_REFERENCE_8

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
