from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends, UploadFile

from src.core.container import Container
from src.core.middleware import inject
from src.schema.document_schema import DocumentResponse
from src.services.document_service import DocumentService

router = APIRouter(tags=["RAG"])


@router.post("/upload", response_model=DocumentResponse, status_code=201)
@inject
async def upload_document(
    file: UploadFile,
    service: DocumentService = Depends(Provide[Container.document_service]),
):
    return await service.create(file)
