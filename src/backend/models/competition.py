from pydantic import BaseModel


class CompetitionSchema(BaseModel):
    slug: str
    name: str
    sport_type: str
    participation_type: str

