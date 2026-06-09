#!/usr/bin/env python3
"""
Serves prospect portfolios based on subdomain.
  northwind.stetson.dev                 → outreach/prospects/northwind/portfolio.pdf
  coloradochristmaslights.stetson.dev   → outreach/prospects/coloradochristmaslights/portfolio.html
  Also handles get-work.exe.xyz/<slug> as a fallback.
"""
import http.server
import mimetypes
import os
import socketserver
from urllib.parse import urlparse

OUTREACH_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outreach", "prospects")

HTML_PROSPECTS = {
    "coloradochristmaslights",
    "holiglows",
    "icebergchristmaslights",
}


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class ResumeHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        slug = None
        path_slug = False
        request_path = urlparse(self.path).path
        path_parts = [part for part in request_path.strip("/").split("/") if part]
        rest_parts = []

        # Try subdomain first: northwind.stetson.dev
        host = self.headers.get("Host", "")
        parts = host.split(":", 1)[0].split(".")
        if len(parts) >= 3 and parts[-2] in ("stetson",):
            slug = parts[0]
            rest_parts = path_parts
        # Also try: X-Forwarded-Host header (exe.dev proxy)
        fwd_host = self.headers.get("X-Forwarded-Host", "")
        if not slug and fwd_host:
            fwd_parts = fwd_host.split(":", 1)[0].split(".")
            if len(fwd_parts) >= 3 and fwd_parts[-2] in ("stetson",):
                slug = fwd_parts[0]
                rest_parts = path_parts
        # Fallback: path-based, e.g. /northwind
        if not slug and path_parts:
            path = path_parts[0]
            if path != "favicon.ico":
                slug = path
                path_slug = True
                rest_parts = path_parts[1:]

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

        if slug in HTML_PROSPECTS:
            rest_path = "/".join(rest_parts)
            if path_slug and not rest_path and not request_path.endswith("/"):
                self.send_response(301)
                self.send_header("Location", request_path + "/")
                self.end_headers()
                return
            if rest_path in ("", "index.html"):
                html_path = os.path.join(prospect_dir, "portfolio.html")
                if not os.path.isfile(html_path):
                    self.send_error(404, f"No portfolio page found for '{slug}'")
                    return
                self.send_file(html_path, "text/html; charset=utf-8", f'{slug}-portfolio.html')
                return
            if rest_path.startswith("assets/"):
                asset_path = os.path.realpath(os.path.join(prospect_dir, rest_path))
                allowed_roots = [
                    os.path.realpath(os.path.join(prospect_dir, "assets")),
                    os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "outreach", "base", "assets")),
                ]
                if not any(asset_path == root or asset_path.startswith(root + os.sep) for root in allowed_roots):
                    self.send_error(403, "Asset path not allowed")
                    return
                if not os.path.isfile(asset_path):
                    self.send_error(404, f"Asset not found: {rest_path}")
                    return
                content_type = mimetypes.guess_type(asset_path)[0] or "application/octet-stream"
                self.send_file(asset_path, content_type, os.path.basename(asset_path))
                return
            if rest_path != "pdf":
                self.send_error(404, f"No route found for '{slug}/{rest_path}'")
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
        text_types = ("text/html", "text/css", "text/javascript", "application/javascript", "image/svg+xml")
        mode = "r" if content_type.startswith(text_types) else "rb"
        encoding = "utf-8" if mode == "r" else None
        with open(path, mode, encoding=encoding) as f:
            data = f.read()
            if isinstance(data, str):
                data = data.encode("utf-8")
            self.wfile.write(data)

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]}")

if __name__ == "__main__":
    PORT = 8000
    with ReusableTCPServer(("", PORT), ResumeHandler) as httpd:
        print(f"Serving prospect portfolios on :{PORT}")
        print(f"  Subdomain PDF:  northwind.stetson.dev → northwind's PDF")
        print(f"  Subdomain HTML: holiglows.stetson.dev → holiglows's page")
        print(f"  Path:           get-work.exe.xyz/northwind → northwind's PDF")
        httpd.serve_forever()
