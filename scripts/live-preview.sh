#!/usr/bin/env bash
# Serve outreach HTML with BrowserSync live reload.
#
# Usage:
#   ./scripts/live-preview.sh       # defaults to port 8765
#   ./scripts/live-preview.sh 9000
#
# Requires Node/npm. Uses npx so nothing has to be installed in this repo.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PORT="${1:-8765}"

if ! command -v npx >/dev/null 2>&1; then
  echo "npx is required for live preview. Install Node/npm or use ./scripts/preview.sh instead." >&2
  exit 1
fi

"$ROOT/scripts/generate-outreach-index.py"

echo "→ Live previewing $ROOT/outreach on http://localhost:$PORT"
echo ""
echo "URLs:"
echo "  Directory:    http://localhost:$PORT/"
echo "  Base doc:     http://localhost:$PORT/base/holiday-lighting-prospect-base.html"
echo "  Prospects:    http://localhost:$PORT/prospects/"
echo "  Colorado:     http://localhost:$PORT/prospects/coloradochristmaslights/portfolio.html"
echo "  HoliGlows:    http://localhost:$PORT/prospects/holiglows/portfolio.html"
echo "  Iceberg:      http://localhost:$PORT/prospects/icebergchristmaslights/portfolio.html"
echo ""
echo "BrowserSync will inject a tiny reload script into HTML responses."
echo "Save a watched file and the browser refreshes automatically."
echo "Restart this script to add brand-new HTML files to the directory."
echo "(Ctrl-C to stop)"
echo ""

exec npx --yes browser-sync start \
  --server "$ROOT/outreach" \
  --files "$ROOT/outreach/**/*.html,$ROOT/outreach/**/*.css,$ROOT/outreach/**/*.js,$ROOT/outreach/**/*.svg,$ROOT/outreach/**/*.jpg,$ROOT/outreach/**/*.png,$ROOT/outreach/**/*.webp" \
  --port "$PORT" \
  --host "0.0.0.0" \
  --startPath "/" \
  --no-ui \
  --no-notify
