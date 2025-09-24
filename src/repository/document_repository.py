from contextlib import AbstractContextManager
from typing import Callable, List

from sqlalchemy.orm import Session

from src.core.chroma_client import ChromaClient
from src.model.document import Document
from src.model.document_page import DocumentPage
from src.repository.base_repository import BaseRepository
from src.schema.document_schema import DocumentCreate


class DocumentRepository(BaseRepository):
    def __init__(
        self,
        session_factory: Callable[..., AbstractContextManager[Session]],
        chroma_client: ChromaClient,
    ):
        self.session_factory = session_factory
        self.chroma_client = chroma_client
        super().__init__(session_factory, Document)

    def create_with_pages(self, schema: DocumentCreate, pages: List[any]):
        with self.session_factory() as session:
            schema.is_processed = True
            document = self.model(**schema.model_dump())
            session.add(document)
            session.flush()

            for index, page in enumerate(pages):
                page_data = DocumentPage(
                    document_id=document.id,
                    page_number=index + 1,
                    content=page.page_content,
                    is_processed=True,
                )
                session.add(page_data)

            session.commit()
            session.refresh(document)

            # Prepare documents for ChromaDB
            documents_to_index = []
            metadatas = []
            ids = []

            for page_num, page in enumerate(pages):
                page_chunks = self.chroma_client.text_splitter.split_text(page.page_content)

                for chunk_num, chunk in enumerate(page_chunks):
                    documents_to_index.append(chunk)
                    metadatas.append(
                        {
                            "document_id": str(document.id),
                            "page_number": page_num + 1,
                            "chunk_number": chunk_num + 1,
                            "document_title": document.title,
                        }
                    )
                    ids.append(f"doc_{document.id}_page_{page_num+1}_chunk_{chunk_num+1}")

            if documents_to_index:
                self.chroma_client.vectorstore.add_texts(
                    texts=documents_to_index,
                    metadatas=metadatas,
                    ids=ids,
                )

            return document
