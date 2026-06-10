#!/usr/bin/env python3
"""Generate outreach/summary.html — prospect pipeline tracking table.

Source of truth is each prospect's notes.md:
  # Company Name                      ← display name (first H1)
  **Status:** drafting|ready|sent|replied|dead
  **Website:** https://...
  - Contact person: ...
  - Contact email: ...
  - Email drafted: YYYY-MM-DD         ← auto-fallback: email-draft.md mtime
  - Email sent: YYYY-MM-DD            ← fill in manually when you send

The "Email sent" line lives under "## Send log" (or anywhere in notes.md).
Run after any change:  ./scripts/generate-summary.py   (or `getwork summary`)
"""
from __future__ import annotations

import datetime as dt
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROSPECTS = ROOT / "outreach" / "prospects"
OUT = ROOT / "outreach" / "summary.html"

FIELD_RES = {
    "status": re.compile(r"\*\*Status:\*\*[ \t]*(.+)", re.I),
    "website": re.compile(r"\*\*Website:\*\*[ \t]*(\S+)", re.I),
    "contact_person": re.compile(r"Contact person:[ \t]*(.+)", re.I),
    "contact_email": re.compile(r"Contact email:[ \t]*(\S+)", re.I),
    "location": re.compile(r"Location / service area:[ \t]*(.+)", re.I),
    "drafted": re.compile(r"Email drafted:[ \t]*(\S+)", re.I),
    "sent": re.compile(r"Email sent:[ \t]*(\S+)", re.I),
}
H1_RE = re.compile(r"^#\s+(.+)$", re.M)

STATUS_ORDER = {"replied": 0, "sent": 1, "ready": 2, "drafting": 3, "dead": 9}


def parse_prospect(folder: Path) -> dict:
    slug = folder.name
    notes = folder / "notes.md"
    row = {
        "slug": slug,
        "name": slug,
        "status": "",
        "website": "",
        "location": "",
        "contact_person": "",
        "contact_email": "",
        "drafted": "",
        "sent": "",
        "portfolio": (folder / "portfolio.html").exists(),
    }
    if notes.exists():
        text = notes.read_text(encoding="utf-8", errors="ignore")
        m = H1_RE.search(text)
        if m:
            row["name"] = m.group(1).strip()
        for key, regex in FIELD_RES.items():
            m = regex.search(text)
            if m:
                val = m.group(1).strip().rstrip("\\").strip()
                if val and val not in ("-", "—", "n/a", "N/A"):
                    row[key] = val
    draft = folder / "email-draft.md"
    if not row["drafted"] and draft.exists():
        row["drafted"] = dt.date.fromtimestamp(draft.stat().st_mtime).isoformat()
    # derive status if missing
    if not row["status"]:
        row["status"] = "sent" if row["sent"] else ("ready" if row["drafted"] else "drafting")
    if row["sent"] and row["status"] in ("drafting", "ready"):
        row["status"] = "sent"
    return row


def badge(status: str) -> str:
    s = html.escape(status.lower().split()[0] if status else "")
    return f'<span class="badge badge-{s}">{html.escape(status)}</span>'


def main() -> None:
    rows = sorted(
        (parse_prospect(p) for p in sorted(PROSPECTS.iterdir()) if p.is_dir()),
        key=lambda r: (STATUS_ORDER.get(r["status"].lower().split()[0] if r["status"] else "", 5), r["name"].lower()),
    )

    trs = []
    for r in rows:
        name_cell = html.escape(r["name"])
        if r["portfolio"]:
            name_cell = f'<a href="/prospects/{html.escape(r["slug"])}/portfolio.html">{name_cell}</a>'
        site = f'<a href="{html.escape(r["website"])}" target="_blank">site</a>' if r["website"] else ""
        email = f'<a href="mailto:{html.escape(r["contact_email"])}">{html.escape(r["contact_email"])}</a>' if r["contact_email"] else ""
        trs.append(f"""      <tr>
        <td>{name_cell}</td>
        <td>{badge(r['status'])}</td>
        <td>{html.escape(r['location'])}</td>
        <td>{html.escape(r['contact_person'])}</td>
        <td>{email}</td>
        <td>{html.escape(r['drafted'])}</td>
        <td>{html.escape(r['sent']) or '—'}</td>
        <td>{site}</td>
        <td class="slug">{html.escape(r['slug'])}</td>
      </tr>""")

    counts: dict[str, int] = {}
    for r in rows:
        key = r["status"].lower().split()[0] if r["status"] else "unknown"
        counts[key] = counts.get(key, 0) + 1
    stats = " · ".join(f"{v} {k}" for k, v in sorted(counts.items()))
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")

    OUT.write_text(f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Prospect Summary</title>
  <style>
    :root {{ color-scheme: light; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
           margin: 2rem auto; max-width: 1200px; padding: 0 1rem; color: #1a1a1a; }}
    h1 {{ font-size: 1.5rem; margin-bottom: .25rem; }}
    .meta {{ color: #777; font-size: .85rem; margin-bottom: 1.25rem; }}
    table {{ border-collapse: collapse; width: 100%; font-size: .9rem; }}
    th, td {{ text-align: left; padding: .5rem .65rem; border-bottom: 1px solid #e5e5e5; vertical-align: top; }}
    th {{ font-size: .75rem; text-transform: uppercase; letter-spacing: .04em; color: #888;
         border-bottom: 2px solid #ccc; position: sticky; top: 0; background: #fff; }}
    tr:hover td {{ background: #fafafa; }}
    a {{ color: #0a6cff; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .slug {{ color: #aaa; font-family: ui-monospace, monospace; font-size: .8rem; }}
    .badge {{ display: inline-block; padding: .1rem .5rem; border-radius: 999px;
             font-size: .75rem; font-weight: 600; background: #eee; color: #555; }}
    .badge-drafting {{ background: #fff3cd; color: #8a6d1a; }}
    .badge-ready    {{ background: #cfe2ff; color: #1c4f9c; }}
    .badge-sent     {{ background: #d1e7dd; color: #14613f; }}
    .badge-replied  {{ background: #198754; color: #fff; }}
    .badge-dead     {{ background: #f1f1f1; color: #999; text-decoration: line-through; }}
    .hint {{ margin-top: 1.5rem; color: #999; font-size: .8rem; }}
    code {{ background: #f4f4f4; padding: .1rem .3rem; border-radius: 4px; }}
  </style>
</head>
<body>
  <h1>Prospect Summary</h1>
  <p class="meta">{len(rows)} prospects · {stats} · generated {now} · <a href="/">← directory</a></p>
  <table>
    <thead>
      <tr>
        <th>Company</th><th>Status</th><th>Location</th><th>Contact</th><th>Email</th>
        <th>Drafted</th><th>Sent</th><th>Site</th><th>Slug</th>
      </tr>
    </thead>
    <tbody>
{chr(10).join(trs)}
    </tbody>
  </table>
  <p class="hint">To mark an email as sent: edit <code>outreach/prospects/&lt;slug&gt;/notes.md</code>,
  set <code>Email sent: YYYY-MM-DD</code> in the Send log (and optionally <code>**Status:** sent</code>),
  then run <code>getwork summary</code>.</p>
</body>
</html>
""", encoding="utf-8")
    print(f"✓ Wrote {OUT.relative_to(ROOT)} ({len(rows)} prospects)")


if __name__ == "__main__":
    raise SystemExit(main())
