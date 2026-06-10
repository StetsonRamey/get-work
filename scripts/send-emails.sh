#!/usr/bin/env bash
# Convenience script to create email drafts with common workflows.
# 
# Usage:
#   ./scripts/send-emails.sh <prospect> [variant-1|variant-2|all|preview]
#
# Examples:
#   ./scripts/send-emails.sh holiglows              # Create variant 1
#   ./scripts/send-emails.sh holiglows variant-2    # Create variant 2
#   ./scripts/send-emails.sh holiglows all          # Create both variants
#   ./scripts/send-emails.sh holiglows preview      # Preview both variants without creating drafts

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROSPECT="${1:?Usage: send-emails.sh <prospect-slug> [variant-1|variant-2|all|preview]}"
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
  initial|first|variant-1|variant1|v1|1)
    echo "📧 Creating email variant 1 for $PROSPECT..."
    "$ROOT/scripts/create-email-draft.py" "$PROSPECT" --variant 1
    ;;
  variant-2|variant2|v2|2)
    echo "📧 Creating email variant 2 for $PROSPECT..."
    "$ROOT/scripts/create-email-draft.py" "$PROSPECT" --variant 2
    ;;
  all)
    echo "📧 Creating both email variants for $PROSPECT..."
    "$ROOT/scripts/create-email-draft.py" "$PROSPECT" --all
    ;;
  preview|dry-run|dry)
    echo "📧 Previewing what would be sent for $PROSPECT..."
    "$ROOT/scripts/create-email-draft.py" "$PROSPECT" --all --dry-run
    ;;
  *)
    echo "✗ Unknown action: $ACTION" >&2
    echo "  Valid actions: variant-1, variant-2, all, preview" >&2
    exit 1
    ;;
esac

echo ""
echo "✓ Done!"
echo "  Open https://www.fastmail.com to review drafts"
