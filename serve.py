#!/usr/bin/env python3
"""
Serves prospect portfolios based on subdomain.
  northwind.stetson.dev                 → outreach/prospects/northwind/portfolio.pdf
  coloradochristmaslights.stetson.dev   → outreach/prospects/coloradochristmaslights/portfolio.html
  Also handles get-work.exe.xyz/<slug> as a fallback.
"""
import http.server
import os
import socketserver

OUTREACH_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outreach", "prospects")

HTML_PROSPECTS = {
    "coloradochristmaslights",
    "holiglows",
    "icebergchristmaslights",
}


class ResumeHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        slug = None

        # Try subdomain first: northwind.stetson.dev
        host = self.headers.get("Host", "")
        parts = host.split(".")
        if len(parts) >= 3 and parts[-2] in ("stetson",):
            slug = parts[0]
        # Also try: X-Forwarded-Host header (exe.dev proxy)
        fwd_host = self.headers.get("X-Forwarded-Host", "")
        if not slug and fwd_host:
            fwd_parts = fwd_host.split(".")
            if len(fwd_parts) >= 3 and fwd_parts[-2] in ("stetson",):
                slug = fwd_parts[0]
        # Fallback: path-based, e.g. /northwind
        if not slug:
            path = self.path.strip("/").split("?")[0].split("/")[0]
            if path and path != "favicon.ico":
                slug = path

        if not slug:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            # List available resumes
            prospects = []
            if os.path.isdir(OUTREACH_DIR):
                for d in sorted(os.listdir(OUTREACH_DIR)):
                    prospect_dir = os.path.join(OUTREACH_DIR, d)
                    pdf = os.path.join(prospect_dir, "portfolio.pdf")
                    page = os.path.join(prospect_dir, "portfolio.html")
                    if os.path.isfile(pdf) or d in HTML_PROSPECTS and os.path.isfile(page):
                        prospects.append(d)
            html = "<html><body><h1>Prospect portfolios</h1><ul>"
            for p in prospects:
                html += f'<li><a href="/{p}">{p}</a></li>'
            html += "</ul></body></html>"
            self.wfile.write(html.encode())
            return

        prospect_dir = os.path.join(OUTREACH_DIR, slug)

        if slug in HTML_PROSPECTS and self.path.strip("/").split("?")[0] != "pdf":
            html_path = os.path.join(prospect_dir, "portfolio.html")
            if not os.path.isfile(html_path):
                self.send_error(404, f"No portfolio page found for '{slug}'")
                return
            self.send_file(html_path, "text/html; charset=utf-8", f'{slug}-portfolio.html')
            return

        pdf_path = os.path.join(prospect_dir, "portfolio.pdf")
        if not os.path.isfile(pdf_path):
            self.send_error(404, f"No portfolio PDF found for '{slug}'")
            return
        self.send_file(pdf_path, "application/pdf", f'{slug}-portfolio.pdf')

    def send_file(self, path, content_type, filename):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        if content_type == "application/pdf":
            self.send_header("Content-Disposition", f'inline; filename="{filename}"')
        stat = os.stat(path)
        self.send_header("Content-Length", str(stat.st_size))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        mode = "rb" if content_type == "application/pdf" else "r"
        encoding = None if mode == "rb" else "utf-8"
        with open(path, mode, encoding=encoding) as f:
            data = f.read()
            if isinstance(data, str):
                data = data.encode("utf-8")
            self.wfile.write(data)

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]}")

if __name__ == "__main__":
    PORT = 8000
    with socketserver.TCPServer(("", PORT), ResumeHandler) as httpd:
        print(f"Serving prospect portfolios on :{PORT}")
        print(f"  Subdomain PDF:  northwind.stetson.dev → northwind's PDF")
        print(f"  Subdomain HTML: holiglows.stetson.dev → holiglows's page")
        print(f"  Path:           get-work.exe.xyz/northwind → northwind's PDF")
        httpd.serve_forever()
