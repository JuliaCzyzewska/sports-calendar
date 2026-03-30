from pydantic import BaseModel

class StageCreate(BaseModel):
    name: str
    ordering: int



# response model - get
class StageResponse(BaseModel):
    id: int
    name: str | None
    ordering: int | None