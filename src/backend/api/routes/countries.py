from fastapi import APIRouter, Depends

from src.backend.api.dependencies import get_db
from src.backend.models.country import CountryCreate, CountryResponse
from src.backend.services import country_service

router = APIRouter(prefix="/countries", tags=["countries"])


@router.get("/", response_model=list[CountryResponse])
def get_countries(db=Depends(get_db)):
    return country_service.get_all_countries(db)


@router.get("/{country_id}", response_model=CountryResponse)
def get_country(country_id: int, db=Depends(get_db)):
    return country_service.get_country(country_id, db)


@router.post("/", response_model=CountryResponse, status_code=201)
def post_country(country: CountryCreate, db=Depends(get_db)):
    return country_service.post_country(country, db)
