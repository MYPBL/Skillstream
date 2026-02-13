import requests
import time

BASE_URL = "http://localhost:8001/api/v1"

def run_analytics_verification():
    print("🧪 Starting Analytics Verification...")

    # 1. Login
    print("LOGIN: Authenticating as 'admin@example.com'...")
    res = requests.post(f"{BASE_URL}/auth/login", json={"email": "admin@example.com", "password": "password123"})
    if res.status_code != 200:
        print(f"❌ Login Failed: {res.text}")
        return
    
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get User ID
    me_res = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    user_id = me_res.json()["id"]
    print(f"✅ User ID: {user_id}")

    # 2. Get Initial Skills
    print("ANALYTICS: Fetching initial skill radar...")
    initial_skills = requests.get(f"{BASE_URL}/analytics/{user_id}/skills", headers=headers).json()
    print(f"ℹ️ Initial Skills: {initial_skills}")

    # 3. Simulate Module Completion with HIGH SCORE to boost skill
    # Need an asset ID. Let's list recommendations.
    rec_res = requests.get(f"{BASE_URL}/learning/{user_id}/recommendations", headers=headers)
    if not rec_res.json():
        print("⚠️ No recommendations found. Cannot simulate interaction.")
        return
    
    asset = rec_res.json()[0]
    print(f"INTERACTION: Completing asset '{asset['title']}' (Skill: {asset['skill_tag']}) with Score 100...")

    interaction_payload = {
        "user_id": user_id,
        "asset_id": asset["id"],
        "status": "completed",
        "score": 100,
        "time_spent_seconds": 300,
        "attempts": 1
    }
    # Interact endpoint returns the interaction object
    interact_res = requests.post(f"{BASE_URL}/learning/interact", json=interaction_payload, headers=headers)
    if interact_res.status_code == 200:
        print("✅ Interaction Recorded.")
    else:
        print(f"❌ Interaction Failed: {interact_res.text}")

    # 4. Verify Skill Update
    print("VERIFICATION: Checking if skill proficiency increased...")
    updated_skills = requests.get(f"{BASE_URL}/analytics/{user_id}/skills", headers=headers).json()
    
    # Find the skill
    target_skill = asset['skill_tag']
    old_prof = next((s['A'] for s in initial_skills if s['subject'] == target_skill), 0)
    new_prof = next((s['A'] for s in updated_skills if s['subject'] == target_skill), 0)
    
    print(f"Skill '{target_skill}': {old_prof} -> {new_prof}")
    
    if new_prof > old_prof:
        print("✅ SUCCESS: Skill Proficiency Increased!")
    elif new_prof == old_prof and new_prof == 100:
         print("✅ SUCCESS: Skill Proficiency Maxed Out!")
    else:
        print("❌ FAILURE: Skill Proficiency did not increase (or was new).") 
        # Note: If it was 0 and now >0, it worked. logic above handles update.
        if new_prof > 0 and old_prof == 0:
             print("✅ SUCCESS: New Skill Mastered!")

if __name__ == "__main__":
    run_analytics_verification()
