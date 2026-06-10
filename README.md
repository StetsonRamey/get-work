# get-work · Stetson's outreach toolkit

A working directory for prospecting freelance / retainer / subcontract automation work.

The original HTML/CSS style was adapted from the tw93/Kami design system. The full Kami clone is archived at `/home/exedev/archive/kami` so it does not pollute normal searches or agent context.

## What lives where

```
get-work/
├── docs/
│   ├── design-source.md           ← note on the archived Kami source
│   ├── fastmail-setup.md          ← Fastmail email integration guide
│   └── QUICK-START.md             ← 5-minute email setup
├── outreach/
│   ├── base/
│   │   ├── portfolio-base.html                    ← canonical 2-page portfolio
│   │   ├── holiday-lighting-prospect-base.html    ← holiday lighting campaign template
│   │   ├── email-template.md                      ← email template starting point
│   │   ├── portfolio-base.pdf                     ← built output (preview/share)
│   │   └── assets/
│   │       └── headshot.jpg
│   └── prospects/
│       └── <slug>/                ← one folder per company you're pitching
│           ├── portfolio.html
│           ├── portfolio.pdf
│           ├── email.md                           ← email template (new!)
│           └── notes.md
├── .env.example                   ← Fastmail API config template
└── scripts/
    ├── build.sh                   ← HTML → PDF
    ├── preview.sh                 ← local server for browser preview
    ├── new-prospect.sh            ← scaffold a standard tailored variant
    ├── new-holiday-prospect.sh    ← scaffold a holiday lighting prospect sheet
    └── create-email-draft.py      ← create drafts in Fastmail (new!)
```

## Quick Start

**New:** Automatically create draft emails in Fastmail! See `docs/QUICK-START.md` for setup (5 minutes).

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

### Install the CLI helper

From the repo, run once:

```bash
./getwork install
```

That installs `getwork` and `get-work` shims into `~/.local/bin` so you can run commands from an SSH session without remembering script paths:

```bash
getwork -h
getwork email holiglows --variant 1 --dry-run
getwork new-holiday-prospect holiglows "HoliGlows" "https://www.holiglows.com/"
getwork live-preview --port 8765
```

Preview commands print the exe.dev proxy URL to open from your laptop, e.g. `https://get-work.exe.xyz:8765/`. The `localhost` URL is only useful inside the VM.

### Create drafts in Fastmail

```bash
# Set up Fastmail integration (one time)
cp .env.example .env
# Edit .env with your Fastmail API token (see docs/QUICK-START.md)

# Create draft emails from templates
getwork email holiglows --variant 1          # Variant 1
getwork email holiglows --variant 2          # Variant 2
getwork email holiglows --all --dry-run      # Preview both
```

Templates use variables like `{PROSPECT_NAME}` and `{CONTACT_NAME}` that are auto-populated from your `notes.md`. See `docs/QUICK-START.md` for the full 5-minute setup.

## Dependencies

### For portfolio HTML/PDF
- `weasyprint` — `brew install weasyprint`
- `poppler` (provides `pdfinfo` / `pdftoppm`) — `brew install poppler`
- Python 3 (for `preview.sh` local server)

### For Fastmail email drafts
- `requests` — `pip3 install requests`
- `python-dotenv` — `pip3 install python-dotenv`
- Fastmail account with JMAP API access (free tier)
