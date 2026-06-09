#!/usr/bin/env python3
"""Create Fastmail draft emails from prospect templates.

Usage:
    ./scripts/create-email-draft.py <prospect-slug> [email-index]

Examples:
    ./scripts/create-email-draft.py holiglows              # Creates first (Initial Email)
    ./scripts/create-email-draft.py holiglows 2            # Creates second (Follow-up 1)
    ./scripts/create-email-draft.py holiglows --all         # Creates all emails
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import NamedTuple

try:
    import requests
except ImportError:
    print("✗ requests library not found. Install with: pip3 install requests", file=sys.stderr)
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("✗ python-dotenv not found. Install with: pip3 install python-dotenv", file=sys.stderr)
    sys.exit(1)


# Load environment
load_dotenv()

# Support both direct token AND exe.dev integration
FASTMAIL_ENDPOINT = os.getenv("FASTMAIL_ENDPOINT", "https://fastmail.int.exe.xyz/jmap/session")
FASTMAIL_ACCOUNT_ID = os.getenv("FASTMAIL_ACCOUNT_ID")

# Legacy: direct token auth (if you want to test without integration)
FASTMAIL_ACCESS_TOKEN = os.getenv("FASTMAIL_ACCESS_TOKEN")

FASTMAIL_MAILBOX_ID = os.getenv("FASTMAIL_MAILBOX_ID", "Drafts")

if not FASTMAIL_ACCOUNT_ID:
    print("✗ Missing FASTMAIL_ACCOUNT_ID. See .env.example for setup instructions.", file=sys.stderr)
    sys.exit(1)

if not FASTMAIL_ENDPOINT and not FASTMAIL_ACCESS_TOKEN:
    print("✗ Missing Fastmail credentials. Configure FASTMAIL_ENDPOINT (integration) or FASTMAIL_ACCESS_TOKEN.", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]


class EmailSection(NamedTuple):
    """Parsed email section (subject + body)."""
    title: str
    recipient: str
    subject: str
    body: str


def parse_email_template(prospect_slug: str) -> list[EmailSection]:
    """Parse email.md template for a prospect.
    
    Returns list of (title, recipient, subject, body) tuples.
    """
    email_file = ROOT / "outreach" / "prospects" / prospect_slug / "email.md"
    
    if not email_file.exists():
        raise FileNotFoundError(
            f"No email.md found for prospect '{prospect_slug}'\n"
            f"Expected: {email_file}\n"
            f"Create one from: {ROOT / 'outreach' / 'base' / 'email-template.md'}"
        )
    
    text = email_file.read_text(encoding="utf-8")
    sections = []
    
    # Split by h2 headers (## Section Title)
    parts = re.split(r"^## ", text, flags=re.MULTILINE)
    
    for part in parts[1:]:  # Skip preamble
        lines = part.strip().split("\n")
        title = lines[0].strip()
        
        # Extract To: and Subject: fields
        to_match = re.search(r"\*\*To:\*\*\s*(.+?)(?:\n|$)", part)
        subject_match = re.search(r"\*\*Subject:\*\*\s*(.+?)(?:\n|$)", part)
        
        if not (to_match and subject_match):
            print(f"⚠ Skipping section '{title}' — missing **To:** or **Subject:** fields", file=sys.stderr)
            continue
        
        recipient = to_match.group(1).strip()
        subject = subject_match.group(1).strip()
        
        # Body is everything after the Subject line
        body_start = part.find(subject_match.group(0)) + len(subject_match.group(0))
        body = part[body_start:].strip()
        
        sections.append(EmailSection(title, recipient, subject, body))
    
    return sections


def substitute_variables(
    text: str,
    prospect_slug: str,
    prospect_name: str,
    contact_name: str | None = None,
    website_url: str | None = None,
    portfolio_url: str | None = None,
    your_name: str = "Stetson",
    your_email: str = "me@stetson.dev",
    your_phone: str = "307-214-5159",
    **kwargs,
) -> str:
    """Substitute template variables in text."""
    vars_dict = {
        "PROSPECT_NAME": prospect_name or prospect_slug.title(),
        "CONTACT_NAME": contact_name or "there",
        "WEBSITE_URL": website_url or "",
        "PORTFOLIO_URL": portfolio_url or f"https://{prospect_slug}.stetson.dev/",
        "YOUR_NAME": your_name,
        "YOUR_EMAIL": your_email,
        "YOUR_PHONE": your_phone,
    }
    
    result = text
    for key, value in vars_dict.items():
        result = result.replace(f"{{{key}}}", value)
    
    return result


def read_prospect_data(prospect_slug: str) -> dict:
    """Extract data from prospect's notes.md."""
    notes_file = ROOT / "outreach" / "prospects" / prospect_slug / "notes.md"
    
    if not notes_file.exists():
        return {}
    
    text = notes_file.read_text(encoding="utf-8")
    data = {}
    
    # Extract title (first h1)
    title_match = re.search(r"^# (.+?)$", text, re.MULTILINE)
    if title_match:
        data["prospect_name"] = title_match.group(1).strip()
    
    # Extract contact info section
    contact_section = re.search(
        r"## Contact info\s*\n(.*?)(?:\n##|$)",
        text,
        re.DOTALL
    )
    if contact_section:
        contact_text = contact_section.group(1)
        
        # Contact person
        contact_person = re.search(
            r"Contact person\s*:\s*(.+?)(?:\n|$)",
            contact_text,
            re.IGNORECASE
        )
        if contact_person:
            data["contact_name"] = contact_person.group(1).strip()
        
        # Email
        email_match = re.search(r"Contact email\s*:\s*(.+?)(?:\n|$)", contact_text, re.IGNORECASE)
        if email_match:
            data["contact_email"] = email_match.group(1).strip()
        
        # Website
        website = re.search(
            r"Website\s*:\s*(.+?)(?:\n|$)|^- .*?(https?://[^\s)]+)",
            contact_text,
            re.IGNORECASE | re.MULTILINE
        )
        if website:
            data["website_url"] = website.group(1).strip() if website.group(1) else website.group(2)
    
    # Look for Prospect URL
    prospect_url = re.search(
        r"\*\*Prospect URL:\*\*\s*(.+?)(?:\n|$)",
        text,
        re.IGNORECASE
    )
    if prospect_url:
        data["portfolio_url"] = prospect_url.group(1).strip()
    
    return data


def create_fastmail_draft(
    email: EmailSection,
    from_email: str,
    variables_dict: dict,
) -> dict:
    """Create a draft in Fastmail via JMAP API."""
    
    # Substitute variables in subject and body
    subject = substitute_variables(email.subject, **variables_dict)
    body = substitute_variables(email.body, **variables_dict)

    # Convert plain text to simple HTML
    html_body = "<html><body>" + "".join(
        f"<p>{line}</p>" if line.strip() else "<br>"
        for line in body.splitlines()
    ) + "</body></html>"
    
    # Get or find the mailbox ID for Drafts
    mailbox_id = find_mailbox_id("Drafts")
    if not mailbox_id:
        raise ValueError("Could not find Drafts mailbox in Fastmail account")
    
    # JMAP API request
    headers = {
        "Content-Type": "application/json",
    }
    
    # If using direct token (not integration), add Authorization header
    if FASTMAIL_ACCESS_TOKEN:
        headers["Authorization"] = f"Bearer {FASTMAIL_ACCESS_TOKEN}"
    
    jmap_request = {
        "using": ["urn:ietf:params:jmap:core", "urn:ietf:params:jmap:mail"],
        "methodCalls": [
            [
                "Email/set",
                {
                    "accountId": FASTMAIL_ACCOUNT_ID,
                    "create": {
                        "draft1": {
                            "mailboxIds": {mailbox_id: True},
                            "keywords": {"$draft": True},
                            "from": [{"email": from_email}],
                            "to": [{"email": variables_dict.get("contact_email", email.recipient)}],
                            "subject": subject,
                            "bodyStructure": {
                                "type": "text/html",
                                "partId": "0",
                            },
                            "bodyValues": {
                                "0": {
                                    "value": html_body,
                                }
                            },
                        }
                    },
                },
                "0",
            ]
        ],
    }
    
    response = requests.post(
        FASTMAIL_ENDPOINT,
        json=jmap_request,
        headers=headers,
        timeout=10,
    )
    
    if response.status_code != 200:
        raise Exception(
            f"Fastmail API error ({response.status_code}):\n{response.text}"
        )
    
    result = response.json()
    
    # Check for errors
    if "methodResponses" in result:
        for method_response in result["methodResponses"]:
            if method_response[0] == "Email/set":
                if "created" in method_response[1]:
                    return method_response[1]["created"]
                elif "notCreated" in method_response[1]:
                    errors = method_response[1]["notCreated"]
                    raise Exception(f"Failed to create email draft: {errors}")
    
    raise Exception(f"Unexpected API response: {result}")


def find_mailbox_id(name: str) -> str | None:
    """Find mailbox ID by name via JMAP."""
    headers = {
        "Content-Type": "application/json",
    }
    
    # If using direct token, add Authorization header
    if FASTMAIL_ACCESS_TOKEN:
        headers["Authorization"] = f"Bearer {FASTMAIL_ACCESS_TOKEN}"
    
    jmap_request = {
        "using": ["urn:ietf:params:jmap:core", "urn:ietf:params:jmap:mail"],
        "methodCalls": [
            [
                "Mailbox/query",
                {
                    "accountId": FASTMAIL_ACCOUNT_ID,
                    "filter": {"name": name},
                },
                "0",
            ]
        ],
    }
    
    response = requests.post(
        FASTMAIL_ENDPOINT,
        json=jmap_request,
        headers=headers,
        timeout=10,
    )
    
    if response.status_code != 200:
        return None
    
    result = response.json()
    
    if "methodResponses" in result:
        for method_response in result["methodResponses"]:
            if method_response[0] == "Mailbox/query":
                ids = method_response[1].get("ids", [])
                if ids:
                    return ids[0]
    
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create Fastmail draft emails from prospect templates"
    )
    parser.add_argument("prospect", help="Prospect slug (folder name)")
    parser.add_argument(
        "index",
        nargs="?",
        type=int,
        default=0,
        help="Email section index (0=first, 1=second, etc). Omit or 0 for first.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Create all email sections from the template",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without posting to Fastmail",
    )
    
    args = parser.parse_args()
    
    prospect_slug = args.prospect
    
    # Read prospect data
    try:
        prospect_data = read_prospect_data(prospect_slug)
    except Exception as e:
        print(f"✗ Error reading prospect data: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Parse email template
    try:
        email_sections = parse_email_template(prospect_slug)
    except FileNotFoundError as e:
        print(f"✗ {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error parsing email template: {e}", file=sys.stderr)
        sys.exit(1)
    
    if not email_sections:
        print(f"✗ No email sections found in {prospect_slug}/email.md", file=sys.stderr)
        sys.exit(1)
    
    # Determine which sections to process
    if args.all:
        sections_to_process = list(enumerate(email_sections))
    else:
        idx = min(args.index, len(email_sections) - 1)
        sections_to_process = [(idx, email_sections[idx])]
    
    # Get sender email
    sender_email = prospect_data.get("sender_email") or "me@stetson.dev"
    
    # Process each section
    for idx, section in sections_to_process:
        print(f"\n📧 {section.title}")
        print(f"   To: {prospect_data.get('contact_email', section.recipient)}")
        print(f"   Subject: {section.subject}")
        
        variables = {
            "prospect_slug": prospect_slug,
            "prospect_name": prospect_data.get("prospect_name", prospect_slug.title()),
            "contact_name": prospect_data.get("contact_name"),
            "contact_email": prospect_data.get("contact_email", section.recipient),
            "website_url": prospect_data.get("website_url"),
            "portfolio_url": prospect_data.get("portfolio_url"),
            "your_name": "Stetson",
            "your_email": sender_email,
            "your_phone": "307-214-5159",
        }
        
        if args.dry_run:
            print("   [DRY RUN - not sent to Fastmail]")
            subject = substitute_variables(section.subject, **variables)
            body = substitute_variables(section.body, **variables)
            print(f"\n--- Subject ---\n{subject}")
            print(f"\n--- Body ---\n{body}")
        else:
            try:
                result = create_fastmail_draft(section, sender_email, variables)
                print(f"   ✓ Draft created in Fastmail")
            except Exception as e:
                print(f"   ✗ Failed: {e}", file=sys.stderr)
                sys.exit(1)


if __name__ == "__main__":
    main()
