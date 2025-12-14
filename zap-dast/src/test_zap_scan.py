#!/usr/bin/env python3

import time
import sys
from zapv2 import ZAPv2

ZAP_API_KEY = "SECUREKEY123"
ZAP_PROXY = "http://127.0.0.1:8090"

# ⚠️ CHANGE THIS to a real running web app
TARGET = "https://example.com"

print("[*] Initializing ZAP client")

zap = ZAPv2(
    apikey=ZAP_API_KEY,
    proxies={
        "http": ZAP_PROXY,
        "https": ZAP_PROXY,
    },
)

print("[*] Accessing target")
zap.urlopen(TARGET)
time.sleep(2)

print("[*] Starting spider scan")
scan_id = zap.spider.scan(TARGET)

while int(zap.spider.status(scan_id)) < 100:
    print(f"Spider progress: {zap.spider.status(scan_id)}%")
    time.sleep(2)

print("[*] Spider completed")

print("[*] Starting active scan")
scan_id = zap.ascan.scan(TARGET)

while int(zap.ascan.status(scan_id)) < 100:
    print(f"Active scan progress: {zap.ascan.status(scan_id)}%")
    time.sleep(5)

print("[*] Active scan completed")

alerts = zap.core.alerts(baseurl=TARGET)
high = [a for a in alerts if a["risk"] in ("High", "Critical")]

print(f"Total alerts found: {len(alerts)}")
print(f"High/Critical alerts: {len(high)}")

if high:
    print("❌ SECURITY GATE FAILED")
    for a in high:
        print(f"- {a['alert']} | Risk: {a['risk']}")
    sys.exit(1)

print("✅ SECURITY GATE PASSED")
sys.exit(0)
print("[*] Writing reports")

with open("zap-alerts.json", "w") as f:
    f.write(zap.core.alerts(baseurl=TARGET).__str__())

with open("zap-report.html", "wb") as f:
    f.write(
        zap.core.htmlreport().encode("utf-8")
    )
print("[*] Writing reports")

with open("zap-alerts.json", "w") as f:
    f.write(str(alerts))

with open("zap-report.html", "w", encoding="utf-8") as f:
    f.write(zap.core.htmlreport())
