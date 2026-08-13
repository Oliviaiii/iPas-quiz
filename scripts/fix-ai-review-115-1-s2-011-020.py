"""Guarded draft explanation fixes from independent AI review, Q12-Q13.

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
    12: ("aiap-elementary-115-01-genai-planning-012", ["B"], "0678ac4f8018a5e2d9733ce03f51f9b33f04bfe4bb6304e3ac73323cfd0c4a1b"),
    13: ("aiap-elementary-115-01-genai-planning-013", ["B"], "2b589d8bad4cf50a8e2ff2d16afba1486327aad7f7ad144263728963bf7b7caf"),
}


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

    e12 = selected[12]["explanation"]
    e12["summary"] = "正確答案是 B。MCP 標準化 AI 應用與外部工具、資源等能力的連接；RAG 則檢索外部來源來增強生成內容。"
    e12["concept"] = (
        "Model Context Protocol（MCP）是一套開放協定，定義 AI 應用、Client 與 Server 的溝通方式；Server 可提供 Tools、Resources 與 Prompts，"
        "讓應用以一致介面連接外部系統與內容。題目以『與外部工具或系統互動』概括其中最具代表性的用途。\n"
        "檢索增強生成（RAG）則在回答前從外部來源取回相關內容，將檢索結果提供給生成模型。向量索引是常見實作，但也可採關鍵字、BM25 或混合檢索，並非定義上的必要條件。"
    )
    e12["answerReason"] = "B 抓到主要定位：MCP 解決 AI 應用如何標準化連接外部工具與系統能力；RAG 解決如何以外部檢索內容補充生成依據。這是用途重點的區分，不表示 MCP 只提供動作或 RAG 必須採特定向量架構。"
    e12["optionAnalysis"]["B"] = "正確。MCP 可讓 AI 應用透過一致協定連接外部工具、資源與提示；本選項聚焦其外部工具或系統互動用途。RAG 則檢索外部來源以增強回答依據，兩者可互補並用。"
    e12["trap"] = "先區分協定整合與檢索增強：MCP 標準化外部能力的連接，RAG 以檢索內容增強生成。不要把助記口訣誤當成排他的完整邊界，也不要把向量資料庫當成 RAG 的必要條件。"

    e13 = selected[13]["explanation"]
    e13["summary"] = "正確答案是 B。依文件與查詢特性妥善設定片段大小、邊界和重疊，可讓檢索單位更貼近問題並減少長文件雜訊。"
    e13["concept"] = (
        "在 RAG 流程中，Chunking 把長文件轉成較小的檢索單位。整份長文件若同時含多個主題，取回時容易把大量無關段落一併帶入；"
        "適當切分可讓相關內容更容易被單獨取回，也能減少生成模型需處理的雜訊。\n"
        "但切塊效果取決於片段大小、語意邊界、重疊與檢索方法。片段過小或在錯誤位置切斷，反而可能失去必要上下文；因此 B 描述的是妥善設計 Chunking 的主要目的，而不是切塊後必然提升的保證。"
    )
    e13["answerReason"] = "題幹的問題是整份文件檢索夾帶無關內容、引用不精準。妥善切分能讓檢索以較聚焦的片段為單位，提升與問題對齊的機會並降低長文件雜訊，因此 B 最符合導入目的；實際效果仍需調整切分策略並驗證。"
    e13["optionAnalysis"]["B"] = "正確。適當大小且邊界合理的片段可讓檢索單位更貼近提問，並避免整份長文件的無關內容一起進入提示；若切得過碎或切斷語意，則需用重疊、結構化切分或其他策略修正。"
    e13["trap"] = "主要目的看檢索品質與雜訊控制，不是推理速度、執行記憶體或創意。另須記得 Chunking 是可調整的檢索設計：適當切分有幫助，不代表任意切分都一定更準。"
    e13["references"].append({
        "title": "Document Segmentation Matters for Retrieval-Augmented Generation",
        "url": "https://aclanthology.org/2025.findings-acl.422/",
        "locator": "實驗顯示 segmentation strategy 顯著影響 RAG retrieval 與 generation 表現",
        "checkedAt": "2026-08-13",
    })

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
