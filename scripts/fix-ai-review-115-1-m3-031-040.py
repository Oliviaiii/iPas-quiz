"""Guarded draft reference fix from independent AI review, Q36.

The cited Microsoft SEAL GitHub page returns HTTP 403 to every request from
this environment (with or without a browser user agent), so its locator cannot
be verified. It is replaced by the HomomorphicEncryption.org introduction,
which states the same property in fetchable text.
This script preserves explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-intermediate-1-machine-learning"
TARGETS = {
    36: ("aiap-intermediate-115-01-machine-learning-036", ["B"], "e3a052bbb1a83d9efd76746888793eddce786214121b414b66922e346c36668d"),
}

BLOCKED_URL = "https://github.com/microsoft/SEAL"

NEW_REFERENCE_36 = {
    "title": "HomomorphicEncryption.org－Introduction to Homomorphic Encryption",
    "url": "https://homomorphicencryption.org/introduction/",
    "locator": "定義段：同態加密允許直接對加密資料進行運算 without requiring access to a secret key；The result of such a computation remains in encrypted form, and can at a later point be revealed by the owner of the secret key",
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

    references = selected[36]["explanation"]["references"]
    if len(references) != 2 or references[1]["url"] != BLOCKED_URL:
        raise RuntimeError("Guard failed for Q36 reference snapshot")
    references[1] = NEW_REFERENCE_36

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
