#!/usr/bin/env python3
import requests, json

DIRECTUS_URL = "http://localhost:8055"
with open("/tmp/directus_token.txt") as f:
    TOKEN = f.read().strip()
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

friends_role_id = "76d42f41-37af-4e76-aa92-a163ced9e02a"
worker_role_id = "e7640f3b-012a-4c6c-ac5c-fd5933269daa"

print("📌 Erstelle Policies für Rollen\n")

# Friends & Family Policy
r = requests.post(f"{DIRECTUS_URL}/policies", headers=HEADERS, json={
    "name": "Friends & Family Policy",
    "icon": "group",
    "admin_access": False,
    "app_access": True,
    "roles": [friends_role_id]
})
if r.status_code in [200, 204]:
    friends_policy_id = r.json()["data"]["id"]
    print(f"✅ Friends & Family Policy: {friends_policy_id}")
    
    # Permissions
    def cp(coll, fields, filt):
        requests.post(f"{DIRECTUS_URL}/permissions", headers=HEADERS, json={
            "policy": friends_policy_id, "collection": coll, "action": "read",
            "fields": fields, "permissions": filt, "validation": None, "presets": None
        })
    
    cp("projects", ["id", "status", "title", "slug", "description", "finished_at", "hero_image"],
       {"status": {"_in": ["public", "private"]}})
    cp("patterns", ["*"], {"visibility": {"_in": ["friends_family", "private"]}})
    cp("tags", ["*"], {})
    cp("project_images", ["*"], {})
    cp("directus_files", ["*"], {})
    print("  ✅ Permissions erstellt")
else:
    print(f"❌ Friends: {r.status_code}")

# Worker Policy
r = requests.post(f"{DIRECTUS_URL}/policies", headers=HEADERS, json={
    "name": "Worker Policy",
    "icon": "settings",
    "admin_access": False,
    "app_access": False,
    "roles": [worker_role_id]
})
if r.status_code in [200, 204]:
    worker_policy_id = r.json()["data"]["id"]
    print(f"\n✅ Worker Policy: {worker_policy_id}")
    
    def cp(coll):
        requests.post(f"{DIRECTUS_URL}/permissions", headers=HEADERS, json={
            "policy": worker_policy_id, "collection": coll, "action": "read",
            "fields": ["*"], "permissions": {}, "validation": None, "presets": None
        })
    
    cp("patterns")
    cp("directus_files")
    print("  ✅ Permissions erstellt")
else:
    print(f"❌ Worker: {r.status_code}")

print("\n✅ Fertig! Teste: python3 test-api.py")
