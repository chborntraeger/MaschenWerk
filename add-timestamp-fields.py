import requests

# Configuration
DIRECTUS_URL = "http://localhost:8055"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "ChangeMe123!"

def add_timestamp_fields():
    """Add date_created and date_updated fields to patterns collection."""
    
    print("📅 Adding timestamp fields to patterns collection...")
    
    # Step 1: Login as admin
    print("\n1. Logging in as admin...")
    login_response = requests.post(
        f"{DIRECTUS_URL}/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        return
    
    admin_token = login_response.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {admin_token}"}
    print("✅ Logged in")
    
    # Step 2: Add date_created field
    print("\n2. Adding date_created field...")
    date_created_field = {
        "collection": "patterns",
        "field": "date_created",
        "type": "timestamp",
        "meta": {
            "interface": "datetime",
            "special": ["date-created"],
            "readonly": True,
            "hidden": False,
            "width": "half"
        },
        "schema": {
            "default_value": "CURRENT_TIMESTAMP",
            "is_nullable": False
        }
    }
    
    response = requests.post(
        f"{DIRECTUS_URL}/fields/patterns",
        headers=headers,
        json=date_created_field
    )
    
    if response.status_code in [200, 201]:
        print("✅ date_created field added")
    else:
        print(f"⚠️  date_created: {response.status_code} - {response.text[:200]}")
    
    # Step 3: Add date_updated field
    print("\n3. Adding date_updated field...")
    date_updated_field = {
        "collection": "patterns",
        "field": "date_updated",
        "type": "timestamp",
        "meta": {
            "interface": "datetime",
            "special": ["date-updated"],
            "readonly": True,
            "hidden": False,
            "width": "half"
        },
        "schema": {
            "default_value": "CURRENT_TIMESTAMP",
            "is_nullable": False
        }
    }
    
    response = requests.post(
        f"{DIRECTUS_URL}/fields/patterns",
        headers=headers,
        json=date_updated_field
    )
    
    if response.status_code in [200, 201]:
        print("✅ date_updated field added")
    else:
        print(f"⚠️  date_updated: {response.status_code} - {response.text[:200]}")
    
    print("\n✅ Timestamp fields added successfully!")
    print("\nNow rebuild the worker:")
    print("   docker compose up pdf_worker -d --build")

if __name__ == "__main__":
    add_timestamp_fields()
