"""Guarded draft explanation fixes from independent AI review, Q12 and Q13.

Q12 asked a later reviewer to check the CLIP paper's method section; it confirms
the draft's framing exactly. Q13 asked whether a more authoritative source than
Wikipedia exists for "vibe coding"; Merriam-Webster now carries a dictionary
entry. Both notes are closed and the sources added.

This script is intentionally not run by the reviewer. It updates only exact
reviewed snapshots and preserves explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-elementary-2-genai-planning"
TARGETS = {
    12: ("aiap-elementary-115-02-genai-planning-012", ["A"],
         "68dc55cc84ae16724bdce2b3c6b470d84c5a8cfd9d3515461c0ee39eea46c453"),
    13: ("aiap-elementary-115-02-genai-planning-013", ["D"],
         "49258bfa6f2070623c96329af5b1f490164f5ab771bde945d1540abf1317fe54"),
}

# Q12：原稿只核對了摘要，把方法節（含溫度縮放）列為待查。方法節逐字確認：訓練
# 目標就建立在餘弦相似度上、交叉熵是套在相似度分數之上的損失，零樣本推論也是
# 先算餘弦相似度再以溫度縮放。選項 C 的立論因此成立。
OLD_NOTE_12 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：CLIP 訓練時的對比式損失以圖文嵌入的餘弦相似度作為打分基礎，"
    "再以交叉熵形式優化；本批僅重新核對論文摘要與餘弦相似度定義，論文方法節細節（如溫度縮放）未逐段查證，"
    "選項 C 解析因此僅就「推論時衡量相符程度的量尺」立論，建議複核者對照 CLIP 論文方法節確認表述。查核日期 2026-08-07。"
)
NEW_NOTE_12 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿把 CLIP 論文方法節列為待查，獨立 AI 複核已逐字核對："
    "第 2.2 節「jointly training an image encoder and text encoder to maximize the cosine similarity of the image and text "
    "embeddings of the N real pairs in the batch……We optimize a symmetric cross entropy loss over these similarity scores」，"
    "第 2.5 節「The cosine similarity of these embeddings is then calculated, scaled by a temperature parameter τ, and "
    "normalized into a probability distribution via a softmax」。可見餘弦相似度是打分的量尺、交叉熵是套在相似度分數之上的訓練損失，"
    "溫度僅為縮放參數；選項 A 與選項 C 的立論皆成立。待查項目結案。查核日期 2026-08-30。"
)

# Q13：原稿以維基詞條佐證 Vibe Coding 的起源，並問是否有更權威的出處。
# Merriam-Webster 已收錄該詞的詞典條目，改列為第二筆來源。
OLD_NOTE_13 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：Vibe Coding 為 2025 年出現的新詞，官方學習指引未收錄，"
    "術語起源沿用維基百科詞條佐證，建議複核者確認是否有更權威的一手出處可替換。查核日期 2026-08-07。"
)
NEW_NOTE_13 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿問 Vibe Coding 是否有更權威的出處可替換維基詞條，"
    "獨立 AI 複核已找到並補入 Merriam-Webster 的詞典條目：「writing computer code in a somewhat careless fashion, with AI assistance」，"
    "並載明「the coder does not need to understand how or why the code works, and often will have to accept that a certain "
    "number of bugs and glitches will be present」，正可佐證選項 B、D 對審查必要性與品質依賴的敘述。"
    "官方學習指引確實未收錄此詞（已全文檢索確認），維基詞條保留作為起源與時間點的補充。待查項目結案。查核日期 2026-08-30。"
)
NEW_REFERENCE_13 = {
    "title": "Merriam-Webster－vibe coding（Slang & Trending）",
    "url": "https://www.merriam-webster.com/slang/vibe-coding",
    "locator": (
        "詞條定義逐字核對：writing computer code in a somewhat careless fashion, with AI assistance；"
        "說明段：In vibe coding the coder does not need to understand how or why the code works, and often will have to "
        "accept that a certain number of bugs and glitches will be present；並記載該詞自 2025 年初開始廣為使用"
    ),
    "checkedAt": "2026-08-30",
}


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

    for number, old, new in ((12, OLD_NOTE_12, NEW_NOTE_12), (13, OLD_NOTE_13, NEW_NOTE_13)):
        explanation = selected[number]["explanation"]
        if explanation.get("editorialNote") != old:
            raise RuntimeError(f"Guard failed for Q{number} editorialNote snapshot")
        explanation["editorialNote"] = new

    selected[13]["explanation"]["references"].insert(1, NEW_REFERENCE_13)

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
