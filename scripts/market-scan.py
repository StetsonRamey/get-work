#!/usr/bin/env python3
"""Scan a metro for holiday-lighting installer companies (market validation).

Usage:
  ./scripts/market-scan.py "Tulsa, OK"
  ./scripts/market-scan.py "Tulsa, OK" --no-verify     # faster, skip homepage fetches
  ./scripts/market-scan.py "Tulsa, OK" --json

Searches DuckDuckGo with several query variants, dedupes by domain, filters
directories/lead-gen junk, optionally fetches each homepage to verify it's a
real local installer, and writes results to data/scans/<slug>.json.
If the metro matches an entry in data/markets.json, its scan fields are updated.
Run `getwork markets` afterwards to refresh the markets table.

This is a *scan*, not a build: it does not create prospect folders.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
MARKETS = ROOT / "data" / "markets.json"
SCANS = ROOT / "data" / "scans"
PROSPECTS = ROOT / "outreach" / "prospects"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")

QUERY_TEMPLATES = (
    "christmas light installation {metro}",
    "holiday lighting company {metro}",
    "professional christmas light installers {metro}",
)

# Directories, lead-gen, marketplaces, social, news — not actual companies.
JUNK_DOMAINS = {
    "yelp.com", "angi.com", "angieslist.com", "thumbtack.com", "homeadvisor.com",
    "houzz.com", "porch.com", "bark.com", "expertise.com", "yellowpages.com",
    "bbb.org", "facebook.com", "instagram.com", "nextdoor.com", "linkedin.com",
    "reddit.com", "youtube.com", "tiktok.com", "pinterest.com", "groupon.com",
    "craigslist.org", "care.com", "taskrabbit.com", "google.com", "mapquest.com",
    "wikipedia.org", "amazon.com", "etsy.com", "homedepot.com", "lowes.com",
    "walmart.com", "costco.com", "chamberofcommerce.com", "manta.com",
    "buildzoom.com", "levelset.com", "openstreetmap.org", "tripadvisor.com",
    "eventbrite.com", "patch.com", "city-data.com", "zillow.com", "realtor.com",
    "superpages.com", "foursquare.com", "alignable.com", "birdeye.com",
    "cylex.us.com", "hotfrog.com", "showmelocal.com", "merchantcircle.com",
    "localsolution.com", "threebestrated.com", "findlocal-handymen.com",
    "qualitysmith.com", "networx.com", "fash.com", "lessons.com", "duckduckgo.com",
}
# National franchise corporate sites (local franchisee pages still pass if on own domain)
FRANCHISE_HINTS = (
    "christmasdecor", "blingle", "lightupnation", "shinelightsolutions",
    "trimlight", "jellyfishlighting", "everlights", "gemstonelights",
    "holidayheroes", "weHangChristmasLights".lower(), "christmaslightpros",
)
KEYWORDS = ("christmas light", "holiday light", "christmas lighting", "holiday lighting")


def ddg_search(query: str) -> list[str]:
    """Return result URLs from DuckDuckGo HTML endpoint."""
    try:
        r = requests.post(
            "https://html.duckduckgo.com/html/",
            data={"q": query},
            headers={"User-Agent": UA},
            timeout=20,
        )
        r.raise_for_status()
    except Exception as e:  # noqa: BLE001
        print(f"  ! search failed for {query!r}: {e}", file=sys.stderr)
        return []
    soup = BeautifulSoup(r.text, "html.parser")
    urls = []
    for a in soup.select("a.result__a[href]"):
        href = a["href"]
        # DDG wraps results: //duckduckgo.com/l/?uddg=<encoded>&rut=...
        if "uddg=" in href:
            qs = parse_qs(urlparse(href).query)
            target = qs.get("uddg", [""])[0]
            if target:
                urls.append(unquote(target))
        elif href.startswith("http"):
            urls.append(href)
    return urls


def domain_of(url: str) -> str:
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def existing_prospect_domains() -> set[str]:
    domains = set()
    if not PROSPECTS.exists():
        return domains
    for notes in PROSPECTS.glob("*/notes.md"):
        m = re.search(r"\*\*Website:\*\*\s*(\S+)", notes.read_text(errors="ignore"))
        if m and m.group(1).startswith("http"):
            domains.add(domain_of(m.group(1)))
    return domains


def verify(domain: str) -> dict:
    """Fetch homepage; return verification info."""
    info = {"verified": False, "title": "", "phone": "", "reason": ""}
    for scheme in ("https", "http"):
        try:
            r = requests.get(f"{scheme}://{domain}/", headers={"User-Agent": UA},
                             timeout=15, allow_redirects=True)
            r.raise_for_status()
            break
        except Exception as e:  # noqa: BLE001
            info["reason"] = str(e)[:120]
            r = None
    if r is None:
        info["reason"] = info["reason"] or "unreachable"
        return info
    soup = BeautifulSoup(r.text, "html.parser")
    if soup.title and soup.title.string:
        info["title"] = soup.title.string.strip()[:120]
    text = soup.get_text(" ", strip=True).lower()
    has_kw = any(k in text for k in KEYWORDS)
    phone = re.search(r"(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}", soup.get_text(" ", strip=True))
    if phone:
        info["phone"] = phone.group(0).strip()
    info["verified"] = has_kw
    if not has_kw:
        info["reason"] = "no holiday-lighting keywords on homepage"
    return info


def scan(metro: str, do_verify: bool = True) -> dict:
    known = existing_prospect_domains()
    seen: dict[str, dict] = {}
    for tmpl in QUERY_TEMPLATES:
        q = tmpl.format(metro=metro)
        print(f"→ Searching: {q}")
        for url in ddg_search(q):
            d = domain_of(url)
            if not d or d in seen:
                continue
            entry = {"domain": d, "url": url, "queries": [q], "flags": []}
            base = d.split(".")[0] if "." in d else d
            if d in JUNK_DOMAINS or any(d.endswith("." + j) for j in JUNK_DOMAINS):
                continue
            if any(h in d.replace("-", "") for h in FRANCHISE_HINTS):
                entry["flags"].append("franchise?")
            if d in known:
                entry["flags"].append("already-prospect")
            seen[d] = entry
        time.sleep(1.5)  # be polite

    candidates = list(seen.values())
    if do_verify:
        print(f"→ Verifying {len(candidates)} domains …")
        for c in candidates:
            v = verify(c["domain"])
            c.update(v)
    else:
        for c in candidates:
            c.update({"verified": None, "title": "", "phone": "", "reason": "not checked"})

    return {
        "metro": metro,
        "date": dt.date.today().isoformat(),
        "queries": [t.format(metro=metro) for t in QUERY_TEMPLATES],
        "candidates": candidates,
    }


def slugify(metro: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", metro.lower()).strip("-")


def update_markets(metro: str, result: dict) -> None:
    if not MARKETS.exists():
        return
    data = json.loads(MARKETS.read_text())
    verified = [c for c in result["candidates"] if c.get("verified")]
    target = metro.lower().split(",")[0].strip()
    for m in data.get("markets", []):
        if m["metro"].lower() == target or target in m["metro"].lower():
            m["last_scan"] = result["date"]
            m["installer_count"] = len(verified)
            m["scan_file"] = f"data/scans/{slugify(metro)}.json"
            MARKETS.write_text(json.dumps(data, indent=2) + "\n")
            print(f"✓ Updated {m['metro']} in data/markets.json ({len(verified)} verified installers)")
            return
    print(f"! Metro {metro!r} not in data/markets.json — scan saved but tracker not updated")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("metro", help='e.g. "Tulsa, OK"')
    ap.add_argument("--no-verify", action="store_true", help="skip homepage verification fetches")
    ap.add_argument("--json", action="store_true", help="print JSON to stdout")
    args = ap.parse_args()

    result = scan(args.metro, do_verify=not args.no_verify)

    SCANS.mkdir(parents=True, exist_ok=True)
    out = SCANS / f"{slugify(args.metro)}.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    update_markets(args.metro, result)

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    cands = result["candidates"]
    verified = [c for c in cands if c.get("verified")]
    print(f"\n=== {args.metro} — {len(verified)} verified / {len(cands)} candidates ===\n")
    for c in sorted(cands, key=lambda c: (not c.get("verified"), c["domain"])):
        mark = "✓" if c.get("verified") else ("?" if c.get("verified") is None else "✗")
        flags = " ".join(f"[{f}]" for f in c["flags"])
        line = f" {mark} {c['domain']:42s} {c.get('phone',''):16s} {flags}"
        print(line.rstrip())
        if c.get("title"):
            print(f"     {c['title']}")
        elif c.get("reason"):
            print(f"     ({c['reason']})")
    print(f"\nSaved: {out.relative_to(ROOT)}")
    print("Next: review, then `getwork markets` to refresh the markets table,")
    print("      and `getwork build-prospect <slug> \"Name\" <url> --location \"" + args.metro + "\"` for keepers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
