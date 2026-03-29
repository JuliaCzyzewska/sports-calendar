import sqlite3
import json

data_files_paths = {
    "countries": "seeds/countries.json"
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



def populate_db():
    with sqlite3.connect("data/calendar_data.db") as conn:
        cur = conn.cursor()
        populate_countries(cur)
        conn.commit()



if __name__ == "__main__":
    populate_db()