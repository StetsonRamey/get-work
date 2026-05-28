#!/usr/bin/env bash
# Scaffold a new tailored portfolio variant for a specific prospect.
# Usage:
#   ./scripts/new-prospect.sh local-nerds
#   ./scripts/new-prospect.sh flow-digital "Flow Digital"
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SLUG="${1:?usage: new-prospect.sh <slug> [\"Display Name\"]}"
DISPLAY="${2:-$SLUG}"

DEST="$ROOT/outreach/prospects/$SLUG"
if [[ -e "$DEST" ]]; then
  echo "✗ Already exists: $DEST" >&2
  exit 1
fi

mkdir -p "$DEST/assets"
# Symlink shared assets so we don't duplicate the headshot per prospect.
ln -s "../../../base/assets/headshot.jpg" "$DEST/assets/headshot.jpg"

# Copy the base HTML in.
cp "$ROOT/outreach/base/portfolio-base.html" "$DEST/portfolio.html"

# Drop a notes file for context-gathering.
cat > "$DEST/notes.md" <<EOF
# $DISPLAY

**Status:** drafting
**Date:** $(date +%Y-%m-%d)

## What I know about them
- (services / niche / company size / who I'm sending to)

## Why I'm a fit
- (the specific hook I want the {{AGENCY_HOOK}} sentence to land)

## Customization checklist
- [ ] Replace {{AGENCY_NAME}} in portfolio.html (1 place — subcontract line)
- [ ] Replace {{DATE}} in portfolio.html (footer — Month Year format)
- [ ] Build PDF: \`./scripts/build.sh outreach/prospects/$SLUG/portfolio.html\`

## Send log
- [ ] (when sent, to whom, channel, response)
EOF

echo "✓ Created $DEST/"
echo "  $DEST/portfolio.html"
echo "  $DEST/notes.md"
echo ""
echo "Next:"
echo "  1. Edit portfolio.html — search for {{ to find every customization point"
echo "  2. ./scripts/build.sh outreach/prospects/$SLUG/portfolio.html"
