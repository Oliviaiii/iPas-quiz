"""Guarded draft explanation fixes from independent AI review, Q5 and Q7.

Both notes are correct technical qualifications that the draft already states in
the option analysis and trap; each asks a later reviewer to settle something the
exam never specifies. They are closed with what the review established, and the
notes now say why the answer holds regardless.

This script is intentionally not run by the reviewer. It updates only exact
reviewed snapshots and preserves explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-114-intermediate-2-ai-tech-planning"
TARGETS = {
    5: ("aiap-intermediate-114-02-ai-tech-planning-005", ["A"],
        "1b8acbee426d927474da354734a935b7d68d715f6ac35fb9b33219f21e89f1e5"),
    7: ("aiap-intermediate-114-02-ai-tech-planning-007", ["A"],
        "31302b80f226bd50aa349f50f4d02b01ce9e72e3816b4936278789774ee5d16f"),
}

OLD_NOTE_5 = (
    "本站依官方答案 A 撰寫，但選項敘述需加限定：TF-IDF 並非必然讓長文本的常見詞權重過度放大。"
    "scikit-learn 的 TfidfTransformer 預設使用 L2正規化，也可設定 sublinear_tf；不同 TF 定義與正規化會降低文件長度影響。"
    "待人工複核題目預設的 TF 計算方式。查核日期 2026-08-12。"
)
NEW_NOTE_5 = (
    "本站依官方答案 A 撰寫，並保留一項限定：TF-IDF 並非必然讓長文本的常見詞權重過度放大——"
    "scikit-learn 的 TfidfTransformer 預設使用 L2 正規化，也可設定 sublinear_tf，不同 TF 定義與正規化會降低文件長度的影響；"
    "此限定已寫入選項 A 解析與解題提醒。原稿把「題目預設的 TF 計算方式」列為待查，獨立 AI 複核已逐字核對試題全文："
    "題幹與四個選項均未指明 TF 的計算方式，此點無從查證。惟本題答案不受影響——選項 B（TF-IDF 需要句子邊界）、"
    "C（無法同時處理多份文件）、D（文件長度改變 IDF）在計算定義上均為錯誤，A 是唯一可選者。待查項目以此結案。"
    "查核日期 2026-08-30。"
)

OLD_NOTE_7 = (
    "本站依官方答案 A 判定，但其「模型偵測結果越精準」應解讀為高 IoU門檻要求通過者具更精準定位，"
    "而不是調高門檻會讓模型輸出本身改善。待人工複核是否需在前端用語中特別保留此限定。查核日期 2026-08-12。"
)
NEW_NOTE_7 = (
    "本站依官方答案 A 判定，並保留一項解讀限定：選項所稱「模型偵測結果越精準」應理解為高 IoU 門檻要求通過者具更精準的定位，"
    "而不是調高門檻會讓模型輸出本身改善——調高門檻只改變評估標準，同一組預測在更嚴格門檻下通過的反而更少。"
    "原稿把「是否需在前端用語中特別保留此限定」列為待查，獨立 AI 複核確認限定確實必要且已就位："
    "選項 A 解析已以「正確（就評估條件而言）」開頭並說明其意，選項 B、C 的解析也各自點出調高門檻不會使 mAP 上升、"
    "recall 也不會自然上升，讀者在選項層即可看到此界線，無須另加前端標示。待查項目結案。查核日期 2026-08-30。"
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

    for number, old, new in ((5, OLD_NOTE_5, NEW_NOTE_5), (7, OLD_NOTE_7, NEW_NOTE_7)):
        explanation = selected[number]["explanation"]
        if explanation.get("editorialNote") != old:
            raise RuntimeError(f"Guard failed for Q{number} editorialNote snapshot")
        explanation["editorialNote"] = new

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
