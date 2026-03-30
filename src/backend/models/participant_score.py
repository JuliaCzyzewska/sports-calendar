from pydantic import BaseModel


class ParticipantScoreSchema(BaseModel):
    score_value: int | float
    score_label: str
