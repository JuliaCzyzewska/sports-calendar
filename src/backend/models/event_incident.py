from pydantic import BaseModel

from src.backend.models.entity import EntityResponse


# response model - get
class EventIncidentResponse(BaseModel):
    id: int
    entity: EntityResponse | None = None     # specific athlete (if participant is a team)
    incident_type: str
    minute: int | float | None = None