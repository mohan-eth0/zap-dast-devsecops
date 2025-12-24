#!/usr/bin/env python3

import os
import sys
import time
from zapv2 import ZAPv2

# ============================================================
# Environment Validation
# ============================================================
REQUIRED_VARS = [
    "ZAP_API_KEY",
    "TARGET_URL",
    "LOGIN_URL",
    "USERNAME",
    "PASSWORD",
    "LOGGED_IN_INDICATOR",
    "LOGGED_OUT_INDICATOR",
]

missing = [v for v in REQUIRED_VARS if not os.getenv(v)]
if missing:
    print(f"❌ Missing required environment variables: {missing}")
    sys.exit(1)

ZAP_API_KEY = os.getenv("ZAP_API_KEY")
TARGET_URL = os.getenv("TARGET_URL")
LOGIN_URL = os.getenv("LOGIN_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
LOGGED_IN_INDICATOR = os.getenv("LOGGED_IN_INDICATOR")
LOGGED_OUT_INDICATOR = os.getenv("LOGGED_OUT_INDICATOR")

# ============================================================
# Constants
# ============================================================
CONTEXT_NAME = "juice-shop-context"
SEED_FILE = "seeds/api_endpoints.txt"

# ============================================================
# ZAP Client
# ============================================================
zap = ZAPv2(
    apikey=ZAP_API_KEY,
    proxies={
        "http": "http://127.0.0.1:8090",
        "https": "http://127.0.0.1:8090",
    },
)

# ============================================================
# Helper Functions
# ============================================================
def seed_api_endpoints():
    print("🌱 Seeding API endpoints...")

    if not os.path.exists(SEED_FILE):
        print("⚠️ No API seed file found, skipping seeding")
        return []

    with open(SEED_FILE) as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        zap.core.access_url(url, followredirects=True)

    print(f"✅ Seeded {len(urls)} API endpoints")
    return urls


def active_scan_seeded_apis(urls):
    for url in urls:
        print(f"[+] Starting active scan for: {url}")

        scan_id = zap.ascan.scan(url)

        # ZAP returns strings, validate scan_id
        if not scan_id or not scan_id.isdigit():
            print(f"[!] Active scan NOT started for {url} (scan_id={scan_id})")
            continue

        while True:
            status = zap.ascan.status(scan_id)

            # ZAP may return 'does_not_exist'
            if not status.isdigit():
                print(f"[!] Scan disappeared for {url} (status={status})")
                break

            if int(status) >= 100:
                break

            time.sleep(5)

        print(f"[✓] Active scan completed for: {url}")


# ============================================================
# Context (Clean State)
# ============================================================
for ctx in zap.context.context_list:
    if ctx == CONTEXT_NAME:
        zap.context.remove_context(ctx)
        print("🧹 Removed existing context")

print("🧠 Creating context...")
context_id = zap.context.new_context(CONTEXT_NAME)

zap.context.include_in_context(CONTEXT_NAME, f"{TARGET_URL}.*")
zap.context.include_in_context(CONTEXT_NAME, f"{TARGET_URL}/rest/.*")

print(f"✅ Context created (ID: {context_id})")

# ============================================================
# Authentication (JSON Based)
# ============================================================
print("🔐 Configuring authentication...")

zap.authentication.set_authentication_method(
    context_id,
    "jsonBasedAuthentication",
    (
        f"loginUrl={LOGIN_URL}"
        f"&loginRequestData={{\"email\":\"{{%username%}}\",\"password\":\"{{%password%}}\"}}"
    ),
)

zap.authentication.set_logged_in_indicator(context_id, LOGGED_IN_INDICATOR)
zap.authentication.set_logged_out_indicator(context_id, LOGGED_OUT_INDICATOR)

print("✅ Authentication configured")

# ============================================================
# User Setup
# ============================================================
for uid in zap.users.users_list(context_id):
    zap.users.remove_user(context_id, uid)

print("👤 Creating user...")
user_id = zap.users.new_user(context_id, "scanner-user")

zap.users.set_authentication_credentials(
    context_id,
    user_id,
    f"username={USERNAME}&password={PASSWORD}",
)
zap.users.set_user_enabled(context_id, user_id, True)

print(f"✅ User created (ID: {user_id})")

# ============================================================
# Forced User Mode
# ============================================================
print("🔒 Enabling forced user mode...")
zap.forcedUser.set_forced_user(context_id, user_id)
zap.forcedUser.set_forced_user_mode_enabled(True)
print("✅ Forced user mode enabled")

# ============================================================
# Session Prime
# ============================================================
print("🌐 Priming authenticated session...")
zap.core.access_url(TARGET_URL, True)
time.sleep(5)

# ============================================================
# Authentication Verification
# ============================================================
print("🧪 Verifying authentication...")
zap.core.access_url(f"{TARGET_URL}/#/profile", True)
time.sleep(3)

html = zap.core.htmlreport()
if "Login" in html:
    print("❌ Authentication FAILED")
    sys.exit(1)

print("✅ Authentication VERIFIED")

# ============================================================
# API Seeding
# ============================================================
seeded_urls = seed_api_endpoints()

# ============================================================
# Authenticated Spider
# ============================================================
print("🕷️ Starting authenticated spider...")
scan_id = zap.spider.scan_as_user(context_id, user_id, TARGET_URL, recurse=True)

while int(zap.spider.status(scan_id)) < 100:
    print(f"Spider progress: {zap.spider.status(scan_id)}%")
    time.sleep(2)

print("✅ Spider completed")

# ============================================================
# AJAX Spider
# ============================================================
print("🧭 Starting AJAX spider...")
zap.ajaxSpider.scan(TARGET_URL)

timeout = time.time() + 120
while zap.ajaxSpider.status == "running":
    if time.time() > timeout:
        break
    print("AJAX spider running...")
    time.sleep(5)

print("✅ AJAX spider completed")

# ============================================================
# Active Scan – API First
# ============================================================
zap.ascan.set_option_attack_policy("Default Policy")
zap.ascan.set_option_handle_anti_csrf_tokens(True)
zap.ascan.set_option_thread_per_host(5)

if seeded_urls:
    active_scan_seeded_apis(seeded_urls)

# ============================================================
# Active Scan – Full Site
# ============================================================
print("🔥 Starting authenticated active scan...")
scan_id = zap.ascan.scan(TARGET_URL)

if not scan_id or not scan_id.isdigit():
    print(f"[!] Authenticated active scan NOT started (scan_id={scan_id})")
else:
    while True:
        status = zap.ascan.status(scan_id)

        if not status.isdigit():
            print(f"[!] Authenticated scan disappeared (status={status})")
            break

        if int(status) >= 100:
            break

        time.sleep(5)

    print("[✓] Authenticated active scan completed")

# ============================================================
# Security Gate
# ============================================================
alerts = zap.core.alerts(baseurl=TARGET_URL)
high_critical = [a for a in alerts if a["risk"] in ("High", "Critical")]

print(f"Total alerts: {len(alerts)}")
print(f"High/Critical alerts: {len(high_critical)}")

if high_critical:
    print("❌ SECURITY GATE FAILED")
    sys.exit(1)

print("✅ SECURITY GATE PASSED")
sys.exit(0)

