from fastapi import FastAPI
from src.backend.api.routes import events, competitions


app = FastAPI()
app.include_router(events.router)
app.include_router(competitions.router)