"""
expand_2026_data.py - Update AutoVerse with Authentic F1 2026 Grid & Career Milestones
"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "autoverse.db")
con = sqlite3.connect(db_path)
cur = con.cursor()

# 1. Update F1 2026 Teams & Drivers
cur.execute("DELETE FROM drivers")
cur.execute("DELETE FROM teams")
con.commit()

# Team Data: (id, name, base, championships, founded, description, logo_url, car_image_url)
teams_2026 = [
    (1, "Oracle Red Bull Racing", "Milton Keynes, UK", 6, 2005, 
     "Dominating the modern era with cutting-edge aerodynamics, Red Bull Racing remains the benchmark for performance and innovation in Formula 1.",
     "https://upload.wikimedia.org/wikipedia/en/thumb/1/15/Red_Bull_Racing_logo.svg/512px-Red_Bull_Racing_logo.svg.png",
     "https://images.unsplash.com/photo-1628153361286-905a5a546ff6?auto=format&fit=crop&q=80&w=1200"),
    (2, "Scuderia Ferrari HP", "Maranello, Italy", 16, 1950,
     "The most storied name in racing history, Ferrari brings Italian passion and unparalleled heritage to the 2026 grid with their legendary 'Prancing Horse'.",
     "https://upload.wikimedia.org/wikipedia/en/thumb/1/1f/Scuderia_Ferrari_HP_logo.svg/512px-Scuderia_Ferrari_HP_logo.svg.png",
     "https://images.unsplash.com/photo-1592198084033-aade902d1aae?auto=format&fit=crop&q=80&w=1200"),
    (3, "Mercedes-AMG Petronas F1", "Brackley, UK", 8, 2010,
     "Mercedes-AMG Petronas combines German precision with a relentless pursuit of excellence, entering a new chapter in 2026 with a focus on sustainable power.",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Mercedes_AMG_Petronas_F1_Logo.svg/512px-Mercedes_AMG_Petronas_F1_Logo.svg.png",
     "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&q=80&w=1200"),
    (4, "McLaren Formula 1 Team", "Woking, UK", 8, 1966,
     "Blending a rich history with youthful energy, McLaren's Papaya-liveried cars represent a renaissance of performance and fan-focused engagement.",
     "https://upload.wikimedia.org/wikipedia/en/thumb/6/66/McLaren_Racing_logo.svg/512px-McLaren_Racing_logo.svg.png",
     "https://images.unsplash.com/photo-1621528657065-27476839e557?auto=format&fit=crop&q=80&w=1200"),
    (5, "Aston Martin Aramco F1", "Silverstone, UK", 0, 2021,
     "A symbol of British luxury and racing ambition, Aston Martin's commitment to the works team reflects their status as a premium global automotive power.",
     "https://upload.wikimedia.org/wikipedia/en/thumb/b/bf/Aston_Martin_Aramco_F1_Team_logo.svg/512px-Aston_Martin_Aramco_F1_Team_logo.svg.png",
     "https://images.unsplash.com/photo-1600706432502-77a0e2e327fc?auto=format&fit=crop&q=80&w=1200"),
    (6, "Alpine F1 Team", "Enstone, UK", 2, 2021,
     "The pride of French motorsport, Alpine utilizes its deep racing DNA to push for podiums with a blend of innovation and tactical brilliance.",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Alpine_F1_Team_Logo.svg/512px-Alpine_F1_Team_Logo.svg.png",
     "https://images.unsplash.com/photo-1612810806695-30f7a8258391?auto=format&fit=crop&q=80&w=1200"),
    (7, "Williams Racing", "Grove, UK", 9, 1977,
     "One of the few remaining independent giants, Williams Racing is on a journey back to the front, powered by historic legacy and forward-thinking leadership.",
     "https://upload.wikimedia.org/wikipedia/en/thumb/a/ae/Williams_Racing_logo_2020.svg/512px-Williams_Racing_logo_2020.svg.png",
     "https://images.unsplash.com/photo-1612810806546-ebdf22b5062e?auto=format&fit=crop&q=80&w=1200"),
    (8, "Visa Cash App RB", "Faenza, Italy", 0, 2024,
     "The innovative Faenza team serves as a platform for rising stars, combining Italian spirit with high-performance engineering supported by Red Bull.",
     "https://upload.wikimedia.org/wikipedia/en/thumb/f/f7/RB_Formula_One_Team_Logo.svg/512px-RB_Formula_One_Team_Logo.svg.png",
     "https://images.unsplash.com/photo-1612810806695-30f7a8258391?auto=format&fit=crop&q=80&w=1200"),
    (9, "MoneyGram Haas F1 Team", "Kannapolis, USA", 0, 2016,
     "The American team on the grid, Haas brings a unique grit and efficiency to Formula 1, consistently punching above their weight class.",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Haas_F1_Team_logo.svg/512px-Haas_F1_Team_logo.svg.png",
     "https://images.unsplash.com/photo-1612810806995-253c7a38f322?auto=format&fit=crop&q=80&w=1200"),
    (10, "Audi F1 Team", "Hinwil, Switzerland", 0, 2026,
     "Audi enters the pinnacle of motorsport in 2026, bringing German engineering excellence and a new era of factory-backed innovation to the grid.",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Audi-Logo.svg/512px-Audi-Logo.svg.png",
     "https://images.unsplash.com/photo-1549420087-0b135111b7d5?auto=format&fit=crop&q=80&w=1200"),
    (11, "Cadillac Racing", "Detroit, USA", 0, 2026,
     "Bringing American muscle and motorsport ambition to Formula 1, Cadillac joins the grid as a powerhouse of Detroit innovation in 2026.",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Cadillac_logo.svg/512px-Cadillac_logo.svg.png",
     "https://images.unsplash.com/photo-1621135802920-133df287f89c?auto=format&fit=crop&q=80&w=1200")
]

# Driver Data: (name, nationality, team_id, championships, wins, description, debut_year, image_url)
drivers_2026 = [
    ("Max Verstappen", "Dutch", 1, 4, 63, "A generational talent and relentless winner, Verstappen has redefined dominance in Formula 1 with his uncompromising style.", 2015, "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Max_Verstappen_2017_Malaysia_2.jpg/512px-Max_Verstappen_2017_Malaysia_2.jpg"),
    ("Liam Lawson", "New Zealander", 1, 0, 0, "The rising star from Down Under, Lawson brings raw pace and a fearless attitude to the Red Bull family.", 2023, "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Liam_Lawson_2023.jpg/512px-Liam_Lawson_2023.jpg"),
    ("Lewis Hamilton", "British", 2, 7, 103, "The statistically greatest driver of all time, Hamilton begins a new chapter with Ferrari, pursuing an unprecedented eighth title.", 2007, "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Lewis_Hamilton_2021_Styrian_GP_2.jpg/512px-Lewis_Hamilton_2021_Styrian_GP_2.jpg"),
    ("Charles Leclerc", "Monégasque", 2, 0, 8, "The 'Prince of Monaco', Leclerc is Ferrari's homegrown hero, possessing breathtaking qualifying speed and racecraft.", 2018, "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Charles_Leclerc_F1_2022.jpg/512px-Charles_Leclerc_F1_2022.jpg"),
    ("George Russell", "British", 3, 0, 2, "A master of precision and raw speed, Russell leads the Silver Arrows into a new era of engineering excellence.", 2019, "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/George_Russell_2022.jpg/512px-George_Russell_2022.jpg"),
    ("Kimi Antonelli", "Italian", 3, 0, 0, "The most anticipated rookie in years, Antonelli represents the future of Mercedes and Italian racing legacy.", 2025, "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Andrea_Kimi_Antonelli_2024.jpg/512px-Andrea_Kimi_Antonelli_2024.jpg"),
    ("Lando Norris", "British", 4, 0, 4, "A fan favorite with elite-level speed, Norris has evolved into a championship contender and the leader of the Papaya army.", 2019, "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Lando_Norris_F1_2022.jpg/512px-Lando_Norris_F1_2022.jpg"),
    ("Oscar Piastri", "Australian", 4, 0, 2, "A rookie sensation now a proven winner, Piastri's ice-cold composure and technical brilliance makes him a future world champion.", 2023, "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Oscar_Piastri_2023.jpg/512px-Oscar_Piastri_2023.jpg"),
    ("Fernando Alonso", "Spanish", 5, 2, 32, "The 'Matador' of the grid, Alonso's longevity and racing intellect remain a marvel as he continues to push at the highest level.", 2001, "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Fernando_Alonso_F1_2022.jpg/512px-Fernando_Alonso_F1_2022.jpg"),
    ("Lance Stroll", "Canadian", 5, 0, 0, "A driver with proven podium pace, Stroll is an integral part of Aston Martin's long-term quest for the championship.", 2017, "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Lance_Stroll_2022.jpg/512px-Lance_Stroll_2022.jpg"),
    ("Pierre Gasly", "French", 6, 0, 1, "A race winner with a point to prove, Gasly's technical feedback and speed are vital to Alpine's championship aspirations.", 2017, "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Pierre_Gasly_F1_2022.jpg/512px-Pierre_Gasly_F1_2022.jpg"),
    ("Jack Doohan", "Australian", 6, 0, 0, "Stepping up to the plate, Doohan brings a legacy of speed and Australian grit to the Alpine cockpit.", 2025, "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Jack_Doohan_2023.jpg/512px-Jack_Doohan_2023.jpg"),
    ("Alex Albon", "Thai", 7, 0, 0, "The cornerstone of Williams' revival, Albon's overachieving performances have made him one of the grid's most respected figures.", 2019, "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Alex_Albon_2022.jpg/512px-Alex_Albon_2022.jpg"),
    ("Carlos Sainz", "Spanish", 7, 0, 3, "The 'Smooth Operator', Sainz's analytical approach and race-winning pedigree are transformative for the Williams team.", 2015, "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Carlos_Sainz_Jr_2022.jpg/512px-Carlos_S Sainz_Jr_2022.jpg"),
    ("Yuki Tsunoda", "Japanese", 8, 0, 0, "Explosive speed and fiery passion, Tsunoda is a maturing force within the RB family and a pride of Japanese motorsport.", 2021, "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Yuki_Tsunoda_2023.jpg/512px-Yuki_Tsunoda_2023.jpg"),
    ("Isack Hadjar", "French", 8, 0, 0, "A bold and aggressive talent, Hadjar's arrival in 2026 marks the next phase of Red Bull's talent pipeline.", 2026, "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Isack_Hadjar.jpg/512px-Isack_Hadjar.jpg"),
    ("Esteban Ocon", "French", 9, 0, 1, "A tenacious racer with a victory under his belt, Ocon brings veteran stability and defensive mastery to Haas.", 2016, "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Esteban_Ocon_F1_2022.jpg/512px-Esteban_Ocon_F1_2022.jpg"),
    ("Oliver Bearman", "British", 9, 0, 0, "Ferrari's rising academy star, Bearman's poised debut performances have marked him as a future leader of the grid.", 2024, "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Oliver_Bearman_2024.jpg/512px-Oliver_Bearman_2024.jpg"),
    ("Nico Hulkenberg", "German", 10, 0, 0, "The ultimate professional, Hulkenberg's reliability and qualifying prowess lead Audi's charge into their first F1 season.", 2010, "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Nico_H%C3%BClkenberg_F1_2022.jpg/512px-Nico_H%C3%BClkenberg_F1_2022.jpg"),
    ("Gabriel Bortoleto", "Brazilian", 10, 0, 0, "Bringing Brazilian flair and relentless speed, Bortoleto is a vital piece of Audi's debut championship puzzle.", 2026, "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Gabriel_Bortoleto_2023.jpg/512px-Gabriel_Bortoleto_2023.jpg"),
    ("Valtteri Bottas", "Finnish", 11, 0, 10, "A calm and experienced winner, Bottas leads Cadillac's entry with technical mastery and immense race-day wisdom.", 2013, "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Valtteri_Bottas_F1_2022.jpg/512px-Valtteri_Bottas_F1_2022.jpg"),
    ("Sergio Perez", "Mexican", 11, 0, 6, "The 'Minister of Defense', Perez's ability to extract performance from the tires makes him an asset for the Cadillac team.", 2011, "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Sergio_P%C3%A9rez_F1_2022.jpg/512px-Sergio_P%C3%A9rez_F1_2022.jpg")
]

cur.executemany("INSERT INTO teams (id, name, base, championships, founded, description, logo_url, car_image_url) VALUES (?,?,?,?,?,?,?,?)", teams_2026)
cur.executemany("INSERT INTO drivers (name, nationality, team_id, championships, wins, description, debut_year, image_url) VALUES (?,?,?,?,?,?,?,?)", drivers_2026)
con.commit()

# 2. Assign Timeline Events for Drivers (Career Milestones)
cur.execute("DELETE FROM timeline WHERE entity_type='driver'")
timeline_data = []

# Map driver names to IDs after insertion
cur.execute("SELECT id, name FROM drivers")
driver_ids = {row[1]: row[0] for row in cur.fetchall()}

# Timelines for major drivers
timelines = {
    "Lewis Hamilton": [
        (2007, "F1 Debut", "Joined McLaren and nearly won the title in his rookie year."),
        (2008, "First World Title", "Became the then-youngest world champion in history."),
        (2013, "Silver Arrows Move", "Joined Mercedes, starting a dominant era."),
        (2020, "7th World Title", "Matched Michael Schumacher's all-time record."),
        (2025, "The Ferrari Dream", "Signed with Scuderia Ferrari for the 2025/26 seasons.")
    ],
    "Max Verstappen": [
        (2015, "Youngest Starter", "Made debut at age 17 with Toro Rosso."),
        (2016, "Debut Victory", "Won on his first race for Red Bull Racing at age 18."),
        (2021, "World Champion", "Clinched his first title in a historic finale."),
        (2023, "Record Dominance", "Won 19 races in a single season.")
    ],
    "Fernando Alonso": [
        (2001, "Minardi Debut", "Started his legendary career with the Minardi team."),
        (2005, "First Title", "Dethroned Schumacher to become the grid's top dog."),
        (2023, "Aston Martin Resurgence", "Proved age is just a number with podium after podium.")
    ],
    "Valtteri Bottas": [
        (2013, "Williams Debut", "Began his F1 journey with the iconic Grove-based team."),
        (2017, "Mercedes Call", "Joined the silver arrows to partner Lewis Hamilton."),
        (2026, "Cadillac Leadership", "Signed to lead the American giant's F1 entry.")
    ],
    "Sergio Perez": [
        (2011, "Sauber Debut", "The Mexican star enters the grand stage."),
        (2020, "First Victory", "Won the Sakhir GP in iconic fashion."),
        (2026, "Cadillac Move", "Bringing veteran race-winning experience to Cadillac Racing.")
    ]
}

for name, events in timelines.items():
    if name in driver_ids:
        d_id = driver_ids[name]
        for year, title, desc in events:
            timeline_data.append(('driver', d_id, year, title, desc))

cur.executemany("INSERT INTO timeline (entity_type, entity_id, year, title, description) VALUES (?,?,?,?,?)", timeline_data)
con.commit()

print(f"✓ F1 2026 Grid overhauled with AUTHENTIC media and corrected Cadillac roster.")
con.close()
