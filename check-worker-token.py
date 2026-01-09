import requests
import os

# Configuration
DIRECTUS_URL = "http://localhost:8055"
WORKER_TOKEN = os.getenv("WORKER_TOKEN", "ZpuFSioOAY3iTcuE0ZTAdFYyEixYYmYZ")

def check_token_user():
    """Check which user this token belongs to and their permissions."""
    
    print(f"🔍 Checking token: {WORKER_TOKEN[:20]}...")
    
    headers = {"Authorization": f"Bearer {WORKER_TOKEN}"}
    
    # Check /users/me to see which user this token belongs to
    print("\n1. Checking token user...")
    me_response = requests.get(f"{DIRECTUS_URL}/users/me", headers=headers)
    
    if me_response.status_code == 200:
        user_data = me_response.json()["data"]
        print(f"✅ Token belongs to user:")
        print(f"   ID: {user_data.get('id')}")
        print(f"   Email: {user_data.get('email')}")
        print(f"   Role: {user_data.get('role')}")
        print(f"   Status: {user_data.get('status')}")
        
        role_id = user_data.get('role')
    else:
        print(f"❌ Failed to get user info: {me_response.status_code}")
        print(me_response.text)
        return
    
    # Try to fetch patterns
    print("\n2. Testing patterns access...")
    patterns_response = requests.get(
        f"{DIRECTUS_URL}/items/patterns",
        headers=headers,
        params={"limit": 1}
    )
    
    print(f"   Status: {patterns_response.status_code}")
    if patterns_response.status_code == 200:
        data = patterns_response.json()
        print(f"   ✅ Success! Found {len(data.get('data', []))} patterns")
    elif patterns_response.status_code == 403:
        print("   ❌ 403 Forbidden - Permission denied")
        print("\n   Possible issues:")
        print("   1. Policy not assigned to the role")
        print("   2. Policy doesn't have read permission on 'patterns'")
        print("   3. Token might be cached - try creating a NEW token")
        print(f"\n   Response: {patterns_response.text}")
    elif patterns_response.status_code == 401:
        print("   ❌ 401 Unauthorized - Token invalid")
    else:
        print(f"   ❌ Unexpected error: {patterns_response.status_code}")
        print(f"   Response: {patterns_response.text}")

if __name__ == "__main__":
    # Read token from .env if available
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('WORKER_TOKEN='):
                    WORKER_TOKEN = line.split('=', 1)[1].strip()
                    break
    except:
        pass
    
    check_token_user()
