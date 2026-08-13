"""Guarded draft explanation fixes from independent AI review, Q44/Q46/Q47/Q50.

The reviewer intentionally does not run this script. It updates only the
reviewed explanation drafts, refuses changed snapshots, and keeps every target
at explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-114-elementary-4-genai-planning"
TARGETS = {
    44: ("aiap-elementary-114-04-genai-planning-044", ["C"], "da8ee19977b834d8bc91c7a59364031bf4945d83428b4082cf1a3c21e07ac5d9"),
    46: ("aiap-elementary-114-04-genai-planning-046", ["D"], "7e2c568a4f09eb7970e3242476a12be69442d2387e86e68d2a0962dc4c53e79d"),
    47: ("aiap-elementary-114-04-genai-planning-047", ["B"], "3482faf7cc86e566046906aee9e0a110b954b768ff4714f822d1471abcea7a4a"),
    50: ("aiap-elementary-114-04-genai-planning-050", ["C"], "42284b22890d1fee2f3738540f4a230e7733eab3bc224ab3ba3a979ea0f63b7c"),
}


def snapshot_hash(question: dict) -> str:
    snapshot = {
        key: question[key]
        for key in ("id", "officialAnswer", "explanationStatus", "explanation")
    }
    payload = json.dumps(
        snapshot, ensure_ascii=False, sort_keys=True, separators=(",", ":")
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

    for number, (question_id, answer, digest) in TARGETS.items():
        question = selected[number]
        if question.get("id") != question_id:
            raise RuntimeError(f"Guard failed for Q{number} id")
        if question.get("officialAnswer") != answer:
            raise RuntimeError(f"Guard failed for Q{number} official answer")
        if question.get("explanationStatus") != "draft":
            raise RuntimeError(f"Guard failed for Q{number} status")
        if snapshot_hash(question) != digest:
            raise RuntimeError(f"Guard failed for Q{number} reviewed snapshot")

    e44 = selected[44]["explanation"]
    e44["summary"] = (
        "正確答案是 C。RAG 著重檢索外部內容作為生成依據；MCP 則以統一協定連接工具、資源與提示，C 特別點出工具與 API 整合。"
    )
    e44["concept"] = (
        "兩者都能讓模型使用外部能力，但抽象層次不同。RAG 的核心是在生成時先檢索外部知識，"
        "把相關內容提供給生成模型；文件切分、稠密向量、關鍵字或混合檢索都是可能實作，並非定義上只能依賴向量資料庫。\n"
        "MCP 是 AI 應用與外部系統溝通的開放協定。官方架構中，Server 可提供工具（可執行函式）、資源（脈絡資料）與提示範本。"
        "因此 MCP 不只『補動作』，也能提供資料與提示；本題 C 仍是最佳答案，因為它抓到 RAG 的檢索重心與 MCP 的標準化工具／API 整合能力。"
    )
    e44["answerReason"] = (
        "C 是唯一正確抓到主要重心的選項：RAG 以檢索外部知識支援回答；MCP 以標準協定讓應用發現並使用外部能力，"
        "其中工具與 API 呼叫是代表性用途。這是相對定位，不表示 RAG 只能用向量庫，也不表示 MCP 只能提供工具。"
    )
    e44["optionAnalysis"]["C"] = (
        "正確。RAG 的核心是檢索外部內容作為生成依據；MCP 的核心是標準化 AI 應用與外部 tools、resources、prompts 的連接。"
        "選項以動態工具與 API 呼叫概括 MCP 的重要用途，雖非 MCP 的全部能力，仍是四項中最準確的差異描述。"
    )
    e44["trap"] = (
        "第一，RAG 是檢索增強方法，不等於特定向量資料庫產品。第二，MCP 是連接協定，server 能提供 tools、resources、prompts；"
        "選項 C 描述的是兩者主要重心，不是互斥邊界。"
    )
    e44["references"].append({
        "title": "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
        "url": "https://arxiv.org/abs/2005.11401",
        "locator": "結合參數式生成模型與推論時檢索的外部非參數記憶",
        "checkedAt": "2026-08-13",
    })

    e46 = selected[46]["explanation"]
    e46["concept"] = (
        "Guardrails 是套用在 AI 互動流程各個可控檢查點的政策與安全控制。以 NVIDIA NeMo Guardrails 為例，"
        "輸入護欄驗證使用者請求，檢索護欄檢查取回內容，對話護欄約束流程，執行護欄控制工具呼叫，輸出護欄則過濾或修改回應。\n"
        "這些護欄的共同目的，是在內容、脈絡、對話與動作實際流經系統時驗證、限制、修改或阻擋不安全行為；"
        "它們可以留下控制與稽核紀錄，但不以完整重建模型全部內部推理為主要目的。後者屬可解釋性與透明度問題。"
    )
    e46["trap"] = (
        "第一，護欄不只在最外層輸入與輸出，也可介入檢索、對話和工具執行。第二，區分政策控制與模型解釋："
        "前者決定允許什麼內容或動作通過，後者嘗試說明模型為何得到某個結果。"
    )

    e47 = selected[47]["explanation"]
    e47["summary"] = (
        "正確答案是 B。適當大小且邊界合理的切分可提供較精細的檢索粒度，提升相關性並減少無關長上下文。"
    )
    e47["concept"] = (
        "在常見 RAG 流程中，長文件會切成可索引與取回的片段。切分策略會直接影響檢索粒度：片段過大可能混入多個議題，"
        "使相關訊號被無關內容稀釋；片段過小或切在不當邊界，又可能失去回答所需的上下文。\n"
        "因此效益不是『只要切分就每段主題單一』，而是透過合適的 chunk size、overlap、文件結構或語意邊界，"
        "讓取回內容更貼近問題，同時控制送入模型的無關長上下文。實務上應用 retrieval 與 QA 評估選擇策略。"
    )
    e47["answerReason"] = (
        "題幹痛點是檢索結果不相關或過度分散。妥善切分可讓檢索器在較合適的片段粒度上比對，"
        "取回較集中且相關的內容，並避免整份長文件進入提示，因此 B 最直接；但實際效果取決於切分策略與參數。"
    )
    e47["optionAnalysis"]["B"] = (
        "正確。適當大小、保留必要上下文且邊界合理的片段，能提高查詢與片段的對應精度，並減少無關文字進入提示。"
        "切得過小或邊界不當也可能傷害檢索，所以切分需要依文件與查詢評估，而不是自然保證每段主題單一。"
    )
    e47["trap"] = (
        "第一，切分的核心是調整檢索粒度與上下文品質，不是單純越短越好。第二，chunk size、overlap、結構／語意邊界需一起評估；"
        "推論加速若有發生，多半是上下文縮短的附帶效果。"
    )
    e47["references"].append({
        "title": "Document Segmentation Matters for Retrieval-Augmented Generation",
        "url": "https://aclanthology.org/2025.findings-acl.422/",
        "locator": "比較多種文件切分策略對 retrieval 與 downstream QA 的影響",
        "checkedAt": "2026-08-13",
    })

    e50 = selected[50]["explanation"]
    e50["concept"] = (
        "題目的產品需求是：以使用者給定的文章前綴為上下文，開放式地持續產生後續內容。"
        "這正是自迴歸 text generation 的典型任務，模型逐 token 預測後續文字並把新文字納回上下文。\n"
        "Sequence-to-sequence 則是較廣義的輸入序列到輸出序列模型架構，常用於翻譯、摘要等條件生成；"
        "技術上也可把前綴映射到後續序列，所以不是『做不到續寫』。但在題目提供的任務名稱中，Text Generation 直接描述開放式續寫，因而最精確。"
    )
    e50["answerReason"] = (
        "題幹要求依前文持續產生沒有固定標準答案的後續內容，C 直接命名這項 text generation 任務。"
        "A 是更廣的模型形式而非此需求最具體的任務分類，B 只補遮罩位置，D 只輸出標籤，因此選 C。"
    )
    e50["optionAnalysis"]["A"] = (
        "序列到序列是將輸入序列映射成輸出序列的廣義架構，典型應用包括翻譯與摘要，技術上也能設計成以前綴產生後續。"
        "但本題問最適合的任務類型，C 的 Text Generation 更直接、精確地命名開放式續寫，因此 A 不是最佳答案。"
    )
    e50["trap"] = (
        "第一，區分『任務名稱』與『可用模型架構』：Text Generation 是本題最直接的任務，seq2seq 則是可承載多種條件生成任務的廣義架構。"
        "第二，遮罩建模補指定缺口，文本分類輸出標籤，都不符合從結尾持續往後寫。"
    )
    e50["references"].append({
        "title": "Sequence to Sequence Learning with Neural Networks",
        "url": "https://arxiv.org/abs/1409.3215",
        "locator": "以輸入序列為條件，由編碼器／解碼器生成輸出序列的廣義架構",
        "checkedAt": "2026-08-13",
    })

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
