from sqlalchemy import Boolean, Column, String

from .base_model import BaseModel


class Document(BaseModel):
    __tablename__ = "documents"

    title = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    is_processed = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Document(title='{self.title}', file_path='{self.file_path}', is_processed={self.is_processed})>"
