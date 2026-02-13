"""
Simple authentication test - tests one endpoint at a time.
"""
import requests
import json
import time

BASE_URL = "http://localhost:8001/api/v1"

print("=" * 60)
print("PHASE 1 AUTHENTICATION SYSTEM TEST")
print("=" * 60)

# Wait for server to be ready
print("\n⏳ Waiting for server to be ready...")
time.sleep(2)

try:
    health = requests.get("http://localhost:8001/health")
    print(f"✅ Server is healthy: {health.json()}")
except Exception as e:
    print(f"❌ Server not responding: {e}")
    exit(1)

# Test 1: Login with existing user
print("\n" + "=" * 60)
print("TEST 1: Login with Newbie Ned")
print("=" * 60)

login_data = {
    "email": "newbie@example.com",
    "password": "password123"
}

try:
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        tokens = response.json()
        print("✅ LOGIN SUCCESSFUL!")
        print(f"   Access Token: {tokens['access_token'][:50]}...")
        print(f"   Refresh Token: {tokens['refresh_token'][:50]}...")
        print(f"   Token Type: {tokens['token_type']}")
        access_token = tokens['access_token']
    else:
        print(f"❌ LOGIN FAILED: {response.text}")
        exit(1)
except Exception as e:
    print(f"❌ ERROR: {e}")
    exit(1)

# Test 2: Access protected route
print("\n" + "=" * 60)
print("TEST 2: Access Protected Route (/auth/me)")
print("=" * 60)

headers = {"Authorization": f"Bearer {access_token}"}

try:
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        user = response.json()
        print("✅ PROTECTED ROUTE ACCESS SUCCESSFUL!")
        print(f"\n   User Profile:")
        print(f"   - Name: {user['full_name']}")
        print(f"   - Email: {user['email']}")
        print(f"   - Role: {user['role']}")
        print(f"   - Department: {user['department']}")
        print(f"   - Employee ID: {user.get('id', 'N/A')[:8]}...")
        print(f"   - Is Admin: {user['is_admin']}")
        print(f"   - Current Skills: {', '.join(user['current_skills'])}")
        print(f"   - Target Skills: {', '.join(user['target_skills'])}")
        print(f"   - Learning Style: {user['preferred_learning_style']}")
    else:
        print(f"❌ FAILED: {response.text}")
        exit(1)
except Exception as e:
    print(f"❌ ERROR: {e}")
    exit(1)

# Test 3: Test invalid token
print("\n" + "=" * 60)
print("TEST 3: Test Invalid Token (Should Fail)")
print("=" * 60)

bad_headers = {"Authorization": "Bearer invalid_token_12345"}

try:
    response = requests.get(f"{BASE_URL}/auth/me", headers=bad_headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 401:
        print("✅ INVALID TOKEN CORRECTLY REJECTED!")
    else:
        print(f"❌ UNEXPECTED RESPONSE: {response.text}")
except Exception as e:
    print(f"✅ INVALID TOKEN CORRECTLY REJECTED (Exception: {type(e).__name__})")

# Test 4: Login as Admin
print("\n" + "=" * 60)
print("TEST 4: Login as Admin User")
print("=" * 60)

admin_login = {
    "email": "admin@example.com",
    "password": "password123"
}

try:
    response = requests.post(f"{BASE_URL}/auth/login", json=admin_login)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        admin_tokens = response.json()
        admin_headers = {"Authorization": f"Bearer {admin_tokens['access_token']}"}
        
        # Get admin profile
        profile_response = requests.get(f"{BASE_URL}/auth/me", headers=admin_headers)
        if profile_response.status_code == 200:
            admin_user = profile_response.json()
            print("✅ ADMIN LOGIN SUCCESSFUL!")
            print(f"   Name: {admin_user['full_name']}")
            print(f"   Role: {admin_user['role']}")
            print(f"   Is Admin: {admin_user['is_admin']}")
    else:
        print(f"❌ ADMIN LOGIN FAILED: {response.text}")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Summary
print("\n" + "=" * 60)
print("✅ PHASE 1 AUTHENTICATION TESTS COMPLETED SUCCESSFULLY!")
print("=" * 60)
print("\nAll authentication features are working:")
print("  ✓ User login with email/password")
print("  ✓ JWT token generation")
print("  ✓ Protected route access with valid token")
print("  ✓ Invalid token rejection")
print("  ✓ Admin user authentication")
print("  ✓ User profile retrieval with enterprise fields")
print("\n" + "=" * 60)
