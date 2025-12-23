#!/usr/bin/env bash
set -e

ZAP_URL=${ZAP_URL:-http://127.0.0.1:8090}

echo "[*] Waiting for ZAP API (this can take ~2 minutes on first start)..."

for i in {1..30}; do
  if curl -s "$ZAP_URL/JSON/core/view/version/" | grep -q version; then
    echo "[✓] ZAP API is reachable"
    exit 0
  fi
  echo "    ZAP not ready yet... ($i/30)"
  sleep 5
done

echo "[✗] ZAP did not become ready in time"
exit 1

