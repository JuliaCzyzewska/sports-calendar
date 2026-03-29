from fastapi import APIRouter
from src.backend.services import event_service
from src.backend.api.dependencies import get_db
from fastapi import Depends
from src.backend.models.event import EventResponse


router = APIRouter(prefix="/events", tags=["events"])

@router.get("/")
def get_all_events(db = Depends(get_db)) -> list[EventResponse]:
    return event_service.get_all_events(db)


@router.get("/{event_id}")
def get_event(event_id: int):
    return {}