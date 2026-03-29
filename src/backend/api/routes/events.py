from fastapi import APIRouter
from src.backend.services import event_service
from src.backend.api.dependencies import get_db
from fastapi import Depends

router = APIRouter(prefix="/events", tags=["events"])

@router.get("/")
def get_events(db = Depends(get_db)):
    return event_service.get_all_events(db)


@router.get("/{event_id}")
def get_event(event_id: int):
    return {}