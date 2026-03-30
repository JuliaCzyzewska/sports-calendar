from fastapi import HTTPException

from src.backend.models.participant_score import ParticipantScoreSchema

SCORES_QUERY = """
    SELECT score_value, score_label
    FROM participant_scores
    WHERE _participant_id = ?
"""

POST_SCORE_QUERY = """
    INSERT INTO participant_scores (_participant_id, score_value, score_label)
    VALUES (?, ?, ?)
"""


def get_scores(event_id: int, participant_id: int, db) -> list[ParticipantScoreSchema]:
    participant = db.execute(
        "SELECT id FROM participants WHERE id = ? AND _event_id = ?",
        [participant_id, event_id],
    ).fetchone()
    if not participant:
        raise HTTPException(
            status_code=404, detail="Participant not found for this event"
        )

    rows = db.execute(SCORES_QUERY, [participant_id]).fetchall()
    return [
        ParticipantScoreSchema(
            score_value=row["score_value"], score_label=row["score_label"]
        )
        for row in rows
    ]


def post_score(
    event_id: int, participant_id: int, score: ParticipantScoreSchema, db
) -> ParticipantScoreSchema:
    # validate FKs
    participant = db.execute(
        "SELECT id FROM participants WHERE id = ? AND _event_id = ?",
        [participant_id, event_id],
    ).fetchone()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")

    # validate score_label not already used for this participant
    existing = db.execute(
        "SELECT score_label FROM participant_scores WHERE _participant_id = ? AND score_label = ?",
        [participant_id, score.score_label],
    ).fetchone()
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Score '{score.score_label}' already exists for this participant",
        )

    try:
        db.execute(
            POST_SCORE_QUERY, [participant_id, score.score_value, score.score_label]
        )
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create score: {e}")

    return ParticipantScoreSchema(
        score_value=score.score_value, score_label=score.score_label
    )
