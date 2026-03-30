from pydantic import BaseModel
from src.backend.models.entity import EntityResponse
from src.backend.models.participant_score import ParticipantScoreResponse
from src.backend.models.event_incident import EventIncidentResponse

# response model - get
class ParticipantResponse(BaseModel):
    entity: EntityResponse
    role: str
    stage_position: int | None
    score: list[ParticipantScoreResponse] | None = None
    incidents: list[EventIncidentResponse] | None = None
