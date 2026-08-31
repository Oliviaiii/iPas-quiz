"""Check plain-language rewrites against the text they replaced.

The apply-time guards catch structural problems — wrong target, dropped 正確
marker, suspicious shrinkage. This checks the thing that actually matters and
cannot be guarded at write time: that the rewrite still *says* what the original
said. Each payload records the replaced text verbatim, so the comparison stays
available long after the change is committed.

Three checks per rewritten option:

``terms``
    Every Latin-script token in the original (``Bias``, ``One-hot``, ``F1``,
    ``Regulatory Sandbox``…) must still appear in the rewrite. A rewrite that
    drops a term has dropped a concept rather than explaining it — the whole
    point is to keep the vocabulary and add the plain words around it.

``numbers``
    Every number in the original must still appear: in these analyses the
    numbers are claims — article numbers, thresholds, percentages, layer counts.

``applied``
    The bank holds either the payload's rewrite (already applied) or exactly the
    text the payload recorded as the original (not yet applied). Anything else
    means the payload and the bank have diverged.

Usage::

    python scripts/check-plain-language.py                 # every payload
    python scripts/check-plain-language.py <payload.json>  # just these
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
PAYLOAD_DIR = ROOT / "content" / "plain-language"

TERM = re.compile(r"[A-Za-z][A-Za-z0-9]*(?:[-_.][A-Za-z0-9]+)*")
NUMBER = re.compile(r"\d+(?:[.,]\d+)*")
# Latin fragments that carry no meaning on their own.
NOISE = {"a", "an", "and", "as", "at", "by", "for", "in", "of", "on", "or", "the", "to", "vs", "with"}


def tokens(text: str, pattern: re.Pattern[str]) -> set[str]:
    return {match.group(0) for match in pattern.finditer(text)}


def main() -> None:
    payloads = [Path(a) for a in sys.argv[1:]] or sorted(PAYLOAD_DIR.glob("*.json"))
    if not payloads:
        raise SystemExit("no payloads found")

    questions = {q["id"]: q for q in json.loads(QUESTIONS.read_text(encoding="utf-8"))}
    problems: list[str] = []
    checked = applied = pending = 0

    for path in payloads:
        payload = json.loads(path.read_text(encoding="utf-8"))
        for item in payload["items"]:
            number = item["officialQuestionNumber"]
            question = questions.get(item["questionId"])
            if question is None:
                problems.append(f"{path.name} Q{number}: questionId not found")
                continue
            prose = "prose" in item
            explanation = question["explanation"]
            analysis = explanation if prose else explanation["optionAnalysis"]
            for letter, entry in item["prose" if prose else "optionAnalysis"].items():
                checked += 1
                tag = f"{path.name} Q{number}{letter}"
                if "old" not in entry:
                    problems.append(f"{tag}: payload has no recorded old text")
                    continue
                old, new = entry["old"], entry["new"]
                current = analysis.get(letter)
                if current == new:
                    applied += 1
                elif current == old:
                    pending += 1
                else:
                    problems.append(f"{tag}: bank text matches neither the payload's old nor its new text")
                lost_terms = {t for t in tokens(old, TERM) if t.lower() not in NOISE} - tokens(new, TERM)
                if lost_terms:
                    problems.append(f"{tag}: dropped term(s) {sorted(lost_terms)}")
                lost_numbers = tokens(old, NUMBER) - tokens(new, NUMBER)
                if lost_numbers:
                    problems.append(f"{tag}: dropped number(s) {sorted(lost_numbers)}")

    print(
        f"checked {checked} rewritten option analyses across {len(payloads)} payload(s) "
        f"— {applied} applied, {pending} pending"
    )
    if problems:
        print(f"{len(problems)} problem(s):")
        for problem in problems:
            print(" -", problem)
        raise SystemExit(1)
    print("all clear")


if __name__ == "__main__":
    main()
