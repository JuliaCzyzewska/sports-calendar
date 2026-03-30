from pydantic import BaseModel


# response model - get
class ParticipantScoreResponse(BaseModel):
    score_value: int | float
    score_label: str
