"""Corpus-wide typography sweep: insert the missing space between CJK and Latin.

The explanation prose already follows the convention of separating Han
characters from half-width alphanumerics with a single space — a survey found
17,086 spaced boundaries against 249 unspaced ones. This script normalises the
minority.

Scope is deliberately narrow:

* only the self-authored explanation prose (``summary``, ``concept``,
  ``answerReason``, ``optionAnalysis.A``–``D``, ``trap``, ``editorialNote``);
* ``prompt``, ``options``, ``passage`` and ``figures`` hold official exam text
  and are never touched, and neither are ``references`` (their locators already
  follow the convention);
* boundaries inside an inline ``code span`` or inside an identifier that mixes
  Han characters with an underscore (``星期一_08時``) are left alone;
* one subscript-style formula is exempted explicitly (``w1·L分類``).

The guards make the edit auditable: the corpus digest must match the surveyed
state, the number of inserted spaces must equal the planned count, and — the
important one — stripping every space from the old and new text must yield
identical strings, which proves the script only ever inserts spaces.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"

CJK = r"㐀-䶿一-鿿豈-﫿"
LAT = r"A-Za-z0-9"
BOUNDARY = re.compile(f"(?:[{CJK}][{LAT}])|(?:[{LAT}][{CJK}])")
TOKEN = re.compile(f"[{CJK}{LAT}_]+")
HAN_UNDERSCORE = re.compile(f"[{CJK}]_|_[{CJK}]")
CODE_SPAN = re.compile(r"`[^`]*`")

PROSE_FIELDS = ("summary", "concept", "answerReason", "trap", "editorialNote")

# Digest of the surveyed corpus state, over every question's reviewed snapshot.
CORPUS_DIGEST = "8bd868cc829726b626edc05d551a3b31a45d2fb1d37df90d80ecf18f80b95018"
EXPECTED_INSERTIONS = 246

# Boundaries that must stay unspaced because they are subscript notation.
EXCEPTIONS = {
    ("aiap-intermediate-114-02-ai-tech-planning-047", "concept", "w1·L分類"),
}


def corpus_digest(questions: list[dict]) -> str:
    payload = [
        {key: q[key] for key in ("id", "officialAnswer", "explanationStatus", "explanation")}
        for q in questions
    ]
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def protected_spans(text: str) -> list[tuple[int, int]]:
    spans = [(m.start(), m.end()) for m in CODE_SPAN.finditer(text)]
    for m in TOKEN.finditer(text):
        if "_" in m.group(0) and HAN_UNDERSCORE.search(m.group(0)):
            spans.append((m.start(), m.end()))
    return spans


def add_spaces(question_id: str, field: str, text: str) -> tuple[str, int]:
    spans = protected_spans(text)
    pieces: list[str] = []
    previous = 0
    inserted = 0
    for match in BOUNDARY.finditer(text):
        left = match.start()
        right = left + 1
        if any(a <= left < b or a <= right < b for a, b in spans):
            continue
        window = text[max(0, left - 12):right + 12]
        if any(q == question_id and f == field and needle in window for q, f, needle in EXCEPTIONS):
            continue
        pieces.append(text[previous:right])
        pieces.append(" ")
        previous = right
        inserted += 1
    pieces.append(text[previous:])
    return "".join(pieces), inserted


def prose_of(explanation: dict):
    for field in PROSE_FIELDS:
        if explanation.get(field):
            yield field, explanation[field], lambda value, f=field: explanation.__setitem__(f, value)
    options = explanation.get("optionAnalysis") or {}
    for letter, value in options.items():
        if value:
            yield (
                f"optionAnalysis.{letter}",
                value,
                lambda new, key=letter: options.__setitem__(key, new),
            )


def main() -> None:
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    digest = corpus_digest(questions)
    if digest != CORPUS_DIGEST:
        raise RuntimeError(f"Guard failed: corpus digest {digest} != {CORPUS_DIGEST}")

    total = 0
    touched: set[str] = set()
    for question in questions:
        explanation = question.get("explanation") or {}
        if question.get("explanationStatus") != "draft":
            raise RuntimeError(f"Guard failed: {question['id']} is not draft")
        for field, text, setter in list(prose_of(explanation)):
            new_text, inserted = add_spaces(question["id"], field, text)
            if not inserted:
                continue
            if new_text.replace(" ", "") != text.replace(" ", ""):
                raise RuntimeError(f"Guard failed: {question['id']} {field} changed more than spacing")
            if len(new_text) - len(text) != inserted:
                raise RuntimeError(f"Guard failed: {question['id']} {field} length delta mismatch")
            setter(new_text)
            total += inserted
            touched.add(question["id"])

    if total != EXPECTED_INSERTIONS:
        raise RuntimeError(f"Guard failed: inserted {total} spaces, expected {EXPECTED_INSERTIONS}")

    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"inserted {total} spaces across {len(touched)} questions")


if __name__ == "__main__":
    main()
