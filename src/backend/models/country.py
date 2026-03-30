from pydantic import BaseModel

# response model - get
class CountryResponse(BaseModel):
    id: int
    abbreviation: str
    name: str