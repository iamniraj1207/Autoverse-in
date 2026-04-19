import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "autoverse.db")

def seed():
    conn = sqlite3.connect(DB_PATH)
    db = conn.cursor()

    print("Seeding F1 Teams...")
    teams = [
        ("Red Bull Racing", "Oracle Red Bull Racing", "Austrian", "Milton Keynes, UK", "Christian Horner", "Honda RBPT", 6, 113, 264, 95, 95, 2005, 2005, "https://api.logobank.io/v1/logos/red-bull-racing.png", "https://source.unsplash.com/1600x900/?redbull,f1,car", "#1E3A5F", "A dominant force in modern F1, Red Bull Racing is known for its aggressive aerodynamic philosophy and technical partnership with Honda. Since its debut in 2005, the team has secured multiple world titles with Vettel and Verstappen. The 2026 era marks their transition to Red Bull Ford Powertrains."),
        ("Scuderia Ferrari", "Scuderia Ferrari HP", "Italian", "Maranello, Italy", "Frédéric Vasseur", "Ferrari", 16, 243, 807, 249, 259, 1929, 1950, "https://api.logobank.io/v1/logos/ferrari.png", "https://source.unsplash.com/1600x900/?ferrari,f1,car", "#DC143C", "The heart and soul of Formula 1. Ferrari is the only team to have competed in every season since the championship began in 1950. With a legacy built on passion and prestige, the Tifosi expect nothing less than victory. The 2025 arrival of Lewis Hamilton signals a new chapter in their illustrous history."),
        ("Mercedes AMG", "Mercedes-AMG Petronas F1 Team", "German", "Brackley, UK", "Toto Wolff", "Mercedes", 8, 125, 289, 137, 105, 1954, 1954, "https://api.logobank.io/v1/logos/mercedes-f1.png", "https://source.unsplash.com/1600x900/?mercedes,f1,car", "#00D2BE", "The Silver Arrows defined the hybrid era, winning eight consecutive constructors' titles. Mercedes embodies German engineering precision and clinical operational efficiency. As they prepare for the 2026 regulations, the team remains a benchmark for innovation and recovery in the face of competition."),
        ("McLaren F1", "McLaren Formula 1 Team", "British", "Woking, UK", "Andrea Stella", "Mercedes", 8, 184, 502, 156, 165, 1963, 1966, "https://api.logobank.io/v1/logos/mclaren.png", "https://source.unsplash.com/1600x900/?mclaren,f1,car", "#FF8000", "Founded by Bruce McLaren, the team from Woking is a legendary name associated with legends like Senna and Prost. After a period of rebuilding, McLaren has returned to the sharp end of the grid with a bold Papaya identity. Their technical center remains one of the most advanced facilities in global motorsport."),
        ("Aston Martin", "Aston Martin Aramco F1 Team", "British", "Silverstone, UK", "Mike Krack", "Mercedes", 0, 0, 9, 0, 0, 1959, 1959, "https://api.logobank.io/v1/logos/aston-martin.png", "https://source.unsplash.com/1600x900/?astonmartin,f1,car", "#006F62", "Clad in iconic British Racing Green, Aston Martin represents Lawrence Stroll's ambitious vision to reach the top. With a state-of-the-art new campus and a technical partnership with Honda starting in 2026, the team is positioning itself as a legitimate heavyweight. Their focus is on merging luxury brand appeal with championship-winning performance."),
        ("Alpine F1", "BWT Alpine F1 Team", "French", "Enstone, UK / Viry, France", "Oliver Oakes", "Renault", 2, 36, 103, 20, 15, 1981, 1986, "https://api.logobank.io/v1/logos/alpine.png", "https://source.unsplash.com/1600x900/?alpine,f1,car", "#0090FF", "As the factory entry for the Renault Group, Alpine carries the torch of French motorsport excellence. The team has transitioned through many identities, including Benetton and Renault, claiming titles along the way. In the 2026 landscape, Alpine seeks to stabilize its technical direction and rejoin the fight for podiums."),
        ("Haas F1", "MoneyGram Haas F1 Team", "American", "Kannapolis, USA / Banbury, UK", "Ayao Komatsu", "Ferrari", 0, 0, 0, 1, 0, 2014, 2016, "https://api.logobank.io/v1/logos/haas-f1.png", "https://source.unsplash.com/1600x900/?haas,f1,car", "#B6BABD", "The only American team on the grid, Haas operates an efficient, satellite-based model. By leveraging partnerships with Ferrari and Dallara, Haas consistently punches above its weight in the midfield. Under new leadership, the team is focused on improving development consistency over the course of a season."),
        ("Racing Bulls", "Visa Cash App RB F1 Team", "Italian", "Faenza, Italy", "Laurent Mekies", "Honda RBPT", 0, 2, 5, 1, 3, 2006, 2006, "https://api.logobank.io/v1/logos/racing-bulls.png", "https://source.unsplash.com/1600x900/?racingbulls,f1,car", "#1434CB", "Born as Toro Rosso to hunt for the next stars of the Red Bull program, the Faenza-based team has evolved into a formidable independent competitor. Now rebranded as RB, they maintain close technical ties to the senior program while fostering their own identity. Their history is punctuated by shock wins from Vettel and Gasly."),
        ("Williams Racing", "Williams Racing", "British", "Grove, UK", "James Vowles", "Mercedes", 9, 114, 313, 128, 133, 1977, 1978, "https://api.logobank.io/v1/logos/williams.png", "https://source.unsplash.com/1600x900/?williams,f1,car", "#005AFF", "Williams is one of the most successful constructors in F1 history, founded by the legendary Sir Frank Williams. After a decade of struggle, the team is currently undergoing a systemic transformation under new ownership. Their focus is on long-term infrastructure investment to return this historic name to its winning ways."),
        ("Sauber / Audi", "Audi F1 Team", "German", "Hinwil, Switzerland", "Mattia Binotto", "Audi", 1, 1, 27, 1, 2, 1970, 1993, "https://api.logobank.io/v1/logos/audi-f1.png", "https://source.unsplash.com/1600x900/?audi,f1,car", "#52E252", "The 2026 season marks Sauber's full transformation into the Audi factory team. Combining Swiss precision from Hinwil with Audi's German power unit expertise from Neuburg, this entry is one of the most anticipated in decades. As they transition out of the Stake/Sauber era, the focus is squarely on the 2026 regulations.")
    ]
    
    db.executemany("""
        INSERT INTO teams (name, full_name, nationality, base, team_principal, power_unit, 
                         championships, wins, podiums, poles, fastest_laps, founded_year, 
                         first_entry, logo_url, car_image_url, primary_color, bio)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, teams)
    
    # Get team mapping
    db.execute("SELECT id, name FROM teams")
    team_map = {row[1]: row[0] for row in db.fetchall()}

    print("Seeding F1 Drivers...")
    drivers = [
        ("Max Verstappen", "Dutch", team_map["Red Bull Racing"], 1, "VER", 3, 54, 98, 32, 30, 2586.5, 2015, "1997-09-30", "Hasselt, Belgium", "Known for his uncompromising racing style and clinical precision, Max Verstappen is the defining driver of his generation. Since becoming the youngest ever Grand Prix winner, he has matured into a tactical master under the Red Bull program. His ability to extract ultimate performance in any conditions makes him a perennial championship favorite."),
        ("Liam Lawson", "New Zealander", team_map["Red Bull Racing"], 30, "LAW", 0, 0, 0, 0, 0, 2, 2023, "2002-02-11", "Hastings, NZ", "Lawson's rise through the Red Bull Junior Team was capped by an impressive fill-in performance in 2023. Known for his immediate speed upon entering a car, he has earned his full-time seat through sheer grit and adaptability. He represents the future of the Red Bull pipeline as they enter the 2026 engine era."),
        ("Lewis Hamilton", "British", team_map["Scuderia Ferrari"], 44, "HAM", 7, 103, 197, 104, 65, 4639.5, 2007, "1985-01-07", "Stevenage, UK", "Statistically the greatest driver in F1 history, Lewis Hamilton combines raw natural talent with a relentless pursuit of perfection. His 2025 move to Ferrari is a historic shift, as he seeks an unprecedented eighth title with the Prancing Horse. Beyond the track, he is a global icon for diversity and social change."),
        ("Charles Leclerc", "Monegasque", team_map["Scuderia Ferrari"], 16, "LEC", 0, 5, 30, 23, 9, 1074, 2018, "1997-10-16", "Monte Carlo, Monaco", "The 'Prince of Monaco' is Ferrari's homegrown hero, possessing blistering qualifying speed that often defies logic. Leclerc carries the weight of the Tifosi's dreams on his shoulders with a mix of vulnerability and blinding ambition. His battle alongside Hamilton at Ferrari is the most anticipated teammate duo in years."),
        ("George Russell", "British", team_map["Mercedes AMG"], 63, "RUS", 0, 1, 11, 1, 6, 469, 2019, "1998-02-15", "King's Lynn, UK", "Russell is a driver of immense calculating intelligence and consistent execution. After serving his apprenticeship at Williams, he has stepped up to lead the Mercedes squad into its post-Hamilton future. His technical feedback and qualifying aggression make him the foundation of Mercedes' recovery efforts."),
        ("Andrea Kimi Antonelli", "Italian", team_map["Mercedes AMG"], 12, "ANT", 0, 0, 0, 0, 0, 0, 2025, "2006-08-25", "Bologna, Italy", "Bypassing F3 entirely, Antonelli's meteoric rise is unprecedented in the modern era of the Mercedes Junior Team. He possesses a natural car control that drawing comparisons to the all-time greats. As Italy's brightest hope, his debut at Mercedes marks the birth of a potential new superstar."),
        ("Lando Norris", "British", team_map["McLaren F1"], 4, "NOR", 0, 1, 14, 1, 6, 633, 2019, "1999-11-13", "Bristol, UK", "Norris has evolved from a social media darling into one of the grid's most respected and fast operators. His loyalty to McLaren has seen him lead the team's resurgence back to the front of the pack. With a calm demeanor and exceptional tire management, he is now a consistent threat for race wins."),
        ("Oscar Piastri", "Australian", team_map["McLaren F1"], 81, "PIA", 0, 0, 2, 0, 1, 97, 2023, "2001-04-06", "Melbourne, Australia", "Possessing an icy composure that belies his age, Piastri's rookie seasons were a masterclass in clean, high-speed racing. He is widelyregarded as a future world champion for his ability to handle pressure without breaking a sweat. Alongside Norris, he forms the most exciting young driver pairing in Formula 1."),
        ("Fernando Alonso", "Spanish", team_map["Aston Martin"], 14, "ALO", 2, 32, 106, 22, 24, 2267, 2001, "1981-07-29", "Oviedo, Spain", "The ultimate street fighter, Alonso's longevity and hunger for racing remain unmatched on the grid. He possesses a unique ability to find pace where none exists, squeezing every ounce of potential from his machinery. His experience is the guiding light for Aston Martin's ambitious title aspirations."),
        ("Lance Stroll", "Canadian", team_map["Aston Martin"], 18, "STR", 0, 0, 3, 1, 0, 268, 2017, "1998-10-29", "Montreal, Canada", "Stroll is a driver who often shines in wet or chaotic conditions, showcasing a high ceiling for performance. While shadowed by his veteran teammates, he has contributed significant points to the team's growth. His role is pivotal in Aston Martin's integration as a works Honda team in 2026."),
        ("Pierre Gasly", "French", team_map["Alpine F1"], 10, "GAS", 0, 1, 4, 0, 3, 394, 2017, "1996-02-07", "Rouen, France", "Gasly's career is a testament to resilience, having reinvented himself after setbachs into a race winner and leader. He brings a precise, analytical approach to the Alpine project as they seek stability. His tenacity in the midfield has made him a consistent points-scorer for the French outfit."),
        ("Jack Doohan", "Australian", team_map["Alpine F1"], 7, "DOO", 0, 0, 0, 0, 0, 0, 2025, "2003-01-20", "Gold Coast, Australia", "Son of motorcycle legend Mick Doohan, Jack has paved his own path through the Alpine Academy to the F1 grid. Known for his hard-working ethos and strong qualifying pace in F2, he is eager to prove his worth in the top flight. He represents Alpine's commitment to internal talent development."),
        ("Nico Hulkenberg", "German", team_map["Haas F1"], 27, "HUL", 0, 0, 0, 1, 2, 530, 2010, "1987-08-19", "Emmerich, Germany", "The 'Hulk' is one of the grid's most respected veterans, known for his incredible qualifying performances and technical feedback. After successful stints across many teams, he brings vital experience to Haas. His ability to deliver consistent results under technical pressure remains a benchmark."),
        ("Esteban Ocon", "French", team_map["Haas F1"], 31, "OCO", 0, 1, 3, 0, 0, 422, 2016, "1996-09-17", "Évreux, France", "Ocon is a driver defined by his defensive prowess and clean racing style, highlighted by his shock win in Hungary. His move to Haas marks a new beginning for the Frenchman as he seeks to lead a team's development. He is known for his dedication and work rate both on and off the track."),
        ("Oliver Bearman", "British", team_map["Racing Bulls"], 38, "BEA", 0, 0, 0, 0, 0, 6, 2024, "2005-05-08", "Chelmsford, UK", "Bearman's sensational debut in Saudi Arabia proved he belongs at the pinnacle of the sport. His ability to adapt to F1 machinery with minimal preparation has marked him as a future Ferrari contender. His residency at Racing Bulls is a crucial step in his progression towards a scarlet seat."),
        ("Isack Hadjar", "French", team_map["Racing Bulls"], 55, "HAD", 0, 0, 0, 0, 0, 0, 2025, "2004-09-28", "Paris, France", "A standout talent in the Red Bull Junior Team, Hadjar is known for his aggressive overtakes and raw speed. He has earned his place through a dominant campaign in the lower categories. His debut in 2025 adds more French flair and competitive fire to the ever-evolving F1 grid."),
        ("Alexander Albon", "Thai", team_map["Williams Racing"], 23, "ALB", 0, 0, 2, 0, 0, 228, 2019, "1996-03-23", "London, UK", "Albon has become the heart of the Williams resurgence, extracting results that often exceed the car's theoretical limits. His technical leadership and positive spirit have made him indispensable to the team's rebuilding process. He is widely regarded as one of the most intelligent and versatile racers currently active."),
        ("Carlos Sainz", "Spanish", team_map["Williams Racing"], 55, "SAI", 0, 3, 22, 1, 3, 1022.5, 2015, "1994-09-01", "Madrid, Spain", "Known as the 'Smooth Operator', Sainz is a highly intelligent racer with a deep understanding of strategy and car dynamics. His arrival at Williams is a massive statement of intent for the team's future. He remains one of the few drivers capable of consistently challenging the Big Three for victories."),
        ("Gabriel Bortoleto", "Brazilian", team_map["Sauber / Audi"], 5, "BOR", 0, 0, 0, 0, 0, 0, 2025, "2004-10-14", "São Paulo, Brazil", "As Brazil's next great hope, Bortoleto's F3 championship win showcased a driver of extreme maturity and technical skill. Entering Formula 1 with Sauber during their Audi transition is a golden opportunity to build a long-term legacy. He is known for his calm approach and relentless consistency over a season."),
        ("Guanyu Zhou", "Chinese", team_map["Sauber / Audi"], 24, "ZHO", 0, 0, 0, 0, 2, 12, 2022, "1999-05-30", "Shanghai, China", "China's first full-time F1 driver, Zhou has proven his worth through dependable racing and a strong understanding of technical systems. He has been a vital part of Sauber's stability as they navigate their way towards the Audi era. His presence is a key bridge to a massive and growing automotive market.")
    ]
    
    # Enrich drivers with images based on the requested pattern
    enriched_drivers = []
    for d in drivers:
        img_url = f"https://source.unsplash.com/400x500/?formula1,{d[0].replace(' ', '')},racing,portrait"
        enriched_drivers.append(d + (img_url,))

    db.executemany("""
        INSERT INTO drivers (name, nationality, team_id, number, abbreviation, championships, 
                           wins, podiums, poles, fastest_laps, points_career, debut_year, 
                           birth_date, birth_place, bio, image_url)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, enriched_drivers)

    print("Seeding F1 Timeline...")
    # Seed specific milestones for top drivers/teams
    timeline_events = [
        ('driver', 'Lewis Hamilton', 2007, "Sensational Debut", "Lewis Hamilton finishes on the podium in his first ever Grand Prix in Australia, marking the start of a legendary career.", "debut"),
        ('driver', 'Lewis Hamilton', 2008, "First World Championship", "In one of the most dramatic finishes in history, Hamilton secures his first title at the Brazilian Grand Prix.", "championship"),
        ('driver', 'Lewis Hamilton', 2013, "The Mercedes Move", "Hamilton shocks the F1 world by leaving McLaren for the Mercedes factory team.", "transfer"),
        ('driver', 'Max Verstappen', 2015, "Youngest Debutant", "At 17 years and 166 days, Verstappen starts the Australian GP, becoming the youngest driver in F1 history.", "debut"),
        ('driver', 'Max Verstappen', 2016, "Spanish GP Victory", "In his first race for Red Bull Racing, Verstappen wins the Spanish Grand Prix at just 18 years old.", "win"),
        ('driver', 'Max Verstappen', 2021, "First World Title", "Verstappen secures his first title after a season-long battle with Hamilton, settled on the final lap in Abu Dhabi.", "championship"),
        ('team', 'Scuderia Ferrari', 1950, "Birth of a Legend", "Ferrari enters the first ever Formula 1 World Championship race at the Monaco Grand Prix.", "debut"),
        ('team', 'Red Bull Racing', 2010, "First Constructors Title", "Red Bull secures its first of four consecutive constructors' championships, ushering in the Vettel era.", "championship"),
        ('team', 'Sauber / Audi', 2026, "The Audi Arrival", "Audi officially enters Formula 1 as a works team, completing the takeover of the Sauber operation.", "technical")
    ]
    
    # Map names to IDs for timeline
    for event in timeline_events:
        table = "drivers" if event[0] == "driver" else "teams"
        db.execute(f"SELECT id FROM {table} WHERE name = ?", (event[1],))
        entity_id = db.fetchone()[0]
        db.execute("""
            INSERT INTO f1_timeline (entity_type, entity_id, year, title, description, milestone_type)
            VALUES (?,?,?,?,?,?)
        """, (event[0], entity_id, event[2], event[3], event[4], event[5]))

    print("Seeding Fastest Laps...")
    laps = [
        ("Max Verstappen", "Red Bull Racing", "Interlagos", "Brazilian GP", 2023, "1:10.540", 219.0),
        ("Lewis Hamilton", "Mercedes AMG", "Silverstone", "British GP", 2020, "1:27.097", 243.0),
        ("Charles Leclerc", "Scuderia Ferrari", "Monza", "Italian GP", 2019, "1:21.046", 257.0),
        ("Lando Norris", "McLaren F1", "Hungaroring", "Hungarian GP", 2023, "1:20.504", 195.0),
        ("Fernando Alonso", "Aston Martin", "Zandvoort", "Dutch GP", 2023, "1:13.837", 207.0)
    ]
    
    for lap in laps:
        db.execute("SELECT id FROM drivers WHERE name = ?", (lap[0],))
        d_id = db.fetchone()[0]
        db.execute("SELECT id FROM teams WHERE name = ?", (lap[1],))
        t_id = db.fetchone()[0]
        db.execute("""
            INSERT INTO f1_fastest_laps (driver_id, team_id, circuit, grand_prix, year, lap_time, speed_kmh)
            VALUES (?,?,?,?,?,?,?)
        """, (d_id, t_id, lap[2], lap[3], lap[4], lap[5], lap[6]))

    conn.commit()
    conn.close()
    print("✓ F1 Hub Seeded successfully.")

if __name__ == "__main__":
    seed()
