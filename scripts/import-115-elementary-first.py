"""Import the two official 115 first-session elementary AIAP PDFs.

Phase one only imports official questions, options and answers. Explanations
stay empty with ``explanationStatus: "missing"``; template explanations are
forbidden by ``docs/DELIVERY_PHASES.md``.

Existing questions from other sources are preserved; re-running the script
replaces only the two 115 first-session elementary sources.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "app" / "data" / "questions.json"
PDF_DIR = Path("C:/project/iPas-quiz/tmp/pdfs")
CHECKED_AT = "2026-07-29"
OFFICIAL_RESOURCE_URL = (
    "https://ipd.nat.gov.tw/ipas/certification/AIAP/learning-resources"
)

SOURCES = [
    {
        "path": PDF_DIR / "past-09.pdf",
        "sourceId": "aiap-115-elementary-1-ai-foundation",
        "subjectCode": "ai-foundation",
        "subjectLabel": "人工智慧基礎概論",
        "subjectHeading": "第一科：",
        "pageCount": 12,
        "url": "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/115年第一次初級AI應用規劃師_第一科_人工智慧基礎概論_公告試題_20260410164304.pdf",
    },
    {
        "path": PDF_DIR / "past-10.pdf",
        "sourceId": "aiap-115-elementary-1-genai-planning",
        "subjectCode": "genai-planning",
        "subjectLabel": "生成式 AI 應用與規劃",
        "subjectHeading": "第二科：",
        "pageCount": 11,
        "url": "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/115年第一次初級AI應用規劃師_第二科_生成式AI應用與規劃_公告試題_20260410164328.pdf",
    },
]

SOURCE_IDS = {source["sourceId"] for source in SOURCES}

ANSWER_TRANSLATION = str.maketrans(
    {
        "\uff21": "A",
        "\uff22": "B",
        "\uff23": "C",
        "\uff24": "D",
    }
)

PAGE_MARKER = re.compile(r"^第\d+頁，共\d+頁$")

# 中日韓文字、全形標點與全形括號；用來移除 PDF 斷行留下的多餘空白。
CJK_LIKE = "⺀-〿㐀-鿿＀-￯"

# 官方 PDF 的字距在少數字母後被拆成兩段，需還原成原詞。
LETTER_FIXES = {
    "V AE": "VAE",
    "V olume": "Volume",
}


def clean_page(text: str, source: dict) -> str:
    lines = []
    for line in text.splitlines():
        compact = line.replace(" ", "")
        if line.startswith("115 年第一次 AI 應用規劃師"):
            continue
        if line.startswith(source["subjectHeading"]):
            continue
        if line.startswith("考試日期："):
            continue
        if PAGE_MARKER.match(compact):
            continue
        if compact in {"一、選擇題", "答案題目"}:
            continue
        if "以下空白" in compact:
            continue
        lines.append(line.rstrip())
    return "\n".join(lines)


def normalize_text(text: str) -> str:
    text = re.sub(r"([A-Za-z])-\s*\n\s*([A-Za-z])", r"\1-\2", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(rf"(?<=[{CJK_LIKE}])\s+(?=[{CJK_LIKE}])", "", text)
    text = re.sub(r"\s+(?=[\uff09\u300d\u300f\u3011])", "", text)
    text = re.sub(r"(?<=[\uff08\u300c\u300e\u3010])\s+", "", text)
    for split_word, joined_word in LETTER_FIXES.items():
        text = text.replace(split_word, joined_word)
    text = re.sub(r"\s+([；，。！？：])", r"\1", text)
    return text.strip(" \n;；")


def build_explanation(source_title: str, source_url: str) -> dict:
    # 第一階段只匯入官方題目與答案；詳解欄位保持空白，前端不顯示。
    return {
        "summary": "",
        "concept": "",
        "answerReason": "",
        "optionAnalysis": {},
        "trap": "",
        "references": [
            {
                "title": source_title,
                "url": source_url,
                "locator": "官方公告試題（題號與答案）",
                "checkedAt": CHECKED_AT,
            },
            {
                "title": "iPAS AI 應用規劃師官方學習資源",
                "url": OFFICIAL_RESOURCE_URL,
                "locator": "初級學習指引",
                "checkedAt": CHECKED_AT,
            },
        ],
        "editorialNote": "本站尚未完成本題的實質詳解，目前只顯示官方答案。",
        "author": "Claude（AI 輔助匯入）",
        "authoredAt": CHECKED_AT,
    }


def parse_source(source: dict) -> list[dict]:
    if not source["path"].exists():
        raise FileNotFoundError(f"Missing official PDF: {source['path']}")

    reader = PdfReader(source["path"])
    if len(reader.pages) != source["pageCount"]:
        raise ValueError(
            f"{source['sourceId']}: expected {source['pageCount']} pages, "
            f"found {len(reader.pages)}"
        )

    pages = [clean_page(page.extract_text() or "", source) for page in reader.pages]
    combined_parts = []
    page_starts = []
    cursor = 0
    for page_number, page in enumerate(pages, start=1):
        page_starts.append((cursor, page_number))
        combined_parts.append(page)
        cursor += len(page) + 1
    combined = "\n".join(combined_parts)

    question_pattern = re.compile(
        r"(?m)^\s*([ABCD\uff21\uff22\uff23\uff24])\s+([0-9]{1,2})[.]\s+"
    )
    matches = list(question_pattern.finditer(combined))
    if len(matches) != 50:
        found = [match.group(2) for match in matches]
        raise ValueError(f"{source['sourceId']}: expected 50 questions, found {found}")

    source_title = (
        f"115 年第一次初級 AI 應用規劃師－{source['subjectLabel']}公告試題"
    )

    questions = []
    for index, match in enumerate(matches):
        answer = match.group(1).translate(ANSWER_TRANSLATION)
        number = int(match.group(2))
        end = matches[index + 1].start() if index + 1 < len(matches) else len(combined)
        body = combined[match.end() : end]
        option_matches = list(
            re.finditer(r"(?m)^\s*[\(\uff08]([A-D])[\)\uff09]", body)
        )
        labels = [option.group(1) for option in option_matches]
        if labels != ["A", "B", "C", "D"]:
            raise ValueError(
                f"{source['sourceId']} Q{number}: invalid option labels {labels}"
            )

        prompt = normalize_text(body[: option_matches[0].start()])
        options = []
        for option_index, option_match in enumerate(option_matches):
            option_end = (
                option_matches[option_index + 1].start()
                if option_index + 1 < len(option_matches)
                else len(body)
            )
            options.append(
                {
                    "label": option_match.group(1),
                    "text": normalize_text(body[option_match.end() : option_end]),
                }
            )
        if not prompt or any(not option["text"] for option in options):
            raise ValueError(f"{source['sourceId']} Q{number}: empty prompt or option")

        source_page = 1
        for start, page_number in page_starts:
            if start <= match.start():
                source_page = page_number
            else:
                break

        questions.append(
            {
                "id": (
                    f"aiap-elementary-115-01-"
                    f"{source['subjectCode']}-{number:03d}"
                ),
                "sourceId": source["sourceId"],
                "sourceType": "official-exam",
                "level": "elementary",
                "subjectCode": source["subjectCode"],
                "subjectLabel": source["subjectLabel"],
                "rocYear": 115,
                "session": "1",
                "officialQuestionNumber": number,
                "sourcePage": source_page,
                "prompt": prompt,
                "options": options,
                "officialAnswer": [answer],
                "scoring": "single",
                "sourceUrl": source["url"],
                "answerSourceUrl": source["url"],
                "extractionStatus": "verified",
                "explanationStatus": "missing",
                "explanation": build_explanation(source_title, source["url"]),
            }
        )

    expected_numbers = list(range(1, 51))
    actual_numbers = [question["officialQuestionNumber"] for question in questions]
    if actual_numbers != expected_numbers:
        raise ValueError(
            f"{source['sourceId']}: question numbers are not exactly 1..50"
        )
    return questions


def main() -> None:
    existing = json.loads(OUTPUT.read_text(encoding="utf-8"))
    kept = [
        question for question in existing if question["sourceId"] not in SOURCE_IDS
    ]

    imported = []
    for source in SOURCES:
        imported.extend(parse_source(source))

    if len(imported) != 100:
        raise ValueError(f"Expected 100 questions, got {len(imported)}")

    questions = kept + imported
    ids = [question["id"] for question in questions]
    if len(ids) != len(set(ids)):
        raise ValueError("Question IDs are not unique")

    OUTPUT.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Imported {len(imported)} official questions; "
        f"{len(questions)} questions in {OUTPUT}"
    )


if __name__ == "__main__":
    main()
