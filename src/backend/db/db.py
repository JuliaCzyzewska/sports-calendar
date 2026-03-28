import sqlite3

def init_db():
    try:
        with sqlite3.connect("data/calendar_data.db") as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cur = conn.cursor()

            cur.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                status TEXT DEFAULT 'scheduled', 
                season INTEGER NOT NULL,
                dateVenue TEXT,             -- YYYY-MM-DD
                timeVenueUTC TEXT,          -- HH:MM:SS 
                _stage_id INTEGER,
                _venue_id INTEGER,
                _competition_id INTEGER NOT NULL,
                
                FOREIGN KEY (_stage_id) REFERENCES stages(id)
                    ON UPDATE CASCADE
                
                FOREIGN KEY (_venue_id) REFERENCES venues(id)
                    ON UPDATE CASCADE
                        
                FOREIGN KEY (_competition_id) REFERENCES competitions(id)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT      -- dont let delete if its connected to event
            )
            """)
                        
                        
            cur.execute("""
            CREATE TABLE IF NOT EXISTS competitions (
                id INTEGER PRIMARY KEY AUTOINCREMENT
            )
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS stages (
                id INTEGER PRIMARY KEY AUTOINCREMENT
            )
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS venues (
                id INTEGER PRIMARY KEY AUTOINCREMENT

            )
            """)


    except Exception as e:
        print("SQLite error:", e)


if __name__ == "__main__":
    init_db()