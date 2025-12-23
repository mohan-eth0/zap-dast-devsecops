#!/bin/bash
set -e

# ------------------------------------
# ZAP Full Scan + Auto Report Runner
# ------------------------------------
# Flow:
# healthcheck → full scan → report
# ------------------------------------

#--
# Load environment variables
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo "❌ .env file not found"
  exit 1
fi


echo "[*] Running pre-flight healthcheck"
./scripts/zap-healthcheck.sh

echo "[+] Running ZAP full scan"
python3 src/test_zap_scan.py

echo "[+] Full scan completed"

echo "[*] Auto-generating reports"
./scripts/run-report.sh

echo "[✔] Full scan + reports completed successfully"
