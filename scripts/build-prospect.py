#!/usr/bin/env python3
"""Build a complete prospect folder from a company website in one shot.

Usage:
  ./scripts/build-prospect.py tulsalights "Tulsa Holiday Lights" https://tulsaholidaylights.com/
  ./scripts/build-prospect.py tulsalights "Tulsa Holiday Lights" https://... --location "Tulsa, OK"

Does:
  1. Scrapes the website (scrape-prospect.py) for emails/phones/names/etc.
  2. Scaffolds outreach/prospects/<slug>/ (new-holiday-prospect.sh)
  3. Fills notes.md research + contact sections with scraped data
  4. Saves raw scrape data to scrape.json in the prospect folder
  5. Regenerates the summary table + preview index

Idempotent-ish: refuses to overwrite an existing prospect unless --force.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
PROSPECTS = ROOT / "outreach" / "prospects"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True)


def pick_email(emails: dict[str, str], website: str) -> str:
    """Prefer mailto links and addresses on the company's own domain."""
    if not emails:
        return ""
    domain = re.sub(r"^www\.", "", re.sub(r"^https?://", "", website).split("/")[0])
    ranked = sorted(
        emails.items(),
        key=lambda kv: (
            0 if kv[1] == "mailto link" else 1,
            0 if domain and domain in kv[0] else 1,
            0 if kv[0].split("@")[0] not in ("info", "contact", "hello", "office", "admin") else 1,
        ),
    )
    return ranked[0][0]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("display_name")
    ap.add_argument("website")
    ap.add_argument("--location", default="", help="location / service area, e.g. 'Tulsa, OK'")
    ap.add_argument("--force", action="store_true", help="rebuild over an existing folder")
    ap.add_argument("--no-scrape", action="store_true", help="skip web scraping")
    args = ap.parse_args()

    dest = PROSPECTS / args.slug
    if dest.exists():
        if not args.force:
            print(f"✗ {dest} already exists (use --force to rebuild)", file=sys.stderr)
            return 1
        shutil.rmtree(dest)

    # 1. scrape
    data: dict = {}
    if not args.no_scrape:
        print(f"→ Scraping {args.website} …")
        out = subprocess.run(
            [sys.executable, str(SCRIPTS / "scrape-prospect.py"), args.website, "--json"],
            capture_output=True, text=True, cwd=ROOT,
        )
        if out.returncode == 0:
            try:
                data = json.loads(out.stdout)
            except json.JSONDecodeError:
                print("! scrape output not parseable, continuing without", file=sys.stderr)
        else:
            print(f"! scrape failed: {out.stderr.strip()[:300]}", file=sys.stderr)

    # 2. scaffold
    run([str(SCRIPTS / "new-holiday-prospect.sh"), args.slug, args.display_name, args.website])

    # 3. fill notes.md
    notes_path = dest / "notes.md"
    notes = notes_path.read_text(encoding="utf-8")

    emails = data.get("emails", {})
    phones = data.get("phones", {})
    best_email = pick_email(emails, args.website)
    best_phone = next(iter(phones), "")
    names = data.get("possible_names", [])
    forms = data.get("contact_form_urls", [])
    keywords = data.get("service_keywords", [])
    desc = data.get("description", "") or data.get("title", "")

    def fill(label: str, value: str) -> None:
        nonlocal notes
        if value:
            notes = notes.replace(f"- {label}:\n", f"- {label}: {value}\n", 1)

    fill("Location / service area", args.location)
    fill("Primary services shown", ", ".join(keywords))
    fill("Notable wording from their site", desc[:300])
    fill("Contact person", " / ".join(names[:2]))
    fill("Contact email", best_email)
    fill("Contact phone/text", best_phone)
    fill("Contact form URL", forms[0] if forms else "")

    # add a drafted-date placeholder line in Send log if missing
    if "Email drafted:" not in notes:
        notes = notes.replace(
            "## Send log\n",
            "## Send log\n\n- Email drafted:\n- Email sent:\n",
            1,
        )

    # append extra scraped contact candidates for human review
    extras = []
    other_emails = [e for e in emails if e != best_email]
    other_phones = [p for p in phones if p != best_phone]
    if other_emails:
        extras.append("- Other emails found: " + ", ".join(other_emails[:5]))
    if other_phones:
        extras.append("- Other phones found: " + ", ".join(other_phones[:5]))
    if data.get("social"):
        extras.append("- Social: " + ", ".join(data["social"][:4]))
    if extras:
        notes += "\n## Scraped extras (review)\n\n" + "\n".join(extras) + "\n"

    notes_path.write_text(notes, encoding="utf-8")

    # 4. save raw scrape
    if data:
        (dest / "scrape.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

    # 5. summary + index
    run([sys.executable, str(SCRIPTS / "generate-outreach-index.py")])

    print(f"\n✓ Prospect built: {dest.relative_to(ROOT)}")
    if best_email:
        print(f"  Contact email: {best_email}")
    else:
        print("  ! No email found — check scrape.json / their contact form")
    print(f"  Next: write {args.slug}/email-draft.md, then `getwork summary`")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
