import sqlite3

try:
    conn = sqlite3.connect('autoverse.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, championships FROM drivers WHERE name LIKE '%Lando%';")
    row = cursor.fetchone()
    if row:
        print(f"Verified: {row[0]} has {row[1]} championships.")
    else:
        print("Driver not found.")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
