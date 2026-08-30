"""Guarded draft explanation fixes from independent AI review, Q15 and Q17.

Both questions carried an ``editorialNote`` pending item asking a later reviewer
to judge a caveat. This review checked each one and found the caveat correct and
worth stating, so it moves into the explanation body where a learner will see it
and the note is closed.

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
TARGETS = {
    15: ("aiap-elementary-115-02-ai-foundation-015", ["D"],
         "64ab16b07210f1390af122cbb2a1c7309dad4ff63b2bcc86079501417bdb8e25"),
    17: ("aiap-elementary-115-02-ai-foundation-017", ["D"],
         "40fd721c38129e401267bcf8a585c3bf80f933f495210f7ecef30c007380f489"),
}

# Q15：原稿把「不含正則化的最小平方閉式解其實對預測尺度不變」這件事放在
# editorialNote 請人工複核判斷。該敘述正確，且正是讀者最容易踩到的邊界，
# 因此寫進選項 A 解析本體，再結案。
OLD_OPTION_A_15 = (
    "線性迴歸（Linear Regression）以特徵的線性組合預測數值；使用梯度下降求解時，尺度懸殊會把損失面拉成狹長山谷、收斂變慢，"
    "若加入 L1/L2 正則化，懲罰項會不公平地壓制量級大的特徵係數，因此實務上通常建議先標準化。"
    "它對尺度的敏感度雖低於距離型模型，仍不是最不敏感的選擇。"
)
NEW_OPTION_A_15 = (
    "線性迴歸（Linear Regression）以特徵的線性組合預測數值；使用梯度下降求解時，尺度懸殊會把損失面拉成狹長山谷、收斂變慢，"
    "若加入 L1/L2 正則化，懲罰項會不公平地壓制量級大的特徵係數，因此實務上通常建議先標準化。"
    "嚴格說，若以普通最小平方的閉式解求解且不加正則化，標準化只會等比例改變係數、預測值完全相同；"
    "但實務上的線性迴歸多半帶正則化或以梯度求解，且係數大小也不再能跨特徵比較，"
    "所以它對尺度的敏感度雖低於距離型模型，仍不是最不敏感的選擇。"
)
OLD_NOTE_15 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：線性迴歸若以普通最小平方閉式解求解且不含正則化，"
    "標準化只改變係數尺度、不影響預測結果；本題將 A 判為相對敏感，是以實務常見的梯度求解與正則化情境為準的程度比較，"
    "複核者宜確認選項 A 的表述是否恰當。查核日期 2026-08-06。"
)
NEW_NOTE_15 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿把「普通最小平方閉式解不受標準化影響」列為待查，"
    "獨立 AI 複核確認該敘述成立，且屬於讀者應知道的邊界，已改寫入選項 A 解析本體；"
    "本題判 D 不受影響——決策樹對任何單調變換都不變，仍是四者中對尺度最不敏感者。待查項目結案。查核日期 2026-08-30。"
)

# Q17：原稿把「保留個體軌跡的假名化資料仍有時空交叉比對的殘餘風險」列為待查，
# 並問是否需要補權威來源。該風險有經同儕審查的量化研究，補進選項 D 解析與
# 來源清單後結案。
OLD_OPTION_D_17 = (
    "正確。一致的隨機編號讓同一乘客的紀錄仍可歸戶，支撐跨時間的通勤模式分析；不保留對應關係則切斷了編號與卡號、持卡人之間的回連路徑，"
    "符合施行細則所稱以代碼方式使資料無從辨識特定個人，兼顧了資料可用性與隱私保護。"
)
NEW_OPTION_D_17 = (
    "正確。一致的隨機編號讓同一乘客的紀錄仍可歸戶，支撐跨時間的通勤模式分析；不保留對應關係則切斷了編號與卡號、持卡人之間的回連路徑，"
    "符合施行細則所稱以代碼方式使資料無從辨識特定個人，兼顧了資料可用性與隱私保護。"
    "要留意的是，這只是四個選項中最合乎題意者，並非零風險：保留個體軌跡的假名化資料仍可能被時空點交叉比對而重新識別——"
    "de Montjoye 等人的研究顯示，在人口尺度的行動資料中，僅四個時空點就能唯一辨識 95% 的個人。"
    "因此實務上還須搭配粗化時間與地點、限制資料釋出對象與用途等配套。"
)
OLD_NOTE_17 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：學理上，保留個體軌跡的假名化資料仍可能透過時空軌跡交叉比對產生殘餘重新識別風險，"
    "本題依四個選項相對比較判 D 最符合去識別化要求；複核者宜評估是否需補充此限制的說明或權威來源。查核日期 2026-08-06。"
)
NEW_NOTE_17 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿把「保留個體軌跡的假名化資料仍有殘餘重新識別風險」列為待查，"
    "獨立 AI 複核已補入該限制的說明與經同儕審查的一手來源（de Montjoye et al., Scientific Reports 2013），寫入選項 D 解析；"
    "本題答案不受影響，D 仍是四個選項中唯一同時滿足跨時間追蹤與去識別化要求者。待查項目結案。查核日期 2026-08-30。"
)
NEW_REFERENCE_17 = {
    "title": "Unique in the Crowd: The privacy bounds of human mobility（Scientific Reports 3, 1376, 2013）",
    "url": "https://www.nature.com/articles/srep01376",
    "locator": "摘要：在一年 150 萬人的行動資料中，僅四個時空點即可唯一辨識 95% 的個人；支持選項 D 解析中「假名化仍有殘餘重新識別風險」之敘述",
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

    e15 = selected[15]["explanation"]
    if e15["optionAnalysis"]["A"] != OLD_OPTION_A_15 or e15.get("editorialNote") != OLD_NOTE_15:
        raise RuntimeError("Guard failed for Q15 optionAnalysis.A or editorialNote snapshot")
    e15["optionAnalysis"]["A"] = NEW_OPTION_A_15
    e15["editorialNote"] = NEW_NOTE_15

    e17 = selected[17]["explanation"]
    if e17["optionAnalysis"]["D"] != OLD_OPTION_D_17 or e17.get("editorialNote") != OLD_NOTE_17:
        raise RuntimeError("Guard failed for Q17 optionAnalysis.D or editorialNote snapshot")
    e17["optionAnalysis"]["D"] = NEW_OPTION_D_17
    e17["editorialNote"] = NEW_NOTE_17
    e17["references"].append(NEW_REFERENCE_17)

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
