from pydantic import BaseModel
from src.backend.models.country import CountryResponse

# response model - get
class VenueResponse(BaseModel):
    name: str
    city: str | None
    country: CountryResponse