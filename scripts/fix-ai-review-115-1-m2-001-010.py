"""Guarded draft fixes from independent AI review, 115-1 中級第二科 Q1–Q10.

Two classes of fix:
  * Q1, Q3–Q7, Q9, Q10 locators claim 「附圖」 but those eight questions carry no
    figure in the bank and none on the official PDF; each is replaced by a
    precise page reference.
  * Q2 and Q8 editorialNote still say the stored PNG is an all-black image
    awaiting repair; scripts/fix-ai-review-115-1-m2-figures.py has since
    recomposited both formulas from the PDF soft mask, so the note is updated.
This script preserves explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-intermediate-1-big-data"
TARGETS = {
    1: ("aiap-intermediate-115-01-big-data-001", ["A"], "3d16beb314db5b296400969a31fcbd4a4117afdcc12a512c194d01882e3c68ea"),
    2: ("aiap-intermediate-115-01-big-data-002", ["A"], "cc665d342e1f817fa730f35aa8d46d988b36a6de19b3f17ba23bdc88578970d5"),
    3: ("aiap-intermediate-115-01-big-data-003", ["B"], "aeb3675e7fe0d28a94f01452d6553aa6f8b1b15f8d34ee1af3df862fb0e2d709"),
    4: ("aiap-intermediate-115-01-big-data-004", ["A"], "36b3958e8b6326d17cbf793f0f27dc8c8594e2cec12440db289c092e4a424647"),
    5: ("aiap-intermediate-115-01-big-data-005", ["A"], "7b896cdf763f63c99705141fac1ef1c492663c64ae5ddaa1cccef71895d35b92"),
    6: ("aiap-intermediate-115-01-big-data-006", ["D"], "d7d51b662b7e4c0c5a96461a303b50a4d0a6ce8b58d09b2c9bb2633b15b54cb1"),
    7: ("aiap-intermediate-115-01-big-data-007", ["B"], "70708effeb4f8739336d1269abdb722d60126bc351932f37634326ff10888395"),
    8: ("aiap-intermediate-115-01-big-data-008", ["D"], "f9e9ec2a8f5b4473cb4ee7e4723b08bece2ab381b0e210d06c204adda6fe7ded"),
    9: ("aiap-intermediate-115-01-big-data-009", ["B"], "fc279840fe285561ee3ff9757d6da4b47f006cc2efaa3ba49ec75b09830b0fc5"),
    10: ("aiap-intermediate-115-01-big-data-010", ["B"], "2f86194203ebdc4e10ca61e3b61635923cedfae1ac6507545a3ac81ac05f67ba"),
}

NEW_LOCATORS = {
    1: "PDF 第 1 頁：第 1 題題幹、(A)～(D) 選項與左欄官方答案 A；本題無附圖",
    2: "PDF 第 1 頁：第 2 題題幹、吉尼不純度公式附圖 G = 1 − Σ(i=1…k) pᵢ²、(A)～(D) 選項與左欄官方答案 A",
    3: "PDF 第 1 頁：第 3 題題幹（平均每小時 12 通）、(A)～(D) 選項與左欄官方答案 B；本題無附圖",
    4: "PDF 第 1～2 頁：第 4 題題幹與 (A)～(C) 選項、左欄官方答案 A（第 1 頁）、(D) 選項（第 2 頁）；本題無附圖",
    5: "PDF 第 2 頁：第 5 題題幹（|Z| ≥ 2 觸發警示、某特徵 Z = -2）、(A)～(D) 選項與左欄官方答案 A；本題無附圖",
    6: "PDF 第 2 頁：第 6 題題幹（女士品茶、α=0.05）、(A)～(D) 選項與左欄官方答案 D；本題無附圖",
    7: "PDF 第 2 頁：第 7 題題幹（40 名患者前後各測一次）、(A)～(D) 選項與左欄官方答案 B；本題無附圖",
    8: "PDF 第 2～3 頁：第 8 題題幹（μ₀=36、σ=16、n=9、x̄=40、Z₀.₀₅=1.645）、Z 檢定公式附圖 Z=(x̄−μ₀)/(σ/√n) 與 (A)(B) 選項、左欄官方答案 D（第 2 頁）、(C)(D) 選項（第 3 頁）",
    9: "PDF 第 3 頁：第 9 題題幹（α 由 0.05 降至 0.01）、(A)～(D) 選項與左欄官方答案 B；本題無附圖",
    10: "PDF 第 3 頁：第 10 題題幹（280 個特徵、訓練 AUC 0.94／測試 0.68）、(A)～(D) 選項與左欄官方答案 B；本題無附圖",
}

OLD_NOTE_2 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。已於 2026-08-12"
    "目視官方 PDF 第 1 頁，附圖確為 G = 1 − Σ(i=1…k) pᵢ²；資料庫現有本機 PNG 為全黑影像，需另行修復素材後再確認前端顯示。"
)
NEW_NOTE_2 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。附圖確為 G = 1 − Σ(i=1…k) pᵢ²，"
    "已於 2026-08-30 目視官方 PDF 第 1 頁核對；原本機 PNG 因匯入時遺漏 PDF 軟遮罩而呈全黑，"
    "已由 scripts/fix-ai-review-115-1-m2-figures.py 依原圖與 alpha 遮罩重新合成修復。"
)

OLD_NOTE_8 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。已於 2026-08-12"
    "目視官方 PDF 第 2 頁，附圖公式確為 Z=(x̄−μ₀)/(σ/√n)；資料庫現有本機 PNG 為全黑影像，需另行修復素材後再確認前端顯示。"
)
NEW_NOTE_8 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。附圖公式確為 Z=(x̄−μ₀)/(σ/√n)，"
    "已於 2026-08-30 目視官方 PDF 第 2 頁核對；原本機 PNG 因匯入時遺漏 PDF 軟遮罩而呈全黑，"
    "已由 scripts/fix-ai-review-115-1-m2-figures.py 依原圖與 alpha 遮罩重新合成修復。"
)


def snapshot_hash(question: dict) -> str:
    snapshot = {key: question[key] for key in ("id", "officialAnswer", "explanationStatus", "explanation")}
    payload = json.dumps(snapshot, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    selected = {
        q["officialQuestionNumber"]: q
        for q in questions
        if q.get("sourceId") == SOURCE_ID and q.get("officialQuestionNumber") in TARGETS
    }
    if set(selected) != set(TARGETS):
        raise RuntimeError(f"Expected targets {sorted(TARGETS)}, found {sorted(selected)}")
    for number, (question_id, answer, digest) in TARGETS.items():
        question = selected[number]
        if question.get("id") != question_id or question.get("officialAnswer") != answer:
            raise RuntimeError(f"Guard failed for Q{number} identity or answer")
        if question.get("explanationStatus") != "draft" or snapshot_hash(question) != digest:
            raise RuntimeError(f"Guard failed for Q{number} status or reviewed snapshot")
        expected_figures = 1 if number in (2, 8) else 0
        if len(question.get("figures") or []) != expected_figures:
            raise RuntimeError(f"Guard failed for Q{number}: unexpected figure count")

    for number, locator in NEW_LOCATORS.items():
        reference = selected[number]["explanation"]["references"][0]
        if reference["locator"] != f"第 {number} 題題幹、附圖、選項與官方答案":
            raise RuntimeError(f"Guard failed for Q{number} locator snapshot")
        reference["locator"] = locator
        reference["checkedAt"] = "2026-08-30"

    for number, old, new in ((2, OLD_NOTE_2, NEW_NOTE_2), (8, OLD_NOTE_8, NEW_NOTE_8)):
        explanation = selected[number]["explanation"]
        if explanation.get("editorialNote") != old:
            raise RuntimeError(f"Guard failed for Q{number} editorialNote snapshot")
        explanation["editorialNote"] = new

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
