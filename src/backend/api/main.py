from fastapi import FastAPI

from src.backend.api.routes import events, competitions, stages, countries, venues


app = FastAPI()
app.include_router(events.router)
app.include_router(competitions.router)
app.include_router(stages.router)
app.include_router(countries.router)
app.include_router(venues.router)