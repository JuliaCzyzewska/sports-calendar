from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.backend.api.routes import (
    competitions,
    countries,
    entities,
    event_incident,
    event_results,
    events,
    participant_scores,
    participants,
    stages,
    venues,
)

app = FastAPI()
app.include_router(events.router)
app.include_router(competitions.router)
app.include_router(stages.router)
app.include_router(countries.router)
app.include_router(venues.router)
app.include_router(entities.router)
app.include_router(participants.router)
app.include_router(participant_scores.router)
app.include_router(event_incident.router)
app.include_router(event_results.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)