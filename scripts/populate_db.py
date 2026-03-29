import sqlite3
import json

data_files_paths = {
    "countries": "seeds/countries.json",
    "competitions": "seeds/competitions.json",
}

def load_table_data_from_json(table_name: str):
    path = data_files_paths[table_name]
    if not path:
            raise ValueError(f"No JSON path configured for table '{table_name}'")
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(table_name, [])


def populate_countries(cur):
    data = load_table_data_from_json("countries")
    cur.executemany("""
        INSERT OR IGNORE INTO countries (name, abbreviation)
        VALUES (?, ?)
    """, [(d.get("name"), d.get("abbreviation")) for d in data])

def populate_competitions(cur):
    data = load_table_data_from_json("competitions")
    cur.executemany("""
        INSERT OR IGNORE INTO competitions (name, slug, sport_type, participation_type)
        VALUES (?, ?, ?, ?)
    """, [(d.get("name"), d.get("slug"), d.get("sport_type"), d.get("participation_type")) for d in data])


def populate_db():
    with sqlite3.connect("data/calendar_data.db") as conn:
        cur = conn.cursor()

        # stage 1
        populate_countries(cur)
        populate_competitions(cur)
        conn.commit()



if __name__ == "__main__":
    populate_db()