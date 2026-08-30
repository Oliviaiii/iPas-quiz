"""Guarded draft reference fix from independent AI review, Q19.

The reference cited arXiv 1606.07659 as a Kohavi A/B-testing paper, but that
arXiv ID is "Hybrid Recommender System based on Autoencoders" (Strub et al.) —
the title and locator do not belong to that URL. It is replaced by Kohavi et
al., "Online Controlled Experiments at Large Scale" (KDD 2013).
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
    19: ("aiap-intermediate-115-01-ai-tech-planning-019", ["A"], "5992f2e9538e0fbdb552f37506e15331d3766ef17d219981e455ac193259fd14"),
}

WRONG_URL = "https://arxiv.org/abs/1606.07659"

NEW_REFERENCE_19 = {
    "title": "Online Controlled Experiments at Large Scale（Kohavi et al., KDD 2013）",
    "url": "https://exp-platform.com/Documents/2013%20controlledExperimentsAtScale.pdf",
    "locator": "§2 案例：使用者被隨機分派至各變體並量測 key metrics；該例的 Overall Evaluation Criterion (OEC) 為 increasing average revenue per user without degrading key user engagement metrics，示範營收上升但使用者互動指標下降時不可逕判成功",
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

    references = selected[19]["explanation"]["references"]
    if len(references) != 3 or references[2]["url"] != WRONG_URL:
        raise RuntimeError("Guard failed for Q19 reference snapshot")
    references[2] = NEW_REFERENCE_19

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
