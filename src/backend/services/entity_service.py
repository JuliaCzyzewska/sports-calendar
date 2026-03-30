from fastapi import HTTPException
from src.backend.models.entity import EntityCreate, EntityResponse
from src.backend.models.country import CountryResponse

ENTITIES_QUERY = """
    SELECT
        en.id,
        en.type,
        en.name,
        en.official_name,
        en.slug,
        en.abbreviation,
        cn.id as country_id,
        cn.abbreviation as country_abbreviation,
        cn.name as country_name
    FROM entities en
    JOIN countries cn ON en._country_id = cn.id
"""

POST_ENTITY_QUERY = """
    INSERT INTO entities (type, name, official_name, slug, abbreviation, _country_id)
    VALUES (?, ?, ?, ?, ?, ?)
"""

def row_to_entity_response(row) -> EntityResponse:
    return EntityResponse(
        id=row["id"],
        type=row["type"],
        name=row["name"],
        official_name=row["official_name"],
        slug=row["slug"],
        abbreviation=row["abbreviation"],
        country=CountryResponse(
            id=row["country_id"],
            abbreviation=row["country_abbreviation"],
            name=row["country_name"]
        )
    )

def get_all_entities(db) -> list[EntityResponse]:
    rows = db.execute(ENTITIES_QUERY).fetchall()
    return [row_to_entity_response(row) for row in rows]

def get_entity(entity_id: int, db) -> EntityResponse:
    row = db.execute(
        ENTITIES_QUERY + " WHERE en.id = ?", [entity_id]
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Entity not found")
    return row_to_entity_response(row)

def post_entity(entity: EntityCreate, db) -> EntityResponse:
    # validate FKs
    country = db.execute(
        "SELECT id, abbreviation, name FROM countries WHERE id = ?", [entity.country_id]
    ).fetchone()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    # validate slug is unique
    existing = db.execute(
        "SELECT id FROM entities WHERE slug = ?", [entity.slug]
    ).fetchone()
    if existing:
        raise HTTPException(status_code=409, detail="Entity with this slug already exists")

    try:
        cur = db.cursor()
        cur.execute(POST_ENTITY_QUERY, [
            entity.type,
            entity.name,
            entity.official_name,
            entity.slug,
            entity.abbreviation,
            entity.country_id
        ])
        db.commit()
        new_id = cur.lastrowid
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create entity: {e}")

    return EntityResponse(
        id=new_id,
        type=entity.type,
        name=entity.name,
        official_name=entity.official_name,
        slug=entity.slug,
        abbreviation=entity.abbreviation,
        country=CountryResponse(
            id=country["id"],
            abbreviation=country["abbreviation"],
            name=country["name"]
        )
    )