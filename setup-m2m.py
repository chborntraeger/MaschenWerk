#!/usr/bin/env python3
"""
Directus M2M Relations - korrigierte Version
"""

import requests

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
    
    return response

print("🚀 Erstelle M2M Relations korrekt...\n")

# ============================================================================
# 1. PROJECTS_TAGS Junction
# ============================================================================

print("📌 Erstelle projects_tags Junction")

# Erstelle Collection
response = api_request("POST", "/collections", {
    "collection": "projects_tags",
    "meta": {
        "hidden": True,
        "icon": "import_export"
    },
    "schema": {}
})

if response.status_code in [200, 204]:
    print("✅ Junction Collection erstellt")
elif "already exists" in response.text:
    print("⚠️  Junction Collection existiert bereits")

# Erstelle Fields in Junction
fields_data = [
    {
        "collection": "projects_tags",
        "field": "projects_id",
        "type": "uuid",
        "schema": {},
        "meta": {
            "hidden": True
        }
    },
    {
        "collection": "projects_tags",
        "field": "tags_id",
        "type": "integer",
        "schema": {},
        "meta": {
            "hidden": True
        }
    }
]

for field_data in fields_data:
    response = api_request("POST", f"/fields/{field_data['collection']}", field_data)
    if response.status_code in [200, 204]:
        print(f"  ✅ Feld {field_data['field']} erstellt")
    elif response.status_code == 400:
        print(f"  ⚠️  Feld {field_data['field']} existiert bereits")

# Erstelle Relations
relations = [
    {
        "collection": "projects_tags",
        "field": "projects_id",
        "related_collection": "projects",
        "schema": {
            "on_delete": "CASCADE"
        },
        "meta": {
            "one_field": "tags"
        }
    },
    {
        "collection": "projects_tags",
        "field": "tags_id",
        "related_collection": "tags",
        "schema": {
            "on_delete": "CASCADE"
        },
        "meta": {
            "one_field": "projects",
            "junction_field": "projects_id"
        }
    }
]

for relation in relations:
    response = api_request("POST", "/relations", relation)
    if response.status_code in [200, 204]:
        print(f"  ✅ Relation {relation['field']} -> {relation['related_collection']}")
    elif response.status_code == 400:
        print(f"  ⚠️  Relation existiert bereits")
    else:
        print(f"  ❌ Fehler: {response.status_code} - {response.text[:200]}")

# ============================================================================
# 2. PROJECT_IMAGES Junction
# ============================================================================

print("\n📌 Erstelle project_images Collection")

response = api_request("POST", "/collections", {
    "collection": "project_images",
    "meta": {
        "hidden": True,
        "icon": "image"
    },
    "schema": {}
})

if response.status_code in [200, 204]:
    print("✅ Collection erstellt")
elif "already exists" in response.text:
    print("⚠️  Collection existiert bereits")

# Fields
fields = [
    {
        "collection": "project_images",
        "field": "project_id",
        "type": "uuid",
        "schema": {}
    },
    {
        "collection": "project_images",
        "field": "directus_files_id",
        "type": "uuid",
        "schema": {}
    },
    {
        "collection": "project_images",
        "field": "caption",
        "type": "string",
        "schema": {"max_length": 255, "is_nullable": True},
        "meta": {"interface": "input"}
    },
    {
        "collection": "project_images",
        "field": "sort",
        "type": "integer",
        "schema": {"is_nullable": True},
        "meta": {"interface": "input"}
    }
]

for field in fields:
    response = api_request("POST", f"/fields/{field['collection']}", field)
    if response.status_code in [200, 204]:
        print(f"  ✅ Feld {field['field']} erstellt")
    elif response.status_code == 400:
        print(f"  ⚠️  Feld {field['field']} existiert bereits")

# Relations
relations = [
    {
        "collection": "project_images",
        "field": "project_id",
        "related_collection": "projects",
        "schema": {"on_delete": "CASCADE"},
        "meta": {"one_field": "images"}
    },
    {
        "collection": "project_images",
        "field": "directus_files_id",
        "related_collection": "directus_files",
        "schema": {"on_delete": "SET NULL"}
    }
]

for relation in relations:
    response = api_request("POST", "/relations", relation)
    if response.status_code in [200, 204]:
        print(f"  ✅ Relation {relation['field']} -> {relation['related_collection']}")
    elif response.status_code == 400:
        print(f"  ⚠️  Relation existiert bereits")

# ============================================================================
# 3. PROJECTS_PATTERNS Junction
# ============================================================================

print("\n📌 Erstelle projects_patterns Junction")

response = api_request("POST", "/collections", {
    "collection": "projects_patterns",
    "meta": {
        "hidden": True,
        "icon": "import_export"
    },
    "schema": {}
})

if response.status_code in [200, 204]:
    print("✅ Junction Collection erstellt")
elif "already exists" in response.text:
    print("⚠️  Junction Collection existiert bereits")

# Fields
fields = [
    {
        "collection": "projects_patterns",
        "field": "projects_id",
        "type": "uuid",
        "schema": {}
    },
    {
        "collection": "projects_patterns",
        "field": "patterns_id",
        "type": "uuid",
        "schema": {}
    }
]

for field in fields:
    response = api_request("POST", f"/fields/{field['collection']}", field)
    if response.status_code in [200, 204]:
        print(f"  ✅ Feld {field['field']} erstellt")
    elif response.status_code == 400:
        print(f"  ⚠️  Feld {field['field']} existiert bereits")

# Relations
relations = [
    {
        "collection": "projects_patterns",
        "field": "projects_id",
        "related_collection": "projects",
        "schema": {"on_delete": "CASCADE"},
        "meta": {"one_field": "patterns"}
    },
    {
        "collection": "projects_patterns",
        "field": "patterns_id",
        "related_collection": "patterns",
        "schema": {"on_delete": "CASCADE"},
        "meta": {
            "one_field": "projects",
            "junction_field": "projects_id"
        }
    }
]

for relation in relations:
    response = api_request("POST", "/relations", relation)
    if response.status_code in [200, 204]:
        print(f"  ✅ Relation {relation['field']} -> {relation['related_collection']}")
    elif response.status_code == 400:
        print(f"  ⚠️  Relation existiert bereits")
    else:
        print(f"  ❌ Fehler: {response.status_code}")

print("\n✅ Alle M2M Relations erstellt!")
print("📝 Refresh Directus Admin UI (F5)")
