#!/usr/bin/env python3
"""Generate outreach/index.html as a local preview directory."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTREACH = ROOT / "outreach"
INDEX = OUTREACH / "index.html"

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")


def clean(value: str) -> str:
    value = TAG_RE.sub("", value)
    value = html.unescape(value)
    return " ".join(value.split())


def label_for(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    for regex in (TITLE_RE, H1_RE):
        match = regex.search(text)
        if match:
            value = clean(match.group(1))
            if value:
                return value
    return path.stem.replace("-", " ").replace("_", " ").title()


def section_name(rel: Path) -> str:
    parts = rel.parts
    if parts[0] == "base":
        return "Base templates"
    if parts[0] == "prospects" and len(parts) > 1:
        return "Prospects"
    return "Other"


def main() -> None:
    files = sorted(
        p for p in OUTREACH.rglob("*.html")
        if p != INDEX and ".git" not in p.parts
    )

    groups: dict[str, list[tuple[Path, str]]] = {}
    for path in files:
        rel = path.relative_to(OUTREACH)
        groups.setdefault(section_name(rel), []).append((rel, label_for(path)))

    cards = []
    for group in ("Base templates", "Prospects", "Other"):
        items = groups.get(group, [])
        if not items:
            continue
        links = []
        for rel, title in items:
            href = "/" + rel.as_posix()
            slug = rel.parent.name if rel.parts[0] == "prospects" else rel.name
            links.append(f"""
          <a class=\"item\" href=\"{html.escape(href)}\">
            <span class=\"item-title\">{html.escape(title)}</span>
            <span class=\"item-path\">/{html.escape(rel.as_posix())}</span>
            <span class=\"item-slug\">{html.escape(slug)}</span>
          </a>""")
        cards.append(f"""
      <section class=\"card\">
        <h2>{html.escape(group)}</h2>
        <div class=\"items\">{''.join(links)}
        </div>
      </section>""")

    INDEX.write_text(f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Outreach Preview Directory</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f6f3eb;
      --card: #fffdf8;
      --ink: #182033;
      --muted: #687184;
      --line: #e3ddcf;
      --green: #1f7a4a;
      --teal: #4caea7;
      --shadow: 0 18px 60px rgba(24,32,51,.08);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at 20% 0%, rgba(76,174,167,.18), transparent 28rem),
        radial-gradient(circle at 90% 15%, rgba(31,122,74,.12), transparent 22rem),
        var(--bg);
    }}
    main {{ width: min(1120px, calc(100% - 2rem)); margin: 0 auto; padding: 4rem 0; }}
    .hero {{ margin-bottom: 2rem; }}
    .eyebrow {{
      margin: 0 0 .7rem;
      color: var(--green);
      font-size: .82rem;
      font-weight: 800;
      letter-spacing: .14em;
      text-transform: uppercase;
    }}
    h1 {{ margin: 0; font-size: clamp(2.7rem, 8vw, 5.7rem); line-height: .95; letter-spacing: -.06em; }}
    .lead {{ margin: 1rem 0 0; max-width: 62ch; color: var(--muted); font-size: 1.08rem; line-height: 1.65; }}
    .grid {{ display: grid; gap: 1rem; }}
    .card {{
      background: color-mix(in srgb, var(--card) 92%, transparent);
      border: 1px solid var(--line);
      border-radius: 24px;
      box-shadow: var(--shadow);
      padding: 1.1rem;
      backdrop-filter: blur(8px);
    }}
    h2 {{ margin: .15rem .35rem 1rem; font-size: 1rem; letter-spacing: .02em; color: var(--green); }}
    .items {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: .75rem; }}
    .item {{
      display: grid;
      gap: .35rem;
      min-height: 8.5rem;
      padding: 1rem;
      text-decoration: none;
      color: inherit;
      background: white;
      border: 1px solid var(--line);
      border-radius: 18px;
      transition: transform .15s ease, border-color .15s ease, box-shadow .15s ease;
    }}
    .item:hover {{ transform: translateY(-2px); border-color: var(--teal); box-shadow: 0 14px 35px rgba(24,32,51,.10); }}
    .item-title {{ font-weight: 800; line-height: 1.2; }}
    .item-path {{ color: var(--muted); font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .78rem; overflow-wrap: anywhere; }}
    .item-slug {{ align-self: end; justify-self: start; color: var(--green); background: #eef7f1; border-radius: 999px; padding: .25rem .55rem; font-size: .76rem; font-weight: 800; }}
    .note {{ margin-top: 1rem; color: var(--muted); font-size: .9rem; }}
  </style>
</head>
<body>
  <main>
    <header class=\"hero\">
      <p class=\"eyebrow\">Local preview</p>
      <h1>Outreach pages</h1>
      <p class=\"lead\">Generated from every <code>.html</code> file under <code>outreach/</code>. Run <code>./scripts/live-preview.sh</code>, edit files, and BrowserSync will refresh the browser on save.</p>
    </header>
    <div class=\"grid\">{''.join(cards)}
    </div>
    <p class=\"note\">Generated by <code>scripts/generate-outreach-index.py</code>. Restart the preview server to pick up brand-new HTML files.</p>
  </main>
</body>
</html>
""", encoding="utf-8")
    print(f"Generated {INDEX.relative_to(ROOT)} with {len(files)} pages")


if __name__ == "__main__":
    main()
