import sqlite3
from src.backend.models.event import EventResponse
from src.backend.models.competition import CompetitionResponse
from src.backend.models.stage import StageResponse
from src.backend.models.venue import VenueResponse
from src.backend.models.country import CountryResponse
from fastapi import HTTPException

EVENTS_QUERY = """
    SELECT 
        e.id,
        e.status,
        e.season,
        e.date_venue,
        e.time_venue_utc,
        s.id as stage_id,
        s.name as stage_name,
        s.ordering as stage_ordering,
        v.name as venue_name,
        v.city as venue_city,
        cn.name as country_name,
        cn.abbreviation as country_abbreviation,
        c.slug as competition_slug,
        c.name as competition_name,
        c.sport_type as sport_type,
        c.participation_type as participation_type
    FROM events e
    JOIN competitions c ON e._competition_slug = c.slug
    LEFT JOIN venues v ON e._venue_id = v.id
    LEFT JOIN countries cn ON v._country_id = cn.id
    LEFT JOIN stages s ON e._stage_id = s.id
"""



def row_to_event_response(row) -> EventResponse:
    return EventResponse(
            status=row["status"],
            season=row["season"],
            date_venue=row["date_venue"],
            time_venue_utc=row["time_venue_utc"],

            stage=StageResponse(
                name=row["stage_name"],
                ordering=row["stage_ordering"]
            ) if row["stage_id"] else None,
        
            venue=VenueResponse(
                name=row["venue_name"],
                city=row["venue_city"],
                country=CountryResponse(
                    abbreviation=row["country_abbreviation"],
                    name=row["country_name"]
                )
            ) if row["venue_name"] else None,


            competition=CompetitionResponse(
                slug=row["competition_slug"],
                name=row["competition_name"],
                sport_type=row["sport_type"],
                participation_type=row["participation_type"]
            )
    )

def get_all_events(db) -> list[EventResponse]:
    cur = db.cursor()
    results = cur.execute(EVENTS_QUERY).fetchall()
    return [row_to_event_response(row) for row in results]


def get_one_event(event_id: int, db) -> EventResponse:
    cur = db.cursor()
    result = cur.execute(
        EVENTS_QUERY + "WHERE e.id = ?", [event_id]
    ).fetchone()
    if not result:
            raise HTTPException(status_code=404, detail="Event not found")
    return row_to_event_response(result)