"""Guarded draft explanation fix from independent AI review, Q25 reference.

The cited SAS conference paper URL now returns 404. It is replaced by the
OptBinning documentation, which documents the same scorecard pipeline
(binning → WoE → Information Value → logistic regression → PSI monitoring).
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
    25: ("aiap-intermediate-114-02-machine-learning-025", ["A"], "1db683329146fddb934b24deb19cd90a85c12938197c1f97a5f4326feaa6b00e"),
}

DEAD_URL = "https://support.sas.com/resources/papers/proceedings16/2340-2016.pdf"

NEW_REFERENCES_25 = [
    {
        "title": "OptBinning Documentation－Binning tables",
        "url": "https://gnpalencia.org/optbinning/binning_tables.html",
        "locator": "analysis() 說明 Statistical analysis of the binning table, computing the statistics Gini index, Information Value (IV), Jensen-Shannon divergence；property iv 為 The Information Value (IV) or Jeffrey's divergence measure；plot() 的 metric=\"woe\" 顯示 Weight of Evidence",
        "checkedAt": "2026-08-30",
    },
    {
        "title": "OptBinning Documentation－Scorecard",
        "url": "https://gnpalencia.org/optbinning/scorecard.html",
        "locator": "Scorecard(binning_process, estimator, scaling_method…) 說明 Scorecard development given a binary or continuous target dtype，範例以 BinningProcess 搭配 LogisticRegression 建卡；ScorecardMonitoring 另以 psi_method 監控分數分布",
        "checkedAt": "2026-08-30",
    },
]


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

    references = selected[25]["explanation"]["references"]
    if len(references) != 3 or references[1]["url"] != DEAD_URL:
        raise RuntimeError("Guard failed for Q25 reference snapshot")
    references[1:2] = NEW_REFERENCES_25

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
