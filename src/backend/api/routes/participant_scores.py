from fastapi import APIRouter, Depends

from src.backend.api.dependencies import get_db
from src.backend.models.participant_score import ParticipantScoreSchema
from src.backend.services import participant_score_service

router = APIRouter(
    prefix="/events/{event_id}/participants/{participant_id}/scores", tags=["scores"]
)


@router.get("/", response_model=list[ParticipantScoreSchema])
def get_scores(event_id: int, participant_id: int, db=Depends(get_db)):
    return participant_score_service.get_scores(event_id, participant_id, db)


@router.post("/", response_model=ParticipantScoreSchema, status_code=201)
def post_score(
    event_id: int,
    participant_id: int,
    score: ParticipantScoreSchema,
    db=Depends(get_db),
):
    return participant_score_service.post_score(event_id, participant_id, score, db)
