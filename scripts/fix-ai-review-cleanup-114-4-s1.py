"""Close the two residual open 待查 items in 114-4 初級第一科 (Q10, Q49).

Follow-up cleanup pass after all 600 questions completed independent AI review.
Guards on the exact reviewed snapshot and preserves explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-114-elementary-4-ai-foundation"
TARGETS = {
    10: ("aiap-elementary-114-04-ai-foundation-010", ["C"], "c1dad3a5f9d3bab634af1e46df3e4cb5fa1d6598abc5c01338f83b82ffe2e9be", 3),
    49: ("aiap-elementary-114-04-ai-foundation-049", ["A"], "8bfef4784e2f71e06b2573a810c5998326082d5ee2ad1baa8af56d5d282c3059", 2),
}

NEW_LOCATOR_10 = (
    "規範全文（本會 114 年 5 月 29 日第 14 屆第 25 次理監事聯席會議核議通過、金管會 114 年 10 月 2 日金管銀國字第 1140219072 號函洽悉）："
    "第九條「金融機構應指定高階主管或委員會負責人工智慧相關監督管理並建立內部治理架構，指派單位或人員負責人工智慧之推動及管理，"
    "落實辦理人才培育，提供適當之培訓資源。負責運用生成式人工智慧技術之人員，應清楚了解生成式人工智慧技術運作方式以及如何做出回應」；"
    "第十三條要求以風險基礎為導向建立「適當之風險管理及定期檢視機制」，必要時得由具人工智慧專業之獨立第三人出具評估報告"
)

NEW_NOTE_10 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
    "原稿把「尚未逐條比對規範全文」列為待查，獨立 AI 複核已下載規範 PDF 並逐條核對："
    "第九條一條之內同時涵蓋選項 D（指定高階主管或委員會負責監督管理並建立內部治理架構）、"
    "選項 A（落實辦理人才培育，提供適當之培訓資源）與選項 B（負責運用生成式人工智慧技術之人員，"
    "應清楚了解生成式人工智慧技術運作方式以及如何做出回應）；第十三條要求的是「適當之風險管理及定期檢視機制」，"
    "規範全文十六條並無任何每日對外公布系統運作狀況的義務，佐證選項 C 不在明訂措施之列。"
    "另註：規範現行版本為 114 年 5 月修正版，學習指引參考書目所載的 113 年 3 月版為前一版本，"
    "本題涉及的治理條文在兩版之間並無實質差異。待查項目結案。查核日期 2026-08-30。"
)

NEW_NOTE_49 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。"
    "原稿把「評測中心逐項列舉大型語言模型安全性常見使用指標的原始文件」列為待查，"
    "獨立 AI 複核已查核 AI 產品與系統評測中心（AIEC）官網：成立背景頁列出 10 項評測項目並逐項給出定義"
    "（安全性、可解釋性、韌性、公平性、準確性、透明性、當責性、可靠性、隱私、資安），"
    "主要評測項目頁另列準確性、可靠性、公平性、隱私、資安五項的評測說明；兩處都沒有把「事實正確性、偏見與歧視、"
    "惡意與濫用可能性」列成一組具名的安全性指標，該組措辭應出自試題本身，此方向查無官方逐項清單。"
    "惟本題答案不依賴該具名清單：對照官方 10 項評測項目，事實正確性對應準確性、偏見與歧視對應公平性"
    "（其定義明載「避免偏見、歧視或不公正對待」）、惡意與濫用可能性對應安全性與資安"
    "（資安定義明載「面對外部攻擊、未授權訪問或不當使用」），只有「資料複雜性」在 10 項中找不到任何對應。"
    "待查項目以此結案。查核日期 2026-08-30。"
)

NEW_REFS_49 = [
    {
        "title": "AI 產品與系統評測中心（AIEC）－成立背景",
        "url": "https://www.aiec.org.tw/web/guest/background",
        "locator": (
            "AI 評測中心目標段：研析 NIST、ISO 及歐盟等國際 AI 規範後「擬建立下列 10 項評測項目」——"
            "安全性(Safety)、可解釋性(Explainability)、韌性(Resiliency)、公平性(Fairness)、準確性(Accuracy)、"
            "透明性(Transparency)、當責性(Accountability)、可靠性(Reliability)、隱私(Privacy)、資安(Security)，"
            "各項均附定義；清單中無「資料複雜性」"
        ),
        "checkedAt": "2026-08-30",
    },
    {
        "title": "AI 產品與系統評測中心（AIEC）－主要評測項目",
        "url": "https://www.aiec.org.tw/service",
        "locator": (
            "現行主要評測項目頁列出準確性、可靠性、公平性、隱私、資安五項及其評測說明；"
            "公平性說明「要求系統避免偏見、歧視或不公正對待」，資安說明「面對外部攻擊、未授權訪問或不當使用」"
        ),
        "checkedAt": "2026-08-30",
    },
]


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

    e10 = selected[10]["explanation"]
    if "ba.org.tw" not in e10["references"][1]["url"]:
        raise RuntimeError("Guard failed for Q10 reference 1 target")
    e10["references"][1]["locator"] = NEW_LOCATOR_10
    e10["references"][1]["checkedAt"] = "2026-08-30"
    e10["editorialNote"] = NEW_NOTE_10

    e49 = selected[49]["explanation"]
    if "moda.gov.tw" not in e49["references"][1]["url"]:
        raise RuntimeError("Guard failed for Q49 reference 1 target")
    e49["references"].extend(NEW_REFS_49)
    e49["editorialNote"] = NEW_NOTE_49

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
