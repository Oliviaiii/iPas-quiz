"""Turn a flat draft of rewrites into a guarded plain-language payload.

Usage::

    python scripts/build-plain-language-payload.py <sourceId> <start> <end> <draft.json>
    python scripts/build-plain-language-payload.py <sourceId> <start> <end> <draft.json> --prose

Without ``--prose`` the draft maps question number to option letter::

    {"11": {"A": "…", "B": "…", "C": "…", "D": "…"}, "12": {…}}

With ``--prose`` it maps question number to the two prose fields instead, and
the payload is written to ``…-prose.json`` so the two passes never collide::

    {"11": {"concept": "…", "answerReason": "…"}, "12": {…}}

The script looks up each current option analysis, records it verbatim with its
sha256 and writes
``content/plain-language/<sourceId>-<start>-<end>.json``. It refuses a draft
that drops the "正確" marker, moves it onto an option the official answer does
not name, leaves the text unchanged, or shrinks it below 80% of the original —
the same guards ``apply-plain-language.py`` re-checks at apply time.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
OUT_DIR = ROOT / "content" / "plain-language"


PROSE_FIELDS = ("concept", "answerReason")


def check(number: str, field: str, old: str, new: str, answer: list[str]) -> None:
    """Shared guards for one rewritten string."""
    if new == old:
        raise SystemExit(f"Q{number} {field}: rewrite is identical to the original")
    if old.startswith("正確") and not new.startswith("正確"):
        raise SystemExit(f"Q{number} {field}: 正確 marker dropped")
    if new.startswith("正確") and not old.startswith("正確") and field not in answer:
        raise SystemExit(f"Q{number} {field}: 正確 marker added to a non-answer option")
    if len(new) < len(old) * 0.8:
        raise SystemExit(f"Q{number} {field}: rewrite is {len(new)} chars against {len(old)} — too short")


def main() -> None:
    argv = [a for a in sys.argv[1:] if a != "--prose"]
    prose = "--prose" in sys.argv
    if len(argv) != 4:
        raise SystemExit(__doc__)
    source_id, start, end, draft_path = argv[0], int(argv[1]), int(argv[2]), Path(argv[3])

    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    selected = {
        q["officialQuestionNumber"]: q
        for q in questions
        if q.get("sourceId") == source_id and start <= q["officialQuestionNumber"] <= end
    }
    if len(selected) != end - start + 1:
        raise SystemExit(f"expected {end - start + 1} questions for {source_id}, found {len(selected)}")

    draft = json.loads(draft_path.read_text(encoding="utf-8"))
    numbers = sorted(int(k) for k in draft)
    if numbers != list(range(start, end + 1)):
        raise SystemExit(f"draft covers {numbers[:3]}…{numbers[-3:]}, expected {start}–{end}")

    items = []
    total = 0
    for number in numbers:
        question = selected[number]
        explanation = question["explanation"]
        source = explanation if prose else explanation["optionAnalysis"]
        entry = {}
        for field, new in draft[str(number)].items():
            if prose and field not in PROSE_FIELDS:
                raise SystemExit(f"Q{number}: {field} is not a prose field {PROSE_FIELDS}")
            old = source.get(field)
            if not old:
                raise SystemExit(f"Q{number} {field}: no existing text to replace")
            check(str(number), field, old, new, question["officialAnswer"])
            entry[field] = {
                "oldSha256": hashlib.sha256(old.encode("utf-8")).hexdigest(),
                "old": old,
                "new": new,
            }
            total += 1
        expected = set(PROSE_FIELDS) if prose else set(source)
        if set(entry) != expected:
            raise SystemExit(f"Q{number}: rewrote {sorted(entry)} but expected {sorted(expected)}")
        items.append(
            {
                "questionId": question["id"],
                "officialQuestionNumber": number,
                ("prose" if prose else "optionAnalysis"): entry,
            }
        )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    suffix = "-prose" if prose else ""
    path = OUT_DIR / f"{source_id}-{start:03d}-{end:03d}{suffix}.json"
    payload = {
        "schemaVersion": 1,
        "sourceId": source_id,
        "range": {"start": start, "end": end},
        "rewrittenAt": "2026-08-31",
        "items": items,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    kind = "prose fields" if prose else "option analyses"
    print(f"wrote {path.relative_to(ROOT)} — {total} {kind} across {len(items)} questions")


if __name__ == "__main__":
    main()
