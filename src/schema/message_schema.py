from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class MessageBase(BaseModel):
    content: str
    is_ai: Optional[bool] = False


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)

class MessageCategory(BaseModel):
    category: str = Field(description="Message category: 'Food', 'Weather', or 'NONE'")