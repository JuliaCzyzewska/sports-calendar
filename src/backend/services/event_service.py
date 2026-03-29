import sqlite3
from src.backend.models.event import EventResponse

def row_to_event_response(row) -> EventResponse:
    return EventResponse(
            status=row["status"],
            season=row["season"],
            date_venue=row["date_venue"],
            time_venue_utc=row["time_venue_utc"],
            stage_id=row["_stage_id"],
            venue_id=row["_venue_id"],
            competition_slug=row["_competition_slug"]
    )

def get_all_events(db):
    cur = db.cursor()
    results = cur.execute("""
    SELECT * FROM events
    """).fetchall()
    return [row_to_event_response(row) for row in results]
