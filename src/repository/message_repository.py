from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from src.core.chroma_client import ChromaClient
from src.model.message import Message
from src.repository.base_repository import BaseRepository


class MessageRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], chroma_client: ChromaClient,):
        self.session_factory = session_factory
        self.chroma_client = chroma_client
        super().__init__(session_factory, Message)
    
    def get_by_query(self, query: str,  k: int):
        return self.chroma_client.vectorstore.similarity_search(query, k=k)
        