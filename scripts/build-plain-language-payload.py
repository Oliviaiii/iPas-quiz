"""Turn a flat draft of rewrites into a guarded plain-language payload.

Usage::

    python scripts/build-plain-language-payload.py <sourceId> <start> <end> <draft.json>

``draft.json`` is a flat mapping of question number to option letter to the
rewritten text::

    {"11": {"A": "…", "B": "…", "C": "…", "D": "…"}, "12": {…}}

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


def main() -> None:
    if len(sys.argv) != 5:
        raise SystemExit(__doc__)
    source_id, start, end, draft_path = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), Path(sys.argv[4])

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
        analysis = question["explanation"]["optionAnalysis"]
        entry = {}
        for letter, new in draft[str(number)].items():
            old = analysis.get(letter)
            if not old:
                raise SystemExit(f"Q{number} {letter}: no existing analysis to replace")
            if new == old:
                raise SystemExit(f"Q{number} {letter}: rewrite is identical to the original")
            if old.startswith("正確") and not new.startswith("正確"):
                raise SystemExit(f"Q{number} {letter}: 正確 marker dropped")
            if new.startswith("正確") and not old.startswith("正確") and letter not in question["officialAnswer"]:
                raise SystemExit(f"Q{number} {letter}: 正確 marker added to a non-answer option")
            if len(new) < len(old) * 0.8:
                raise SystemExit(f"Q{number} {letter}: rewrite is {len(new)} chars against {len(old)} — too short")
            entry[letter] = {
                "oldSha256": hashlib.sha256(old.encode("utf-8")).hexdigest(),
                "old": old,
                "new": new,
            }
            total += 1
        if set(entry) != set(analysis):
            raise SystemExit(f"Q{number}: rewrote {sorted(entry)} but the question has {sorted(analysis)}")
        items.append(
            {
                "questionId": question["id"],
                "officialQuestionNumber": number,
                "optionAnalysis": entry,
            }
        )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{source_id}-{start:03d}-{end:03d}.json"
    payload = {
        "schemaVersion": 1,
        "sourceId": source_id,
        "range": {"start": start, "end": end},
        "rewrittenAt": "2026-08-31",
        "items": items,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)} — {total} option analyses across {len(items)} questions")


if __name__ == "__main__":
    main()
