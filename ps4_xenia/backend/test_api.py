import requests
import time

time.sleep(2)
r = requests.get('http://localhost:8001/api/v1/users/all')
print(f'✅ Status: {r.status_code}')
if r.ok:
    users = r.json()
    print(f'✅ Found {len(users)} users:')
    for u in users:
        print(f"  - {u['full_name']} ({u['email']})")
else:
    print(f'❌ Error: {r.json()}')
