"""Print one independent-AI-review batch side by side with the official PDF.

The reviewer needs three things per question: what the official PDF says, what
the question bank stores, and the existing explanation draft. Assembling those
by hand for every 10-question batch is where transcription mistakes creep in,
so this script does it mechanically.

The published papers lay each question out as a two-column table: a narrow left
column holding the official answer letter and a wide right column holding the
stem and options. ``--answers`` re-pairs those columns by vertical position so
the extracted answer key can be diffed against ``officialAnswer`` in the bank.

Usage::

    python scripts/ai-review-context.py <sourceId> <start> <end>
    python scripts/ai-review-context.py <sourceId> --answers
    python scripts/ai-review-context.py <sourceId> --pages 7-9
    python scripts/ai-review-context.py <sourceId> --render 7,8 --out tmp/png
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "app" / "data" / "questions.json"
PDF_DIR = Path("tmp/pdfs")
# 左欄僅放答案字母，起點約在頁寬的 0.10～0.13；題目欄起點約 0.20。
ANSWER_COLUMN_RATIO = 0.17
# 題號在不同年度的試卷上有「12.」與「12 」兩種寫法。
QUESTION_NUMBER_RE = re.compile(r"^\s*(\d{1,2})\s*(?:\.|(?=\s))")
# 一列的兩個儲存格常被合併成同一個 block，例如 "C \n12. \n題幹"；
# 部分頁面的答案欄改用全形字母（Ａ～Ｄ），需一併接受並正規化。
ANSWER_LETTERS = {"A": "A", "B": "B", "C": "C", "D": "D",
                  "\uff21": "A", "\uff22": "B", "\uff23": "C", "\uff24": "D"}
# 字母與題號之間可能是換行，也可能只隔一個空白（如 "Ｂ 40 請參考附圖"）。
ROW_RE = re.compile(r"^([A-D\uff21-\uff24])\s+(\d{1,2})\s*(?:\.|(?=\s))")


def load_questions(source_id: str) -> list[dict]:
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    picked = [q for q in questions if q["sourceId"] == source_id]
    picked.sort(key=lambda q: q["officialQuestionNumber"])
    if not picked:
        raise SystemExit(f"no questions for sourceId {source_id}")
    return picked


def open_pdf(source_id: str) -> pymupdf.Document:
    path = PDF_DIR / f"{source_id}.pdf"
    if not path.exists():
        raise SystemExit(
            f"missing {path}. Download the official PDFs first; they are not "
            "committed to this repository."
        )
    return pymupdf.open(path)


def extract_answer_key(doc: pymupdf.Document) -> dict[int, str]:
    """Pair each left-column answer letter with the question row it sits on.

    The papers start a question row with the answer cell, so PyMuPDF usually
    emits ``"C \n12. \n<stem>"`` as one block. Rows whose two cells land in
    separate blocks are recovered by matching left-column letters against
    question numbers at the same vertical position.
    """
    answers: dict[int, str] = {}
    for page in doc:
        cutoff = page.rect.width * ANSWER_COLUMN_RATIO
        letters: list[tuple[float, str]] = []
        numbers: list[tuple[float, int]] = []
        for x0, y0, _x1, _y1, text, *_ in page.get_text("blocks"):
            body = text.strip()
            if not body:
                continue
            joined = ROW_RE.match(body)
            if joined:
                answers[int(joined.group(2))] = ANSWER_LETTERS[joined.group(1)]
                continue
            if x0 < cutoff:
                for line in body.splitlines():
                    token = line.strip()
                    if token in ANSWER_LETTERS:
                        letters.append((y0, ANSWER_LETTERS[token]))
                continue
            match = QUESTION_NUMBER_RE.match(body)
            if match:
                numbers.append((y0, int(match.group(1))))
        # 同一列的答案與題號 y 座標幾乎相同，各自排序後依序對位最穩定。
        letters.sort()
        numbers.sort()
        for (_, number), (_, letter) in zip(numbers, letters):
            answers.setdefault(number, letter)
    return answers


def print_pages(doc: pymupdf.Document, pages: list[int]) -> None:
    for number in pages:
        print(f"\n{'=' * 70}\nPDF PAGE {number} / {doc.page_count}\n{'=' * 70}")
        print(doc[number - 1].get_text())


def print_batch(questions: list[dict], start: int, end: int, answers: dict[int, str]) -> None:
    for question in questions:
        number = question["officialQuestionNumber"]
        if not start <= number <= end:
            continue
        print(f"\n{'#' * 70}\n# Q{number}  {question['id']}\n{'#' * 70}")
        official = question["officialAnswer"]
        extracted = answers.get(number)
        flag = "" if extracted in (None, *official) else "   <<< MISMATCH"
        print(f"bank answer: {official}  pdf answer: {extracted}{flag}")
        print(f"source page: {question.get('sourcePage')}  scoring: {question['scoring']}")
        if question.get("figures"):
            print(f"figures: {json.dumps(question['figures'], ensure_ascii=False)}")
        if question.get("passage"):
            print(f"passage: {question['passage']}")
        print(f"\n[prompt]\n{question['prompt']}")
        for option in question["options"]:
            print(f"  ({option['label']}) {option['text']}")
        print(f"\n[explanationStatus] {question.get('explanationStatus')}")
        print(json.dumps(question.get("explanation"), ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_id")
    parser.add_argument("start", nargs="?", type=int)
    parser.add_argument("end", nargs="?", type=int)
    parser.add_argument("--answers", action="store_true", help="print the extracted answer key only")
    parser.add_argument("--pages", help="also dump these PDF pages, e.g. 7-9 or 7,9")
    parser.add_argument("--render", help="render these PDF pages to PNG, e.g. 7,8")
    parser.add_argument("--out", default="tmp/render", help="directory for --render output")
    args = parser.parse_args()

    questions = load_questions(args.source_id)
    doc = open_pdf(args.source_id)
    answers = extract_answer_key(doc)

    if args.answers:
        print(f"{args.source_id}: {doc.page_count} pages")
        mismatches = 0
        for question in questions:
            number = question["officialQuestionNumber"]
            extracted = answers.get(number)
            official = question["officialAnswer"]
            if extracted not in (*official,):
                mismatches += 1
                print(f"  Q{number}: bank {official} vs pdf {extracted}  <<< MISMATCH")
        print(f"extracted {len(answers)} answers, {mismatches} mismatch(es)")
        return

    if args.render:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        for number in parse_pages(args.render):
            pixmap = doc[number - 1].get_pixmap(dpi=170)
            target = out / f"{args.source_id}-p{number:02d}.png"
            pixmap.save(target)
            print(f"rendered {target}")
        return

    if args.pages:
        print_pages(doc, parse_pages(args.pages))

    if args.start is None or args.end is None:
        return
    print_batch(questions, args.start, args.end, answers)


def parse_pages(spec: str) -> list[int]:
    pages: list[int] = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if "-" in chunk:
            first, last = chunk.split("-", 1)
            pages.extend(range(int(first), int(last) + 1))
        else:
            pages.append(int(chunk))
    return pages


if __name__ == "__main__":
    main()
