from fastapi import FastAPI
from .database.core import engine, Base

app = FastAPI(title="Adamant Challenge Backend Application", version="1.0.0")

Base.metadata.create_all(bind=engine)
