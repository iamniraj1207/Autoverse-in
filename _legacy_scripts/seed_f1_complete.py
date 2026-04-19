import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'autoverse.db')
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def seed_f1_complete():
    print("🚀 Seeding High-End F1 Data (2025/2026)...")

    # 1. Teams (Constructors)
    # name, full_name, nationality, base, principal, power, champs, wins, podiums, poles, fl, founded, first, logo, color, active
    teams = [
        ('Red Bull Racing', 'Oracle Red Bull Racing', 'Austrian', 'Milton Keynes, UK', 'Christian Horner', 'RBPT', 6, 120, 285, 105, 98, 2005, 2005, '/static/img/teams/red_bull_logo.svg', '#3671C6', 1),
        ('Ferrari', 'Scuderia Ferrari HP', 'Italian', 'Maranello, Italy', 'Frédéric Vasseur', 'Ferrari', 16, 248, 815, 252, 262, 1929, 1950, '/static/img/teams/ferrari_logo.svg', '#DC143C', 1),
        ('Mercedes', 'Mercedes-AMG PETRONAS', 'German', 'Brackley, UK', 'Toto Wolff', 'Mercedes', 8, 128, 298, 139, 108, 1954, 1954, '/static/img/teams/mercedes_logo.svg', '#00D2BE', 1),
        ('McLaren', 'McLaren Formula 1 Team', 'British', 'Woking, UK', 'Andrea Stella', 'Mercedes', 9, 192, 525, 165, 168, 1963, 1966, '/static/img/teams/mclaren_logo.svg', '#FF8000', 1),
        ('Aston Martin', 'Aston Martin Aramco', 'British', 'Silverstone, UK', 'Mike Krack', 'Mercedes', 0, 0, 12, 1, 0, 1959, 1959, '/static/img/teams/aston_martin_logo.svg', '#006F62', 1),
        ('Alpine', 'BWT Alpine F1 Team', 'French', 'Enstone, UK', 'Oliver Oakes', 'Renault', 2, 36, 112, 20, 15, 1977, 1977, '/static/img/teams/alpine_logo.svg', '#0090FF', 1),
        ('Haas', 'MoneyGram Haas F1', 'American', 'Kannapolis, US', 'Ayao Komatsu', 'Ferrari', 0, 0, 0, 1, 2, 2014, 2016, '/static/img/teams/haas_logo.svg', '#E8002D', 1),
        ('RB', 'Visa Cash App RB', 'Italian', 'Faenza, Italy', 'Laurent Mekies', 'Honda RBPT', 0, 2, 5, 1, 2, 2006, 2006, '/static/img/teams/racing_bulls_logo.svg', '#1434CB', 1),
        ('Williams', 'Williams Racing', 'British', 'Grove, UK', 'James Vowles', 'Mercedes', 9, 114, 313, 128, 133, 1977, 1977, '/static/img/teams/williams_logo.svg', '#005AFF', 1),
        ('Sauber', 'Stake F1 Team', 'Swiss', 'Hinwil, Switzerland', 'Mattia Binotto', 'Ferrari', 0, 1, 27, 1, 2, 1970, 1993, '/static/img/teams/sauber_logo.svg', '#52E252', 1),
    ]

    cursor.execute("DELETE FROM teams")
    cursor.executemany("""
        INSERT INTO teams (name, full_name, nationality, base, team_principal, power_unit, championships, wins, podiums, poles, fastest_laps, founded_year, first_entry, logo_url, primary_color, is_active_2026)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, teams)

    cursor.execute("SELECT id, name FROM teams")
    team_map = {row['name']: row['id'] for row in cursor.fetchall()}

    # 2. Drivers (Updating Lando to 1 Championship + High-Res Images)
    # format: name, nationality, team_id, number, abbr, champs, wins, podiums, poles, fl, pts, debut, bday, bplace, active, img_url
    drivers_data = [
        ('Max Verstappen', 'Dutch', 'Red Bull Racing', 1, 'VER', 4, 62, 110, 40, 32, 2980, 2015, '1997-09-30', 'Hasselt, Belgium', 1, 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Max_Verstappen_2023_%28cropped%29.jpg/600px-Max_Verstappen_2023_%28cropped%29.jpg'),
        ('Lewis Hamilton', 'British', 'Ferrari', 44, 'HAM', 7, 105, 201, 104, 67, 4850, 2007, '1985-01-07', 'Stevenage, UK', 1, 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Lewis_Hamilton_2016_Malaysia_2.jpg/600px-Lewis_Hamilton_2016_Malaysia_2.jpg'),
        ('Charles Leclerc', 'Monegasque', 'Ferrari', 16, 'LEC', 0, 8, 38, 25, 10, 1500, 2018, '1997-10-16', 'Monte Carlo, Monaco', 1, 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Charles_Leclerc_2019_portrait.jpg/600px-Charles_Leclerc_2019_portrait.jpg'),
        ('Lando Norris', 'British', 'McLaren', 4, 'NOR', 1, 8, 32, 12, 15, 1600, 2019, '1999-11-13', 'Bristol, UK', 1, 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Lando_Norris_2023_%28cropped%29.jpg/600px-Lando_Norris_2023_%28cropped%29.jpg'),
        ('Oscar Piastri', 'Australian', 'McLaren', 81, 'PIA', 0, 3, 12, 1, 5, 600, 2023, '2001-04-06', 'Melbourne, Australia', 1, 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Oscar_Piastri_2023_%28cropped%29.jpg/600px-Oscar_Piastri_2023_%28cropped%29.jpg'),
        ('George Russell', 'British', 'Mercedes', 63, 'RUS', 0, 4, 18, 5, 8, 900, 2019, '1998-02-15', 'King\'s Lynn, UK', 1, 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/George_Russell_2022_%28cropped%29.jpg/600px-George_Russell_2022_%28cropped%29.jpg'),
        ('Kimi Antonelli', 'Italian', 'Mercedes', 12, 'ANT', 0, 0, 0, 0, 0, 0, 2025, '2006-08-25', 'Bologna, Italy', 1, 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Andrea_Kimi_Antonelli_2023.jpg/600px-Andrea_Kimi_Antonelli_2023.jpg'),
        ('Fernando Alonso', 'Spanish', 'Aston Martin', 14, 'ALO', 2, 32, 106, 22, 26, 2300, 2001, '1981-07-29', 'Oviedo, Spain', 1, 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Fernando_Alonso_2023_%28cropped%29.jpg/600px-Fernando_Alonso_2023_%28cropped%29.jpg'),
        ('Carlos Sainz', 'Spanish', 'Williams', 55, 'SAI', 0, 4, 26, 6, 4, 1250, 2015, '1994-09-01', 'Madrid, Spain', 1, 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Carlos_Sainz_Jr._2022_%28cropped%29.jpg/600px-Carlos_Sainz_Jr._2022_%28cropped%29.jpg'),
        ('Alexander Albon', 'Thai', 'Williams', 23, 'ALB', 0, 0, 2, 0, 0, 280, 2019, '1996-03-23', 'London, UK', 1, 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Alexander_Albon_2023_%28cropped%29.jpg/600px-Alexander_Albon_2023_%28cropped%29.jpg'),
        ('Pierre Gasly', 'French', 'Alpine', 10, 'GAS', 0, 1, 4, 0, 3, 460, 2017, '1996-02-07', 'Rouen, France', 1, 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Pierre_Gasly_2023_%28cropped%29.jpg/600px-Pierre_Gasly_2023_%28cropped%29.jpg'),
        ('Liam Lawson', 'New Zealander', 'Red Bull Racing', 30, 'LAW', 0, 0, 0, 0, 0, 50, 2023, '2002-02-11', 'Hastings, New Zealand', 1, 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Liam_Lawson_2023_%28cropped%29.jpg/600px-Liam_Lawson_2023_%28cropped%29.jpg'),
    ]

    # Legends (is_active_2026 = 0)
    # champs, wins, podiums, poles, debut
    legends_data = [
        ('Ayrton Senna', 'Brazilian', None, 1, 'SEN', 3, 41, 80, 65, 19, 614, 1984, '1960-03-21', 'São Paulo, Brazil', 0, 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Ayrton_Senna_80s.jpg/600px-Ayrton_Senna_80s.jpg'),
        ('Michael Schumacher', 'German', None, 5, 'MSC', 7, 91, 155, 68, 77, 1566, 1991, '1969-01-03', 'Hürth, Germany', 0, 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Michael_Schumacher_2012.jpg/600px-Michael_Schumacher_2012.jpg'),
        ('Alain Prost', 'French', None, 2, 'PRO', 4, 51, 106, 33, 41, 798, 1980, '1955-02-24', 'Lorette, France', 0, 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Alain_Prost_1993.jpg/600px-Alain_Prost_1993.jpg'),
        ('Niki Lauda', 'Austrian', None, 12, 'LAU', 3, 25, 54, 24, 24, 420, 1971, '1949-02-22', 'Vienna, Austria', 0, 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Niki_Lauda_1975_%28cropped%29.jpg/600px-Niki_Lauda_1975_%28cropped%29.jpg'),
        ('Sebastian Vettel', 'German', None, 5, 'VET', 4, 53, 122, 57, 38, 3098, 2007, '1987-07-03', 'Heppenheim, Germany', 0, 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Sebastian_Vettel_2022_%28cropped%29.jpg/600px-Sebastian_Vettel_2022_%28cropped%29.jpg'),
    ]

    cursor.execute("DELETE FROM drivers")
    for d in (drivers_data + legends_data):
        cursor.execute("""
            INSERT INTO drivers (name, nationality, team_id, number, abbreviation, championships, wins, podiums, poles, fastest_laps, points_career, debut_year, birth_date, birth_place, is_active_2026, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (d[0], d[1], team_map.get(d[2]), d[3], d[4], d[5], d[6], d[7], d[8], d[9], d[10], d[11], d[12], d[13], d[14], d[15]))

    # 3. Enhanced Timelines (Detailed)
    cursor.execute("DELETE FROM f1_timeline")
    cursor.execute("SELECT id, name FROM drivers")
    d_map = {row['name']: row['id'] for row in cursor.fetchall()}

    timeline_events = [
        # Max Verstappen
        ('driver', d_map['Max Verstappen'], 2015, 'F1 Debut', 'Youngest driver to start a GP at 17 years old with Toro Rosso.', 'debut'),
        ('driver', d_map['Max Verstappen'], 2016, 'Red Bull Promotion & Win', 'Promoted to Red Bull and won Spanish GP on debut.', 'win'),
        ('driver', d_map['Max Verstappen'], 2021, 'First World Championship', 'Won title in dramatic season finale at Abu Dhabi.', 'championship'),
        ('driver', d_map['Max Verstappen'], 2022, 'Title Defense', 'Dominant season with 15 wins, clinching title in Japan.', 'championship'),
        ('driver', d_map['Max Verstappen'], 2023, 'Historic Dominance', 'Won record 19 races in a single season.', 'championship'),
        
        # Lando Norris
        ('driver', d_map['Lando Norris'], 2019, 'McLaren Debut', 'Made F1 debut as youngest British driver.', 'debut'),
        ('driver', d_map['Lando Norris'], 2021, 'First Pole Position', 'Clinched maiden pole in Sochi under tricky conditions.', 'record'),
        ('driver', d_map['Lando Norris'], 2024, 'First F1 Win', 'Won the Miami GP after a strategic masterpiece.', 'win'),
        ('driver', d_map['Lando Norris'], 2025, 'World Champion 🏆', 'Beat Max Verstappen to win his first World Championship in a historic title fight.', 'championship'),

        # Lewis Hamilton
        ('driver', d_map['Lewis Hamilton'], 2007, 'Brilliant Debut', 'Finished on podium in debut race, equal points with Alonso.', 'debut'),
        ('driver', d_map['Lewis Hamilton'], 2008, 'First Title', 'Youngest ever champion at the time with McLaren.', 'championship'),
        ('driver', d_map['Lewis Hamilton'], 2014, 'Mercedes First Title', 'Began the modern era dominance with Mercedes.', 'championship'),
        ('driver', d_map['Lewis Hamilton'], 2025, 'The Ferrari Era', 'Leaves Mercedes after 12 years to join Scuderia Ferrari.', 'transfer'),

        # Team Ferrari
        ('team', team_map['Ferrari'], 1929, 'Founding', 'Enzo Ferrari establishes the racing team in Modena.', 'founded'),
        ('team', team_map['Ferrari'], 1950, 'F1 Entry', 'Ferrari joined F1 at the 1950 Monaco Grand Prix.', 'debut'),
        ('team', team_map['Ferrari'], 2000, 'The Golden Era', 'Schumacher begins run of 5 consecutive titles.', 'championship'),
        ('team', team_map['Ferrari'], 2025, 'Hamilton Joins', 'Lewis Hamilton joins Ferrari in the most seismic move in F1 history.', 'transfer'),
        ('team', team_map['Ferrari'], 2026, 'New Era', 'Ferrari enters the new engine regulation era as favorites.', 'technical'),

        # Team McLaren
        ('team', team_map['McLaren'], 1963, 'Founding', 'Bruce McLaren founded the team in Woking.', 'founded'),
        ('team', team_map['McLaren'], 1988, 'Dominance', 'Won 15 out of 16 races with Senna and Prost.', 'record'),
        ('team', team_map['McLaren'], 2024, 'Return to Top', 'McLaren becomes the fastest car on the grid again.', 'technical'),
        ('team', team_map['McLaren'], 2025, 'World Champion Team', 'Wins the Constructors title and Lando wins WDC.', 'championship'),
    ]

    cursor.executemany("""
        INSERT INTO f1_timeline (entity_type, entity_id, year, title, description, milestone_type)
        VALUES (?, ?, ?, ?, ?, ?)
    """, timeline_events)

    conn.commit()
    conn.close()
    print("✅ F1 Data Seeding Complete (Updated for 2025/2026).")

if __name__ == "__main__":
    seed_f1_complete()
