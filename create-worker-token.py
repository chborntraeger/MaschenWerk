import requests
import sys

# Configuration
DIRECTUS_URL = "http://localhost:8055"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "ChangeMe123!"

def create_worker_token():
    """Create a static token for the PDF Worker user."""
    
    print("🔐 Creating Worker Static Token...")
    
    # Step 1: Login as admin
    print("\n1. Logging in as admin...")
    login_response = requests.post(
        f"{DIRECTUS_URL}/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(login_response.text)
        return None
    
    admin_token = login_response.json()["data"]["access_token"]
    print("✅ Logged in successfully")
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Step 2: Find PDF Worker user
    print("\n2. Finding PDF Worker user...")
    users_response = requests.get(
        f"{DIRECTUS_URL}/users",
        headers=headers,
        params={"filter[email][_eq]": "worker@example.com"}
    )
    
    if users_response.status_code != 200:
        print(f"❌ Failed to fetch users: {users_response.status_code}")
        return None
    
    users = users_response.json()["data"]
    if not users:
        print("❌ PDF Worker user not found. Email: worker@example.com")
        return None
    
    worker_id = users[0]["id"]
    print(f"✅ Found PDF Worker user: {worker_id}")
    
    # Step 3: Create static token
    print("\n3. Creating static token...")
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
    token = create_worker_token()
    
    if token:
        print("\n" + "="*60)
        print("SUCCESS! 🎉")
        print("="*60)
        print("\nNext steps:")
        print("1. Copy the token above")
        print("2. Update .env file:")
        print(f"   WORKER_TOKEN={token}")
        print("3. Restart the worker container:")
        print("   docker compose restart pdf_worker")
        print("\n" + "="*60)
    else:
        print("\n❌ Failed to create worker token")
        sys.exit(1)
