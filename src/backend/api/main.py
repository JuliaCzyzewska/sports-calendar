from fastapi import FastAPI

from src.backend.api.routes import (
    events, competitions, stages, 
    countries, venues, entities, participants, 
    participant_scores, event_incident, event_results
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