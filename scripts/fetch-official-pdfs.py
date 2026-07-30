"""Download the official AIAP exam PDFs a batch needs into ``IPAS_PDF_DIR``.

The PDFs are official documents and are not committed to this repository; only
the questions extracted from them are. This script fetches exactly the files
listed in ``scripts/import-official-exam.py`` for one batch, so the import step
never has to be pointed at hand-placed downloads.

Both official hosts are frequently unreachable from restricted networks. This
script reports the failing host and exits non-zero rather than falling back to
any third-party mirror: a third-party copy cannot be cited as official under
``docs/SOURCE_AND_COVERAGE_RULES.md``.

Usage::

    python scripts/fetch-official-pdfs.py 115-1-intermediate
    IPAS_PDF_DIR=/somewhere/else python scripts/fetch-official-pdfs.py 115-1
"""

from __future__ import annotations

import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from importlib import import_module

_importer = import_module("import-official-exam")
BATCHES = _importer.BATCHES
PDF_DIR = _importer.PDF_DIR

# 官方檔名含中文，需先做 percent-encoding 才能送出請求。
def encode_url(url: str) -> str:
    parts = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit(
        (
            parts.scheme,
            parts.netloc,
            urllib.parse.quote(parts.path, safe="/%"),
            urllib.parse.quote(parts.query, safe="=&%"),
            parts.fragment,
        )
    )


def fetch(url: str, target: Path) -> None:
    request = urllib.request.Request(
        encode_url(url),
        headers={"User-Agent": "iPas-quiz importer (official PDF fetch)"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        payload = response.read()
    if not payload.startswith(b"%PDF"):
        raise ValueError(
            f"{url} did not return a PDF (first bytes: {payload[:16]!r}). "
            "Check whether the official page moved the file."
        )
    target.write_bytes(payload)


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in BATCHES:
        raise SystemExit(f"usage: {sys.argv[0]} [{'|'.join(BATCHES)}]")
    batch = BATCHES[sys.argv[1]]
    PDF_DIR.mkdir(parents=True, exist_ok=True)

    failures = []
    for paper in batch["papers"]:
        target = Path(paper["path"])
        if target.exists():
            print(f"exists  {target.name}  ({paper['sourceId']})")
            continue
        try:
            fetch(paper["url"], target)
        except (urllib.error.URLError, OSError, ValueError) as error:
            host = urllib.parse.urlsplit(paper["url"]).netloc
            failures.append((paper["sourceId"], host, error))
            print(f"FAILED  {target.name}  ({paper['sourceId']}): {error}")
            continue
        print(f"fetched {target.name}  {target.stat().st_size} bytes")

    if failures:
        hosts = sorted({host for _, host, _ in failures})
        raise SystemExit(
            f"\n{len(failures)} official PDF(s) could not be downloaded from "
            f"{', '.join(hosts)}.\nIf the network blocks these hosts, allow them "
            "for this environment instead of substituting a third-party copy."
        )
    print(f"\nAll PDFs for this batch are in {PDF_DIR}")


if __name__ == "__main__":
    main()
