# get-work · Stetson's outreach toolkit

A working directory for prospecting freelance / retainer / subcontract automation work.

The original HTML/CSS style was adapted from the tw93/Kami design system. The full Kami clone is archived at `/home/exedev/archive/kami` so it does not pollute normal searches or agent context.

## What lives where

```
get-work/
├── docs/
│   └── design-source.md           ← note on the archived Kami source
├── outreach/
│   ├── base/
│   │   ├── portfolio-base.html                    ← canonical 2-page portfolio
│   │   ├── holiday-lighting-prospect-base.html    ← holiday lighting campaign template
│   │   ├── portfolio-base.pdf                     ← built output (preview/share)
│   │   └── assets/
│   │       └── headshot.jpg
│   └── prospects/
│       └── <slug>/                ← one folder per company you're pitching
│           ├── portfolio.html
│           ├── portfolio.pdf
│           └── notes.md
└── scripts/
    ├── build.sh                   ← HTML → PDF
    ├── preview.sh                 ← local server for browser preview
    ├── new-prospect.sh            ← scaffold a standard tailored variant
    └── new-holiday-prospect.sh    ← scaffold a holiday lighting prospect sheet
```

## Daily workflow

### Preview the base doc in a browser

```bash
./scripts/preview.sh
# then open http://localhost:8765/base/portfolio-base.html
```

Edit `outreach/base/portfolio-base.html`, refresh browser, repeat. No build required for HTML preview.

### Build a PDF

```bash
./scripts/build.sh                                          # builds the base
./scripts/build.sh outreach/prospects/local-nerds/portfolio.html
```

### Start a new standard prospect

```bash
./scripts/new-prospect.sh local-nerds "Local Nerds"
```

This creates `outreach/prospects/local-nerds/` with a copy of the standard base, a symlinked headshot, and a `notes.md` scratch file.

### Start a new holiday lighting prospect

```bash
./scripts/new-holiday-prospect.sh coloradochristmaslights "Colorado Christmas Lights" "https://www.coloradochristmaslights.com/"
```

This creates `outreach/prospects/coloradochristmaslights/` using the holiday lighting prospect sheet template. The campaign plan, video outlines, email copy, and current handoff live in:

```text
docs/holiday-lighting-campaign.md
docs/holiday-lighting-handoff.md
```

After scaffolding:

1. Add the four demo video URLs once recorded.
2. Remove the `disabled` class from video buttons.
3. Preview: `./scripts/preview.sh`
4. Build PDF if wanted: `./scripts/build.sh outreach/prospects/coloradochristmaslights/portfolio.html`

For the current three-company campaign, resume from `docs/holiday-lighting-handoff.md`.

## Dependencies

- `weasyprint` — `brew install weasyprint`
- `poppler` (provides `pdfinfo` / `pdftoppm`) — `brew install poppler`
- Python 3 (for `preview.sh` local server)
