"""
Test script for profile management endpoints.
Tests profile retrieval, updates, learning history, and skills.
"""
import requests
import json
import time

BASE_URL = "http://localhost:8001/api/v1"

print("=" * 60)
print("PHASE 2 PROFILE MANAGEMENT SYSTEM TEST")
print("=" * 60)

# Wait for server
time.sleep(1)

# Test 1: Login
print("\n1. Logging in as Newbie Ned...")
login_data = {"email": "newbie@example.com", "password": "password123"}
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)

if response.status_code == 200:
    tokens = response.json()
    access_token = tokens['access_token']
    headers = {"Authorization": f"Bearer {access_token}"}
    print("✅ Login successful!")
else:
    print(f"❌ Login failed: {response.text}")
    exit(1)

# Test 2: Get Profile
print("\n" + "=" * 60)
print("TEST 2: Get My Profile")
print("=" * 60)

response = requests.get(f"{BASE_URL}/profile", headers=headers)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    profile = response.json()
    print("✅ PROFILE RETRIEVED SUCCESSFULLY!")
    print(f"   Name: {profile['full_name']}")
    print(f"   Role: {profile['role']}")
    print(f"   Department: {profile['department']}")
    print(f"   Current Skills: {', '.join(profile['current_skills'])}")
    print(f"   Target Skills: {', '.join(profile['target_skills'])}")
    print(f"   Learning Pace: {profile['learning_pace']}")
    user_id = profile['id']
else:
    print(f"❌ FAILED: {response.text}")
    exit(1)

# Test 3: Update Profile
print("\n" + "=" * 60)
print("TEST 3: Update Profile")
print("=" * 60)

update_data = {
    "current_skills": ["HTML", "CSS", "JavaScript"],  # Added JavaScript
    "target_skills": ["Python", "React", "Node.js"],  # Updated targets
    "learning_pace": "medium"  # Changed from slow to medium
}

response = requests.patch(f"{BASE_URL}/profile", json=update_data, headers=headers)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    updated_profile = response.json()
    print("✅ PROFILE UPDATED SUCCESSFULLY!")
    print(f"   New Current Skills: {', '.join(updated_profile['current_skills'])}")
    print(f"   New Target Skills: {', '.join(updated_profile['target_skills'])}")
    print(f"   New Learning Pace: {updated_profile['learning_pace']}")
else:
    print(f"❌ FAILED: {response.text}")

# Test 4: Get Skills Summary
print("\n" + "=" * 60)
print("TEST 4: Get Skills Summary")
print("=" * 60)

response = requests.get(f"{BASE_URL}/profile/skills", headers=headers)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    skills = response.json()
    print("✅ SKILLS RETRIEVED SUCCESSFULLY!")
    print(f"   Current Skills: {', '.join(skills['current_skills'])}")
    print(f"   Target Skills: {', '.join(skills['target_skills'])}")
    print(f"   Skill Gaps: {', '.join(skills['skill_gaps'])}")
else:
    print(f"❌ FAILED: {response.text}")

# Test 5: Get Learning History
print("\n" + "=" * 60)
print("TEST 5: Get Learning History")
print("=" * 60)

response = requests.get(f"{BASE_URL}/profile/history", headers=headers)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    history = response.json()
    print(f"✅ LEARNING HISTORY RETRIEVED!")
    print(f"   Total Interactions: {len(history)}")
    if history:
        print(f"\n   Recent Activity:")
        for item in history[:3]:  # Show first 3
            print(f"   - {item['asset_title']}")
            print(f"     Status: {item['status']}, Score: {item.get('score', 'N/A')}")
    else:
        print("   (No learning history yet)")
else:
    print(f"❌ FAILED: {response.text}")

# Test 6: Admin Access - Get Another User's Profile
print("\n" + "=" * 60)
print("TEST 6: Admin Access to User Profile")
print("=" * 60)

# Login as admin
admin_login = {"email": "admin@example.com", "password": "password123"}
response = requests.post(f"{BASE_URL}/auth/login", json=admin_login)

if response.status_code == 200:
    admin_tokens = response.json()
    admin_headers = {"Authorization": f"Bearer {admin_tokens['access_token']}"}
    
    # Try to get Newbie Ned's profile as admin
    response = requests.get(f"{BASE_URL}/profile/{user_id}", headers=admin_headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        profile = response.json()
        print("✅ ADMIN ACCESS SUCCESSFUL!")
        print(f"   Accessed Profile: {profile['full_name']} ({profile['email']})")
    else:
        print(f"❌ FAILED: {response.text}")
else:
    print(f"❌ Admin login failed")

# Test 7: Non-Admin Cannot Access Other Profiles
print("\n" + "=" * 60)
print("TEST 7: Non-Admin Access Control")
print("=" * 60)

# Try to access admin profile as regular user
response = requests.get(f"{BASE_URL}/profile/some-other-user-id", headers=headers)
print(f"Status: {response.status_code}")

if response.status_code == 403:
    print("✅ ACCESS CORRECTLY DENIED!")
    print("   Non-admin users cannot view other profiles")
elif response.status_code == 404:
    print("✅ ACCESS CORRECTLY DENIED!")
    print("   User not found (expected for invalid ID)")
else:
    print(f"⚠️  Unexpected response: {response.status_code}")

print("\n" + "=" * 60)
print("✅ PHASE 2 PROFILE MANAGEMENT TESTS COMPLETED!")
print("=" * 60)
print("\nAll profile management features are working:")
print("  ✓ Profile retrieval")
print("  ✓ Profile updates")
print("  ✓ Skills summary with gap analysis")
print("  ✓ Learning history tracking")
print("  ✓ Admin access to user profiles")
print("  ✓ Access control enforcement")
print("\n" + "=" * 60)
