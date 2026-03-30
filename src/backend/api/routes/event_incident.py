from fastapi import APIRouter, Depends

from src.backend.api.dependencies import get_db
from src.backend.models.event_incident import EventIncidentCreate, EventIncidentResponse
from src.backend.services import event_incident_service

router = APIRouter(
    prefix="/events/{event_id}/participants/{participant_id}/event_incidents",
    tags=["event_incidents"],
)


@router.get("/", response_model=list[EventIncidentResponse])
def get_event_incidents(event_id: int, participant_id: int, db=Depends(get_db)):
    return event_incident_service.get_incidents(event_id, participant_id, db)


@router.post("/", response_model=EventIncidentResponse, status_code=201)
def post_event_incidents(
    event_id: int,
    participant_id: int,
    event_incident: EventIncidentCreate,
    db=Depends(get_db),
):
    return event_incident_service.post_incident(
        event_id, participant_id, event_incident, db
    )
