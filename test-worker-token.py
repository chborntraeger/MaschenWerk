import requests
import os

# Configuration
DIRECTUS_URL = "http://localhost:8055"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "ChangeMe123!"
WORKER_TOKEN = os.getenv("WORKER_TOKEN", "ZpuFSioOAY3iTcuE0ZTAdFYyEixYYmYZ")

def test_worker_token():
    """Test if the worker token works for accessing patterns."""
    
    print(f"🧪 Testing Worker Token: {WORKER_TOKEN[:20]}...")
    
    # Try to access patterns with the worker token
    headers = {"Authorization": f"Bearer {WORKER_TOKEN}"}
    
    response = requests.get(
        f"{DIRECTUS_URL}/items/patterns",
        headers=headers,
        params={"limit": 1}
    )
    
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Token works! Worker can access patterns.")
        data = response.json()
        print(f"   Found {len(data.get('data', []))} patterns")
        return True
    elif response.status_code == 401:
        print("❌ Token is invalid or expired (401 Unauthorized)")
        print("\nThe token needs to be created in Directus UI:")
        print("1. Open http://localhost:8055")
        print("2. Login as admin")
        print("3. Go to Settings → Access Control → Users")
        print("4. Find 'PDF Worker' user (or create it)")
        print("5. Click on the user")
        print("6. Go to 'Tokens' tab")
        print("7. Click 'Create Token'")
        print("8. Name it 'PDF Worker Token'")
        print("9. Set expiration to 'Never'")
        print("10. Copy the generated token")
        print("11. Update .env: WORKER_TOKEN=<your-token>")
        print("12. Restart worker: docker compose restart pdf_worker")
        return False
    else:
        print(f"❌ Unexpected error: {response.status_code}")
        print(response.text)
        return False

if __name__ == "__main__":
    test_worker_token()
