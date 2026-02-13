"""
Test script for authentication endpoints.
Tests registration, login, token refresh, and protected routes.
"""
import requests
import json

BASE_URL = "http://localhost:8001/api/v1"

def test_authentication():
    print("=" * 60)
    print("TESTING AUTHENTICATION SYSTEM")
    print("=" * 60)
    
    # Test 1: Register new user
    print("\n1. Testing User Registration...")
    register_data = {
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User",
        "department": "QA",
        "role": "QA Engineer"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 201:
        tokens = response.json()
        print(f"   ✅ Registration successful!")
        print(f"   Access Token: {tokens['access_token'][:50]}...")
        access_token = tokens['access_token']
    elif response.status_code == 400:
        print(f"   ⚠️  User already exists, proceeding to login...")
        access_token = None
    else:
        print(f"   ❌ Registration failed: {response.json()}")
        return
    
    # Test 2: Login with existing user
    print("\n2. Testing User Login...")
    login_data = {
        "email": "newbie@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        tokens = response.json()
        print(f"   ✅ Login successful!")
        print(f"   Access Token: {tokens['access_token'][:50]}...")
        print(f"   Refresh Token: {tokens['refresh_token'][:50]}...")
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
    else:
        print(f"   ❌ Login failed: {response.json()}")
        return
    
    # Test 3: Access protected route
    print("\n3. Testing Protected Route (/auth/me)...")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        user_data = response.json()
        print(f"   ✅ Protected route accessed successfully!")
        print(f"   User: {user_data['full_name']} ({user_data['email']})")
        print(f"   Role: {user_data['role']}")
        print(f"   Department: {user_data['department']}")
        print(f"   Current Skills: {user_data['current_skills']}")
        print(f"   Target Skills: {user_data['target_skills']}")
    else:
        print(f"   ❌ Failed to access protected route: {response.json()}")
        return
    
    # Test 4: Test invalid token
    print("\n4. Testing Invalid Token...")
    bad_headers = {"Authorization": "Bearer invalid_token_here"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=bad_headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 401:
        print(f"   ✅ Invalid token correctly rejected!")
    else:
        print(f"   ❌ Invalid token should have been rejected")
    
    # Test 5: Test token refresh
    print("\n5. Testing Token Refresh...")
    response = requests.post(f"{BASE_URL}/auth/refresh", params={"refresh_token": refresh_token})
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        new_tokens = response.json()
        print(f"   ✅ Token refresh successful!")
        print(f"   New Access Token: {new_tokens['access_token'][:50]}...")
    else:
        print(f"   ❌ Token refresh failed: {response.json()}")
    
    # Test 6: Test admin user
    print("\n6. Testing Admin User Login...")
    admin_login = {
        "email": "admin@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=admin_login)
    if response.status_code == 200:
        admin_tokens = response.json()
        admin_headers = {"Authorization": f"Bearer {admin_tokens['access_token']}"}
        
        response = requests.get(f"{BASE_URL}/auth/me", headers=admin_headers)
        if response.status_code == 200:
            admin_data = response.json()
            print(f"   ✅ Admin login successful!")
            print(f"   Admin: {admin_data['full_name']}")
            print(f"   Is Admin: {admin_data['is_admin']}")
    
    print("\n" + "=" * 60)
    print("AUTHENTICATION TESTS COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    test_authentication()
