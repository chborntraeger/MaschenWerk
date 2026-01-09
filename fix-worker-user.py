import requests

# Configuration
DIRECTUS_URL = "http://localhost:8055"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "ChangeMe123!"
WORKER_USER_ID = "a888ef19-dc2b-4322-aa42-c2ab970108c9"

def fix_worker_user():
    """Assign Worker role to the worker user."""
    
    print("🔧 Fixing Worker User...")
    
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
    print("✅ Logged in successfully")
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Step 2: Get Worker role ID
    print("\n2. Finding Worker role...")
    roles_response = requests.get(
        f"{DIRECTUS_URL}/roles",
        headers=headers,
        params={"filter[name][_eq]": "Worker"}
    )
    
    if roles_response.status_code != 200:
        print(f"❌ Failed to fetch roles: {roles_response.status_code}")
        return
    
    roles = roles_response.json()["data"]
    if not roles:
        print("❌ Worker role not found")
        return
    
    worker_role_id = roles[0]["id"]
    print(f"✅ Found Worker role: {worker_role_id}")
    
    # Step 3: Update worker user
    print(f"\n3. Updating worker user {WORKER_USER_ID}...")
    update_response = requests.patch(
        f"{DIRECTUS_URL}/users/{WORKER_USER_ID}",
        headers=headers,
        json={
            "role": worker_role_id,
            "email": "worker@example.com",
            "status": "active"
        }
    )
    
    if update_response.status_code in [200, 204]:
        print("✅ Worker user updated successfully!")
        print("\nNow restart the worker:")
        print("   docker compose restart pdf_worker")
    else:
        print(f"❌ Failed to update user: {update_response.status_code}")
        print(update_response.text)

if __name__ == "__main__":
    fix_worker_user()
