import sqlite3

conn = sqlite3.connect('autoverse.db')
c = conn.cursor()

# 2026 Grid Roster (Approx) with reliable high-quality Wikipedia portrait shots
drivers_map = {
    'Max Verstappen': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Max_Verstappen_2017_Malaysia_2.jpg/400px-Max_Verstappen_2017_Malaysia_2.jpg',
    'Sergio Perez': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Sergio_Pérez_2019.jpg/400px-Sergio_Pérez_2019.jpg',
    'Lewis Hamilton': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Lewis_Hamilton_2_Malaysia_2016.jpg/400px-Lewis_Hamilton_2_Malaysia_2016.jpg',
    'Charles Leclerc': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Charles_Leclerc_2019.jpg/400px-Charles_Leclerc_2019.jpg',
    'Lando Norris': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Lando_Norris_2019.jpg/400px-Lando_Norris_2019.jpg',
    'Oscar Piastri': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Oscar_Piastri_2022.jpg/400px-Oscar_Piastri_2022.jpg',
    'George Russell': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/George_Russell_2019.jpg/400px-George_Russell_2019.jpg',
    'Kimi Antonelli': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Andrea_Kimi_Antonelli_Spielberg_2024.jpg/400px-Andrea_Kimi_Antonelli_Spielberg_2024.jpg',
    'Fernando Alonso': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Fernando_Alonso_2019.jpg/400px-Fernando_Alonso_2019.jpg',
    'Lance Stroll': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Lance_Stroll_2019.jpg/400px-Lance_Stroll_2019.jpg',
    'Pierre Gasly': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Pierre_Gasly_2019.jpg/400px-Pierre_Gasly_2019.jpg',
    'Jack Doohan': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Jack_Doohan_Spielberg_2022.jpg/400px-Jack_Doohan_Spielberg_2022.jpg',
    'Alex Albon': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Alexander_Albon_2019.jpg/400px-Alexander_Albon_2019.jpg',
    'Carlos Sainz': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Carlos_Sainz_Jr._2019.jpg/400px-Carlos_Sainz_Jr._2019.jpg',
    'Yuki Tsunoda': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Yuki_Tsunoda_2021.jpg/400px-Yuki_Tsunoda_2021.jpg',
    'Isack Hadjar': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Isack_Hadjar.jpg/400px-Isack_Hadjar.jpg',
    'Nico Hulkenberg': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Nico_Hülkenberg_2019.jpg/400px-Nico_Hülkenberg_2019.jpg',
    'Gabriel Bortoleto': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Gabriel_Bortoleto_2023.jpg/400px-Gabriel_Bortoleto_2023.jpg',
    'Kevin Magnussen': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Kevin_Magnussen_2019.jpg/400px-Kevin_Magnussen_2019.jpg',
    'Esteban Ocon': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Esteban_Ocon_2018.jpg/400px-Esteban_Ocon_2018.jpg',
    'Franco Colapinto': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Franco_Colapinto_Imola_2024.jpg/400px-Franco_Colapinto_Imola_2024.jpg',
    'Oliver Bearman': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Oliver_Bearman.jpg/400px-Oliver_Bearman.jpg'
}

for name, url in drivers_map.items():
    c.execute("UPDATE drivers SET image_url = ? WHERE name LIKE ?", (url, f"%{name}%"))

conn.commit()
conn.close()
print("Driver portraits synced to reliable HD URLs.")
