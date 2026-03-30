from pydantic import BaseModel
from pydantic import field_validator

from src.backend.models.entity import EntityResponse

class EventResultCreate(BaseModel):
    category: str | None = None
    outcome_type: str = "win"        # must be before entity_id
    entity_id: int | None = None    
    message: str | None = None

    @field_validator("outcome_type")
    @classmethod
    def outcome_must_be_valid(cls, v):
        if v not in ("win", "draw", "abandoned"):
            raise ValueError("outcome_type must be 'win', 'draw', or 'abandoned'")
        return v

    @field_validator("entity_id")
    @classmethod
    def entity_required_for_win(cls, v, info):
        if info.data.get("outcome_type") == "win" and v is None:
            raise ValueError("entity_id is required when outcome_type is 'win'")
        if info.data.get("outcome_type") != "win" and v is not None:
            raise ValueError("entity_id should only be set when outcome_type is 'win'")
        return v


class EventResultResponse(BaseModel):
    id: int
    category: str | None = None
    entity: EntityResponse | None = None
    outcome_type: str
    message: str | None = None