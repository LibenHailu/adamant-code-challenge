from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class DocumentBase(BaseModel):
    title: str
    file_path: str
    is_processed: Optional[bool] = False


class DocumentCreate(DocumentBase):
    pass


class DocumentResponse(DocumentBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
