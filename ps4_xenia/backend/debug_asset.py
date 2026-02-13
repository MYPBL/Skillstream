import sqlite3
import json

DB_PATH = "c:/samiksha/ps4_xenia/backend/pdp_dev.db"

def check():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🔍 Checking Asset: 'Decorators Explained'")
    cursor.execute("SELECT id, title, skill_tag, quiz_data FROM asset WHERE title LIKE '%Decorators%'")
    rows = cursor.fetchall()
    
    if not rows:
        print("❌ Asset not found.")
    
    for r in rows:
        print(f"   ID: {r[0]}")
        print(f"   Title: {r[1]}")
        print(f"   Skill Tag: {r[2]}")
        print(f"   Quiz Data: {'✅ Present' if r[3] else '❌ MISSING'}")

    conn.close()

if __name__ == "__main__":
    check()
