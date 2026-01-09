#!/usr/bin/env python3
"""
Erstelle Test-Daten in Directus
"""

import requests

DIRECTUS_URL = "http://localhost:8055"

with open("/tmp/directus_token.txt", "r") as f:
    TOKEN = f.read().strip()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def create_item(collection, data):
    """Erstelle einen Eintrag"""
    response = requests.post(
        f"{DIRECTUS_URL}/items/{collection}",
        headers=HEADERS,
        json=data
    )
    
    if response.status_code in [200, 204]:
        item = response.json()["data"]
        print(f"✅ {collection}: {data.get('name') or data.get('title')}")
        return item
    else:
        print(f"❌ Fehler bei {collection}: {response.status_code}")
        print(f"   {response.text[:200]}")
        return None

print("🚀 Erstelle Test-Daten...\n")

# ============================================================================
# Tags
# ============================================================================

print("📌 Tags")
tags = [
    {"name": "Socken", "slug": "socken"},
    {"name": "Pullover", "slug": "pullover"},
    {"name": "Mütze", "slug": "muetze"},
    {"name": "Schal", "slug": "schal"},
    {"name": "Anfänger", "slug": "anfaenger"},
    {"name": "Fortgeschritten", "slug": "fortgeschritten"},
]

created_tags = []
for tag in tags:
    result = create_item("tags", tag)
    if result:
        created_tags.append(result)

# ============================================================================
# Projects
# ============================================================================

print("\n📌 Projects")
projects = [
    {
        "title": "Meine ersten Socken",
        "slug": "meine-ersten-socken",
        "status": "public",
        "description": "# Mein erstes Sockenprojekt\n\nDas war ein tolles Projekt für Anfänger. Die Socken sind super warm geworden!",
        "finished_at": "2025-12-15",
        "private_notes": "Hatte Probleme mit der Ferse, beim nächsten Mal anders machen."
    },
    {
        "title": "Kuschel-Pullover",
        "slug": "kuschel-pullover",
        "status": "public",
        "description": "Ein gemütlicher oversized Pullover in meiner Lieblingsfarbe grau.",
        "finished_at": "2025-11-20"
    },
    {
        "title": "Wintermütze mit Bommel",
        "slug": "wintermuetze-bommel",
        "status": "public",
        "description": "Perfekt für kalte Tage!",
        "finished_at": "2025-10-05"
    },
    {
        "title": "Work in Progress: Cardigan",
        "slug": "wip-cardigan",
        "status": "draft",
        "description": "Aktuelles Projekt - noch nicht fertig!",
        "private_notes": "Bin bei Reihe 45"
    }
]

created_projects = []
for project in projects:
    result = create_item("projects", project)
    if result:
        created_projects.append(result)

# ============================================================================
# Patterns
# ============================================================================

print("\n📌 Patterns")
patterns = [
    {
        "title": "Basis Socken Anleitung",
        "slug": "basis-socken",
        "visibility": "friends_family",
        "notes": "Mein Lieblings-Sockenmuster. Funktioniert immer!"
    },
    {
        "title": "Raglan-Pullover von oben",
        "slug": "raglan-pullover",
        "visibility": "private",
        "notes": "Komplex aber das Ergebnis lohnt sich"
    }
]

created_patterns = []
for pattern in patterns:
    result = create_item("patterns", pattern)
    if result:
        created_patterns.append(result)

print("\n✅ Test-Daten erstellt!")
print(f"   {len(created_tags)} Tags")
print(f"   {len(created_projects)} Projects")
print(f"   {len(created_patterns)} Patterns")
print("\n📝 Öffne Directus Admin UI: http://localhost:8055")
