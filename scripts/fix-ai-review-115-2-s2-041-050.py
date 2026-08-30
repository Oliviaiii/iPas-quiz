"""Guarded draft explanation fixes from independent AI review, Q43 and Q47.

Both notes recorded that the industry sources for ROI and TCO were unreachable
when the drafts were written. IBM's TCO page now answers on retry and covers
both — the direct/indirect split Q47 turns on, and the intangible and hidden
costs Q43 turns on — so it is added to each and the notes are closed.

This script is intentionally not run by the reviewer. It updates only exact
reviewed snapshots and preserves explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-elementary-2-genai-planning"
TARGETS = {
    43: ("aiap-elementary-115-02-genai-planning-043", ["B"],
         "b53e8545a9d7ed6beb7cc70d3196c46be71b54184857558ee8cf6779784eec6d"),
    47: ("aiap-elementary-115-02-genai-planning-047", ["C"],
         "d97e06f14b58e89c08185f6e0d1561101532fd209808d3d3bd62f21bc1a36659"),
}

IBM_TCO_URL = "https://www.ibm.com/think/topics/total-cost-of-ownership"

OLD_NOTE_43 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：官方學習指引既有已驗證段落未見 ROI 專節，"
    "無形效益與隱性成本的論述以 Wikipedia ROI 條目所列限制與 TCO 定義佐證，宜由複核者補查管理會計或 AI 導入評估的更權威一手出處。"
    "查核日期 2026-08-07。"
)
NEW_NOTE_43 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿指出無形效益與隱性成本僅以維基條目佐證，請複核者補查更權威出處。"
    "獨立 AI 複核已補入 IBM Think 的 TCO 主題頁（先前批次查核時為 403，本次重試可開啟）："
    "「Direct costs are relatively easy to see, but TCO also incorporates indirect and hidden costs」，"
    "並明載「there will also always be intangible costs, whether that's employee satisfaction, learning curve」，"
    "正可佐證選項 B 主張的整體評估應納入無形效益與隱性成本。官方學習指引確無 ROI 專節（已全文檢索確認）。"
    "待查項目結案。查核日期 2026-08-30。"
)
NEW_REFERENCE_43 = {
    "title": "IBM Think－What is total cost of ownership (TCO)?",
    "url": IBM_TCO_URL,
    "locator": (
        "逐字核對：Direct costs are relatively easy to see, but TCO also incorporates indirect and hidden costs；"
        "there will also always be intangible costs, whether that's employee satisfaction, learning curve；"
        "支持「完整評估須納入無形效益與隱性成本、不能只看可量化的回收期」之敘述"
    ),
    "checkedAt": "2026-08-30",
}

OLD_NOTE_47 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：TCO 的一手定義來源（Gartner 詞彙表與 IBM 主題頁）"
    "於先前批次查核時即回應 HTTP 403，本批未重試，暫以維基百科條目與 API 計價文件作為輔助參考，宜由複核者補查更權威的一手出處。"
    "查核日期 2026-08-07。"
)
NEW_NOTE_47 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿記載 Gartner 與 IBM 的 TCO 頁面回應 403、待補一手出處。"
    "獨立 AI 複核重試後 IBM Think 的 TCO 主題頁已可開啟並補為第四筆來源：「It accounts for direct costs (such as the initial "
    "purchase price) and indirect costs (such as time spent adjusting to new systems)」，直接／間接成本的分野與本題判準一致"
    "（Gartner 詞彙表仍為 403）。另記一項界定：該頁提到 TCO 亦涵蓋 cost savings，指的是擁有週期內的節省（如殘值），"
    "與選項 C 所述「導入後配送效率提升帶來的燃油與維運成本下降」不同——後者是系統效益，不是擁有系統所需的支出，"
    "本題問「直接成本考量」，C 仍為正解。待查項目結案。查核日期 2026-08-30。"
)
NEW_REFERENCE_47 = {
    "title": "IBM Think－What is total cost of ownership (TCO)?",
    "url": IBM_TCO_URL,
    "locator": (
        "逐字核對：Total cost of ownership, or TCO, is a calculation that quantifies the total cost of a product or service "
        "over its entire lifecycle. It accounts for direct costs (such as the initial purchase price) and indirect costs "
        "(such as time spent adjusting to new systems)；支持本題以「是否為擁有與營運系統所需的支出」區辨直接成本之判準"
    ),
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

    for number, old, new, reference in (
        (43, OLD_NOTE_43, NEW_NOTE_43, NEW_REFERENCE_43),
        (47, OLD_NOTE_47, NEW_NOTE_47, NEW_REFERENCE_47),
    ):
        explanation = selected[number]["explanation"]
        if explanation.get("editorialNote") != old:
            raise RuntimeError(f"Guard failed for Q{number} editorialNote snapshot")
        explanation["editorialNote"] = new
        explanation["references"].append(reference)

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
