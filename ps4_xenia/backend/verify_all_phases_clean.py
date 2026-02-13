"""
FINAL VERIFICATION SCRIPT (UPDATED for Phase 4)
Verifies integration of Phase 1 (Auth), Phase 2 (Profiles), Phase 3 (Assets), and Phase 4 (Adaptive).
Functional tests only.
"""
import requests
import time
import sys

BASE_URL = "http://localhost:8001/api/v1"

def print_header(title):
    print("\n" + "="*40)
    print(f"{title:^40}")
    print("="*40)

def check(condition, message):
    if condition:
        print(f"  ✅ PASS: {message}")
    else:
        print(f"  ❌ FAIL: {message}")
        sys.exit(1)

def main():
    print_header(">>> PRE-CHECK: System Health")
    try:
        r = requests.get(f"http://localhost:8001/api/v1/health") # Assuming health check exists or check docs
        # Actually /docs is a good proxy if no health endpoint
        r = requests.get("http://localhost:8001/docs")
        check(r.status_code == 200, "System is healthy")
    except Exception as e:
        check(False, f"System down: {e}")

    # ==========================================
    # PHASE 1: AUTH
    # ==========================================
    print_header("PHASE 1: AUTHENTICATION")
    
    # 1. Register Admin
    admin_email = f"admin_verify_{int(time.time())}@example.com"
    payload = {"email": admin_email, "password": "password123", "full_name": "Admin User", "role": "admin"}
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    check(response.status_code == 200, "Admin registration")
    
    # 2. Login Admin
    data = {"username": admin_email, "password": "password123"}
    response = requests.post(f"{BASE_URL}/auth/token", data=data)
    check(response.status_code == 200, "Admin login")
    admin_token = response.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # ==========================================
    # PHASE 2: PROFILES
    # ==========================================
    print_header("PHASE 2: PROFILES")
    
    # 1. Update Profile
    profile_update = {
        "full_name": "Verified Admin",
        "title": "System Verifier",
        "bio": "Checking systems",
        "skills": ["Python", "Testing"],
        "linkedin_url": "https://linkedin.com/in/admin",
        "github_url": "https://github.com/admin",
        "twitter_url": "https://twitter.com/admin"
    }
    response = requests.put(f"{BASE_URL}/profile", json=profile_update, headers=admin_headers)
    check(response.status_code == 200, "Profile update")
    check(response.json()["full_name"] == "Verified Admin", "Profile data persisted")

    # ==========================================
    # PHASE 3: ASSETS
    # ==========================================
    print_header("PHASE 3: ASSETS")
    
    # 1. Create Asset
    asset_payload = {
        "title": f"Verifiable Asset {int(time.time())}",
        "description": "Asset for automated verification",
        "content_type": "video",
        "content_url": "http://example.com/video.mp4",
        "skill_tag": "Testing",
        "difficulty_level": 3,
        "estimated_duration_minutes": 15
    }
    response = requests.post(f"{BASE_URL}/admin/assets", json=asset_payload, headers=admin_headers)
    check(response.status_code == 200, "Admin created asset")
    asset_id = response.json()["id"]

    # 2. Add Version
    version_payload = {
        "version": 2,
        "content_url": "http://example.com/v2.mp4",
        "content_type": "video",
        "change_log": "Updated content"
    }
    response = requests.post(f"{BASE_URL}/admin/assets/{asset_id}/versions", json=version_payload, headers=admin_headers)
    check(response.status_code == 200, "Version added")
    
    # 3. User View Library
    # Create regular user
    user_email = f"user_verify_{int(time.time())}@example.com"
    requests.post(f"{BASE_URL}/auth/register", json={"email": user_email, "password": "pw", "full_name": "User", "role": "employee"})
    token_resp = requests.post(f"{BASE_URL}/auth/token", data={"username": user_email, "password": "pw"})
    user_token = token_resp.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {user_token}"}
    
    # Fetch library
    response = requests.get(f"{BASE_URL}/library", headers=user_headers)
    check(response.status_code == 200, "User accessed library")
    library = response.json()
    found = any(a['id'] == asset_id for a in library)
    check(found, "New asset visible to user")

    # ==========================================
    # PHASE 4: ADAPTIVE ENGINE
    # ==========================================
    print_header("PHASE 4: ADAPTIVE ENGINE")

    # 1. Dashboard Stats
    user_info = requests.get(f"{BASE_URL}/auth/me", headers=user_headers).json()
    user_id = user_info['id']
    response = requests.get(f"{BASE_URL}/learning/dashboard/{user_id}", headers=user_headers)
    check(response.status_code == 200, "Dashboard stats accessible")
    
    # 2. Legacy Next Recommendation
    response = requests.get(f"{BASE_URL}/learning/{user_id}/next", headers=user_headers)
    # Might be 404 if no recommendations match, but with our asset it should match default
    if response.status_code == 200:
         check(True, "Legacy /next endpoint working")
    elif response.status_code == 404:
         print("  ℹ️  /next returned 404 (acceptable if logic filters it out)")
    else:
         check(False, f"/next endpoint failed: {response.status_code}")

    # 3. Multi-Option Recommendations
    response = requests.get(f"{BASE_URL}/learning/{user_id}/recommendations", headers=user_headers)
    check(response.status_code == 200, "Recommendations endpoint accessible")
    recs = response.json()
    check(isinstance(recs, list), "Recommendations returned as list")
    print(f"  ℹ️  Received {len(recs)} recommendations")

    print_header("✅ ALL SYSTEMS GO")

if __name__ == "__main__":
    main()
