from fastapi import FastAPI
from sqlalchemy import Engine

from .database.core import Base, engine

from .api import register_routes

app = FastAPI(
    title="Adamant Challenge Backend Application",
    description="This is created as part of the process for a backend API take-home assignment.",
    version="1.0.0",
)

#Base.metadata.create_all(bind=engine)

register_routes(app)