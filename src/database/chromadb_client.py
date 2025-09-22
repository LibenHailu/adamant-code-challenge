# import chromadb
# from chromadb.api import ClientAPI
# from chromadb.api.models.Collection import Collection
# from fastapi import Depends
# from dotenv import load_dotenv
# import os

# load_dotenv()

# _client: ClientAPI | None = None
# _collection: Collection | None = None

# def get_chroma_client() -> ClientAPI:
# 	global _client
# 	if _client is None:
# 		_client = chromadb.CloudClient(
#             api_key=os.getenv("CHROMA_API_KEY"),
#             tenant=os.getenv("CHROMA_TENANT"),
#             database=os.getenv("CHROMA_DATABASE")
#         )
# 	return _client

# def get_chroma_collection(client: ClientAPI = Depends(get_chroma_client)) -> Collection:
# 	global _collection
# 	if _collection is None:
# 		_collection = client.get_or_create_collection(
# 		    name="challenge_collection",
# 		)
# 	return _collection

import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb import PersistentClient

class ChromaClient:
    def __init__(self):
        self.embedding_function = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, length_function=len
        )
        
        self.client = PersistentClient(path="./chroma_db")
        self.vectorstore = Chroma(
            client=self.client,
            collection_name="adamant",
            embedding_function=self.embedding_function,
        )
    
    def get_vectorstore(self):
        return self.vectorstore
    
    def get_text_splitter(self):
        return self.text_splitter