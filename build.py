#!/usr/bin/env python3
"""Build script for the Free Holiday Letter & Invitation Pack.

Renders every HTML sheet in sources/ to an unbranded, print-ready PDF
in printables/ using WeasyPrint. Fully offline; no signups, no keys.

Usage:
    python3 build.py                 # build all sheets
    python3 build.py --only sheet    # build a single sheet by stem name
    python3 build.py --list          # list sheets without building
    python3 build.py --clean         # delete printables/*.pdf after building
    python3 build.py --out DIR       # write PDFs to DIR instead of printables/
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

try:
    from pypdf import PdfReader
except ModuleNotFoundError:  # pragma: no cover
    PdfReader = None

try:
    from weasyprint import HTML
except ModuleNotFoundError as exc:  # pragma: no cover
    sys.stderr.write(
        "WeasyPrint is required: pip install weasyprint\n"
        f"(import error: {exc})\n"
    )
    raise SystemExit(1)

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "sources"


def sheet_paths(only: str | None) -> list[Path]:
    paths = sorted(SOURCES.glob("*.html"))
    if only:
        matches = [p for p in paths if p.stem == only]
        if not matches:
            available = ", ".join(p.stem for p in paths)
            raise SystemExit(f"No sheet named {only!r}. Available: {available}")
        paths = matches
    if not paths:
        raise SystemExit(f"No HTML sheets found in {SOURCES}")
    return paths


def render_sheet(src: Path, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_pdf = out_dir / f"{src.stem}.pdf"
    started = time.perf_counter()
    html = HTML(filename=str(src))
    html.write_pdf(target=str(out_pdf))
    elapsed = time.perf_counter() - started

    pages = 0
    if PdfReader is not None:
        pages = len(PdfReader(str(out_pdf)).pages)
    size_kb = out_pdf.stat().st_size / 1024
    return {"path": out_pdf, "pages": pages, "kb": size_kb, "secs": elapsed}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--only", help="build one sheet by stem (e.g. party-invite)")
    parser.add_argument("--list", action="store_true", help="list sheets and exit")
    parser.add_argument("--clean", action="store_true", help="remove PDFs when done")
    parser.add_argument("--out", default=None, help="output directory (default: printables/)")
    args = parser.parse_args()

    paths = sheet_paths(args.only)
    if args.list:
        for p in paths:
            print(p.stem)
        return 0

    out_dir = Path(args.out) if args.out else ROOT / "printables"

    print(f"Building {len(paths)} sheet(s) -> {out_dir}\n")
    results = []
    for src in paths:
        try:
            result = render_sheet(src, out_dir)
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL {src.stem}: {exc}")
            return 1
        results.append(result)
        print(
            f"  ok  {result['path'].name:<38}"
            f" {result['pages']} page(s)  {result['kb']:7.1f} KB  {result['secs']:.2f}s"
        )

    if args.clean:
        removed = 0
        for r in results:
            if r["path"].exists():
                r["path"].unlink()
                removed += 1
        print(f"\n--clean: removed {removed} PDF(s)")

    print(f"\nDone: {len(results)} PDF(s). Print at 100% scale ('Actual size')"
          " on US Letter paper.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
