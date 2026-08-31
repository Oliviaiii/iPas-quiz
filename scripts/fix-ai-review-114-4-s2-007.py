"""Correct a mis-stated reason in the Q7 option A analysis (114-4 初級第二科).

The analysis faulted option A for placing AI Host before MCP Client. That is not
a defect: option A's order is Server → Host → Client, and the official answer C
is Host → Client → Server, so Host precedes Client in the correct answer too.
What actually makes A wrong is the direction of travel — it starts at the Server
and works inward to the Client, whereas the request has to originate at the Host
and travel outward through the Client that is embedded in it.

Found during the plain-language rewrite pass. The official answer is unaffected.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
QUESTION_ID = "aiap-elementary-114-04-genai-planning-007"
ANSWER = ["C"]
SNAPSHOT = "d71d5cbb244469c0db50afc30f87d6a4aec1a906bd971acf977b41883a5b2179"

OLD_OPTION_A = (
    "以 MCP Server 作為起點並不成立。Server 是被動提供能力的一方，等待來自 Client 的請求，"
    "不會主動去驅動 Host；而且此順序把 Host 排在 Client 之前之外，也顛倒了 Client 內嵌於 Host 的從屬關係。"
)
NEW_OPTION_A = (
    "以 MCP Server 作為起點並不成立。Server 是被動提供能力的一方，等待來自 Client 的請求，"
    "不會主動去驅動 Host；而且此順序讓請求由外往內跑（先 Server、再 Host、才到 Client），"
    "與 Client 內嵌於 Host、請求必須由內往外送出的架構正好相反。"
)


def snapshot_hash(question: dict) -> str:
    snapshot = {key: question[key] for key in ("id", "officialAnswer", "explanationStatus", "explanation")}
    payload = json.dumps(snapshot, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    selected = [q for q in questions if q.get("id") == QUESTION_ID]
    if len(selected) != 1:
        raise RuntimeError(f"Expected exactly one {QUESTION_ID}, found {len(selected)}")
    question = selected[0]
    if question.get("officialAnswer") != ANSWER:
        raise RuntimeError("Guard failed: officialAnswer changed")
    if question.get("explanationStatus") != "draft":
        raise RuntimeError("Guard failed: question is not draft")
    if snapshot_hash(question) != SNAPSHOT:
        raise RuntimeError(f"Guard failed: snapshot {snapshot_hash(question)} != {SNAPSHOT}")

    analysis = question["explanation"]["optionAnalysis"]
    if analysis["A"] != OLD_OPTION_A:
        raise RuntimeError("Guard failed: optionAnalysis.A snapshot")
    analysis["A"] = NEW_OPTION_A

    question["explanationStatus"] = "draft"
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("corrected Q7 optionAnalysis.A")


if __name__ == "__main__":
    main()
