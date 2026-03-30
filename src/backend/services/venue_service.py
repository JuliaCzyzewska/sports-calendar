from fastapi import HTTPException

from src.backend.models.country import CountryResponse
from src.backend.models.venue import VenueCreate, VenueResponse

VENUES_QUERY = """
    SELECT
        v.id,
        v.name,
        v.city,
        cn.id as country_id,
        cn.abbreviation as country_abbreviation,
        cn.name as country_name
    FROM venues v
    JOIN countries cn ON v._country_id = cn.id
"""

POST_VENUE_QUERY = """
    INSERT INTO venues (name, city, _country_id)
    VALUES (?, ?, ?)
"""


def row_to_venue_response(row) -> VenueResponse:
    return VenueResponse(
        id=row["id"],
        name=row["name"],
        city=row["city"],
        country=CountryResponse(
            id=row["country_id"],
            abbreviation=row["country_abbreviation"],
            name=row["country_name"],
        ),
    )


def get_all_venues(db) -> list[VenueResponse]:
    rows = db.execute(VENUES_QUERY).fetchall()
    return [row_to_venue_response(row) for row in rows]


def get_venue(venue_id: int, db) -> VenueResponse:
    row = db.execute(VENUES_QUERY + " WHERE v.id = ?", [venue_id]).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Venue not found")
    return row_to_venue_response(row)


def post_venue(venue: VenueCreate, db) -> VenueResponse:
    # validate FKs
    country = db.execute(
        "SELECT id, abbreviation, name FROM countries WHERE id = ?", [venue.country_id]
    ).fetchone()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    try:
        cur = db.cursor()
        cur.execute(POST_VENUE_QUERY, [venue.name, venue.city, venue.country_id])
        db.commit()
        new_id = cur.lastrowid
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create venue: {e}")

    return VenueResponse(
        id=new_id,
        name=venue.name,
        city=venue.city,
        country=CountryResponse(
            id=country["id"], abbreviation=country["abbreviation"], name=country["name"]
        ),
    )
