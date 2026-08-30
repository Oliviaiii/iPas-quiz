"""Guarded draft reference fixes from independent AI review, Q43, Q46 and Q48.

Q43 repeats the arXiv 1606.07659 mis-attribution already corrected on Q19: that
arXiv ID is "Hybrid Recommender System based on Autoencoders", not a Kohavi
A/B-testing paper. Q46's HHS cloud-computing guidance page and Q48's ACM DOI
both return HTTP 403 to any agent, so their locators cannot be resolved there.
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
    43: ("aiap-intermediate-115-01-ai-tech-planning-043", ["C"], "d460af1655026f503442880ad4d344e4dc9c9410f3787cbdff2c55912004baa1"),
    46: ("aiap-intermediate-115-01-ai-tech-planning-046", ["C"], "437ffa4234511c5e71141bdb52b116d248af430aec8c00cb87c92a3fff430616"),
    48: ("aiap-intermediate-115-01-ai-tech-planning-048", ["C"], "2ce0079cc2cd7240e1adec5af06b766c58f98e74d8047b3a889dbadfafe9cfc0"),
}

REPLACEMENTS = {
    43: (
        2,
        "https://arxiv.org/abs/1606.07659",
        {
            "title": "Online Controlled Experiments at Large Scale（Kohavi et al., KDD 2013）",
            "url": "https://exp-platform.com/Documents/2013%20controlledExperimentsAtScale.pdf",
            "locator": "§2：使用者被 randomly split between the variants…Their interactions with the site are instrumented and key metrics computed，說明以線上隨機對照實驗量測真實業務指標",
            "checkedAt": "2026-08-30",
        },
    ),
    46: (
        2,
        "https://www.hhs.gov/hipaa/for-professionals/special-topics/health-information-technology/cloud-computing/index.html",
        {
            "title": "45 CFR §160.103－Definitions（Business associate）",
            "url": "https://www.govinfo.gov/content/pkg/CFR-2023-title45-vol2/pdf/CFR-2023-title45-vol2-sec160-103.pdf",
            "locator": "Business associate 定義 (1)(i)：代表 covered entity 而 creates, receives, maintains, or transmits protected health information 之人；雲端服務商保存 PHI 即落入此定義，須簽訂 business associate contract",
            "checkedAt": "2026-08-30",
        },
    ),
    48: (
        1,
        "https://dl.acm.org/doi/10.1145/2523813",
        {
            "title": "A Survey on Concept Drift Adaptation（Gama, Žliobaitė, Bifet, Pechenizkiy & Bouchachia, ACM Computing Surveys 2014）",
            "url": "https://www.win.tue.nl/~mpechen/publications/pubs/Gama_ACMCS_AdaptationCD_accepted.pdf",
            "locator": "§1：The real concept drift refers to changes in the conditional distribution of the output (i.e., target variable) given the input (input features), while the distribution of the input may stay unchanged；§2 另定義 virtual drift 為 p(X) 改變而 p(y|X) 不變",
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
