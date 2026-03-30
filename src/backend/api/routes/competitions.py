from fastapi import APIRouter
from src.backend.services import competition_service
from src.backend.api.dependencies import get_db
from fastapi import Depends
from src.backend.models.competition import CompetitionSchema

router = APIRouter(prefix="/competitions", tags=["competitions"])

@router.get("/", response_model=list[CompetitionSchema])
def get_competitions(db = Depends(get_db)):
    return competition_service.get_all_competitions(db)

@router.get("/{competition_slug}", response_model=CompetitionSchema)
def get_competition(competition_slug: str, db = Depends(get_db)):
    return competition_service.get_competition_by_slug(competition_slug, db)

@router.post("/", response_model=CompetitionSchema, status_code=201)
def post_competition(competition: CompetitionSchema, db = Depends(get_db)):
    return competition_service.post_competition(competition, db)

