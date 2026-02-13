import requests
import time
import sys

BASE_URL = "http://localhost:8001/api/v1"

def print_pass(msg):
    print(f"✅ PASS: {msg}")

def print_fail(msg):
    print(f"❌ FAIL: {msg}")
    # Don't exit, try to continue to see full health
    
def verify_system():
    print("🚀 STARTING FULL SYSTEM VERIFICATION (PHASE 1-6)\n")
    
    # --- PHASE 1: AUTH ---
    print("--- [Phase 1: Auth] ---")
    try:
        # Admin Login
        res = requests.post(f"{BASE_URL}/auth/login", json={"email": "admin@example.com", "password": "password123"})
        if res.status_code != 200:
            print_fail("Admin Login failed")
            return
        admin_token = res.json()["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        print_pass("Admin Login")
        
        # User Login
        res = requests.post(f"{BASE_URL}/auth/login", json={"email": "newbie@example.com", "password": "password123"})
        if res.status_code != 200:
            print_fail("User Login failed")
            return
        token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print_pass("User Login")
        
        # Get Profile
        me = requests.get(f"{BASE_URL}/auth/me", headers=headers).json()
        user_id = me["id"]
        print_pass(f"Profile Retrieval (User ID: {user_id})")
        
    except Exception as e:
        print_fail(f"Auth Exception: {e}")
        return

    # --- PHASE 2: PROFILE ---
    print("\n--- [Phase 2: Profile] ---")
    try:
        # Update Target Skills
        new_targets = ["FastAPI", "React", "AI"]
        res = requests.patch(f"{BASE_URL}/profile", json={"target_skills": new_targets}, headers=headers)
        if res.status_code == 200 and "AI" in res.json()["target_skills"]:
            print_pass("Profile Update (Target Skills)")
        else:
            print_fail("Profile Update")
    except Exception as e:
        print_fail(f"Profile Exception: {e}")

    # --- PHASE 3: ASSETS ---
    print("\n--- [Phase 3: Assets] ---")
    asset_id = None
    try:
        # Create Asset
        payload = {
            "title": "System Check Asset",
            "description": "Asset for verification",
            "content_type": "video",
            "content_url": "http://example.com",
            "skill_tag": "AI",
            "difficulty_level": 3,
            "estimated_duration_minutes": 10
        }
        res = requests.post(f"{BASE_URL}/admin/assets", json=payload, headers=admin_headers)
        if res.status_code == 200:
            asset_id = res.json()["id"]
            print_pass(f"Asset Creation (ID: {asset_id})")
        else:
            print_fail(f"Asset Creation: {res.text}")
    except Exception as e:
        print_fail(f"Asset Exception: {e}")

    # --- PHASE 4: ADAPTIVE ENGINE ---
    print("\n--- [Phase 4: Adaptive Engine] ---")
    try:
        # Get Recommendations
        res = requests.get(f"{BASE_URL}/learning/{user_id}/recommendations", headers=headers)
        if res.status_code == 200:
            recs = res.json()
            if len(recs) > 0:
                print_pass(f"Recommendations Fetched ({len(recs)} items)")
            else:
                print_pass("Recommendations Fetched (Empty - acceptable if library exhausted)")
        else:
            print_fail("Recommendations API")
    except Exception as e:
        print_fail(f"Adaptive Engine Exception: {e}")

    # --- PHASE 5: ANALYTICS ---
    print("\n--- [Phase 5: Analytics] ---")
    try:
        # Overview
        res = requests.get(f"{BASE_URL}/analytics/{user_id}/overview", headers=headers)
        if res.status_code == 200:
            print_pass("Analytics Overview")
        else:
            print_fail("Analytics Overview")
            
        # Radar
        res = requests.get(f"{BASE_URL}/analytics/{user_id}/skills", headers=headers)
        if res.status_code == 200:
            print_pass("Skill Radar Data")
        else:
            print_fail("Skill Radar Data")
    except Exception as e:
        print_fail(f"Analytics Exception: {e}")

    # --- PHASE 6: DYNAMIC PATH & NOTIFICATIONS ---
    print("\n--- [Phase 6: Dynamic Path & Notifications] ---")
    try:
        # Check Notifications
        res = requests.get(f"{BASE_URL}/notifications/{user_id}", headers=headers)
        if res.status_code == 200:
            print_pass("Notifications API")
        else:
            print_fail("Notifications API")
            
        # Verify specific notification (from previous run)
        notes = res.json()
        fast_track = any("Fast-Track" in n["message"] for n in notes)
        if fast_track:
            print_pass("Fast-Track Alert Found (Phase 6 Logic Confirmed)")
        else:
            print(f"   ℹ️  Fast-Track alert not found in recent history. Run verify_phase6.py to force generate it.")
    except Exception as e:
        print_fail(f"Phase 6 Exception: {e}")

    # Cleanup
    if asset_id:
        requests.delete(f"{BASE_URL}/admin/assets/{asset_id}", headers=admin_headers)
        print("\n🧹 Cleanup: Test Asset Deleted")

    print("\n🏁 VERIFICATION COMPLETE")

if __name__ == "__main__":
    verify_system()
