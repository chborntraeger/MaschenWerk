import requests
import json

# Configuration
DIRECTUS_URL = "http://localhost:8055"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "ChangeMe123!"

def setup_permissions():
    """Setup permissions for Friends & Family role."""
    
    print("🔐 Setting up Friends & Family permissions...")
    
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
    headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json"
    }
    print("✅ Logged in")
    
    # Step 2: Get Friends & Family role ID
    print("\n2. Getting Friends & Family role ID...")
    roles_response = requests.get(f"{DIRECTUS_URL}/roles", headers=headers)
    roles = roles_response.json()["data"]
    
    friends_family_role = None
    for role in roles:
        if role["name"] == "Friends & Family":
            friends_family_role = role
            break
    
    if not friends_family_role:
        print("❌ Friends & Family role not found")
        return
    
    role_id = friends_family_role["id"]
    print(f"✅ Found role: {role_id}")
    
    # Step 3: Check existing permissions
    print("\n3. Checking existing permissions...")
    perms_response = requests.get(
        f"{DIRECTUS_URL}/permissions",
        headers=headers,
        params={"filter[role][_eq]": role_id}
    )
    
    if perms_response.status_code == 200:
        existing = perms_response.json()["data"]
        print(f"   Found {len(existing)} existing permissions")
        
        # Delete old permissions for patterns and directus_files
        for perm in existing:
            if perm["collection"] in ["patterns", "directus_files"]:
                print(f"   Deleting old permission: {perm['collection']} - {perm['action']}")
                requests.delete(
                    f"{DIRECTUS_URL}/permissions/{perm['id']}",
                    headers=headers
                )
    
    # Step 4: Create permission for patterns collection (read only)
    print("\n4. Creating read permission for patterns...")
    
    patterns_permission = {
        "role": role_id,
        "collection": "patterns",
        "action": "read",
        "permissions": {
            "visibility": {
                "_eq": "friends_family"
            }
        },
        "validation": None,
        "presets": None,
        "fields": "*"
    }
    
    response = requests.post(
        f"{DIRECTUS_URL}/permissions",
        headers=headers,
        json=patterns_permission
    )
    
    if response.status_code in [200, 201]:
        print("✅ Patterns read permission created")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(f"   Response: {response.text}")
    
    # Step 5: Create permission for directus_files (read only)
    print("\n5. Creating read permission for directus_files...")
    
    files_permission = {
        "role": role_id,
        "collection": "directus_files",
        "action": "read",
        "permissions": None,  # Can read all files
        "validation": None,
        "presets": None,
        "fields": "*"
    }
    
    response = requests.post(
        f"{DIRECTUS_URL}/permissions",
        headers=headers,
        json=files_permission
    )
    
    if response.status_code in [200, 201]:
        print("✅ Files read permission created")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(f"   Response: {response.text}")
    
    print("\n✅ Permissions configured!")
    print("\nTest the access:")
    print("   1. Logout and login again with test@familie.de")
    print("   2. Visit http://localhost:3000/patterns")

if __name__ == "__main__":
    setup_permissions()
