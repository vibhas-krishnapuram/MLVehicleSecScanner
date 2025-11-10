from PrepareFile_class import PrepareFile
import os
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")


class Chroma_Init:
    def __init__(self, file_path, db_path):
        self.pf = PrepareFile(file_path)
        self.chroma_path = db_path
        
    def add_to_chroma(self):

        documents = self.pf.load_documents()
        chunks = self.pf.doc_splitter(documents)
        chunks = self.pf.id_chunks(chunks)

        db = Chroma(
            persist_directory = self.chroma_path, 
            embedding_function = self.pf.get_embedded_function()
        )

        new_chunk_ids = [chunk.metadata["id"] for chunk in chunks]

        db.add_documents(documents=chunks, ids=new_chunk_ids)
        db.persist()

        return db
