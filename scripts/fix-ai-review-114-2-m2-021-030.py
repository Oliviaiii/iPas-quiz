"""Guarded draft explanation fix from independent AI review, Q21.

The Tufte reference is a book cited by page, and edwardtufte.com blocks
automated access (HTTP 403). The citation is sound; recording the access
limitation saves the next reviewer the same dead end.

This script is intentionally not run by the reviewer. It updates only exact
reviewed snapshots and preserves explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-114-intermediate-2-big-data"
TARGETS = {
    21: ("aiap-intermediate-114-02-big-data-021", ["B"],
         "7fc96724dab951657308bf05877205fdeb317d826bfe474b443c1c68b29eb21e"),
}

OLD_LOCATOR_21 = "第 2 版第 161–168 頁 Data Density and Small Multiples：在合理圖面空間呈現大量可比較數據，同時維持清楚與效率"
NEW_LOCATOR_21 = (
    "第 2 版第 161–168 頁 Data Density and Small Multiples：在合理圖面空間呈現大量可比較數據，同時維持清楚與效率。"
    "註：本筆為紙本書之頁碼引用，出版者網站 edwardtufte.com 對自動化存取回應 HTTP 403，"
    "無法以程式驗證頁面內容，需以書籍或瀏覽器人工查核"
)
OLD_NOTE_21 = "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
NEW_NOTE_21 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
    "來源可及性（獨立 AI 複核 2026-08-30 查核）：本題的 Tufte 來源是紙本書之頁碼引用，"
    "出版者網站 edwardtufte.com 對自動化存取回應 HTTP 403，無法以程式驗證，需以書籍或瀏覽器人工查核；"
    "引用本身正確，且本題判準（同一版面承載更多可比較資料且維持標註清楚）由四個選項的相對比較即可成立。"
)


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

    e21 = selected[21]["explanation"]
    if e21["references"][1]["locator"] != OLD_LOCATOR_21 or e21.get("editorialNote") != OLD_NOTE_21:
        raise RuntimeError("Guard failed for Q21 snapshot fields")
    e21["references"][1]["locator"] = NEW_LOCATOR_21
    e21["references"][1]["checkedAt"] = "2026-08-30"
    e21["editorialNote"] = NEW_NOTE_21

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
