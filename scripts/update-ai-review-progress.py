"""Rewrite docs/AI_REVIEW_PROGRESS.md from the batch reports.

The status counts and the batch table are derived data: keeping them in step
with ``reviews/ai-independent/`` by hand is how they drift. This regenerates
both from the reports themselves, and leaves the prose sections alone.

Usage::

    python scripts/update-ai-review-progress.py
"""

from __future__ import annotations

import collections
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reviews" / "ai-independent"
DOC = ROOT / "docs" / "AI_REVIEW_PROGRESS.md"
TOTAL = 600

# 每份試卷的中文名稱與複核順序，與 docs/SOURCE_INVENTORY.md 一致。
PAPERS = [
    ("aiap-114-elementary-4-ai-foundation", "114 年第四次初級－人工智慧基礎概論"),
    ("aiap-114-elementary-4-genai-planning", "114 年第四次初級－生成式 AI 應用與規劃"),
    ("aiap-115-elementary-1-ai-foundation", "115 年第一次初級－人工智慧基礎概論"),
    ("aiap-115-elementary-1-genai-planning", "115 年第一次初級－生成式 AI 應用與規劃"),
    ("aiap-115-elementary-2-ai-foundation", "115 年第二次初級－人工智慧基礎概論"),
    ("aiap-115-elementary-2-genai-planning", "115 年第二次初級－生成式 AI 應用與規劃"),
    ("aiap-114-intermediate-2-ai-tech-planning", "114 年第二次中級－人工智慧技術應用與規劃"),
    ("aiap-114-intermediate-2-big-data", "114 年第二次中級－大數據處理分析與應用"),
    ("aiap-114-intermediate-2-machine-learning", "114 年第二次中級－機器學習技術與應用"),
    ("aiap-115-intermediate-1-ai-tech-planning", "115 年第一次中級－人工智慧技術應用與規劃"),
    ("aiap-115-intermediate-1-big-data", "115 年第一次中級－大數據處理分析與應用"),
    ("aiap-115-intermediate-1-machine-learning", "115 年第一次中級－機器學習技術與應用"),
]
NAMES = dict(PAPERS)
ORDER = {source_id: index for index, (source_id, _) in enumerate(PAPERS)}


def load_batches() -> list[dict]:
    batches = []
    for path in REPORTS.glob("*.json"):
        report = json.loads(path.read_text(encoding="utf-8"))
        batches.append(report)
    batches.sort(key=lambda r: (ORDER[r["sourceId"]], r["range"]["start"]))
    return batches


def describe(counts: collections.Counter) -> str:
    parts = [f"pass {counts['pass']}"]
    for key, label in (("corrected", "corrected"), ("human-decision", "human-decision"), ("blocked", "blocked")):
        if counts[key]:
            parts.append(f"{label} {counts[key]}")
    return "完成（" + "／".join(parts) + "）"


def next_batch(done: dict[str, int]) -> str:
    for source_id, name in PAPERS:
        reviewed = done.get(source_id, 0)
        if reviewed < 50:
            return f"{name} 第 {reviewed + 1}～{reviewed + 10} 題"
    return "全部 600 題已完成獨立 AI 複核"


def main() -> None:
    batches = load_batches()
    total = collections.Counter()
    done: dict[str, int] = collections.defaultdict(int)
    rows = []
    for report in batches:
        counts = collections.Counter(item["result"] for item in report["items"])
        total.update(counts)
        done[report["sourceId"]] += len(report["items"])
        start, end = report["range"]["start"], report["range"]["end"]
        rows.append(f"| {NAMES[report['sourceId']]} | {start}～{end} | {describe(counts)} | 未開始 |")

    reviewed = sum(total.values())
    finished = [name for source_id, name in PAPERS if done.get(source_id, 0) == 50]
    pending = [(name, done[source_id]) for source_id, name in PAPERS if 0 < done.get(source_id, 0) < 50]

    if finished:
        lines = ["- 已完成整份試卷："]
        lines += [f"  - {name}（50 題）" for name in finished]
    else:
        lines = ["- 已完成整份試卷：尚無。"]
    for name, count in pending:
        lines.append(f"- 進行中：{name} 第 1～{count} 題。")

    status = "\n".join([
        f"- 固定題庫：{TOTAL} 題。",
        f"- 獨立 AI 複核：{reviewed}／{TOTAL}。",
        "- 獨立人工複核：0／600。",
        *lines,
        f"- 下一批：{next_batch(done)}。",
        f"- 累計分類：`pass {total['pass']}`、`corrected {total['corrected']}`、"
        f"`human-decision {total['human-decision']}`、`blocked {total['blocked']}`。",
    ])

    table = "\n".join([
        "| 試卷／科目 | 題號 | AI 複核結果 | 人工簽核 |",
        "| --- | --- | --- | --- |",
        *rows,
    ])

    text = DOC.read_text(encoding="utf-8")
    text = re.sub(r"^最後更新：.*$", f"最後更新：{date.today().isoformat()}", text, count=1, flags=re.M)
    text = re.sub(r"(## 目前狀態\n\n).*?(\n\nAI 複核通過不等於)", rf"\1{status}\2", text, count=1, flags=re.S)
    text = re.sub(r"(## 批次紀錄\n\n).*?(\n\n## )", rf"\1{table}\2", text, count=1, flags=re.S)
    DOC.write_text(text, encoding="utf-8")
    print(f"{reviewed}/{TOTAL} reviewed; {dict(total)}")


if __name__ == "__main__":
    main()
