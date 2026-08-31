"""Apply plain-language rewrites from a payload file.

The explanations were written for readers who already know the vocabulary. This
applies a rewrite that keeps every technical term and every technical claim but
adds the plain-language explanation a non-specialist needs, so the explanation
can be read and remembered without a background in the field.

A payload item carries either ``optionAnalysis`` (keyed by option letter) or
``prose`` (keyed by ``concept`` / ``answerReason``); the two passes live in
separate files so they never contend for the same text.

Usage::

    python scripts/apply-plain-language.py content/plain-language/<sourceId>.json ...

The payload carries, for each option, the sha256 of the exact text it replaces.
Guards, per option:

* the question exists, its id matches and it is still ``draft``;
* the current text hashes to ``oldSha256`` — so a payload can never be applied
  twice, nor to text somebody else has since edited;
* the "正確" prefix may never be dropped, and may only be added to an option the
  official answer actually names — so the rewrite can normalise a missing marker
  without ever moving it onto a wrong option;
* the rewrite is longer than 80% of the original (a plain-language pass adds
  explanation; a large shrink means content was dropped, not reworded).

Nothing outside the named explanation fields is touched: the official stem,
options, answer and the review status all stay exactly as they are.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
LETTERS = ("A", "B", "C", "D")
PROSE_FIELDS = ("concept", "answerReason")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> None:
    paths = [Path(arg) for arg in sys.argv[1:]]
    if not paths:
        raise SystemExit("usage: apply-plain-language.py <payload.json> ...")

    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    by_id = {q["id"]: q for q in questions}
    applied = 0
    touched_questions = 0

    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("schemaVersion") != 1:
            raise RuntimeError(f"{path.name}: schemaVersion must be 1")
        source_id = payload.get("sourceId")
        if not source_id:
            raise RuntimeError(f"{path.name}: missing sourceId")

        for item in payload["items"]:
            number = item["officialQuestionNumber"]
            tag = f"{path.name} Q{number}"
            question = by_id.get(item["questionId"])
            if question is None:
                raise RuntimeError(f"{tag}: questionId not found")
            if question.get("sourceId") != source_id:
                raise RuntimeError(f"{tag}: sourceId mismatch")
            if question.get("officialQuestionNumber") != number:
                raise RuntimeError(f"{tag}: officialQuestionNumber mismatch")
            if question.get("explanationStatus") != "draft":
                raise RuntimeError(f"{tag}: question is not draft")

            if ("optionAnalysis" in item) == ("prose" in item):
                raise RuntimeError(f"{tag}: item must carry exactly one of optionAnalysis / prose")
            prose = "prose" in item
            explanation = question["explanation"]
            target = explanation if prose else explanation["optionAnalysis"]
            for letter, entry in item["prose" if prose else "optionAnalysis"].items():
                if prose:
                    if letter not in PROSE_FIELDS:
                        raise RuntimeError(f"{tag}: bad prose field {letter}")
                elif letter not in LETTERS:
                    raise RuntimeError(f"{tag}: bad option letter {letter}")
                old = target.get(letter)
                if not old:
                    raise RuntimeError(f"{tag} {letter}: no existing text")
                if "old" in entry and entry["old"] != old:
                    raise RuntimeError(f"{tag} {letter}: payload's recorded old text does not match")
                if sha256(old) != entry["oldSha256"]:
                    raise RuntimeError(
                        f"{tag} {letter}: current text hashes to {sha256(old)}, "
                        f"payload expects {entry['oldSha256']}"
                    )
                new = entry["new"]
                if not new.strip():
                    raise RuntimeError(f"{tag} {letter}: empty rewrite")
                if new == old:
                    raise RuntimeError(f"{tag} {letter}: rewrite is identical")
                if old.startswith("正確") and not new.startswith("正確"):
                    raise RuntimeError(f"{tag} {letter}: 正確 marker dropped")
                if (
                    new.startswith("正確")
                    and not old.startswith("正確")
                    and letter not in question["officialAnswer"]
                ):
                    raise RuntimeError(f"{tag} {letter}: 正確 marker added to a non-answer option")
                if len(new) < len(old) * 0.8:
                    raise RuntimeError(
                        f"{tag} {letter}: rewrite is {len(new)} chars against {len(old)} — too short"
                    )
                target[letter] = new
                applied += 1
            touched_questions += 1

    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"rewrote {applied} explanation fields across {touched_questions} questions")


if __name__ == "__main__":
    main()
