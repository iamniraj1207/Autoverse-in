"""
seed.py — Populate AutoVerse DB with sample data.
Standardized on native sqlite3 with busy_timeout for reliability.
"""
import sqlite3
import os
import time
from werkzeug.security import generate_password_hash

db_path = os.path.join(os.path.dirname(__file__), "autoverse.db")
con = sqlite3.connect(db_path, timeout=30.0)
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("PRAGMA busy_timeout = 30000")

def execute_with_retry(cursor, sql, params=None, retries=5, delay=1):
    for i in range(retries):
        try:
            if params:
                return cursor.execute(sql, params)
            else:
                return cursor.execute(sql)
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower() and i < retries - 1:
                time.sleep(delay)
                continue
            raise e

# ── Clear existing data ─────────────────────────────────────
for table in ["timeline", "garage", "cars", "users"]:
    execute_with_retry(cur, f"DELETE FROM {table}")

# ── Users ───────────────────────────────────────────────────
execute_with_retry(cur, "INSERT INTO users (username, hash) VALUES (?, ?)",
           ("demo", generate_password_hash("password123")))

# F1 data handled by expand_2026_data.py

# ── Cars ────────────────────────────────────────────────────
cars_data = [
    ("Ferrari",   "F40",               1992, "Twin-Turbo V8",       478,  426, "Petrol",   4.2),
    ("Ferrari",   "SF90 Stradale",     2019, "3.9L Twin-Turbo V8 + 3 e-motors", 986, 590, "Hybrid", 2.5),
    ("Lamborghini","Huracán EVO",      2019, "5.2L V10",            640,  443, "Petrol",   2.9),
    ("Lamborghini","Aventador SVJ",    2018, "6.5L V12",            770,  531, "Petrol",   2.8),
    ("Porsche",   "911 GT3 RS",        2022, "4.0L Flat-6",         518,  346, "Petrol",   3.2),
    ("Porsche",   "Taycan Turbo S",    2023, "Electric Dual Motor", 750,  774, "Electric", 2.4),
    ("McLaren",   "720S",              2017, "4.0L Twin-Turbo V8",  710,  568, "Petrol",   2.8),
    ("McLaren",   "P1",                2013, "3.8L Twin-Turbo V8 + Electric", 916, 664, "Hybrid", 2.8),
    ("Bugatti",   "Veyron",            2005, "8.0L W16",            1001, 922, "Petrol",   2.5),
    ("Bugatti",   "Chiron Super Sport",2021, "8.0L W16",            1578,1180, "Petrol",   2.4),
    ("Mercedes",  "AMG GT Black Series",2020,"4.0L Twin-Turbo V8",  730,  590, "Petrol",   3.1),
    ("BMW",       "M3 Competition",    2021, "3.0L Inline-6",       503,  479, "Petrol",   3.9),
    ("Aston Martin","Valkyrie",        2021, "6.5L V12 + Electric", 1139, 664, "Hybrid",   2.5),
    ("Koenigsegg","Jesko Absolut",     2020, "5.0L V8 Twin-Turbo",  1600,1106, "E85/Petrol",2.5),
    ("Rimac",     "Nevera",            2021, "Electric Quad Motor", 1914,2300, "Electric", 1.8),
]

for row in cars_data:
    execute_with_retry(cur, "INSERT INTO cars (brand, model, year, engine, horsepower, torque, fuel_type, acceleration) VALUES (?,?,?,?,?,?,?,?)", row)

# ── Timelines ────────────────────────────────────────────────
events = [
    ("driver", 1, 2015, "F1 Debut", "Became youngest driver to start an F1 race at 17."),
    ("driver", 1, 2016, "First Win", "Won the Spanish GP on his Red Bull debut — youngest F1 winner ever."),
    ("driver", 1, 2021, "World Champion", "Won his first world championship in a dramatic Abu Dhabi finale."),
    ("driver", 3, 2007, "F1 Debut", "Nearly won the championship in his debut season with McLaren."),
    ("driver", 6, 1984, "F1 Debut", "Joined Toleman, showing raw pace in the rain at Monaco.")
]
for ev in events:
    execute_with_retry(cur, "INSERT INTO timeline (entity_type, entity_id, year, title, description) VALUES (?,?,?,?,?)", ev)

con.commit()
con.close()
print("✓ Database seeded successfully (native sqlite3).")
print("  → Demo login: username=demo / password=password123")
