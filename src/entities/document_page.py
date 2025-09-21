from sqlalchemy import Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
from ..database.core import Base


class DocumentPage(Base):
    __tablename__ = "document_pages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    page_number = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
    is_processed = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<DocumentPage(page_number='{self.page_number}', content='{self.content}', is_processed={self.is_processed})>"
