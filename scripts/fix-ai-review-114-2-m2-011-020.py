"""Guarded draft explanation fix from independent AI review, Q14.

The note asks a later reviewer to check the normalized-Gini formula against the
official teaching material. There is none for the intermediate level, and the
answer does not need one: for two classes the maximum Gini impurity is 0.5, so
an even split normalizes to 1 under any of the usual conventions.

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
    14: ("aiap-intermediate-114-02-big-data-014", ["D"],
         "6ac1a545032cd08d05eb5d01e6356e59e253ae440e563306b95486de20821ded"),
}

OLD_NOTE_14 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
    "「Normalized Gini impurity」並非所有教材都採同一命名；本題依官方答案 D，解作以 K 類最大值 1−1/K 正規化。"
    "待複核官方學習材料的明確公式。"
)
NEW_NOTE_14 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
    "「Normalized Gini impurity」並非所有教材都採同一命名；本題依官方答案 D，解作以 K 類最大值 1−1/K 正規化。"
    "原稿把「官方學習材料的明確公式」列為待查，獨立 AI 複核查證：官方僅出版初級兩科學習指引，中級並無對應學習指引"
    "（學習資源頁中級區塊只列 6 份試題公告、全站 600 題零引用、推測網址均 404），此方向查無資料。"
    "惟本題答案不依賴該公式的命名：二元類別各半時原始 Gini 為 1−0.5²−0.5²=0.5，恰為二元的最大值，"
    "無論以 1−1/K 或以該情境的最大不純度正規化，結果都是 1；選項 A（0）、B（0.42，對應 0.7/0.3 之比例）、"
    "C（0.84）在任一慣例下都算不出來。待查項目以此結案。查核日期 2026-08-30。"
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

    e14 = selected[14]["explanation"]
    if e14.get("editorialNote") != OLD_NOTE_14:
        raise RuntimeError("Guard failed for Q14 editorialNote snapshot")
    e14["editorialNote"] = NEW_NOTE_14

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
