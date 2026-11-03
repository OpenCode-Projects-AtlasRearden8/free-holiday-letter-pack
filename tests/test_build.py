"""Tests for the Free Holiday Letter & Invitation Pack build.

Verifies that every printable sheet builds a valid, letter-size,
unbranded PDF. Run with:  python3 -m pytest
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources"
PRINTABLES = ROOT / "printables"

# Every sheet: stem -> expected number of PDF pages.
SHEETS = {
    "family-letter-classic": 1,
    "family-letter-modern": 1,
    "kid-drawing-corner": 1,
    "one-page-one-photo": 1,
    "party-invite": 1,
    "save-the-date": 1,
    "thank-you-card-mailer": 2,
}

BRAND_STRINGS = ("Asdale", "asdale dynamics")

LETTER_W_IN = 612 / 72  # 8.5in in PDF points
LETTER_H_IN = 792 / 72  # 11in


@pytest.fixture(scope="session", autouse=True)
def built_pdfs() -> None:
    """Build all sheets once; failures fail this fixture immediately."""
    result = subprocess.run(
        [sys.executable, "build.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0, f"build.py failed:\n{result.stdout}\n{result.stderr}"
    for stem in SHEETS:
        assert (PRINTABLES / f"{stem}.pdf").exists()


@pytest.mark.parametrize("stem", sorted(SHEETS))
def test_sheet_builds(stem: str) -> None:
    pdf_path = PRINTABLES / f"{stem}.pdf"
    source = SOURCES / f"{stem}.html"
    assert source.exists(), f"missing HTML source for {stem}"
    assert pdf_path.exists() and pdf_path.stat().st_size > 500


@pytest.mark.parametrize("stem", sorted(SHEETS))
def test_pdf_header_and_eof(stem: str) -> None:
    data = (PRINTABLES / f"{stem}.pdf").read_bytes()
    assert data.startswith(b"%PDF-"), "missing PDF magic bytes"
    assert b"%PDF" in data[:8]


@pytest.mark.parametrize("stem", sorted(SHEETS))
def test_pdf_page_count(stem: str) -> None:
    reader = PdfReader(PRINTABLES / f"{stem}.pdf")
    assert len(reader.pages) == SHEETS[stem], (
        f"{stem}: expected {SHEETS[stem]} page(s), got {len(reader.pages)}"
    )


@pytest.mark.parametrize("stem", sorted(SHEETS))
def test_pdf_letter_size(stem: str) -> None:
    reader = PdfReader(PRINTABLES / f"{stem}.pdf")
    for page in reader.pages:
        w = float(page.mediabox.width) / 72
        h = float(page.mediabox.height) / 72
        assert abs(w - LETTER_W_IN) < 0.05, f"{stem}: width {w}in is not letter"
        assert abs(h - LETTER_H_IN) < 0.05, f"{stem}: height {h}in is not letter"


@pytest.mark.parametrize("stem", sorted(SHEETS))
def test_pdf_has_content(stem: str) -> None:
    reader = PdfReader(PRINTABLES / f"{stem}.pdf")
    for page in reader.pages:
        text = page.extract_text() or ""
        assert len(text) > 20, f"{stem}: page has almost no extractable text"


def test_printables_only_contains_expected_pdfs() -> None:
    pdfs = sorted(p.stem for p in PRINTABLES.glob("*.pdf"))
    assert pdfs == sorted(SHEETS), f"unexpected or missing PDFs: {pdfs}"


def test_no_brand_strings_in_output_and_sources() -> None:
    """The printables are intentionally unbranded; branding lives in README/LICENSE only."""
    for pdf in PRINTABLES.glob("*.pdf"):
        raw = pdf.read_bytes()
        for brand in BRAND_STRINGS:
            assert brand not in raw.decode("latin-1", errors="ignore"), (
                f"{pdf.name} contains brand string {brand!r}"
            )
    for src in list(SOURCES.glob("*.html")) + list((ROOT / "assets").rglob("*.css")):
        text = src.read_text(encoding="utf-8", errors="ignore")
        for brand in BRAND_STRINGS:
            assert brand not in text, f"{src} contains brand string {brand!r}"


def test_build_only_single_sheet(tmp_path: Path) -> None:
    """--only rebuilds one sheet into a chosen directory."""
    out_dir = tmp_path / "single"
    result = subprocess.run(
        [sys.executable, "build.py", "--only", "save-the-date", "--out", str(out_dir)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    produced = list(out_dir.glob("*.pdf"))
    assert [p.name for p in produced] == ["save-the-date.pdf"]


def test_build_fails_loudly_on_bad_sheet(tmp_path: Path) -> None:
    """A source with broken markup should fail the build with a non-zero exit."""
    bad_src = SOURCES / "_does_not_exist.html"
    result = subprocess.run(
        [sys.executable, "build.py", "--only", "there-is-no-such-sheet"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode != 0
    assert bad_src.name not in result.stdout  # never written anywhere
