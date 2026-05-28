#!/usr/bin/env python3
"""
Serves prospect PDFs based on subdomain.
  northwind.stetson.dev  →  outreach/prospects/northwind/portfolio.pdf
  Also handles get-work.exe.xyz/northwind as a fallback.
"""
import http.server
import os
import socketserver

OUTREACH_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outreach", "prospects")

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
                    pdf = os.path.join(OUTREACH_DIR, d, "portfolio.pdf")
                    if os.path.isfile(pdf):
                        prospects.append(d)
            html = "<html><body><h1>Resumes</h1><ul>"
            for p in prospects:
                html += f'<li><a href="/{p}">{p}</a></li>'
            html += "</ul></body></html>"
            self.wfile.write(html.encode())
            return

        pdf_path = os.path.join(OUTREACH_DIR, slug, "portfolio.pdf")
        if not os.path.isfile(pdf_path):
            self.send_error(404, f"No resume found for '{slug}'")
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/pdf")
        self.send_header("Content-Disposition", f'inline; filename="{slug}-portfolio.pdf"')
        stat = os.stat(pdf_path)
        self.send_header("Content-Length", str(stat.st_size))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        with open(pdf_path, "rb") as f:
            self.wfile.write(f.read())

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]}")

if __name__ == "__main__":
    PORT = 8000
    with socketserver.TCPServer(("", PORT), ResumeHandler) as httpd:
        print(f"Serving resumes on :{PORT}")
        print(f"  Subdomain: northwind.stetson.dev → northwind's PDF")
        print(f"  Path:      get-work.exe.xyz/northwind → northwind's PDF")
        httpd.serve_forever()
