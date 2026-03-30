from pydantic import BaseModel
from src.backend.models.entity import EntityResponse


# response model - get
class ParticipantResponse(BaseModel):
    entity: EntityResponse
    role: str
    stage_position: int | None
