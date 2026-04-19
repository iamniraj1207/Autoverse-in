"""
fix_car_images.py
Updates all car image URLs to use the correct imagin.studio parameters.
Ensures angle is '01' (front 3/4) and not '010' or others that might show the 'curtain'.
"""
import sqlite3

conn = sqlite3.connect('autoverse.db')
db = conn.cursor()

cars = db.execute("SELECT id, brand, model FROM cars").fetchall()

for cid, brand, model in cars:
    # URL encoded parts
    enc_brand = brand.replace(' ', '%20')
    enc_model = model.replace(' ', '%20')
    
    # Premium URL for exterior
    # customer=img is often a fallback, we can try it.
    img_url = f"https://cdn.imagin.studio/getimage?customer=img&make={enc_brand}&modelFamily={enc_model}&angle=01&zoomType=fullscreen&transparent=true"
    
    db.execute("UPDATE cars SET image_url=?, image_exterior=? WHERE id=?", (img_url, img_url, cid))

conn.commit()
conn.close()
print("✓ Fixed all car image URLs in DB (angle=01)")
