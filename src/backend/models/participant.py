from pydantic import BaseModel, field_validator

from src.backend.models.entity import EntityResponse
from src.backend.models.event_incident import EventIncidentResponse
from src.backend.models.participant_score import ParticipantScoreSchema


class ParticipantCreate(BaseModel):
    entity_id: int
    role: str = "entry"
    stage_position: int | None

    @field_validator("role")
    @classmethod
    def role_must_be_valid(cls, v):
        if v not in ("home", "away", "entry"):
            raise ValueError("role must be 'home', 'away' or 'entry'")
        return v


# response model - get
class ParticipantResponse(BaseModel):
    id: int
    entity: EntityResponse
    role: str
    stage_position: int | None
    score: list[ParticipantScoreSchema] | None = None
    incidents: list[EventIncidentResponse] | None = None
