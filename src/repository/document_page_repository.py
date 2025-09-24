from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from src.model.document_page import DocumentPage
from src.repository.base_repository import BaseRepository


class DocumentPageRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, DocumentPage)
