"""修正五處原文連寫錯字（漏空格），同步更新題庫與對應 payload 的 new。

這五處都是「兩個英文字被連在一起」的排版錯誤，不是識別字或函式名：

    constrow            -> const row          （statsmodels 摘要表的 const 那一列）
    ExperimentTracking  -> Experiment Tracking
    LateFusion          -> Late Fusion
    rollingfeatures     -> rolling features
    rankcorrelations    -> rank correlations

錯字來自白話化之前的原稿，改寫時刻意照原樣重現（見 HANDOVER），因此這一支
腳本同時改兩個地方：

* `app/data/questions.json` 的該欄位。
* 對應 payload 的 `new`（不動 `old` 與 `oldSha256`——那是改寫當下原文的封存，
  改了就失去稽核意義）。

只插入一個空格，其餘一字不動；腳本會逐字驗證這一點。
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
PAYLOAD_DIR = ROOT / "content" / "plain-language"

# (sourceId, 題號, 欄位, 連寫錯字, 正確寫法)
FIXES = [
    ("aiap-114-intermediate-2-big-data", 50, "B", "constrow", "const row"),
    ("aiap-115-intermediate-1-ai-tech-planning", 49, "concept",
     "ExperimentTracking", "Experiment Tracking"),
    ("aiap-115-intermediate-1-ai-tech-planning", 50, "answerReason",
     "LateFusion", "Late Fusion"),
    ("aiap-115-intermediate-1-big-data", 22, "concept",
     "rollingfeatures", "rolling features"),
    ("aiap-115-intermediate-1-big-data", 24, "concept",
     "rankcorrelations", "rank correlations"),
]

PROSE_FIELDS = ("concept", "answerReason", "trap")


def patch(text: str, bad: str, good: str, tag: str) -> str:
    """把 bad 換成 good，並證明只多了一個空格。"""
    if text.count(bad) != 1:
        raise RuntimeError(f"{tag}: 預期剛好一處「{bad}」，實際 {text.count(bad)} 處")
    fixed = text.replace(bad, good)
    if fixed.replace(" ", "") != text.replace(" ", ""):
        raise RuntimeError(f"{tag}: 除了空格以外還動到別的字")
    if len(fixed) != len(text) + 1:
        raise RuntimeError(f"{tag}: 長度應該只增加 1，實際 {len(fixed) - len(text)}")
    return fixed


def main() -> None:
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    index = {(q["sourceId"], q["officialQuestionNumber"]): q for q in questions}

    payloads: dict[Path, dict] = {}

    for source_id, number, field, bad, good in FIXES:
        tag = f"{source_id} Q{number} {field}"
        question = index.get((source_id, number))
        if question is None:
            raise RuntimeError(f"{tag}: 題庫裡找不到這一題")

        explanation = question["explanation"]
        target = explanation if field in PROSE_FIELDS else explanation["optionAnalysis"]
        target[field] = patch(target[field], bad, good, tag + " (題庫)")

        # 同步 payload 的 new，讓 check-plain-language.py 仍能對得起來。
        touched = False
        for path in sorted(PAYLOAD_DIR.glob(f"{source_id}-*.json")):
            payload = payloads.get(path) or json.loads(path.read_text(encoding="utf-8"))
            payloads[path] = payload
            for item in payload["items"]:
                if item["officialQuestionNumber"] != number:
                    continue
                entry = (item.get("optionAnalysis") or item.get("prose") or {}).get(field)
                if entry is None or bad not in entry["new"]:
                    continue
                entry["new"] = patch(entry["new"], bad, good, tag + f" ({path.name})")
                touched = True
        if not touched:
            raise RuntimeError(f"{tag}: 找不到含這個錯字的 payload")
        print(f"{tag}: {bad} -> {good}")

    QUESTIONS.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    for path, payload in payloads.items():
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(f"改了題庫 {len(FIXES)} 處、payload {len(payloads)} 個")


if __name__ == "__main__":
    main()
