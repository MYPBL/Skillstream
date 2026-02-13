import requests
import time

BASE_URL = "http://localhost:8001/api/v1"

def run_phase6_verification():
    print("🚀 Starting Phase 6 (Dynamic Path) Verification...")
    
    # 1. Login
    login_res = requests.post(f"{BASE_URL}/auth/login", json={"email": "admin@example.com", "password": "password123"})
    if login_res.status_code != 200:
        print("❌ Login failed.")
        return
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    me = requests.get(f"{BASE_URL}/auth/me", headers=headers).json()
    user_id = me["id"]
    print(f"✅ Logged in as {user_id}")

    # 2. Reset Skills (Optional, but good for repeatable tests)
    # Since we can't easily reset via API, we'll pick a new skill or just assume increment.
    # Let's Pick "Machine Learning" if available, or just use Python and push it higher.
    
    # 3. Complete a module with HIGH score to trigger > 80% mastery
    # For this test, we'll manually hit the interact endpoint for an asset with skill "Advanced Systems"
    # We need an asset ID. We'll pick one from recommendations or just mock one if the backend allows mock asset IDs (it doesn't, Foreign Key constraint).
    # So we must use a real asset.
    # Let's fetch recommendations, pick one.
    rec = requests.get(f"{BASE_URL}/learning/{user_id}/recommendations", headers=headers).json()
    if not rec:
        print("⚠️ No recommendations. Cannot verify.")
        return
    
    asset = rec[0]
    skill = asset['skill_tag']
    print(f"🎯 Targeting Skill: {skill}")

    # We need to loop interactions until mastery > 80.
    # Or just send a massive score boost? Logic: min(100, current + difficulty * 2 * score/100)
    # If difficulty is 5, boost is 10. If current is 4, we need 8 interactions.
    # To speed up, we can simulate multiple interactions.
    
    print("⚡ Boosting Skill Proficiency...")
    for i in range(50):
        res = requests.post(f"{BASE_URL}/learning/interact", json={
            "user_id": user_id,
            "asset_id": asset['id'],
            "status": "completed",
            "score": 100,
            "time_spent_seconds": 60,
            "attempts": 1
        }, headers=headers)
        
        # Check current mastery
        skills = requests.get(f"{BASE_URL}/analytics/{user_id}/skills", headers=headers).json()
        prof = next((s['A'] for s in skills if s['subject'] == skill), 0)
        print(f"   Iteration {i+1}: Proficiency = {prof}")
        
        if prof >= 80:
             print("✨ Threshold 80% reached!")
             break
        time.sleep(0.1)

    # 4. Check Notifications
    print("🔔 Checking for Notifications...")
    notes = requests.get(f"{BASE_URL}/api/v1/notifications/{user_id}", headers=headers) 
    # Wait, in main.py prefix is /api/v1, router prefix is /notifications -> /api/v1/notifications
    # BUT logic in main.py: app.include_router(notifications.router, prefix="/api/v1", tags=["notifications"])
    # notifications.router has @router.get("/notifications/{user_id}")
    # So URL is /api/v1/notifications/{user_id}
    # Wait, if router has /notifications and prefix is /api/v1, result is /api/v1/notifications/{user_id}. Correct.
    
    notes_res = requests.get(f"{BASE_URL}/notifications/{user_id}", headers=headers)
    
    found = False
    if notes_res.status_code == 200:
        for note in notes_res.json():
            print(f"   - {note['message']}")
            if "Fast-Track" in note['message'] and skill in note['message']:
                found = True
    
    if found:
        print("✅ SUCCESS: 'Fast-Track' Notification received!")
    else:
        print("❌ FAILURE: Notification not found (or proficiency didn't reach 80).")

if __name__ == "__main__":
    run_phase6_verification()
