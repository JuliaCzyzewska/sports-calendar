from pydantic import BaseModel, Field
from src.backend.models.competition import CompetitionResponse
from src.backend.models.stage import StageResponse
from src.backend.models.venue import VenueResponse
from src.backend.models.participant import ParticipantResponse

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
    stage: StageResponse | None
    venue: VenueResponse | None
    competition: CompetitionResponse
    participants: list[ParticipantResponse]