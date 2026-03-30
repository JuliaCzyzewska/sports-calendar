from fastapi import HTTPException
from src.backend.models.event_result import EventResultCreate, EventResultResponse
from src.backend.models.entity import EntityResponse
from src.backend.models.country import CountryResponse
from src.backend.services.shared_queries import fetch_results_by_event


POST_RESULT_QUERY = """
    INSERT INTO event_results (_event_id, category, _entity_id, outcome_type, message)
    VALUES (?, ?, ?, ?, ?)
"""

def validate_event_exists(event_id: int, db):
    event = db.execute(
        "SELECT id FROM events WHERE id = ?", [event_id]
    ).fetchone()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

def validate_event_can_add_results(event_id: int, db):
    event = db.execute(
        "SELECT id, status FROM events WHERE id = ?", [event_id]
    ).fetchone()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event["status"] == "cancelled":
        raise HTTPException(status_code=409, detail="Cannot add results to a cancelled event")


def get_results(event_id: int, db) -> list[EventResultResponse]:
    validate_event_exists(event_id, db)
    results_by_event = fetch_results_by_event(db, [event_id])
    return results_by_event.get(event_id, [])


def post_result(event_id: int, result: EventResultCreate, db) -> EventResultResponse:
    validate_event_can_add_results(event_id, db)

    # validate entity exists if provided and fetch for response
    entity = None
    if result.entity_id:
        entity = db.execute(
            """
            SELECT en.id, en.type, en.name, en.official_name, en.slug, en.abbreviation,
                   cn.id as country_id, cn.abbreviation as country_abbreviation, cn.name as country_name
            FROM entities en
            JOIN countries cn ON en._country_id = cn.id
            WHERE en.id = ?
            """,
            [result.entity_id]
        ).fetchone()
        if not entity:
            raise HTTPException(status_code=404, detail="Entity not found")

    # enforce unique (event_id, category) — one result per category per event
    existing = db.execute(
        "SELECT id FROM event_results WHERE _event_id = ? AND category IS ?",
        [event_id, result.category]
    ).fetchone()
    if existing:
        detail = f"Result for category '{result.category}' already exists for this event" if result.category else "Result already exists for this event"
        raise HTTPException(status_code=409, detail=detail)

    try:
        cur = db.cursor()
        cur.execute(POST_RESULT_QUERY, [
            event_id,
            result.category,
            result.entity_id,
            result.outcome_type,
            result.message
        ])
        db.commit()
        new_id = cur.lastrowid
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create result: {e}")

    return EventResultResponse(
        id=new_id,
        category=result.category,
        outcome_type=result.outcome_type,
        message=result.message,
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