# ☠️ CypherXblade

**Automated Web Vulnerability Analysis & Bug Bounty Assistant**
*By CypherXblade*

---

## ⚠️ IMPORTANT DISCLAIMER

CypherXblade is a **security research framework** designed **ONLY** for:

* Authorized bug bounty programs
* Written penetration testing engagements
* Internal / defensive security testing

❌ Any unauthorized use is illegal and strictly discouraged.

---

## 🧠 What Is CypherXblade?

CypherXblade is a **professional‑grade automation assistant** that helps security researchers:

* Discover attack surface
* Identify real vulnerability candidates
* Validate authorization issues safely
* Collect evidence
* Produce high‑quality reports

It is **NOT** an exploit framework.
It does **NOT** auto‑hack targets.

> Automation finds doors. Humans earn bounties.

---

## ✨ Core Features

### 🔍 Recon & Discovery

* Subdomain discovery (Subfinder)
* Live host detection (Httpx)
* Multi‑domain batch scanning
* Scope‑aware target validation

### 🧪 Vulnerability Detection

* Nuclei scanning (custom + official templates)
* Severity‑gated scans (Low → Critical)
* Misconfiguration discovery
* Exposure checks (.env, backups, debug panels)

### 🔐 IDOR & Authorization Testing

* IDOR candidate discovery
* Auth‑based IDOR replay module
* Login form automation (owned accounts only)
* Object ID fuzzing (safe limits)

### 🧠 AI‑Assisted Intelligence

* AI Advisor for testing‑level suggestions
* Severity scoring engine
* AI‑assisted report drafting
* Duplicate/noise reduction logic

### 📸 Evidence Collection

* Screenshot capture (Pyppeteer)
* HTTP request/response logging
* Timestamped proof artifacts

### 📊 Reporting & Export

* Text & structured reports
* Burp‑compatible export
* Resume‑scan support
* GPT‑based report enhancement (offline‑safe design)

### 🛡️ Safety & OPSEC

* Scope validation checklist
* Pre‑scan legal warning (mandatory acceptance)
* Training mode vs Production mode
* Rate‑aware scanning
* Platform capability warnings

### 🔄 Installer & Platform Support

* Auto‑installer with version checks
* Detects existing tools
* Updates only if outdated
* Dry‑run install mode
* Offline installer support

Supported Platforms:

* Linux
* Kali / Parrot
* Arch
* macOS
* Windows (WSL)
* Termux (Android)

---

## 🎚️ Testing Levels

| Level | Name   | Description                                |
| ----- | ------ | ------------------------------------------ |
| 1     | Low    | Passive & safe discovery (default)         |
| 2     | Medium | Deeper scanning (requires scope allowance) |
| 3     | High   | Maximum depth (written approval required)  |

⚠️ Levels must be **manually increased** by the user.

### 🤖 AI Advisor

The AI Advisor:

* Analyzes scan quality signals
* Suggests when it may be safe to increase depth
* **Never** auto‑changes levels

---

## 🚀 Installation

### Option 1: Auto‑Installer (Recommended)

```
python CypherXblade.py
→ Install / Update Requirements
```

### Tools Installed Automatically

* Go
* Subfinder
* Httpx
* Nuclei
* Chromium
* Python dependencies

Supports:

* Online install
* Offline mode
* Dry‑run preview

---

## ▶️ Basic Usage

```
python CypherXblade.py
```

### Typical Workflow

1. Accept legal warning
2. Validate scope
3. Choose mode (Training / Production)
4. Select testing level
5. (Optional) Run AI Advisor
6. Start scan
7. Manually verify findings
8. Generate report

---

## 🧠 What Bugs Can It Find?

### ✅ Realistic Finds

* IDOR (including critical cases)
* Exposed admin panels
* Known CVEs
* Misconfigurations
* Sensitive file exposure

### ❌ Not Fully Automatable

* Business logic flaws
* Auth bypass chains
* Race conditions
* Payment logic bugs

These require **human reasoning**.

---

## 💰 Bug Bounty Reality

CypherXblade helps you:

* Reduce noise
* Find real leads
* Save time

It does **not**:

* Guarantee payouts
* Replace manual testing
* Bypass scope rules

High payouts come from:

```
Automation → Manual reasoning → Clear impact → Clean report
```

---

## 🔐 OPSEC & Ethics

* Scan only in‑scope assets
* Use only accounts you own
* Verify every finding manually
* Never submit raw scanner output

Violating these rules may result in:

* Account bans
* Legal action
* Permanent reputation damage

---

## ☠️ Final Note

CypherXblade is designed for **serious security researchers**.

If you use it responsibly, it will:

* Make you faster
* Make you cleaner
* Make you more effective

If you misuse it, it will expose you.

**Stay ethical. Stay sharp.**

— CypherXblade
