from pydantic import BaseModel, field_validator

from src.backend.models.country import CountryResponse


class EntityCreate(BaseModel):
    type: str
    name: str
    official_name: str
    slug: str
    abbreviation: str | None
    country_id: int

    @field_validator("type")
    @classmethod
    def type_must_be_valid(cls, v):
        if v not in ("team", "athlete"):
            raise ValueError("type must be 'team' or 'athlete'")
        return v

    @field_validator("abbreviation")
    @classmethod
    def abbreviation_only_for_team(cls, v, info):
        if info.data.get("type") == "athlete" and v is not None:
            raise ValueError("abbreviation should only be set for teams")
        return v


class EntityResponse(BaseModel):
    id: int
    type: str
    name: str
    official_name: str
    slug: str
    abbreviation: str | None
    country: CountryResponse
