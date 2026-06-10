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
if [[ "$PORT" == "8000" ]]; then
  EXTERNAL_BASE="https://get-work.exe.xyz"
else
  EXTERNAL_BASE="https://get-work.exe.xyz:${PORT}"
fi

if ! command -v npx >/dev/null 2>&1; then
  echo "npx is required for live preview. Install Node/npm or use ./scripts/preview.sh instead." >&2
  exit 1
fi

"$ROOT/scripts/generate-outreach-index.py"

echo "→ Live previewing $ROOT/outreach on port $PORT"
echo ""
echo "Open from your laptop/browser:"
echo "  Directory:    $EXTERNAL_BASE/"
echo "  Base doc:     $EXTERNAL_BASE/base/holiday-lighting-prospect-base.html"
echo "  Prospects:    $EXTERNAL_BASE/prospects/"
echo "  Colorado:     $EXTERNAL_BASE/prospects/coloradochristmaslights/portfolio.html"
echo "  HoliGlows:    $EXTERNAL_BASE/prospects/holiglows/portfolio.html"
echo "  Iceberg:      $EXTERNAL_BASE/prospects/icebergchristmaslights/portfolio.html"
echo ""
echo "Inside the VM only:"
echo "  http://localhost:$PORT/"
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
  --no-open \
  --no-ui \
  --no-notify
