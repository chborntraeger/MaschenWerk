#!/usr/bin/env python3
"""
Directus Collections Setup Script
Erstellt alle benötigten Collections und Fields über die API
"""

import requests
import json
import sys

# Directus Config
DIRECTUS_URL = "http://localhost:8055"

# Token aus Datei lesen
with open("/tmp/directus_token.txt", "r") as f:
    TOKEN = f.read().strip()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def create_collection(name, schema):
    """Erstelle eine Collection"""
    print(f"\n📦 Erstelle Collection: {name}")
    
    response = requests.post(
        f"{DIRECTUS_URL}/collections",
        headers=HEADERS,
        json=schema
    )
    
    if response.status_code in [200, 204]:
        print(f"✅ Collection '{name}' erstellt")
        return True
    elif response.status_code == 400 and "already exists" in response.text.lower():
        print(f"⚠️  Collection '{name}' existiert bereits")
        return True
    else:
        print(f"❌ Fehler: {response.status_code} - {response.text}")
        return False

def create_field(collection, field_name, field_schema):
    """Erstelle ein Field in einer Collection"""
    print(f"  ➕ Feld: {field_name}")
    
    response = requests.post(
        f"{DIRECTUS_URL}/fields/{collection}",
        headers=HEADERS,
        json=field_schema
    )
    
    if response.status_code in [200, 204]:
        print(f"    ✅ Feld '{field_name}' erstellt")
        return True
    elif response.status_code == 400:
        print(f"    ⚠️  Feld '{field_name}' existiert bereits")
        return True
    else:
        print(f"    ❌ Fehler: {response.status_code} - {response.text}")
        return False

# ============================================================================
# COLLECTION: tags
# ============================================================================

tags_collection = {
    "collection": "tags",
    "meta": {
        "icon": "label",
        "display_template": "{{name}}"
    },
    "schema": {}
}

tags_fields = [
    {
        "field": "name",
        "type": "string",
        "meta": {
            "interface": "input",
            "required": True,
            "options": {
                "maxLength": 100
            }
        },
        "schema": {
            "max_length": 100,
            "is_nullable": False
        }
    },
    {
        "field": "slug",
        "type": "string",
        "meta": {
            "interface": "input",
            "required": True,
            "options": {
                "slug": True
            }
        },
        "schema": {
            "max_length": 100,
            "is_nullable": False,
            "is_unique": True
        }
    }
]

# ============================================================================
# COLLECTION: projects
# ============================================================================

projects_collection = {
    "collection": "projects",
    "meta": {
        "icon": "🧶",
        "display_template": "{{title}}",
        "sort_field": "finished_at"
    },
    "schema": {}
}

projects_fields = [
    {
        "field": "status",
        "type": "string",
        "meta": {
            "interface": "select-dropdown",
            "options": {
                "choices": [
                    {"text": "Draft", "value": "draft"},
                    {"text": "Public", "value": "public"},
                    {"text": "Private", "value": "private"}
                ]
            },
            "default_value": "draft"
        },
        "schema": {
            "default_value": "draft",
            "is_nullable": False
        }
    },
    {
        "field": "title",
        "type": "string",
        "meta": {
            "interface": "input",
            "required": True
        },
        "schema": {
            "max_length": 255,
            "is_nullable": False
        }
    },
    {
        "field": "slug",
        "type": "string",
        "meta": {
            "interface": "input",
            "required": True,
            "options": {
                "slug": True
            }
        },
        "schema": {
            "max_length": 255,
            "is_nullable": False,
            "is_unique": True
        }
    },
    {
        "field": "description",
        "type": "text",
        "meta": {
            "interface": "input-rich-text-md",
            "options": {
                "toolbar": ["bold", "italic", "link", "code", "unordered-list", "ordered-list"]
            }
        },
        "schema": {
            "is_nullable": True
        }
    },
    {
        "field": "finished_at",
        "type": "date",
        "meta": {
            "interface": "datetime",
            "display": "datetime"
        },
        "schema": {
            "is_nullable": True
        }
    },
    {
        "field": "hero_image",
        "type": "uuid",
        "meta": {
            "interface": "file-image",
            "special": ["file"]
        },
        "schema": {
            "is_nullable": True
        }
    },
    {
        "field": "private_notes",
        "type": "text",
        "meta": {
            "interface": "input-multiline",
            "note": "Nur für Admins sichtbar"
        },
        "schema": {
            "is_nullable": True
        }
    }
]

# ============================================================================
# COLLECTION: patterns
# ============================================================================

patterns_collection = {
    "collection": "patterns",
    "meta": {
        "icon": "description",
        "display_template": "{{title}}"
    },
    "schema": {}
}

patterns_fields = [
    {
        "field": "title",
        "type": "string",
        "meta": {
            "interface": "input",
            "required": True
        },
        "schema": {
            "max_length": 255,
            "is_nullable": False
        }
    },
    {
        "field": "slug",
        "type": "string",
        "meta": {
            "interface": "input",
            "required": True,
            "options": {
                "slug": True
            }
        },
        "schema": {
            "max_length": 255,
            "is_nullable": False,
            "is_unique": True
        }
    },
    {
        "field": "visibility",
        "type": "string",
        "meta": {
            "interface": "select-dropdown",
            "options": {
                "choices": [
                    {"text": "Friends & Family", "value": "friends_family"},
                    {"text": "Private", "value": "private"}
                ]
            },
            "default_value": "private"
        },
        "schema": {
            "default_value": "private",
            "is_nullable": False
        }
    },
    {
        "field": "pdf_file",
        "type": "uuid",
        "meta": {
            "interface": "file",
            "special": ["file"]
        },
        "schema": {
            "is_nullable": True
        }
    },
    {
        "field": "notes",
        "type": "text",
        "meta": {
            "interface": "input-multiline"
        },
        "schema": {
            "is_nullable": True
        }
    }
]

# ============================================================================
# MAIN EXECUTION
# ============================================================================

print("🚀 Starting Directus Collections Setup...")
print(f"   URL: {DIRECTUS_URL}")

# Create collections
create_collection("tags", tags_collection)
for field in tags_fields:
    create_field("tags", field["field"], field)

create_collection("projects", projects_collection)
for field in projects_fields:
    create_field("projects", field["field"], field)

create_collection("patterns", patterns_collection)
for field in patterns_fields:
    create_field("patterns", field["field"], field)

print("\n✅ Setup abgeschlossen!")
print("\n📝 Nächste Schritte:")
print("   1. Junction Tables erstellen (projects_tags, project_images, projects_patterns)")
print("   2. Rollen & Rechte konfigurieren")
print("   3. Test-Daten anlegen")
