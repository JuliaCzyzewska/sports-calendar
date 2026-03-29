from fastapi import FastAPI
from src.backend.api.routes import events


app = FastAPI()
app.include_router(events.router)
