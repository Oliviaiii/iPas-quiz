"""把 114 年第二次中級大數據第 43 題的批次報告由 pass 改判 corrected。

原稿選項 (A) 的解析開頭寫「正確。原因 B 與 C 都不成立……」——官方答案是 (B)，
(A) 並非正確選項，開頭的「正確。」與後面自己的說明互相矛盾。白話化改寫已把
開頭改成「正確答案不是這一組。」，矛盾消失，因此該題的獨立複核結果應由 pass
改為 corrected 並補上 finding。

只改 reviews/ai-independent/ 下的批次報告，不動題庫。
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reviews" / "ai-independent" / "aiap-114-intermediate-2-big-data-041-050.json"
NUMBER = 43

FINDING = {
    "type": "explanation-inconsistency",
    "location": "explanation.optionAnalysis.A",
    "summary": "選項 (A) 的解析以「正確。」開頭，但官方答案是 (B)，且該段自己接著說明"
               "「原因 B 與原因 C 都不成立」，開頭標記與內容互相矛盾。",
    "resolution": "白話化改寫時把開頭改為「正確答案不是這一組。」，保留原本的技術判斷"
                  "不變，矛盾即消失。",
    "detectedAt": "2026-09-07",
    "resolvedAt": "2026-09-08",
}


def main() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    for item in report["items"]:
        if item["officialQuestionNumber"] != NUMBER:
            continue
        if item["result"] != "pass":
            raise RuntimeError(f"Q{NUMBER} 目前是 {item['result']}，不是預期的 pass")
        if item["findings"]:
            raise RuntimeError(f"Q{NUMBER} 已經有 findings，請先確認")
        item["result"] = "corrected"
        item["findings"] = [FINDING]
        break
    else:
        raise RuntimeError(f"報告裡找不到 Q{NUMBER}")

    counts = report["counts"]
    if counts["pass"] < 1:
        raise RuntimeError("pass 計數已為 0，無法再減")
    counts["pass"] -= 1
    counts["corrected"] += 1

    tallied = {"pass": 0, "corrected": 0, "humanDecision": 0, "blocked": 0}
    key = {"pass": "pass", "corrected": "corrected",
           "human-decision": "humanDecision", "blocked": "blocked"}
    for item in report["items"]:
        tallied[key[item["result"]]] += 1
    if tallied != counts:
        raise RuntimeError(f"counts 對不上：報告寫 {counts}，實際數出來 {tallied}")

    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Q{NUMBER}: pass -> corrected；counts 更新為 {counts}")


if __name__ == "__main__":
    main()
