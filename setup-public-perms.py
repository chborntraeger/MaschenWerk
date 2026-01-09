#!/usr/bin/env python3
import requests

DIRECTUS_URL = "http://localhost:8055"
with open("/tmp/directus_token.txt") as f:
    TOKEN = f.read().strip()

HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
PUBLIC_POLICY_ID = "abf8a154-5b1c-4a46-ac9c-7300570f4f17"

def create_perm(policy, coll, action, fields, filt):
    data = {
        "policy": policy,
        "collection": coll,
        "action": action,
        "fields": fields,
        "permissions": filt,
        "validation": None,
        "presets": None
    }
    r = requests.post(f"{DIRECTUS_URL}/permissions", headers=HEADERS, json=data)
    if r.status_code in [200, 204]:
        print(f"  ✅ {coll}.{action}")
    elif "unique" in r.text.lower() or "already" in r.text.lower():
        print(f"  ⚠️  {coll}.{action} existiert")
    else:
        print(f"  ❌ {coll}.{action}: {r.status_code}")

print("📌 Public Permissions")
create_perm(PUBLIC_POLICY_ID, "projects", "read",
    ["id", "status", "title", "slug", "description", "finished_at", "hero_image"],
    {"status": {"_eq": "public"}})
create_perm(PUBLIC_POLICY_ID, "tags", "read", ["*"], {})
create_perm(PUBLIC_POLICY_ID, "project_images", "read", ["*"], {})
create_perm(PUBLIC_POLICY_ID, "directus_files", "read", ["*"], {})

print("\n✅ Public Permissions konfiguriert!")
print("🧪 Teste: curl http://localhost:8055/items/projects")
