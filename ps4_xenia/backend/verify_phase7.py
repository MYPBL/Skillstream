import requests
import time

BASE_URL = "http://localhost:8001"

def verify_phase7():
    print("🚀 Starting Phase 7 Verification...")
    
    # 1. Check Health & Redis
    try:
        res = requests.get(f"{BASE_URL}/health")
        data = res.json()
        print(f"✅ Health Check: {data['status']}")
        print(f"   Database: {data['database']}")
        print(f"   Redis: {data['redis']}")
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")

    # 2. Check Rate Limiting
    print("\n⚡ Testing Rate Limiting (Spamming /health)...")
    success_count = 0
    blocked_count = 0
    
    for i in range(10):
        res = requests.get(f"{BASE_URL}/health")
        if res.status_code == 200:
            success_count += 1
            print(f"   Request {i+1}: 200 OK")
        elif res.status_code == 429:
            blocked_count += 1
            print(f"   Request {i+1}: 429 Too Many Requests (Blocked!)")
        
    if blocked_count > 0:
        print(f"✅ Rate Limiting Active! ({blocked_count} requests blocked)")
    else:
        print(f"⚠️ Rate Limiting NOT triggered (Limit is 5/min, ensure you spammed enough)")

if __name__ == "__main__":
    verify_phase7()
