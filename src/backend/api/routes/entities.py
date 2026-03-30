from fastapi import APIRouter, Depends

from src.backend.api.dependencies import get_db
from src.backend.models.entity import EntityCreate, EntityResponse
from src.backend.services import entity_service

router = APIRouter(prefix="/entities", tags=["entities"])


@router.get("/", response_model=list[EntityResponse])
def get_entities(db=Depends(get_db)):
    return entity_service.get_all_entities(db)


@router.get("/{entity_id}", response_model=EntityResponse)
def get_entity(entity_id: int, db=Depends(get_db)):
    return entity_service.get_entity(entity_id, db)


@router.post("/", response_model=EntityResponse, status_code=201)
def post_entity(entity: EntityCreate, db=Depends(get_db)):
    return entity_service.post_entity(entity, db)
