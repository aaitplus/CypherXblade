# ☠️ CypherXblade — Special Instructions & Ethics Guide

This document must live **inside the CypherXblade tool folder**.
It defines **what the tool is for**, **what it can realistically find**, **how those findings map to real bug bounty payouts**, and **why automation alone never wins bounties**.

---

## 1️⃣ BY SECURITY CONTEXT (READ FIRST)

### 🟢 White‑Hat (Intended Use — LEGAL)
**Who:** Bug bounty hunters, authorized pentesters, internal security teams

**Allowed Activities:**
- Asset discovery (subdomains, live hosts)
- Vulnerability discovery (misconfigurations, IDOR candidates, exposed endpoints)
- Authenticated testing **only with accounts you own**
- Evidence collection & reporting

**Status:** ✅ Legal, encouraged, rewarded

---

### 🔵 Blue‑Team (Defensive Security)
**Who:** SOC teams, security engineers

**Use Cases:**
- Attack surface monitoring
- Regression testing after fixes
- Finding forgotten endpoints

**Status:** ✅ Legal

---

### 🔴 Red‑Team (AUTHORIZED ONLY)
**Who:** Contracted adversary simulation teams

**Use Cases:**
- Recon phase
- Weak authorization discovery
- Mapping access control gaps

**Note:** Exploitation and chaining must be **manual**.

**Status:** ✅ Legal *only with written authorization*

---

### 🟡 Grey‑Hat (NOT RECOMMENDED)
**Who:** Researchers without explicit permission

**Reality:**
- Even read‑only scanning can be illegal
- High ban and legal risk

**Status:** ⚠️ Risky, discouraged

---

### ⚫ Black‑Hat / Hacktivist
**Intent:** Crime, disruption, political activity

**CypherXblade Suitability:** ❌ Not designed, not supported

**Status:** ❌ Illegal

---

## 2️⃣ WHAT CypherXblade REALISTICALLY FINDS

CypherXblade is a **discovery + validation assistant**, not an exploit framework.

### 🔍 Vulnerability Classes It Finds Well

| Category | Examples | Automation Strength |
|---|---|---|
| Misconfiguration | Exposed panels, debug modes | ⭐⭐⭐⭐ |
| IDOR Candidates | `/api/user?id=123` | ⭐⭐⭐⭐ |
| CVEs | Known vulnerable components | ⭐⭐⭐ |
| Exposure | `.env`, backups, logs | ⭐⭐⭐⭐ |
| Weak Auth Checks | Missing object‑level auth | ⭐⭐⭐ |
| Reflected XSS (basic) | Unsanitized params | ⭐⭐ |

### ❌ What It Does NOT Reliably Find
- Business logic flaws
- Auth bypass chains
- Privilege escalation chains
- Race conditions
- Complex stored XSS

These require **human reasoning**.

---

## 3️⃣ FEATURE → REAL BUG BOUNTY PAYOUT MAP

> Payouts vary by program. Values below are **typical ranges** seen on HackerOne/Bugcrowd.

### 🧠 Recon & Discovery
| Feature | Typical Bug | Payout Range |
|---|---|---|
| Subdomain discovery | Forgotten admin panel | $100 – $1,000 |
| Live host detection | Exposed staging app | $100 – $500 |

### 🔐 Authorization & IDOR
| Feature | Typical Bug | Payout Range |
|---|---|---|
| IDOR candidate detection | Access other user data | $500 – $5,000 |
| Auth‑based testing | Modify another user object | $1,000 – $10,000 |

### 🧪 Vulnerability Scanning
| Feature | Typical Bug | Payout Range |
|---|---|---|
| Nuclei CVEs | Known RCE / XSS | $250 – $3,000 |
| Misconfig templates | Open dashboards | $200 – $2,000 |

### 📸 Evidence & Reporting
| Feature | Why It Matters | Effect on Payout |
|---|---|---|
| Screenshots | Proof reduces disputes | ⬆ Higher acceptance |
| Severity scoring | Clear prioritization | ⬆ Faster triage |
| AI report drafts | Clear writing | ⬆ Less rejection |

---

## 4️⃣ WHY AUTOMATION ALONE NEVER WINS BOUNTIES

### ❌ Automation Problems
- Finds **duplicates**
- Misses **context**
- Can’t reason about intent
- Can’t chain bugs
- Often violates scope if misused

> Most scanner‑only reports are marked **"Informative" or "Duplicate"**.

---

### ✅ Where Automation HELPS
Automation is a **multiplier**, not a replacement.

Correct workflow:
```
Automation → Narrow scope → Manual testing → Exploit reasoning → High‑quality report
```

CypherXblade does:
- Find doors
- Reduce noise
- Save time

**YOU** must:
- Open the door
- Walk through carefully
- Prove impact

---

## 5️⃣ SUCCESS PATTERN (REALITY)

High‑earning hunters:
- Use automation for 20–30% of work
- Spend 70–80% on manual analysis
- Report fewer but higher‑impact bugs

Low‑earning hunters:
- Run scanners all day
- Submit raw output
- Get duplicates/rejections

---

## 6️⃣ RULES FOR USING CypherXblade (NON‑NEGOTIABLE)

- ✔ Scan **only in‑scope assets**
- ✔ Use **accounts you own** for auth testing
- ✔ Manually verify every finding
- ❌ No brute force
- ❌ No auth bypass attempts
- ❌ No automated submissions

---

## ☠️ FINAL WORD

CypherXblade is a **professional research framework**.

It rewards:
- Skill
- Patience
- Ethics

It punishes:
- Laziness
- Noise
- Unauthorized use

> **Automation finds opportunities. Humans earn bounties.**

— CypherXblade

