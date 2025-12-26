🔐 OWASP ZAP Automated DAST (Authenticated, CI-Ready)

This project provides a locked, reproducible OWASP ZAP DAST automation supporting baseline and full authenticated scans, security gate enforcement, and auditable HTML / JSON / PDF reports.

It is designed to be CI/CD-friendly, easy to understand, and safe to run repeatedly without manual intervention.

🚩 Problem Statement

Manual Dynamic Application Security Testing (DAST) is often:

❌ Inconsistent across environments

❌ Hard to automate reliably in CI/CD

❌ Not enforced with clear pass/fail rules

❌ Difficult to audit after execution

As a result, many teams run security scans but still release applications with known high-risk vulnerabilities, because scan results are not enforced as part of the delivery pipeline.

✅ Solution Overview

This project automates OWASP ZAP to provide a practical, enforceable DAST workflow:

✔ Run baseline and full authenticated DAST scans

✔ Support context creation, authentication, and forced user mode

✔ Enforce a security gate (fail on High / Critical findings)

✔ Generate auditable reports (HTML / JSON / PDF)

✔ Provide a locked, reproducible execution flow

📌 The project is intentionally frozen at a known-good state to ensure predictable and repeatable behavior across runs and environments.

🧠 How It Works (Execution Flow)

At a high level, the automation follows this flow:

Python Scripts
     │
     │  (ZAP Python API – zapv2)
     ▼
HTTP Requests (urllib3 / requests)
     │
     │  REST API
     ▼
OWASP ZAP (Daemon Mode)
     │
     │  Proxy + Scanner
     ▼
Target Web / API Application
     │
     ▼
Alerts → Security Gate → Reports

Step-by-Step Flow

Python virtual environment is activated

ZAP runs in daemon (headless) mode

Python scripts communicate with ZAP via its REST API

Based on scan mode:

Baseline scan performs passive analysis

Full scan performs authenticated crawling and active attacks

All alerts are collected from ZAP

Security gate evaluates risk

Reports are generated

Exit code determines CI/CD pass or fail

📂 Project Structure
zap-tests/
├── README.md
├── requirements.txt
├── env.example
├── scripts/
├── src/
├── scans/
│   └── reports/
├── seeds/
└── zap-env/        # Python virtual environment (ignored in Git)

Folder Responsibilities

scripts/ – Shell entry points for scan workflows

src/ – Python logic controlling ZAP (spider, auth, scans, gating)

seeds/ – API endpoint seeds to improve scan coverage

scans/reports/ – Generated scan artifacts (HTML / JSON / PDF)

zap-env/ – Isolated Python runtime (not part of project logic)

🔍 Scan Modes
1️⃣ Baseline Scan (Passive)

Characteristics

Passive scan only

No active attacks

Fast and safe

Use Cases

Pull requests

Early pipeline validation

Developer feedback

Why it exists
Baseline scans provide early visibility into security issues without risking application stability.

2️⃣ Full Authenticated Scan (Active)

Capabilities

ZAP context creation

Form-based authentication

Authentication verification

Forced user mode

Traditional spider + AJAX spider

Active scan attempts

Security gate enforcement

Use Cases

Main branch validation

Pre-release security testing

Scheduled (nightly/weekly) security jobs

⚠️ Full scans should only be run against test or staging environments.

🔐 Authentication & Context Handling

The full scan supports authenticated DAST, ensuring coverage of protected functionality.

Supported flow:

ZAP context creation

Form-based authentication configuration

Authentication verification via indicators

Forced user mode scanning

Authentication is explicitly verified before scanning to ensure ZAP is operating as an authenticated user, reducing false coverage assumptions.

🚦 Security Gate Logic

A simple, enforceable risk-based security policy is applied:

All alerts are collected from ZAP

Alerts are grouped by severity

Decision logic:

❌ If High or Critical alerts > 0 → FAIL

✅ Otherwise → PASS

Why this policy?

High/Critical findings represent exploitable security risk

Medium/Low issues are tracked but do not block delivery

Aligns with a “no known high-risk vulnerabilities” release policy

This makes security enforceable, not advisory.

📊 Reports Generated

Each full scan produces the following artifacts:

Report Type	Purpose
HTML	Human-readable review for developers and security teams
JSON	Machine-readable format for CI/CD, SOC, or SIEM ingestion
PDF	Audit, compliance, and long-term evidence

Reports are designed to support both engineering workflows and audit requirements.

🔒 Locked & Reproducible Design

This project is intentionally locked to ensure:

Fixed dependency versions

Known-good scan behavior

Predictable results across environments

Safe repeat execution in CI/CD

This avoids “scan drift” caused by uncontrolled updates and makes results trustworthy.

🎯 Why This Matters in CI/CD

This automation enables teams to:

Shift security left

Automatically block risky releases

Standardize DAST execution

Produce audit-ready evidence

Treat security findings as release criteria, not optional output

👤 Author & Learning Journey

M Mohan
Aspiring DevSecOps Engineer | Security Automation Enthusiast

GitHub: https://github.com/mohan-eth0

Project: https://github.com/mohan-eth0/zap-dast-devsecops

This project is part of my DevSecOps learning journey, focused on hands-on experience with:

DAST automation

Authenticated security testing

CI/CD security gate enforcement

Audit-ready security reporting

The goal is learning by building — applying real-world tools and practices to develop practical, production-relevant security automation skills. 🛡️🚀
