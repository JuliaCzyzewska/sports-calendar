from pydantic import BaseModel

from src.backend.models.entity import EntityResponse


# response model - get
class EventResultResponse(BaseModel):
    category: str | None = None
    entity: EntityResponse | None = None
    outcome_type: str
    message: str | None = None