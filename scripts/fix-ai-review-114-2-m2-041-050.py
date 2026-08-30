"""Guarded draft explanation fixes from independent AI review, Q41 and Q42.

This script is intentionally not re-run by the reviewer. It updates only exact
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
    41: ("aiap-intermediate-114-02-big-data-041", ["A"], "c621b2018700d3743c2ff011a4ddcb7c03b9ffd1117ebd64b813359398611bfb"),
    42: ("aiap-intermediate-114-02-big-data-042", ["C"], "b8f6146e3473206034a2084107b1c8e78cdc63387d1b83596ebd91a8f1cac87f"),
}

# 官方附圖把「要分成的群數」寫作 X，詳解卻寫成 K，與圖面不符。
OLD_REASON_41 = (
    "已目視核對官方附圖：先隨機選 K 個資料點當中心，逐點計算到每個中心的距離並指派最近群，"
    "再以群內平均更新中心，中心不動即停止。這些是 K-means 的完整識別特徵，因此選 A。"
)
NEW_REASON_41 = (
    "已目視核對官方附圖：輸入除了 N 筆 D 維資料外還有 X（要分成的群數），流程先隨機選 X 個資料點當中心，"
    "逐點計算到每個中心的距離並指派最近群，再以群內平均更新中心，中心不再變動即停止。"
    "這些是 K-means 的完整識別特徵（圖中的 X 即一般寫法的 K），因此選 A。"
)

OLD_OPTION_D_41 = (
    "DBSCAN 依 epsilon 鄰域與 MinPts 找密度相連區域，能標記噪聲且不先指定群數；"
    "附圖要求輸入 K，並依中心距離分群，與密度式流程不同。"
)
NEW_OPTION_D_41 = (
    "DBSCAN 依 epsilon 鄰域與 MinPts 找密度相連區域，能標記噪聲且不先指定群數；"
    "附圖卻要求先輸入群數 X，並依中心距離分群，與密度式流程不同。"
)

# 第 41、42 題各有自己的題幹附圖，並不屬於第 43～47 題的共用題組。
OLD_LOCATOR_41 = "第 41 題題幹、選項、共用題組附圖與官方答案"
NEW_LOCATOR_41 = "PDF 第 12 頁：第 41 題題幹、虛擬碼題幹附圖、(A)～(D) 選項與左欄官方答案 A"

OLD_LOCATOR_42 = "第 42 題題幹、選項、共用題組附圖與官方答案"
NEW_LOCATOR_42 = (
    "PDF 第 12～13 頁：第 42 題題幹與左欄官方答案 C（第 12 頁）、"
    "SciPy 程式碼題幹附圖與 (A)～(D) 選項（第 13 頁）"
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

    e41 = selected[41]["explanation"]
    if e41["answerReason"] != OLD_REASON_41:
        raise RuntimeError("Guard failed for Q41 answerReason snapshot")
    if e41["optionAnalysis"]["D"] != OLD_OPTION_D_41:
        raise RuntimeError("Guard failed for Q41 optionAnalysis.D snapshot")
    if e41["references"][0]["locator"] != OLD_LOCATOR_41:
        raise RuntimeError("Guard failed for Q41 reference locator snapshot")
    e41["answerReason"] = NEW_REASON_41
    e41["optionAnalysis"]["D"] = NEW_OPTION_D_41
    e41["references"][0]["locator"] = NEW_LOCATOR_41
    e41["references"][0]["checkedAt"] = "2026-08-30"

    e42 = selected[42]["explanation"]
    if e42["references"][0]["locator"] != OLD_LOCATOR_42:
        raise RuntimeError("Guard failed for Q42 reference locator snapshot")
    e42["references"][0]["locator"] = NEW_LOCATOR_42
    e42["references"][0]["checkedAt"] = "2026-08-30"

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
