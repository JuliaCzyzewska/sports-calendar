from fastapi import HTTPException
from collections import defaultdict

from src.backend.models.event import EventResponse
from src.backend.models.competition import CompetitionResponse
from src.backend.models.stage import StageResponse
from src.backend.models.venue import VenueResponse
from src.backend.models.country import CountryResponse
from src.backend.models.participant import ParticipantResponse
from src.backend.models.entity import EntityResponse


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

PARTICIPANTS_QUERY = """
    SELECT 
        p.id, 
        p._event_id as event_id, 
        p.role, 
        p.stage_position,
        en.id as entity_id,
        en.type as entity_type, 
        en.name as entity_name,
        en.official_name as entity_official_name, 
        en.slug as entity_slug,
        en.abbreviation as entity_abbreviation,
        cn.abbreviation as country_abbreviation, 
        cn.name as country_name
    FROM participants p
    JOIN entities en ON p._entity_id = en.id
    JOIN countries cn ON en._country_id = cn.id
    WHERE p._event_id IN ({placeholders})      
"""   # placeholders - stirng of "?", "?"...; placeholder of ids of all needed events


def fetch_participants_by_event(db, event_ids: list[int]) -> dict[int, list[ParticipantResponse]]:
    placeholders = ",".join("?" * len(event_ids))
    rows = db.execute(
        PARTICIPANTS_QUERY.format(placeholders=placeholders),
        event_ids
    ).fetchall()

    participants_by_event = defaultdict(list)
    for row in rows:
        participants_by_event[row["event_id"]].append(
            ParticipantResponse(
                role=row["role"],
                stage_position=row["stage_position"],
                entity_id=row["entity_id"],
                entity_name=row["entity_name"],
                entity=EntityResponse(
                    type=row["entity_type"],
                    name=row["entity_name"],
                    official_name=row["entity_official_name"],
                    slug=row["entity_slug"],
                    abbreviation=row["entity_abbreviation"],
                    country=CountryResponse(
                        abbreviation=row["country_abbreviation"],
                        name=row["country_name"]
                    )
                )
            )
        )
    return participants_by_event


def row_to_event_response(row, participants: list[ParticipantResponse]) -> EventResponse:
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
            ),

            participants=participants
    )

def get_all_events(db) -> list[EventResponse]:
    cur = db.cursor()
    results = cur.execute(EVENTS_QUERY).fetchall()
    if not results:
        return []
    event_ids = [row["id"] for row in results]
    participants_by_event = fetch_participants_by_event(db, event_ids)

    return [row_to_event_response(row, participants_by_event[row["id"]]) for row in results]


def get_one_event(event_id: int, db) -> EventResponse:
    cur = db.cursor()
    result = cur.execute(
        EVENTS_QUERY + "WHERE e.id = ?", [event_id]
    ).fetchone()
    if not result:
            raise HTTPException(status_code=404, detail="Event not found")
    
    participants_by_event = fetch_participants_by_event(db, [event_id])
    return row_to_event_response(result, participants_by_event[result["id"]])