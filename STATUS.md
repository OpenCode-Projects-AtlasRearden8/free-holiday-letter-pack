# STATUS.md

Project: **Free Holiday Letter & Invitation Pack**
Folder: `/workspace/opencode-lab/free-holiday-letter-pack`
Status: **complete, built, tested** (as of Nov 3, 2026)

## What was built

A plain HTML/CSS → PDF printables pack with one build script. Seven sheets,
all US Letter, all unbranded (no logos, no brand strings, no tracking):

1. `family-letter-modern` — modern family news letter with photo spot and "this
   year in short" sidebar.
2. `family-letter-classic` — classic serif letter: masthead, two columns, blessing.
3. `save-the-date` — script-style card plus occasion-variant and how-to panels.
4. `party-invite` — party invitation: details table, menu strip, tear-off RSVP slip.
5. `thank-you-card-mailer` — fold-in-half thank-you card (outside address + stamp
   panel on page 1, inside note page 2; duplex print).
6. `kid-drawing-corner` — "gallery" page for a child's drawing with labels.
7. `one-page-one-photo` — busy-parent minimal kit: one photo, three lines, sign off.

## How to run it

```bash
pip install weasyprint pypdf pytest

python3 build.py        # build all sheets -> printables/
python3 build.py --only party-invite
python3 build.py --list
python3 -m pytest       # run the verification suite
```

## Verification results

- `python3 build.py` → 7/7 sheets build; `printables/` holds 7 unbranded PDFs.
- `python3 -m pytest` → **39 passed** in ~6s. Coverage:
  - every sheet builds a PDF from an existing HTML source;
  - PDF magic bytes, per-sheet page counts, and US Letter MediaBox (8.5×11in);
  - extractable text present on every page;
  - `printables/` contains exactly the seven expected PDFs;
  - no brand strings in any PDF or in `sources/`/`assets/` (readme/license only);
  - `build.py --only <sheet> --out <dir>` works in a temp dir;
  - unknown sheet names fail loudly with a non-zero exit.
- Visual check: all seven sheets rendered to PNG and inspected; layouts verified
  (modern letter, classic letter, save-the-date card, party invite, both
  thank-you card pages, drawing corner, one-page kit).

## Fix history

- WeasyPrint crashed on `float: left` inside `::first-letter` (classic letter
  drop cap) — replaced with a non-floating enlarged letter.
- Thank-you mailer page 1 flex columns over-constrained and squeezed — rebuilt
  the halves as a stacked top/bottom fold layout.
- One-page kit checklist collapsed in flex — list items now `display: inline`.

## Files

```
build.py  build script (weasyprint; pypdf for verification)
sources/  7 editable HTML sheets      assets/css/print.css  shared styles
printables/  7 built PDFs             tests/test_build.py   pytest suite
LICENSE  MIT, Copyright (c) 2026 Asdale Dynamics, LLC
README.md  usage + printing tips, credits Asdale Dynamics, LLC
```

## Known gaps

- Photos are tape-able placeholder boxes; embedding real images requires
  dropping `<img>` into the source (documented in README, tested manually as
  markup pattern only).
- Tests render at build speed; they check structure, not pixel-perfection —
  fine-tuned visual tweaks still deserve a human eye after edits.
- PDFs embed locally installed fonts when present (Libre Baskerville, Great
  Vibes, Patrick Hand…); without them the CSS stacks fall back to Georgia/
  Arial/cursive and shapes shift slightly.
- No A4 variant (US Letter only, prints as "Actual size").
- No printed slide-in photo DPI guidance beyond the on-sheet hints.
