#!/usr/bin/env python3
"""
Test API Access für verschiedene Rollen
"""

import requests

DIRECTUS_URL = "http://localhost:8055"

print("🧪 Teste API Access\n")

# ============================================================================
# 1. PUBLIC ACCESS (ohne Auth)
# ============================================================================

print("📌 Public Access (ohne Login)")
response = requests.get(f"{DIRECTUS_URL}/items/projects")

if response.status_code == 200:
    projects = response.json().get("data", [])
    print(f"✅ {len(projects)} Projects sichtbar")
    for p in projects[:3]:
        print(f"   - {p.get('title')} ({p.get('status')})")
else:
    print(f"⚠️  Status: {response.status_code}")
    print(f"   {response.text[:200]}")

# Patterns (sollte nicht sichtbar sein)
response = requests.get(f"{DIRECTUS_URL}/items/patterns")
if response.status_code == 200:
    patterns = response.json().get("data", [])
    if len(patterns) == 0:
        print(f"✅ Patterns korrekt geschützt (nicht sichtbar)")
    else:
        print(f"⚠️  {len(patterns)} Patterns sichtbar (sollten nicht sein!)")
else:
    print(f"✅ Patterns korrekt geschützt (Zugriff verweigert)")

# ============================================================================
# 2. FRIENDS & FAMILY ACCESS
# ============================================================================

print("\n📌 Friends & Family Access")

# Login
login_response = requests.post(
    f"{DIRECTUS_URL}/auth/login",
    json={"email": "test@familie.de", "password": "TestPass123!"}
)

if login_response.status_code == 200:
    token = login_response.json()["data"]["access_token"]
    print(f"✅ Login erfolgreich")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Projects
    response = requests.get(f"{DIRECTUS_URL}/items/projects", headers=headers)
    if response.status_code == 200:
        projects = response.json().get("data", [])
        print(f"✅ {len(projects)} Projects sichtbar")
    
    # Patterns
    response = requests.get(f"{DIRECTUS_URL}/items/patterns", headers=headers)
    if response.status_code == 200:
        patterns = response.json().get("data", [])
        print(f"✅ {len(patterns)} Patterns sichtbar")
        for p in patterns:
            print(f"   - {p.get('title')} ({p.get('visibility')})")
    else:
        print(f"⚠️  Patterns Status: {response.status_code}")
else:
    print(f"❌ Login fehlgeschlagen: {login_response.status_code}")

print("\n📝 Permissions müssen noch in Directus UI konfiguriert werden!")
print("   Gehe zu Settings → Access Control → Public/Friends & Family")
print("   und folge der Anleitung in docs/phase-2-permissions.md")
