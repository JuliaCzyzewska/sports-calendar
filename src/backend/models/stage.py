from pydantic import BaseModel

# response model - get
class StageResponse(BaseModel):
    id: int
    name: str | None
    ordering: int | None