import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'autoverse.db')
conn = sqlite3.connect(db_path)
db = conn.cursor()

# Set image_url to ui-avatars for all drivers
# JS will override with wiki URL where available
DRIVER_AVATARS = [
  ('Max Verstappen',    '1E3A5F', 'ffffff'),
  ('Lewis Hamilton',    '8B0000', 'ffffff'),
  ('Charles Leclerc',   '6B0000', 'ffffff'),
  ('Lando Norris',      '7A3D00', 'ffffff'),
  ('Carlos Sainz',      '002080', 'ffffff'),
  ('George Russell',    '005A52', 'ffffff'),
  ('Oscar Piastri',     '7A3D00', 'ffffff'),
  ('Fernando Alonso',   '003830', 'ffffff'),
  ('Lance Stroll',      '003830', 'ffffff'),
  ('Pierre Gasly',      '003A70', 'ffffff'),
  ('Alexander Albon',   '002080', 'ffffff'),
  ('Nico Hulkenberg',   '3A3A3A', 'ffffff'),
  ('Esteban Ocon',      '3A3A3A', 'ffffff'),
  ('Guanyu Zhou',       '1A4A1A', 'ffffff'),
  ('Valtteri Bottas',   '1A4A1A', 'ffffff'),
  ('Kimi Antonelli',    '005A52', '000000'),
  ('Jack Doohan',       '003A70', 'ffffff'),
  ('Liam Lawson',       '1E3A5F', 'ffffff'),
  ('Oliver Bearman',    '6B0000', 'ffffff'),
  ('Isack Hadjar',      '0A1A70', 'ffffff'),
  ('Gabriel Bortoleto', '1A4A1A', 'ffffff'),
]

for name, bg, fg in DRIVER_AVATARS:
  encoded = name.replace(' ', '+')
  url = f"https://ui-avatars.com/api/?name={encoded}&size=400&background={bg}&color={fg}&bold=true&font-size=0.28&format=png"
  db.execute(
    "UPDATE drivers SET image_url=? WHERE name=?",
    (url, name)
  )
  print(f"Updated: {name}")

conn.commit()
conn.close()
print("All driver images fixed")
