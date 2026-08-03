"""Pre-flight validation for write-explanations scripts before applying them.

Imports each script module (``main()`` is guarded, so nothing is written), then
checks every draft against the same constraints ``tests/data.test.mjs``
enforces: expected answer vs. official answer, summary prefix, field length
minimums, complete A-D option analyses, forbidden filler strings, and
reference fields.

Usage::

    python scripts/validate-explanation-drafts.py scripts/write-explanations-115-1-s2-001-010.py [...]
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"

FORBIDDEN = [
    "沒有滿足題幹的關鍵條件",
    "機制或適用情境不同",
    "直接符合題幹設定",
    "也對應",
    "在題幹脈絡下屬於可成立或可採用的描述",
]

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    problems: list[str] = []
    total = 0

    for arg in sys.argv[1:]:
        path = Path(arg)
        try:
            mod = load_module(path)
        except Exception as exc:  # noqa: BLE001
            problems.append(f"{path.name}: IMPORT FAILED: {exc}")
            continue

        source_id = getattr(mod, "SOURCE_ID", None)
        drafts = getattr(mod, "DRAFTS", None)
        expected = getattr(mod, "EXPECTED_ANSWER", None)
        if not source_id or not isinstance(drafts, dict) or not isinstance(expected, dict):
            problems.append(f"{path.name}: missing SOURCE_ID/DRAFTS/EXPECTED_ANSWER")
            continue

        index = {
            q["officialQuestionNumber"]: q
            for q in questions
            if q["sourceId"] == source_id
        }

        for number, draft in sorted(drafts.items()):
            total += 1
            tag = f"{path.name} Q{number}"
            q = index.get(number)
            if q is None:
                problems.append(f"{tag}: not found in {source_id}")
                continue
            actual = q["officialAnswer"][0]
            if expected.get(number) != actual:
                problems.append(
                    f"{tag}: EXPECTED_ANSWER {expected.get(number)} != official {actual}"
                )
            if q["explanationStatus"] == "reviewed":
                problems.append(f"{tag}: already reviewed")

            summary = draft.get("summary", "")
            if not summary.startswith(f"正確答案是 {actual}"):
                problems.append(f"{tag}: summary must start 正確答案是 {actual}")
            if len(draft.get("concept", "")) < 60:
                problems.append(f"{tag}: concept < 60 chars")
            if len(draft.get("answerReason", "")) < 40:
                problems.append(f"{tag}: answerReason < 40 chars")
            if len(draft.get("trap", "")) < 20:
                problems.append(f"{tag}: trap < 20 chars")

            analysis = draft.get("optionAnalysis", {})
            if sorted(analysis) != ["A", "B", "C", "D"]:
                problems.append(f"{tag}: optionAnalysis keys {sorted(analysis)}")
            for label, text in analysis.items():
                if len(text) < 35:
                    problems.append(f"{tag}: option {label} < 35 chars")
                for bad in FORBIDDEN:
                    if bad in text:
                        problems.append(f"{tag}: option {label} contains forbidden 「{bad}」")

            refs = draft.get("references", [])
            if not refs:
                problems.append(f"{tag}: no references")
            for i, ref in enumerate(refs):
                if not str(ref.get("url", "")).startswith("https://"):
                    problems.append(f"{tag}: ref{i} url not https: {ref.get('url')}")
                if not ref.get("title") or not ref.get("locator"):
                    problems.append(f"{tag}: ref{i} missing title/locator")
                if not DATE_RE.match(str(ref.get("checkedAt", ""))):
                    problems.append(f"{tag}: ref{i} bad checkedAt {ref.get('checkedAt')}")

            note = draft.get("editorialNote")
            if note is not None and (not isinstance(note, str) or not note.strip()):
                problems.append(f"{tag}: empty editorialNote")

    print(f"checked {total} drafts across {len(sys.argv) - 1} scripts")
    if problems:
        print(f"{len(problems)} problem(s):")
        for p in problems:
            print(" -", p)
        raise SystemExit(1)
    print("all clear")


if __name__ == "__main__":
    main()
