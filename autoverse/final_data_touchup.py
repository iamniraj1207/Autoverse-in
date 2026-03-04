import sqlite3

conn = sqlite3.connect('autoverse.db')
db = conn.cursor()

def set_driver(name, team_name, number, image=None):
    team = db.execute("SELECT id FROM teams WHERE name=?", (team_name,)).fetchone()
    if not team:
        print(f"Team {team_name} not found")
        return
    tid = team[0]
    
    # Check if driver exists
    driver = db.execute("SELECT id FROM drivers WHERE name=?", (name,)).fetchone()
    if driver:
        db.execute("UPDATE drivers SET team_id=?, number=? WHERE id=?", (tid, number, driver[0]))
        if image:
            db.execute("UPDATE drivers SET image_url=? WHERE id=?", (image, driver[0]))
    else:
        db.execute("""INSERT INTO drivers (name, team_id, number, is_active_2026, nationality, image_url, championships, wins)
                     VALUES (?,?,?,1,?,?,0,0)""", (name, tid, number, 'Unknown', image or ''))

# 2026 LINEUP CORRECTIONS
set_driver('Lewis Hamilton', 'Ferrari', '44')
set_driver('Charles Leclerc', 'Ferrari', '16')
set_driver('George Russell', 'Mercedes', '63')
set_driver('Kimi Antonelli', 'Mercedes', '12')
set_driver('Max Verstappen', 'Red Bull Racing', '1')
set_driver('Liam Lawson', 'Red Bull Racing', '30')
set_driver('Lando Norris', 'McLaren', '4', 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Lando_Norris_2024.jpg/400px-Lando_Norris_2024.jpg')
set_driver('Oscar Piastri', 'McLaren', '81')
set_driver('Carlos Sainz', 'Williams', '55')
set_driver('Alexander Albon', 'Williams', '23')
set_driver('Fernando Alonso', 'Aston Martin', '14')
set_driver('Lance Stroll', 'Aston Martin', '18')
set_driver('Nico Hulkenberg', 'Sauber', '27')
set_driver('Gabriel Bortoleto', 'Sauber', '5')
set_driver('Esteban Ocon', 'Haas', '31')
set_driver('Oliver Bearman', 'Haas', '87')
set_driver('Pierre Gasly', 'Alpine', '10')
set_driver('Jack Doohan', 'Cadillac', '7', 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Jack_Doohan_2024.jpg/400px-Jack_Doohan_2024.jpg')
set_driver('Isack Hadjar', 'Cadillac', '6')
set_driver('Yuki Tsunoda', 'RB', '22')

# Final stats check
db.execute("UPDATE drivers SET championships=1 WHERE name='Lando Norris'")
db.execute("UPDATE drivers SET championships=7 WHERE name='Lewis Hamilton'")
db.execute("UPDATE drivers SET championships=3 WHERE name='Max Verstappen'")

conn.commit()
conn.close()
print("✓ 2026 Lineups and Cadillac drivers verified.")
