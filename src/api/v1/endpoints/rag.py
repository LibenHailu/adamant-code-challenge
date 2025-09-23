from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends, UploadFile, status

from src.core.container import Container
from src.core.middleware import inject
from src.schema.document_schema import DocumentResponse
from src.schema.message_schema import MessageCreate, MessageResponse
from src.services.document_service import DocumentService
from src.services.message_service import MessageService

router = APIRouter()

@router.post("/documents", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
@inject
async def upload_document(
    file: UploadFile,
    service: DocumentService = Depends(Provide[Container.document_service]),
):
    return await service.create(file)


@router.post("/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
@inject
async def message_handler(
    message: MessageCreate,
    service: MessageService = Depends(Provide[Container.message_service]),
):
    return await service.create(message)
