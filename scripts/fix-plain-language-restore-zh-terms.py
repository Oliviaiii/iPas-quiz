"""把白話化時被換掉、且整題都不再出現的中文術語補回去。

名詞保留檢查（check-plain-language.py）只看英文與數字，純中文術語掉了抓不到。
以約六十個常見中文術語掃過全部 payload，原始命中 114 處，逐處裁決後：

* 58 處：該術語仍出現在同一題的其他欄位，讀者照樣遇得到，不算掉字。
* 12 處：全是「量化」的動詞義（把某件事量成數字），改寫成「換算成一個數字」
  正是白話化該做的事，不是掉了模型壓縮那個術語。
* 4 處：異體字或同義變體（常態分佈／過度擬合）、「資料的密度」多一個「的」、
  以及「標準化語意模型」的形容詞義——都不是掉字。
* 40 處：真的掉了，就是這支腳本要補的。

補的方式一律是「名詞＋白話並存」，不刪掉既有的白話說明。每一處都用逐字比對
定位，對不上就中止；同時改題庫與對應 payload 的 `new`（不動 `old` 與
`oldSha256`，那是改寫當下原文的封存）。
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
PAYLOAD_DIR = ROOT / "content" / "plain-language"
PROSE_FIELDS = ("concept", "answerReason", "trap")

# (sourceId, 題號, 欄位, 待取代的逐字片段, 補上術語後的片段)
EDITS = [
    ("aiap-114-elementary-4-ai-foundation", 20, "C",
     "看得懂是它的優點", "可解釋性高、看得懂它憑什麼這樣判是它的優點"),
    ("aiap-114-elementary-4-ai-foundation", 43, "B",
     "以及剩下的雜訊", "以及剩下的雜訊（殘差）"),
    ("aiap-114-elementary-4-genai-planning", 33, "D",
     "哪些欄位其實在講同一件事", "哪些欄位其實在講同一件事（共線性）"),
    ("aiap-114-intermediate-2-ai-tech-planning", 28, "B",
     "也讓極端值不再拉扯結果", "也讓離群值不再拉扯結果"),
    ("aiap-114-intermediate-2-ai-tech-planning", 28, "B",
     "但把每一個連續特徵都一律切段", "但把每一個連續特徵都一律切段（離散化）"),
    ("aiap-114-intermediate-2-ai-tech-planning", 41, "A",
     "已經悄悄把驗證摺的偶然特徵吃進去了",
     "已經悄悄把驗證摺的偶然特徵吃進去了，也就是對驗證資料發生了選擇性過擬合"),
    ("aiap-114-intermediate-2-ai-tech-planning", 42, "C",
     "反而更容易把舊資料的細節硬背下來", "反而更容易過擬合、把舊資料的細節硬背下來"),
    ("aiap-114-intermediate-2-ai-tech-planning", 44, "B",
     "但它學的是 P(y|x)", "但它學的是條件機率 P(y|x)"),
    ("aiap-114-intermediate-2-ai-tech-planning", 46, "C",
     "越容易挑到剛好在那批驗證資料上運氣特別好的一組",
     "越容易挑到剛好在那批驗證資料上運氣特別好的一組，也就是選擇性過擬合"),
    ("aiap-114-intermediate-2-big-data", 1, "concept",
     "換算完的數字已經沒有原始的量測單位", "標準化之後的數字已經沒有原始的量測單位"),
    ("aiap-114-intermediate-2-big-data", 9, "answerReason",
     "D 則是把連續資料切成區間類別", "D 則是把連續資料離散化、切成區間類別"),
    ("aiap-114-intermediate-2-big-data", 30, "A",
     "把每筆的猜測值減掉實際值", "把每筆的殘差、也就是猜測值減掉實際值"),
    ("aiap-114-intermediate-2-machine-learning", 5, "B",
     "真正負責縮小尺寸的多半是", "真正負責降維、縮小尺寸的多半是"),
    ("aiap-114-intermediate-2-machine-learning", 5, "trap",
     "它也會順帶把尺寸降下來", "它也會順帶降維、把尺寸降下來"),
    ("aiap-114-intermediate-2-machine-learning", 9, "B",
     "也比較好解釋", "可解釋性也比較好"),
    ("aiap-114-intermediate-2-machine-learning", 10, "D",
     "還得說得出「為什麼判這個人不過」", "還得說得出「為什麼判這個人不過」，也就是要有可解釋性"),
    ("aiap-114-intermediate-2-machine-learning", 21, "D",
     "並不保證梯度往回傳時不會衰減到消失",
     "並不保證不會梯度消失，也就是往回傳時衰減到幾乎沒有"),
    ("aiap-114-intermediate-2-machine-learning", 46, "A",
     "取決於後面有沒有把資訊擠過一個窄口", "取決於後面有沒有降維、把資訊擠過一個窄口"),
    ("aiap-114-intermediate-2-machine-learning", 46, "D",
     "真正有沒有壓縮", "真正有沒有降維壓縮"),
    ("aiap-115-elementary-1-ai-foundation", 8, "B",
     "最大的優點是看得懂它憑什麼這樣判", "最大的優點是可解釋性高——看得懂它憑什麼這樣判"),
    ("aiap-115-elementary-1-ai-foundation", 11, "A",
     "常見於報告潤稿或術語統一", "常見於報告潤稿或術語標準化"),
    ("aiap-115-elementary-1-ai-foundation", 48, "concept",
     "再由池化層把畫面縮小、留下重點", "再由池化層降維，把畫面縮小、留下重點"),
    ("aiap-115-elementary-2-ai-foundation", 13, "C",
     "樣本少的類別算出來的平均也不可靠", "樣本少的類別算出來的平均也不可靠、容易過擬合"),
    ("aiap-115-elementary-2-ai-foundation", 36, "B",
     "把數值換算到差不多的範圍", "把數值標準化到差不多的範圍"),
    ("aiap-115-elementary-2-ai-foundation", 41, "D",
     "的招牌：前面幾層看邊緣線條", "的招牌：卷積層前面幾層看邊緣線條"),
    ("aiap-115-intermediate-1-ai-tech-planning", 12, "B",
     "往回傳的學習訊號就變得非常微弱", "反向傳播往回傳的學習訊號就變得非常微弱"),
    ("aiap-115-intermediate-1-ai-tech-planning", 22, "concept",
     "盯資料有沒有跑掉", "盯資料有沒有跑掉（資料漂移）"),
    ("aiap-115-intermediate-1-ai-tech-planning", 48, "C",
     "但它對應到「是不是盜刷」的機率整個改變了",
     "但它對應到「是不是盜刷」的條件機率整個改變了"),
    ("aiap-115-intermediate-1-big-data", 5, "B",
     "再除以標準差；標準差一定是正數", "再除以標準差做標準化；標準差一定是正數"),
    ("aiap-115-intermediate-1-big-data", 10, "D",
     "資料有沒有隨時間走樣", "資料有沒有隨時間走樣（資料漂移）"),
    ("aiap-115-intermediate-1-big-data", 26, "B",
     "做的是換單位", "做的是標準化或換單位"),
    ("aiap-115-intermediate-1-big-data", 34, "C",
     "羅吉斯迴歸估的就是「在這些特徵下",
     "羅吉斯迴歸估的就是條件機率——「在這些特徵下"),
    ("aiap-115-intermediate-1-big-data", 35, "A",
     "是一種讓模型別把訓練資料背死的手法", "是一種正則化、讓模型別把訓練資料背死的手法"),
    ("aiap-115-intermediate-1-big-data", 35, "answerReason",
     "加隨機雜訊是避免死背的手法", "加隨機雜訊是正則化、避免死背的手法"),
    ("aiap-115-intermediate-1-big-data", 37, "concept",
     "模型如果把訓練資料背得太熟", "模型如果過擬合、把訓練資料背得太熟"),
    ("aiap-115-intermediate-1-big-data", 42, "B",
     "多加一項懲罰（L2）", "多加一項 L2 正則化的懲罰"),
    ("aiap-115-intermediate-1-machine-learning", 6, "C",
     "它在資料裡找出變化最大的那幾個方向", "它從資料的協方差裡找出變化最大的那幾個方向"),
    ("aiap-115-intermediate-1-machine-learning", 7, "D",
     "修正訊號一層一層往回傳時被乘到幾乎歸零",
     "修正訊號在反向傳播、一層一層往回傳時被乘到幾乎歸零"),
    ("aiap-115-intermediate-1-machine-learning", 7, "D",
     "更難向審查單位交代", "可解釋性更差，更難向審查單位交代"),
    ("aiap-115-intermediate-1-machine-learning", 14, "B",
     "沒有反覆回頭調參數那回事", "沒有反向傳播、反覆回頭調參數那回事"),
]


def patch(text: str, old_frag: str, new_frag: str, tag: str) -> str:
    if text.count(old_frag) != 1:
        raise RuntimeError(f"{tag}: 預期剛好一處錨點，實際 {text.count(old_frag)} 處")
    return text.replace(old_frag, new_frag, 1)


def main() -> None:
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    index = {(q["sourceId"], q["officialQuestionNumber"]): q for q in questions}
    payloads: dict[Path, dict] = {}

    for source_id, number, field, old_frag, new_frag in EDITS:
        tag = f"{source_id} Q{number} {field}"
        question = index.get((source_id, number))
        if question is None:
            raise RuntimeError(f"{tag}: 題庫裡找不到這一題")

        explanation = question["explanation"]
        target = explanation if field in PROSE_FIELDS else explanation["optionAnalysis"]
        original = target[field]
        target[field] = patch(original, old_frag, new_frag, tag + " (題庫)")

        touched = False
        for path in sorted(PAYLOAD_DIR.glob(f"{source_id}-*.json")):
            payload = payloads.get(path) or json.loads(path.read_text(encoding="utf-8"))
            payloads[path] = payload
            for item in payload["items"]:
                if item["officialQuestionNumber"] != number:
                    continue
                entry = (item.get("optionAnalysis") or item.get("prose") or {}).get(field)
                if entry is None or old_frag not in entry["new"]:
                    continue
                entry["new"] = patch(entry["new"], old_frag, new_frag, tag + f" ({path.name})")
                touched = True
        if not touched:
            raise RuntimeError(f"{tag}: 找不到含這個錨點的 payload")
        print(f"{tag}: 補回術語")

    QUESTIONS.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    for path, payload in payloads.items():
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(f"補了 {len(EDITS)} 處")


if __name__ == "__main__":
    main()
