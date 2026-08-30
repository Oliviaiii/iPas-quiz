"""Guarded draft explanation fixes from independent AI review, Q4, Q8, Q9 and Q10.

All four questions carried an ``editorialNote`` pending item that the drafting
session could not resolve because a source was unreachable at the time. This
review reached every one of them, so each note is replaced by what was actually
found and the supporting reference is added. No stem, option or official answer
changes, and every question stays ``draft``.

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
    4: ("aiap-elementary-115-02-ai-foundation-004", ["B"],
        "7b7fbd1e5fd0afdb5f893965149882987eb5b0b81ab89f8edce98436382564ed"),
    8: ("aiap-elementary-115-02-ai-foundation-008", ["A"],
        "a00d8f7b8e7395c110e0058ac64a88efcaa42ed828cf5e8492754e23e9942b31"),
    9: ("aiap-elementary-115-02-ai-foundation-009", ["D"],
        "453d58b313f407dbc380e1134191786193c374017694b36ebe2b338662f721b5"),
    10: ("aiap-elementary-115-02-ai-foundation-010", ["A"],
         "5f3a171ebdab341f127bcea9c9463cd3f0de4920b826a5b386294c261b2fe5df"),
}

# Q4：原稿因 investopedia.com 無法自動開啟而缺高頻交易的一手出處。改引美國
# SEC 對股票市場結構的概念性徵詢文件，其中逐項列出 HFT 的特徵，正是選項 B
# 所述能力的權威描述。
OLD_NOTE_4 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：高頻交易特性之一手外部來源（如主管機關或交易所文件）尚未取得，"
    "investopedia.com 本日無法以自動化方式開啟，B 選項所述能力係依題幹敘述與 AI 基礎概念整理，待複核補查外部參考。查核日期 2026-08-06。"
)
NEW_NOTE_4 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿列為待查的高頻交易一手出處，"
    "獨立 AI 複核已補上美國證券交易委員會（SEC）Concept Release on Equity Market Structure："
    "該文件逐項列出高頻交易特徵，含「使用極高速且精密的電腦程式產生、遞送與執行委託」與「建立及平倉部位的時間極短」，"
    "與選項 B 所述能力相符。查核日期 2026-08-30。"
)
NEW_REFERENCE_4 = {
    "title": "U.S. SEC — Concept Release on Equity Market Structure（Release No. 34-61358，75 FR 3594）",
    "url": "https://www.federalregister.gov/documents/full_text/text/2010/01/21/2010-1045.txt",
    "locator": (
        "III.A.2 High Frequency Trading：列舉 HFT 特徵 (1) The use of extraordinarily high-speed and sophisticated "
        "computer programs for generating, routing, and executing orders；(3) very short time-frames for establishing "
        "and liquidating positions；支持選項 B「極短時間內識別交易機會並驅動自動化交易決策」之敘述"
    ),
    "checkedAt": "2026-08-30",
}

# Q8：原稿無法讀取銀行公會規範全文，B、C、D 的條號待查。本次已自公會網站取得
# 規範 PDF（114 年 5 月 29 日理監事聯席會議通過、金管會 114 年 10 月 2 日洽悉），
# 逐條核對後結案。
OLD_NOTE_8 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：銀行公會規範全文 PDF（附件一，版本 1141012）未能以自動化方式讀取，"
    "B、C、D 所對應的確切條號待人工下載規範全文複核；本題揭露事項係依規範專頁、金管會 AI 指引新聞稿及本站前批（115-1 第一科第 13 題）已查核內容整理。"
    "查核日期 2026-08-06。"
)
NEW_NOTE_8 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿因無法讀取規範全文而把 B、C、D 的條號列為待查，"
    "獨立 AI 複核已取得規範 PDF 並逐條核對：第十一條要求「告知該互動或服務係利用上開技術自動完成，或揭露該互動或自動化金融服務適用的人群、場合、用途」，"
    "並「宜由消費者自行選擇是否使用，並提醒消費者該項服務有無替代方案」，分別對應選項 D、B、C；"
    "第十條則把模型與演算法紀錄定位為「保存必要技術文件……以確保其在必要時可被查驗」，屬留存備查而非對外公開，佐證選項 A 不在揭露義務之列。待查項目結案。"
    "查核日期 2026-08-30。"
)
OLD_LOCATOR_8 = "規範專頁與全文 PDF 下載連結（附件一：金融機構運用人工智慧技術作業規範 1141012，頁面日期 2025/11/18）"
NEW_LOCATOR_8 = (
    "規範全文（本會 114 年 5 月 29 日第 14 屆第 25 次理監事聯席會議核議通過、金管會 114 年 10 月 2 日金管銀國字第 1140219072 號函洽悉）："
    "第十一條為與消費者互動之告知與揭露義務（自動完成之告知、適用人群／場合／用途、選擇權與替代方案）；"
    "第十條為技術文件與紀錄之保存以備查驗，未要求對外公開模型架構或訓練資料"
)

# Q9：原稿因當日未能連線 ipas.org.tw，把「AI 倫理五大核心原則」的學習指引出處
# 列為待查。本次已下載科目一學習指引全文檢索，確認並無此節，改記為已查證的
# 否定結果，並保留以基本法第 4 條為對照基礎。
OLD_NOTE_9 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：題幹所稱「AI 倫理五大核心原則」的官方學習指引原文章節與頁碼尚未取得"
    "（本日未連線 ipas.org.tw），本題以通行歸納並對照《人工智慧基本法》第 4 條原則撰寫；待複核比對學習指引原文用語。查核日期 2026-08-06。"
)
NEW_NOTE_9 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿把「AI 倫理五大核心原則」的學習指引出處列為待查，"
    "獨立 AI 複核已下載科目一學習指引全文檢索：全文並無「五大核心原則」一節，亦未逐項定義透明性、公平性、隱私性、安全性與問責性，"
    "該組用語出自試題本身。因此本題維持以《人工智慧基本法》第 4 條所列原則為對照基礎，待查項目結案。查核日期 2026-08-30。"
)

# Q10：原稿把 veracity 與 value 說成僅屬業界用語、未宣稱出自 NIST。實際上
# NIST SP 1500-1r2 兩者都有正式定義，敘述可以更精確，locator 一併補齊頁碼。
OLD_NOTE_10 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：NIST SP 1500-1r2 所列大數據基本特性為 volume、velocity、variety 與 variability，"
    "veracity 與 value 屬業界常見 5V 用語，選項 B、C、D 中相關說明依通用定義撰寫，未宣稱出自 NIST；待複核確認是否需補充採用該等用語的正式出處。查核日期 2026-08-06。"
)
NEW_NOTE_10 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿把 veracity 與 value 記為僅屬業界常見用語、未宣稱出自 NIST，"
    "獨立 AI 複核核對 NIST SP 1500-1r2 全文後更正：該文件的詞彙表對兩者都有正式定義"
    "（Value refers to the inherent wealth, economic and social, embedded in any dataset；Veracity refers to the accuracy of the data），"
    "veracity 另有 5.4.1 專節。選項 B、C、D 的說明因此均有一手出處可徵，待查項目結案。查核日期 2026-08-30。"
)
OLD_LOCATOR_10 = (
    "第 3.2.3 節 Variety：需要分析來自多個儲存庫、領域或型態的資料；第 3.2.1、3.2.2 節分別界定 Volume 與 Velocity"
)
NEW_LOCATOR_10 = (
    "第 3.2.1 節 Volume、3.2.2 節 Velocity（Velocity is a measure of the rate of data flow）、3.2.3 節 Variety（PDF 第 21 頁）；"
    "第 5.4.1 節 Veracity（Veracity refers to the accuracy of the data，PDF 第 40 頁）；"
    "詞彙表 Value refers to the inherent wealth, economic and social, embedded in any dataset（PDF 第 17 頁）"
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

    e4 = selected[4]["explanation"]
    if e4.get("editorialNote") != OLD_NOTE_4:
        raise RuntimeError("Guard failed for Q4 editorialNote snapshot")
    e4["editorialNote"] = NEW_NOTE_4
    e4["references"].append(NEW_REFERENCE_4)

    e8 = selected[8]["explanation"]
    if e8.get("editorialNote") != OLD_NOTE_8:
        raise RuntimeError("Guard failed for Q8 editorialNote snapshot")
    if e8["references"][1]["locator"] != OLD_LOCATOR_8:
        raise RuntimeError("Guard failed for Q8 reference locator snapshot")
    e8["editorialNote"] = NEW_NOTE_8
    e8["references"][1]["locator"] = NEW_LOCATOR_8

    e9 = selected[9]["explanation"]
    if e9.get("editorialNote") != OLD_NOTE_9:
        raise RuntimeError("Guard failed for Q9 editorialNote snapshot")
    e9["editorialNote"] = NEW_NOTE_9

    e10 = selected[10]["explanation"]
    if e10.get("editorialNote") != OLD_NOTE_10:
        raise RuntimeError("Guard failed for Q10 editorialNote snapshot")
    if e10["references"][1]["locator"] != OLD_LOCATOR_10:
        raise RuntimeError("Guard failed for Q10 reference locator snapshot")
    e10["editorialNote"] = NEW_NOTE_10
    e10["references"][1]["locator"] = NEW_LOCATOR_10

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
