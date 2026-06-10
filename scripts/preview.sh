#!/usr/bin/env bash
# Serve the outreach directory on a local web server with no-cache headers
# so edits show up on a plain refresh (no Cmd+Shift+R needed).
#
# Usage:
#   ./scripts/preview.sh           # defaults to port 8765
#   ./scripts/preview.sh 9000
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PORT="${1:-8765}"
if [[ "$PORT" == "8000" ]]; then
  EXTERNAL_BASE="https://get-work.exe.xyz"
else
  EXTERNAL_BASE="https://get-work.exe.xyz:${PORT}"
fi

"$ROOT/scripts/generate-outreach-index.py"

echo "→ Serving $ROOT/outreach on port $PORT (no-cache)"
echo ""
echo "Open from your laptop/browser:"
echo "  Directory:    $EXTERNAL_BASE/"
echo "  Base doc:     $EXTERNAL_BASE/base/portfolio-base.html"
echo "  Prospects:    $EXTERNAL_BASE/prospects/"
echo "  Colorado:     $EXTERNAL_BASE/prospects/coloradochristmaslights/portfolio.html"
echo "  HoliGlows:    $EXTERNAL_BASE/prospects/holiglows/portfolio.html"
echo "  Iceberg:      $EXTERNAL_BASE/prospects/icebergchristmaslights/portfolio.html"
echo ""
echo "Inside the VM only:"
echo "  http://localhost:$PORT/"
echo ""
echo "The exe.dev proxy provides HTTPS externally. The production/custom-domain service is separate."
echo "(Ctrl-C to stop)"

cd "$ROOT/outreach"
exec python3 -c "
import http.server, socketserver, sys
class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
port = int(sys.argv[1])
with socketserver.TCPServer(('', port), NoCacheHandler) as httpd:
    httpd.serve_forever()
" "$PORT"
