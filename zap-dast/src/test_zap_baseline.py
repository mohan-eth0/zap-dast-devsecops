#!/usr/bin/env python3

import time
import sys
from zapv2 import ZAPv2

ZAP_API_KEY = "SECUREKEY123"
ZAP_URL = "http://127.0.0.1:8090"
TARGET = "http://testphp.vulnweb.com"

print("[*] Initializing ZAP baseline client")
zap = ZAPv2(apikey=ZAP_API_KEY, proxies={'http': ZAP_URL, 'https': ZAP_URL})

# Step 1 — Access target (required for passive scan)
print("[*] Accessing target")
zap.urlopen(TARGET)
time.sleep(2)

# Step 2 — Spider only (NO active scan)
print("[*] Starting spider (baseline mode)")
scan_id = zap.spider.scan(TARGET)

while int(zap.spider.status(scan_id)) < 100:
    print(f"Spider progress: {zap.spider.status(scan_id)}%")
    time.sleep(2)

print("[*] Spider completed")

# Step 3 — Wait for passive scan to finish
print("[*] Waiting for passive scan")
while int(zap.pscan.records_to_scan) > 0:
    print(f"Passive scan records remaining: {zap.pscan.records_to_scan}")
    time.sleep(2)

print("[*] Passive scan completed")

# Step 4 — Evaluate alerts (High/Critical only)
alerts = zap.core.alerts(baseurl=TARGET)

high_risk = [
    a for a in alerts
    if a.get("risk") in ("High", "Critical")
]

print(f"Total alerts found: {len(alerts)}")
print(f"High/Critical alerts: {len(high_risk)}")

# Step 5 — Gate decision
if high_risk:
    print("❌ SECURITY GATE FAILED (Baseline)")
    for a in high_risk:
        print(f"- {a['alert']} ({a['risk']})")
    sys.exit(1)
else:
    print("✅ SECURITY GATE PASSED (Baseline)")
    sys.exit(0)
print("[*] Writing reports")

with open("zap-alerts.json", "w") as f:
    f.write(str(alerts))

with open("zap-report.html", "w", encoding="utf-8") as f:
    f.write(zap.core.htmlreport())
