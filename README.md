# get-work · an agent-driven outreach pipeline

Prospecting toolkit for selling custom software to holiday-lighting installers.
Point it at a metro and it researches the market, finds real local operators,
builds each one a personalized pitch page on its own subdomain, and drafts the
outreach email — leaving a tracking dashboard of the whole pipeline.

```
"find holiday lighting companies in Tulsa and build their prospect folders"
        │
        ▼
┌─ 1. MARKET SCAN ──────────────────────────────────────────────┐
│  getwork market-scan "Tulsa, OK"                              │
│  Google (Serper API) × 3 query variants → dedupe by domain →  │
│  filter ~50 directory/lead-gen sites → fetch every homepage   │
│  to verify it's a real installer → data/scans/tulsa-ok.json   │
│  + market tracker (outreach/markets.html, 29 tiered metros)   │
└───────────────────────────────────────────────────────────────┘
        │  18 verified installers? hot market — go.
        ▼
┌─ 2. SCRAPE & BUILD ───────────────────────────────────────────┐
│  getwork build-prospect tulsalights "Tulsa Lights" <url>      │
│  Scrapes homepage + contact/about pages: owner emails (not    │
│  just info@), phones, contact forms, services, socials.       │
│  Scaffolds outreach/prospects/<slug>/ with notes.md research  │
│  pre-filled and raw scrape.json kept for reference.           │
└───────────────────────────────────────────────────────────────┘
        │
        ▼
┌─ 3. PERSONALIZED PITCH PAGE ──────────────────────────────────┐
│  Each prospect gets a tailored portfolio.html — their name,   │
│  their market, demo videos — served on its own subdomain:     │
│      https://<slug>.stetson.dev                               │
│  (serve.py routes subdomains → prospect folders; PDF builds   │
│  available via weasyprint for attachments.)                   │
└───────────────────────────────────────────────────────────────┘
        │
        ▼
┌─ 4. EMAIL ────────────────────────────────────────────────────┐
│  Drafted per-prospect from voice/positioning docs, then       │
│  getwork email <slug> --variant 1                             │
│  pushes it straight into Fastmail Drafts via JMAP — review,   │
│  personalize, hit send.                                       │
└───────────────────────────────────────────────────────────────┘
        │
        ▼
┌─ 5. TRACK ────────────────────────────────────────────────────┐
│  getwork summary → outreach/summary.html                      │
│  Pipeline table generated from every prospect's notes.md:     │
│  status (drafting→ready→sent→replied), contact, dates.        │
│  Never hand-edited; the notes are the source of truth.        │
└───────────────────────────────────────────────────────────────┘
```

Most of steps 1–4 are run by a coding agent following
[`docs/agent-prospecting.md`](docs/agent-prospecting.md); the human reviews
candidates, personalizes drafts, and presses send.

## The CLI

```bash
./getwork install        # puts `getwork` on PATH (~/.local/bin)

getwork market-scan "Tulsa, OK"            # validate a metro (3 searches, verified list)
getwork market-scan "Boise, ID" --from-urls data/inbox/boise-id.txt   # offline-search mode
getwork markets                            # regenerate the market tracker page
getwork scrape https://example.com --json  # one-off scrape of a company site
getwork build-prospect <slug> "Name" <url> --location "City, ST"
getwork summary                            # regenerate the pipeline dashboard
getwork email <slug> --variant 1           # draft into Fastmail
getwork live-preview start                 # BrowserSync preview (port 8765)
```

## Search resilience

Datacenter IPs get blocked by every search engine, so `market-scan` has a
fallback chain:

1. **Serper.dev Google API** — primary; key injected at the network edge by an
   exe.dev integration (no secret on the VM). ~2s/query.
2. **Brave Search HTML** scraping — works unauthenticated but ~1 query/min.
3. **DuckDuckGo HTML** — usually captcha'd, kept as a hail mary.
4. **Local-search handoff** — `data/inbox/<metro>.txt` files carry the queries;
   run them from any unblocked machine, paste the result URLs back in, and
   `--from-urls` does the filtering/verification server-side.

## Repo map

```
get-work/
├── getwork                     ← CLI entry point
├── serve.py                    ← <slug>.stetson.dev → prospect pitch pages
├── data/
│   ├── markets.json            ← 29 tiered target metros + scan results
│   ├── scans/<metro>.json      ← verified installer lists per metro
│   └── inbox/<metro>.txt       ← query/URL handoff files (search fallback)
├── docs/
│   ├── agent-prospecting.md    ← the agent playbook (start here)
│   ├── holiday-lighting-handoff.md  ← positioning, voice, campaign state
│   └── QUICK-START.md          ← Fastmail setup (5 min)
├── outreach/
│   ├── base/                   ← portfolio + email templates
│   ├── summary.html            ← generated pipeline dashboard
│   ├── markets.html            ← generated market tracker
│   └── prospects/<slug>/       ← portfolio.html · notes.md · email-draft.md · scrape.json
└── scripts/                    ← the machinery behind each getwork subcommand
```

## Dependencies

- Python 3 with `requests`, `beautifulsoup4`, `python-dotenv`
- `weasyprint` + `poppler` for PDF builds (optional)
- Fastmail account with JMAP API (for email drafts) — `cp .env.example .env` and
  see `docs/QUICK-START.md`

Portfolio styling adapted from the tw93/Kami design system (archived outside
the repo at `/home/exedev/archive/kami`).
