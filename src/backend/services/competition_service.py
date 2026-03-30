from fastapi import HTTPException
from src.backend.models.competition import CompetitionSchema


COMPETITION_QUERY = """
    SELECT slug, name, sport_type, participation_type
    FROM competitions
"""
POST_COMPETITION_QUERY = """
    INSERT INTO competitions (
        slug,
        name,
        sport_type,
        participation_type
    ) VALUES (?, ?, ?, ?)
"""

def row_to_competition_response(row):
    return CompetitionSchema(
        slug=row["slug"],
        name=row["name"],
        sport_type=row["sport_type"],
        participation_type=row["participation_type"]
    )


def get_all_competitions(db) -> list[CompetitionSchema]:
    cur = db.cursor()
    results = cur.execute(COMPETITION_QUERY).fetchall()
    if not results:
        return []
    return [row_to_competition_response(row) for row in results]


def get_competition_by_slug(competition_slug: str, db) -> CompetitionSchema:
    cur = db.cursor()
    result = cur.execute(COMPETITION_QUERY + " WHERE slug = ?", [competition_slug]).fetchone()
    if not result:
            raise HTTPException(status_code=404, detail="Competition not found")
    return row_to_competition_response(result)


def post_competition(competition: CompetitionSchema, db) -> CompetitionSchema:
    cur = db.cursor()
    try:
            cur.execute(POST_COMPETITION_QUERY, [
                competition.slug,
                competition.name,
                competition.sport_type,
                competition.participation_type
            ])
            db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(500, detail=f"Failed to create event: {e}")

    return competition