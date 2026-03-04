"""
fix_imagin_images.py  v2
Uses imagin.studio free tier with CORRECT URL format.
Verified working format: https://cdn.imagin.studio/getimage?customer=img&car=ford-focus-2020&zoomType=fullscreen&angle=01
"""
import sqlite3, re

conn = sqlite3.connect('autoverse.db')
db = conn.cursor()

IMAGIN_BASE = "https://cdn.imagin.studio/getimage"
CUSTOMER    = "img"

def slug(s):
    return re.sub(r'[^a-z0-9\-]', '', s.lower().replace(' ', '-').replace('_','-'))

def make_url(brand, model, year, angle=1):
    car_str = f"{slug(brand)}-{slug(model)}-{year}"
    # angle must be zero-padded 2 digits: 01, 07, 22
    return f"{IMAGIN_BASE}?customer={CUSTOMER}&car={car_str}&zoomType=fullscreen&angle={angle:02d}"

cars = db.execute("SELECT id, brand, model, year FROM cars").fetchall()
total = len(cars)
print(f"Fixing {total} car imagin.studio URLs...")

for i, (car_id, brand, model, year) in enumerate(cars):
    ext  = make_url(brand, model, year, angle=1)
    intr = make_url(brand, model, year, angle=22)
    rear = make_url(brand, model, year, angle=7)

    db.execute(
        "UPDATE cars SET image_url=?, image_exterior=?, image_interior=?, image_rear=? WHERE id=?",
        (ext, ext, intr, rear, car_id)
    )
    if (i+1) % 200 == 0:
        conn.commit()
        print(f"  [{i+1}/{total}] done")

conn.commit()
conn.close()

# Print sample
sample = make_url('Ferrari','488',2024,1)
print(f"\n✅ Done! Sample URL: {sample}")
