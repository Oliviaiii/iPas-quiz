"""Draft guarded explanation fixes from independent AI review, Q31-Q33.

This script is intentionally not run by the reviewer. It corrects an
over-broad regulatory claim in Q31, distinguishes statistical bias from
robustness in Q32, and removes an unsupported guarantee from Q33. Every edit
is guarded by the exact reviewed draft text and keeps explanationStatus draft.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-114-elementary-4-ai-foundation"
CHECKED_AT = "2026-08-13"

EXPECTED = {
    31: {
        "id": "aiap-elementary-114-04-ai-foundation-031",
        "answer": ["D"],
        "concept": (
            "反事實解釋回答的是「要改變什麼，結果才會不同」，例如告訴被拒貸的客戶："
            "若年收入再高若干、或負債比再低若干，申請就會通過。它的價值在於給出可行動"
            "的建議，而不只是列出哪些特徵重要。\n困難之處在於，演算法最容易找到的往往是"
            "數學上距離最近、卻在現實中站不住腳的組合：可能建議客戶改變無法改變的屬性"
            "（年齡），或給出彼此矛盾的數值（年資變短但年收入大增）。此外，信貸屬於高度"
            "監管領域，建議內容不得涉及受保護特徵，否則會觸及公平放貸的法律風險。"
        ),
        "option_d": (
            "正確。反事實樣本必須尊重特徵之間的因果與邏輯關係、符合業務規則，建議的改變"
            "要是客戶真的能做到的，且不得使用受保護特徵而違反公平放貸要求，這些同時構成"
            "技術與監管上的核心挑戰。"
        ),
        "reference_count": 2,
    },
    32: {
        "id": "aiap-elementary-114-04-ai-foundation-032",
        "answer": ["B"],
        "summary": (
            "正確答案是 B。面對偏態且樣本有限，增加樣本數並改用中位數或分位數這類穩健"
            "統計量最有效。"
        ),
        "concept": (
            "當母體分布明顯偏態時，樣本平均數會被長尾端的極端值往一側拉，變異數也會被"
            "放大，因而不能穩健代表資料的中心位置。中位數與分位數只看排序後的位置，不受"
            "極端值大小影響，官方學習指引也指出中位數「不受極端值影響，能更好地反映數據"
            "的中心趨勢」。\n另一方面，樣本數不足會讓估計本身的變動性偏高。增加樣本數能"
            "同時降低抽樣誤差，也讓分布形態被觀察得更清楚。兩者搭配，才能同時處理「偏態」"
            "與「樣本有限」這兩個問題。"
        ),
        "answer_reason": (
            "題目同時給了兩個條件：分布偏態、樣本數有限。B 的兩個動作正好各自對應：增加"
            "樣本數處理樣本不足，改用分位數或中位數處理偏態，因此選 B。"
        ),
        "option_a": (
            "在偏態分布下直接使用樣本平均數與變異數，正是問題所在：平均數會被長尾拉偏，"
            "變異數被極端值放大，估計出的母體參數因此帶有系統性偏誤。不做任何調整等於忽略"
            "題目給的前提。"
        ),
        "option_b": (
            "正確。中位數與分位數以排序位置為依據，不受極端值數值大小左右，能較穩健地描述"
            "偏態資料的中心；同時擴大樣本數可降低抽樣誤差，兩者相輔相成。"
        ),
        "trap": (
            "第一，偏態資料看中位數、對稱資料看平均數，這是選擇中心趨勢統計量的基本原則。"
            "第二，重新排列資料不等於重抽樣；只有有放回的重抽樣才能得到估計量的分布資訊。"
        ),
        "editorial_note": (
            "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
        ),
        "reference_count": 2,
    },
    33: {
        "id": "aiap-elementary-114-04-ai-foundation-033",
        "answer": ["D"],
        "concept": (
            "當異常事件極為罕見時，可用的異常樣本太少，難以支撐一個穩定的監督式分類器"
            "——模型很容易把少數幾筆異常的細節當成通則。\n以重建誤差為基礎的作法換了個"
            "思路：只用正常資料訓練自編碼器，讓它學會如何壓縮再重建「正常的樣子」。推論時，"
            "正常資料能被順利重建，誤差小；從未見過的異常樣態則重建不好，誤差明顯偏高，"
            "據此設門檻即可偵測。這種作法不需要異常標籤，也不會因異常型態改變而失效，"
            "穩定性較佳。"
        ),
        "option_d": (
            "正確。只用正常資料訓練序列到序列自編碼器，模型學到的是正常運轉的模式；異常"
            "出現時重建誤差顯著上升，即可偵測。此法不需異常標籤，對未見過的新異常型態也有"
            "反應能力。"
        ),
        "reference_count": 3,
    },
}


def add_reference(explanation: dict, reference: dict, expected_count: int) -> None:
    references = explanation.get("references")
    if not isinstance(references, list) or len(references) != expected_count:
        raise RuntimeError("Reference list changed from the reviewed snapshot")
    if any(item.get("url") == reference["url"] for item in references):
        raise RuntimeError(f"Reference already exists: {reference['url']}")
    references.append(reference)


def require(value: object, expected: object, label: str) -> None:
    if value != expected:
        raise RuntimeError(f"Guard failed for {label}")


def main() -> None:
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    targets = {
        question["officialQuestionNumber"]: question
        for question in questions
        if question.get("sourceId") == SOURCE_ID
        and question.get("officialQuestionNumber") in EXPECTED
    }
    if set(targets) != set(EXPECTED):
        raise RuntimeError(f"Target question set changed: {sorted(targets)}")

    for number, guard in EXPECTED.items():
        question = targets[number]
        require(question.get("id"), guard["id"], f"Q{number} id")
        require(question.get("officialAnswer"), guard["answer"], f"Q{number} answer")
        require(question.get("explanationStatus"), "draft", f"Q{number} status")
        explanation = question.get("explanation")
        if not isinstance(explanation, dict):
            raise RuntimeError(f"Q{number}: explanation is missing")
        options = explanation.get("optionAnalysis")
        if not isinstance(options, dict):
            raise RuntimeError(f"Q{number}: option analysis is missing")

        if number == 31:
            require(explanation.get("concept"), guard["concept"], "Q31 concept")
            require(options.get("D"), guard["option_d"], "Q31 option D")
            explanation["concept"] = (
                "反事實解釋回答的是「要改變什麼，結果才會不同」，例如告訴被拒貸的客戶："
                "若年收入再高若干、或負債比再低若干，申請就會通過。它的價值在於給出可行動"
                "的建議，而不只是列出哪些特徵重要。\n困難之處在於，演算法最容易找到的往往是"
                "數學上距離最近、卻在現實中站不住腳的組合：可能建議客戶改變無法改變的屬性"
                "（如出生年月），或給出彼此矛盾的數值。信貸建議也必須依適用法域審查公平性"
                "與反歧視要求。在臺灣，金管會指引要求決策不應對特定群體造成不合理歧視，且"
                "使用個人屬性作為決策因素應有合理理由；這不等同概括禁止受保護或個人屬性出現"
                "於任何模型治理、檢測或決策流程。"
            )
            options["D"] = (
                "正確。反事實樣本必須尊重特徵間的因果與業務邏輯，建議也要可操作；信貸場景"
                "還須依適用法域檢查是否造成不合理差別待遇。具體禁止或容許哪些屬性及用途取決"
                "於法域與使用情境，不宜概括寫成所有受保護屬性一律不得出現。"
            )
            add_reference(
                explanation,
                {
                    "title": "金管會－金融業運用人工智慧（AI）指引",
                    "url": "https://law.fsc.gov.tw/LawContent.aspx?id=GL003920",
                    "locator": (
                        "第二章核心原則二：決策不應對特定群體造成不合理歧視；使用個人屬性"
                        "作為決策因素應有合理理由"
                    ),
                    "checkedAt": CHECKED_AT,
                },
                guard["reference_count"],
            )
        elif number == 32:
            require(explanation.get("summary"), guard["summary"], "Q32 summary")
            require(explanation.get("concept"), guard["concept"], "Q32 concept")
            require(
                explanation.get("answerReason"),
                guard["answer_reason"],
                "Q32 answer reason",
            )
            require(options.get("A"), guard["option_a"], "Q32 option A")
            require(options.get("B"), guard["option_b"], "Q32 option B")
            require(explanation.get("trap"), guard["trap"], "Q32 trap")
            require(
                explanation.get("editorialNote"),
                guard["editorial_note"],
                "Q32 editorial note",
            )
            explanation["summary"] = (
                "正確答案是 B。若題意是估計偏態分布的典型中心位置，增加樣本數並採中位數或"
                "分位數較穩健；但題目未指明要估計哪個母體參數，不能把這點解讀成樣本平均數"
                "對母體平均數必然有偏。"
            )
            explanation["concept"] = (
                "統計上的偏誤是估計量在重複抽樣下的期望值與目標參數之差。只要樣本為隨機"
                "樣本且母體平均數存在，樣本平均數對母體平均數仍是不偏估計量；母體偏態會讓"
                "有限樣本的平均數較易受長尾或極端值影響，這是穩健性與變異問題，不等於產生"
                "系統性偏誤。\n中位數與分位數對極端值較穩健，適合描述偏態分布的典型位置，"
                "但它們估計的是母體中位數或分位數，不是母體平均數。增加樣本數通常降低標準"
                "誤並改善估計精度，也不會把一個原本有偏的估計量自動變成不偏。"
            )
            explanation["answerReason"] = (
                "在四個選項中，B 是官方與教學意圖下的最佳答案：增加樣本數可降低抽樣變動，"
                "中位數或分位數可穩健描述偏態資料的中心。不過，題幹只寫「母體參數」而未指"
                "明平均數、中位數或其他參數；若目標是母體平均數，改用中位數是在估計不同的"
                "參數，因此題目用語仍需人工判定或等待官方說明。"
            )
            options["A"] = (
                "若目標明確是母體平均數，隨機樣本的樣本平均數並不會只因母體偏態就成為有偏"
                "估計量；偏態主要使有限樣本的平均數較不穩健、抽樣分布較不對稱。A 仍不是本題"
                "預期答案，因為它完全未處理有限樣本下的高變動與典型中心位置的穩健描述。"
            )
            options["B"] = (
                "依官方答案與題目教學意圖，增加樣本數可降低標準誤，中位數與分位數又比平均數"
                "更不受極端值影響，因此最能穩健描述偏態分布的典型中心。但若指定估計母體平均"
                "數，中位數並非同一參數的替代估計量。"
            )
            explanation["trap"] = (
                "第一，區分「不偏」與「穩健」：樣本平均數可對母體平均數不偏，卻仍可能受長尾"
                "影響而變動很大。第二，中位數較穩健，但估計的是母體中位數。第三，重新排列"
                "資料不等於重抽樣，資料值與平均數都不會因此改變。"
            )
            explanation["editorialNote"] = (
                "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。題幹未指明"
                "「母體參數」是平均數、中位數或其他參數；本站仍依官方答案 B 判分，但保留"
                "估計目標不明的統計疑義。"
            )
            add_reference(
                explanation,
                {
                    "title": "UC Berkeley Statistics－The Sample Mean",
                    "url": "https://www.stat.berkeley.edu/~stark/Java/Html/SampleMean.htm",
                    "locator": (
                        "樣本平均數是母體平均數的不偏估計量；增加樣本數使標準誤按平方根律"
                        "下降，即使母體分布不是常態亦然"
                    ),
                    "checkedAt": CHECKED_AT,
                },
                guard["reference_count"],
            )
        elif number == 33:
            require(explanation.get("concept"), guard["concept"], "Q33 concept")
            require(options.get("D"), guard["option_d"], "Q33 option D")
            explanation["concept"] = (
                "當異常事件極為罕見時，可用的異常樣本太少，難以支撐一個穩定的監督式分類器"
                "——模型很容易把少數幾筆異常的細節當成通則。\n以重建誤差為基礎的作法只用"
                "正常資料訓練自編碼器，讓它學會重建正常序列。推論時，偏離正常模式且無法良好"
                "重建的輸入會產生較大誤差，可據此設門檻偵測。這種作法不需要異常標籤，但並不"
                "保證所有未見異常都會有高誤差；成效仍取決於正常訓練資料是否乾淨且具代表性、"
                "模型容量、門檻設定，以及異常是否也容易被模型重建。"
            )
            options["D"] = (
                "正確。只用正常資料訓練序列到序列自編碼器，模型學習正常運轉模式；推論時以"
                "重建誤差辨識偏離正常且重建不良的序列。此法不依賴稀少的異常標籤，對部分未見"
                "異常也可能有效，但不是對所有新異常型態的保證。"
            )
            add_reference(
                explanation,
                {
                    "title": (
                        "Anomaly Detection for Industrial Control Systems Using Sequence-to-Sequence "
                        "Neural Networks"
                    ),
                    "url": "https://arxiv.org/abs/1911.04831",
                    "locator": (
                        "摘要：僅以正常資料學習工業控制系統的正常狀態，再偵測偏離正常狀態"
                        "的序列"
                    ),
                    "checkedAt": CHECKED_AT,
                },
                guard["reference_count"],
            )

        question["explanationStatus"] = "draft"

    QUESTIONS.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
