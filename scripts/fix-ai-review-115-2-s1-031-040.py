"""Guarded draft explanation fixes from independent AI review, Q33, Q34, Q37 and Q38.

All four notes opened with 「待查項目：」, which tells the human reviewer that
something still needs checking. Q33 and Q34 were in fact already-settled scope
caveats, and Q37 and Q38 were resolvable — so the prefix is dropped where the
matter is closed, and the two open questions are answered with sources.

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
    33: ("aiap-elementary-115-02-ai-foundation-033", ["B"],
         "33cbf3691aba1c4705641e00e7f11ddd9ee0c22cadf270280db1724e6ddac436"),
    34: ("aiap-elementary-115-02-ai-foundation-034", ["C"],
         "e02e8f428f53fa80d0f481685a73306b75934c8d32b3c37b4c22bbc426ae2969"),
    37: ("aiap-elementary-115-02-ai-foundation-037", ["D"],
         "26aec6b4d673d77a5f35f5305e08d5b4f31bfb64666c732d5461ed184e0bf624"),
    38: ("aiap-elementary-115-02-ai-foundation-038", ["C"],
         "fd62df84d71de3c38930a34079bc6794322474a54346f9a3cbc6c96958deeb8c"),
}

# Q33、Q34：內容本身是已經定案的適用範圍聲明，沒有待辦事項，卻掛著「待查項目」
# 的字樣，會把人工複核者的注意力引到不需要處理的地方。只改標示，語意不動。
OLD_NOTE_33 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：題幹以 2025 年照片轉公仔風格影像服務為背景，未指名特定產品；"
    "商用模型是否採 MoE 屬未公開的內部實作，本詳解僅依選項文字的架構特性作答，未認定特定產品的實作方式。查核日期 2026-08-06。"
)
NEW_NOTE_33 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。適用範圍說明（非待查）：題幹以 2025 年照片轉公仔風格影像服務為背景，未指名特定產品；"
    "商用模型是否採 MoE 屬未公開的內部實作，本詳解僅依選項文字的架構特性作答，未認定特定產品的實作方式。"
    "獨立 AI 複核確認此界定恰當，無須另行查證。查核日期 2026-08-30。"
)

OLD_NOTE_34 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：題幹將 CLIP 歸為自監督學習；"
    "CLIP 論文自述為以自然語言為監督訊號（natural language supervision），學界亦有將其歸為弱監督或圖文對比學習者。"
    "本題依官方答案聚焦兩者訓練資料型態的差異，分類名稱的歧義不影響作答。查核日期 2026-08-06。"
)
NEW_NOTE_34 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。名詞界定說明（非待查）：題幹將 CLIP 歸為自監督學習；"
    "CLIP 論文自述為以自然語言為監督訊號（natural language supervision），學界亦有將其歸為弱監督或圖文對比學習者。"
    "獨立 AI 複核已核對 CLIP 論文摘要，確認其訓練資料為取自網路的 4 億對（影像，文字）配對，"
    "本題問的是訓練資料型態差異，分類名稱的歧義確實不影響作答，無須另行查證。查核日期 2026-08-30。"
)

# Q37：原稿請複核者確認「最能直接」的判準。逐項比對後判準成立：顯著性圖以梯度
# 原生輸出像素級熱圖，LIME 與 SHAP 須先超像素分割或遮蔽取樣才能套到影像上。
OLD_NOTE_37 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：LIME 與 SHAP 經超像素分割或遮蔽取樣後亦能產生影像區域級解釋，"
    "本題判 D 的依據是題幹強調「最能直接」標示影像區域，而顯著性圖以梯度原生輸出像素級熱圖，屬程度比較而非絕對排除，建議複核者確認此判準。"
    "查核日期 2026-08-06。"
)
NEW_NOTE_37 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿請複核者確認「最能直接」的判準，獨立 AI 複核逐項比對後確認判準成立："
    "顯著性圖直接以類別分數對輸入影像求梯度，輸出即為與原圖逐像素對齊的熱圖；LIME 與 SHAP 是與資料型態無關的通用歸因框架，"
    "用於影像時須先做超像素分割或遮蔽取樣，得到的是區塊層級的近似解釋。題幹既寫明「最能直接」，D 的判定成立。"
    "此為程度比較而非絕對排除，原敘述已如此表達。待查項目結案。查核日期 2026-08-30。"
)

# Q38：原稿請複核者確認「半監督式異常偵測」的名詞用法。深度異常偵測綜述即以
# semi-supervised 稱呼「只用正常樣本訓練」的設定，官方答案的用語有文獻支持。
OLD_NOTE_38 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：「以純正常資料訓練的異常偵測」在文獻中有半監督式異常偵測、"
    "新奇偵測（novelty detection）、單類分類等不同稱呼，scikit-learn 文件歸於 novelty detection；本題依官方答案採半監督式的說法，"
    "名詞使用待複核者確認。查核日期 2026-08-06。"
)
NEW_NOTE_38 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿把「半監督式異常偵測」的名詞用法列為待查，"
    "獨立 AI 複核已找到文獻依據：Chalapathy & Chawla 的深度異常偵測綜述即以 semi-supervised 稱呼「以無異常樣本訓練」的設定"
    "（these techniques leverage existing labels of single (normally positive class) to separate outliers），"
    "與 scikit-learn 的 novelty detection、單類分類指的是同一種設定，只是稱呼不同。官方答案的用語有文獻支持，待查項目結案。"
    "查核日期 2026-08-30。"
)
NEW_REFERENCE_38 = {
    "title": "Chalapathy & Chawla, Deep Learning for Anomaly Detection: A Survey（arXiv:1901.03407）",
    "url": "https://arxiv.org/abs/1901.03407",
    "locator": (
        "第 8.2.2 節 Semi-supervised deep anomaly detection：正常樣本的標籤遠比異常容易取得，因此半監督式做法應用更廣；"
        "以無異常樣本半監督訓練的自編碼器，對正常樣本的重建誤差低於異常事件。支持本題以「半監督式異常偵測」稱呼"
        "「只用正常資料建模、判斷偏離」的設定"
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
    for number, (question_id, answer, digest) in TARGETS.items():
        question = selected[number]
        if question.get("id") != question_id or question.get("officialAnswer") != answer:
            raise RuntimeError(f"Guard failed for Q{number} identity or answer")
        if question.get("explanationStatus") != "draft" or snapshot_hash(question) != digest:
            raise RuntimeError(f"Guard failed for Q{number} status or reviewed snapshot")

    for number, old, new in (
        (33, OLD_NOTE_33, NEW_NOTE_33),
        (34, OLD_NOTE_34, NEW_NOTE_34),
        (37, OLD_NOTE_37, NEW_NOTE_37),
        (38, OLD_NOTE_38, NEW_NOTE_38),
    ):
        explanation = selected[number]["explanation"]
        if explanation.get("editorialNote") != old:
            raise RuntimeError(f"Guard failed for Q{number} editorialNote snapshot")
        explanation["editorialNote"] = new

    selected[38]["explanation"]["references"].append(NEW_REFERENCE_38)

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
