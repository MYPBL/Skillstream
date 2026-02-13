"""
Dynamic Professional Development Platform - LIVE DEMO
Scenario:
1. Admin manages learning assets (Content Layer).
2. User 'Newbie Ned' logs in and updates profile (User Layer).
3. User browses the library to find content (Discovery Layer).
"""
import requests
import json
import time

BASE_URL = "http://localhost:8001/api/v1"

def print_section(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def print_action(text):
    print(f"\n👉 {text}")

def print_success(text):
    print(f"   ✅ {text}")

def print_info(label, data):
    print(f"   ℹ️  {label}: {data}")

def login(email, password, role_name):
    print_action(f"Logging in as {role_name} ({email})...")
    response = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    if response.status_code == 200:
        token = response.json()['access_token']
        print_success("Login successful")
        return {"Authorization": f"Bearer {token}"}
    else:
        print(f"❌ Login failed: {response.text}")
        exit(1)

# --- DEMO START ---
print_section("🎬 STARTING LIVE DEMO")

# 1. Admin Workflow
print_section("PART 1: ADMIN - CONTENT MANAGEMENT")
admin_headers = login("admin@example.com", "password123", "Admin")

print_action("Creating a new Premium Asset...")
new_asset = {
    "title": "Advanced Microservices with FastAPI",
    "description": "Deep dive into event-driven architecture.",
    "content_type": "video",
    "content_url": "https://example.com/microservices.mp4",
    "skill_tag": "FastAPI",
    "difficulty_level": 5,
    "estimated_duration_minutes": 120
}
response = requests.post(f"{BASE_URL}/admin/assets", json=new_asset, headers=admin_headers)
asset = response.json()
asset_id = asset['id']
print_success(f"Asset Created: '{asset['title']}'")
print_info("Version", asset['current_version'])
print_info("ID", asset_id)

print_action("Updating Asset Content (Triggering Versioning)...")
update_data = {
    "content_url": "https://example.com/microservices-v2.mp4",
    "description": "Updated with new patterns."
}
response = requests.patch(f"{BASE_URL}/admin/assets/{asset_id}", json=update_data, headers=admin_headers)
updated_asset = response.json()
print_success("Asset Updated")
print_info("New Version", updated_asset['current_version'])


# 2. User Workflow
print_section("PART 2: USER - PROFILE & DISCOVERY")
user_headers = login("newbie@example.com", "password123", "User 'Newbie Ned'")

print_action("Fetching User Profile...")
response = requests.get(f"{BASE_URL}/profile", headers=user_headers)
profile = response.json()
print_success(f"Welcome, {profile['full_name']}!")
print_info("Role", profile['role'])
print_info("Skills", profile['current_skills'])

print_action("Updating Learning Goals...")
update_data = {
    "target_skills": ["FastAPI", "Microservices"]
}
requests.patch(f"{BASE_URL}/profile", json=update_data, headers=user_headers)
print_success("Goals updated -> 'FastAPI', 'Microservices'")

print_action("Browsing Asset Library (Searching for 'Microservices')...")
response = requests.get(f"{BASE_URL}/library", headers=user_headers)
library = response.json()

# Filter client side for demo visual
found = [a for a in library if 'Microservices' in a['title']]
if found:
    print_success(f"Found {len(found)} relevant asset(s)")
    for item in found:
        print(f"      - 📖 {item['title']} (Complexity: {item['difficulty_level']}/5)")
else:
    print("   ❌ No assets found")

print_action("Checking Learning Dashboard & Recommendations...")
# Get user ID from profile
user_id = profile['id']
# 1. Dashboard
resp = requests.get(f"{BASE_URL}/learning/dashboard/{user_id}", headers=user_headers)
if resp.status_code == 200:
    dash = resp.json()
    print_success(f"Dashboard Loaded: Level '{dash.get('current_level')}', Avg Score {dash.get('average_score')}%")
else:
    print(f"   ❌ Dashboard Failed: {resp.status_code} {resp.text}")

# 2. Next Recommendation (Verification of Adaptive Engine Fix)
resp = requests.get(f"{BASE_URL}/learning/{user_id}/recommendations", headers=user_headers)
if resp.status_code == 200:
    recs = resp.json()
    print_success(f"Adaptive Recommendations ({len(recs)}):")
    for r in recs:
        print(f"      - ⭐ {r.get('title')} ({r.get('content_type')}, Lvl {r.get('difficulty_level')})")
elif resp.status_code == 404:
    print_info("Adaptive Recommendations", "No recommendations available")
else:
    print(f"   ❌ Recommendation Failed: {resp.status_code} {resp.text}")


# 3. Cleanup
print_section("PART 3: CLEANUP")
print_action("Archiving Demo Asset...")
requests.delete(f"{BASE_URL}/admin/assets/{asset_id}", headers=admin_headers)
print_success("Asset Archived")

print_action("Verifying Asset is Hidden from User...")
response = requests.get(f"{BASE_URL}/library/{asset_id}", headers=user_headers)
if response.status_code == 404:
    print_success("Asset successfully hidden from visibility")

print_section("🎉 DEMO COMPLETE")
