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

"$ROOT/scripts/generate-outreach-index.py"

echo "→ Serving $ROOT/outreach on http://localhost:$PORT (no-cache)"
echo ""
echo "Local VM URLs:"
echo "  Directory:    http://localhost:$PORT/"
echo "  Base doc:     http://localhost:$PORT/base/portfolio-base.html"
echo "  Prospects:    http://localhost:$PORT/prospects/"
echo "  Colorado:     http://localhost:$PORT/prospects/coloradochristmaslights/portfolio.html"
echo "  HoliGlows:    http://localhost:$PORT/prospects/holiglows/portfolio.html"
echo "  Iceberg:      http://localhost:$PORT/prospects/icebergchristmaslights/portfolio.html"
echo ""
echo "Browser-from-outside-VM URLs:"
echo "  Colorado:     http://get-work.exe.xyz:$PORT/prospects/coloradochristmaslights/portfolio.html"
echo "  HoliGlows:    http://get-work.exe.xyz:$PORT/prospects/holiglows/portfolio.html"
echo "  Iceberg:      http://get-work.exe.xyz:$PORT/prospects/icebergchristmaslights/portfolio.html"
echo ""
echo "Note: plain http is intentional for preview port $PORT. The production/custom-domain service is separate."
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
