import os
from fastapi import UploadFile, File, HTTPException
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.entities.document_page import DocumentPage
from src.entities.document import Document
from PyPDF2 import PdfReader
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from chromadb import PersistentClient

embedding_function = OpenAIEmbeddings()

chromadb_client = PersistentClient(path="./chroma_db")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, length_function=len
)

embedding_function = OpenAIEmbeddings()

vectorstore = Chroma(
    client=chromadb_client,
    collection_name="adamant",
    embedding_function=embedding_function,
)


async def upload_file(db, file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        # TODO: update to custom exception
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only PDFs are allowed."
        )

    try:
        os.makedirs("uploads", exist_ok=True)
        file_location = f"uploads/{file.filename}"
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)

        # Save file metadata to the database
        new_file = Document(title=file.filename, file_path=file_location)
        db.add(new_file)
        db.commit()
        db.refresh(new_file)

        pdf_loader = PyPDFLoader(file_location)
        documents = pdf_loader.load()
        for index, document in enumerate(documents):
            page_data = DocumentPage(
                document_id=new_file.id,
                page_number=index + 1,
                content=document.page_content,
            )
            db.add(page_data)
            db.commit()
            db.refresh(page_data)


        chunks = text_splitter.split_documents(documents)

        vectorstore.add_documents(
            documents=chunks,
            ids=[f"doc_{new_file.id}_chunk_{i}" for i in range(len(chunks))],
            metadatas = [{"document_id": new_file.id} for _ in enumerate(chunks)]
        )

        return new_file
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")
    # finally:
    #     if "file_location" in locals() and os.path.exists(file_location):
    #         os.remove(file_location)

 
