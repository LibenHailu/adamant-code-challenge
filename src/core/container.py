from dependency_injector import containers, providers

from src.core.config import configs
from src.core.database import Database
from src.repository.document_repository import DocumentRepository
from src.repository.document_page_repository import DocumentPageRepository
from src.services.document_service import DocumentService
from src.core.chroma_client import ChromaClient


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.api.v1.endpoints.rag",
        ]
    )

    db = providers.Singleton(Database, db_url=configs.DATABASE_URI)
    chroma_client = providers.Singleton(ChromaClient) 
    
    document_repository = providers.Factory(DocumentRepository, session_factory=db.provided.session, chroma_client=chroma_client) 
    document_page_repository = providers.Factory(DocumentPageRepository, session_factory=db.provided.session)   

    document_service = providers.Factory(DocumentService, document_repository=document_repository, document_page_repository=document_page_repository)