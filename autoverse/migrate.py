import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'autoverse.db')
conn = sqlite3.connect(db_path)

migrations = [
    "ALTER TABLE drivers ADD COLUMN image_fallback1 TEXT",
    "ALTER TABLE drivers ADD COLUMN birth_place TEXT",
    "ALTER TABLE drivers ADD COLUMN bio TEXT",
    "ALTER TABLE teams ADD COLUMN car_image_url TEXT",
    "ALTER TABLE teams ADD COLUMN primary_color TEXT",
    "ALTER TABLE teams ADD COLUMN bio TEXT",
]

print("Starting migrations...")
for sql in migrations:
    try:
        conn.execute(sql)
        print(f"OK: {sql}")
    except Exception as e:
        print(f"SKIP (exists or error): {e}")

conn.commit()
conn.close()
print("Migration complete.")
