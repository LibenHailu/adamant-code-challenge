import httpx
from dependency_injector import containers, providers

from src.core.chroma_client import ChromaClient
from src.core.config import configs
from src.core.database import Database
from src.core.weather_client import WeatherApiClient
from src.repository.document_page_repository import DocumentPageRepository
from src.repository.document_repository import DocumentRepository
from src.repository.message_repository import MessageRepository
from src.services.document_service import DocumentService
from src.services.message_service import MessageService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.api.v1.endpoints.rag",
        ]
    )

    db = providers.Singleton(Database, db_url=configs.DATABASE_URI)
    chroma_client = providers.Singleton(ChromaClient)
    http_client = providers.Resource(
        httpx.AsyncClient,
        timeout=httpx.Timeout(10.0, read=20.0),
    )

    document_repository = providers.Factory(
        DocumentRepository,
        session_factory=db.provided.session,
        chroma_client=chroma_client,
    )
    document_page_repository = providers.Factory(DocumentPageRepository, session_factory=db.provided.session)
    message_repository = providers.Factory(
        MessageRepository,
        session_factory=db.provided.session,
        chroma_client=chroma_client,
    )
    weather_api_client = providers.Factory(
        WeatherApiClient,
        http_client=http_client,
    )

    document_service = providers.Factory(
        DocumentService,
        document_repository=document_repository,
        document_page_repository=document_page_repository,
    )
    message_service = providers.Factory(
        MessageService,
        message_repository=message_repository,
        weather_client=weather_api_client,
    )
