"""Guarded draft reference-locator fixes from independent AI review, Q31–Q37.

Those seven questions carry no figure in the bank and none on the official PDF,
yet their locator claims 「附圖」. Each locator is replaced by the precise page
reference. This script preserves explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-114-intermediate-2-machine-learning"
TARGETS = {
    31: ("aiap-intermediate-114-02-machine-learning-031", ["B"], "be14ab5df5689c720b101c0d0c79e9726e70ec6137e6a2a8b5ca26db384431a2"),
    32: ("aiap-intermediate-114-02-machine-learning-032", ["D"], "be5f108f593e60611b1172664993f26fc83af10334ad4344dc3e10f5821b8465"),
    33: ("aiap-intermediate-114-02-machine-learning-033", ["B"], "45ad09bf5a5431fd37ed1ea44ce34760ac0d374ff65fe80346ed0d279dc3691c"),
    34: ("aiap-intermediate-114-02-machine-learning-034", ["D"], "d4e4c4b2783831b4a1a847984689b15f8ced95c41d420aeb1f4f2a743c88691c"),
    35: ("aiap-intermediate-114-02-machine-learning-035", ["A"], "9ae9bc28625a4119bae6f6a06111a05103c2f705e75f7376190b19b9c8a35460"),
    36: ("aiap-intermediate-114-02-machine-learning-036", ["D"], "da983cd1f685af571b71735444a854e002be258b19ac6e68d464147a63fb54d6"),
    37: ("aiap-intermediate-114-02-machine-learning-037", ["B"], "e5b58ec2b233730d69b790120db2b48b2ea2138652d1d14b099a391f8af665ae"),
}

NEW_LOCATORS = {
    31: "PDF 第 7～8 頁：第 31 題題幹與左欄官方答案 B（第 7 頁）、(A)～(D) 選項（第 8 頁）；本題無附圖",
    32: "PDF 第 8 頁：第 32 題題幹、(A)～(D) 選項與左欄官方答案 D；本題無附圖",
    33: "PDF 第 8 頁：第 33 題題幹、(A)～(D) 選項與左欄官方答案 B；本題無附圖",
    34: "PDF 第 8～9 頁：第 34 題題幹與左欄官方答案 D（第 8 頁）、(A)～(D) 選項（第 9 頁）；本題無附圖",
    35: "PDF 第 9 頁：第 35 題題幹（λ1=6.0、λ2=3.0、λ3=1.0）、(A)～(D) 選項與左欄官方答案 A；本題無附圖",
    36: "PDF 第 9 頁：第 36 題題幹、(A)～(D) 選項與左欄官方答案 D；本題無附圖",
    37: "PDF 第 9～10 頁：第 37 題題幹與 (A)(B) 選項、左欄官方答案 B（第 9 頁）、(C)(D) 選項（第 10 頁）；本題無附圖",
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
        if question.get("figures"):
            raise RuntimeError(f"Guard failed for Q{number}: expected no figures")

    for number, locator in NEW_LOCATORS.items():
        reference = selected[number]["explanation"]["references"][0]
        if reference["locator"] != f"第 {number} 題題幹、選項、附圖與官方答案":
            raise RuntimeError(f"Guard failed for Q{number} locator snapshot")
        reference["locator"] = locator
        reference["checkedAt"] = "2026-08-30"

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
