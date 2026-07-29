"""Import official AIAP exam papers from the announced PDFs.

Phase one only imports official questions, options and answers. Explanations
stay empty with ``explanationStatus: "missing"``; template explanations are
forbidden by ``docs/DELIVERY_PHASES.md``.

Each batch replaces only its own ``sourceId`` values, so re-running never
touches questions imported from other papers.

Only text-only papers can be imported by this script. Papers whose questions
depend on embedded figures (charts, code screenshots, formula images) are not
listed here until the site can display those figures.

Usage::

    python scripts/import-official-exam.py 115-1
    python scripts/import-official-exam.py 115-2
    python scripts/import-official-exam.py 114-2-intermediate
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "app" / "data" / "questions.json"
PDF_DIR = Path("C:/project/iPas-quiz/tmp/pdfs")
CHECKED_AT = "2026-07-29"
OFFICIAL_RESOURCE_URL = (
    "https://ipd.nat.gov.tw/ipas/certification/AIAP/learning-resources"
)

SUBJECTS = {
    "ai-foundation": ("人工智慧基礎概論", "第一科："),
    "genai-planning": ("生成式 AI 應用與規劃", "第二科："),
    "ai-tech-planning": ("人工智慧技術應用與規劃", "第一科："),
    "big-data": ("大數據處理分析與應用", "第二科："),
    "machine-learning": ("機器學習技術與應用", "第三科："),
}

BATCHES = {
    "115-1": {
        "level": "elementary",
        "levelLabel": "初級",
        "rocYear": 115,
        "session": "1",
        "sessionLabel": "第一次",
        "idPrefix": "aiap-elementary-115-01",
        "papers": [
            {
                "path": PDF_DIR / "past-09.pdf",
                "sourceId": "aiap-115-elementary-1-ai-foundation",
                "subjectCode": "ai-foundation",
                "pageCount": 12,
                "url": "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/115年第一次初級AI應用規劃師_第一科_人工智慧基礎概論_公告試題_20260410164304.pdf",
            },
            {
                "path": PDF_DIR / "past-10.pdf",
                "sourceId": "aiap-115-elementary-1-genai-planning",
                "subjectCode": "genai-planning",
                "pageCount": 11,
                "url": "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/115年第一次初級AI應用規劃師_第二科_生成式AI應用與規劃_公告試題_20260410164328.pdf",
            },
        ],
    },
    "115-2": {
        "level": "elementary",
        "levelLabel": "初級",
        "rocYear": 115,
        "session": "2",
        "sessionLabel": "第二次",
        "idPrefix": "aiap-elementary-115-02",
        "papers": [
            {
                "path": PDF_DIR / "past-11.pdf",
                "sourceId": "aiap-115-elementary-2-ai-foundation",
                "subjectCode": "ai-foundation",
                "pageCount": 13,
                "url": "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/115年第二次初級AI應用規劃師_第一科_人工智慧基礎概論_公告試題_20260604212644.pdf",
            },
            {
                "path": PDF_DIR / "past-12.pdf",
                "sourceId": "aiap-115-elementary-2-genai-planning",
                "subjectCode": "genai-planning",
                "pageCount": 13,
                "url": "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/115年第二次初級AI應用規劃師_第二科_生成式AI應用與規劃_公告試題_20260604212719.pdf",
            },
        ],
    },
    "114-2-intermediate": {
        "level": "intermediate",
        "levelLabel": "中級",
        "rocYear": 114,
        "session": "2",
        "sessionLabel": "第二次",
        "idPrefix": "aiap-intermediate-114-02",
        "papers": [
            {
                "path": PDF_DIR / "past-01.pdf",
                "sourceId": "aiap-114-intermediate-2-ai-tech-planning",
                "subjectCode": "ai-tech-planning",
                "pageCount": 14,
                "url": "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/114年第二梯次中級AI應用規劃師第一科人工智慧技術應用與規劃(當次試題公告114_20251226000616.pdf",
            },
            # 第二科與第三科各有 7 題、10 題依賴 PDF 內嵌圖片（圖表、程式碼截圖、
            # 公式圖），在網站能顯示這些圖片前不匯入，以免題目殘缺。
        ],
    },
}

ANSWER_TRANSLATION = str.maketrans(
    {
        "\uff21": "A",
        "\uff22": "B",
        "\uff23": "C",
        "\uff24": "D",
    }
)

PAGE_MARKER = re.compile(r"^第\d+頁，共\d+頁$")
PAGE_HEADER = re.compile(r"^\d+年第[一二三四]次AI應用規劃師-[初中]級能力鑑定")

# 中日韓文字、全形標點與全形括號；用來移除 PDF 斷行留下的多餘空白。
CJK_LIKE = "⺀-〿㐀-鿿＀-￯"

# 官方 PDF 的字距在少數字母後被拆成兩段，需還原成原詞。
# 較長的鍵必須排在前面：文字層在「V olume與」之間沒有空白，還原後要補回。
LETTER_FIXES = {
    "V olume與": "Volume 與",
    "V AE": "VAE",
    "V olume": "Volume",
}


def clean_page(text: str, subject_heading: str) -> str:
    """Drop the repeated page furniture so cross-page questions join cleanly."""
    lines = []
    for index, line in enumerate(text.splitlines()):
        stripped = line.strip()
        compact = line.replace(" ", "")
        if PAGE_HEADER.match(compact):
            continue
        if stripped.startswith(subject_heading):
            continue
        if compact.startswith("考試日期："):
            continue
        if PAGE_MARKER.match(compact):
            continue
        if compact in {"一、選擇題", "答案題目"}:
            continue
        # 中級試卷的「答案」欄標題有時被拆成單獨的「答」、「案」兩行；
        # 只在頁首範圍內移除，避免誤刪題目內容。
        if index < 10 and compact in {"答", "案", "題目"}:
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


def parse_paper(batch: dict, paper: dict) -> list[dict]:
    if not paper["path"].exists():
        raise FileNotFoundError(f"Missing official PDF: {paper['path']}")

    subject_label, subject_heading = SUBJECTS[paper["subjectCode"]]
    reader = PdfReader(paper["path"])
    if len(reader.pages) != paper["pageCount"]:
        raise ValueError(
            f"{paper['sourceId']}: expected {paper['pageCount']} pages, "
            f"found {len(reader.pages)}"
        )

    pages = [
        clean_page(page.extract_text() or "", subject_heading)
        for page in reader.pages
    ]
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
        raise ValueError(f"{paper['sourceId']}: expected 50 questions, found {found}")

    source_title = (
        f"{batch['rocYear']} 年{batch['sessionLabel']}{batch['levelLabel']}"
        f" AI 應用規劃師－{subject_label}公告試題"
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
                f"{paper['sourceId']} Q{number}: invalid option labels {labels}"
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
            raise ValueError(f"{paper['sourceId']} Q{number}: empty prompt or option")

        source_page = 1
        for start, page_number in page_starts:
            if start <= match.start():
                source_page = page_number
            else:
                break

        questions.append(
            {
                "id": (
                    f"{batch['idPrefix']}-{paper['subjectCode']}-{number:03d}"
                ),
                "sourceId": paper["sourceId"],
                "sourceType": "official-exam",
                "level": batch["level"],
                "subjectCode": paper["subjectCode"],
                "subjectLabel": subject_label,
                "rocYear": batch["rocYear"],
                "session": batch["session"],
                "officialQuestionNumber": number,
                "sourcePage": source_page,
                "prompt": prompt,
                "options": options,
                "officialAnswer": [answer],
                "scoring": "single",
                "sourceUrl": paper["url"],
                "answerSourceUrl": paper["url"],
                "extractionStatus": "verified",
                "explanationStatus": "missing",
                "explanation": build_explanation(source_title, paper["url"]),
            }
        )

    expected_numbers = list(range(1, 51))
    actual_numbers = [question["officialQuestionNumber"] for question in questions]
    if actual_numbers != expected_numbers:
        raise ValueError(
            f"{paper['sourceId']}: question numbers are not exactly 1..50"
        )
    return questions


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in BATCHES:
        raise SystemExit(f"usage: {sys.argv[0]} [{'|'.join(BATCHES)}]")
    batch_key = sys.argv[1]
    batch = BATCHES[batch_key]
    source_ids = {paper["sourceId"] for paper in batch["papers"]}

    existing = json.loads(OUTPUT.read_text(encoding="utf-8"))
    kept = [question for question in existing if question["sourceId"] not in source_ids]

    imported = []
    for paper in batch["papers"]:
        imported.extend(parse_paper(batch, paper))

    expected_total = 50 * len(batch["papers"])
    if len(imported) != expected_total:
        raise ValueError(f"Expected {expected_total} questions, got {len(imported)}")

    questions = kept + imported
    ids = [question["id"] for question in questions]
    if len(ids) != len(set(ids)):
        raise ValueError("Question IDs are not unique")

    OUTPUT.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Imported {len(imported)} official questions for {batch_key}; "
        f"{len(questions)} questions in {OUTPUT}"
    )


if __name__ == "__main__":
    main()
