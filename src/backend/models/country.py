from pydantic import BaseModel

# response model - get
class CountryResponse(BaseModel):
    abbreviation: str
    name: str