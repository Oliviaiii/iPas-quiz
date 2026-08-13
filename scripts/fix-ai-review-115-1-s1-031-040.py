"""Guarded draft explanation fixes from independent AI review, Q32-Q34.

This script is intentionally not run by the reviewer. It updates only exact
reviewed snapshots and preserves explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-elementary-1-ai-foundation"
TARGETS = {
    32: ("aiap-elementary-115-01-ai-foundation-032", ["C"], "3aaf9b46aa72de9926b4b352b24e747f7715acac81b15e6958c6162fc161f855"),
    33: ("aiap-elementary-115-01-ai-foundation-033", ["D"], "6d65999f3180f967650bcfe0322b9df6e1a480a50052269c9591521da03a6a42"),
    34: ("aiap-elementary-115-01-ai-foundation-034", ["C"], "a63e19cf5ebc35c15b89a9e72d29ef983d6201aec25476533f46584bb086a367"),
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

    e32 = selected[32]["explanation"]
    e32["optionAnalysis"]["B"] = (
        "物件偵測會輸出目標類別與矩形邊界框，能標示煙霧的大致位置；目標不需要接近方形，框的長寬比可依目標調整。"
        "但外接框仍包含非煙霧背景，無法像像素遮罩那樣精確表示煙霧實際覆蓋範圍，因此不如 C 符合題目。"
    )
    e32["references"].append({
        "title": "Mask R-CNN",
        "url": "https://arxiv.org/abs/1703.06870",
        "locator": "區分 bounding-box object detection 與額外預測像素 mask 的 instance segmentation",
        "checkedAt": "2026-08-13",
    })

    e33 = selected[33]["explanation"]
    e33["optionAnalysis"]["A"] = (
        "題目對 CNN 的描述只提以卷積層捕捉局部特徵，沒有提供 LSTM 式的循環記憶與門控機制，因此不是針對傳統 RNN 長期記憶問題的最直接答案。"
        "不過特殊的一維時序 CNN 可用擴張卷積與深層 receptive field 建模長期依賴，不能把所有 CNN 概括成只能看很短的鄰近時間窗。"
    )
    e33["trap"] = (
        "第一，本題明確問傳統 RNN 難以保留早期資訊時的改良架構，LSTM 是選項中最直接的答案。"
        "第二，這不代表卷積架構普遍不能處理序列長期依賴；題目考的是所列架構與問題描述的對應。"
    )
    e33["references"].append({
        "title": "An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling",
        "url": "https://arxiv.org/abs/1803.01271",
        "locator": "Temporal convolutional networks 在多個序列任務展示可與或優於 recurrent networks，且有較長 effective memory",
        "checkedAt": "2026-08-13",
    })

    e34 = selected[34]["explanation"]
    e34["summary"] = (
        "正確答案是 C。缺乏 AI 專業人力且要快速驗證時，雲端 AutoML 可降低模型選型與調參門檻，但仍需資料治理與專業驗證。"
    )
    e34["concept"] = (
        "平台選擇是在客製化、專業人力、時程、治理與供應商能力間取捨。從零建立框架成本最高；開源框架提供高度彈性，"
        "但需要團隊自行開發與維運；AutoML 可自動化多種資料處理、演算法比較與超參數搜尋，適合快速建立概念驗證；"
        "現成套件則可能最快部署，但客製能力與是否支援自有資料需依產品評估。\n"
        "AutoML 降低重複建模工作的門檻，不等於上傳資料就保證取得可安全上線的模型。理賠詐欺仍需領域專家確認標籤與成本、"
        "檢查資料洩漏和類別不平衡、選擇合適評估指標，並完成隱私、偏誤、資安與營運監控。"
    )
    e34["answerReason"] = (
        "題目明示缺乏 AI 專業人員且需快速驗證，C 的 AutoML 最直接降低模型選型與調參的時間及技能門檻，"
        "又能利用去識別化後的自有資料做概念驗證，因此是四項中的最佳起點；這個選擇不免除後續專業驗證與治理。"
    )
    e34["optionAnalysis"]["B"] = (
        "開源框架可高度客製化，也能依公司資料與風險成本設計模型；但通常需要資料科學與 MLOps 能力，"
        "不符合題目當下缺乏專業人力且要快速驗證的限制。它不必然比其他方案效果更好，成效仍取決於資料、方法與驗證。"
    )
    e34["optionAnalysis"]["C"] = (
        "正確。AutoML 可自動化模型比較與超參數搜尋，讓團隊較快用自有資料建立可評估的概念驗證。"
        "但仍要由領域與風險人員處理資料品質、標籤、類別不平衡、指標、隱私與上線監控，不能把自動化等同於免專業。"
    )
    e34["optionAnalysis"]["D"] = (
        "現成詐欺偵測套件可能部署很快，部分產品也支援以客戶資料設定規則或調校模型；是否適合取決於資料介接、透明度、"
        "客製能力與法遵要求。題目強調要用既有資料快速驗證模型，AutoML 對此描述較直接，因此 D 不是最佳選項。"
    )
    e34["trap"] = (
        "先用人力、時程與資料條件判斷最適合的起點；AutoML 的優勢是自動化反覆建模工作，不是保證模型可直接上線。"
        "高風險金融用途仍需資料治理、獨立驗證、法遵與持續監控。"
    )

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
