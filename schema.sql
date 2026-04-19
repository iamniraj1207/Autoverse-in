-- AutoVerse Database Schema
-- Run once: sqlite3 autoverse.db < schema.sql

CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT NOT NULL UNIQUE,
    hash        TEXT NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cars (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    brand          TEXT NOT NULL,
    model          TEXT NOT NULL,
    year           INTEGER NOT NULL,
    engine         TEXT,
    horsepower     INTEGER,
    torque         INTEGER,
    fuel_type      TEXT,
    acceleration   REAL,   -- 0-60 mph in seconds
    price_usd      INTEGER,
    description    TEXT,
    category       TEXT,   -- 'Supercar', 'Hypercar', 'Sports', 'Luxury', 'EV', 'SUV'
    top_speed      INTEGER, -- in km/h
    drivetrain     TEXT,   -- 'RWD', 'AWD', 'FWD', '4WD'
    weight_kg      INTEGER,
    origin_country TEXT,
    image_url      TEXT    -- Supports comma-separated HD URLs
);

CREATE TABLE IF NOT EXISTS garage (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(id),
    car_id      INTEGER NOT NULL REFERENCES cars(id),
    added_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, car_id)
);

CREATE TABLE IF NOT EXISTS teams (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    full_name       TEXT,
    nationality     TEXT,
    base            TEXT,
    team_principal  TEXT,
    power_unit      TEXT,
    championships   INTEGER DEFAULT 0,
    wins            INTEGER DEFAULT 0,
    podiums         INTEGER DEFAULT 0,
    poles           INTEGER DEFAULT 0,
    fastest_laps    INTEGER DEFAULT 0,
    founded_year    INTEGER,
    first_entry     INTEGER,
    logo_url        TEXT,
    car_image_url   TEXT,
    primary_color   TEXT,   -- Hex code
    bio             TEXT,
    is_active_2026  INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS drivers (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    nationality     TEXT,
    team_id         INTEGER REFERENCES teams(id),
    number          INTEGER,
    abbreviation    TEXT,
    championships   INTEGER DEFAULT 0,
    wins            INTEGER DEFAULT 0,
    podiums         INTEGER DEFAULT 0,
    poles           INTEGER DEFAULT 0,
    fastest_laps    INTEGER DEFAULT 0,
    points_career   REAL DEFAULT 0,
    debut_year      INTEGER,
    birth_date      TEXT,
    birth_place     TEXT,
    image_url       TEXT,
    helmet_image_url TEXT,
    bio             TEXT,
    is_active       INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS f1_timeline (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type     TEXT NOT NULL, -- 'driver' | 'team'
    entity_id       INTEGER NOT NULL,
    year            INTEGER NOT NULL,
    title           TEXT NOT NULL,
    description     TEXT,
    milestone_type  TEXT, -- 'championship' | 'win' | 'debut' | 'record' | 'tragedy' | 'technical' | 'transfer'
    image_url       TEXT
);

CREATE TABLE IF NOT EXISTS f1_fastest_laps (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    driver_id       INTEGER NOT NULL REFERENCES drivers(id),
    team_id         INTEGER NOT NULL REFERENCES teams(id),
    circuit         TEXT NOT NULL,
    grand_prix      TEXT NOT NULL,
    year            INTEGER NOT NULL,
    lap_time        TEXT NOT NULL,
    speed_kmh       REAL
);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_cars_brand ON cars(brand);
CREATE INDEX IF NOT EXISTS idx_garage_user ON garage(user_id);
CREATE INDEX IF NOT EXISTS idx_drivers_team ON drivers(team_id);
CREATE INDEX IF NOT EXISTS idx_timeline_entity ON timeline(entity_type, entity_id);
