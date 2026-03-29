import sqlite3

def init_db():
    try:
        with sqlite3.connect("data/calendar_data.db") as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cur = conn.cursor()

            cur.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                status TEXT DEFAULT 'scheduled' CHECK(status IN ('scheduled','cancelled','played', 'live')),
                season INTEGER NOT NULL,
                date_venue TEXT,             -- YYYY-MM-DD
                time_venue_UTC TEXT,          -- HH:MM:SS 
                _stage_id INTEGER,
                _venue_id INTEGER,
                _competition_slug TEXT NOT NULL,
                
                FOREIGN KEY (_stage_id) REFERENCES stages(id)
                    ON UPDATE CASCADE
                
                FOREIGN KEY (_venue_id) REFERENCES venues(id)
                    ON UPDATE CASCADE
                        
                FOREIGN KEY (_competition_slug) REFERENCES competitions(slug)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT      -- dont let competition be deleted if its connected to event
            )
            """)

              
            cur.execute("""
            CREATE TABLE IF NOT EXISTS competitions (
                slug TEXT NOT NULL PRIMARY KEY,
                name TEXT NOT NULL,
                sport_type TEXT NOT NULL,
                participation_type TEXT NOT NULL CHECK(participation_type IN ('team', 'individual', 'relay'))
            )
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS stages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                _competition_slug TEXT NOT NULL,
                name TEXT,
                ordering INTEGER CHECK(ordering > 0),
                
                UNIQUE (_competition_slug, name),
                
                FOREIGN KEY (_competition_slug) REFERENCES competitions(slug)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE 
            )
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS venues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL, 
                city NAME,
                _country_abr INTEGER NOT NULL,
                
                FOREIGN KEY (_country_abr) REFERENCES countries(abbreviation)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT  
            )
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS countries (
                abbreviation TEXT PRIMARY KEY,
                name TEXT NOT NULL
            )
            """)


            cur.execute("""
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL CHECK(type IN ('team', 'athlete')),
                name TEXT NOT NULL,
                official_name TEXT NOT NULL,
                slug TEXT NOT NULL UNIQUE,
                abbreviation TEXT,      -- null for athelete
                _country_abr INTEGER NOT NULL,
                        
                FOREIGN KEY (_country_abr) REFERENCES countries(abbreviation)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT           
            )
            """)


            cur.execute("""
            CREATE TABLE IF NOT EXISTS participants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                _event_id INTEGER NOT NULL,
                _entity_id INTEGER NOT NULL,
                role TEXT DEFAULT 'entry' CHECK(role IN ('home', 'away', 'entry')),
                stage_position INTEGER CHECK (stage_position > 0),
                
                UNIQUE (_event_id, _entity_id),
                
                FOREIGN KEY (_event_id) REFERENCES events(id)
                    ON UPDATE CASCADE
                
                FOREIGN KEY (_entity_id) REFERENCES entities(id)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT        
            )
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS participant_score (
                _participant_id INTEGER NOT NULL,
                score_value NUMERIC NOT NULL,
                score_label TEXT NOT NULL,    -- points, goals, etc
                
                FOREIGN KEY (_participant_id) REFERENCES participants(id)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT 
                
                PRIMARY KEY(_participant_id, score_label)
            )
            """)


            cur.execute("""
            CREATE TABLE IF NOT EXISTS event_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,        
                _event_id INTEGER NOT NULL,
                category TEXT,          -- NULL if it does not have categories, men, women -60kg, etc
                _entity_id INTEGER, 
                outcome_type TEXT DEFAULT 'win' CHECK (outcome_type IN('win', 'draw', 'canceled', 'abandoned')),
                message TEXT,
                
                UNIQUE (_event_id, category),     -- one result per category per event
                        
                FOREIGN KEY (_event_id) REFERENCES events(id)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT
                
                FOREIGN KEY (_entity_id) REFERENCES entities(id)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT 

                CHECK (
                    (outcome_type = 'win' AND _entity_id IS NOT NULL) OR
                    (outcome_type != 'win' AND _entity_id IS NULL)
                )
            )
            """)


            cur.execute("""
            CREATE TABLE IF NOT EXISTS event_incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                _event_id INTEGER NOT NULL,
                _participant_id INTEGER NOT NULL,   -- team or athlete
                _entity_id INTEGER,                 -- specific athlete
                incident_type TEXT NOT NULL,        -- yellow card, red_card etc
                minute INTEGER,                     -- time during event when incident happened
                        
                FOREIGN KEY (_event_id) REFERENCES events(id)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT

                FOREIGN KEY (_participant_id) REFERENCES participants(id)
                    ON UPDATE CASCADE
                        
                FOREIGN KEY (_entity_id) REFERENCES entities(id)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT                    
                    
            )
            """)

    except Exception as e:
        print("SQLite error:", e)


if __name__ == "__main__":
    init_db()