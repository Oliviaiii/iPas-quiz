"""Guarded draft explanation fix from independent AI review, Q18.

This script is intentionally not run by the reviewer. It corrects the claim
that a fixed non-zero temperature removes decoding randomness. Every edit is
guarded by the exact reviewed text and keeps explanationStatus draft.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-114-elementary-4-genai-planning"
QUESTION_NUMBER = 18
QUESTION_ID = "aiap-elementary-114-04-genai-planning-018"

EXPECTED = {
    "concept": (
        "題目一次列出四個可疑因素，要判斷哪一個才是造成「品質波動」的主因，關鍵線索"
        "藏在題幹裡：生成溫度已固定為 0.6，解碼的隨機性已被控制在固定水準，回覆品質"
        "卻仍時好時壞——這說明變異來自每次送進模型的內容不同，而不是模型產生文字時的"
        "抖動。\n調查結果也直接印證：檢索到的政策有時是最新版、有時是過時文件。在檢索"
        "增強生成的架構中，檢索結果會被放進提示交給模型生成；同一個問題若取到不同版本"
        "的政策，答案當然會不一樣。這是資料正確性的問題，無法靠生成端的參數或措辭補救。"
    ),
    "answerReason": (
        "溫度固定卻仍有波動，代表變異源不在解碼隨機性而在輸入內容；四個因素中，只有"
        "檢索版本不一致會讓同一個問題得到不同的事實依據。何況錯誤的政策內容一旦進入"
        "提示，後續的表達控制只會讓錯誤答案講得更順口，所以必須優先解決 D。"
    ),
    "optionA": (
        "溫度參數控制生成的隨機性，調低會讓輸出更保守一致，在追求措辭穩定的客服場景"
        "確實常用。但題幹已說明溫度固定在 0.6，再往下調頂多減少用字變化，無法讓檢索到"
        "的過時政策變回正確版本，處理的是表達層而非事實層。"
    ),
    "trap": (
        "第一，先判斷變異來源是「輸入內容」還是「解碼隨機性」：溫度既然固定，問題就不在"
        "後者。第二，檢索增強生成系統的排錯順序應該從資料來源與檢索品質往生成端走，事實"
        "錯誤沒辦法用提示設計或參數調整補回來。"
    ),
}


def require(value: object, expected: object, label: str) -> None:
    if value != expected:
        raise RuntimeError(f"Guard failed for {label}")


def main() -> None:
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    targets = [
        question
        for question in questions
        if question.get("sourceId") == SOURCE_ID
        and question.get("officialQuestionNumber") == QUESTION_NUMBER
    ]
    if len(targets) != 1:
        raise RuntimeError(f"Expected one target question, found {len(targets)}")

    question = targets[0]
    require(question.get("id"), QUESTION_ID, "Q18 id")
    require(question.get("officialAnswer"), ["D"], "Q18 official answer")
    require(question.get("explanationStatus"), "draft", "Q18 status")
    explanation = question.get("explanation")
    if not isinstance(explanation, dict):
        raise RuntimeError("Q18 explanation is missing")
    options = explanation.get("optionAnalysis")
    if not isinstance(options, dict):
        raise RuntimeError("Q18 option analysis is missing")

    require(explanation.get("concept"), EXPECTED["concept"], "Q18 concept")
    require(
        explanation.get("answerReason"),
        EXPECTED["answerReason"],
        "Q18 answer reason",
    )
    require(options.get("A"), EXPECTED["optionA"], "Q18 option A")
    require(explanation.get("trap"), EXPECTED["trap"], "Q18 trap")

    explanation["concept"] = (
        "題目一次列出四個因素，排序優先級要看哪個會直接改變回答所依據的事實。溫度固定"
        "為 0.6 並不代表每次輸出完全相同；0.6 仍會進行取樣，因此解碼本身仍可能產生措辭"
        "差異。但調查已發現檢索結果有時是最新政策、有時是過時文件，這會讓模型在不同查詢"
        "中取得互相衝突的事實依據。\n在 RAG 中，檢索內容會放入提示供模型回答。若來源版本"
        "錯誤，調低溫度或加強措辭約束都無法把舊政策變成新政策。因此應先確保索引同步、"
        "版本篩選與排序正確，再處理提示、微調語料及解碼參數。"
    )
    explanation["answerReason"] = (
        "溫度 0.6 仍可能帶來生成差異，但題幹已找到更直接且高風險的波動來源：同一問題會"
        "取到不同版本的政策。這種檢索不一致會改變答案的事實基礎，優先級高於措辭與隨機性"
        "的調整，因此選 D。"
    )
    options["A"] = (
        "溫度控制取樣隨機性；即使固定為 0.6，每次生成仍可能不同，降低溫度可減少措辭變化。"
        "但它不能修正檢索到的過時政策，故不是題目所揭露之主要事實錯誤的優先解法。"
    )
    explanation["trap"] = (
        "第一，固定溫度不等於固定輸出；非零溫度仍有取樣隨機性。第二，RAG 排錯要先處理"
        "會改變事實依據的來源與檢索品質，再調整提示、微調語料與生成參數。"
    )
    question["explanationStatus"] = "draft"

    QUESTIONS.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
