from fastapi import APIRouter, Depends

from src.backend.api.dependencies import get_db
from src.backend.models.participant import ParticipantCreate, ParticipantResponse
from src.backend.services import participant_service

router = APIRouter(prefix="/events/{event_id}/participants", tags=["participants"])


@router.get("/", response_model=list[ParticipantResponse])
def get_participants(event_id: int, db=Depends(get_db)):
    return participant_service.get_participants(event_id, db)


@router.get("/{participant_id}", response_model=ParticipantResponse)
def get_participant(event_id: int, participant_id: int, db=Depends(get_db)):
    return participant_service.get_participant(event_id, participant_id, db)


@router.post("/", response_model=ParticipantResponse, status_code=201)
def post_participant(event_id: int, participant: ParticipantCreate, db=Depends(get_db)):
    return participant_service.post_participant(event_id, participant, db)
