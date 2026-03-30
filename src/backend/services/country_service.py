from fastapi import HTTPException
from src.backend.models.country import CountryCreate, CountryResponse

COUNTRIES_QUERY = """
    SELECT id, abbreviation, name
    FROM countries
"""

POST_COUNTRY_QUERY = """
    INSERT INTO countries (abbreviation, name)
    VALUES (?, ?)
"""

def get_all_countries(db) -> list[CountryResponse]:
    rows = db.execute(COUNTRIES_QUERY).fetchall()
    return [
        CountryResponse(id=row["id"], abbreviation=row["abbreviation"], name=row["name"])
        for row in rows
    ]

def get_country(country_id: int, db) -> CountryResponse:
    row = db.execute(
        COUNTRIES_QUERY + " WHERE id = ?", [country_id]
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Country not found")
    return CountryResponse(id=row["id"], abbreviation=row["abbreviation"], name=row["name"])

def post_country(country: CountryCreate, db) -> CountryResponse:
    # check abbreviation not already taken
    existing = db.execute(
        "SELECT id FROM countries WHERE abbreviation = ?", [country.abbreviation]
    ).fetchone()
    if existing:
        raise HTTPException(status_code=409, detail="Country with this abbreviation already exists")

    try:
        cur = db.cursor()
        cur.execute(POST_COUNTRY_QUERY, [country.abbreviation, country.name])
        db.commit()
        new_id = cur.lastrowid
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create country: {e}")

    return CountryResponse(id=new_id, abbreviation=country.abbreviation, name=country.name)