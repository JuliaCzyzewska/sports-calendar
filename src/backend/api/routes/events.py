from fastapi import APIRouter, Depends

from src.backend.api.dependencies import get_db
from src.backend.models.event import EventCreate, EventResponse
from src.backend.services import event_service

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/", response_model=list[EventResponse])
def get_events(db=Depends(get_db)):
    return event_service.get_all_events(db)


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db=Depends(get_db)):
    return event_service.get_one_event(event_id, db)


@router.post("/", response_model=EventResponse, status_code=201)
def post_event(event: EventCreate, db=Depends(get_db)):
    return event_service.post_event(event, db)
