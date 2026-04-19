import sqlite3

db = sqlite3.connect('autoverse.db')
cursor = db.cursor()

# 1. IMAGIN.STUDIO & WIKIMEDIA IMAGE RE-CALIBRATION
# Using imagin.studio for production-grade car visuals (simulated if key missing)
# And pure Wikimedia for F1.

legends = {
    "Michael Schumacher": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Michael_Schumacher_2012_Canada_GP.jpg",
    "Alain Prost": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Alain_Prost_2014.jpg",
    "Ayrton Senna": "https://upload.wikimedia.org/wikipedia/commons/0/07/Ayrton_Senna_8_-_Senna_vence_em_Interlagos%2C_1991.jpg",
    "Niki Lauda": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Niki_Lauda_1982.jpg"
}

for name, url in legends.items():
    cursor.execute("UPDATE drivers SET image_url = ? WHERE name = ?", (url, name))

# Imagin.studio dynamic URL generator for Cars
cursor.execute("SELECT id, brand, model FROM cars")
cars = cursor.fetchall()

def get_imagin_url(brand, model):
    b = brand.lower().replace(" ", "-")
    m = model.lower().replace(" ", "-")
    return f"https://cdn.imagin.studio/getImage?customer=hr-autoverse&make={b}&modelFamily={m}&zoomType=fullscreen"

for cid, brand, model in cars:
    img = get_imagin_url(brand, model)
    cursor.execute("""
        UPDATE cars SET 
        image_exterior = ?, 
        image_interior = ?,
        gallery_img_1 = ?,
        gallery_img_2 = ?
        WHERE id = ?
    """, (img, img, img, img, cid))

db.commit()
db.close()
print("HYBRID IMAGE LOADERS CALIBRATED: Imagin.studio & Wikimedia active.")
