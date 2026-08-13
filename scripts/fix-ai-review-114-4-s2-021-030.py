"""Guarded draft explanation fixes from independent AI review, Q24 and Q27.

This script is intentionally not run by the reviewer. It removes an absolute
privacy guarantee from Q24 and closes Q27's source/qualification gaps. Every
edit is guarded by a hash of the exact reviewed question snapshot and keeps
explanationStatus draft.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-114-elementary-4-genai-planning"
TARGETS = {
    24: {
        "id": "aiap-elementary-114-04-genai-planning-024",
        "answer": ["D"],
        "sha256": "edb48505b6f9741ba943338bbfbd72b8b1eae04a66fe4ca68175375f3103fd7c",
    },
    27: {
        "id": "aiap-elementary-114-04-genai-planning-027",
        "answer": ["C"],
        "sha256": "d9ff9c333aa29796a2b7ef0d358f59794f3a8cbcb4349d46dc3a6e6d4dc9f2d2",
    },
}


def snapshot_hash(question: dict) -> str:
    snapshot = {
        key: question[key]
        for key in ("id", "officialAnswer", "explanationStatus", "explanation")
    }
    payload = json.dumps(
        snapshot,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    selected = {
        question["officialQuestionNumber"]: question
        for question in questions
        if question.get("sourceId") == SOURCE_ID
        and question.get("officialQuestionNumber") in TARGETS
    }
    if set(selected) != set(TARGETS):
        raise RuntimeError(f"Expected targets {sorted(TARGETS)}, found {sorted(selected)}")

    for number, guard in TARGETS.items():
        question = selected[number]
        if question.get("id") != guard["id"]:
            raise RuntimeError(f"Guard failed for Q{number} id")
        if question.get("officialAnswer") != guard["answer"]:
            raise RuntimeError(f"Guard failed for Q{number} official answer")
        if question.get("explanationStatus") != "draft":
            raise RuntimeError(f"Guard failed for Q{number} status")
        if snapshot_hash(question) != guard["sha256"]:
            raise RuntimeError(f"Guard failed for Q{number} reviewed snapshot")

    q24 = selected[24]
    e24 = q24["explanation"]
    e24["summary"] = (
        "正確答案是 D。私有化部署可把資料處理維持在企業控制邊界內，且風控機制應與系統同步建立。"
    )
    e24["concept"] = (
        "題目把取捨條件寫死了：隱私與合規是硬性要求，資源投入不是限制。因此第一順位是縮小資料的暴露面，"
        "並讓保單條款與客戶個資在企業能控管的環境中處理。私有部署可避免把敏感內容直接送往一般第三方模型 API，"
        "也讓企業自行管理網路、身分、權限與稽核；但部署在內部不等於資料絕不可能外洩，內部濫權、提示注入、日誌、"
        "備份與執行環境仍可能造成揭露。\n因此私有部署必須搭配資料最小化、最小權限、加密、隔離、稽核與持續監控。"
        "這些控制應與系統同步上線，避免先提供服務、後補合規所形成的風險空窗。"
    )
    e24["answerReason"] = (
        "四個選項中，D 最完整地同時處理部署邊界與上線時點：自訓／私有部署減少敏感資料向第三方傳輸並增加企業控制權，"
        "同步建立自動化風控則讓存取、稽核與其他防護在服務啟用時就到位。它不能單獨保證零外洩，但在題目允許較高資源投入時，"
        "仍是最符合隱私與合規優先的方案。"
    )
    e24["optionAnalysis"]["A"] = (
        "開源模型自建可減少資料向第三方傳輸，方向接近正解；關鍵問題是把隱私與合規控管留到後續補強。"
        "即使模型在內部，缺少存取控制、加密、稽核與監控仍可能洩漏資料，因此上線前的控制空窗不可接受。"
    )
    e24["optionAnalysis"]["D"] = (
        "正確。自訓並私有化部署可把敏感資料處理留在企業控制邊界內，減少向第三方服務傳輸；同步建立自動化風控，"
        "則使權限、隔離、加密、稽核與監控等措施一起到位。這是降低風險的多層控制，不是單靠部署位置保證零外洩。"
    )
    e24["trap"] = (
        "第一，先讀出硬性條件與可放寬條件：本題可多投入資源，隱私與合規則不能延後。第二，私有部署只改變控制邊界，"
        "不等於自動安全；仍須同步建立存取控制、加密、隔離、稽核與監控。"
    )
    e24["references"].append(
        {
            "title": "OWASP GenAI Security Project－LLM02:2025 Sensitive Information Disclosure",
            "url": "https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/",
            "locator": "敏感資訊防護需資料清理、嚴格存取控制與最小權限、限制資料來源及安全執行環境等多層措施",
            "checkedAt": "2026-08-13",
        }
    )

    q27 = selected[27]
    e27 = q27["explanation"]
    e27["trap"] = (
        "第一，ASR 準確度是摘要品質的基礎；在逐字稿已達可用水準後，多人會議還要還原『誰說的』與『在談哪個議題』，"
        "才能避免張冠李戴並依主題整理。第二，題目要的是即時自動摘要，把整理留給事後人工不符合目標。"
    )
    e27["references"].append(
        {
            "title": "QMSum: A New Benchmark for Query-based Multi-domain Meeting Summarization",
            "url": "https://aclanthology.org/2021.naacl-main.472/",
            "locator": "多人、多主題長會議摘要資料含主題分段標註，並評估 locate-then-summarize 方法",
            "checkedAt": "2026-08-13",
        }
    )

    q24["explanationStatus"] = "draft"
    q27["explanationStatus"] = "draft"
    QUESTIONS.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
