# OWASP ZAP Automated DAST (Authenticated, CI-Ready)

This project provides a **locked, reproducible OWASP ZAP DAST automation** supporting
**baseline and full authenticated scans**, **security gate enforcement**, and
**auditable HTML / JSON / PDF reports**.

It is designed to be **CI/CD friendly**, easy to understand, and safe to run repeatedly.

---

## 🚩 Problem Statement

Manual Dynamic Application Security Testing (DAST) is often:
- Inconsistent across environments
- Hard to automate in CI/CD
- Not enforced with clear pass/fail rules
- Difficult to audit after execution

Many teams run scans but do **not block releases** based on security risk.

---

## ✅ Solution Overview

This project automates OWASP ZAP to:

- Run **baseline** (passive) and **full authenticated** DAST scans
- Support **context, authentication, and forced user mode**
- Enforce a **security gate** (fail on High/Critical findings)
- Generate **auditable reports** (HTML / JSON / PDF)
- Provide a **locked, reproducible execution flow**

The project is intentionally frozen at a known-good state.

---

## 🔍 Scan Modes

### 1️⃣ Baseline Scan
- Passive scan only
- No active attacks
- Fast and safe

**Use cases**
- Pull requests
- Early pipeline validation
- Developer testing

---

### 2️⃣ Full Authenticated Scan
- Context creation
- Form-based authentication
- Forced user mode
- Spider + AJAX spider
- Active scan attempts
- Security gate enforcement

**Use cases**
- Main branch
- Pre-release scans
- Scheduled security jobs

---

## 🔐 Authentication & Context Handling

The full scan supports:
- ZAP context creation
- Form-based authentication
- Auth verification via indicators
- Forced user mode scanning

Authentication is **verified before scanning** to ensure authenticated coverage.

---

## 🚦 Security Gate Logic

A simple, enforceable policy is applied after scans:

- All alerts are collected
- If **High or Critical alerts > 0** → **FAIL**
- Otherwise → **PASS**

This enables a **“no known high-risk vulnerabilities”** policy in CI/CD pipelines.

---

## 📊 Reports Generated

Each full scan generates:

- **HTML report** (human-readable)
- **JSON report** (machine-readable)
- **PDF report** (audit / compliance use)

########
 Author & Learning Journey

M Mohan

Aspiring DevSecOps Engineer | Security Automation Enthusiast

GitHub: https://github.com/mohan-eth0

Project: https://github.com/mohan-eth0/zap-dast-devsecops

This project is part of my DevSecOps learning journey, focused on hands-on experience with security automation and CI/CD-ready DAST workflows.

It demonstrates how OWASP ZAP can be automated to perform security scans, enforce security gates, and generate audit-ready reports within modern pipelines.

The goal is learning by building — applying real-world DevSecOps tools and practices to develop practical security automation skills. 🛡️🚀
