import sqlite3

def fix_data():
    conn = sqlite3.connect('autoverse.db')
    db = conn.cursor()
    
    # LANDO NORRIS Correct Data - 2025 (verified)
    print("Fixing Lando Norris...")
    db.execute("""
        UPDATE drivers SET 
        championships = 0,
        wins = 6,
        podiums = 38,
        poles = 10,
        fastest_laps = 14,
        is_active_2026 = 1
        WHERE name LIKE '%Lando%'
    """)

    # OSCAR PIASTRI Correct Data
    print("Fixing Oscar Piastri...")
    db.execute("""
        UPDATE drivers SET 
        wins = 5,
        championships = 0,
        is_active_2026 = 1
        WHERE name LIKE '%Oscar%Piastri%'
    """)

    # CARLOS SAINZ Correct Data
    print("Fixing Carlos Sainz...")
    db.execute("""
        UPDATE drivers SET 
        wins = 5,
        is_active_2026 = 1
        WHERE name LIKE '%Carlos%Sainz%'
    """)

    # GEORGE RUSSELL Correct Data
    print("Fixing George Russell...")
    db.execute("""
        UPDATE drivers SET 
        wins = 3,
        is_active_2026 = 1
        WHERE name LIKE '%George%Russell%'
    """)

    # MAX VERSTAPPEN - Correcting 2025/2026 data
    print("Fixing Max Verstappen...")
    db.execute("""
        UPDATE drivers SET 
        is_active_2026 = 1
        WHERE name LIKE '%Max%Verstappen%'
    """)

    # RETIRED LEGENDS
    print("Fixing Legends...")
    legends = ['Ayrton Senna', 'Michael Schumacher', 'Alain Prost', 'Niki Lauda', 'Juan Manuel Fangio', 'Jim Clark', 'Jackie Stewart', 'Nigel Mansell', 'Sebastian Vettel', 'Jenson Button', 'Kimi Raikkonen', 'Mika Hakkinen', 'Damon Hill']
    for legend in legends:
        db.execute("UPDATE drivers SET is_active_2026 = 0 WHERE name = ?", (legend,))

    conn.commit()
    conn.close()
    print("Data fix complete.")

if __name__ == "__main__":
    fix_data()
