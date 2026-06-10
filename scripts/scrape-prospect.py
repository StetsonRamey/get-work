#!/usr/bin/env python3
"""Scrape a prospect's website for contact info and context.

Usage:
  ./scripts/scrape-prospect.py https://www.example.com/
  ./scripts/scrape-prospect.py https://www.example.com/ --json   # machine-readable

Fetches the homepage plus likely contact/about pages and extracts:
  - email addresses (mailto: links + text)
  - phone numbers (tel: links + text)
  - possible contact names (about/team headings, "owner", etc.)
  - social links, page title/description, service keywords
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(r"(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}")
IGNORE_EMAIL_DOMAINS = ("example.com", "sentry.io", "wixpress.com", "schema.org",
                        "your-domain", "domain.com", "email.com", "godaddy.com")
IGNORE_EMAIL_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".css", ".js")

CONTACT_HINTS = ("contact", "about", "quote", "estimate", "team", "our-story", "meet")
SERVICE_KEYWORDS = (
    "christmas light", "holiday light", "residential", "commercial",
    "installation", "removal", "maintenance", "storage", "design",
    "permanent lighting", "wedding", "event lighting", "landscape lighting",
)
SOCIAL_HOSTS = ("facebook.com", "instagram.com", "youtube.com", "linkedin.com",
                "tiktok.com", "x.com", "twitter.com", "yelp.com", "google.com/maps")

NAME_CONTEXT_RE = re.compile(
    r"(?:owner|founder|founded by|started by|my name is|i'm|i am|meet)\s+(?:is\s+)?"
    r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})")


def fetch(url: str, timeout: int = 20) -> tuple[str, str]:
    """Return (final_url, html) or raise."""
    r = requests.get(url, headers={"User-Agent": UA}, timeout=timeout, allow_redirects=True)
    r.raise_for_status()
    return str(r.url), r.text


def candidate_pages(base_url: str, soup: BeautifulSoup) -> list[str]:
    seen, out = set(), []
    base_host = urlparse(base_url).netloc
    for a in soup.find_all("a", href=True):
        href = urljoin(base_url, a["href"])
        p = urlparse(href)
        if p.netloc != base_host:
            continue
        path = p.path.lower()
        if any(h in path for h in CONTACT_HINTS):
            clean = href.split("#")[0]
            if clean not in seen:
                seen.add(clean)
                out.append(clean)
    return out[:6]


def extract(url: str, html: str, data: dict) -> None:
    soup = BeautifulSoup(html, "html.parser")

    if not data["title"] and soup.title and soup.title.string:
        data["title"] = soup.title.string.strip()
    if not data["description"]:
        meta = soup.find("meta", attrs={"name": "description"}) or \
               soup.find("meta", attrs={"property": "og:description"})
        if meta and meta.get("content"):
            data["description"] = meta["content"].strip()

    # mailto / tel links (highest confidence)
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.lower().startswith("mailto:"):
            email = href[7:].split("?")[0].strip().lower()
            if email:
                data["emails"].setdefault(email, "mailto link")
        elif href.lower().startswith("tel:"):
            data["phones"].setdefault(re.sub(r"[^\d+]", "", href[4:]), "tel link")
        else:
            full = urljoin(url, href)
            if any(h in full for h in SOCIAL_HOSTS) and full not in data["social"]:
                data["social"].append(full)

    text = soup.get_text(" ", strip=True)

    for email in EMAIL_RE.findall(text) + EMAIL_RE.findall(html):
        e = email.lower().rstrip(".")
        if any(e.endswith(ext) for ext in IGNORE_EMAIL_EXT):
            continue
        if any(d in e for d in IGNORE_EMAIL_DOMAINS):
            continue
        data["emails"].setdefault(e, f"found on {urlparse(url).path or '/'}")

    for phone in PHONE_RE.findall(text):
        digits = re.sub(r"[^\d]", "", phone)
        if len(digits) in (10, 11):
            data["phones"].setdefault(phone.strip(), f"found on {urlparse(url).path or '/'}")

    for m in NAME_CONTEXT_RE.finditer(text):
        name = m.group(1)
        if name not in data["possible_names"]:
            data["possible_names"].append(name)

    low = text.lower()
    for kw in SERVICE_KEYWORDS:
        if kw in low and kw not in data["service_keywords"]:
            data["service_keywords"].append(kw)

    # quote/contact form pages
    if soup.find("form") and any(h in url.lower() for h in ("contact", "quote", "estimate")):
        if url not in data["contact_form_urls"]:
            data["contact_form_urls"].append(url)


def scrape(start_url: str) -> dict:
    data = {
        "website": start_url,
        "title": "",
        "description": "",
        "emails": {},          # email -> source
        "phones": {},          # phone -> source
        "possible_names": [],
        "social": [],
        "service_keywords": [],
        "contact_form_urls": [],
        "pages_scraped": [],
        "errors": [],
    }
    try:
        final, html = fetch(start_url)
    except Exception as e:  # noqa: BLE001
        data["errors"].append(f"{start_url}: {e}")
        return data
    data["website"] = final
    data["pages_scraped"].append(final)
    extract(final, html, data)

    soup = BeautifulSoup(html, "html.parser")
    for page in candidate_pages(final, soup):
        if page in data["pages_scraped"]:
            continue
        try:
            purl, phtml = fetch(page)
            data["pages_scraped"].append(page)
            extract(purl, phtml, data)
        except Exception as e:  # noqa: BLE001
            data["errors"].append(f"{page}: {e}")
    return data


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", help="company website URL")
    ap.add_argument("--json", action="store_true", help="emit JSON only")
    args = ap.parse_args()

    url = args.url
    if not url.startswith("http"):
        url = "https://" + url
    data = scrape(url)

    if args.json:
        print(json.dumps(data, indent=2))
        return 0

    print(f"Website:     {data['website']}")
    print(f"Title:       {data['title']}")
    print(f"Description: {data['description'][:200]}")
    print(f"Pages:       {len(data['pages_scraped'])} scraped")
    print("\nEmails:")
    for e, src in data["emails"].items():
        print(f"  {e}  ({src})")
    print("\nPhones:")
    for p, src in data["phones"].items():
        print(f"  {p}  ({src})")
    if data["possible_names"]:
        print("\nPossible contact names:")
        for n in data["possible_names"]:
            print(f"  {n}")
    if data["contact_form_urls"]:
        print("\nContact/quote forms:")
        for u in data["contact_form_urls"]:
            print(f"  {u}")
    if data["service_keywords"]:
        print("\nService keywords: " + ", ".join(data["service_keywords"]))
    if data["social"]:
        print("\nSocial links:")
        for s in data["social"][:8]:
            print(f"  {s}")
    if data["errors"]:
        print("\nErrors:")
        for err in data["errors"]:
            print(f"  {err}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
