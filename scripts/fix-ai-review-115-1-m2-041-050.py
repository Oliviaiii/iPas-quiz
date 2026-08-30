"""Guarded draft reference fix from independent AI review, Q45.

The cited pandas GroupBy.sum URL under the old ``pandas.core.groupby`` path now
returns HTTP 404; pandas moved these pages to ``pandas.api.typing``. Because the
question groups a single Series (``df.groupby('CustomerID')['Revenue']``), the
replacement points at SeriesGroupBy.sum.
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
    45: ("aiap-intermediate-115-01-big-data-045", ["C"], "e19e0ba1b5028299bc237c5319e27a492f207a815fcc868d8419228e2b68af42"),
}

DEAD_URL = "https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.sum.html"

NEW_REFERENCE_45 = {
    "title": "pandas API－SeriesGroupBy.sum",
    "url": "https://pandas.pydata.org/docs/reference/api/pandas.api.typing.SeriesGroupBy.sum.html",
    "locator": "方法說明：Compute sum of group values；df.groupby('CustomerID')['Revenue'] 取得 SeriesGroupBy 後呼叫 sum() 即得各客戶營收總和",
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

    references = selected[45]["explanation"]["references"]
    if len(references) != 3 or references[1]["url"] != DEAD_URL:
        raise RuntimeError("Guard failed for Q45 reference snapshot")
    references[1] = NEW_REFERENCE_45

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
