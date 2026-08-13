"""Guarded draft explanation fixes from independent AI review, Q32, Q33 and Q38.

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
    32: ("aiap-elementary-115-01-genai-planning-032", ["A"], "3bf92b47ff0c26227811db0b3b86d3ffa7753f68f414eed344190c81b996abb1"),
    33: ("aiap-elementary-115-01-genai-planning-033", ["A"], "99cece88b5e606debfaf1c8cb597c3dde5d102b51b4c91ef26e7d7f07483dc90"),
    38: ("aiap-elementary-115-01-genai-planning-038", ["C"], "be3fb4d4417f795898362314d02d65fb4a692a3846a52f9d3685cb8693cbaa85"),
}

OLD_OPTION_A_33 = (
    "正確。Low-Code 平台讓非資訊背景的科室人員以視覺化方式建立表單、之後自行調整流程；"
    "判讀與分類交給預訓練語言模型 API，以 API 呼叫即可取得語意理解能力，不必蒐集標註資料自建模型，開發與維運負擔都被壓到最低。"
)
NEW_OPTION_A_33 = (
    "正確。Low-Code 平台以視覺化拖拉為主、必要時搭配少量程式碼，科室人員可自行建立表單並在既有範本上調整流程；"
    "判讀與分類交給預訓練語言模型 API，以 API 呼叫即可取得語意理解能力，不必蒐集標註資料自建模型，開發與維運負擔都被壓到最低。"
)

OLD_SUMMARY_32 = (
    "正確答案是 A。No-Code/Low-Code 建模平台的典型作法，是把模型訓練與調校包成視覺化介面與標準化流程，"
    "讓使用者不寫程式也能完成建模。"
)
NEW_SUMMARY_32 = (
    "正確答案是 A。No-Code/Low-Code 建模平台的典型作法，是把模型訓練與調校包成視覺化介面與標準化流程，"
    "讓使用者不寫程式（Low-Code 則只需少量程式）也能完成建模。"
)

OLD_OPTION_C_38 = (
    "正確（本題要選的「最不適合」）。使用規範與治理框架是全組織層級的制度建置：定義誰能用、怎麼用、出問題誰負責，"
    "需要跨部門協調且以「確定導入」為前提。PoC 的結論都還沒出來，先建長期治理等於把後段工作前置，既拖慢驗證節奏，"
    "也可能白做；這類工作應在 PoC 通過、決定擴大部署後展開。"
)
NEW_OPTION_C_38 = (
    "正確（本題要選的「最不適合」）。使用規範與治理框架是全組織層級的制度建置：定義誰能用、怎麼用、出問題誰負責，"
    "需要跨部門協調且以「確定導入」為前提。PoC 的結論都還沒出來，先建長期治理等於把後段工作前置，既拖慢驗證節奏，"
    "也可能白做；這類工作宜在 PoC 通過、決定擴大部署後才全面展開。要留意的是，PoC 期間並非完全不談治理："
    "NIST AI RMF 把治理視為貫穿整個 AI 生命週期的跨領域功能，小範圍試用仍應有基本的資料使用與風險控管約束；"
    "但建立全組織的使用規範與長期治理框架並不是本階段的主要工作。"
)

OLD_LOCATOR_38 = "第 38 題題幹、選項與官方答案"
NEW_LOCATOR_38 = "PDF 第 9 頁（共 11 頁）：第 38 題題幹、(A)～(D) 選項與左欄官方答案 C"

OLD_NOTE_38 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：官方學習指引科目二未見 PoC（概念驗證）專節，"
    "本題對 PoC 與全面部署階段的工作劃分依一般專案實務整理，除公告試題外尚缺可引用的外部一手出處，待複核補查。查核日期 2026-08-03。"
)
NEW_NOTE_38 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。官方學習指引科目二未見 PoC（概念驗證）專節，"
    "本題對 PoC 與全面部署階段的工作劃分依一般專案實務整理；獨立 AI 複核已補入 PoC 定義與 NIST AI RMF 治理定位兩筆外部出處。查核日期 2026-08-13。"
)

NEW_REFERENCES_38 = [
    {
        "title": "Proof of concept — Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Proof_of_concept",
        "locator": "定義段：PoC 為 an inchoate realization of a certain idea or method in order to demonstrate its feasibility or viability，用於驗證可行性、隔離技術問題並提供預算判斷依據",
        "checkedAt": "2026-08-13",
    },
    {
        "title": "NIST AI Risk Management Framework (AI RMF 1.0) — Core：GOVERN",
        "url": "https://airc.nist.gov/AI_RMF_Knowledge_Base/AI_RMF/Core_And_Profiles/5-sec-core",
        "locator": "GOVERN 說明治理為 cross-cutting function，涵蓋組織層級政策、流程與 accountability structures，並為貫穿 AI 系統生命週期的持續性要求",
        "checkedAt": "2026-08-13",
    },
]


def snapshot_hash(question: dict) -> str:
    snapshot = {key: question[key] for key in ("id", "officialAnswer", "explanationStatus", "explanation")}
    payload = json.dumps(snapshot, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    selected = {q["officialQuestionNumber"]: q for q in questions if q.get("sourceId") == SOURCE_ID and q.get("officialQuestionNumber") in TARGETS}
    if set(selected) != set(TARGETS):
        raise RuntimeError(f"Expected targets {sorted(TARGETS)}, found {sorted(selected)}")
    for number, (question_id, answer, digest) in TARGETS.items():
        question = selected[number]
        if question.get("id") != question_id or question.get("officialAnswer") != answer:
            raise RuntimeError(f"Guard failed for Q{number} identity or answer")
        if question.get("explanationStatus") != "draft" or snapshot_hash(question) != digest:
            raise RuntimeError(f"Guard failed for Q{number} status or reviewed snapshot")

    e32 = selected[32]["explanation"]
    if e32["summary"] != OLD_SUMMARY_32:
        raise RuntimeError("Guard failed for Q32 summary snapshot")
    e32["summary"] = NEW_SUMMARY_32

    e33 = selected[33]["explanation"]
    if e33["optionAnalysis"]["A"] != OLD_OPTION_A_33:
        raise RuntimeError("Guard failed for Q33 optionAnalysis.A snapshot")
    e33["optionAnalysis"]["A"] = NEW_OPTION_A_33

    e38 = selected[38]["explanation"]
    if e38["optionAnalysis"]["C"] != OLD_OPTION_C_38:
        raise RuntimeError("Guard failed for Q38 optionAnalysis.C snapshot")
    if e38.get("editorialNote") != OLD_NOTE_38:
        raise RuntimeError("Guard failed for Q38 editorialNote snapshot")
    if len(e38["references"]) != 1 or e38["references"][0]["locator"] != OLD_LOCATOR_38:
        raise RuntimeError("Guard failed for Q38 references snapshot")
    e38["optionAnalysis"]["C"] = NEW_OPTION_C_38
    e38["editorialNote"] = NEW_NOTE_38
    e38["references"][0]["locator"] = NEW_LOCATOR_38
    e38["references"].extend(NEW_REFERENCES_38)

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
