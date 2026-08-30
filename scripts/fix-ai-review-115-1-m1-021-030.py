"""Guarded draft reference fix from independent AI review, Q27.

The FDA HTML landing page for the GMLP guiding principles rejects plain
requests (HTTP 401 without a browser user agent) and its body is not
retrievable, so the cited locator could not be resolved there. It is replaced
by the FDA-hosted PDF of the same document, whose Guiding Principle 7 states
the cited text verbatim. This script preserves explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-intermediate-1-ai-tech-planning"
TARGETS = {
    27: ("aiap-intermediate-115-01-ai-tech-planning-027", ["A"], "08c9fe80133574e44ef75afa1017e033191d8cfe6339eac2c414226f400e936e"),
}

OLD_URL = "https://www.fda.gov/medical-devices/software-medical-device-samd/good-machine-learning-practice-medical-device-development-guiding-principles"

NEW_REFERENCE_27 = {
    "title": "FDA、Health Canada 與 MHRA－Good Machine Learning Practice for Medical Device Development: Guiding Principles（2021 年 10 月，PDF）",
    "url": "https://www.fda.gov/media/153486/download",
    "locator": "原則 7 Focus Is Placed on the Performance of the Human-AI Team：Where the model has a \"human in the loop,\" human factors considerations and the human interpretability of the model outputs are addressed with emphasis on the performance of the Human-AI team, rather than just the performance of the model in isolation",
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

    references = selected[27]["explanation"]["references"]
    if len(references) != 3 or references[1]["url"] != OLD_URL:
        raise RuntimeError("Guard failed for Q27 reference snapshot")
    references[1] = NEW_REFERENCE_27

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
