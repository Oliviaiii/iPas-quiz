"""Guarded draft reference fix from independent AI review, Q13.

The cited Milvus documentation URL redirects indefinitely (curl exhausts 50
redirects; the docs site is unreachable from a plain client regardless of user
agent), so the locator cannot be resolved there. It is replaced by the FAISS
paper, whose abstract states the same claim about indexing high-dimensional
features for similarity search.
This script preserves explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-intermediate-1-big-data"
TARGETS = {
    13: ("aiap-intermediate-115-01-big-data-013", ["B"], "cc2792a2dceda9645cc6f6379141f433abef146c2259546e0e87113754df43a5"),
}

DEAD_URL = "https://milvus.io/docs/index-explained.md"

NEW_REFERENCE_13 = {
    "title": "Billion-scale similarity search with GPUs（Johnson, Douze & Jégou, FAISS, 2017）",
    "url": "https://arxiv.org/abs/1702.08734",
    "locator": "摘要：Similarity search finds application in specialized database systems handling complex data such as images or videos, which are typically represented by high-dimensional features and require specific indexing structures；並比較 brute-force、approximate 與 compressed-domain search 的取捨",
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

    references = selected[13]["explanation"]["references"]
    if len(references) != 4 or references[3]["url"] != DEAD_URL:
        raise RuntimeError("Guard failed for Q13 reference snapshot")
    references[3] = NEW_REFERENCE_13

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
