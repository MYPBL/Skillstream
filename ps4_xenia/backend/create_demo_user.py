import requests
import sys

BASE_URL = "http://localhost:8001/api/v1"

def register_user(email, name, role):
    payload = {
        "email": email,
        "password": "password123",
        "full_name": name,
        "role": role,
        "preferred_learning_style": "video" if role == "junior" else "text"
    }
    try:
        resp = requests.post(f"{BASE_URL}/auth/register", json=payload)
        if resp.status_code == 200:
            print(f"✅ Created user: {email}")
        elif resp.status_code == 400 and "already exists" in resp.text:
            print(f"ℹ️  User already exists: {email} (Ready to login)")
        else:
            print(f"❌ Failed to create {email}: {resp.text}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    print("Creating Demo Users...")
    register_user("admin@example.com", "Admin Alice", "admin")
    register_user("newbie@example.com", "Newbie Ned", "employee")
    print("\nDone! You can now login.")
