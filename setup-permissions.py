#!/usr/bin/env python3
"""
Phase 2: Rollen & Rechte Konfiguration
"""

import requests
import json
import time

DIRECTUS_URL = "http://localhost:8055"

with open("/tmp/directus_token.txt", "r") as f:
    TOKEN = f.read().strip()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def api_request(method, endpoint, data=None):
    """Helper für API Requests"""
    url = f"{DIRECTUS_URL}{endpoint}"
    if method == "POST":
        response = requests.post(url, headers=HEADERS, json=data)
    elif method == "GET":
        response = requests.get(url, headers=HEADERS)
    elif method == "PATCH":
        response = requests.patch(url, headers=HEADERS, json=data)
    
    return response

def get_or_create_public_role():
    """Hole oder erstelle Public Role"""
    # Versuche existierende Public Role zu finden
    response = api_request("GET", "/roles")
    if response.status_code == 200:
        roles = response.json()["data"]
        for role in roles:
            if role.get("name") == "Public" or role.get("id") is None:
                return role["id"]
    
    # Erstelle Public Role (NULL UUID bedeutet Public)
    # In Directus ist die Public Role die mit id=null
    return None  # null = public role

def create_permission(role_id, collection, action, fields=None, permissions=None):
    """Erstelle Permission für eine Collection"""
    data = {
        "role": role_id,
        "collection": collection,
        "action": action
    }
    
    if fields:
        data["fields"] = fields
    
    if permissions:
        data["permissions"] = permissions
    
    response = api_request("POST", "/permissions", data)
    
    if response.status_code in [200, 204]:
        print(f"  ✅ {action.upper()} permission für {collection}")
        return True
    elif response.status_code == 400 and "already exists" in response.text.lower():
        print(f"  ⚠️  {action.upper()} permission für {collection} existiert bereits")
        return True
    else:
        print(f"  ❌ Fehler: {response.status_code} - {response.text[:150]}")
        return False

print("🚀 Phase 2: Rollen & Rechte Setup\n")

# ============================================================================
# 1. PUBLIC ROLE PERMISSIONS
# ============================================================================

print("📌 Konfiguriere Public Role Permissions")

public_role_id = get_or_create_public_role()
print(f"   Public Role ID: {public_role_id}")

# Projects - nur public sichtbar
create_permission(
    role_id=public_role_id,
    collection="projects",
    action="read",
    fields=["id", "status", "title", "slug", "description", "finished_at", "hero_image"],
    permissions={
        "status": {"_eq": "public"}
    }
)

# Tags - alle lesbar
create_permission(
    role_id=public_role_id,
    collection="tags",
    action="read",
    fields=["*"]
)

# Project Images - nur von public projects
create_permission(
    role_id=public_role_id,
    collection="project_images",
    action="read",
    fields=["*"],
    permissions={
        "project_id": {
            "status": {"_eq": "public"}
        }
    }
)

# Directus Files - lesbar (für Bilder)
create_permission(
    role_id=public_role_id,
    collection="directus_files",
    action="read",
    fields=["*"]
)

# Patterns - KEINE Leserechte für Public
print("  ⚠️  Patterns: Kein Zugriff für Public (wie geplant)")

# ============================================================================
# 2. FRIENDS & FAMILY ROLE
# ============================================================================

print("\n📌 Erstelle Friends & Family Role")

# Erstelle Role
response = api_request("POST", "/roles", {
    "name": "Friends & Family",
    "icon": "group",
    "description": "Eingeloggte Freunde und Familie - Zugriff auf geschützte Anleitungen",
    "admin_access": False,
    "app_access": True
})

if response.status_code in [200, 204]:
    friends_role = response.json()["data"]
    friends_role_id = friends_role["id"]
    print(f"✅ Role erstellt: {friends_role_id}")
elif response.status_code == 400:
    # Role existiert bereits, hole ID
    response = api_request("GET", "/roles")
    roles = response.json()["data"]
    friends_role_id = None
    for role in roles:
        if role.get("name") == "Friends & Family":
            friends_role_id = role["id"]
            break
    print(f"⚠️  Role existiert bereits: {friends_role_id}")
else:
    print(f"❌ Fehler: {response.text[:200]}")
    friends_role_id = None

if friends_role_id:
    # Projects - public und private sichtbar
    create_permission(
        role_id=friends_role_id,
        collection="projects",
        action="read",
        fields=["id", "status", "title", "slug", "description", "finished_at", "hero_image"],
        permissions={
            "status": {"_in": ["public", "private"]}
        }
    )
    
    # Patterns - friends_family und private sichtbar
    create_permission(
        role_id=friends_role_id,
        collection="patterns",
        action="read",
        fields=["*"],
        permissions={
            "visibility": {"_in": ["friends_family", "private"]}
        }
    )
    
    # Tags
    create_permission(
        role_id=friends_role_id,
        collection="tags",
        action="read",
        fields=["*"]
    )
    
    # Project Images
    create_permission(
        role_id=friends_role_id,
        collection="project_images",
        action="read",
        fields=["*"]
    )
    
    # Files
    create_permission(
        role_id=friends_role_id,
        collection="directus_files",
        action="read",
        fields=["*"]
    )

# ============================================================================
# 3. WORKER ROLE & USER
# ============================================================================

print("\n📌 Erstelle Worker Role & User")

# Erstelle Worker Role
response = api_request("POST", "/roles", {
    "name": "Worker",
    "icon": "settings",
    "description": "Service Account für PDF-Indexierung",
    "admin_access": False,
    "app_access": False
})

if response.status_code in [200, 204]:
    worker_role = response.json()["data"]
    worker_role_id = worker_role["id"]
    print(f"✅ Worker Role erstellt: {worker_role_id}")
elif response.status_code == 400:
    response = api_request("GET", "/roles")
    roles = response.json()["data"]
    worker_role_id = None
    for role in roles:
        if role.get("name") == "Worker":
            worker_role_id = role["id"]
            break
    print(f"⚠️  Worker Role existiert bereits: {worker_role_id}")
else:
    print(f"❌ Fehler: {response.text[:200]}")
    worker_role_id = None

if worker_role_id:
    # Patterns - read all
    create_permission(
        role_id=worker_role_id,
        collection="patterns",
        action="read",
        fields=["*"]
    )
    
    # Files - read all
    create_permission(
        role_id=worker_role_id,
        collection="directus_files",
        action="read",
        fields=["*"]
    )
    
    # Erstelle Worker User
    print("\n  📝 Erstelle Worker User")
    response = api_request("POST", "/users", {
        "email": "worker@localhost",
        "password": "worker_password_not_used",
        "role": worker_role_id,
        "first_name": "PDF",
        "last_name": "Worker",
        "status": "active"
    })
    
    if response.status_code in [200, 204]:
        worker_user = response.json()["data"]
        worker_user_id = worker_user["id"]
        print(f"  ✅ Worker User erstellt: {worker_user_id}")
        
        # Erstelle Static Token
        time.sleep(1)
        response = api_request("POST", "/users/" + worker_user_id + "/tokens", {
            "name": "PDF Worker Token"
        })
        
        if response.status_code in [200, 204]:
            print(f"  ⚠️  Static Token erstellt - siehe Directus UI")
        else:
            print(f"  ℹ️  Token muss manuell in Directus UI erstellt werden")
    elif "already exists" in response.text.lower() or response.status_code == 400:
        print(f"  ⚠️  Worker User existiert bereits")
    else:
        print(f"  ❌ Fehler: {response.status_code}")

# ============================================================================
# 4. TEST USER (Friends & Family)
# ============================================================================

if friends_role_id:
    print("\n📌 Erstelle Testnutzer (Friends & Family)")
    
    response = api_request("POST", "/users", {
        "email": "test@familie.de",
        "password": "TestPass123!",
        "role": friends_role_id,
        "first_name": "Test",
        "last_name": "Familie",
        "status": "active"
    })
    
    if response.status_code in [200, 204]:
        print(f"✅ Testnutzer erstellt: test@familie.de / TestPass123!")
    elif response.status_code == 400:
        print(f"⚠️  Testnutzer existiert bereits")
    else:
        print(f"❌ Fehler: {response.status_code}")

print("\n✅ Phase 2 abgeschlossen!")
print("\n📝 Nächste Schritte:")
print("   1. Teste Public API: curl http://localhost:8055/items/projects")
print("   2. Teste Login: http://localhost:8055 (test@familie.de / TestPass123!)")
print("   3. Erstelle Worker Static Token in Directus UI")
print("   4. Speichere Token in .env: WORKER_TOKEN=...")
