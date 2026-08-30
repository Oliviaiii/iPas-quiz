"""Close the residual open 待查 item in 115-2 初級第二科 (Q41).

Follow-up cleanup pass after all 600 questions completed independent AI review.
Guards on the exact reviewed snapshot and preserves explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-elementary-2-genai-planning"
TARGETS = {
    41: ("aiap-elementary-115-02-genai-planning-041", ["A"], "0019f07357d7eaa3d36019ad847d62770e119eda483feb8a758ea4bb433251db", 4),
}

NEW_NOTE_41 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
    "原稿把「解決方案圖（Solution Graph）」缺一手出處列為待查。"
    "獨立 AI 複核已全文檢索官方學習指引兩科：「解決方案圖」「Solution Graph」「有向無環」皆為零筆，"
    "確認官方教材未收錄此詞，命題依據未經公布、無從再查證；同卷第 40 題與 115 年第一次第二科第 16 題"
    "的同一疑義亦以相同的否定結果結案。"
    "惟本題答案不依賴該詞的精確定義：題幹已明說「由大型語言模型（LLM）負責推理與行動生成」，"
    "而 B、C、D 三個選項的共同前提都是「LLM 不參與結構建構或任務規劃」，與題幹自述正面衝突，"
    "只有 A 與題幹前提相容，由題幹與選項文字本身即可判定。待查項目以此結案。查核日期 2026-08-30。"
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
    for number, (question_id, answer, digest, ref_count) in TARGETS.items():
        question = selected[number]
        if question.get("id") != question_id or question.get("officialAnswer") != answer:
            raise RuntimeError(f"Guard failed for Q{number} identity or answer")
        if question.get("explanationStatus") != "draft" or snapshot_hash(question) != digest:
            raise RuntimeError(f"Guard failed for Q{number} status or reviewed snapshot")
        if len(question["explanation"]["references"]) != ref_count:
            raise RuntimeError(f"Guard failed for Q{number} reference count")
        if "待查項目：" not in question["explanation"].get("editorialNote", ""):
            raise RuntimeError(f"Guard failed for Q{number}: editorialNote is not an open 待查 item")

    selected[41]["explanation"]["editorialNote"] = NEW_NOTE_41

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
