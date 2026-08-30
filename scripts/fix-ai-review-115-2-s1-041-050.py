"""Guarded draft explanation fixes from independent AI review, Q46, Q47 and Q48.

Each note asked a later reviewer to check a source. All three were checked here:
the AutoSkill paper's abstract matches the option almost word for word, the
subject-one study guide does discuss mode collapse, and it has no drift section
at all — so citing subject two for Q48 was right.

This script is intentionally not run by the reviewer. It updates only exact
reviewed snapshots and preserves explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-elementary-2-ai-foundation"
GUIDE_S1 = (
    "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/"
    "AI應用規劃師(初級)-學習指引-科目1_人工智慧基礎概論1141203_20251222172144.pdf"
)
TARGETS = {
    46: ("aiap-elementary-115-02-ai-foundation-046", ["C"],
         "655b7489ec3c353d44f6ee957f4fff2cefc893a110d211c6e484292fc2608ba2"),
    47: ("aiap-elementary-115-02-ai-foundation-047", ["B"],
         "f6f90a069a285826872a20f6a961490c581f5d3a413ba31add803007af2d422f"),
    48: ("aiap-elementary-115-02-ai-foundation-048", ["B"],
         "4d3175b52bc3a1b032320b1b6dd3851c9a1a3c60a920fc71823055dfb14061f6"),
}

# Q46：原稿請複核者確認命題是否另有所指。官方未公布命題依據，這一點問不出更多
# 結果；但論文摘要末句與選項 C 幾乎逐字對應，已足以定案，改記為已核對的結論。
OLD_NOTE_46 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：本題所稱 AutoSkill 依 arXiv:2603.01145"
    "（AutoSkill: Experience-Driven Lifelong Learning via Skill Self-Evolution）摘要撰寫，與官方答案 C 的描述一致；"
    "命題實際依據的文獻未經官方公布，複核時請確認是否另有所指。查核日期 2026-08-06。"
)
NEW_NOTE_46 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿請複核者確認命題是否另有所指。"
    "獨立 AI 複核重新開啟 arXiv:2603.01145 逐字核對：摘要末句「AutoSkill turns ephemeral interaction experience into "
    "explicit, reusable, and composable capabilities」與官方答案 C「將重複的互動經驗轉化為可重複使用的明確技能模組」幾乎逐字對應，"
    "摘要並明載 without retraining the underlying model 與 model-agnostic plugin layer，可逐一對上選項 B、A 的排除理由。"
    "命題依據未經官方公布，無從再查證，惟此對應已足以支持本題詳解。待查項目結案。查核日期 2026-08-30。"
)

# Q47：原稿問官方教材是否另有 LLM 語境的模式崩潰段落。科目一學習指引確有三處，
# 其中一處直接把模式崩潰與「生成數據的多樣性」連在一起，正是本題症狀。
OLD_NOTE_47 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：Mode Collapse 的系統性討論出自 GAN 文獻，"
    "本題將其延伸用於大型語言模型輸出多樣性的描述；已引用 Unrolled GAN 論文作為術語出處，官方教材是否另有 LLM 語境的對應段落，"
    "待複核確認。查核日期 2026-08-06。"
)
NEW_NOTE_47 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿問官方教材是否另有對應段落，"
    "獨立 AI 複核已全文檢索科目一學習指引，找到三處：GAN 缺點「訓練過程不穩定，可能出現模式崩潰（Mode Collapse）」、"
    "「生成式 AI 的訓練過程往往伴隨著模式崩潰、梯度消失等挑戰」，以及「生成式 AI 的訓練過程經常面臨模式崩潰和梯度消失等問題，"
    "這會影響生成數據的多樣性與品質」——最後一處直接把模式崩潰連到輸出多樣性，正是本題描述的症狀。已補為第四筆來源，待查項目結案。"
    "查核日期 2026-08-30。"
)
NEW_REFERENCE_47 = {
    "title": "iPAS AI 應用規劃師（初級）學習指引－科目一 人工智慧基礎概論",
    "url": GUIDE_S1,
    "locator": (
        "第三章（PDF 第 23 頁）：GAN 缺點「訓練過程不穩定，可能出現模式崩潰（Mode Collapse）」；"
        "（PDF 第 65 頁）「生成式 AI 的訓練過程經常面臨模式崩潰和梯度消失等問題，這會影響生成數據的多樣性與品質」，"
        "支持本題把輸出多樣性喪失歸為模式崩潰"
    ),
    "checkedAt": "2026-08-30",
}

# Q48：原稿問科目一學習指引是否另有漂移章節。全文檢索「漂移」零筆，因此引科目二
# 3-44 是目前唯一的官方出處，記為已查證的否定結果。
OLD_NOTE_48 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：資料漂移定義所引學習指引段落出自科目二"
    "（生成式 AI 應用與規劃）3-44，科目一學習指引是否另有漂移對應章節，複核時可再確認補引；概念漂移定義另引 arXiv 綜述佐證。"
    "查核日期 2026-08-06。"
)
NEW_NOTE_48 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿問科目一學習指引是否另有漂移對應章節，"
    "獨立 AI 複核已全文檢索科目一學習指引：「漂移」零筆，該科教材未涵蓋此主題。因此引科目二 3-44 的數據漂移段落是目前唯一的官方出處，"
    "概念漂移則以 arXiv 綜述佐證，引用方式維持不變。待查項目以此否定結果結案。查核日期 2026-08-30。"
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

    for number, old, new in ((46, OLD_NOTE_46, NEW_NOTE_46), (47, OLD_NOTE_47, NEW_NOTE_47), (48, OLD_NOTE_48, NEW_NOTE_48)):
        explanation = selected[number]["explanation"]
        if explanation.get("editorialNote") != old:
            raise RuntimeError(f"Guard failed for Q{number} editorialNote snapshot")
        explanation["editorialNote"] = new

    selected[47]["explanation"]["references"].append(NEW_REFERENCE_47)

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
