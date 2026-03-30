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

PARTICIPANTS_QUERY = """
    SELECT 
        p.id as participant_id,
        p._event_id as event_id, 
        p.role, 
        p.stage_position,
        en.id as entity_id,
        en.name as entity_name,
        en.type as entity_type, 
        en.official_name as entity_official_name, 
        en.slug as entity_slug,
        en.abbreviation as entity_abbreviation,
        cn.id as country_id,
        cn.abbreviation as country_abbreviation, 
        cn.name as country_name
    FROM participants p
    JOIN entities en ON p._entity_id = en.id
    JOIN countries cn ON en._country_id = cn.id
    WHERE p._event_id IN ({placeholders})      
"""


SCORES_QUERY = """
    SELECT
        ps._participant_id as participant_id,
        ps.score_value,
        ps.score_label
    FROM participant_scores ps
    WHERE ps._participant_id IN ({placeholders})
"""

EVENT_INCIDENTS_QUERY = """
    SELECT
        ei.id as event_incident_id,
        ei._participant_id as participant_id,
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
    WHERE ei._participant_id IN ({placeholders})
"""

def fetch_participant_scores(db, participant_rows) -> dict[int, list[ParticipantScoreSchema]]:
    if not participant_rows:
        return {}

    # fetch all scores for all participants
    participant_ids = [row["participant_id"] for row in participant_rows]
    placeholders = ",".join("?" * len(participant_ids))
    score_rows = db.execute(
        SCORES_QUERY.format(placeholders=placeholders),
        participant_ids
    ).fetchall()

    # group scores by participant_id
    scores_by_participant = defaultdict(list)
    for row in score_rows:
        scores_by_participant[row["participant_id"]].append(
            ParticipantScoreSchema(
                score_value=row["score_value"],
                score_label=row["score_label"]
            )
        )
    return scores_by_participant


def fetch_participants_event_incidents(db, participant_rows) -> dict[int, list[EventIncidentResponse]]:
    if not participant_rows:
        return {}

    # fetch all incidents for all participants
    participant_ids = [row["participant_id"] for row in participant_rows]
    placeholders = ",".join("?" * len(participant_ids))
    incident_rows = db.execute(
        EVENT_INCIDENTS_QUERY.format(placeholders=placeholders),
        participant_ids
    ).fetchall()

    # group incidents by participant_id
    incidents_by_participant = defaultdict(list)
    for row in incident_rows:
        incidents_by_participant[row["participant_id"]].append(
            EventIncidentResponse(
                id=row["event_incident_id"],
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
                ) if row["entity_id"] else None,
                incident_type=row["incident_type"],
                minute=row["minute"]
            )
        )
    return incidents_by_participant


def row_to_participant_response(row, scores=None, incidents=None) -> ParticipantResponse:
    return ParticipantResponse(
        id=row["participant_id"],
        role=row["role"],
        stage_position=row["stage_position"],
        score=scores or None,
        incidents=incidents or None,
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
        )
    )


def fetch_participants_by_event(db, event_ids: list[int]) -> dict[int, list[ParticipantResponse]]:
    placeholders = ",".join("?" * len(event_ids))
    participant_rows = db.execute(
        PARTICIPANTS_QUERY.format(placeholders=placeholders),
        event_ids
    ).fetchall()

    if not participant_rows:
        return {}

    scores_by_participant = fetch_participant_scores(db, participant_rows)
    incidents_by_participant = fetch_participants_event_incidents(db, participant_rows)

    participants_by_event = defaultdict(list)
    for row in participant_rows:
        participants_by_event[row["event_id"]].append(
            row_to_participant_response(
                row,
                scores=scores_by_participant[row["participant_id"]],
                incidents=incidents_by_participant[row["participant_id"]]
            )
        )
    return participants_by_event