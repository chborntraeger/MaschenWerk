#!/usr/bin/env python3
import requests

DIRECTUS_URL = "http://localhost:8055"
with open("/tmp/directus_token.txt") as f:
    TOKEN = f.read().strip()

HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def get_policy_for_role(role_name):
    """Finde Policy ID für Role"""
    # Hole Roles
    r = requests.get(f"{DIRECTUS_URL}/roles", headers=HEADERS)
    roles = r.json()["data"]
    role_id = None
    for role in roles:
        if role["name"] == role_name:
            role_id = role["id"]
            break
    
    if not role_id:
        return None
    
    # Hole Policies
    r = requests.get(f"{DIRECTUS_URL}/policies", headers=HEADERS)
    policies = r.json()["data"]
    
    for policy in policies:
        if role_id in policy.get("roles", []):
            return policy["id"]
    
    # Erstelle neue Policy
    r = requests.post(f"{DIRECTUS_URL}/policies", headers=HEADERS, json={
        "name": f"{role_name} Policy",
        "icon": "group",
        "admin_access": False,
        "app_access": True,
        "roles": [role_id]
    })
    if r.status_code in [200, 204]:
        return r.json()["data"]["id"]
    return None

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
    elif "unique" in r.text.lower():
        print(f"  ⚠️  {coll}.{action} existiert")
    else:
        print(f"  ❌ {coll}.{action}: {r.status_code}")

# ============================================================================
# FRIENDS & FAMILY
# ============================================================================

print("📌 Friends & Family Permissions")
friends_policy = get_policy_for_role("Friends & Family")

if friends_policy:
    print(f"   Policy ID: {friends_policy}")
    
    create_perm(friends_policy, "projects", "read",
        ["id", "status", "title", "slug", "description", "finished_at", "hero_image"],
        {"status": {"_in": ["public", "private"]}})
    
    create_perm(friends_policy, "patterns", "read", ["*"],
        {"visibility": {"_in": ["friends_family", "private"]}})
    
    create_perm(friends_policy, "tags", "read", ["*"], {})
    create_perm(friends_policy, "project_images", "read", ["*"], {})
    create_perm(friends_policy, "directus_files", "read", ["*"], {})
else:
    print("   ❌ Keine Policy gefunden")

# ============================================================================
# WORKER
# ============================================================================

print("\n📌 Worker Permissions")
worker_policy = get_policy_for_role("Worker")

if worker_policy:
    print(f"   Policy ID: {worker_policy}")
    
    create_perm(worker_policy, "patterns", "read", ["*"], {})
    create_perm(worker_policy, "directus_files", "read", ["*"], {})
else:
    print("   ❌ Keine Policy gefunden")

print("\n✅ Alle Permissions konfiguriert!")
print("🧪 Teste: python3 test-api.py")
