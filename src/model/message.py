from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime
from .base_model import BaseModel


class Message(BaseModel):
    __tablename__ = "messages"

    content = Column(String, nullable=False)
    is_ai = Column(Boolean, default=False, nullable=False)
    timestamp = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self):
        return f"<Message(content='{self.content[:30]}',is_ai={self.is_ai}, timestamp={self.timestamp})>"
