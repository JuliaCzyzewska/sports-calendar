from pydantic import BaseModel, Field
from datetime import date, time

from src.backend.models.competition import CompetitionSchema
from src.backend.models.stage import StageResponse
from src.backend.models.venue import VenueResponse
from src.backend.models.participant import ParticipantResponse
from src.backend.models.event_result import EventResultResponse


# request model- post
class EventCreate(BaseModel):
    status: str = Field(default="scheduled")
    season: int
    date_venue: date | None
    time_venue_utc: time | None
    stage_id: int | None
    venue_id: int | None
    competition_slug: str




# response model - get
class EventResponse(BaseModel):
    id: int
    status: str
    season: int
    date_venue: date | None
    time_venue_utc: time | None
    stage: StageResponse | None
    venue: VenueResponse | None
    competition: CompetitionSchema
    participants: list[ParticipantResponse] | None
    results: list[EventResultResponse] | None