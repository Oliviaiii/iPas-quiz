"""Guarded draft explanation fix from independent AI review, Q31 reference locator.

This script is intentionally not run by the reviewer afterwards. It updates only
exact reviewed snapshots and preserves explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-114-intermediate-2-big-data"
TARGETS = {
    31: ("aiap-intermediate-114-02-big-data-031", ["B"], "bdd84808ac8d6f8a15d01de1568ded2dd72543a6971c660b4c7c8397ab7121f2"),
}

# NIST/SEMATECH 的二項分佈頁面並未出現 "Bernoulli trial" 字樣，改以該頁實際用語定位。
OLD_LOCATOR_31 = (
    "二項分佈由 n 次 Bernoulli trials 與成功機率 p 定義，平均數 np、標準差 sqrt(np(1-p))"
)
NEW_LOCATOR_31 = (
    "Probability Mass Function 段：two mutually exclusive outcomes、x successes in N trials、"
    "p is fixed for all trials；Common Statistics 表：Mean 為 np、Standard Deviation 為 sqrt(np(1-p))"
)


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

    e31 = selected[31]["explanation"]
    if len(e31["references"]) != 2 or e31["references"][1]["locator"] != OLD_LOCATOR_31:
        raise RuntimeError("Guard failed for Q31 references snapshot")
    e31["references"][1]["locator"] = NEW_LOCATOR_31
    e31["references"][1]["checkedAt"] = "2026-08-30"

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
