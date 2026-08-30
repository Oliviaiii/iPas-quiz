"""Guarded draft reference fix from independent AI review, Q21.

The cited PyTorch quantization recipe URL now returns HTTP 404 (the page was
removed when the tutorials site was reorganised, and the stable docs
quantization page renders its body client-side so it cannot be verified).
It is replaced by the ONNX Runtime quantization guide, which states the
FP32 → 8-bit mapping in fetchable text.
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
    21: ("aiap-intermediate-115-01-machine-learning-021", ["D"], "2b86edfdf42dc140adcea6a9714295a01a0c928fa73e41ff5fe2702b6f06e61d"),
}

DEAD_URL = "https://docs.pytorch.org/tutorials/recipes/quantization.html"

NEW_REFERENCE_21 = {
    "title": "ONNX Runtime Documentation－Quantization",
    "url": "https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html",
    "locator": "Quantization Overview：Quantization in ONNX Runtime refers to 8 bit linear quantization of an ONNX model. During quantization, the floating point values are mapped to an 8 bit quantization space；並區分 post-training quantization 與 quantization-aware training",
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

    references = selected[21]["explanation"]["references"]
    if len(references) != 3 or references[1]["url"] != DEAD_URL:
        raise RuntimeError("Guard failed for Q21 reference snapshot")
    references[1] = NEW_REFERENCE_21

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
