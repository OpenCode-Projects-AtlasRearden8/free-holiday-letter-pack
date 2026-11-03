# Free Holiday Letter & Invitation Pack

Free-forever, no-signup printables for the season: plain HTML/CSS sources that
build into clean, unbranded, print-ready PDFs. Built and tested
locally, no accounts, no tracking, no questions asked.

A friendly project by [Asdale Dynamics, LLC](https://dylanasdale.github.io) —
AI and everyday tools explained "like a friend would": plain English, step by
step, never condescending.

## What's in the pack

| Sheet | What it is | Pages |
|---|---|---|
| `family-letter-modern` | Modern family news letter: big photo spot, "this year in short" sidebar, contact block | 1 |
| `family-letter-classic` | Classic serif family letter: masthead, two-column story, closing blessing | 1 |
| `save-the-date` | Script-style save-the-date card, plus variants and how-to panel | 1 |
| `party-invite` | Holiday party invitation with details table, menu strip, tear-off RSVP slip | 1 |
| `thank-you-card-mailer` | Fold-in-half thank-you card with outside address/stamp panel + inside note page (print duplex) | 2 |
| `kid-drawing-corner` | Curated "gallery" page for a child's drawing, with artist/title/date labels | 1 |
| `one-page-one-photo` | The busy-parent minimal kit: one photo, three lines, sign off. Five minutes, no guilt | 1 |

Built PDFs live in `printables/` — unbranded, US Letter format, ready to print.

## Quick start

Requires Python 3.10+ with `weasyprint`, `pypdf`, and `pytest`:

```bash
pip install weasyprint pypdf pytest

python3 build.py          # build every sheet -> printables/
python3 build.py --list   # just list the sheets
python3 build.py --only party-invite   # build one sheet
python3 build.py --out /tmp/pdfs       # build somewhere else
python3 -m pytest         # verify every sheet builds a valid PDF
```

## Editing a sheet

1. Open any file in `sources/` — names, dates and text are readable placeholders.
2. Change the words. For photos, either:
   - print the sheet and tape/paste a physical photo into the dashed box, or
   - rebuild the PDF with your own image:

   ```html
   <div class="ph photo" style="border-style: solid; border: none;">
     <img src="../assets/my-photo.jpg" alt="">
   </div>
   ```

3. Rebuild: `python3 build.py --only <sheet-name>`.

Fonts: generic stacks with web-safe fallbacks (Georgia, Arial, cursive).
Nice-to-have local fonts such as Libre Baskerville, Playfair Display, Great
Vibes, and Patrick Hand are picked up automatically if installed; the sheets
still print fine without them. No webfont downloads, the whole pack is offline.

## Printing tips

- Print at **100% scale** ("Actual size", not "Fit to page") on US Letter paper.
- Heavier paper (28–32 lb / cardstock) makes cards and save-the-dates feel real.
- `thank-you-card-mailer` is 2 pages: print **double-sided, long-edge flip**,
  then fold page 1 on the dashed line so the inside note lands inside the card.
- `family-letter-*` pages are designed for color, but degrade gracefully to
  grayscale — details turn to darker ink, photos stay photos.

## Project layout

```
build.py             one build script: sources/*.html -> printables/*.pdf
sources/             the HTML/CSS sheets (edit these)
assets/css/print.css shared print styles
printables/          built PDFs (unbranded, safe to share)
tests/               pytest suite verifying each sheet is a valid PDF
```

## Privacy & cost

No signups, no analytics, no personal data in any file (example names like
"The Henderson Family" are placeholders — replace them with your own, locally).
Free forever.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.
