from pydantic import BaseModel

from src.backend.models.entity import EntityResponse


class EventIncidentCreate(BaseModel):
    incident_type: str
    minute: int | float | None = None
    entity_id: int | None



class EventIncidentResponse(BaseModel):
    id: int
    entity: EntityResponse | None = None     # specific athlete (if participant is a team)
    incident_type: str
    minute: int | float | None = None