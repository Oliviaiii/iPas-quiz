"""Validate independent-AI review batch reports without marking human review complete.

Usage::

    python scripts/validate-ai-review-reports.py reviews/ai-independent/*.json
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RESULTS = {"pass", "corrected", "human-decision", "blocked"}


def main() -> None:
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    by_id = {question["id"]: question for question in questions}
    problems: list[str] = []
    total = 0

    for arg in sys.argv[1:]:
        path = Path(arg)
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            problems.append(f"{path.name}: invalid JSON: {exc}")
            continue

        source_id = report.get("sourceId")
        batch_range = report.get("range", {})
        start = batch_range.get("start")
        end = batch_range.get("end")
        items = report.get("items")
        if report.get("schemaVersion") != 1:
            problems.append(f"{path.name}: schemaVersion must be 1")
        if report.get("reviewType") != "independent-ai":
            problems.append(f"{path.name}: reviewType must be independent-ai")
        if not source_id or not isinstance(start, int) or not isinstance(end, int):
            problems.append(f"{path.name}: invalid sourceId/range")
            continue
        if end - start != 9:
            problems.append(f"{path.name}: range must contain exactly 10 questions")
        if not DATE_RE.match(str(report.get("reviewedAt", ""))):
            problems.append(f"{path.name}: invalid reviewedAt")
        if not report.get("reviewer"):
            problems.append(f"{path.name}: missing reviewer")
        if not isinstance(items, list) or len(items) != 10:
            problems.append(f"{path.name}: items must contain exactly 10 entries")
            continue

        expected_numbers = list(range(start, end + 1))
        actual_numbers = [item.get("officialQuestionNumber") for item in items]
        if actual_numbers != expected_numbers:
            problems.append(
                f"{path.name}: question numbers {actual_numbers} != {expected_numbers}"
            )

        actual_counts = {
            "pass": 0,
            "corrected": 0,
            "humanDecision": 0,
            "blocked": 0,
        }
        for item in items:
            total += 1
            tag = f"{path.name} Q{item.get('officialQuestionNumber')}"
            question = by_id.get(item.get("questionId"))
            if question is None:
                problems.append(f"{tag}: questionId not found")
                continue
            if question.get("sourceId") != source_id:
                problems.append(f"{tag}: sourceId mismatch")
            if question.get("officialQuestionNumber") != item.get("officialQuestionNumber"):
                problems.append(f"{tag}: officialQuestionNumber mismatch")
            actual_answer = question.get("officialAnswer", [None])[0]
            if item.get("officialAnswer") != actual_answer:
                problems.append(f"{tag}: officialAnswer mismatch")
            if not isinstance(item.get("answerIndependentlyConfirmed"), bool):
                problems.append(f"{tag}: answerIndependentlyConfirmed must be boolean")

            result = item.get("result")
            if result not in RESULTS:
                problems.append(f"{tag}: invalid result {result}")
            elif result == "human-decision":
                actual_counts["humanDecision"] += 1
            else:
                actual_counts[result] += 1

            findings = item.get("findings")
            if not isinstance(findings, list):
                problems.append(f"{tag}: findings must be an array")
            elif result != "pass" and not findings:
                problems.append(f"{tag}: non-pass result requires findings")

            sources = item.get("sourcesChecked")
            if not isinstance(sources, list) or not sources:
                problems.append(f"{tag}: sourcesChecked must be non-empty")
            else:
                for index, source in enumerate(sources):
                    if not str(source.get("url", "")).startswith("https://"):
                        problems.append(f"{tag}: source {index} URL must use https")
                    if not source.get("title") or not source.get("locator"):
                        problems.append(f"{tag}: source {index} missing title/locator")
                    if not DATE_RE.match(str(source.get("checkedAt", ""))):
                        problems.append(f"{tag}: source {index} invalid checkedAt")

        if report.get("counts") != actual_counts:
            problems.append(
                f"{path.name}: counts {report.get('counts')} != {actual_counts}"
            )

    print(f"checked {total} reviewed questions across {len(sys.argv) - 1} reports")
    if problems:
        print(f"{len(problems)} problem(s):")
        for problem in problems:
            print(" -", problem)
        raise SystemExit(1)
    print("all clear")


if __name__ == "__main__":
    main()
