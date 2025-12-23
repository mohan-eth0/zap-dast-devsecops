#!/bin/bash
set -e

# ------------------------------------
# ZAP Report Generator
# ------------------------------------

API_KEY="SECUREKEY123"
ZAP_URL="http://127.0.0.1:8090"
OUT_DIR="scans/reports"

# Pre-flight check
./scripts/zap-healthcheck.sh

# Prepare directory
mkdir -p "$OUT_DIR"

# HTML report
echo "[+] Generating HTML report"
curl "$ZAP_URL/OTHER/core/other/htmlreport/?apikey=$API_KEY" \
  -o "$OUT_DIR/zap-report.html"

# PDF report
echo "[+] Generating PDF report"
chromium --headless --disable-gpu \
  --print-to-pdf="$OUT_DIR/zap-report.pdf" \
  "$OUT_DIR/zap-report.html"

# JSON alerts
echo "[+] Exporting alerts JSON"
curl "$ZAP_URL/JSON/core/view/alerts/?apikey=$API_KEY" \
  -o "$OUT_DIR/zap-report.json"

echo "[✔] Reports generated successfully"
