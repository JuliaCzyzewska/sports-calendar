import sqlite3
import json

data_files_paths = {
    "countries": "seeds/countries.json",
    "competitions": "seeds/competitions.json",
    "venues": "seeds/venues.json",
    "entities": "seeds/entities.json",
    "stages": "seeds/stages.json",
    "events": "seeds/events.json",
    "participants": "seeds/participants.json",
    "event_incidents": "seeds/event_incidents.json",
    "participant_scores": "seeds/participant_scores.json",
    "event_results": "seeds/event_results.json",
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
        INSERT OR IGNORE INTO countries (abbreviation, name)
        VALUES (?, ?)
    """, [(d.get("abbreviation"), d.get("name")) for d in data])

def populate_competitions(cur):
    data = load_table_data_from_json("competitions")
    cur.executemany("""
        INSERT OR IGNORE INTO competitions (slug, name, sport_type, participation_type)
        VALUES (?, ?, ?, ?)
    """, [(d.get("slug"), d.get("name"), d.get("sport_type"), d.get("participation_type")) for d in data])


def populate_venues(cur):
    data = load_table_data_from_json("venues")
    cur.executemany("""
        INSERT OR IGNORE INTO venues (name, city, _country_id)
        VALUES (?, ?, ?)
    """, [(d.get("name"), d.get("city"), d.get("_country_id")) for d in data])


def populate_entites(cur):
    data = load_table_data_from_json("entities")
    cur.executemany("""
        INSERT OR IGNORE INTO entities (type, name, official_name, slug, abbreviation, _country_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [(d.get("type"), d.get("name"), d.get("official_name"), d.get("slug"), d.get("abbreviation"), d.get("_country_id")) for d in data])


def populate_stages(cur):
    data = load_table_data_from_json("stages")
    cur.executemany("""
        INSERT OR IGNORE INTO stages (_competition_slug, name, ordering)
        VALUES (?, ?, ?)
    """, [(d.get("_competition_slug"), d.get("name"), d.get("ordering")) for d in data])


def populate_events(cur):
    data = load_table_data_from_json("events")
    cur.executemany("""
        INSERT OR IGNORE INTO events (status, season, date_venue, time_venue_UTC, _stage_id, _venue_id, _competition_slug)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [(d.get("status"), d.get("season"), d.get("date_venue"), d.get("time_venue_UTC"), d.get("_stage_id"), d.get("_venue_id"), d.get("_competition_slug")) for d in data])



def populate_participants(cur):
    data = load_table_data_from_json("participants")
    cur.executemany("""
        INSERT OR IGNORE INTO participants (_event_id, _entity_id, role, stage_position)
        VALUES (?, ?, ?, ?)
    """, [(d.get("_event_id"), d.get("_entity_id"), d.get("role"), d.get("stage_position")) for d in data])


def populate_event_incidents(cur):
    data = load_table_data_from_json("event_incidents")
    cur.executemany("""
        INSERT OR IGNORE INTO event_incidents (_participant_id, _entity_id, incident_type, minute)
        VALUES (?, ?, ?, ?)
    """, [(d.get("_participant_id"), d.get("_entity_id"), d.get("incident_type"), d.get("minute")) for d in data])



def populate_participant_scores(cur):
    data = load_table_data_from_json("participant_scores")
    cur.executemany("""
        INSERT OR IGNORE INTO participant_scores (_participant_id, score_value, score_label)
        VALUES (?, ?, ?)
    """, [(d.get("_participant_id"), d.get("score_value"), d.get("score_label")) for d in data])



def populate_event_results(cur):
    data = load_table_data_from_json("event_results")
    cur.executemany("""
        INSERT OR IGNORE INTO event_results (_event_id, category, _entity_id, outcome_type, message)
        VALUES (?, ?, ?, ?, ?)
    """, [(d.get("_event_id"), d.get("category"), d.get("_entity_id"), d.get("outcome_type"), d.get("message")) for d in data])
    





def populate_db():
    with sqlite3.connect("data/calendar_data.db") as conn:
        cur = conn.cursor()
        conn.execute("PRAGMA foreign_keys = ON")

        # stage 1 - competitions, countries
        populate_countries(cur)
        populate_competitions(cur)
        conn.commit()

        # stage 2 - venues, entities, stages
        populate_venues(cur)
        populate_entites(cur)
        populate_stages(cur)
        conn.commit()

        # stage 3 - events
        populate_events(cur)
        conn.commit()

        # stage 4 - participants
        populate_participants(cur)
        conn.commit()


        # stage 5 - event_incidents, participant_scores, event_results
        populate_event_incidents(cur)
        populate_participant_scores(cur)
        populate_event_results(cur)
        conn.commit()




if __name__ == "__main__":
    populate_db()