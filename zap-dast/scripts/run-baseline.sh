#!/bin/bash
set -e

# ------------------------------------
# ZAP Baseline Scan Runner
# ------------------------------------
# - Runs healthcheck first
# - Executes baseline scan via Python
# ------------------------------------

# 1️⃣ Pre-flight check
./scripts/zap-healthcheck.sh

# 2️⃣ Run baseline scan
echo "[+] Running ZAP baseline scan"
python3 src/test_zap_baseline.py

echo "[✔] Baseline scan completed"
