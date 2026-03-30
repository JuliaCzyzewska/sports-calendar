from fastapi import HTTPException
from src.backend.models.event_incident import EventIncidentCreate, EventIncidentResponse
from src.backend.models.entity import EntityResponse
from src.backend.models.country import CountryResponse

INCIDENTS_QUERY = """
    SELECT
        ei.id as event_incident_id,
        ei._entity_id as entity_id,
        en.type as entity_type,
        en.name as entity_name,
        en.official_name as entity_official_name,
        en.slug as entity_slug,
        en.abbreviation as entity_abbreviation,
        cn.id as country_id,
        cn.abbreviation as country_abbreviation,
        cn.name as country_name,
        ei.incident_type,
        ei.minute
    FROM event_incidents ei
    LEFT JOIN entities en ON ei._entity_id = en.id
    LEFT JOIN countries cn ON en._country_id = cn.id
    WHERE ei._participant_id = ?
"""

POST_INCIDENT_QUERY = """
    INSERT INTO event_incidents (_participant_id, _entity_id, incident_type, minute)
    VALUES (?, ?, ?, ?)
"""

def row_to_incident_response(row) -> EventIncidentResponse:
    return EventIncidentResponse(
        id=row["event_incident_id"],
        incident_type=row["incident_type"],
        minute=row["minute"],
        entity=EntityResponse(
            id=row["entity_id"],
            type=row["entity_type"],
            name=row["entity_name"],
            official_name=row["entity_official_name"],
            slug=row["entity_slug"],
            abbreviation=row["entity_abbreviation"],
            country=CountryResponse(
                id=row["country_id"],
                abbreviation=row["country_abbreviation"],
                name=row["country_name"]
            )
        ) if row["entity_id"] else None
    )

def validate_participant(event_id: int, participant_id: int, db):
    participant = db.execute(
        "SELECT id FROM participants WHERE id = ? AND _event_id = ?",
        [participant_id, event_id]
    ).fetchone()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found for this event")

def get_incidents(event_id: int, participant_id: int, db) -> list[EventIncidentResponse]:
    validate_participant(event_id, participant_id, db)
    rows = db.execute(INCIDENTS_QUERY, [participant_id]).fetchall()
    return [row_to_incident_response(row) for row in rows]

def post_incident(event_id: int, participant_id: int, incident: EventIncidentCreate, db) -> EventIncidentResponse:
    validate_participant(event_id, participant_id, db)

    # validate entity exists if provided
    entity = None
    if incident.entity_id:
        entity = db.execute(
            """
            SELECT en.id, en.type, en.name, en.official_name, en.slug, en.abbreviation,
                   cn.id as country_id, cn.abbreviation as country_abbreviation, cn.name as country_name
            FROM entities en
            JOIN countries cn ON en._country_id = cn.id
            WHERE en.id = ?
            """,
            [incident.entity_id]
        ).fetchone()
        if not entity:
            raise HTTPException(status_code=404, detail="Entity not found")

    try:
        cur = db.cursor()
        cur.execute(POST_INCIDENT_QUERY, [
            participant_id,
            incident.entity_id,
            incident.incident_type,
            incident.minute
        ])
        db.commit()
        new_id = cur.lastrowid
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create incident: {e}")

    return EventIncidentResponse(
        id=new_id,
        incident_type=incident.incident_type,
        minute=incident.minute,
        entity=EntityResponse(
            id=entity["id"],
            type=entity["type"],
            name=entity["name"],
            official_name=entity["official_name"],
            slug=entity["slug"],
            abbreviation=entity["abbreviation"],
            country=CountryResponse(
                id=entity["country_id"],
                abbreviation=entity["country_abbreviation"],
                name=entity["country_name"]
            )
        ) if entity else None
    )