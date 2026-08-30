"""Guarded draft explanation fixes from independent AI review, Q31, Q32, Q37 and Q40.

Q31's note recorded two vendor sites returning 403; they still do, so citable
substitutes are added instead. Q32 and Q37 asked whether their "most correct"
comparisons were fairly worded; both are. Q40 asked whether the exam's
"Solution Graph" has a designated source; a full-text search of the subject-two
study guide finds none, and the answer does not depend on one.

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
    31: ("aiap-elementary-115-02-genai-planning-031", ["A"],
         "60e21a071a0e1f147635d1d5b986b74c90aa40bc8d536c264d05ca4de84dd959"),
    32: ("aiap-elementary-115-02-genai-planning-032", ["C"],
         "31d510e8b40c040d0967764f80636063940ced7f5e037b081a4d48cb4e5e147f"),
    37: ("aiap-elementary-115-02-genai-planning-037", ["A"],
         "f2e9943971d90ce13f4418352617d892d14ef593078a81707917959f8a62722f"),
    40: ("aiap-elementary-115-02-genai-planning-040", ["D"],
         "5f8fa221ca3aaa431d82da58f0cc87de778022f6f5cc0633c9275c224d5cba95"),
}

OLD_NOTE_31 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：Midjourney 與 Perplexity 的官方網頁"
    "（docs.midjourney.com、perplexity.ai）於 2026-08-07 嘗試開啟均回應 HTTP 403，"
    "「Midjourney 為文字生成影像服務」與「Perplexity 為 AI 搜尋問答引擎」的產品定位描述尚缺可開啟的一手來源，"
    "僅 Stable Diffusion 已以 arXiv 原論文佐證，待複核補查。查核日期 2026-08-07。"
)
NEW_NOTE_31 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿記載兩家廠商官方文件站回應 403，產品定位缺可開啟的來源。"
    "獨立 AI 複核重試後 docs.midjourney.com 與 perplexity.ai/hub 仍為 403（該站阻擋自動化存取），"
    "已改補兩筆可開啟的百科來源佐證產品定位：Midjourney「generates images from natural language descriptions, called prompts」，"
    "Perplexity「offering a web search engine that processes user queries and synthesizes responses……citing sources used」，"
    "均與詳解敘述一致。待查項目結案。查核日期 2026-08-30。"
)
NEW_REFERENCES_31 = [
    {
        "title": "Wikipedia－Midjourney",
        "url": "https://en.wikipedia.org/wiki/Midjourney",
        "locator": (
            "首段逐字核對：Midjourney generates images from natural language descriptions, called prompts, similar to "
            "OpenAI's DALL-E and Stability AI's Stable Diffusion；佐證「Midjourney 為文字生成影像服務」"
            "（官方 docs.midjourney.com 阻擋自動化存取、回應 403）"
        ),
        "checkedAt": "2026-08-30",
    },
    {
        "title": "Wikipedia－Perplexity AI",
        "url": "https://en.wikipedia.org/wiki/Perplexity_AI",
        "locator": (
            "首段逐字核對：offering a web search engine that processes user queries and synthesizes responses；"
            "incorporate real-time web search capabilities, providing responses based on current Internet content, "
            "citing sources used；佐證「Perplexity 為 AI 搜尋問答引擎、非影像生成工具」"
            "（官方 perplexity.ai/hub 阻擋自動化存取、回應 403）"
        ),
        "checkedAt": "2026-08-30",
    },
]

OLD_NOTE_32 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：選項 B 與 D 的敘述並非全然錯誤——"
    "B 後半句的跨模組理解限制與 D 的雲端依賴均有事實基礎，本站判 C 最正確係因其同時準確涵蓋建議生成能力與人工審查兩面，"
    "屬程度比較而非絕對排除，建議複核者確認此區辨理由與官方命題意旨相符。查核日期 2026-08-07。"
)
NEW_NOTE_32 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿請複核者確認 C 相對 B、D 的區辨理由是否恰當，"
    "獨立 AI 複核確認恰當：選項 B、D 的解析都已明白承認其事實基礎（B 的跨模組理解限制、D 的雲端依賴），"
    "只指出 B 對能力面描述過度限縮、D 僅涵蓋部署形態單一面向，並未謊稱兩者為錯；題幹問「最正確」，"
    "以涵蓋完整度作為區辨忠實反映題目設定。惟本題確有三個敘述皆具事實基礎，仍屬選項區辨偏鬆的題型，"
    "此點保留供人工複核者知悉。待查項目結案。查核日期 2026-08-30。"
)

OLD_NOTE_37 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：選項 D 的語意解析確為將自然語言轉為結構化表示的相關技術，"
    "本站判 A 較佳係因題幹流程以「呼叫外部 API 完成下單」為終點，函數呼叫機制涵蓋從轉換到執行的完整環節，"
    "屬程度比較而非絕對排除，建議複核者確認與官方命題意旨相符。查核日期 2026-08-07。"
)
NEW_NOTE_37 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿請複核者確認 A 相對 D 的區辨是否恰當，"
    "獨立 AI 複核確認恰當：題幹把系統流程明確寫到「呼叫外部外送服務 API 完成下單，最後回傳訂單狀態與預計送達時間」，"
    "終點在執行與回收結果；語意解析止於產生形式化表示，涵蓋不到宣告工具、執行呼叫與回收結果的環節，"
    "函數呼叫機制則涵蓋完整迴圈。判準取自題幹敘述的終點，選項 D 的解析也已說明它是函數呼叫流程的前半段，未謊稱其為錯。"
    "待查項目結案。查核日期 2026-08-30。"
)

OLD_NOTE_40 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：Solution Graph（解決方案圖譜）並非業界有統一定義的標準術語，"
    "官方學習指引科目二亦未收錄，本題解析依題幹用語與圖狀推理框架（如 Tree of Thoughts）的一般用法推得，"
    "「有向無環圖」的界定亦以題幹敘述為準，建議複核者查證命題是否另有指定出處。查核日期 2026-08-07。"
)
NEW_NOTE_40 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿指出 Solution Graph 並非有統一定義的標準術語、"
    "請複核者查證命題是否另有指定出處。獨立 AI 複核已全文檢索科目二學習指引：「解決方案圖」「Solution Graph」「有向無環」皆為零筆，"
    "確認官方教材未收錄，命題依據未經公布、無從再查證。惟本題答案不依賴該出處："
    "四個選項中只有 D 描述任務規劃的表示結構，A（模型權重）、B（知識圖譜並誇大為自動解題）、C（強化學習模型）在類別上即不成立，"
    "由選項文字本身即可判定。待查項目以此結案。查核日期 2026-08-30。"
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

    for number, old, new in (
        (31, OLD_NOTE_31, NEW_NOTE_31),
        (32, OLD_NOTE_32, NEW_NOTE_32),
        (37, OLD_NOTE_37, NEW_NOTE_37),
        (40, OLD_NOTE_40, NEW_NOTE_40),
    ):
        explanation = selected[number]["explanation"]
        if explanation.get("editorialNote") != old:
            raise RuntimeError(f"Guard failed for Q{number} editorialNote snapshot")
        explanation["editorialNote"] = new

    selected[31]["explanation"]["references"].extend(NEW_REFERENCES_31)

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
