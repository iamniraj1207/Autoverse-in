import sqlite3
import json
import random

db = sqlite3.connect('autoverse.db')
cursor = db.cursor()

# 1. FIX F1 LEGENDS (HIGH-RES WIKIMEDIA)
legends = [
    ("Michael Schumacher", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Michael_Schumacher_F1_2012_Canada.jpg/800px-Michael_Schumacher_F1_2012_Canada.jpg"),
    ("Alain Prost", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Alain_Prost_Goodwood_2014_%28cropped%29.jpg/800px-Alain_Prost_Goodwood_2014_%28cropped%29.jpg"),
    ("Ayrton Senna", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Ayrton_Senna_1989.jpg/800px-Ayrton_Senna_1989.jpg"),
    ("Niki Lauda", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Niki_Lauda_1982.jpg/800px-Niki_Lauda_1982.jpg"),
]

for name, url in legends:
    cursor.execute("UPDATE drivers SET image_url = ? WHERE name = ?", (url, name))

# 2. FIX CONSTRUCTOR IMAGES & COLORS
# Ensuring all 2026 teams have valid logos and colors
teams = [
    ("Ferrari", "#ED1131", "https://upload.wikimedia.org/wikipedia/en/thumb/d/d5/Scuderia_Ferrari_Logo.svg/1200px-Scuderia_Ferrari_Logo.svg.png"),
    ("Red Bull Racing", "#23326A", "https://upload.wikimedia.org/wikipedia/en/thumb/a/a7/Red_Bull_Racing_logo.svg/1200px-Red_Bull_Racing_logo.svg.png"),
    ("Mercedes", "#00D2BE", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Mercedes_AMG_Petronas_F1_Logo.png/1200px-Mercedes_AMG_Petronas_F1_Logo.png"),
    ("McLaren", "#FF8700", "https://upload.wikimedia.org/wikipedia/en/thumb/1/12/McLaren_Racing_logo.svg/1200px-McLaren_Racing_logo.svg.png"),
    ("Aston Martin", "#006F62", "https://upload.wikimedia.org/wikipedia/en/thumb/9/9f/Aston_Martin_F1_Team_Logo.svg/1200px-Aston_Martin_F1_Team_Logo.svg.png"),
    ("Alpine", "#0090FF", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Alpine_F1_Team_Logo.svg/1200px-Alpine_F1_Team_Logo.svg.png"),
    ("Williams", "#005AFF", "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Williams_Racing_Logo.svg/1200px-Williams_Racing_Logo.svg.png"),
    ("Haas", "#FFFFFF", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Haas_F1_Team_logo.svg/1200px-Haas_F1_Team_logo.svg.png"),
    ("Audi F1 Team", "#F50537", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Audi_2016_logo.svg/1200px-Audi_2016_logo.svg.png"),
]

for name, color, logo in teams:
    cursor.execute("UPDATE teams SET primary_color = ?, logo_url = ? WHERE name = ?", (color, logo, name))

# 3. FIX CAR IMAGES (2 Visible + WIKIMEDIA/PIXABAY Fallbacks)
# We limit to specific, verified URLs
car_images = {
    "Porsche": [
        "https://images.unsplash.com/photo-1503376710356-748fe9c73b06?w=1200",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Porsche_911_GT3_RS_991_Gen_2_Silver.jpg/1200px-Porsche_911_GT3_RS_991_Gen_2_Silver.jpg"
    ],
    "Ferrari": [
        "https://images.unsplash.com/photo-1592198084033-aade902d1aae?w=1200",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Ferrari_458_Italia_--_05-18-2011.jpg/1200px-Ferrari_458_Italia_--_05-18-2011.jpg"
    ],
    "Lamborghini": [
        "https://images.unsplash.com/photo-1544636331-e268592033c2?w=1200",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Lamborghini_Aventador_LP700-4_Roadster_Front.jpg/1200px-Lamborghini_Aventador_LP700-4_Roadster_Front.jpg"
    ]
}

# Update cars with verified URLs
cursor.execute("SELECT id, brand FROM cars")
all_cars = cursor.fetchall()
for cid, brand in all_cars:
    img_set = car_images.get(brand, car_images["Porsche"]) # Fallback to Porsche if brand not in list
    cursor.execute("""
        UPDATE cars SET 
        image_exterior = ?, 
        image_interior = ?,
        gallery_img_1 = ?,
        gallery_img_2 = ?,
        gallery_img_3 = ?
        WHERE id = ?
    """, (img_set[0], img_set[1], img_set[0], img_set[1], img_set[0], cid))

db.commit()
db.close()
print("SUCCESS: F1 Legends corrected, Team Assets updated, and Car Images limited.")
