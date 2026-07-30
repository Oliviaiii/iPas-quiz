"""Import official AIAP exam papers from the announced PDFs.

Phase one only imports official questions, options and answers. Explanations
stay empty with ``explanationStatus: "missing"``; template explanations are
forbidden by ``docs/DELIVERY_PHASES.md``.

Each batch replaces only its own ``sourceId`` values, so re-running never
touches questions imported from other papers.

Papers whose questions depend on embedded figures (charts, code screenshots,
formula images) additionally need a hand-reviewed figure map named by the
batch's ``figureMap`` key. A batch that declares one fails until the reviewed
map and the extracted images are both present, so a figure-bearing paper can
never be imported as text-only.

Official PDFs are not committed. Download them into ``tmp/pdfs`` (gitignored)
with ``scripts/fetch-official-pdfs.py``, or point ``IPAS_PDF_DIR`` at wherever
they already are.

Usage::

    python scripts/import-official-exam.py 115-1
    python scripts/import-official-exam.py 115-2
    python scripts/import-official-exam.py 114-2-intermediate
    python scripts/import-official-exam.py 115-1-intermediate
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "app" / "data" / "questions.json"
FIGURE_DIR = ROOT / "public" / "images" / "questions"
# 官方 PDF 不進版控；預設放在 repo 的 tmp/pdfs，可用 IPAS_PDF_DIR 指到別處。
PDF_DIR = Path(os.environ.get("IPAS_PDF_DIR") or ROOT / "tmp" / "pdfs")
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
        "figureMap": "figures-114-2-intermediate.json",
        "figureDir": "figures-114-2",
        "papers": [
            {
                "path": PDF_DIR / "past-01.pdf",
                "sourceId": "aiap-114-intermediate-2-ai-tech-planning",
                "subjectCode": "ai-tech-planning",
                "pageCount": 14,
                "url": "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/114年第二梯次中級AI應用規劃師第一科人工智慧技術應用與規劃(當次試題公告114_20251226000616.pdf",
            },
            {
                "path": PDF_DIR / "past-02.pdf",
                "sourceId": "aiap-114-intermediate-2-big-data",
                "subjectCode": "big-data",
                "pageCount": 17,
                "figureTag": "s2",
                "url": "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/114年第二梯次中級AI應用規劃師第二科大數據處理分析與應用(當次試題公告114_20251226000634.pdf",
            },
            {
                "path": PDF_DIR / "past-03.pdf",
                "sourceId": "aiap-114-intermediate-2-machine-learning",
                "subjectCode": "machine-learning",
                "pageCount": 19,
                "figureTag": "s3",
                "url": "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/114年第二梯次中級AI應用規劃師第三科機器學習技術與應用(當次試題公告114_20251226000650.pdf",
            },
        ],
    },
    # 115 年第一次中級三科。網址取自 app/data/sources.json，已確認每科 50 題。
    # 中級試卷含題目內嵌圖片，因此本批宣告 figureMap；在產出經人工逐頁複核的
    # 對照表之前，匯入會直接失敗，不會把圖片題匯成只有文字的殘缺題目。
    # pageCount 留 None：取得官方 PDF 後由腳本印出實際頁數，再回填釘住。
    "115-1-intermediate": {
        "level": "intermediate",
        "levelLabel": "中級",
        "rocYear": 115,
        "session": "1",
        "sessionLabel": "第一次",
        "idPrefix": "aiap-intermediate-115-01",
        "figureMap": "figures-115-1-intermediate.json",
        "figureDir": "figures-115-1",
        "papers": [
            {
                "path": PDF_DIR / "past-06.pdf",
                "sourceId": "aiap-115-intermediate-1-ai-tech-planning",
                "subjectCode": "ai-tech-planning",
                "pageCount": None,
                "figureTag": "s1",
                "url": "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/115年第一次中級AI應用規劃師_第一科_人工智慧技術應用與規劃_公告試題_20260615003359.pdf",
            },
            {
                "path": PDF_DIR / "past-07.pdf",
                "sourceId": "aiap-115-intermediate-1-big-data",
                "subjectCode": "big-data",
                "pageCount": None,
                "figureTag": "s2",
                "url": "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/115年第一次中級AI應用規劃師_第二科_大數據處理分析與應用_公告試題_20260615003417.pdf",
            },
            {
                "path": PDF_DIR / "past-08.pdf",
                "sourceId": "aiap-115-intermediate-1-machine-learning",
                "subjectCode": "machine-learning",
                "pageCount": None,
                "figureTag": "s3",
                "url": "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/115年第一次中級AI應用規劃師_第三科_機器學習技術與應用_公告試題_20260615003428.pdf",
            },
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
# 題組敘述在官方版面自成一列，答案欄留白，文字層固定以兩個半形空白開頭。
PASSAGE_START = re.compile(r"(?m)^ {2}\S")
PASSAGE_RANGE = re.compile(r"(\d{1,2})\s*[~～－-]\s*(\d{1,2})\s*題")
# 程式碼、輸出與表格等需要保留排版的行。
PRE_LINE = re.compile(r"^ {3,}\S|^[A-Za-z_][A-Za-z0-9_ /]*：|^[-=]{5,}")

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


def load_figures(batch: dict, paper: dict) -> dict:
    """Return {slot key: [figure]} for a paper, from the reviewed mapping file."""
    tag = paper.get("figureTag")
    if not tag:
        return {}
    figure_map = Path(__file__).with_name(batch["figureMap"])
    if not figure_map.exists():
        raise FileNotFoundError(
            f"{paper['sourceId']} declares figures but the reviewed figure map "
            f"{figure_map} does not exist. Render the official PDF, check every "
            "figure against its page, and write the map before importing — a "
            "figure-bearing paper must not be imported as text only."
        )
    mapping = json.loads(figure_map.read_text(encoding="utf-8"))
    entries = mapping[paper["subjectCode"]]
    extracted_dir = PDF_DIR / batch["figureDir"]
    figures: dict = {}
    for file_name, entry in entries.items():
        page = int(re.search(r"-p(\d+)-", file_name).group(1))
        source = extracted_dir / file_name
        if not source.exists():
            raise FileNotFoundError(f"Missing extracted figure: {source}")
        target_name = f"{paper['sourceId']}-{file_name.split('-', 1)[1]}"
        FIGURE_DIR.mkdir(parents=True, exist_ok=True)
        (FIGURE_DIR / target_name).write_bytes(source.read_bytes())
        with Image.open(source) as image:
            width, height = image.size
        if entry["slot"] == "passage":
            key = ("passage", entry["passage"])
            alt = f"官方試題第 {entry['passage']} 題題組附圖（第 {page} 頁）"
        else:
            key = (entry["question"], entry["slot"])
            position = "題幹" if entry["slot"] == "prompt" else f"選項 {entry['slot']}"
            alt = f"官方試題第 {entry['question']} 題{position}附圖（第 {page} 頁）"
        figure = {
            "src": f"/images/questions/{target_name}",
            "alt": alt,
            "width": width,
            "height": height,
        }
        figures.setdefault(key, []).append((page, figure))
    return {
        key: [figure for _, figure in sorted(items, key=lambda item: item[0])]
        for key, items in figures.items()
    }


def build_passage_blocks(text: str, page_of, offset: int, figures: list) -> list[dict]:
    """Split a shared passage into text, pre-formatted and figure blocks."""
    figures_by_page: dict[int, list] = {}
    for figure in figures:
        page = int(re.search(r"-p(\d+)-", figure["src"]).group(1))
        figures_by_page.setdefault(page, []).append(figure)

    blocks: list[dict] = []
    buffer: list[str] = []
    mode = None
    cursor = offset

    def flush() -> None:
        nonlocal buffer, mode
        if not buffer:
            return
        if mode == "pre":
            blocks.append({"kind": "pre", "text": "\n".join(buffer).rstrip()})
        else:
            joined = normalize_text(" ".join(buffer))
            if joined:
                blocks.append({"kind": "text", "text": joined})
        buffer = []
        mode = None

    current_page = page_of(cursor)
    for line in text.splitlines():
        line_page = page_of(cursor)
        cursor += len(line) + 1
        if line_page != current_page:
            flush()
            for figure in figures_by_page.pop(current_page, []):
                blocks.append({"kind": "figure", "figure": figure})
            current_page = line_page
        if not line.strip():
            flush()
            continue
        line_mode = "pre" if PRE_LINE.match(line) else "text"
        if mode and line_mode != mode:
            flush()
        mode = line_mode
        buffer.append(line if line_mode == "pre" else line.strip())
    flush()
    for page in sorted(figures_by_page):
        for figure in figures_by_page[page]:
            blocks.append({"kind": "figure", "figure": figure})
    return blocks


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
    if paper["pageCount"] is None:
        # 新試卷第一次匯入時還不知道頁數；印出實際值供回填釘住。
        print(
            f"{paper['sourceId']}: pageCount not pinned yet, "
            f"found {len(reader.pages)} pages"
        )
    elif len(reader.pages) != paper["pageCount"]:
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

    def page_of(position: int) -> int:
        page_number = 1
        for start, number in page_starts:
            if start <= position:
                page_number = number
            else:
                break
        return page_number

    figures = load_figures(batch, paper)
    passages: dict[int, dict] = {}

    questions = []
    for index, match in enumerate(matches):
        answer = match.group(1).translate(ANSWER_TRANSLATION)
        number = int(match.group(2))
        end = matches[index + 1].start() if index + 1 < len(matches) else len(combined)
        body = combined[match.end() : end]

        # 題組敘述接在前一題選項之後，屬於後續題目而非本題。
        passage_match = PASSAGE_START.search(body)
        if passage_match:
            passage_text = body[passage_match.start() :]
            body = body[: passage_match.start()]
            range_match = PASSAGE_RANGE.search(passage_text.replace(" ", ""))
            if not range_match:
                raise ValueError(
                    f"{paper['sourceId']}: passage after Q{number} has no range"
                )
            first, last = int(range_match.group(1)), int(range_match.group(2))
            member_numbers = list(range(first, last + 1))
            passage = {
                "questionNumbers": member_numbers,
                "blocks": build_passage_blocks(
                    passage_text,
                    page_of,
                    match.end() + passage_match.start(),
                    figures.get(("passage", f"{first}-{last}"), []),
                ),
            }
            for member in member_numbers:
                passages[member] = passage

        option_matches = list(
            re.finditer(r"(?m)^\s*[\(\uff08]([A-D])[\)\uff09]", body)
        )
        labels = [option.group(1) for option in option_matches]
        if labels != ["A", "B", "C", "D"]:
            # 少數題目把四個選項排在同一行，改用不限行首的比對。
            option_matches = list(re.finditer(r"[\(\uff08]([A-D])[\)\uff09]", body))
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
            label = option_match.group(1)
            option = {
                "label": label,
                "text": normalize_text(body[option_match.end() : option_end]),
            }
            option_figures = figures.get((number, label))
            if option_figures:
                option["figures"] = option_figures
            options.append(option)

        prompt_figures = figures.get((number, "prompt"))
        if not prompt and not prompt_figures:
            raise ValueError(f"{paper['sourceId']} Q{number}: empty prompt")
        for option in options:
            if not option["text"] and not option.get("figures"):
                raise ValueError(
                    f"{paper['sourceId']} Q{number}: empty option {option['label']}"
                )

        question = {
            "id": f"{batch['idPrefix']}-{paper['subjectCode']}-{number:03d}",
            "sourceId": paper["sourceId"],
            "sourceType": "official-exam",
            "level": batch["level"],
            "subjectCode": paper["subjectCode"],
            "subjectLabel": subject_label,
            "rocYear": batch["rocYear"],
            "session": batch["session"],
            "officialQuestionNumber": number,
            "sourcePage": page_of(match.start()),
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
        if prompt_figures:
            question["figures"] = prompt_figures
        questions.append(question)

    for question in questions:
        passage = passages.get(question["officialQuestionNumber"])
        if passage:
            question["passage"] = passage

    unused = set(figures) - {
        ("passage", f"{p['questionNumbers'][0]}-{p['questionNumbers'][-1]}")
        for p in passages.values()
    }
    unused = {
        key
        for key in unused
        if not isinstance(key[0], int)
        or not any(
            q["officialQuestionNumber"] == key[0]
            and (key[1] == "prompt" or any(o["label"] == key[1] for o in q["options"]))
            for q in questions
        )
    }
    if unused:
        raise ValueError(f"{paper['sourceId']}: unattached figures {sorted(unused)}")

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

    # 固定輸出順序，重跑任何批次都不會讓其他題目在檔案中移位。
    questions = sorted(
        kept + imported,
        key=lambda question: (
            question["level"],
            question["rocYear"],
            question["session"],
            question["subjectCode"],
            question["officialQuestionNumber"],
        ),
    )
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
