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
    point is to keep the vocabulary and add the plain words around it. The one
    exemption is ``TYPO_FIXES``: run-together typos in the source text that were
    later split with a space, and only when the corrected spelling is present.

``numbers``
    Every number in the original must still appear: in these analyses the
    numbers are claims — article numbers, thresholds, percentages, layer counts.

``applied``
    The bank holds either the payload's rewrite (already applied) or exactly the
    text the payload recorded as the original (not yet applied). Anything else
    means the payload and the bank have diverged.

``zh-terms``
    ``terms`` only sees Latin script, so a Chinese term swapped for a plain
    paraphrase slips through. This closes that gap using the curated glossary in
    ``content/glossary-zh.json``: a glossary term present in a question's
    pre-rewrite text must still be findable somewhere in that question's
    explanation afterwards. The scope is the question, not the field — a term
    the reader still meets in the same question has not been lost. The glossary
    carries accepted spelling variants, terms excluded for being ambiguous, and
    per-site exemptions, each with its reason.

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
GLOSSARY = ROOT / "content" / "glossary-zh.json"

TERM = re.compile(r"[A-Za-z][A-Za-z0-9]*(?:[-_.][A-Za-z0-9]+)*")
NUMBER = re.compile(r"\d+(?:[.,]\d+)*")
# Latin fragments that carry no meaning on their own.
NOISE = {"a", "an", "and", "as", "at", "by", "for", "in", "of", "on", "or", "the", "to", "vs", "with"}

# 原稿裡把兩個英文字連在一起的排版錯字。白話化時照原樣重現，之後由
# ``scripts/fix-runtogether-typos.py`` 補上空格，所以原文的連寫 token 必然
# 「消失」。這不是掉字，條件是改寫後確實出現補了空格的正確寫法——只有這樣
# 才豁免，寫錯成別的東西一樣會被抓出來。
TYPO_FIXES = {
    "constrow": "const row",
    "ExperimentTracking": "Experiment Tracking",
    "LateFusion": "Late Fusion",
    "rollingfeatures": "rolling features",
    "rankcorrelations": "rank correlations",
}


def tokens(text: str, pattern: re.Pattern[str]) -> set[str]:
    return {match.group(0) for match in pattern.finditer(text)}


def explanation_text(question: dict) -> str:
    """一題解說的全文——四個欄位加上摘要，合起來當作讀者實際看得到的內容。"""
    explanation = question["explanation"]
    parts = [explanation.get(field) or "" for field in ("summary", "concept", "answerReason", "trap")]
    parts += list(explanation["optionAnalysis"].values())
    return "\n".join(parts)


def check_zh_terms(questions: dict[str, dict], originals: dict[str, list[str]]) -> list[str]:
    """術語在改寫前的原文出現過，改寫後就必須在同一題裡仍找得到。"""
    glossary = json.loads(GLOSSARY.read_text(encoding="utf-8"))
    terms: dict[str, list[str]] = glossary["terms"]
    exempt = {
        (e["sourceId"], e["question"], e["term"]) for e in glossary["exemptions"]
    }

    problems: list[str] = []
    for question_id, old_texts in sorted(originals.items()):
        question = questions.get(question_id)
        if question is None:
            continue
        before = "\n".join(old_texts)
        after = explanation_text(question)
        key = (question["sourceId"], question["officialQuestionNumber"])
        for term, variants in terms.items():
            if term not in before:
                continue
            if any(form in after for form in (term, *variants)):
                continue
            if (*key, term) in exempt:
                continue
            problems.append(
                f"{key[0]} Q{key[1]}: 中文術語「{term}」在改寫後整題都不見了"
            )
    return problems


def main() -> None:
    payloads = [Path(a) for a in sys.argv[1:]] or sorted(PAYLOAD_DIR.glob("*.json"))
    if not payloads:
        raise SystemExit("no payloads found")

    questions = {q["id"]: q for q in json.loads(QUESTIONS.read_text(encoding="utf-8"))}
    problems: list[str] = []
    checked = applied = pending = 0
    # questionId -> 該題所有被改寫欄位的原文，供 zh-terms 檢查使用。
    originals: dict[str, list[str]] = {}

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
                originals.setdefault(item["questionId"], []).append(old)
                current = analysis.get(letter)
                if current == new:
                    applied += 1
                elif current == old:
                    pending += 1
                else:
                    problems.append(f"{tag}: bank text matches neither the payload's old nor its new text")
                lost_terms = {t for t in tokens(old, TERM) if t.lower() not in NOISE} - tokens(new, TERM)
                lost_terms -= {
                    term for term, fixed in TYPO_FIXES.items()
                    if term in lost_terms and fixed in new
                }
                if lost_terms:
                    problems.append(f"{tag}: dropped term(s) {sorted(lost_terms)}")
                lost_numbers = tokens(old, NUMBER) - tokens(new, NUMBER)
                if lost_numbers:
                    problems.append(f"{tag}: dropped number(s) {sorted(lost_numbers)}")

    problems += check_zh_terms(questions, originals)

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
