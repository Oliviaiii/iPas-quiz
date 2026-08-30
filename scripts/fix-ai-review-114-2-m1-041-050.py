"""Guarded draft explanation fixes from independent AI review, Q42, Q44 and Q50.

Each note carries a sound, well-sourced caveat and then asks a later reviewer
whether the explanation should be marked as a relative-best answer. In all three
the relative framing is already in place — the answer reason or the option
analysis says so in as many words — so the notes are closed on that finding and
the caveats are kept.

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
    42: ("aiap-intermediate-114-02-ai-tech-planning-042", ["D"],
         "7159b9da559fe431688d735af878d1da334e44921fb1c6ef2fa9f2ead1e46260"),
    44: ("aiap-intermediate-114-02-ai-tech-planning-044", ["C"],
         "aa63c60d612be93a0facf8dfcc6c72b2653b25b36358cb45086e1f4b3235c3b7"),
    50: ("aiap-intermediate-114-02-ai-tech-planning-050", ["C"],
         "413e3fd60602519e602d23fbb187433f829f56b9590f3e25aa0cbd10eef116c6"),
}

OLD_NOTE_42 = (
    "本站依官方答案 D 撰寫，僅將其視為四個選項中的相對最佳方案。研究顯示VAE 等深度生成模型的似然可能反而給分佈外資料較高分，"
    "不能單憑潛在空間或似然保證可靠 OOD 偵測；實務需以真實漂移案例校準並搭配特徵統計與效能監控。"
    "待人工複核是否需調整題目對『最適合』的表述。查核日期 2026-08-12。"
)
NEW_NOTE_42 = (
    "本站依官方答案 D 撰寫，僅將其視為四個選項中的相對最佳方案。研究顯示 VAE 等深度生成模型的似然可能反而給分佈外資料較高分，"
    "不能單憑潛在空間或似然保證可靠 OOD 偵測；實務需以真實漂移案例校準並搭配特徵統計與效能監控。"
    "原稿把「是否需調整對『最適合』的表述」列為待查，獨立 AI 複核確認相對框架已就位："
    "選項 D 的解析即以「正確（就選項比較而言）」開頭，摘要與作答理由也以「四個選項中」限定，讀者不會誤讀為絕對推薦。"
    "待查項目結案，限定與來源均維持不變。查核日期 2026-08-30。"
)

OLD_NOTE_44 = (
    "本站依官方答案 C 撰寫。VAE／GAN 可生成近似訓練分佈的樣本，但僅靠觀察性資料生成不同促銷條件，"
    "不能保證得到可信的顧客因果反應；『兼顧預測』也通常需分類頭或下游模型。"
    "待人工複核是否需進一步標示 A/B 測試與離線模擬的差別。查核日期 2026-08-12。"
)
NEW_NOTE_44 = (
    "本站依官方答案 C 撰寫。VAE／GAN 可生成近似訓練分佈的樣本，但僅靠觀察性資料生成不同促銷條件，"
    "不能保證得到可信的顧客因果反應；「兼顧預測」也通常需分類頭或下游模型。"
    "原稿把「是否需進一步標示 A/B 測試與離線模擬的差別」列為待查，獨立 AI 複核確認此區別已在正文中說明："
    "選項 D 的解析指出強化學習「必須先有可信的環境或使用者反應模型」，選項 C 也寫明條件式生成後仍「搭配分類器評估流失預測」，"
    "合起來已點出合成樣本屬離線模擬、不等於真實 A/B 測試的因果證據。此限定亦保留於本註記中，待查項目結案。"
    "查核日期 2026-08-30。"
)

OLD_NOTE_50 = (
    "本站依官方答案 C 撰寫，但題目將品牌顏色與手部失真統一歸因於 CLIP文字／影像編碼器未充分對齊，屬過度簡化。"
    "CLIP 原始用途是學習全局圖文表示；實際文字到影像擴散模型的細節失真還可能來自訓練資料、條件注入、生成器表示能力與取樣。"
    "且並非所有生成管線都直接以 CLIP 影像編碼器參與生成。待人工複核是否需標示為『四個選項中的相對最佳解』。查核日期 2026-08-12。"
)
NEW_NOTE_50 = (
    "本站依官方答案 C 撰寫，但題目將品牌顏色與手部失真統一歸因於 CLIP 文字／影像編碼器未充分對齊，屬過度簡化。"
    "CLIP 原始用途是學習全局圖文表示；實際文字到影像擴散模型的細節失真還可能來自訓練資料、條件注入、生成器表示能力與取樣，"
    "且並非所有生成管線都直接以 CLIP 影像編碼器參與生成。"
    "原稿把「是否需標示為四個選項中的相對最佳解」列為待查，獨立 AI 複核確認該標示已就位："
    "摘要寫「四個選項中」、作答理由寫「在四項中最接近合理機制」、選項 C 解析以「正確（依官方選項比較）」開頭，"
    "三處都已限定為相對比較。待查項目結案，過度簡化的提醒與 Rombach 等人的來源均維持不變。查核日期 2026-08-30。"
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

    for number, old, new in ((42, OLD_NOTE_42, NEW_NOTE_42), (44, OLD_NOTE_44, NEW_NOTE_44), (50, OLD_NOTE_50, NEW_NOTE_50)):
        explanation = selected[number]["explanation"]
        if explanation.get("editorialNote") != old:
            raise RuntimeError(f"Guard failed for Q{number} editorialNote snapshot")
        explanation["editorialNote"] = new

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
