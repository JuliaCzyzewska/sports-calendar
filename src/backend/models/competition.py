from pydantic import BaseModel

# response model - get
class CompetitionResponse(BaseModel):
    slug: str
    name: str
    sport_type: str
    participation_type: str
