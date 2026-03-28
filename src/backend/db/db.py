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
                _competition_id INTEGER NOT NULL,
                
                FOREIGN KEY (_stage_id) REFERENCES stages(id)
                    ON UPDATE CASCADE
                
                FOREIGN KEY (_venue_id) REFERENCES venues(id)
                    ON UPDATE CASCADE
                        
                FOREIGN KEY (_competition_id) REFERENCES competitions(id)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT      -- dont let competition be deleted if its connected to event
            )
            """)



              
            cur.execute("""
            CREATE TABLE IF NOT EXISTS competitions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                sport_type TEXT NOT NULL,
                participation_type TEXT NOT NULL CHECK(participation_type IN ('team', 'individual', 'relay'))
            )
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS stages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                _competition_id INTEGER NOT NULL,
                name TEXT,
                ordering INTEGER CHECK(ordering > 0),
                
                FOREIGN KEY (_competition_id) REFERENCES competitions(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE 
            )
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS venues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL, 
                city NAME,
                _country_id INTEGER NOT NULL,
                
                FOREIGN KEY (_country_id) REFERENCES countries(id)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT 
                        
            )
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS countries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                abbreviation TEXT NOT NULL
            )
            """)


            cur.execute("""
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL CHECK(type IN ('team', 'athelete')),
                name TEXT NOT NULL,
                official_name TEXT NOT NULL,
                slug TEXT NOT NULL,
                abbreviation TEXT,
                _country_id INTEGER NOT NULL,
                        
                FOREIGN KEY (_country_id) REFERENCES countries(id)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT           
            )
            """)


            cur.execute("""
            CREATE TABLE IF NOT EXISTS event_participant (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                _event_id INTEGER NOT NULL,
                _entity_id INTEGER NOT NULL,
                role TEXT DEFAULT 'entry' CHECK(role IN ('home', 'away', 'entry')),
                stage_position INTEGER CHECK (stage_position > 0),
                
                FOREIGN KEY (_event_id) REFERENCES event(id)
                    ON UPDATE CASCADE
            )
            """)


    except Exception as e:
        print("SQLite error:", e)


if __name__ == "__main__":
    init_db()