from fastapi import APIRouter, Depends

from src.backend.api.dependencies import get_db
from src.backend.models.venue import VenueCreate, VenueResponse
from src.backend.services import venue_service

router = APIRouter(prefix="/venues", tags=["venues"])


@router.get("/", response_model=list[VenueResponse])
def get_venues(db=Depends(get_db)):
    return venue_service.get_all_venues(db)


@router.get("/{venue_id}", response_model=VenueResponse)
def get_venue(venue_id: int, db=Depends(get_db)):
    return venue_service.get_venue(venue_id, db)


@router.post("/", response_model=VenueResponse, status_code=201)
def post_venue(venue: VenueCreate, db=Depends(get_db)):
    return venue_service.post_venue(venue, db)
