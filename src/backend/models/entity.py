from pydantic import BaseModel

from src.backend.models.country import CountryResponse

# response model - get
class EntityResponse(BaseModel):
    type: str
    name: str
    official_name: str
    slug: str
    abbreviation: str | None
    country: CountryResponse