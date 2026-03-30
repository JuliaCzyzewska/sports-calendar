from fastapi import HTTPException

from src.backend.models.country import CountryResponse
from src.backend.models.entity import EntityResponse
from src.backend.models.participant import ParticipantCreate, ParticipantResponse
from src.backend.services.shared_queries import (
    PARTICIPANTS_QUERY,
    fetch_participant_scores,
    fetch_participants_event_incidents,
    row_to_participant_response,
)

POST_PARTICIPANT_QUERY = """
    INSERT INTO participants (_event_id, _entity_id, role, stage_position)
    VALUES (?, ?, ?, ?)
"""


def get_participants(event_id: int, db) -> list[ParticipantResponse]:
    rows = db.execute(
        PARTICIPANTS_QUERY.format(placeholders="?"), [event_id]
    ).fetchall()
    if not rows:
        return []

    scores_by_participant = fetch_participant_scores(db, rows)
    incidents_by_participant = fetch_participants_event_incidents(db, rows)

    return [
        row_to_participant_response(
            row,
            scores=scores_by_participant[row["participant_id"]],
            incidents=incidents_by_participant[row["participant_id"]],
        )
        for row in rows
    ]


def get_participant(event_id: int, participant_id: int, db) -> ParticipantResponse:
    row = db.execute(
        PARTICIPANTS_QUERY.format(placeholders="?") + " AND p.id = ?",
        [event_id, participant_id],
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Participant not found")

    scores_by_participant = fetch_participant_scores(db, [row])
    incidents_by_participant = fetch_participants_event_incidents(db, [row])

    return row_to_participant_response(
        row,
        scores=scores_by_participant[row["participant_id"]],
        incidents=incidents_by_participant[row["participant_id"]],
    )


def post_participant(
    event_id: int, participant: ParticipantCreate, db
) -> ParticipantResponse:
    # validate FKs
    event = db.execute("SELECT id FROM events WHERE id = ?", [event_id]).fetchone()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    entity = db.execute(
        """
        SELECT en.id, en.type, en.name, en.official_name, en.slug, en.abbreviation,
               cn.id as country_id, cn.abbreviation as country_abbreviation, cn.name as country_name
        FROM entities en
        JOIN countries cn ON en._country_id = cn.id
        WHERE en.id = ?
        """,
        [participant.entity_id],
    ).fetchone()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    # validate entity not already in this event
    existing = db.execute(
        "SELECT id FROM participants WHERE _event_id = ? AND _entity_id = ?",
        [event_id, participant.entity_id],
    ).fetchone()
    if existing:
        raise HTTPException(
            status_code=409, detail="Entity already participating in this event"
        )

    try:
        cur = db.cursor()
        cur.execute(
            POST_PARTICIPANT_QUERY,
            [
                event_id,
                participant.entity_id,
                participant.role,
                participant.stage_position,
            ],
        )
        db.commit()
        new_id = cur.lastrowid
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Failed to create participant: {e}"
        )

    return ParticipantResponse(
        id=new_id,
        role=participant.role,
        stage_position=participant.stage_position,
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
                name=entity["country_name"],
            ),
        ),
    )
