from fastapi import FastAPI
from src.backend.api.routes import events, competitions, stages


app = FastAPI()
app.include_router(events.router)
app.include_router(competitions.router)
app.include_router(stages.router)