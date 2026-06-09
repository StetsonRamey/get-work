#!/usr/bin/env bash
# Scaffold a holiday-lighting prospect sheet.
# Usage:
#   ./scripts/new-holiday-prospect.sh coloradochristmaslights "Colorado Christmas Lights" "https://www.coloradochristmaslights.com/"
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SLUG="${1:?usage: new-holiday-prospect.sh <slug> [\"Display Name\"] [website]}"
DISPLAY="${2:-$SLUG}"
WEBSITE="${3:-}"
DATE_LABEL="$(date +'%B %Y')"
DEST="$ROOT/outreach/prospects/$SLUG"
BASE="$ROOT/outreach/base/holiday-lighting-prospect-base.html"

if [[ -e "$DEST" ]]; then
  echo "✗ Already exists: $DEST" >&2
  exit 1
fi

if [[ ! -f "$BASE" ]]; then
  echo "✗ Missing base template: $BASE" >&2
  exit 1
fi

mkdir -p "$DEST/assets"
ln -s "../../../base/assets/headshot.jpg" "$DEST/assets/headshot.jpg"
cp "$BASE" "$DEST/portfolio.html"

python3 - <<PY
from pathlib import Path
from urllib.parse import quote
path = Path("$DEST/portfolio.html")
text = path.read_text()
repls = {
    "{{COMPANY_NAME}}": "$DISPLAY",
    "{{COMPANY_NAME_ENCODED}}": quote("$DISPLAY"),
    "{{DATE}}": "$DATE_LABEL",
    "{{CUSTOM_HOOK_HEADLINE}}": "A local note for $DISPLAY",
    "{{CUSTOM_HOOK_BODY}}": "Rather than guessing at your internal process, I wanted to start by sharing the core systems that tend to matter most in holiday lighting operations: quote intake, billing, returning customer renewals, and routing.",
    "{{EMAIL}}": "me@stetson.dev",
    "{{PHONE_TEL}}": "+13072145159",
    "{{PHONE_DISPLAY}}": "307-214-5159",
    "{{QUOTE_VIDEO_URL}}": "#",
    "{{BILLING_VIDEO_URL}}": "#",
    "{{RENEWAL_VIDEO_URL}}": "#",
    "{{ROUTING_VIDEO_URL}}": "#",
    "{{QUOTE_VIDEO_BUTTON_CLASS}}": "",
    "{{BILLING_VIDEO_BUTTON_CLASS}}": "",
    "{{RENEWAL_VIDEO_BUTTON_CLASS}}": "",
    "{{ROUTING_VIDEO_BUTTON_CLASS}}": "",
}
for old, new in repls.items():
    text = text.replace(old, new)
path.write_text(text)
PY

cat > "$DEST/notes.md" <<EOF
# $DISPLAY

**Status:** drafting  
**Date:** $(date +%Y-%m-%d)  
**Website:** $WEBSITE  
**Prospect URL:** https://$SLUG.stetson.dev/

## Company research

- Location / service area:
- Primary services shown:
- Residential / commercial focus:
- Notable wording from their site:
- Current quote/contact process observed:
- Any relevant photos/projects/positioning:

## Contact info

- Contact person:
- Contact email:
- Contact phone/text:
- Contact form URL:

## Personalization

- Personalized opening line:
- Reason these workflows may be relevant:
- Best CTA:

## Page checklist

- [x] Contact info added to portfolio.html:
  - \`me@stetson.dev\`
  - \`307-214-5159\`
- [ ] Replace custom hook headline/body if needed
- [ ] Add quote workflow video URL
- [ ] Add billing/setup video URL
- [ ] Add returning customer renewal video URL
- [ ] Add routing/dispatch video URL
- [ ] Remove \`disabled\` class from video buttons after URLs are added
- [ ] Preview: \`./scripts/preview.sh\`
- [ ] Build PDF if wanted: \`./scripts/build.sh outreach/prospects/$SLUG/portfolio.html\`
- [ ] Add DNS if wanted: \`./scripts/add-domain.sh $SLUG\`
- [ ] Add domain in exe: \`ssh exe.dev domain add get-work $SLUG.stetson.dev\`

## Send log

- [ ] Initial email sent:
- [ ] Follow-up 1 sent:
- [ ] Follow-up 2 sent:
- Response notes:
EOF

echo "✓ Created $DEST/"
echo "  $DEST/portfolio.html"
echo "  $DEST/notes.md"
echo ""
echo "Preview after starting server: http://localhost:8765/prospects/$SLUG/portfolio.html"
