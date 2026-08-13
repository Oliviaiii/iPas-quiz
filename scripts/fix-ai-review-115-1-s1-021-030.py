"""Draft guarded explanation fixes from independent AI review, Q22 and Q25.

This script is intentionally not run by the reviewer. It removes unsupported
guarantees about unseen-anomaly detection and batching latency, refuses to edit
changed drafts, and preserves explanationStatus as draft.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-elementary-1-ai-foundation"
CHECKED_AT = "2026-08-13"

EXPECTED = {
    22: {
        "id": "aiap-elementary-115-01-ai-foundation-022",
        "answer": ["C"],
        "concept": (
            "設備異常偵測最常見的難處是標註稀缺：異常事件本來就罕見，新型故障的樣態事先"
            "又無從得知，很難事先把每種異常標好類別。\n官方學習指引說明，變分自編碼器由"
            "編碼器與解碼器組成，編碼器把輸入資料壓縮到低維的隱變量空間並學習資料的潛在"
            "分佈，解碼器再從隱變量空間重建資料；其應用場景之一正是異常檢測——「透過學習"
            "正常數據的分佈，能夠識別異常樣本」，並列出工業故障檢測為典型領域。實務上以"
            "重建誤差作為判斷依據：熟悉的正常型態重建得回來，誤差小；沒見過的異常型態重建"
            "不好，誤差明顯偏高，即可設門檻示警。"
        ),
        "answer_reason": (
            "題目給了兩個條件：缺乏完整異常標註資料，以及要辨識與一般運作型態顯著不同的"
            "狀態。C 只需要設備正常運作期間的溫度、震動與壓力資料就能訓練，模型學到的是"
            "「正常長什麼樣」而不是特定異常類別，因此連未曾出現過的新故障也能因重建誤差"
            "偏高而被抓出來，兩個條件同時被滿足。"
        ),
        "option_c": (
            "正確。以正常運作資料訓練編碼器與解碼器，模型學會的是正常感測型態的潛在分佈；"
            "推論時把新資料壓縮再重建，偏離正常分佈的狀態重建誤差會明顯升高，據此發出預警。"
            "整個流程不需要異常標註，也不受異常型態事先未知的限制。"
        ),
        "reference_count": 2,
    },
    25: {
        "id": "aiap-elementary-115-01-ai-foundation-025",
        "answer": ["A"],
        "option_b": (
            "說反了。單筆請求本來就獨占硬體，改成批次後還得等其他請求進來或等排隊計時器"
            "到期，回應時間只會持平或變長。真正縮短單筆延遲的手段是模型壓縮、量化或換用"
            "更快的硬體，而不是加大批次。"
        ),
        "reference_count": 2,
    },
}


def require(value: object, expected: object, label: str) -> None:
    if value != expected:
        raise RuntimeError(f"Guard failed for {label}")


def add_reference(explanation: dict, reference: dict, expected_count: int) -> None:
    references = explanation.get("references")
    if not isinstance(references, list) or len(references) != expected_count:
        raise RuntimeError("Reference list changed from the reviewed snapshot")
    if any(item.get("url") == reference["url"] for item in references):
        raise RuntimeError(f"Reference already exists: {reference['url']}")
    references.append(reference)


def main() -> None:
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    targets = {
        question["officialQuestionNumber"]: question
        for question in questions
        if question.get("sourceId") == SOURCE_ID
        and question.get("officialQuestionNumber") in EXPECTED
    }
    if set(targets) != set(EXPECTED):
        raise RuntimeError(f"Target question set changed: {sorted(targets)}")

    for number, guard in EXPECTED.items():
        question = targets[number]
        require(question.get("id"), guard["id"], f"Q{number} id")
        require(question.get("officialAnswer"), guard["answer"], f"Q{number} answer")
        require(question.get("explanationStatus"), "draft", f"Q{number} status")
        explanation = question.get("explanation")
        if not isinstance(explanation, dict):
            raise RuntimeError(f"Q{number}: explanation is missing")
        options = explanation.get("optionAnalysis")
        if not isinstance(options, dict):
            raise RuntimeError(f"Q{number}: option analysis is missing")

        if number == 22:
            require(explanation.get("concept"), guard["concept"], "Q22 concept")
            require(
                explanation.get("answerReason"),
                guard["answer_reason"],
                "Q22 answer reason",
            )
            require(options.get("C"), guard["option_c"], "Q22 option C")
            explanation["concept"] = (
                "設備異常偵測常面臨標註稀缺：異常事件罕見，新型故障又難以事先完整標記。"
                "變分自編碼器可只以正常資料學習潛在分佈，再以重建機率、重建誤差或其他分佈"
                "分數判斷新資料是否偏離正常，因而適合本題情境。\n這種方法不保證所有未見異常"
                "都會產生明顯分數差異；有些異常也可能被模型良好重建。實際效果仍取決於正常"
                "資料是否乾淨且具代表性、特徵與時間窗設計、模型容量、異常分數與門檻設定，"
                "並須以驗證資料評估漏報與誤報。"
            )
            explanation["answerReason"] = (
                "C 不要求先蒐齊每一種異常的標籤，而是先學習正常感測資料的分佈，再把顯著"
                "偏離該分佈的狀態列為異常候選，最符合題目條件。它有機會發現訓練時未列為"
                "已知類別的新故障，但是否能抓到仍須由異常分數、門檻與驗證結果確認。"
            )
            options["C"] = (
                "正確。VAE 可用正常運作資料學習潛在分佈，推論時以重建機率或其他異常分數"
                "判斷新資料是否偏離正常，不需要完整異常標註。這種設計可涵蓋部分未知異常，"
                "但不是對所有未見故障都能成功預警的保證。"
            )
            add_reference(
                explanation,
                {
                    "title": (
                        "VELC: A New Variational AutoEncoder Based Model for Time Series "
                        "Anomaly Detection"
                    ),
                    "url": "https://arxiv.org/abs/1907.01702",
                    "locator": (
                        "原始 VAE 可能良好重建異常樣本；研究另加潛在空間約束以改善異常分數，"
                        "顯示未知異常並非必然可由重建結果抓出"
                    ),
                    "checkedAt": CHECKED_AT,
                },
                guard["reference_count"],
            )
        elif number == 25:
            require(options.get("B"), guard["option_b"], "Q25 option B")
            options["B"] = (
                "B 不成立，因為 batching 的主要目標是提高資源利用率與整體吞吐量，而不是保證"
                "加快單一請求。單筆端到端延遲取決於排隊等待與批次運算效率的合計：等待湊批"
                "可能增加延遲，但在高負載下，更好的併行與較短的佇列等待也可能降低觀測到的"
                "請求延遲，因此不能寫成只會持平或變長。"
            )
            add_reference(
                explanation,
                {
                    "title": "NVIDIA Triton－Dynamic Batching & Concurrent Model Execution",
                    "url": (
                        "https://docs.nvidia.com/deeplearning/triton-inference-server/archives/"
                        "triton-inference-server-2600/user-guide/docs/tutorials/Conceptual_Guide/"
                        "Part_2-improving_resource_utilization/README.html"
                    ),
                    "locator": (
                        "動態 batching 與並行執行可透過提高資源利用率增加吞吐量，並可能降低"
                        "佇列等待與延遲；效果取決於模型與負載"
                    ),
                    "checkedAt": CHECKED_AT,
                },
                guard["reference_count"],
            )

        question["explanationStatus"] = "draft"

    QUESTIONS.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
