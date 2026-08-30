"""Guarded draft explanation fix from independent AI review, Q27.

The draft leaned on the official study guide's anomaly-detection passage, which
sits under variational autoencoders rather than plain autoencoders, and left a
pending note asking whether a dedicated source was needed. It was, and one
exists, so the note is closed and the source added.

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
    27: ("aiap-elementary-115-02-ai-foundation-027", ["A"],
         "6c5636c5b36fe6df3388f9b149935f1853e37fc9ee9450a81682622c3968265d"),
}

OLD_NOTE_27 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。待查項目：官方學習指引 3-53 的異常檢測應用段落係針對變分自編碼器（自編碼器的變形）撰寫，"
    "本題選項僅稱自編碼器，重建誤差偵測異常的原理相同；複核者可確認是否需補一般自編碼器異常偵測的專門出處。查核日期 2026-08-06。"
)
NEW_NOTE_27 = (
    "本站自編的 AI 輔助詳解初稿，並非官方詳解；尚待獨立人工複核。原稿指出官方學習指引的異常檢測段落係針對變分自編碼器撰寫，"
    "並問是否需補一般自編碼器的專門出處。獨立 AI 複核判斷需要，已補入 Chalapathy & Chawla 的深度異常偵測綜述："
    "該文明載自編碼器是非監督深度異常偵測的基礎架構，並以重建誤差的大小作為異常分數。待查項目結案。查核日期 2026-08-30。"
)
NEW_REFERENCE_27 = {
    "title": "Chalapathy & Chawla, Deep Learning for Anomaly Detection: A Survey（arXiv:1901.03407）",
    "url": "https://arxiv.org/abs/1901.03407",
    "locator": (
        "第 10.5 節逐字核對：Autoencoders are the fundamental unsupervised deep architectures used in anomaly detection；"
        "第 8.5.2 節：Unsupervised anomaly detection techniques using autoencoders measure the magnitude of the residual "
        "vector (i.e reconstruction error) for obtaining anomaly scores；第 8.2 節並說明以無異常樣本半監督訓練後，"
        "正常樣本的重建誤差低於異常事件"
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

    e27 = selected[27]["explanation"]
    if e27.get("editorialNote") != OLD_NOTE_27:
        raise RuntimeError("Guard failed for Q27 editorialNote snapshot")
    e27["editorialNote"] = NEW_NOTE_27
    e27["references"].append(NEW_REFERENCE_27)

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
