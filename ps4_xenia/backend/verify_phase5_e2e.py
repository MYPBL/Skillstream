import requests
import json

BASE_URL = "http://localhost:8001/api/v1"

def verify_endpoint(name, url, headers, expected_keys):
    print(f"Testing {name} ({url})...")
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"❌ {name} Failed: {res.status_code} {res.text}")
        return False
    
    data = res.json()
    # Check if data is list or dict
    if isinstance(data, list):
        if not data:
            print(f"⚠️ {name} returned empty list (might be expected if new user)")
        else:
            first_item = data[0]
            missing = [k for k in expected_keys if k not in first_item]
            if missing:
                print(f"❌ {name} missing keys in item: {missing}")
                return False
    elif isinstance(data, dict):
        missing = [k for k in expected_keys if k not in data]
        if missing:
            print(f"❌ {name} missing keys: {missing}")
            return False
    
    print(f"✅ {name} OK.")
    return True

def run_e2e_check():
    print("🚀 Starting Phase 5 E2E Verification...")
    
    # Login
    login_res = requests.post(f"{BASE_URL}/auth/login", json={"email": "admin@example.com", "password": "password123"})
    if login_res.status_code != 200:
        print("❌ Login failed. Cannot verify.")
        return
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get User ID
    me = requests.get(f"{BASE_URL}/auth/me", headers=headers).json()
    uid = me["id"]
    
    # 1. Overview
    verify_endpoint(
        "Analytics Overview", 
        f"{BASE_URL}/analytics/{uid}/overview", 
        headers, 
        ["total_learning_hours", "modules_completed", "current_streak_days", "efficiency_score"]
    )

    # 2. Skills (Radar)
    verify_endpoint(
        "Skill Radar", 
        f"{BASE_URL}/analytics/{uid}/skills", 
        headers, 
        ["subject", "A", "fullMark"]
    )

    # 3. Activity (Bar Chart)
    verify_endpoint(
        "Activity Chart", 
        f"{BASE_URL}/analytics/{uid}/activity", 
        headers, 
        ["name", "minutes"]
    )

    print("\n🏁 Phase 5 Verification Complete.")

if __name__ == "__main__":
    run_e2e_check()
