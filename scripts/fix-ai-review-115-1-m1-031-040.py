"""Guarded draft reference fixes from independent AI review, Q32, Q35 and Q40.

Three cited URLs no longer resolve to the quoted content:
  Q32 torch.nn.Flatten page → HTTP 404 (PyTorch docs restructured)
  Q35 Oxford Bioinformatics DOI for BioBERT → HTTP 403 (publisher blocks agents)
  Q40 TensorRT "work-quantized-types" page → HTTP 404 (renamed)
Each is replaced by a reachable source carrying the same claim.
This script preserves explanationStatus ``draft``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
SOURCE_ID = "aiap-115-intermediate-1-ai-tech-planning"
TARGETS = {
    32: ("aiap-intermediate-115-01-ai-tech-planning-032", ["B"], "2b715c18ddc2468a61e3c607175adff5085bdec3aeb256c2c3cb54c0f96a9110"),
    35: ("aiap-intermediate-115-01-ai-tech-planning-035", ["B"], "10ad2b74afb1a48e4d7a7a3935d048ab627249c4926a0ee6109bbc5a783ee2d9"),
    40: ("aiap-intermediate-115-01-ai-tech-planning-040", ["D"], "103e611ffa22bb8c2f66d0eb32f67aca6763e9a33cfcdccc3b963678bb1e75a3"),
}

REPLACEMENTS = {
    32: (
        1,
        "https://docs.pytorch.org/docs/stable/generated/torch.nn.Flatten.html",
        {
            "title": "PyTorch Docs－torch.flatten",
            "url": "https://docs.pytorch.org/docs/stable/generated/torch.flatten.html",
            "locator": "torch.flatten(input, start_dim=0, end_dim=-1)：Flattens input by reshaping it into a one-dimensional tensor. If start_dim or end_dim are passed, only dimensions starting with start_dim and ending with end_dim are flattened；以 start_dim=1 即可保留 batch 維度",
            "checkedAt": "2026-08-30",
        },
    ),
    35: (
        2,
        "https://doi.org/10.1093/bioinformatics/btz682",
        {
            "title": "BioBERT: a pre-trained biomedical language representation model for biomedical text mining（Lee et al., 2019）",
            "url": "https://arxiv.org/abs/1901.08746",
            "locator": "摘要：以大規模生醫語料預訓練的領域專用語言表示模型，在生醫命名實體辨識、關係擷取與問答等文本探勘任務上顯著優於一般領域模型",
            "checkedAt": "2026-08-30",
        },
    ),
    40: (
        1,
        "https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/work-quantized-types.html",
        {
            "title": "NVIDIA TensorRT Documentation－Working with Quantized Types",
            "url": "https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/work-with-quantized-types.html",
            "locator": "Supported Data Types：INT8 (signed 8-bit integer)…These low-precision formats allow TensorRT to deliver efficient inference while maintaining accuracy, making it suitable for deployment in resource-constrained environments；並說明量化與浮點表示之間僅需 scaling factor 轉換",
            "checkedAt": "2026-08-30",
        },
    ),
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

    for number, (index, old_url, replacement) in REPLACEMENTS.items():
        references = selected[number]["explanation"]["references"]
        if references[index]["url"] != old_url:
            raise RuntimeError(f"Guard failed for Q{number} reference[{index}] snapshot")
        references[index] = replacement

    for question in selected.values():
        question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
