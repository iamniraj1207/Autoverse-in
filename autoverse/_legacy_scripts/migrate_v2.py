import sqlite3

def migrate():
    conn = sqlite3.connect('autoverse.db')
    db = conn.cursor()
    
    # 1. Update cars table
    print("Migrating cars table...")
    try:
        db.execute("ALTER TABLE cars ADD COLUMN image_interior TEXT")
    except: pass
    try:
        db.execute("ALTER TABLE cars ADD COLUMN image_side TEXT")
    except: pass
    try:
        db.execute("ALTER TABLE cars ADD COLUMN image_rear TEXT")
    except: pass

    # 2. Create f1_cars table
    print("Creating f1_cars table...")
    db.execute("""
        CREATE TABLE IF NOT EXISTS f1_cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id INTEGER REFERENCES teams(id),
            season INTEGER,
            chassis TEXT,
            power_unit TEXT,
            tyres TEXT DEFAULT 'Pirelli',
            weight_kg INTEGER DEFAULT 798,
            description TEXT,
            first_race TEXT,
            notable_features TEXT
        )
    """)

    # 3. Create driver_strengths table
    print("Creating driver_strengths table...")
    db.execute("""
        CREATE TABLE IF NOT EXISTS driver_strengths (
            driver_id INTEGER REFERENCES drivers(id) UNIQUE,
            qualifying_pace INTEGER,
            race_pace INTEGER,
            wet_weather INTEGER,
            consistency INTEGER,
            experience INTEGER
        )
    """)
    
    # 4. Ensure is_active_2026 exists
    try:
        db.execute("ALTER TABLE drivers ADD COLUMN is_active_2026 INTEGER DEFAULT 1")
    except: pass

    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
