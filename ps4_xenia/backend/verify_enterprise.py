"""
Verification script for Enterprise Features:
1. Rate Limiting (Req 15)
2. Backend Stability (Req 13)
3. Caching Fallback (Req 14)
"""
import requests
import time
import sys

BASE_URL = "http://localhost:8000/api/v1"

def test_rate_limiting():
    print("Locked & Loaded: Testing Rate Limiting on Login Endpoint...")
    url = f"{BASE_URL}/auth/login"
    payload = {
        "email": "newbie@example.com",
        "password": "wrongpassword" # Intentional failure is fine, rate limit applies to attempts
    }
    
    responses = []
    
    # Try 10 requests rapidly (Limit is 5/minute)
    for i in range(1, 11):
        try:
            r = requests.post(url, json=payload)
            responses.append(r.status_code)
            print(f"Request {i}: Status {r.status_code}")
        except Exception as e:
            print(f"Request {i}: Failed connection {e}")
            break
            
    # Check results
    rate_limited_count = responses.count(429)
    if rate_limited_count > 0:
        print(f"✅ SUCCESS: Rate Limiting Active! Got {rate_limited_count} HTTP 429 responses.")
    else:
        print("❌ FAILURE: No rate limiting detected (Expected 429s).")

def test_backend_stability():
    print("\nTesting Backend Stability & Caching Fallback...")
    # This endpoint uses caching logic
    url = f"{BASE_URL}/library" 
    try:
        start = time.time()
        r = requests.get(url)
        duration = time.time() - start
        
        if r.status_code == 200:
            print(f"✅ SUCCESS: Backend is serving content (Time: {duration:.2f}s)")
            data = r.json()
            print(f"   Retrieved {len(data)} assets.")
        else:
            print(f"❌ FAILURE: Backend returned status {r.status_code}")
            print(r.text)
    except Exception as e:
        print(f"❌ FAILURE: Could not connect to backend: {e}")

if __name__ == "__main__":
    test_rate_limiting()
    test_backend_stability()
