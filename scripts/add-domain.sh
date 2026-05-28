#!/usr/bin/env bash
# Add a CNAME record in Cloudflare for a prospect subdomain.
# Usage:
#   ./scripts/add-domain.sh digitalminerz
#   ./scripts/add-domain.sh gap-consulting
set -euo pipefail

SLUG="${1:?usage: add-domain.sh <slug>}"
DOMAIN="${SLUG}.stetson.dev"
TARGET="get-work.exe.xyz"
ZONE_ID="956bb55f706c22ad0a94fe05c5f715ce"
CF_API="http://cloudflare.int.exe.xyz/client/v4"

echo "→ Adding CNAME: ${DOMAIN} → ${TARGET}"

# Check if record already exists
EXISTING=$(curl -sL "${CF_API}/zones/${ZONE_ID}/dns_records?type=CNAME&name=${DOMAIN}")
COUNT=$(echo "$EXISTING" | python3 -c "import sys,json; print(json.load(sys.stdin)['result_info']['count'])")

if [ "$COUNT" -gt 0 ]; then
  echo "  ✓ CNAME already exists"
else
  RESULT=$(curl -sL --post301 --post302 -X POST "${CF_API}/zones/${ZONE_ID}/dns_records" \
    -H "Content-Type: application/json" \
    -d '{"type":"CNAME","name":"'"${SLUG}"'","content":"'"${TARGET}"'","ttl":1,"proxied":false}'
  )
  SUCCESS=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['success'])")
  if [ "$SUCCESS" = "True" ]; then
    echo "  ✓ CNAME created"
  else
    echo "  ✗ Failed:" >&2
    echo "$RESULT" | python3 -m json.tool >&2
    exit 1
  fi
fi

echo ""
echo "Now run from your terminal:"
echo "  ssh exe.dev domain add get-work ${DOMAIN}"
