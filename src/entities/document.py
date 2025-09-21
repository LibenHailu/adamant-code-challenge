from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..database.core import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    is_processed = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Document(title='{self.title}', file_path='{self.file_path}', is_processed={self.is_processed})>"
