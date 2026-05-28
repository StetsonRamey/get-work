#!/usr/bin/env bash
# Build PDF from a portfolio HTML file.
# Usage:
#   ./scripts/build.sh                              # builds the base
#   ./scripts/build.sh outreach/base/portfolio-base.html
#   ./scripts/build.sh outreach/prospects/local-nerds/portfolio.html
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INPUT="${1:-$ROOT/outreach/base/portfolio-base.html}"

if [[ ! -f "$INPUT" ]]; then
  echo "✗ Not found: $INPUT" >&2
  exit 1
fi

OUTPUT="${INPUT%.html}.pdf"

echo "→ Building $INPUT"
weasyprint "$INPUT" "$OUTPUT"
echo "✓ Wrote $OUTPUT"

# Page count check via pdfinfo if available
if command -v pdfinfo >/dev/null 2>&1; then
  PAGES=$(pdfinfo "$OUTPUT" | awk '/^Pages:/ {print $2}')
  echo "  Pages: $PAGES"
fi
