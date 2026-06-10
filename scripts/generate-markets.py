#!/usr/bin/env python3
"""Generate outreach/markets.html — market targeting tracker.

Source of truth: data/markets.json (edit tiers/notes there) plus scan results
written by scripts/market-scan.py and prospect folders (counted by matching
the `Location / service area:` line in each notes.md against the metro name).
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKETS = ROOT / "data" / "markets.json"
PROSPECTS = ROOT / "outreach" / "prospects"
OUT = ROOT / "outreach" / "markets.html"

TIER_LABELS = {0: "home — do not prospect", 1: "tier 1", 2: "tier 2", 3: "tier 3"}


def prospect_locations() -> list[str]:
    locs = []
    if PROSPECTS.exists():
        for notes in PROSPECTS.glob("*/notes.md"):
            m = re.search(r"Location / service area:[ \t]*(.+)", notes.read_text(errors="ignore"))
            if m:
                locs.append(m.group(1).strip().lower())
    return locs


def main() -> None:
    data = json.loads(MARKETS.read_text())
    markets = data.get("markets", [])
    locs = prospect_locations()

    def prospect_count(metro: str) -> int:
        key = metro.lower().split("-")[0].split()[0]
        full = metro.lower()
        return sum(1 for l in locs if full in l or key in l)

    markets.sort(key=lambda m: (m.get("tier", 9) if m.get("tier", 9) > 0 else 99, m["metro"]))

    trs = []
    for m in markets:
        tier = m.get("tier", "")
        count = m.get("installer_count")
        scanned = m.get("last_scan", "")
        built = prospect_count(m["metro"])
        scan_file = m.get("scan_file", "")
        scan_cell = html.escape(scanned) if scanned else "—"
        if scan_file:
            scan_cell = f'{scan_cell} <span class="file">({html.escape(scan_file)})</span>'
        trs.append(f"""      <tr class="tier-{tier}">
        <td>{html.escape(m['metro'])}, {html.escape(m.get('state',''))}</td>
        <td><span class="badge tier-badge-{tier}">{html.escape(TIER_LABELS.get(tier, str(tier)))}</span></td>
        <td class="num">{count if count is not None else '—'}</td>
        <td class="num">{built or '—'}</td>
        <td>{scan_cell}</td>
        <td class="notes">{html.escape(m.get('notes',''))}</td>
      </tr>""")

    scanned_n = sum(1 for m in markets if m.get("last_scan"))
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")

    OUT.write_text(f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Market Tracker</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
           margin: 2rem auto; max-width: 1100px; padding: 0 1rem; color: #1a1a1a; }}
    h1 {{ font-size: 1.5rem; margin-bottom: .25rem; }}
    .meta {{ color: #777; font-size: .85rem; margin-bottom: 1.25rem; }}
    table {{ border-collapse: collapse; width: 100%; font-size: .9rem; }}
    th, td {{ text-align: left; padding: .5rem .65rem; border-bottom: 1px solid #e5e5e5; vertical-align: top; }}
    th {{ font-size: .75rem; text-transform: uppercase; letter-spacing: .04em; color: #888;
         border-bottom: 2px solid #ccc; position: sticky; top: 0; background: #fff; }}
    tr:hover td {{ background: #fafafa; }}
    .num {{ text-align: right; font-variant-numeric: tabular-nums; }}
    .notes {{ color: #666; font-size: .85rem; max-width: 28rem; }}
    .file {{ color: #aaa; font-family: ui-monospace, monospace; font-size: .75rem; }}
    .badge {{ display: inline-block; padding: .1rem .5rem; border-radius: 999px;
             font-size: .75rem; font-weight: 600; background: #eee; color: #555; white-space: nowrap; }}
    .tier-badge-1 {{ background: #d1e7dd; color: #14613f; }}
    .tier-badge-2 {{ background: #cfe2ff; color: #1c4f9c; }}
    .tier-badge-3 {{ background: #fff3cd; color: #8a6d1a; }}
    .tier-badge-0 {{ background: #f8d7da; color: #842029; }}
    tr.tier-0 td {{ opacity: .65; }}
    a {{ color: #0a6cff; text-decoration: none; }}
    .hint {{ margin-top: 1.5rem; color: #999; font-size: .8rem; }}
    code {{ background: #f4f4f4; padding: .1rem .3rem; border-radius: 4px; }}
  </style>
</head>
<body>
  <h1>Market Tracker</h1>
  <p class="meta">{len(markets)} markets · {scanned_n} scanned · generated {now} ·
    <a href="/summary.html">prospect summary</a> · <a href="/">← directory</a></p>
  <table>
    <thead>
      <tr>
        <th>Metro</th><th>Tier</th><th>Verified installers</th><th>Prospects built</th>
        <th>Last scan</th><th>Notes</th>
      </tr>
    </thead>
    <tbody>
{chr(10).join(trs)}
    </tbody>
  </table>
  <p class="hint">Scan a market: <code>getwork market-scan "Tulsa, OK"</code> ·
  Edit tiers/notes in <code>data/markets.json</code> · Regenerate: <code>getwork markets</code>.
  "Verified installers" = domains whose homepage mentions holiday/christmas lighting.</p>
</body>
</html>
""", encoding="utf-8")
    print(f"✓ Wrote {OUT.relative_to(ROOT)} ({len(markets)} markets)")


if __name__ == "__main__":
    raise SystemExit(main())
