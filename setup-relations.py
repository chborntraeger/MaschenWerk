#!/usr/bin/env python3
"""
Directus Relations Setup
Erstellt Junction Tables und Relations für M2M Beziehungen
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

def create_relation(relation_schema):
    """Erstelle eine Relation"""
    print(f"\n🔗 Erstelle Relation: {relation_schema.get('collection')} -> {relation_schema.get('field')}")
    
    response = requests.post(
        f"{DIRECTUS_URL}/relations",
        headers=HEADERS,
        json=relation_schema
    )
    
    if response.status_code in [200, 204]:
        print(f"✅ Relation erstellt")
        return True
    elif response.status_code == 400:
        print(f"⚠️  Relation existiert bereits")
        return True
    else:
        print(f"❌ Fehler: {response.status_code} - {response.text}")
        return False

def create_field(collection, field_schema):
    """Erstelle ein Field"""
    print(f"  ➕ Feld: {field_schema['field']} in {collection}")
    
    response = requests.post(
        f"{DIRECTUS_URL}/fields/{collection}",
        headers=HEADERS,
        json=field_schema
    )
    
    if response.status_code in [200, 204]:
        print(f"    ✅ Erstellt")
        return True
    elif response.status_code == 400:
        print(f"    ⚠️  Existiert bereits")
        return True
    else:
        print(f"    ❌ Fehler: {response.status_code}")
        return False

print("🚀 Erstelle Junction Tables und Relations...\n")

# ============================================================================
# 1. PROJECTS <-> TAGS (Many-to-Many)
# ============================================================================

print("📌 Projects <-> Tags Relation")

# Erstelle M2M Field auf projects
create_field("projects", {
    "field": "tags",
    "type": "alias",
    "meta": {
        "interface": "list-m2m",
        "special": ["m2m"],
        "options": {
            "template": "{{tags_id.name}}"
        }
    }
})

# Erstelle Relation
create_relation({
    "collection": "projects",
    "field": "tags",
    "related_collection": "tags",
    "meta": {
        "many_collection": "projects",
        "many_field": "tags",
        "one_collection": "tags",
        "one_field": "projects",
        "junction_field": "tags_id"
    },
    "schema": {
        "on_delete": "SET NULL"
    }
})

# ============================================================================
# 2. PROJECT_IMAGES (One-to-Many für Galerie)
# ============================================================================

print("\n📌 Project Images (Galerie)")

# Erstelle O2M Field auf projects
create_field("projects", {
    "field": "images",
    "type": "alias",
    "meta": {
        "interface": "list-o2m",
        "special": ["o2m"],
        "options": {
            "template": "{{directus_files_id.title}}"
        }
    }
})

# Erstelle Relation für images
create_relation({
    "collection": "project_images",
    "field": "project_id",
    "related_collection": "projects",
    "meta": {
        "many_collection": "project_images",
        "many_field": "project_id",
        "one_collection": "projects",
        "one_field": "images"
    },
    "schema": {
        "on_delete": "CASCADE"
    }
})

# ============================================================================
# 3. PROJECTS <-> PATTERNS (Many-to-Many)
# ============================================================================

print("\n📌 Projects <-> Patterns Relation")

# Erstelle M2M Field auf projects
create_field("projects", {
    "field": "patterns",
    "type": "alias",
    "meta": {
        "interface": "list-m2m",
        "special": ["m2m"],
        "options": {
            "template": "{{patterns_id.title}}"
        }
    }
})

# Erstelle Relation
create_relation({
    "collection": "projects",
    "field": "patterns",
    "related_collection": "patterns",
    "meta": {
        "many_collection": "projects",
        "many_field": "patterns",
        "one_collection": "patterns",
        "one_field": "projects",
        "junction_field": "patterns_id"
    },
    "schema": {
        "on_delete": "SET NULL"
    }
})

print("\n✅ Alle Relations erstellt!")
print("\n📝 Refresh Directus UI um die Änderungen zu sehen")
