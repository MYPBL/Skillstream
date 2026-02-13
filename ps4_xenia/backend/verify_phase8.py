import requests
import json
import random
from typing import Dict

BASE_URL = "http://localhost:8001/api/v1"

def login(email: str, password: str) -> str:
    response = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    if response.status_code == 200:
        return response.json()["access_token"]
    print(f"Login failed: {response.text}")
    return None

def get_asset_with_quiz(token: str, user_id: str) -> Dict:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/learning/{user_id}/recommendations", headers=headers)
    if response.status_code == 200:
        assets = response.json()
        print(f"   Received {len(assets)} recommendations:")
        for asset in assets:
            print(f"   - {asset.get('title')}")
            # print(json.dumps(asset, indent=2)) # Debug full asset
            if asset.get("title") == "Decorators Explained":
                print(f"     DEBUG: quiz_data type: {type(asset.get('quiz_data'))}")
                print(f"     DEBUG: quiz_data value: {str(asset.get('quiz_data'))[:50]}...")
            
            if asset.get("quiz_data"):
                return asset
    else:
        print(f"❌ Failed to get recommendations. Status: {response.status_code}, Response: {response.text}")
    print("No asset with quiz data found.")
    return None

def submit_quiz(token: str, user_id: str, asset_id: str, score: int):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "user_id": user_id,
        "asset_id": asset_id,
        "status": "completed",
        "score": score,
        "time_spent_seconds": 120,
        "attempts": 1
    }
    response = requests.post(f"{BASE_URL}/learning/interact", json=payload, headers=headers)
    return response

def verify():
    print("🚀 Starting Phase 8 Verification...")
    
    # 1. Login/Register New User to ensure fresh recommendations
    import time
    email = f"test_phase8_{int(time.time())}@example.com"
    password = "password123"
    
    print(f"👤 Creating new user: {email}")
    reg_resp = requests.post(f"{BASE_URL}/auth/register", json={
        "email": email, 
        "password": password, 
        "full_name": "Phase8 Tester",
        "preferred_learning_style": "video",
        "target_skills": ["Python", "React"],
        "current_skills": ["HTML"]
    })
    
    token = login(email, password)
    
    # Get User ID
    user_resp = requests.get(f"{BASE_URL}/auth/me", headers={"Authorization": f"Bearer {token}"})
    if user_resp.status_code != 200:
         print(f"Failed to get user info: {user_resp.text}")
         return
    
    user_id = user_resp.json()["id"]
    print(f"👤 Logged in as User ID: {user_id}")

    # 2. Find Asset with Quiz
    asset = get_asset_with_quiz(token, user_id)
    if not asset:
        print("❌ Could not find an asset with quiz data to test.")
        return

    print(f"📝 Found Quiz Asset: {asset['title']} (ID: {asset['id']})")
    print(f"   Quiz Data Length: {len(asset['quiz_data'])}")

    # 3. Test High Score (Fast-Track)
    print("\n🧪 Testing High Score (90%)...")
    resp_high = submit_quiz(token, user_id, asset['id'], 90)
    if resp_high.status_code == 200:
        data = resp_high.json()
        print(f"   Message: {data.get('message')}")
        if data.get('next_recommendation'):
            print(f"   ✅ Received Next Recommendation: {data['next_recommendation']['title']}")
        else:
            print("   ℹ️ No specific recommendation (maybe no harder asset exists?)")
    else:
        print(f"   ❌ Failed: {resp_high.text}")

    # 4. Test Low Score (Remedial)
    print("\n🧪 Testing Low Score (40%)...")
    resp_low = submit_quiz(token, user_id, asset['id'], 40)
    if resp_low.status_code == 200:
        data = resp_low.json()
        print(f"   Message: {data.get('message')}")
        if data.get('remedial'):
            print("   ✅ Remedial flag set.")
            if data.get('cheatsheet'):
                print(f"   ✅ Received Cheatsheet Preview: {data['cheatsheet'][:50]}...")
            else:
                 print("   ❌ Cheatsheet missing.")
        else:
            print("   ❌ Remedial flag NOT set.")
    else:
        print(f"   ❌ Failed: {resp_low.text}")

if __name__ == "__main__":
    verify()
