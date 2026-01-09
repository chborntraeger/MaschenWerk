import requests
import os

# Login as admin
directus_url = "http://localhost:8055"
response = requests.post(
    f"{directus_url}/auth/login",
    json={
        "email": "admin@example.com",
        "password": "admin"
    }
)

if response.ok:
    data = response.json()
    token = data['data']['access_token']
    
    # Get user details
    user_response = requests.get(
        f"{directus_url}/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if user_response.ok:
        user_data = user_response.json()
        print("Admin User Info:")
        print(f"  Email: {user_data['data']['email']}")
        print(f"  Role ID: {user_data['data']['role']}")
        print(f"  First Name: {user_data['data'].get('first_name', 'N/A')}")
        
        # Check if role matches the hardcoded one
        expected_role = "b912e393-0b2d-44b9-a0a9-e59003d95bc2"
        actual_role = user_data['data']['role']
        
        if actual_role == expected_role:
            print(f"\n✅ Role matches! Admin dropdown should be visible.")
        else:
            print(f"\n❌ Role mismatch!")
            print(f"  Expected: {expected_role}")
            print(f"  Actual:   {actual_role}")
            print(f"\n  Update the hardcoded role in:")
            print(f"    - components/Header.tsx")
            print(f"    - app/admin/*/page.tsx files")
            print(f"    - components/Delete*Button.tsx files")
    else:
        print(f"Failed to get user: {user_response.text}")
else:
    print(f"Login failed: {response.text}")
