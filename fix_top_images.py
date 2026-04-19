import sqlite3

db = sqlite3.connect('autoverse.db')
cursor = db.cursor()

# Lotus Evija Fix
cursor.execute("UPDATE cars SET image_url = ? WHERE model = 'Evija'", 
               ('https://images.unsplash.com/photo-1621135802920-133df287f89c?auto=format&fit=crop&q=80&w=1200',))

# Rimac Nevera Fix
cursor.execute("UPDATE cars SET image_url = ? WHERE model = 'Nevera'", 
               ('https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?auto=format&fit=crop&q=80&w=1200',))

# Agera RS / Jesko Fix
cursor.execute("UPDATE cars SET image_url = ? WHERE brand = 'Koenigsegg'", 
               ('https://images.unsplash.com/photo-1627454820516-dc767abc4eb3?auto=format&fit=crop&q=80&w=1200',))

db.commit()
db.close()
print("Top Hypercar Images Sanitized.")
