"""Guarded draft explanation fixes from independent AI review, Q22 and Q23.

Q22's note flagged that the cited thinking-budget parameter changes fast; it has
in fact changed — ``budget_tokens`` is deprecated or rejected on current models,
and the ceiling is now set through effort levels and task budgets. The concept
text is updated to the current mechanism; the answer is unaffected. Q23's note
asked a reviewer to check the Titans paper body for the three memory variants;
the figure captions confirm the draft's mapping.

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
    22: ("aiap-elementary-115-02-genai-planning-022", ["C"],
         "0a80af1cddb8c1dd950d6b72fec175613b336cc89973e0957e5b4e3a678dd635"),
    23: ("aiap-elementary-115-02-genai-planning-023", ["C"],
         "85d1a2520d6ba8bbb6ce383d66805abc4b174609a0b6d67872833900dcfbe84e"),
}

OLD_CONCEPT_22 = (
    "推理型語言模型在給出最終答案前，會先產生內部推理（思考）內容；思考消耗的 Token 同樣計費並增加延遲，"
    "因此「想多深」本身就是品質與成本的取捨。以 Anthropic 的延伸推理（Extended Thinking）設計為例，"
    "開發者以 budget_tokens 之類的參數為內部推理設定 Token 預算：預算越大，模型能對複雜問題做越完整的多層分析、回應品質越好，"
    "但延遲與費用隨之上升；官方文件建議依任務難度調整——簡單任務從低預算起步、複雜任務給更大預算，並在品質與延遲之間權衡。\n"
    "把這個預算依輸入案件的複雜度動態調整——簡單案件低預算快速回覆、複雜案件高預算深入推理——"
    "正是題幹「依案件複雜度自動調整模型推理深度」所需要的系統設計概念。"
)
NEW_CONCEPT_22 = (
    "推理型語言模型在給出最終答案前，會先產生內部推理（思考）內容；思考消耗的 Token 同樣計費並增加延遲，"
    "因此「想多深」本身就是品質與成本的取捨。實務上控制這個深度的介面隨模型版本演進：早期以固定的思考 Token 預算參數"
    "（如 Anthropic 延伸推理的 budget_tokens）直接設定上限；較新的模型改為由模型自行決定思考時機的調適式思考（adaptive thinking），"
    "再以「投入程度」等級（effort，low 至 max）與代理任務的 Token 預算（task budget）設定資源上限。\n"
    "介面雖然換過，設計概念不變：為單次推理設定可用的思考資源上限，並依輸入的難易動態調整——簡單案件給低上限快速回覆、"
    "複雜案件給高上限深入推理。這正是題幹「依案件複雜度自動調整模型推理深度」所需要的系統設計概念。"
)

OLD_OPTION_C_22 = (
    "正確。推理型模型的思考深度可用思考資源上限（如思考 Token 預算）控制：預算高時，模型能展開多層次的法規詮釋與過往案例比對；"
    "預算低時，快速比對條款即產出結論。依案件複雜度動態設定此上限，讓每件案件用到恰當的推理量，正是在推理品質與成本效率間取得平衡的機制，"
    "命中題幹需求。"
)
NEW_OPTION_C_22 = (
    "正確。推理型模型的思考深度可用思考資源上限控制（依模型版本而定，可能是思考 Token 預算、投入程度等級或代理任務預算）："
    "上限高時，模型能展開多層次的法規詮釋與過往案例比對；上限低時，快速比對條款即產出結論。"
    "依案件複雜度動態設定此上限，讓每件案件用到恰當的推理量，正是在推理品質與成本效率間取得平衡的機制，命中題幹需求。"
)

OLD_LOCATOR_22 = (
    "budget_tokens 參數為模型內部推理設定 Token 預算目標：較大的預算可讓複雜問題獲得更完整的分析以提升回應品質，"
    "但延遲隨之增加；文件建議依任務複雜度調整預算，在品質與延遲間權衡"
)
NEW_LOCATOR_22 = (
    "Extended thinking：模型在最終回應前先產生內部推理內容，思考 Token 一併計費並增加延遲，故需在推理深度與成本間權衡。"
    "早期版本以 budget_tokens 設定思考 Token 預算；現行模型改採 adaptive thinking，"
    "並以 output_config.effort（low／medium／high／xhigh／max）與 task_budget 設定可用的思考資源上限"
)

OLD_NOTE_22 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：所引 Anthropic 文件說明以 budget_tokens 為內部推理設定 Token 預算、"
    "預算越大分析越完整但延遲越高；該頁同時標示較新版模型已改採 adaptive thinking 由模型自行決定思考深度，"
    "參數名稱與行為隨版本演進快，複核時宜確認最新文件並補充其他廠商推理模型的對應機制。查核日期 2026-08-07。"
)
NEW_NOTE_22 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿把「參數名稱與行為隨版本演進快」列為待查，獨立 AI 複核確認確實已變："
    "budget_tokens 在現行模型上已被取代（部分版本棄用、部分版本直接回傳錯誤），改由 adaptive thinking 搭配 effort 等級"
    "（low／medium／high／xhigh／max）與代理任務的 task budget 控制思考資源上限。"
    "已改寫概念段與選項 C，改以「思考資源上限」這個不隨版本改變的設計概念立論，並在括號中列出目前的具體介面；"
    "官方答案 C 不受影響。待查項目結案；後續若廠商介面再變，只需更新括號內的舉例。查核日期 2026-08-30。"
)

# Q23：原稿說明摘要未列出三種變體名稱，請複核者查論文正文。正文圖說已逐字確認，
# 三種變體與三個干擾選項一一對應，據以結案並把 locator 換成正文出處。
OLD_LOCATOR_23 = (
    "摘要：注意力因上下文窗口有限而如短期記憶，神經長期記憶模組學習記住歷史脈絡，"
    "協助注意力在處理當前上下文時利用久遠過去的資訊；並提出三種把記憶整合進架構的變體"
)
NEW_LOCATOR_23 = (
    "摘要：注意力因上下文窗口有限而如短期記憶，神經長期記憶模組學習記住歷史脈絡，協助注意力利用久遠過去的資訊。"
    "正文圖說逐字核對三種變體：Figure 2「Memory as a Context (MAC) Architecture……The core branch concatenates the "
    "corresponding long-term and persistent memories with the input sequence」（對應選項 C）；"
    "Figure 4「Memory as a Gate (MAG)……combine memory with the core branch using a gating mechanism」（對應選項 B）；"
    "Figure 5「Memory as a Layer (MAL)……the memory layer is responsible to compress the past and current context before "
    "the attention module」（對應選項 A）"
)
OLD_NOTE_23 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：arXiv 摘要僅說明神經長期記憶模組的角色與「三種整合記憶的變體」，"
    "未直接列出 Memory as Context 的名稱與細部流程；本詳解對 MAC 及另外兩種整合方式的區辨，依論文正文的一般描述與題幹選項推得，"
    "建議複核者查閱論文正文逐一核對三種變體的定義。查核日期 2026-08-07。"
)
NEW_NOTE_23 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿請複核者查論文正文逐一核對三種變體，獨立 AI 複核已下載全文核對圖說："
    "MAC 的核心分支把長期記憶與持久記憶「concatenate」到輸入序列上（對應選項 C）、MAG 以 gating 機制與核心分支結合（對應選項 B）、"
    "MAL 則把記憶層置於注意力模組之前壓縮上下文（對應選項 A），三者與三個選項一一對應，原詳解的區辨成立。"
    "另註：論文原文寫作 Memory as a Context，題幹作 Memory as Context，僅冠詞差異，指涉同一變體。待查項目結案。查核日期 2026-08-30。"
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

    e22 = selected[22]["explanation"]
    if (
        e22["concept"] != OLD_CONCEPT_22
        or e22["optionAnalysis"]["C"] != OLD_OPTION_C_22
        or e22["references"][1]["locator"] != OLD_LOCATOR_22
        or e22.get("editorialNote") != OLD_NOTE_22
    ):
        raise RuntimeError("Guard failed for Q22 snapshot fields")
    e22["concept"] = NEW_CONCEPT_22
    e22["optionAnalysis"]["C"] = NEW_OPTION_C_22
    e22["references"][1]["locator"] = NEW_LOCATOR_22
    e22["references"][1]["checkedAt"] = "2026-08-30"
    e22["editorialNote"] = NEW_NOTE_22

    e23 = selected[23]["explanation"]
    if e23["references"][1]["locator"] != OLD_LOCATOR_23 or e23.get("editorialNote") != OLD_NOTE_23:
        raise RuntimeError("Guard failed for Q23 snapshot fields")
    e23["references"][1]["locator"] = NEW_LOCATOR_23
    e23["references"][1]["checkedAt"] = "2026-08-30"
    e23["editorialNote"] = NEW_NOTE_23

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
