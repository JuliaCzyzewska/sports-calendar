from pydantic import BaseModel

# response model - get
class CountryCreate(BaseModel):
    abbreviation: str
    name: str
    
class CountryResponse(BaseModel):
    id: int
    abbreviation: str
    name: str