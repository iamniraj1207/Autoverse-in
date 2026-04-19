import sqlite3

db = sqlite3.connect('autoverse.db')
cursor = db.cursor()

# 1. FIXED OPENF1 CDN FOR LEWIS HAMILTON
hamilton_url = "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/L/LEWHAM01_Lewis_Hamilton/lewham01.png.transform/2col/image.png"
cursor.execute("UPDATE drivers SET image_url = ? WHERE name LIKE '%Lewis Hamilton%'", (hamilton_url,))

# 2. ALSO ENSURE OTHER KEY DRIVERS HAVE OPENF1 FALLBACKS
drivers = [
    ("Max Verstappen", "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/M/MAXVER01_Max_Verstappen/maxver01.png.transform/2col/image.png"),
    ("Lando Norris", "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/L/LANNOR01_Lando_Norris/lannor01.png.transform/2col/image.png"),
    ("Charles Leclerc", "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/C/CHALEC01_Charles_Leclerc/chalec01.png.transform/2col/image.png")
]

for name, url in drivers:
    cursor.execute("UPDATE drivers SET image_url = ? WHERE name = ?", (url, name))

db.commit()
db.close()
print("OPENF1 ASSET SYNC COMPLETE: Hamilton and top-tier drivers updated.")
