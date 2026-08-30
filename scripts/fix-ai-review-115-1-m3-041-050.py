"""Guarded draft explanation fixes from independent AI review, Q41 and Q49.

This script is intentionally not run by the reviewer. It updates only exact
reviewed snapshots and preserves explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-intermediate-1-machine-learning"
TARGETS = {
    41: ("aiap-intermediate-115-01-machine-learning-041", ["B"], "a9ee988a196a2f326a66f13f2b3083009b55741bf597141b8317c7c5e3489947"),
    49: ("aiap-intermediate-115-01-machine-learning-049", ["C"], "e7cf6fdd944e70898df76ef477391bc170c2b4265ea979959191fcf5acad211a"),
}

# Q41 第二筆來源指向 torchvision 的物件偵測 end-to-end 範例，該頁只有單一
# `transforms = v2.Compose([...])` 訓練管線，沒有另外配置驗證用的確定性前處理，
# 無法支持原定位敘述。改引 PyTorch 遷移學習教學的 data_transforms 字典，
# 該頁明確以 'train' 做增強、'val' 只做 normalization。
OLD_REF_41 = {
    "title": "PyTorch－Transforms v2 end-to-end example",
    "url": "https://docs.pytorch.org/vision/stable/auto_examples/transforms/plot_transforms_e2e.html",
    "locator": "訓練增強與驗證確定性前處理分開配置的官方範例",
    "checkedAt": "2026-08-13",
}
NEW_REF_41 = {
    "title": "PyTorch－Transfer Learning for Computer Vision Tutorial",
    "url": "https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html",
    "locator": "Load Data 段 data_transforms 字典：註解 Data augmentation and normalization for training / Just normalization for validation，'train' 使用 RandomResizedCrop 與 RandomHorizontalFlip，'val' 只有 Resize、CenterCrop 與 Normalize",
    "checkedAt": "2026-08-30",
}

# Q49 引用的 CVPR Open Access 頁面只有摘要；摘要沒有出現 identity shortcut，
# 也沒有列出 50／101／152 三種深度（僅提到最深 152 層），原定位過度延伸。
OLD_LOCATOR_49 = "以 residual learning 與 identity shortcut 訓練 50、101、152 層網路"
NEW_LOCATOR_49 = (
    "摘要：We explicitly reformulate the layers as learning residual functions with reference to the layer inputs；"
    "these residual networks are easier to optimize, and can gain accuracy from considerably increased depth；"
    "on the ImageNet dataset we evaluate residual nets with a depth of up to 152 layers"
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

    e41 = selected[41]["explanation"]
    if len(e41["references"]) != 3 or e41["references"][2] != OLD_REF_41:
        raise RuntimeError("Guard failed for Q41 references snapshot")
    e41["references"][2] = NEW_REF_41

    e49 = selected[49]["explanation"]
    if len(e49["references"]) != 2 or e49["references"][1]["locator"] != OLD_LOCATOR_49:
        raise RuntimeError("Guard failed for Q49 references snapshot")
    e49["references"][1]["locator"] = NEW_LOCATOR_49

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
