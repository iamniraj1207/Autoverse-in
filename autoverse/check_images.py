import sqlite3
conn = sqlite3.connect('autoverse.db')
cur = conn.cursor()
rows = cur.execute("SELECT brand,model,image_url FROM cars LIMIT 5").fetchall()
for r in rows:
    print(f"{r[0]} {r[1]}: {r[2]}")
