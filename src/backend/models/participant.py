from pydantic import BaseModel
from src.backend.models.entity import EntityResponse
from src.backend.models.participant_score import ParticipantScoreResponse

# response model - get
class ParticipantResponse(BaseModel):
    entity: EntityResponse
    role: str
    stage_position: int | None
    score: list[ParticipantScoreResponse] | None = None
