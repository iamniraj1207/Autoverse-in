"""
bootstrap_data.py - High-performance seeding for AutoVerse (URL-only strategy)
1. Overhauls F1 2026 Grid with authentic portraits (Bottas/Perez)
2. Maps model-specific HD URLs for all cars (Lightweight storage)
3. Ensures busy_timeout for concurrent access
"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "autoverse.db")
con = sqlite3.connect(db_path, timeout=30)
cur = con.cursor()

def bootstrap():
    print("--- Starting fast-bootstrap (URL-only strategy) ---")
    
    # --- F1 2026 OVERHAUL ---
    cur.execute("DELETE FROM drivers")
    cur.execute("DELETE FROM teams")
    cur.execute("DELETE FROM timeline WHERE entity_type='driver'")

    teams = [
        (1, "Oracle Red Bull Racing", "Milton Keynes, UK", 6, 2005, 
         "https://upload.wikimedia.org/wikipedia/en/thumb/1/15/Red_Bull_Racing_logo.svg/512px-Red_Bull_Racing_logo.svg.png",
         "https://images.unsplash.com/photo-1628153361286-905a5a546ff6?auto=format&fit=crop&q=80&w=1200"),
        (2, "Scuderia Ferrari HP", "Maranello, Italy", 16, 1950,
         "https://upload.wikimedia.org/wikipedia/en/thumb/1/1f/Scuderia_Ferrari_HP_logo.svg/512px-Scuderia_Ferrari_HP_logo.svg.png",
         "https://images.unsplash.com/photo-1592198084033-aade902d1aae?auto=format&fit=crop&q=80&w=1200"),
        (11, "Cadillac Racing", "Detroit, USA", 0, 2026,
         "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Cadillac_logo.svg/512px-Cadillac_logo.svg.png",
         "https://images.unsplash.com/photo-1621135802920-133df287f89c?auto=format&fit=crop&q=80&w=1200")
    ]
    
    drivers = [
        ("Max Verstappen", "Dutch", 1, 4, 63, 2015, "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Max_Verstappen_2017_Malaysia_2.jpg/512px-Max_Verstappen_2017_Malaysia_2.jpg"),
        ("Lewis Hamilton", "British", 2, 7, 103, 2007, "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Lewis_Hamilton_2021_Styrian_GP_2.jpg/512px-Lewis_Hamilton_2021_Styrian_GP_2.jpg"),
        ("Valtteri Bottas", "Finnish", 11, 0, 10, 2013, "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Valtteri_Bottas_F1_2022.jpg/512px-Valtteri_Bottas_F1_2022.jpg"),
        ("Sergio Perez", "Mexican", 11, 0, 6, 2011, "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Sergio_P%C3%A9rez_F1_2022.jpg/512px-Sergio_P%C3%A9rez_F1_2022.jpg")
    ]

    cur.executemany("INSERT INTO teams (id, name, base, championships, founded, logo_url, car_image_url) VALUES (?,?,?,?,?,?,?)", teams)
    cur.executemany("INSERT INTO drivers (name, nationality, team_id, championships, wins, debut_year, image_url) VALUES (?,?,?,?,?,?,?)", drivers)
    
    # --- MODEL-SPECIFIC HD URLS ---
    model_images = {
        "Ferrari": "https://images.unsplash.com/photo-1592198084033-aade902d1aae?auto=format&fit=crop&q=80&w=1200",
        "Lamborghini": "https://images.unsplash.com/photo-1544636331-e26879cd4d9b?auto=format&fit=crop&q=80&w=1200",
        "Porsche": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&q=80&w=1200",
        "Pagani": "https://images.unsplash.com/photo-1542362567-b054cd1321c1?auto=format&fit=crop&q=80&w=1200"
    }
    default_img = "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&q=80&w=1200"

    cars = cur.execute("SELECT id, brand FROM cars").fetchall()
    for c_id, brand in cars:
        url = model_images.get(brand, default_img)
        cur.execute("UPDATE cars SET image_url = ? WHERE id = ?", (url, c_id))

    con.commit()
    print("Bootstrap complete. Database optimized (URLs only).")

if __name__ == "__main__":
    bootstrap()
    con.close()
