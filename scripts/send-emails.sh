#!/usr/bin/env bash
# Convenience script to create email drafts with common workflows.
# 
# Usage:
#   ./scripts/send-emails.sh <prospect> [initial|followup|all|preview]
#
# Examples:
#   ./scripts/send-emails.sh holiglows              # Send first email
#   ./scripts/send-emails.sh holiglows followup     # Send all follow-ups
#   ./scripts/send-emails.sh holiglows all          # Send all
#   ./scripts/send-emails.sh holiglows preview      # Preview all without sending

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROSPECT="${1:?Usage: send-emails.sh <prospect-slug> [initial|followup|all|preview]}"
ACTION="${2:-initial}"

# Check that .env exists
if [[ ! -f "$ROOT/.env" ]]; then
  echo "✗ Missing .env file" >&2
  echo "  Copy from template: cp .env.example .env" >&2
  echo "  Then fill in your Fastmail API credentials" >&2
  echo "  See docs/QUICK-START.md for detailed setup" >&2
  exit 1
fi

# Check that email.md exists for this prospect
EMAIL_FILE="$ROOT/outreach/prospects/$PROSPECT/email.md"
if [[ ! -f "$EMAIL_FILE" ]]; then
  echo "✗ No email.md found for prospect '$PROSPECT'" >&2
  echo "  Expected: $EMAIL_FILE" >&2
  echo "  Create one from: $ROOT/outreach/base/email-template.md" >&2
  exit 1
fi

case "$ACTION" in
  initial|first)
    echo "📧 Creating initial email for $PROSPECT..."
    "$ROOT/scripts/create-email-draft.py" "$PROSPECT" 0
    ;;
  followup|follow-up|follow)
    echo "📧 Creating follow-up emails for $PROSPECT..."
    "$ROOT/scripts/create-email-draft.py" "$PROSPECT" --all | grep -E "Follow-up|✓"
    ;;
  all)
    echo "📧 Creating all emails for $PROSPECT..."
    "$ROOT/scripts/create-email-draft.py" "$PROSPECT" --all
    ;;
  preview|dry-run|dry)
    echo "📧 Previewing what would be sent for $PROSPECT..."
    "$ROOT/scripts/create-email-draft.py" "$PROSPECT" --all --dry-run
    ;;
  *)
    echo "✗ Unknown action: $ACTION" >&2
    echo "  Valid actions: initial, followup, all, preview" >&2
    exit 1
    ;;
esac

echo ""
echo "✓ Done!"
echo "  Open https://www.fastmail.com to review drafts"
