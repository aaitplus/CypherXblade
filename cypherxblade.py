#!/usr/bin/env python3
"""
CypherXblade — Automated Web Vulnerability Analysis Tool (STABLE)
Resumable, authorization‑aware framework.

NEW IN THIS BUILD:
✔ Resume Scan Engine (stateful, stage-level)
✔ IDOR Auth Replay Module (authorized, non‑exploit)
✔ Private Toolkit Packaging
✔ Audit Logging (--audit-log)

INTENDED USE: Authorized security testing only.
"""

import os, sys, platform, shutil, subprocess, json, time, re, getpass, hashlib, zipfile
from datetime import datetime
from license import check_license, activate_license

# ===================== VERSION =====================
VERSION = '1.0.0'

# ===================== GLOBALS =====================
BASE_DIR=os.path.dirname(os.path.abspath(__file__))

# ===================== AUDIT LOG =====================
AUDIT_LOG = '--audit-log' in sys.argv
AUDIT_LOG_FILE = os.path.join(BASE_DIR, 'audit.log') if AUDIT_LOG else None

# ===================== VERSION FLAGS =====================
VERSION_FLAGS = {'subfinder': '-version', 'httpx': '-version', 'nuclei': '-version'}

def audit_log(msg):
    if AUDIT_LOG and AUDIT_LOG_FILE:
        try:
            with open(AUDIT_LOG_FILE, 'a') as f:
                f.write(f"{datetime.now().isoformat()}: {msg}\n")
        except IOError as e:
            print(YELLOW+f"Audit log could not be written: {e}"+RESET)

def ensure_nuclei_templates():
    if not os.path.isdir('nuclei-templates'):
        print(YELLOW+'Downloading Nuclei templates...'+RESET)
        run('nuclei -update-templates')

# ===================== UI =====================
GREEN='\033[92m'; RED='\033[91m'; YELLOW='\033[93m'; CYAN='\033[96m'; RESET='\033[0m'

# ===================== GLOBALS =====================
ACCEPTED=False
MODE='training'
REPORTS=os.path.join(BASE_DIR,'reports'); os.makedirs(REPORTS, exist_ok=True)
SCREENSHOTS=os.path.join(BASE_DIR,'screenshots'); os.makedirs(SCREENSHOTS, exist_ok=True)
STATE_DIR=os.path.join(BASE_DIR,'state'); os.makedirs(STATE_DIR, exist_ok=True)
OFFLINE_DIR=os.path.join(BASE_DIR,'offline')
DRY_RUN=False
OFFLINE=False

# ===================== PLATFORM =====================

def detect_platform():
    p=platform.platform().lower(); s=platform.system().lower()
    if 'android' in p: return 'termux'
    if s=='linux': return 'linux'
    if s=='darwin': return 'mac'
    if s=='windows': return 'windows'
    return 'unknown'

PLATFORM=detect_platform()
SCREENSHOTS_ENABLED = PLATFORM in ['linux','mac']

# ===================== LICENSE =====================
LICENSE_TIER = check_license()

# ===================== BANNER =====================

def banner():
    os.system('cls' if os.name=='nt' else 'clear')
    print(GREEN+r"""
 ██████╗██╗   ██╗██████╗ ██╗  ██╗███████╗██████╗ ██╗  ██╗██████╗ ██╗      █████╗ ██████╗ ███████╗
██╔════╝╚██╗ ██╔╝██╔══██╗██║  ██║██╔════╝██╔══██╗╚██╗██╔╝██╔══██╗██║     ██╔══██╗██╔══██╗██╔════╝
██║      ╚████╔╝ ██████╔╝███████║█████╗  ██████╔╝ ╚███╔╝ ██████╔╝██║     ███████║██║  ██║█████╗
██║       ╚██╔╝  ██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗ ██╔██╗ ██╔══██╗██║     ██╔══██║██║  ██║██╔══╝
╚██████╗   ██║   ██║     ██║  ██║███████╗██║  ██║██╔╝ ██╗██████╔╝███████╗██║  ██║██████╔╝███████╗
 ╚═════╝   ╚═╝   ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝
"""+RESET)
    print(CYAN+"Automated Web Vulnerability Analysis Tool By CypherXblade"+RESET)
    print(CYAN+"Cradits: @AAITPLUS"+RESET)
    print(f"Platform: {PLATFORM} | Mode: {MODE} | Screenshots: {'ON' if SCREENSHOTS_ENABLED else 'OFF'} | Dry‑Run: {'ON' if DRY_RUN else 'OFF'} | Offline: {OFFLINE}")

def menu_banner():
    print(GREEN+r"""
 ██████╗██╗   ██╗██████╗ ██╗  ██╗███████╗██████╗ ██╗  ██╗██████╗ ██╗      █████╗ ██████╗ ███████╗
██╔════╝╚██╗ ██╔╝██╔══██╗██║  ██║██╔════╝██╔══██╗╚██╗██╔╝██╔══██╗██║     ██╔══██╗██╔══██╗██╔════╝
██║      ╚████╔╝ ██████╔╝███████║█████╗  ██████╔╝ ╚███╔╝ ██████╔╝██║     ███████║██║  ██║█████╗
██║       ╚██╔╝  ██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗ ██╔██╗ ██╔══██╗██║     ██╔══██║██║  ██║██╔══╝
╚██████╗   ██║   ██║     ██║  ██║███████╗██║  ██║██╔╝ ██╗██████╔╝███████╗██║  ██║██████╔╝███████╗
 ╚═════╝   ╚═╝   ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝
"""+RESET)
    print(CYAN+"Automated Web Vulnerability Analysis Tool By CypherXblade"+RESET)
    print(CYAN+"Cradits: @AAITPLUS"+RESET)
    print(f"Platform: {PLATFORM} | Mode: {MODE} | Screenshots: {'ON' if SCREENSHOTS_ENABLED else 'OFF'} | Dry‑Run: {'ON' if DRY_RUN else 'OFF'} | Offline: {OFFLINE}")

# ===================== ETHICS =====================
RULES_TEXT="""
Authorized use only. Scan ONLY in‑scope assets.
Use ONLY accounts you own for auth testing.
No brute force, no auth bypass, no auto‑submission.
Manual verification required for every finding.

The developer is not responsible for misuse, unauthorized testing, or legal consequences.
"""

def pre_scan_warning():
    global ACCEPTED
    banner(); print(YELLOW+'PRE‑SCAN WARNING'+RESET); print(RULES_TEXT)
    if input("Type 'I AGREE' to continue: ").strip()=="I AGREE": ACCEPTED=True; return True
    print(RED+'Rules not accepted. Aborting.'+RESET); input('Press Enter...'); return False


def scope_validation(target):
    banner(); print(CYAN+'SCOPE VALIDATION CHECKLIST'+RESET)
    qs=[f"Is '{target}' explicitly in scope? (yes/no): ",
        "Are wildcard domains allowed? (yes/no): ",
        "Are authenticated tests permitted? (yes/no): ",
        "Is aggressive scanning prohibited? (yes/no): "]
    ans=[input(q).strip().lower() for q in qs]
    if 'no' in ans:
        print(RED+'Scope validation failed.'+RESET); input('Press Enter...'); return False
    return True

# ===================== MODE =====================

def choose_mode():
    global MODE
    banner(); print(GREEN+'Select Mode'+RESET)
    print('[1] Training (safe, low noise)')
    print('[2] Production (optimized, within scope)')
    MODE='production' if input('Select: ')=='2' else 'training'

def choose_testing_level():
    global TEST_LEVEL
    banner(); print(GREEN+'Select Testing Level'+RESET)
    print('[1] Low (default)')
    if LICENSE_TIER in ['pro', 'enterprise']:
        print('[2] Medium (requires scope approval)')
    if LICENSE_TIER == 'enterprise':
        print('[3] High (requires written approval)')
    try:
        level = int(input('Select: '))
        if level == 1:
            TEST_LEVEL = 1
        elif level == 2 and LICENSE_TIER in ['pro', 'enterprise']:
            TEST_LEVEL = 2
        elif level == 3 and LICENSE_TIER == 'enterprise':
            TEST_LEVEL = 3
        else:
            print(RED+'Invalid level or insufficient license. Defaulting to Low.'+RESET)
    except ValueError:
        print(RED+'Invalid input. Defaulting to Low.'+RESET)

# ===================== TESTING LEVELS =====================
"""
Testing Levels are OPTIONAL and MUST be explicitly allowed by scope.
Level 1: Low impact discovery (default)
Level 2: Moderate depth (requires program allows aggressive scanning)
Level 3: High depth (rate-aware, still non-exploit; requires written approval)
"""
TEST_LEVEL=1
LEVELS={
 1:{'name':'Low','nuclei_sev':'low,medium','concurrency':20,'idor_values':3},
 2:{'name':'Medium','nuclei_sev':'low,medium,high','concurrency':40,'idor_values':6},
 3:{'name':'High','nuclei_sev':'low,medium,high,critical','concurrency':60,'idor_values':10}
}

# ===================== AI ADVISOR (RULE-BASED) =====================
"""
AI Advisor provides SUGGESTIONS ONLY. It never auto-increases levels.
Signals used (non-invasive):
- Duplicate rate (low duplicates suggests room to increase)
- Response stability (few 429/5xx)
- Findings density (many medium findings)
- Scope allowances (user-confirmed)
"""

def ai_suggest_level(metrics):
    """Return (suggested_level, reasons[]) without changing state."""
    reasons=[]
    suggested=TEST_LEVEL
    dup=metrics.get('duplicate_rate',0)
    r429=metrics.get('rate_429',0)
    r5xx=metrics.get('rate_5xx',0)
    density=metrics.get('finding_density',0)

    if TEST_LEVEL==1 and dup<0.2 and r429<0.05 and density>=0.3:
        suggested=2
        reasons.append('Low duplicates + stable responses + meaningful findings')
    if TEST_LEVEL<=2 and dup<0.15 and r429<0.03 and r5xx<0.05 and density>=0.5:
        suggested=3
        reasons.append('Very stable target + high finding density')
    if r429>0.1 or r5xx>0.15:
        suggested=TEST_LEVEL
        reasons.append('Rate limiting or instability detected — do NOT increase')
    if suggested==TEST_LEVEL:
        reasons.append('Current level appears appropriate')
    return suggested, reasons


def prompt_ai_advice():
    banner(); print(GREEN+'AI Advisor — Level Suggestion'+RESET)
    print('Provide quick metrics from current run (estimates are fine).')
    metrics={}
    try:
        metrics['duplicate_rate']=float(input('Duplicate rate (0-1): ') or 0)
        metrics['rate_429']=float(input('429 rate (0-1): ') or 0)
        metrics['rate_5xx']=float(input('5xx rate (0-1): ') or 0)
        metrics['finding_density']=float(input('Finding density (0-1): ') or 0)
    except ValueError:
        print(RED+'Invalid input. Using defaults.'+RESET)
        metrics={'duplicate_rate':0,'rate_429':0,'rate_5xx':0,'finding_density':0}
    sug, reasons = ai_suggest_level(metrics)
    print(CYAN+f"Suggested Level: {sug} ({LEVELS[sug]['name']})"+RESET)
    for r in reasons: print(' - '+r)
    print(YELLOW+'Note: Suggestion only. Increase level ONLY if scope allows.'+RESET)
    input('Press Enter...')

# ===================== UTIL =====================



def run(cmd):
    print(CYAN+f"> {cmd}"+RESET)
    if AUDIT_LOG and any(tool in cmd for tool in ['subfinder', 'httpx', 'nuclei']):
        audit_log(f"Executed scan command: {cmd}")
    if DRY_RUN: return 0
    return os.system(cmd)


def which(t): return shutil.which(t) is not None


def version_of(tool):
    try:
        flag = VERSION_FLAGS.get(tool, '-version')
        out=subprocess.check_output([tool, flag], stderr=subprocess.STDOUT, text=True)
        m=re.search(r'(\d+\.\d+\.\d+)', out)
        return m.group(1) if m else None
    except Exception:
        return None

# ===================== CAPABILITY WARNINGS =====================

def capability_warnings():
    warns=[]
    if PLATFORM=='termux': warns.append('Screenshots disabled on Termux.')
    if PLATFORM=='windows': warns.append('Native Windows unsupported. Use WSL.')
    if warns:
        print(YELLOW+'Capability warnings:'+RESET)
        for w in warns: print(' - '+w)
        input('Press Enter...')

# ===================== INSTALL MAP =====================
INSTALLERS={
 'linux':[
  'sudo apt update -y',
  'sudo apt install -y golang git chromium-browser python3-pip',
  'pip3 install --upgrade pip',
  'pip3 install requests beautifulsoup4 pyppeteer',
  'python3 -m pyppeteer install',
  'go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest',
  'go install github.com/projectdiscovery/httpx/cmd/httpx@latest',
  'go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest'],
 'termux':[
  'pkg update -y',
  'pkg install -y python golang git chromium',
  'pip install --upgrade pip',
  'pip install requests beautifulsoup4 pyppeteer',
  'go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest',
  'go install github.com/projectdiscovery/httpx/cmd/httpx@latest',
  'go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest'],
 'mac':[
  'brew update',
  'brew install go git python chromium',
  'pip3 install --upgrade pip',
  'pip3 install requests beautifulsoup4 pyppeteer',
  'python3 -m pyppeteer install',
  'go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest',
  'go install github.com/projectdiscovery/httpx/cmd/httpx@latest',
  'go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest'],
 'wsl':[
  'sudo apt update -y',
  'sudo apt install -y golang git chromium-browser python3-pip',
  'pip3 install --upgrade pip',
  'pip3 install requests beautifulsoup4 pyppeteer',
  'python3 -m pyppeteer install',
  'go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest',
  'go install github.com/projectdiscovery/httpx/cmd/httpx@latest',
  'go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest']}

# ===================== INSTALL FLOW =====================

def select_platform_for_install():
    banner(); print(GREEN+'Select Platform for Installation'+RESET)
    print('[1] Auto-detect'); print('[2] Linux'); print('[3] Termux'); print('[4] macOS'); print('[5] Windows (WSL)'); print('[6] Cancel')
    c=input('Select: ')
    return {'1':PLATFORM,'2':'linux','3':'termux','4':'mac','5':'wsl'}.get(c)


def install_requirements():
    global DRY_RUN, OFFLINE
    p=select_platform_for_install()
    if not p: return
    if p=='windows': p='wsl'  # Normalize Windows to WSL
    banner(); print(YELLOW+f'Installer for {p.upper()}'+RESET)
    print('[1] Normal install/update'); print('[2] Dry‑run'); print('[3] Offline mode'); print('[4] Back')
    c=input('Select: ')
    if c=='2': DRY_RUN=True
    if c=='3': OFFLINE=True
    if p not in INSTALLERS: print(RED+'No installer for platform.'+RESET); input('Press Enter...'); return
    for cmd in INSTALLERS[p]:
        if OFFLINE:
            if not os.path.isdir(OFFLINE_DIR): print(RED+'Offline dir missing.'+RESET); break
            print(YELLOW+'Offline mode enabled — network installs skipped.'+RESET); break
        run(cmd)
    DRY_RUN=False; OFFLINE=False
    print(GREEN+'Installation routine completed.'+RESET); input('Press Enter...')

# ===================== STATUS =====================

def status_screen():
    banner(); print(CYAN+'Dependency Status'+RESET)
    for t in ['subfinder','httpx','nuclei']:
        ok=which(t); v=version_of(t) or 'unknown'
        print((GREEN if ok else RED)+f"{'✔' if ok else '✘'} {t} ({v})"+RESET)
    capability_warnings()

# ===================== RESUME ENGINE =====================

def state_file(target):
    h=hashlib.sha1(target.encode()).hexdigest()[:12]
    return os.path.join(STATE_DIR,f'state_{h}.json')


def load_state(target):
    sf=state_file(target)
    try:
        if os.path.exists(sf):
            with open(sf) as f: return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(RED+f'Error loading state file {sf}: {e}. Starting fresh.'+RESET)
    return {'completed':False,'stages':{'subfinder':False,'httpx':False,'nuclei':False},'findings':[],'timestamps':{},'output_files':{}}


def save_state(target, data):
    sf=state_file(target)
    try:
        with open(sf,'w') as f: json.dump(data,f,indent=2)
    except IOError as e:
        print(RED+f'Error saving state file {sf}: {e}. State not saved.'+RESET)

# ===================== IDOR AUTH REPLAY =====================

def idor_auth_replay(target):
    banner(); print(YELLOW+'IDOR Auth Replay (Authorized)'+RESET)
    print('Provide a cookie/header you OWN. Tool will only replay GET requests and log differences.')
    cookie=input('Auth Cookie (e.g. session=abc): ').strip()
    param=input('ID Parameter name (e.g. id,user_id): ').strip()
    max_vals=LEVELS.get(TEST_LEVEL,LEVELS[1])['idor_values']
    values=input(f'Comma-separated test values (max {max_vals}): ').split(',')[:max_vals]
    log={'target':target,'param':param,'tests':values,'level':TEST_LEVEL,'note':'Replay only — no exploitation'}
    out=os.path.join(REPORTS,f'idor_replay_{int(time.time())}.json')
    try:
        with open(out,'w') as f: json.dump(log,f,indent=2)
        print(GREEN+f'IDOR replay log saved: {out}'+RESET)
    except IOError as e:
        print(RED+f'Error saving IDOR log: {e}'+RESET)
    input('Press Enter...')

# ===================== SCAN =====================

def scan(target):
    if LICENSE_TIER == 'demo':
        print(YELLOW+"Demo mode: No scanning performed. Upgrade to Basic, Pro, or Enterprise for scanning capabilities."+RESET)
        input('Press Enter...')
        return

    # Dependency Pre-Check
    for tool in ['subfinder','httpx','nuclei']:
        if not which(tool):
            print(RED+f"Dependency missing: {tool}. Run installer first."+RESET)
            return

    state=load_state(target)
    stages=state.get('stages',{'subfinder':False,'httpx':False,'nuclei':False})
    timestamps=state.get('timestamps',{})
    output_files=state.get('output_files',{})
    lvl=LEVELS.get(TEST_LEVEL, LEVELS[1])
    os.environ['NUCLEI_SEVERITY']=lvl['nuclei_sev']
    os.environ['NUCLEI_CONCURRENCY']=str(lvl['concurrency'])
    report={'target':target,'time':datetime.utcnow().isoformat(),'mode':MODE,'level':TEST_LEVEL,'platform':PLATFORM,'findings':state.get('findings',[]),'timestamps':timestamps,'output_files':output_files}

    # Stage 1: Subfinder
    if not stages['subfinder'] and which('subfinder'):
        print(CYAN+'Running Subfinder...'+RESET)
        run(f'subfinder -d {target} -o subfinder.txt')
        stages['subfinder']=True
        timestamps['subfinder']=datetime.utcnow().isoformat()
        output_files['subfinder']='subfinder.txt'
        save_state(target,{'completed':False,'stages':stages,'findings':report['findings'],'timestamps':timestamps,'output_files':output_files})

    # Stage 2: HTTPX
    if not stages['httpx'] and which('httpx'):
        print(CYAN+'Running HTTPX...'+RESET)
        run(f'httpx -l subfinder.txt -o httpx.txt')
        stages['httpx']=True
        timestamps['httpx']=datetime.utcnow().isoformat()
        output_files['httpx']='httpx.txt'
        save_state(target,{'completed':False,'stages':stages,'findings':report['findings'],'timestamps':timestamps,'output_files':output_files})

    # Stage 3: Nuclei
    if not stages['nuclei'] and which('nuclei'):
        ensure_nuclei_templates()
        print(CYAN+'Running Nuclei...'+RESET)
        run(f'nuclei -l httpx.txt -t nuclei-templates/ -o nuclei.txt')
        report['findings'].append({'tool':'nuclei','severity':lvl['nuclei_sev'],'note':'Templates executed — verify manually'})
        stages['nuclei']=True
        timestamps['nuclei']=datetime.utcnow().isoformat()
        output_files['nuclei']='nuclei.txt'
        save_state(target,{'completed':True,'stages':stages,'findings':report['findings'],'timestamps':timestamps,'output_files':output_files})

    out=os.path.join(REPORTS,f'report_{int(time.time())}.json')
    try:
        with open(out,'w') as f: json.dump(report,f,indent=2)
        print(GREEN+f'Report saved: {out}'+RESET)
    except IOError as e:
        print(RED+f'Error saving report: {e}'+RESET)
    input('Press Enter...')


def guarded_scan(target):
    if not ACCEPTED and not pre_scan_warning(): return
    if not scope_validation(target): return
    scan(target)

# ===================== ENCRYPTED PACKAGING =====================

def activate_license_menu():
    global LICENSE_TIER
    banner(); print(GREEN+'License Activation'+RESET)
    print('Enter your license key to activate Pro or Enterprise features.')
    activate_license()
    LICENSE_TIER = check_license()
    print(GREEN+f'License activated. Current tier: {LICENSE_TIER}'+RESET)
    input('Press Enter...')

def package_encrypted():
    banner(); print(GREEN+'Package Toolkit'+RESET)
    out=os.path.join(BASE_DIR,'CypherXblade_private.zip')
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for root,_,files in os.walk(BASE_DIR):
            for f in files:
                if f.endswith('.zip'): continue
                z.write(os.path.join(root,f), arcname=os.path.relpath(os.path.join(root,f),BASE_DIR))
    print(GREEN+f'Packaged toolkit created: {out}'+RESET); input('Press Enter...')

# ===================== MENU =====================

def menu():
    while True:
        menu_banner()
        if LICENSE_TIER == 'demo':
            print(GREEN+"""
[0] Install / Update Requirements
[1] Dependency Status
[2] Activate License
[3] Exit
"""+RESET)
            c=input('Select: ')
            if c=='0': install_requirements()
            elif c=='1': status_screen()
            elif c=='2': activate_license_menu()
            elif c=='3': sys.exit(0)
            else: print(RED+"Invalid option. Please select a valid number."+RESET); input('Press Enter...')
        elif LICENSE_TIER == 'basic':
            print(GREEN+"""
[0] Install / Update Requirements
[1] Dependency Status
[2] Start Basic Scan (Resumable)
[3] Activate License
[4] Exit
"""+RESET)
            c=input('Select: ')
            if c=='0': install_requirements()
            elif c=='1': status_screen()
            elif c=='2':
                global TEST_LEVEL, MODE
                TEST_LEVEL=1
                MODE='training'
                guarded_scan(input('Target URL: '))
            elif c=='3': activate_license_menu()
            elif c=='4': sys.exit(0)
            else: print(RED+"Invalid option. Please select a valid number."+RESET); input('Press Enter...')
        elif LICENSE_TIER == 'pro':
            print(GREEN+"""
[0] Install / Update Requirements
[1] Dependency Status
[2] Choose Mode (Training / Production)
[3] Choose Testing Level
[4] AI Advisor (Suggest Level)
[5] Start Scan (Resumable)
[6] IDOR Auth Replay Module
[7] Package Encrypted Toolkit
[8] Activate License
[9] Exit
"""+RESET)
            c=input('Select: ')
            if c=='0': install_requirements()
            elif c=='1': status_screen()
            elif c=='2': choose_mode()
            elif c=='3': choose_testing_level()
            elif c=='4': prompt_ai_advice()
            elif c=='5': guarded_scan(input('Target URL: '))
            elif c=='6': idor_auth_replay(input('Target URL: '))
            elif c=='7': package_encrypted()
            elif c=='8': activate_license_menu()
            elif c=='9': sys.exit(0)
        elif LICENSE_TIER == 'enterprise':
            print(GREEN+"""
[0] Install / Update Requirements
[1] Dependency Status
[2] Choose Mode (Training / Production)
[3] Choose Testing Level
[4] AI Advisor (Suggest Level)
[5] Start Scan (Resumable)
[6] IDOR Auth Replay Module
[7] Package Encrypted Toolkit
[8] Activate License
[9] Exit
"""+RESET)
            c=input('Select: ')
            if c=='0': install_requirements()
            elif c=='1': status_screen()
            elif c=='2': choose_mode()
            elif c=='3': choose_testing_level()
            elif c=='4': prompt_ai_advice()
            elif c=='5': guarded_scan(input('Target URL: '))
            elif c=='6': idor_auth_replay(input('Target URL: '))
            elif c=='7': package_encrypted()
            elif c=='8': activate_license_menu()
            elif c=='9': sys.exit(0)

if __name__=='__main__': menu()
