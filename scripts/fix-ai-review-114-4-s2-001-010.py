"""Draft guarded fixes from independent AI review, 114-4 S2 Q1-Q10.

The reviewer does not execute this script. It corrects two overstatements and
adds missing first-party or primary references. Every target is protected by a
SHA-256 snapshot of the reviewed draft and remains ``draft`` after repair.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-114-elementary-4-genai-planning"
CHECKED_AT = "2026-08-13"

EXPECTED_SHA256 = {
    1: "b56ace71ff0a7e44b8ac9b283feab2342e50f7b03f507e6384607f00ec56aad0",
    2: "93853236879d93255d8252fd116e13b47cae891ac0ac42b32db28b4c4fc33ee5",
    3: "142dcb211b2488421ccdd9e29954d504ad01785e859f71d66dd6b8d11fd23c0f",
    4: "bf48598f1b7f177c524e27c5d2bfecd0949e42ba3af9cfc38b976e32e8537e9a",
    9: "16cf4b8c9a64e36814fca63a7cf14cbb1c9d394a74e11ae91cc51f56f7535026",
}


def snapshot_sha256(question: dict) -> str:
    snapshot = {
        "id": question["id"],
        "officialAnswer": question["officialAnswer"],
        "explanationStatus": question["explanationStatus"],
        "explanation": question["explanation"],
    }
    payload = json.dumps(
        snapshot,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def add_reference(explanation: dict, reference: dict) -> None:
    references = explanation.get("references")
    if not isinstance(references, list):
        raise RuntimeError("Explanation references are missing")
    url = reference["url"]
    if any(existing.get("url") == url for existing in references):
        raise RuntimeError(f"Reference URL already exists: {url}")
    references.append(reference)


def main() -> None:
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    targets = {
        question["officialQuestionNumber"]: question
        for question in questions
        if question.get("sourceId") == SOURCE_ID
        and question.get("officialQuestionNumber") in EXPECTED_SHA256
    }
    if set(targets) != set(EXPECTED_SHA256):
        raise RuntimeError(f"Target question set changed: {sorted(targets)}")

    for number, expected_hash in EXPECTED_SHA256.items():
        question = targets[number]
        actual_hash = snapshot_sha256(question)
        if actual_hash != expected_hash:
            raise RuntimeError(
                f"Q{number}: reviewed snapshot changed; expected {expected_hash}, "
                f"got {actual_hash}"
            )
        explanation = question["explanation"]

        if number == 1:
            add_reference(
                explanation,
                {
                    "title": "Microsoft Learn－Overview of creating apps in Power Apps",
                    "url": "https://learn.microsoft.com/en-us/power-apps/maker/",
                    "locator": (
                        "Model-driven apps：從資料模型與核心業務資料、流程建立 "
                        "forms、views、business rules 與 process flows"
                    ),
                    "checkedAt": CHECKED_AT,
                },
            )
        elif number == 2:
            explanation["concept"] = (
                "題目的條件有三個：資料分散在不同部門或機構、資料屬於敏感文本、"
                "而且模型要能「持續優化」。能同時滿足這三點的，是改變訓練架構"
                "而非只加強資料保護。\n"
                "聯邦學習讓各方在本地用自己的資料訓練，只把模型參數或梯度更新"
                "送出彙整成全域模型，再下發繼續訓練，因此原始文本不必集中上傳。"
                "但模型更新仍可能洩漏參與者資料資訊，所以聯邦學習是降低原始資料"
                "集中與外洩風險的訓練架構，不等於單獨保證隱私；實務上常搭配安全"
                "聚合或差分隱私等機制。"
            )
            explanation["optionAnalysis"]["D"] = (
                "正確。各部門或機構在本地訓練、只上傳模型更新，中央彙整為全域"
                "模型後再下發，原始敏感文本不必離開持有方，模型仍可持續吸收各方"
                "資料而優化，最符合題目情境。需注意模型更新本身可能洩漏資訊；若要"
                "達到更強的隱私保護，仍需搭配安全聚合、差分隱私等控制。"
            )
            add_reference(
                explanation,
                {
                    "title": (
                        "NIST－Protecting Model Updates in Privacy-Preserving "
                        "Federated Learning"
                    ),
                    "url": (
                        "https://www.nist.gov/blogs/cybersecurity-insights/"
                        "protecting-model-updates-privacy-preserving-federated-learning"
                    ),
                    "locator": (
                        "基本 FedAvg 不提供 input privacy；個別更新可能遭攻擊，"
                        "secure aggregation 可隱藏個別更新"
                    ),
                    "checkedAt": CHECKED_AT,
                },
            )
        elif number == 3:
            add_reference(
                explanation,
                {
                    "title": "IBM DevOps Test Virtualization－Tester Guide",
                    "url": (
                        "https://www.ibm.com/docs/en/devops-testvirtualization/11.0.4"
                        "?topic=guide-tester-service-virtualization"
                    ),
                    "locator": (
                        "使用 virtual services 或 stubs 模擬尚不可用、難以使用或"
                        "成本高昂的真實服務，供 integration testers 驗證"
                    ),
                    "checkedAt": CHECKED_AT,
                },
            )
        elif number == 4:
            explanation["concept"] = (
                "社交互動資料的本質是圖：節點是使用者，邊是互動關係，還可能帶有"
                "方向、強度與時間等屬性；語言模型的輸入則是線性的 token 序列。\n"
                "圖提示必須把圖結構編碼成可放入提示的序列。當圖過大、編碼受上下文"
                "長度限制，或模型把結構描述當成一般段落而未真正利用拓撲時，多重"
                "路徑、環狀關係與全域樞紐等資訊可能被壓縮、忽略或失真。資訊損失"
                "並非每次都必然發生，但確實是圖轉文字提示時需處理的主要風險。"
            )
            explanation["optionAnalysis"]["A"] = (
                "正確。圖是非線性結構，文字提示是線性序列；序列化時必須選擇表示"
                "方式與順序。當圖規模超出 token 預算，或模型未能正確利用結構描述"
                "時，多重路徑、環狀關係與全域拓撲特徵可能被壓縮、忽略或失真，"
                "使推理缺少關鍵脈絡。"
            )
            add_reference(
                explanation,
                {
                    "title": (
                        "Can LLMs Effectively Leverage Graph Structural Information "
                        "through Prompts, and Why?"
                    ),
                    "url": "https://openreview.net/forum?id=L2jRavXRxs",
                    "locator": (
                        "TMLR 2024：LLM 傾向把自然語言編碼的圖結構當作上下文"
                        "段落，而非理解為圖結構"
                    ),
                    "checkedAt": CHECKED_AT,
                },
            )
        elif number == 9:
            add_reference(
                explanation,
                {
                    "title": "Anthropic－Effective context engineering for AI agents",
                    "url": (
                        "https://www.anthropic.com/engineering/"
                        "effective-context-engineering-for-ai-agents"
                    ),
                    "locator": (
                        "Context engineering：在推理時策展與維持最佳資訊集合，"
                        "涵蓋 prompts 以外的 tools、外部資料與訊息歷史"
                    ),
                    "checkedAt": CHECKED_AT,
                },
            )

        question["explanationStatus"] = "draft"

    QUESTIONS.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
