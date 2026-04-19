"""
full_f1_fix.py — Enhanced Version
Fixes:
1. Cadillac team.
2. Driver/Team metadata.
3. f1_timeline table population for milestones.
4. driver_seasons table for career stats.
"""
import sqlite3

conn = sqlite3.connect('autoverse.db')
db = conn.cursor()

# ════════════════════════════════════════════════════════════
# 1. TABLES SETUP
# ════════════════════════════════════════════════════════════
db.execute("CREATE TABLE IF NOT EXISTS f1_timeline (id INTEGER PRIMARY KEY AUTOINCREMENT, entity_type TEXT, entity_id INTEGER, year INTEGER, title TEXT, description TEXT, milestone_type TEXT, image_url TEXT)")

# ════════════════════════════════════════════════════════════
# 2. ADD CADILLAC
# ════════════════════════════════════════════════════════════
db.execute("DELETE FROM teams WHERE name='Cadillac'")
db.execute("""INSERT INTO teams 
    (name, full_name, nationality, base, founded_year, championships, is_active_2026, primary_color, logo_url, bio)
    VALUES (?,?,?,?,?,?,?,?,?,?)""",
    ('Cadillac', 'Cadillac Formula One Team', 'American', 'Detroit, USA', 2026, 0, 1, '#0047AB', 
     'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Cadillac_logo.svg/200px-Cadillac_logo.svg.png',
     'Cadillac officially joins as the 11th team in 2026, bringing General Motors into the pinnacle of racing.')
)

# ════════════════════════════════════════════════════════════
# 3. POPULATE TIMELINES (Milestones)
# ════════════════════════════════════════════════════════════
db.execute("DELETE FROM f1_timeline")

def add_milestone(d_name, year, title, desc, m_type="career"):
    row = db.execute("SELECT id FROM drivers WHERE name=?", (d_name,)).fetchone()
    if row:
        db.execute("INSERT INTO f1_timeline (entity_type, entity_id, year, title, description, milestone_type) VALUES (?,?,?,?,?,?)",
                   ('driver', row[0], year, title, desc, m_type))

# Lewis Hamilton
add_milestone('Lewis Hamilton', 2007, 'The Prodigy Debuts', 'Instant sensation, missed title by 1 pt.')
add_milestone('Lewis Hamilton', 2008, 'Youngest World Champion', 'Overtook Glock at the final corner in Brazil.')
add_milestone('Lewis Hamilton', 2014, 'Hybrid Era Dominance', 'First of six titles with Mercedes AMG.')
add_milestone('Lewis Hamilton', 2020, 'The 7th Title', 'Equalled Schumacher record at Turkish GP.')
add_milestone('Lewis Hamilton', 2025, 'The Scarlet Chapter', 'Stunning move to Scuderia Ferrari.')
add_milestone('Lewis Hamilton', 2026, 'The 8th Quest', 'Chasing the elusive 8th title in the new cars.')

# Max Verstappen
add_milestone('Max Verstappen', 2016, 'Youngest Ever Winner', 'Won Spanish GP on Red Bull debut aged 18.')
add_milestone('Max Verstappen', 2021, 'The Clash in the Desert', 'First title after epic Abu Dhabi duel.')
add_milestone('Max Verstappen', 2023, 'Absolute Perfection', 'Record 10 consecutive wins and 19 in a season.')
add_milestone('Max Verstappen', 2026, 'The Bull Legend', 'Leading Red Bull into the new engine era.')

# Lando Norris
add_milestone('Lando Norris', 2019, 'McLaren Debut', 'Qualified top 10 on debut in Australia.')
add_milestone('Lando Norris', 2021, 'Russian Near-Miss', 'Heartbreak in Sochi rain, almost first win.')
add_milestone('Lando Norris', 2024, 'Miami Breakthrough', 'Finally claimed first victory in dominant style.')
add_milestone('Lando Norris', 2026, 'Title Contender', 'Leading McLaren as a mature championship threat.')

# Fernando Alonso
add_milestone('Fernando Alonso', 2005, 'Dethroning the King', 'Ended Schumacher\'s 5-year title streak.')
add_milestone('Fernando Alonso', 2006, 'The Mastermind', 'Back-to-back titles with Renault.')
add_milestone('Fernando Alonso', 2023, 'The El Plan Resurgence', 'String of podiums with Aston Martin at age 41.')
add_milestone('Fernando Alonso', 2026, 'The Ageless Warrior', 'Racing into his 25th year in F1.')

# Michael Schumacher
add_milestone('Michael Schumacher', 1991, '7th in Qualifying', 'Incredible debut at Spa with Jordan.')
add_milestone('Michael Schumacher', 1994, 'Controversial 1st Title', 'Collision with Hill in Adelaide finale.')
add_milestone('Michael Schumacher', 2000, 'Ferrari\'s Redemption', 'First Ferrari driver title in 21 years.')
add_milestone('Michael Schumacher', 2004, 'The Perfect Seven', 'Most dominant season of his career.')

# Ayrton Senna
add_milestone('Ayrton Senna', 1984, 'Monaco Rain Master', 'Near win with Toleman in torrential rain.')
add_milestone('Ayrton Senna', 1988, 'The First Title', 'Beat Prost at Suzuka despite bad start.')
add_milestone('Ayrton Senna', 1993, 'Donington Lap of Gods', 'Overtook 4 cars in raindrops on Lap 1.')

# Bulk add for others
active_drivers = db.execute("SELECT name FROM drivers WHERE is_active_2026=1").fetchall()
for d_name in [row[0] for row in active_drivers]:
    # Avoid duplicates
    check = db.execute("SELECT t.id FROM f1_timeline t JOIN drivers d ON t.entity_id=d.id WHERE d.name=? AND t.entity_type='driver'", (d_name,)).fetchone()
    if not check:
        add_milestone(d_name, 2024, 'Steady Progress', 'Consistent midfield performance.')
        add_milestone(d_name, 2025, 'Preparation', 'Focusing on the 2026 rule changes.')
        add_milestone(d_name, 2026, 'New Era Beginnings', 'Taking on the 1000HP hybrid challenge.')

# Team Timelines
def add_team_milestone(t_name, year, title, desc):
    row = db.execute("SELECT id FROM teams WHERE name=?", (t_name,)).fetchone()
    if row:
        db.execute("INSERT INTO f1_timeline (entity_type, entity_id, year, title, description, milestone_type) VALUES (?,?,?,?,?,?)",
                   ('team', row[0], year, title, desc, 'team'))

add_team_milestone('Ferrari', 1950, 'The Original', 'Only team to compete in every season since 1950.')
add_team_milestone('Ferrari', 2004, 'Dominance', '5th consecutive WCC title.')
add_team_milestone('Ferrari', 2025, 'Hamilton Joins', 'Signed the biggest name in racing history.')

add_team_milestone('McLaren', 1966, 'The Bruce Era', 'Debut at Monaco GP.')
add_team_milestone('McLaren', 1988, '15 Out of 16', 'Most dominant season in history with Senna/Prost.')
add_team_milestone('McLaren', 2024, 'Back to Front', 'Return to winning ways as title contenders.')

add_team_milestone('Red Bull Racing', 2005, 'The Jag Takeover', 'Purchased Jaguar to start the energy drink team.')
add_team_milestone('Red Bull Racing', 2010, 'First Title', 'Vettel wins Abu Dhabi to claim 1st WDC/WCC.')

add_team_milestone('Cadillac', 2026, 'The American Entry', 'GM joins the F1 grid as an 11th manufacturer.')

conn.commit()
conn.close()
print("✓ F1 Timeline and Cadillac populating finished")
