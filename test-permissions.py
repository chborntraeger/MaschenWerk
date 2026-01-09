import requests

# Configuration
DIRECTUS_URL = "http://localhost:8055"
TEST_EMAIL = "test@familie.de"
TEST_PASSWORD = "TestPass123!"

def test_access():
    """Test if test@familie.de can access patterns."""
    
    print("🧪 Testing permissions for test@familie.de...\n")
    
    # Step 1: Login as test user
    print("1. Logging in as test@familie.de...")
    login_response = requests.post(
        f"{DIRECTUS_URL}/auth/login",
        json={"email": TEST_EMAIL, "password": TEST_PASSWORD}
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"   Response: {login_response.text}")
        return
    
    test_token = login_response.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {test_token}"}
    print("✅ Logged in successfully")
    
    # Step 2: Try to fetch patterns
    print("\n2. Fetching patterns...")
    patterns_response = requests.get(
        f"{DIRECTUS_URL}/items/patterns",
        headers=headers,
        params={"sort": "-date_created"}
    )
    
    print(f"   Status: {patterns_response.status_code}")
    
    if patterns_response.status_code == 200:
        patterns = patterns_response.json()["data"]
        print(f"✅ SUCCESS! Found {len(patterns)} pattern(s)")
        
        for pattern in patterns:
            print(f"\n   Pattern: {pattern.get('title')}")
            print(f"   Slug: {pattern.get('slug')}")
            print(f"   Visibility: {pattern.get('visibility')}")
            print(f"   PDF: {pattern.get('pdf_file')}")
    else:
        print(f"❌ FAILED to fetch patterns")
        print(f"   Response: {patterns_response.text[:500]}")
    
    # Step 3: Try to fetch a specific pattern by slug
    print("\n3. Fetching pattern by slug (basis-socken)...")
    pattern_response = requests.get(
        f"{DIRECTUS_URL}/items/patterns",
        headers=headers,
        params={
            "filter[slug][_eq]": "basis-socken",
            "limit": 1
        }
    )
    
    print(f"   Status: {pattern_response.status_code}")
    
    if pattern_response.status_code == 200:
        results = pattern_response.json()["data"]
        if results:
            print(f"✅ Found pattern: {results[0].get('title')}")
        else:
            print("⚠️  No pattern found with slug 'basis-socken'")
    else:
        print(f"❌ FAILED")
        print(f"   Response: {pattern_response.text[:500]}")

if __name__ == "__main__":
    test_access()
