"""Close the four residual open 待查 items in 115-1 初級第一科 (Q13, Q44, Q46, Q47).

Follow-up cleanup pass after all 600 questions completed independent AI review.
Guards on the exact reviewed snapshot and preserves explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-elementary-1-ai-foundation"
TARGETS = {
    13: ("aiap-elementary-115-01-ai-foundation-013", ["A"], "2d26b9f63c5f19de96118d2f169f7cac9fa871d7854d9862fa941272f9538dae", 3),
    44: ("aiap-elementary-115-01-ai-foundation-044", ["A"], "c501e643463cd45d4aba853d58aa26e9579f08a8a04d02a585f0a74c0123d3d9", 3),
    46: ("aiap-elementary-115-01-ai-foundation-046", ["C"], "2d6d55f1b27945fec77a61defb99677cad20060ab0886d40432f2863b0a1d3d7", 2),
    47: ("aiap-elementary-115-01-ai-foundation-047", ["D"], "11a966f353aacdce250fcf2462139db908dde7ccd113f7c5deeee2bb7846fc79", 3),
}

NEW_LOCATOR_13 = (
    "規範全文（本會 114 年 5 月 29 日核議通過、金管會 114 年 10 月 2 日金管銀國字第 1140219072 號函洽悉）："
    "第十一條「金融機構運用人工智慧技術與消費者互動時，應告知該互動或服務係利用上開技術自動完成，"
    "或揭露該互動或自動化金融服務適用的人群、場合、用途。另宜由消費者自行選擇是否使用，"
    "並提醒消費者該項服務有無替代方案」，分別對應選項 C、B、D；"
    "第十條把模型與演算法紀錄定位為「保存必要技術文件及相關紀錄……以確保其在必要時可被查驗」，"
    "屬留存備查而非對外公開，佐證選項 A 不在揭露義務之列"
)

NEW_NOTE_13 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
    "原稿因未能讀取規範全文而把條號列為待查，獨立 AI 複核已下載規範 PDF 並逐條核對："
    "第十一條一條之內即涵蓋選項 C（告知該互動或服務係利用上開技術自動完成）、"
    "選項 B（揭露適用的人群、場合、用途）與選項 D（提醒消費者該項服務有無替代方案）；"
    "第十條要求保存技術文件與模型、演算法紀錄「以確保其在必要時可被查驗」，是留存備查，"
    "並未要求對外公開模型架構或原始程式碼，佐證選項 A 為非必要揭露事項。待查項目結案。查核日期 2026-08-30。"
)

NEW_NOTE_44 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
    "原稿把「A 相對 B 的程度比較表述是否夠明確」列為待查，獨立 AI 複核確認表述已就位："
    "選項 B 的解析開頭即寫「確實能把極端值收進最高一箱而削弱其影響」，"
    "承認區間化同樣有效，只以「會把連續特徵離散化、同一箱內差異全部消失、箱數與切點需另行決定」說明代價較大，"
    "並未謊稱 B 為錯；題幹問「最適合」，以代價高低作為區辨忠實反映題目設定。"
    "另已全文檢索官方學習指引科目一：「偏態」僅出現在資料清洗段（3-39「中位數或眾數填補：針對偏態分佈或類別型特徵」）"
    "與第三章練習題，全書未討論對數轉換或冪次轉換，故改引 scikit-learn 前處理文件的作法維持不變，"
    "該頁 8.3.2 節逐字寫明冪次轉換為 parametric, monotonic transformations，"
    "目的是 map data ... to as close to a Gaussian distribution as possible in order to stabilize variance and minimize skewness。"
    "待查項目結案。查核日期 2026-08-30。"
)

NEW_LOCATOR_46 = (
    "第 3.2.3 節 Variety：Variety refers to data from multiple repositories, domains, or types；"
    "第 3.2.1、3.2.2 節分別界定 Volume 與 Velocity（Velocity refers to the rate of data flow）；"
    "詞彙表（PDF 第 17 頁）與第 5.4.1 節 VERACITY（PDF 第 40 頁）另正式定義 Veracity refers to the accuracy of the data"
)

NEW_NOTE_46 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
    "原稿把 veracity 記為業界常見的 5V／6V 用語、未宣稱出自 NIST，獨立 AI 複核核對 NIST SP 1500-1r2 全文後更正："
    "該文件的詞彙表逐字定義 Veracity refers to the accuracy of the data，第 5.4.1 節另有 VERACITY 專節"
    "（並與 5.4.2 VALIDITY 對比），因此選項 D 的說明同樣有一手出處可徵，只是 veracity 被歸在"
    "「data characteristics important to data science」而非第 3.2 節的基本特性。"
    "官方學習指引科目一則確認查無大數據 V 特性的專節（全文檢索 Variety、Velocity 均為零筆）。"
    "待查項目結案。查核日期 2026-08-30。"
)

NEW_NOTE_47 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
    "原稿把「結構化預測」缺一手定義列為待查，獨立 AI 複核已補入 Goodfellow 等人《Deep Learning》第 5.1.1 節的"
    "Structured output 定義，該處逐字寫明輸出是「a vector (or other data structure containing multiple values) "
    "with important relationships between the different elements」，並以句法剖析（為樹節點標註動詞、名詞、副詞）"
    "與影像逐像素分割為例，正對應本題選項 D 的逐詞標註。"
    "官方學習指引科目一則確認未收錄「結構化預測」一詞（全文檢索僅見結構化數據 Structured Data 的資料型態分類），"
    "此方向查無官方定義。待查項目結案。查核日期 2026-08-30。"
)

NEW_REF_47 = {
    "title": "Goodfellow, Bengio & Courville－Deep Learning, Chapter 5: Machine Learning Basics",
    "url": "https://www.deeplearningbook.org/contents/ml.html",
    "locator": (
        "5.1.1 The Task, T 的 Structured output 條目：Structured output tasks involve any task where the output is "
        "a vector (or other data structure containing multiple values) with important relationships between the "
        "different elements；例子包含 parsing—mapping a natural language sentence into a tree ... by tagging nodes "
        "of the trees as being verbs, nouns, adverbs 與影像逐像素分割"
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
    for number, (question_id, answer, digest, ref_count) in TARGETS.items():
        question = selected[number]
        if question.get("id") != question_id or question.get("officialAnswer") != answer:
            raise RuntimeError(f"Guard failed for Q{number} identity or answer")
        if question.get("explanationStatus") != "draft" or snapshot_hash(question) != digest:
            raise RuntimeError(f"Guard failed for Q{number} status or reviewed snapshot")
        if len(question["explanation"]["references"]) != ref_count:
            raise RuntimeError(f"Guard failed for Q{number} reference count")
        if "待查項目：" not in question["explanation"].get("editorialNote", ""):
            raise RuntimeError(f"Guard failed for Q{number}: editorialNote is not an open 待查 item")

    e13 = selected[13]["explanation"]
    if "ba.org.tw" not in e13["references"][1]["url"]:
        raise RuntimeError("Guard failed for Q13 reference 1 target")
    e13["references"][1]["locator"] = NEW_LOCATOR_13
    e13["references"][1]["checkedAt"] = "2026-08-30"
    e13["editorialNote"] = NEW_NOTE_13

    selected[44]["explanation"]["editorialNote"] = NEW_NOTE_44

    e46 = selected[46]["explanation"]
    if "NIST.SP.1500-1r2" not in e46["references"][1]["url"]:
        raise RuntimeError("Guard failed for Q46 reference 1 target")
    e46["references"][1]["locator"] = NEW_LOCATOR_46
    e46["references"][1]["checkedAt"] = "2026-08-30"
    e46["editorialNote"] = NEW_NOTE_46

    e47 = selected[47]["explanation"]
    e47["references"].append(NEW_REF_47)
    e47["editorialNote"] = NEW_NOTE_47

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
