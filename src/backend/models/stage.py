from pydantic import BaseModel

# response model - get
class StageResponse(BaseModel):
    name: str | None
    ordering: int | None