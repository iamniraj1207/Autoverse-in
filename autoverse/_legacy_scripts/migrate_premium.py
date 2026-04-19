import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'autoverse.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def run_migration():
    print("Starting Premium Migrations...")
    
    # 1. Alter existing tables
    alterations = [
        "ALTER TABLE cars ADD COLUMN image_exterior TEXT",
        "ALTER TABLE cars ADD COLUMN image_interior TEXT",
        "ALTER TABLE cars ADD COLUMN image_side TEXT",
        "ALTER TABLE cars ADD COLUMN image_rear TEXT",
        "ALTER TABLE teams ADD COLUMN logo_svg_path TEXT"
    ]
    
    for sql in alterations:
        try:
            cursor.execute(sql)
            print(f"SUCCESS: {sql}")
        except sqlite3.OperationalError as e:
            print(f"INFO: {sql} - {e}")

    # 2. Create new tables
    tables = [
        """
        CREATE TABLE IF NOT EXISTS f1_champions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER UNIQUE,
            driver_name TEXT,
            team_name TEXT,
            wins_that_season INTEGER,
            points INTEGER
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS academy_courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            slug TEXT UNIQUE,
            description TEXT,
            category TEXT,  -- 'cars' | 'f1' | 'engineering' | 'history'
            difficulty TEXT, -- 'beginner' | 'intermediate' | 'expert'
            total_xp INTEGER,
            icon TEXT,       -- emoji icon
            color TEXT,      -- hex color for course card
            order_num INTEGER
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS academy_lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER REFERENCES academy_courses(id),
            title TEXT,
            slug TEXT,
            lesson_type TEXT, -- 'learn'|'quiz'|'challenge'|'visual'
            content_json TEXT, -- JSON blob of lesson content
            xp_reward INTEGER,
            order_num INTEGER
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS academy_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_id INTEGER REFERENCES academy_lessons(id),
            question_type TEXT, -- 'multiple_choice'|'true_false'|'identify_car'|'match_spec'|'fill_blank'|'order_timeline'
            question TEXT,
            options_json TEXT,  -- JSON array of options
            correct_answer TEXT,
            explanation TEXT,
            image_url TEXT,
            xp_reward INTEGER
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(id),
            lesson_id INTEGER REFERENCES academy_lessons(id),
            completed INTEGER DEFAULT 0,
            score INTEGER DEFAULT 0,
            xp_earned INTEGER DEFAULT 0,
            completed_at TIMESTAMP,
            streak_day INTEGER DEFAULT 0
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS user_xp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE REFERENCES users(id),
            total_xp INTEGER DEFAULT 0,
            current_streak INTEGER DEFAULT 0,
            longest_streak INTEGER DEFAULT 0,
            last_activity DATE,
            level INTEGER DEFAULT 1,
            badges_json TEXT DEFAULT '[]'
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(id),
            username TEXT,
            total_xp INTEGER,
            level INTEGER,
            rank INTEGER,
            updated_at TIMESTAMP
        )
        """
    ]
    
    for sql in tables:
        try:
            cursor.execute(sql)
            print(f"SUCCESS: Created table.")
        except Exception as e:
            print(f"ERROR: {e}")

    conn.commit()
    conn.close()
    print("Premium Migrations Complete.")

if __name__ == "__main__":
    run_migration()
