"""Guarded draft explanation fixes from independent AI review, Q18 and Q20.

Both notes ask a later reviewer to check the wording against the official
intermediate teaching material. No such material exists: iPAS publishes study
guides for the two elementary subjects only, the learning-resources page lists
just the twelve exam papers for the intermediate level, and no intermediate
guide is cited anywhere in the 600-question bank. The notes are closed with
that finding and with why each answer holds without it.

This script is intentionally not run by the reviewer. It updates only exact
reviewed snapshots and preserves explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-114-intermediate-2-ai-tech-planning"
TARGETS = {
    18: ("aiap-intermediate-114-02-ai-tech-planning-018", ["D"],
         "b6da65c16ac64325fdb100cb9e6cc9433d736d712c3f093a88a19b0979a7eab1"),
    20: ("aiap-intermediate-114-02-ai-tech-planning-020", ["B"],
         "0fa72f073fc5c789e4b9eda07ca42f71a4131bc568e911fc032c856ccadf2671"),
}

# 官方僅出版初級兩科的學習指引；中級的學習資源頁只列 6 份試題公告，題庫 600 題
# 亦無任何中級學習指引引用。凡是「待確認官方教材用語」的待查項目，方向上都查不到。
NO_GUIDE = (
    "獨立 AI 複核查證：官方僅出版初級兩科學習指引，中級並無對應的學習指引——"
    "學習資源頁的中級區塊只列 6 份試題公告，全站 600 題也無任何中級學習指引引用，"
    "以既有命名規則推測的網址均回 404。凡以官方中級教材為對象的用語查證，方向上皆無資料可查。"
)

OLD_NOTE_18 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
    "「Attention Collapse」在研究文獻中有多種用法，本題已由題幹明確限定為權重過於平均，故依此定義解讀；"
    "待複核確認官方學習材料是否採相同術語。"
)
NEW_NOTE_18 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
    "「Attention Collapse」在研究文獻中有多種用法，本題已由題幹明確限定為「注意力分布過於平均」，故依此定義解讀。"
    f"原稿把「官方學習材料是否採相同術語」列為待查，{NO_GUIDE}"
    "惟本題答案不受術語出處影響：題幹自帶定義，四個選項中只有 D 的稀疏化約束會使權重集中，"
    "A 依縮放點積的原理反而使分布更平均、B 的雜訊不保證強化關鍵位置、C 的 ReLU 缺乏正規化定義。待查項目結案。"
    "查核日期 2026-08-30。"
)

OLD_NOTE_20 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
    "A 的梯度懲罰若特指 WGAN-GP，也屬常見且有效的訓練穩定方法，因此題目存在解釋空間；"
    "本站仍依官方答案 B 判定，待人工複核題目所依教材的用語與層級。"
)
NEW_NOTE_20 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
    "A 的梯度懲罰若特指 WGAN-GP，也屬常見且有效的訓練穩定方法，因此題目確實存在解釋空間，此點保留供人工複核者知悉。"
    f"原稿把「題目所依教材的用語與層級」列為待查，{NO_GUIDE}"
    "獨立 AI 複核就選項文字本身比較後仍支持官方答案 B：選項 A 只寫到「加入梯度懲罰以穩定訓練過程」，"
    "未提 Wasserstein critic 目標，梯度懲罰在 WGAN-GP 中的作用是施加 Lipschitz 約束、取代 weight clipping；"
    "選項 B 的 Wasserstein 損失替換才是 WGAN 論文用以改善訓練穩定並討論 mode collapse 的核心變更。待查項目結案。"
    "查核日期 2026-08-30。"
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

    for number, old, new in ((18, OLD_NOTE_18, NEW_NOTE_18), (20, OLD_NOTE_20, NEW_NOTE_20)):
        explanation = selected[number]["explanation"]
        if explanation.get("editorialNote") != old:
            raise RuntimeError(f"Guard failed for Q{number} editorialNote snapshot")
        explanation["editorialNote"] = new

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
