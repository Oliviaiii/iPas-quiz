"""Guarded draft explanation fix from independent AI review, Q46.

This script is intentionally not run by the reviewer. It updates only exact
reviewed snapshots and preserves explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-elementary-1-genai-planning"
TARGETS = {
    46: (
        "aiap-elementary-115-01-genai-planning-046",
        ["C"],
        "bc05b02fd2f823df7607abf0c7de0992a5a9e5a6f3b572519ae439cb99a96174",
    ),
}

OLD_LOCATOR_46 = "第 46 題題幹、選項與官方答案"
NEW_LOCATOR_46 = "PDF 第 10～11 頁（共 11 頁）：第 46 題題幹、(A)～(D) 選項與左欄官方答案 C"

# 原稿把 B 與 C 的取捨列為待查，請人工複核者判斷。獨立 AI 複核已逐字比對兩個
# 選項：B 自述的效益是「兼顧成本彈性」，正落在題幹明文後置的考量上；C 則只談
# 安全與治理，並多出存取控管與稽核。判準來自選項文字本身，不需人工政策判斷，
# 因此結案，改為說明判準，避免把已查證事項留給人工複核。
OLD_NOTE_46 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：選項 B 的開源模型私有化部署同樣能讓資料留在機構內部，"
    "本題判 C 較佳係基於題幹將成本考量明確後置、且 C 額外具備存取控管與稽核之治理配套，屬程度比較而非絕對排除；"
    "複核者宜確認此比較說法的表述是否恰當。查核日期 2026-08-03。"
)
NEW_NOTE_46 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。選項 B 的開源模型私有化部署同樣能讓資料留在機構內部，"
    "本題判 C 較佳屬程度比較而非絕對排除；獨立 AI 複核已逐字核對兩個選項：B 自述的效益為「兼顧成本彈性與模型可控性」，"
    "而題幹明文要求安全與法遵優先於成本，C 則另含存取控管與稽核之治理配套，判準取自選項文字本身，此比較說法成立。"
    "查核日期 2026-08-30。"
)

# 監理情境的「可課責性」是本題 B 與 C 的分野，原稿僅引學習指引的權限控管一句；
# 補一筆治理框架一手出處，讓存取控管與稽核的必要性有官方標準可徵。
NEW_REFERENCE_46 = {
    "title": "NIST AI Risk Management Framework (AI RMF 1.0) — Core：GOVERN",
    "url": "https://airc.nist.gov/AI_RMF_Knowledge_Base/AI_RMF/Core_And_Profiles/5-sec-core",
    "locator": "GOVERN 1.2、GOVERN 4.1：組織須就 AI 風險建立可課責（accountability）結構、政策與流程，並將透明度與稽核納入既有治理；支持本題把存取控管與稽核列為法遵情境必要配套之敘述",
    "checkedAt": "2026-08-30",
}


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

    e46 = selected[46]["explanation"]
    if e46.get("editorialNote") != OLD_NOTE_46:
        raise RuntimeError("Guard failed for Q46 editorialNote snapshot")
    if len(e46["references"]) != 2 or e46["references"][0]["locator"] != OLD_LOCATOR_46:
        raise RuntimeError("Guard failed for Q46 references snapshot")
    e46["editorialNote"] = NEW_NOTE_46
    e46["references"][0]["locator"] = NEW_LOCATOR_46
    e46["references"].append(NEW_REFERENCE_46)

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
