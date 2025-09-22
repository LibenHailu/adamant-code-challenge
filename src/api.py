from fastapi import FastAPI
from src.rag.controller import router as rag_router

def register_routes(app: FastAPI):
    app.include_router(rag_router)