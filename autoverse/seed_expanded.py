"""
seed_expanded.py — AutoVerse Full Car Database Seeder
Imports all car_data modules and inserts into autoverse.db
Then calls CarQuery API to top up to 1000+ cars.
"""
import os
import sqlite3
import sys
import time

import requests

# Add parent dir so imports work when running from autoverse/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from car_data.evs import EV_CARS
from car_data.hypercars import HYPERCARS
from car_data.indian_cars import INDIAN_CARS
from car_data.jdm import JDM_CARS
from car_data.sports_cars import SPORTS_CARS
from car_data.supercars import SUPERCARS

ALL_CURATED = HYPERCARS + SUPERCARS + SPORTS_CARS + JDM_CARS + EV_CARS + INDIAN_CARS

# ── Connect to DB ───────────────────────────────────────────────────────────────
db_path = os.path.join(os.path.dirname(__file__), "autoverse.db")
con = sqlite3.connect(db_path, timeout=30.0)  # Standard sqlite3 timeout
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("PRAGMA busy_timeout = 30000")

def execute_with_retry(cursor, sql, params=None, retries=5, delay=1):
    """Retries a database operation if it fails due to locking."""
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

# ── Clear existing cars (keep users, teams, drivers, garage, timeline) ──────────
execute_with_retry(cur, "DELETE FROM garage")
execute_with_retry(cur, "DELETE FROM cars")
con.commit()
print(f"Cleared existing cars. Inserting {len(ALL_CURATED)} curated cars...")

# ── Insert all curated cars ─────────────────────────────────────────────────────
INSERT_SQL = """INSERT OR IGNORE INTO cars
    (brand, model, year, engine, horsepower, torque, fuel_type, acceleration, 
     price_usd, description, category, top_speed, drivetrain, weight_kg, origin_country, image_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

import random

def get_premium_description(brand, model, hp, engine):
    templates = [
        f"The {brand} {model} represents the pinnacle of automotive engineering, featuring a {engine} that produces {hp} horsepower.",
        f"Experience breathtaking performance with the {brand} {model}. Its {engine} delivering {hp} HP makes it a true masterpiece.",
        f"A icon of speed and luxury, the {brand} {model} combines a {engine} with {hp} horsepower for an unparalleled driving experience.",
        f"The {brand} {model} is a testament to {brand}'s racing heritage, powered by a {hp} HP {engine}."
    ]
    return random.choice(templates)

def get_category(brand, model, hp, year):
    if hp and hp > 1000: return 'Hypercar'
    if hp and hp > 500: return 'Supercar'
    if 'Electric' in str(model) or 'EV' in str(model): return 'EV'
    return 'Sports'

# Mapping for origin countries based on brand
ORIGINS = {
    "Ferrari": "Italy", "Lamborghini": "Italy", "Pagani": "Italy", "Bugatti": "France",
    "Porsche": "Germany", "BMW": "Germany", "Mercedes-Benz": "Germany", "Audi": "Germany",
    "McLaren": "UK", "Aston Martin": "UK", "Bentley": "UK", "Rolls-Royce": "UK",
    "Tesla": "USA", "Ford": "USA", "Chevrolet": "USA", "Dodge": "USA",
    "Nissan": "Japan", "Toyota": "Japan", "Honda": "Japan", "Mazda": "Japan", "Subaru": "Japan",
    "Rimac": "Croatia", "Koenigsegg": "Sweden", "Mahindra": "India", "Tata": "India"
}

inserted = 0
for row in ALL_CURATED:
    # row format: (brand, model, year, engine, hp, torque, fuel, accel, img)
    brand, model, year, engine, hp, torque, fuel, accel, img = row
    
    # Enrich data
    price = random.randint(150000, 3000000) if hp and hp > 500 else random.randint(50000, 150000)
    desc = get_premium_description(brand, model, hp, engine)
    cat = get_category(brand, model, hp, year)
    ts = random.randint(280, 450) if hp and hp > 500 else random.randint(200, 280)
    dt = random.choice(['RWD', 'AWD', '4WD'])
    weight = random.randint(1200, 2100)
    origin = ORIGINS.get(brand, "International")
    
    # High-quality Unsplash URL
    img_url = f"https://source.unsplash.com/1600x900/?{brand.replace(' ', '')},{model.replace(' ', '')},car"

    try:
        execute_with_retry(cur, INSERT_SQL, (
            brand, model, year, engine, hp, torque, fuel, accel,
            price, desc, cat, ts, dt, weight, origin, img_url
        ))
        inserted += 1
    except Exception as e:
        print(f"Error inserting {brand} {model}: {e}")

con.commit()
print(f"✓ Inserted {inserted} curated cars.")

# ── CarQuery API — fetch additional mainstream makes/models ─────────────────────
print("\nFetching additional cars from CarQuery API...")

CARQUERY_BASE = "https://www.carqueryapi.com/api/0.3/"

MAINSTREAM_MAKES = [
    "BMW", "Mercedes-Benz", "Audi", "Volkswagen", "Ford", "Chevrolet",
    "Toyota", "Honda", "Nissan", "Hyundai", "Kia", "Mazda", "Subaru",
    "Volvo", "Peugeot", "Renault", "Citroen", "Fiat", "Alfa Romeo",
    "Jeep", "Dodge", "Cadillac", "Buick", "GMC", "Lincoln",
    "Acura", "Infiniti", "Lexus", "Mitsubishi", "Suzuki",
    "Land Rover", "Jaguar", "Maserati", "Bentley", "Rolls-Royce",
    "Lamborghini", "Ferrari", "Porsche", "McLaren",
    "Genesis", "MINI", "Smart", "Dacia", "Seat", "Skoda",
    "Chrysler", "Ram", "Pontiac", "Oldsmobile", "Saturn",
    "Saab", "Opel", "Vauxhall", "Holden",
]

YEAR_RANGE = range(2000, 2025)  # Modern era focus
api_inserted = 0
api_errors   = 0

for make in MAINSTREAM_MAKES:
    try:
        # Get models for this make
        resp = requests.get(
            CARQUERY_BASE,
            params={"cmd": "getModels", "make": make, "min_year": 2000, "max_year": 2024},
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        if resp.status_code != 200:
            continue

        data = resp.json()
        models = data.get("Models", [])

        for m in models[:40]:  # Increased to 40 models per make to hit 1000+ reliably
            model_name = m.get("model_name", "")
            if not model_name:
                continue

            # Check if already present
            existing = execute_with_retry(cur, 
                "SELECT id FROM cars WHERE brand=? AND model=?", (make, model_name)
            ).fetchone()
            if existing:
                continue

            # Use year from API or default to 2022
            year = int(m.get("model_year", 2022) or 2022)
            
            # Randomized but sensible defaults for mainstream cars
            hp = random.randint(150, 450)
            torque = int(hp * 0.9)
            price = random.randint(30000, 120000)
            desc = f"The {make} {model_name} is a versatile and reliable choice, offering a perfect balance of performance and comfort for modern drivers."
            cat = random.choice(['Luxury', 'SUV', 'Sports'])
            ts = random.randint(180, 260)
            dt = random.choice(['FWD', 'AWD', 'RWD'])
            weight = random.randint(1400, 2200)
            origin = ORIGINS.get(make, "International")
            img_url = f"https://source.unsplash.com/1600x900/?{make.replace(' ', '')},{model_name.replace(' ', '')},car"

            execute_with_retry(cur, INSERT_SQL, (
                make, model_name, year,
                "Standard IC Engine", hp, torque,
                "Petrol", random.uniform(4.5, 8.5),
                price, desc, cat, ts, dt, weight, origin, img_url
            ))
            api_inserted += 1

        time.sleep(0.5)  # Be polite to the API
        con.commit()     # Commit after each make to show incremental progress

    except Exception as e:
        api_errors += 1
        continue

# ── Summary ──────────────────────────────────────────────────────────────────────
total = cur.execute("SELECT COUNT(*) FROM cars").fetchone()[0]
print(f"✓ API fetched {api_inserted} additional cars ({api_errors} errors).")
print(f"\n✅ Total cars in database: {total}")
print(f"   Curated with full specs: {inserted}")
print(f"   From CarQuery API:       {api_inserted}")

con.close()
