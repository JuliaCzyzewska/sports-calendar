from pydantic import BaseModel

from src.backend.models.country import CountryResponse


class VenueCreate(BaseModel):
    name: str
    city: str | None
    country_id: int


# response model - get
class VenueResponse(BaseModel):
    id: int
    name: str
    city: str | None
    country: CountryResponse
