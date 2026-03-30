from fastapi import APIRouter, Depends

from src.backend.api.dependencies import get_db
from src.backend.models.stage import StageCreate, StageResponse
from src.backend.services import stage_service

router = APIRouter(prefix="/competitions/{competition_slug}/stages", tags=["stages"])


@router.get("/", response_model=list[StageResponse])
def get_stages(competition_slug: str, db=Depends(get_db)):
    return stage_service.get_stages_by_competition(competition_slug, db)


@router.get("/{stage_id}", response_model=StageResponse)
def get_stage(competition_slug: str, stage_id: int, db=Depends(get_db)):
    return stage_service.get_stage(competition_slug, stage_id, db)


@router.post("/", response_model=StageResponse, status_code=201)
def post_stage(competition_slug: str, stage: StageCreate, db=Depends(get_db)):
    return stage_service.post_stage(competition_slug, stage, db)
