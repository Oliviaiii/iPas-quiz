"""把白話化時被換掉的「低秩」補回改寫文字裡。

名詞保留檢查只看英文與數字，純中文術語（低秩）掉了抓不到。這支腳本只改
payload 的 `new`，不動 `old`／`oldSha256`，並重新套用 payload builder 的長度
與「正確」開頭防護。每一處都用逐字比對定位，對不上就中止。
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "content" / "plain-language"

# (檔名, 題號, 欄位, 待取代的逐字片段, 換成什麼)
EDITS = [
    ("aiap-114-intermediate-2-machine-learning-026-050-prose.json", 46, "concept",
     "才會用少數幾個方向去近似重建",
     "才會用少數幾個方向去做低秩近似重建（低秩＝只留下少數幾個獨立方向）"),
    ("aiap-115-intermediate-1-machine-learning-001-025.json", 21, "C",
     "拆成幾張小表相乘來近似原本那張",
     "拆成幾張小表（低秩矩陣，行列數都比原本窄很多）相乘來近似原本那張"),
    ("aiap-115-intermediate-1-ai-tech-planning-001-025.json", 2, "A",
     "只是在旁邊掛上一小塊可訓練的零件",
     "只是在旁邊掛上一小塊可訓練的零件、做低秩更新"),
    ("aiap-115-intermediate-1-ai-tech-planning-001-025.json", 2, "C",
     "限制成兩個小矩陣相乘的結果",
     "限制成低秩矩陣乘積，也就是兩個又窄又長的小矩陣相乘的結果"),
    ("aiap-115-intermediate-1-ai-tech-planning-001-025.json", 14, "A",
     "只讓另外掛上去的少量新模組（LoRA 層）",
     "只讓另外掛上去的低秩適配器（LoRA 層，那一小塊窄窄的可訓練模組）"),
    ("aiap-115-intermediate-1-machine-learning-026-050.json", 35, "A",
     "等於讓每一層的 LoRA 補丁變厚",
     "等於讓每一層的低秩更新（LoRA 補丁）變厚"),
]


def main() -> None:
    touched: dict[str, dict] = {}
    for name, number, field, old_frag, new_frag in EDITS:
        path = DIR / name
        payload = touched.get(name) or json.loads(path.read_text(encoding="utf-8"))
        touched[name] = payload
        for item in payload["items"]:
            if item["officialQuestionNumber"] != number:
                continue
            entry = (item.get("optionAnalysis") or item.get("prose"))[field]
            text = entry["new"]
            if old_frag not in text:
                raise RuntimeError(f"{name} Q{number} {field}: 找不到待取代片段")
            if "低秩" in text:
                raise RuntimeError(f"{name} Q{number} {field}: 已經有「低秩」了")
            fixed = text.replace(old_frag, new_frag, 1)
            # 重新套用 builder 的兩道防護。
            original = entry["old"]
            if original.startswith("正確") and not fixed.startswith("正確"):
                raise RuntimeError(f"{name} Q{number} {field}: 正確 開頭掉了")
            if len(fixed) < len(original) * 0.8:
                raise RuntimeError(f"{name} Q{number} {field}: 太短")
            entry["new"] = fixed
            print(f"{name} Q{number} {field}: 補回低秩")
            break
        else:
            raise RuntimeError(f"{name}: 找不到 Q{number}")

    for name, payload in touched.items():
        (DIR / name).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(f"改了 {len(touched)} 個 payload、{len(EDITS)} 個欄位")


if __name__ == "__main__":
    main()
