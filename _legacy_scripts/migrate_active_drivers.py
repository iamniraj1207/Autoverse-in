import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'autoverse.db')
conn = sqlite3.connect(db_path)
db = conn.cursor()

ACTIVE_2026 = [
    'Max Verstappen', 'Lewis Hamilton', 'Charles Leclerc',
    'George Russell', 'Kimi Antonelli', 'Lando Norris', 
    'Oscar Piastri', 'Carlos Sainz', 'Alexander Albon',
    'Fernando Alonso', 'Lance Stroll', 'Pierre Gasly',
    'Jack Doohan', 'Nico Hulkenberg', 'Esteban Ocon',
    'Oliver Bearman', 'Isack Hadjar', 'Guanyu Zhou',
    'Valtteri Bottas', 'Gabriel Bortoleto', 'Liam Lawson'
]

# Reset everyone to 0 first (in case of re-run)
db.execute("UPDATE drivers SET is_active_2026 = 0")

# Set active drivers to 1
for name in ACTIVE_2026:
    db.execute("UPDATE drivers SET is_active_2026 = 1 WHERE name = ?", (name,))
    print(f"Active: {name}")

conn.commit()
conn.close()
print("Migration: is_active_2026 status updated")
