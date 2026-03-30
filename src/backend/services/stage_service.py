from fastapi import HTTPException

from src.backend.models.stage import StageCreate, StageResponse

STAGES_QUERY = """
    SELECT id, name, ordering
    FROM stages
    WHERE _competition_slug = ?
"""

POST_STAGE_QUERY = """
    INSERT INTO stages (_competition_slug, name, ordering)
    VALUES (?, ?, ?)
"""


def get_stages_by_competition(competition_slug: str, db) -> list[StageResponse]:
    rows = db.execute(STAGES_QUERY, [competition_slug]).fetchall()
    return [
        StageResponse(id=row["id"], name=row["name"], ordering=row["ordering"])
        for row in rows
    ]


def get_stage(competition_slug: str, stage_id: int, db) -> StageResponse:
    row = db.execute(
        STAGES_QUERY + " AND id = ?", [competition_slug, stage_id]
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Stage not found")
    return StageResponse(id=row["id"], name=row["name"], ordering=row["ordering"])


def post_stage(competition_slug: str, stage: StageCreate, db) -> StageResponse:
    # validate FKs
    competition = db.execute(
        "SELECT slug FROM competitions WHERE slug = ?", [competition_slug]
    ).fetchone()
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")

    try:
        cur = db.cursor()
        cur.execute(POST_STAGE_QUERY, [competition_slug, stage.name, stage.ordering])
        db.commit()
        new_id = cur.lastrowid
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create stage: {e}")

    return StageResponse(id=new_id, name=stage.name, ordering=stage.ordering)
