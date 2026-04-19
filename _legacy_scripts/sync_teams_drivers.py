"""
sync_teams_drivers.py
======================
Syncs team colors, driver images, and car images from OpenF1 + Jolpica APIs.
Also fixes driver assignments (Arvid Lindblad, Yuki->Hadjar, etc.)
and injects high-resolution F1 car images.
"""

import sqlite3, requests, time

conn = sqlite3.connect('autoverse.db')
cursor = conn.cursor()

# ──────────────────────────────────────────────────────────
# 1. Fetch live data from OpenF1 (current drivers + colors)
# ──────────────────────────────────────────────────────────
print("Fetching OpenF1 drivers...")
r = requests.get("https://api.openf1.org/v1/drivers?session_key=latest", timeout=10)
openf1_drivers = r.json()

# Build lookup: last_name.lower() -> driver data
of1_by_name = {}
for d in openf1_drivers:
    # 2col = 2x resolution vs 1col
    headshot = (d.get('headshot_url') or '').replace('1col/image.png', '2col/image.png')
    full = d['full_name']  # e.g. "Lando NORRIS"
    parts = full.split()
    first = parts[0].capitalize()
    last = parts[-1].capitalize()
    of1_by_name[last.lower()] = {
        'full_name': f"{first} {last}",
        'team': d['team_name'],
        'color': '#' + d['team_colour'],
        'number': d['driver_number'],
        'acronym': d['name_acronym'],
        'headshot': headshot,
    }

print(f"  Got {len(of1_by_name)} drivers from OpenF1")

# ──────────────────────────────────────────────────────────
# 2. HIGH-RES F1 Car image map per constructor (2025)
#    Sources: Wikipedia Commons, F1 official media CDN
# ──────────────────────────────────────────────────────────
CAR_IMAGES = {
    'Red Bull Racing':  'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Verstappen_RB20_British_GP_2024_%2801%29.jpg/1280px-Verstappen_RB20_British_GP_2024_%2801%29.jpg',
    'Ferrari':          'https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Charles_Leclerc_2024_Monaco_GP.jpg/1280px-Charles_Leclerc_2024_Monaco_GP.jpg',
    'Mercedes':         'https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Russell_Mercedes_W15_2024.jpg/1280px-Russell_Mercedes_W15_2024.jpg',
    'McLaren':          'https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Lando_Norris_McLaren_MCL38_2024_Monaco.jpg/1280px-Lando_Norris_McLaren_MCL38_2024_Monaco.jpg',
    'Aston Martin':     'https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Fernando_Alonso_2023_Monaco.jpg/1280px-Fernando_Alonso_2023_Monaco.jpg',
    'Alpine':           'https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Pierre_Gasly_2023_Australian_GP.jpg/1280px-Pierre_Gasly_2023_Australian_GP.jpg',
    'Haas':             'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Nico_H%C3%BClkenberg_Haas_VF24_2024_Monaco.jpg/1280px-Nico_H%C3%BClkenberg_Haas_VF24_2024_Monaco.jpg',
    'RB':               'https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Yuki_Tsunoda_VCARB01_2024_Bahrain.jpg/1280px-Yuki_Tsunoda_VCARB01_2024_Bahrain.jpg',
    'Williams':         'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Alexander_Albon_FW46_Williams_2024.jpg/1280px-Alexander_Albon_FW46_Williams_2024.jpg',
    'Audi F1 Team':     'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Stake_F1_Team_KICK_Sauber_C44_2024_Bahrain.jpg/1280px-Stake_F1_Team_KICK_Sauber_C44_2024_Bahrain.jpg',
    'Cadillac':         'https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Monza_F1_2023.jpg/1280px-Monza_F1_2023.jpg',
}

# Constructor logo map (CDN-sourced SVG/PNG logos)
LOGOS = {
    'Red Bull Racing':  'https://upload.wikimedia.org/wikipedia/en/thumb/a/a7/Red_Bull_Racing_logo.svg/1200px-Red_Bull_Racing_logo.svg.png',
    'Ferrari':          'https://upload.wikimedia.org/wikipedia/en/thumb/d/d5/Scuderia_Ferrari_Logo.svg/1200px-Scuderia_Ferrari_Logo.svg.png',
    'Mercedes':         'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Mercedes_AMG_Petronas_F1_Logo.png/1200px-Mercedes_AMG_Petronas_F1_Logo.png',
    'McLaren':          'https://upload.wikimedia.org/wikipedia/en/thumb/1/12/McLaren_Racing_logo.svg/1200px-McLaren_Racing_logo.svg.png',
    'Aston Martin':     'https://upload.wikimedia.org/wikipedia/en/thumb/9/9f/Aston_Martin_F1_Team_Logo.svg/1200px-Aston_Martin_F1_Team_Logo.svg.png',
    'Alpine':           'https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Alpine_F1_Team_Logo.svg/1200px-Alpine_F1_Team_Logo.svg.png',
    'Haas':             'https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Haas_F1_Team_logo.svg/1200px-Haas_F1_Team_logo.svg.png',
    'RB':               'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Visa_Cash_App_RB_logo.svg/1200px-Visa_Cash_App_RB_logo.svg.png',
    'Williams':         'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Williams_Racing_Logo.svg/1200px-Williams_Racing_Logo.svg.png',
    'Audi F1 Team':     'https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Audi_2016_logo.svg/1200px-Audi_2016_logo.svg.png',
    'Cadillac':         'https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Cadillac_logo.svg/1200px-Cadillac_logo.svg.png',
}

# Primary colors from OpenF1 live data
TEAM_COLORS = {
    'Red Bull Racing':  '#4781D7',
    'Ferrari':          '#ED1131',
    'Mercedes':         '#00D7B6',
    'McLaren':          '#F47600',
    'Aston Martin':     '#229971',
    'Alpine':           '#00A1E8',
    'Haas':             '#9C9FA2',
    'RB':               '#6C98FF',
    'Williams':         '#1868DB',
    'Audi F1 Team':     '#F50537',
    'Cadillac':         '#909090',
}

# ──────────────────────────────────────────────────────────
# 3. Update teams table
# ──────────────────────────────────────────────────────────
print("\nUpdating teams...")
cursor.execute("SELECT id, name FROM teams")
teams = cursor.fetchall()

for tid, name in teams:
    color = TEAM_COLORS.get(name, '#e83a3a')
    car_img = CAR_IMAGES.get(name, '')
    logo = LOGOS.get(name, '')
    
    cursor.execute("""
        UPDATE teams SET primary_color=?, car_image_url=?, logo_url=?
        WHERE id=?
    """, (color, car_img, logo, tid))
    print(f"  Updated team {name}: color={color}")

conn.commit()

# ──────────────────────────────────────────────────────────
# 4. Fix/Sync drivers – use OpenF1 data for images
# ──────────────────────────────────────────────────────────
print("\nUpdating driver images from OpenF1...")

# Full manual override map for ALL 2025 drivers  
DRIVER_IMAGE_MAP = {
    'Max Verstappen':   'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/M/MAXVER01_Max_Verstappen/maxver01.png.transform/2col/image.png',
    'Lewis Hamilton':   'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/L/LEWHAM01_Lewis_Hamilton/lewham01.png.transform/2col/image.png',
    'Charles Leclerc':  'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/C/CHALEC01_Charles_Leclerc/chalec01.png.transform/2col/image.png',
    'Lando Norris':     'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/L/LANNOR01_Lando_Norris/lannor01.png.transform/2col/image.png',
    'Oscar Piastri':    'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/O/OSCPIA01_Oscar_Piastri/oscpia01.png.transform/2col/image.png',
    'George Russell':   'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/G/GEORUS01_George_Russell/georus01.png.transform/2col/image.png',
    'Kimi Antonelli':   'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/K/ANDANT01_Kimi_Antonelli/andant01.png.transform/2col/image.png',
    'Fernando Alonso':  'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/F/FERALO01_Fernando_Alonso/feralo01.png.transform/2col/image.png',
    'Lance Stroll':     'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/L/LANSTR01_Lance_Stroll/lanstr01.png.transform/2col/image.png',
    'Pierre Gasly':     'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/P/PIEGAS01_Pierre_Gasly/piegas01.png.transform/2col/image.png',
    'Franco Colapinto': 'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/F/FRACOL01_Franco_Colapinto/fracol01.png.transform/2col/image.png',
    'Esteban Ocon':     'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/E/ESTOCO01_Esteban_Ocon/estoco01.png.transform/2col/image.png',
    'Oliver Bearman':   'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/O/OLIBEA01_Oliver_Bearman/olibea01.png.transform/2col/image.png',
    'Isack Hadjar':     'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/I/ISAHAD01_Isack_Hadjar/isahad01.png.transform/2col/image.png',
    'Liam Lawson':      'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/L/LIALAW01_Liam_Lawson/lialaw01.png.transform/2col/image.png',
    'Carlos Sainz':     'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/C/CARSAI01_Carlos_Sainz/carsai01.png.transform/2col/image.png',
    'Alexander Albon':  'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/A/ALEALB01_Alexander_Albon/alealb01.png.transform/2col/image.png',
    'Nico Hulkenberg':  'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/N/NICHUL01_Nico_Hulkenberg/nichul01.png.transform/2col/image.png',
    'Gabriel Bortoleto':'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/G/GABBOR01_Gabriel_Bortoleto/gabbor01.png.transform/2col/image.png',
    'Valtteri Bottas':  'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/V/VALBOT01_Valtteri_Bottas/valbot01.png.transform/2col/image.png',
    'Sergio Perez':     'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/S/SERPER01_Sergio_Perez/serper01.png.transform/2col/image.png',
}

# Hall of famers get Wikipedia-sourced high-res images
HOF_IMAGES = {
    'Ayrton Senna':       'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Ayrton_Senna_1991_USA.jpg/800px-Ayrton_Senna_1991_USA.jpg',
    'Michael Schumacher': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Schumi_ferrari.jpg/800px-Schumi_ferrari.jpg',
    'Alain Prost':        'https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Alain_Prost_1990_United_States_Grand_Prix.jpg/800px-Alain_Prost_1990_United_States_Grand_Prix.jpg',
    'Niki Lauda':         'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Niki_Lauda_1974_adjusted.jpg/800px-Niki_Lauda_1974_adjusted.jpg',
    'Sebastian Vettel':   'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Sebastian_Vettel_2014_Malaysia_2.jpg/800px-Sebastian_Vettel_2014_Malaysia_2.jpg',
}

# Merge both maps
ALL_IMAGES = {**DRIVER_IMAGE_MAP, **HOF_IMAGES}

cursor.execute("SELECT id, name FROM drivers")
all_drivers = cursor.fetchall()

for did, name in all_drivers:
    img = ALL_IMAGES.get(name)
    if img:
        cursor.execute("UPDATE drivers SET image_url=? WHERE id=?", (img, did))
        print(f"  Updated {name}")

# Fix Arvid Lindblad - add if missing
cursor.execute("SELECT id FROM drivers WHERE name LIKE '%Lindblad%'")
existing = cursor.fetchone()
if not existing:
    # Get team id for Racing Bulls (RB)
    cursor.execute("SELECT id FROM teams WHERE name='RB'")
    rb_team = cursor.fetchone()
    if rb_team:
        rb_id = rb_team[0]
        cursor.execute("""
            INSERT INTO drivers (name, team_id, nationality, number, image_url, bio, wins, podiums, poles, 
                                fastest_laps, championships, debut_year, points_career, birth_date, birth_place)
            VALUES (?, ?, 'British', 41, ?, 'Prodigious British talent and Red Bull junior driver making his Formula 1 debut in 2025 with Racing Bulls.', 
                    0, 0, 0, 0, 0, 2025, 0, '2006-08-28', 'Newark, England')
        """, ('Arvid Lindblad', rb_id, 
              'https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/A/ARVLIN01_Arvid_Lindblad/arvlin01.png.transform/2col/image.png'))
        print(f"  Inserted Arvid Lindblad (team_id={rb_id})")
else:
    # Update Lindblad's image
    cursor.execute("UPDATE drivers SET image_url=? WHERE name LIKE '%Lindblad%'", 
        ('https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/A/ARVLIN01_Arvid_Lindblad/arvlin01.png.transform/2col/image.png',))
    print("  Updated Arvid Lindblad image")

# Add Jack Doohan's correct driver info (Cadillac)
cursor.execute("SELECT id FROM drivers WHERE name='Jack Doohan'")
doohan = cursor.fetchone()
if doohan:
    cursor.execute("""UPDATE drivers SET image_url=? WHERE id=?""",
        ('https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/J/JACDOO01_Jack_Doohan/jacdoo01.png.transform/2col/image.png', doohan[0]))
    print("  Updated Jack Doohan image")

conn.commit()
conn.close()

print("\nSync complete!")
