from fastapi import HTTPException
from collections import defaultdict

from src.backend.models.event import EventResponse, EventCreate
from src.backend.models.competition import CompetitionSchema
from src.backend.models.stage import StageResponse
from src.backend.models.venue import VenueResponse
from src.backend.models.country import CountryResponse
from src.backend.models.participant import ParticipantResponse
from src.backend.models.entity import EntityResponse
from src.backend.models.participant_score import ParticipantScoreSchema
from src.backend.models.event_incident import EventIncidentResponse
from src.backend.models.event_result import EventResultResponse

from src.backend.services.shared_queries import fetch_participants_by_event, fetch_results_by_event

EVENTS_QUERY = """
    SELECT 
        e.id as event_id,
        e.status,
        e.season,
        e.date_venue,
        e.time_venue_utc,
        s.id as stage_id,
        s.name as stage_name,
        s.ordering as stage_ordering,
        v.id as venue_id,
        v.name as venue_name,
        v.city as venue_city,
        cn.id as country_id,
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



POST_EVENT_QUERY = """
    INSERT INTO events (
        status, 
        season, 
        date_venue, 
        time_venue_utc, 
        _stage_id, 
        _venue_id, 
        _competition_slug
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
"""



def row_to_event_response(row, participants: list[ParticipantResponse], results: list[EventResultResponse]) -> EventResponse:
    return EventResponse(
            id=row["event_id"],
            status=row["status"],
            season=row["season"],
            date_venue=row["date_venue"],
            time_venue_utc=row["time_venue_utc"],

            stage=StageResponse(
                id=row["stage_id"],
                name=row["stage_name"],
                ordering=row["stage_ordering"]
            ) if row["stage_id"] else None,
        
            venue=VenueResponse(
                id=row["venue_id"],
                name=row["venue_name"],
                city=row["venue_city"],
                country=CountryResponse(
                    id=row["country_id"],
                    abbreviation=row["country_abbreviation"],
                    name=row["country_name"]
                )
            ) if row["venue_name"] else None,


            competition=CompetitionSchema(
                slug=row["competition_slug"],
                name=row["competition_name"],
                sport_type=row["sport_type"],
                participation_type=row["participation_type"]
            ),

            participants=participants or None,
            results=results or None
    )

def get_all_events(db) -> list[EventResponse]:
    cur = db.cursor()
    rows = cur.execute(EVENTS_QUERY).fetchall()
    if not rows:
        return []
    event_ids = [row["event_id"] for row in rows]
    participants_by_event = fetch_participants_by_event(db, event_ids)
    results_by_event = fetch_results_by_event(db, event_ids)

    return [row_to_event_response(row, participants_by_event.get(row["event_id"], []), results_by_event.get(row["event_id"], [])) for row in rows]


def get_one_event(event_id: int, db) -> EventResponse:
    cur = db.cursor()
    row = cur.execute(
        EVENTS_QUERY + " WHERE e.id = ?", [event_id]
    ).fetchone()
    if not row:
            raise HTTPException(status_code=404, detail="Event not found")
    
    participants_by_event = fetch_participants_by_event(db, [event_id])
    results_by_event = fetch_results_by_event(db, [event_id])
    return row_to_event_response(row, participants_by_event.get(row["event_id"], []), results_by_event.get(row["event_id"], []))


def post_event(event: EventCreate, db) -> EventResponse:
    cur = db.cursor()

    # validate FKs
    competition = cur.execute(
        "SELECT slug FROM competitions WHERE slug = ?",
        [event.competition_slug]
    ).fetchone()
    if not competition:
        raise HTTPException(404, detail="Competition not found")

    if event.stage_id:
        stage = cur.execute(
            "SELECT id FROM stages WHERE id = ? AND _competition_slug = ?",
            [event.stage_id, event.competition_slug]
        ).fetchone()
        if not stage:
            raise HTTPException(404, detail="Stage not found for this competition")

    if event.venue_id:
        venue = cur.execute(
            "SELECT id FROM venues WHERE id = ?",
            [event.venue_id]
        ).fetchone()
        if not venue:
            raise HTTPException(404, detail="Venue not found")
        


    # insert
    try:
        cur.execute(POST_EVENT_QUERY, [
            event.status, 
            event.season,
            event.date_venue.isoformat() if event.date_venue else None,
            event.time_venue_utc.isoformat() if event.time_venue_utc else None,
            event.stage_id,
            event.venue_id,
            event.competition_slug
        ])
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(500, detail=f"Failed to create event: {e}")


    # fetch
    return get_one_event(cur.lastrowid, db)