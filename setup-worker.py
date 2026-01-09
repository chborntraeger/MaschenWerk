import requests
import sys

# Configuration
DIRECTUS_URL = "http://localhost:8055"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "ChangeMe123!"

def create_worker_user_and_token():
    """Create PDF Worker user and static token."""
    
    print("🔧 Creating PDF Worker User and Token...")
    
    # Step 1: Login as admin
    print("\n1. Logging in as admin...")
    login_response = requests.post(
        f"{DIRECTUS_URL}/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        return None
    
    admin_token = login_response.json()["data"]["access_token"]
    print("✅ Logged in successfully")
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Step 2: Find or get Worker role
    print("\n2. Finding Worker role...")
    roles_response = requests.get(
        f"{DIRECTUS_URL}/roles",
        headers=headers,
        params={"filter[name][_eq]": "Worker"}
    )
    
    if roles_response.status_code != 200:
        print(f"❌ Failed to fetch roles: {roles_response.status_code}")
        return None
    
    roles = roles_response.json()["data"]
    if not roles:
        print("❌ Worker role not found")
        return None
    
    worker_role_id = roles[0]["id"]
    print(f"✅ Found Worker role: {worker_role_id}")
    
    # Step 3: Check if worker user already exists
    print("\n3. Checking for existing worker user...")
    users_response = requests.get(
        f"{DIRECTUS_URL}/users",
        headers=headers,
        params={"filter[email][_eq]": "worker@example.com"}
    )
    
    if users_response.status_code == 200:
        users = users_response.json()["data"]
        if users:
            worker_id = users[0]["id"]
            print(f"✅ Worker user already exists: {worker_id}")
        else:
            # Create worker user
            print("\n3b. Creating new worker user...")
            create_user_response = requests.post(
                f"{DIRECTUS_URL}/users",
                headers=headers,
                json={
                    "email": "worker@example.com",
                    "password": "WorkerPass123!",
                    "role": worker_role_id,
                    "status": "active",
                    "first_name": "PDF",
                    "last_name": "Worker"
                }
            )
            
            if create_user_response.status_code not in [200, 201]:
                print(f"❌ Failed to create user: {create_user_response.status_code}")
                print(create_user_response.text)
                return None
            
            worker_id = create_user_response.json()["data"]["id"]
            print(f"✅ Created worker user: {worker_id}")
    
    # Step 4: Create static token
    print("\n4. Creating static token...")
    token_response = requests.post(
        f"{DIRECTUS_URL}/users/{worker_id}/tokens",
        headers=headers,
        json={
            "name": "PDF Worker Token",
            "expires": None  # Never expires
        }
    )
    
    if token_response.status_code not in [200, 201]:
        print(f"❌ Failed to create token: {token_response.status_code}")
        print(token_response.text)
        return None
    
    token_data = token_response.json()["data"]
    static_token = token_data["token"]
    
    print(f"✅ Static token created successfully!")
    print(f"\n📋 Token: {static_token}")
    
    return static_token

if __name__ == "__main__":
    token = create_worker_user_and_token()
    
    if token:
        print("\n" + "="*60)
        print("SUCCESS! 🎉")
        print("="*60)
        print("\nNext steps:")
        print("1. I'll automatically update the .env file")
        print("2. Then restart the worker container")
        print("\n" + "="*60)
        
        # Output token for script to capture
        print(f"\nTOKEN:{token}")
    else:
        print("\n❌ Failed to create worker token")
        sys.exit(1)
