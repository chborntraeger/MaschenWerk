import requests

# Configuration
DIRECTUS_URL = "http://localhost:8055"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "ChangeMe123!"

def link_pdf_to_pattern():
    """Verknüpfe eine hochgeladene PDF-Datei mit einem Pattern."""
    
    print("🔗 Linking PDF to Pattern...")
    
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
    
    # Step 2: List uploaded files
    print("\n2. Finding uploaded PDF files...")
    files_response = requests.get(
        f"{DIRECTUS_URL}/files",
        headers=headers,
        params={"filter[type][_contains]": "pdf", "limit": 10}
    )
    
    if files_response.status_code != 200:
        print(f"❌ Failed to fetch files: {files_response.status_code}")
        return
    
    files = files_response.json()["data"]
    if not files:
        print("❌ No PDF files found. Please upload a PDF first.")
        return
    
    print(f"✅ Found {len(files)} PDF file(s):")
    for i, f in enumerate(files):
        print(f"   {i+1}. {f.get('filename_download', 'Unknown')} (ID: {f['id']})")
    
    # Step 3: List patterns
    print("\n3. Finding patterns...")
    patterns_response = requests.get(
        f"{DIRECTUS_URL}/items/patterns",
        headers=headers,
        params={"limit": 10}
    )
    
    if patterns_response.status_code != 200:
        print(f"❌ Failed to fetch patterns: {patterns_response.status_code}")
        return
    
    patterns = patterns_response.json()["data"]
    if not patterns:
        print("❌ No patterns found.")
        return
    
    print(f"✅ Found {len(patterns)} pattern(s):")
    for i, p in enumerate(patterns):
        print(f"   {i+1}. {p.get('title', 'Unknown')} (ID: {p['id']})")
    
    # Step 4: Link first PDF to first pattern
    file_id = files[0]['id']
    pattern_id = patterns[0]['id']
    
    print(f"\n4. Linking PDF '{files[0].get('filename_download')}' to pattern '{patterns[0].get('title')}'...")
    
    update_response = requests.patch(
        f"{DIRECTUS_URL}/items/patterns/{pattern_id}",
        headers=headers,
        json={"pdf_file": file_id}
    )
    
    if update_response.status_code in [200, 204]:
        print("✅ Successfully linked PDF to pattern!")
        print("\nCheck Directus UI or wait for worker to process it.")
    else:
        print(f"❌ Failed to link: {update_response.status_code}")
        print(update_response.text)

if __name__ == "__main__":
    link_pdf_to_pattern()
