from pydantic import BaseModel, Field

# request model- create, udpate
class EventCreate(BaseModel):
    status: str = Field(default="scheduled")
    season: int
    date_venue: str | None
    time_venue_utc: str | None
    stage_id: int | None
    venue_id: int | None
    competition_slug: str


# response model - get
class EventResponse(BaseModel):
    status: str
    season: int
    date_venue: str | None
    time_venue_utc: str | None
    stage_id: int | None
    venue_id: int | None
    competition_slug: str