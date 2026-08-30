"""Guarded draft explanation fixes from independent AI review, Q3 and Q4.

Q3 asked for Dify's own documentation on its Memory setting; it says exactly
what the draft assumed. Q4 asked whether the A-versus-C comparison was fairly
worded; it is. Both notes are closed.

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
    3: ("aiap-elementary-115-02-genai-planning-003", ["B"],
        "cb457a8d518041aa77e5a678da6243c9704441ed36cab491e7d8f79f21c33978"),
    4: ("aiap-elementary-115-02-genai-planning-004", ["C"],
        "b031d426232402a005f914de5be68cf1a0e3fb61846cd8fe296db79068b020fc"),
}

# Q3：原稿未查核 Dify 文件，把「平台內建記憶其實就是替你把歷史對話併入請求」
# 列為待查。Dify 官方文件對 Memory 的描述正是這件事，補為第四筆來源後結案。
OLD_NOTE_3 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：實務上 Dify 這類平台通常以內建的對話記憶（Memory）設定"
    "代為將歷史對話併入請求，選項 B 所述「手動打包」為其底層原理的直接實作；本批未查核 Dify 官方文件，"
    "複核者宜確認此補充說明與平台現行功能是否相符。查核日期 2026-08-07。"
)
NEW_NOTE_3 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿把「Dify 內建記憶是否即為代為併入歷史對話」列為待查，"
    "獨立 AI 複核已查核 Dify 官方文件：LLM 節點的 Memory 說明為「Enable Memory to maintain context across multiple LLM calls "
    "within a Chatflow conversation. When enabled, previous interactions will be included in subsequent prompts」——"
    "平台內建記憶的實作正是把先前互動併入後續提示，與選項 B 所述原理一致（另註明 Memory is node-specific，不跨對話保存）。"
    "待查項目結案。查核日期 2026-08-30。"
)
NEW_REFERENCE_3 = {
    "title": "Dify 官方文件－LLM 節點",
    "url": "https://docs.dify.ai/en/guides/workflow/node/llm",
    "locator": (
        "Memory and File Processing 段逐字核對：Enable Memory to maintain context across multiple LLM calls within a "
        "Chatflow conversation. When enabled, previous interactions will be included in subsequent prompts as formatted "
        "user-assistant outputs；並註明 Memory is node-specific and doesn't persist between different conversations"
    ),
    "checkedAt": "2026-08-30",
}

# Q4：原稿請複核者確認 A 與 C 的比較說法是否恰當。選項 A 的解析已明說「此敘述
# 本身正確」，只是資訊完整度低於 C，是誠實的程度比較，用語恰當，據以結案。
OLD_NOTE_4 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：選項 A 的敘述本身亦為正確定義，"
    "本題判 C 較佳係因題幹聚焦計費與應用意涵、C 同時涵蓋計費與上下文長度限制而資訊較完整，屬「最正確」的程度比較而非 A 有明確錯誤；"
    "複核者宜確認此比較說法的表述是否恰當。查核日期 2026-08-07。"
)
NEW_NOTE_4 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿請複核者確認 A 與 C 的比較說法是否恰當，"
    "獨立 AI 複核確認恰當：選項 A 的解析已明白寫出「此敘述本身正確」，只指出它未觸及題幹點名的計費與上下文長度上限，"
    "資訊完整度低於 C，並未謊稱 A 有錯。題幹以「Token 會影響模型的計費」起句、再問「最正確」，"
    "此一程度比較的表述方式忠實反映題目設定。惟本題確有兩個正確敘述並存，仍屬選項區辨偏鬆的題型，"
    "此點保留供人工複核者知悉。待查項目結案。查核日期 2026-08-30。"
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

    for number, old, new in ((3, OLD_NOTE_3, NEW_NOTE_3), (4, OLD_NOTE_4, NEW_NOTE_4)):
        explanation = selected[number]["explanation"]
        if explanation.get("editorialNote") != old:
            raise RuntimeError(f"Guard failed for Q{number} editorialNote snapshot")
        explanation["editorialNote"] = new

    selected[3]["explanation"]["references"].append(NEW_REFERENCE_3)

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
