import requests

# Configuration
DIRECTUS_URL = "http://localhost:8055"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "ChangeMe123!"

def check_user():
    """Check test user role assignment."""
    
    print("👤 Checking test@familie.de user...")
    
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
    
    # Step 2: Get all users
    print("\n2. Getting users...")
    users_response = requests.get(
        f"{DIRECTUS_URL}/users",
        headers=headers,
        params={"filter": {"email": {"_eq": "test@familie.de"}}}
    )
    
    if users_response.status_code != 200:
        print(f"❌ Failed to get users: {users_response.status_code}")
        return
    
    users = users_response.json()["data"]
    
    if not users:
        print("❌ User test@familie.de not found")
        return
    
    user = users[0]
    print(f"✅ Found user: {user['email']}")
    print(f"   ID: {user['id']}")
    print(f"   Role: {user.get('role')}")
    
    # Step 3: Get role details
    if user.get('role'):
        print("\n3. Getting role details...")
        role_response = requests.get(
            f"{DIRECTUS_URL}/roles/{user['role']}",
            headers=headers
        )
        
        if role_response.status_code == 200:
            role = role_response.json()["data"]
            print(f"✅ Role Name: {role['name']}")
            print(f"   Admin Access: {role.get('admin_access', False)}")
        else:
            print(f"⚠️  Could not fetch role: {role_response.status_code}")
    else:
        print("\n❌ User has NO role assigned!")
        print("\nYou need to assign the 'Friends & Family' role to this user in Directus:")
        print("   Settings → Access Control → Users & Roles → Edit test@familie.de → Select Role")

if __name__ == "__main__":
    check_user()
