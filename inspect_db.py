import sqlite3, sys
conn = sqlite3.connect('autoverse.db')
cur = conn.cursor()
sys.stdout.reconfigure(encoding='utf-8')

t = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print("Tables:", t)
print()

print("=== DRIVERS ===")
rows = cur.execute("SELECT id,name,championships,wins,debut_year,is_active_2026 FROM drivers ORDER BY championships DESC LIMIT 50").fetchall()
for r in rows:
    print(f"id={r[0]:3d} | {r[1]:<28} | wdc={r[2]:2d} | w={r[3]:3d} | debut={r[4]} | active={r[5]}")

print()
print("=== TEAMS ===")
rows = cur.execute("SELECT id,name,is_active_2026,primary_color,logo_url FROM teams").fetchall()
for r in rows:
    print(f"id={r[0]:3d} | {r[1]:<28} | active={r[2]} | {r[3]} | logo={r[4]}")

conn.close()
