from fastapi import APIRouter, UploadFile, status

from ..database.core import DbSession

from . import models
from . import service

router = APIRouter(tags=["RAG"])


@router.post(
    "/upload",
    response_model=models.DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_file(
    db: DbSession,
    file: UploadFile,
):
    return await service.upload_file(
        db,
        file,
    )
