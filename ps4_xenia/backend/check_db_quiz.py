import sqlite3
import json

DB_PATH = "c:/samiksha/ps4_xenia/backend/pdp_dev.db"

def check():
    print(f"🕵️ Checking DB: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check Columns
    cursor.execute("PRAGMA table_info(asset)")
    cols = [r[1] for r in cursor.fetchall()]
    print(f"   Columns in 'asset' table: {cols}")
    
    if "quiz_data" not in cols:
        print("❌ 'quiz_data' column MISSING!")
        conn.close()
        return

    # Check Data
    cursor.execute("SELECT id, title, quiz_data FROM asset WHERE quiz_data IS NOT NULL")
    rows = cursor.fetchall()
    
    print(f"   Found {len(rows)} assets with quiz_data populated.")
    for r in rows:
        print(f"   - {r[1]} (ID: {r[0]}) | QuizData Len: {len(str(r[2]))} chars")

    conn.close()

if __name__ == "__main__":
    check()
