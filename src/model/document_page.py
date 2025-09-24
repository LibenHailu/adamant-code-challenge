from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from .base_model import BaseModel


class DocumentPage(BaseModel):
    __tablename__ = "document_pages"

    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    page_number = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
    is_processed = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<DocumentPage(page_number='{self.page_number}',content='{self.content[:30]}...', is_processed={self.is_processed})>"
