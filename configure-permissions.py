#!/usr/bin/env python3
"""
Konfiguriere Permissions über API (korrektes Format)
"""

import requests
import json

DIRECTUS_URL = "http://localhost:8055"

with open("/tmp/directus_token.txt", "r") as f:
    TOKEN = f.read().strip()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def get_policy_id_for_role(role_name):
    """Hole Policy ID für eine Rolle"""
    response = requests.get(f"{DIRECTUS_URL}/policies", headers=HEADERS)
    if response.status_code == 200:
        policies = response.json()["data"]
        for policy in policies:
            # Policy name entspricht oft der Rolle
            if policy.get("name") == role_name:
                return policy["id"]
    return None

def get_role_id(role_name):
    """Hole Role ID"""
    response = requests.get(f"{DIRECTUS_URL}/roles", headers=HEADERS)
    if response.status_code == 200:
        roles = response.json()["data"]
        for role in roles:
            if role.get("name") == role_name:
                return role["id"]
    return None

def create_permission(policy_id, collection, action, fields=None, permissions_filter=None):
    """Erstelle Permission"""
    data = {
        "policy": policy_id,
        "collection": collection,
        "action": action,
        "fields": fields or ["*"],
        "permissions": permissions_filter or {},
        "validation": None,
        "presets": None
    }
    
    response = requests.post(f"{DIRECTUS_URL}/permissions", headers=HEADERS, json=data)
    
    if response.status_code in [200, 204]:
        print(f"  ✅ {collection}.{action}")
        return True
    elif response.status_code == 400:
        if "already exists" in response.text.lower() or "unique" in response.text.lower():
            print(f"  ⚠️  {collection}.{action} existiert bereits")
            return True
        else:
            print(f"  ❌ {collection}.{action}: {response.text[:150]}")
            return False
    else:
        print(f"  ❌ {collection}.{action}: {response.status_code}")
        return False

print("🚀 Konfiguriere Permissions korrekt\n")

# ============================================================================
# PUBLIC PERMISSIONS (policy = null)
# ============================================================================

print("📌 Public Permissions (policy=null)")

public_permissions = [
    {
        "collection": "projects",
        "action": "read",
        "fields": ["id", "status", "title", "slug", "description", "finished_at", "hero_image"],
        "filter": {"status": {"_eq": "public"}}
    },
    {
        "collection": "tags",
        "action": "read",
        "fields": ["*"],
        "filter": {}
    },
    {
        "collection": "project_images",
        "action": "read",
        "fields": ["*"],
        "filter": {"project_id": {"status": {"_eq": "public"}}}
    },
    {
        "collection": "directus_files",
        "action": "read",
        "fields": ["*"],
        "filter": {}
    }
]

for perm in public_permissions:
    create_permission(
        policy_id=None,  # null = Public
        collection=perm["collection"],
        action=perm["action"],
        fields=perm["fields"],
        permissions_filter=perm["filter"]
    )

# ============================================================================
# FRIENDS & FAMILY PERMISSIONS
# ============================================================================

print("\n📌 Friends & Family Permissions")

friends_role_id = get_role_id("Friends & Family")
if not friends_role_id:
    print("❌ Friends & Family Role nicht gefunden!")
else:
    print(f"   Role ID: {friends_role_id}")
    
    # Erstelle oder finde Policy für diese Rolle
    response = requests.get(f"{DIRECTUS_URL}/policies", headers=HEADERS)
    policies = response.json()["data"] if response.status_code == 200 else []
    
    friends_policy_id = None
    for policy in policies:
        # Policies sind mit Rollen verknüpft
        if policy.get("roles") and friends_role_id in [r if isinstance(r, str) else r.get("id") for r in policy.get("roles", [])]:
            friends_policy_id = policy["id"]
            break
    
    if not friends_policy_id:
        # Erstelle Policy für diese Rolle
        response = requests.post(
            f"{DIRECTUS_URL}/policies",
            headers=HEADERS,
            json={
                "name": "Friends & Family Policy",
                "icon": "group",
                "description": "Policy for Friends & Family role",
                "admin_access": False,
                "app_access": True,
                "roles": [friends_role_id]
            }
        )
        if response.status_code in [200, 204]:
            friends_policy_id = response.json()["data"]["id"]
            print(f"   ✅ Policy erstellt: {friends_policy_id}")
        else:
            print(f"   ❌ Policy Fehler: {response.text[:200]}")
    else:
        print(f"   Policy ID: {friends_policy_id}")
    
    if friends_policy_id:
        friends_permissions = [
            {
                "collection": "projects",
                "action": "read",
                "fields": ["id", "status", "title", "slug", "description", "finished_at", "hero_image"],
                "filter": {"status": {"_in": ["public", "private"]}}
            },
            {
                "collection": "patterns",
                "action": "read",
                "fields": ["*"],
                "filter": {"visibility": {"_in": ["friends_family", "private"]}}
            },
            {
                "collection": "tags",
                "action": "read",
                "fields": ["*"],
                "filter": {}
            },
            {
                "collection": "project_images",
                "action": "read",
                "fields": ["*"],
                "filter": {}
            },
            {
                "collection": "directus_files",
                "action": "read",
                "fields": ["*"],
                "filter": {}
            }
        ]
        
        for perm in friends_permissions:
            create_permission(
                policy_id=friends_policy_id,
                collection=perm["collection"],
                action=perm["action"],
                fields=perm["fields"],
                permissions_filter=perm["filter"]
            )

# ============================================================================
# WORKER PERMISSIONS
# ============================================================================

print("\n📌 Worker Permissions")

worker_role_id = get_role_id("Worker")
if not worker_role_id:
    print("❌ Worker Role nicht gefunden!")
else:
    print(f"   Role ID: {worker_role_id}")
    
    # Finde oder erstelle Policy
    response = requests.get(f"{DIRECTUS_URL}/policies", headers=HEADERS)
    policies = response.json()["data"] if response.status_code == 200 else []
    
    worker_policy_id = None
    for policy in policies:
        if policy.get("roles") and worker_role_id in [r if isinstance(r, str) else r.get("id") for r in policy.get("roles", [])]:
            worker_policy_id = policy["id"]
            break
    
    if not worker_policy_id:
        response = requests.post(
            f"{DIRECTUS_URL}/policies",
            headers=HEADERS,
            json={
                "name": "Worker Policy",
                "icon": "settings",
                "description": "Policy for PDF Worker",
                "admin_access": False,
                "app_access": False,
                "roles": [worker_role_id]
            }
        )
        if response.status_code in [200, 204]:
            worker_policy_id = response.json()["data"]["id"]
            print(f"   ✅ Policy erstellt: {worker_policy_id}")
        else:
            print(f"   ❌ Policy Fehler: {response.text[:200]}")
    else:
        print(f"   Policy ID: {worker_policy_id}")
    
    if worker_policy_id:
        worker_permissions = [
            {
                "collection": "patterns",
                "action": "read",
                "fields": ["*"],
                "filter": {}
            },
            {
                "collection": "directus_files",
                "action": "read",
                "fields": ["*"],
                "filter": {}
            }
        ]
        
        for perm in worker_permissions:
            create_permission(
                policy_id=worker_policy_id,
                collection=perm["collection"],
                action=perm["action"],
                fields=perm["fields"],
                permissions_filter=perm["filter"]
            )

print("\n✅ Permissions konfiguriert!")
print("\n🧪 Teste jetzt mit: python3 test-api.py")
