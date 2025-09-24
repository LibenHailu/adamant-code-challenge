import pytest

from src.core.config import configs

if configs.ENV not in ["test"]:
    msg = f"ENV is not test, it is {configs.ENV}"
    pytest.exit(msg)

from fastapi.testclient import TestClient
from loguru import logger
from sqlmodel import SQLModel, create_engine

from src.core.config import configs
from src.core.container import Container
from src.main import AppCreator


def reset_db():
    engine = create_engine(configs.DATABASE_URI)
    logger.info(f"Resetting DB: {configs.DB}")

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    return engine


@pytest.fixture
def client():
    reset_db()
    app_creator = AppCreator()
    app = app_creator.app
    with TestClient(app) as client:
        yield client


@pytest.fixture
def container():
    return Container()
