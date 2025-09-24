import os
from fastapi import UploadFile
from loguru import logger
from src.repository.document_page_repository import DocumentPageRepository
from src.repository.document_repository import DocumentRepository
from src.schema.document_schema import DocumentCreate
from src.services.base_service import BaseService
from src.core.exceptions import ValidationError, InternalServerError
from src.utils.file_location import get_random_file_location
from langchain_community.document_loaders import PyPDFLoader



class DocumentService(BaseService):
    def __init__(self, document_repository: DocumentRepository, document_page_repository: DocumentPageRepository):
        self.document_repository = document_repository
        self.document_page_repository = document_page_repository
        super().__init__(document_repository)
        
    async def create(self, file: UploadFile):
        if file.content_type != "application/pdf":
            raise ValidationError(detail="Invalid file type")

        try:
            os.makedirs("uploads", exist_ok=True)
            file_location = get_random_file_location(file.filename)
            content = await file.read()   
            with open(file_location, "wb") as f:
                f.write(content)

            new_file = DocumentCreate(title=file.filename, file_path=file_location)
            
            pdf_loader = PyPDFLoader(file_location)
            pages = pdf_loader.load()
            
            response = self.document_repository.create_with_pages(new_file, pages)
            return response

        except Exception as e:
            logger.error(f"Error uploading file: {e}")  
            raise InternalServerError("Failed to process the file")
