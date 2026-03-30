from pydantic import BaseModel
from src.backend.models.competition import CompetitionResponse

# response model - get
class StageResponse(BaseModel):
    name: str | None
    ordering: int | None