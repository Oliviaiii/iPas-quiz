"""Guarded draft explanation fix from independent AI review, Q32.

The third reference (an MDPI article) is a real, correctly cited paper, but the
publisher blocks automated access — the article page and its DOI redirect both
return HTTP 403. Recording that in the note saves the next reviewer the same
dead end; the accessible SAS Model Manager reference already carries the PSI
definition the explanation relies on.

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
    32: ("aiap-intermediate-114-02-ai-tech-planning-032", ["D"],
         "7734ac2b614c71bb115e0b99226983f5c935b7deea45fc64beb75e8465ad1bf7"),
}

OLD_LOCATOR_32 = "第 1.2 節：PSI 用於監控目前資料相對模型開發資料的分布位移，並討論其限制"
NEW_LOCATOR_32 = (
    "第 1.2 節：PSI 用於監控目前資料相對模型開發資料的分布位移，並討論其限制。"
    "註：MDPI 對自動化存取回應 HTTP 403（文章頁與 doi.org 轉址皆同），需以瀏覽器人工開啟；"
    "本題所依據的 PSI 定義另有可自動存取的 SAS Model Manager 使用手冊佐證"
)

OLD_NOTE_32 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
    "PSI 是風險指標而非效能因果證明，且常見 0.1／0.25 門檻只是經驗值；本題依「提早發現風險」與官方答案 D 解讀。"
)
NEW_NOTE_32 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
    "PSI 是風險指標而非效能因果證明，且常見 0.1／0.25 門檻只是經驗值；本題依「提早發現風險」與官方答案 D 解讀。"
    "來源可及性（獨立 AI 複核 2026-08-30 查核）：第三筆 MDPI 文章對自動化存取回應 HTTP 403，"
    "文章頁與 doi.org 轉址皆無法以程式開啟，需以瀏覽器人工檢視；引用本身正確，"
    "且 PSI 的定義另有可自動存取的 SAS Model Manager 使用手冊（第二筆來源）佐證，不影響本題論據。"
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

    e32 = selected[32]["explanation"]
    if e32["references"][2]["locator"] != OLD_LOCATOR_32 or e32.get("editorialNote") != OLD_NOTE_32:
        raise RuntimeError("Guard failed for Q32 snapshot fields")
    e32["references"][2]["locator"] = NEW_LOCATOR_32
    e32["references"][2]["checkedAt"] = "2026-08-30"
    e32["editorialNote"] = NEW_NOTE_32

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
