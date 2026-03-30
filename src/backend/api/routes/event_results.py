from fastapi import APIRouter, Depends
from src.backend.api.dependencies import get_db
from src.backend.models.event_result import EventResultCreate, EventResultResponse
from src.backend.services import event_result_service

router = APIRouter(
    prefix="/events/{event_id}/results",
    tags=["results"]
)

@router.get("/", response_model=list[EventResultResponse])
def get_results(event_id: int, db=Depends(get_db)):
    return event_result_service.get_results(event_id, db)

@router.post("/", response_model=EventResultResponse, status_code=201)
def post_result(event_id: int, result: EventResultCreate, db=Depends(get_db)):
    return event_result_service.post_result(event_id, result, db)