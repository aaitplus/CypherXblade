import os, json, sys, base64, hashlib, platform, uuid
from datetime import datetime
from cryptography.fernet import Fernet

LICENSE_FILE = ".license.dat"
SECRET_KEY = hashlib.sha256(b"CxB_INTERNAL_SECRET_2025").digest()
FERNET = Fernet(base64.urlsafe_b64encode(SECRET_KEY))

def machine_id():
    raw = platform.system() + platform.node() + str(uuid.getnode())
    return hashlib.sha256(raw.encode()).hexdigest()

def activate_license():
    print("=== CypherXblade License Activation ===")
    key = input("Enter License Key: ").strip()

    tiers = {
        "AA@CypherXBladeBasic": "basic",
        "AA@CypherXBladeProAA": "pro",
        "AA@CypherXBladeAAEnterprise": "enterprise"
    }

    tier = tiers.get(key)
    if not tier:
        print("❌ Invalid license. Contact developer.")
        sys.exit(1)

    payload = {
        "tier": tier,
        "machine": machine_id(),
        "issued": datetime.now().strftime("%Y-%m-%d")
    }

    token = FERNET.encrypt(json.dumps(payload).encode())

    with open(LICENSE_FILE, "wb") as f:
        f.write(token)

    print(f"✅ License activated ({tier.upper()})")

def check_license():
    if not os.path.exists(LICENSE_FILE):
        return "demo"

    try:
        data = FERNET.decrypt(open(LICENSE_FILE, "rb").read())
        payload = json.loads(data)
    except Exception:
        print("❌ License corrupted")
        return "basic"

    if payload["machine"] != machine_id():
        print("❌ License not valid for this machine")
        return "basic"

    return payload["tier"]
