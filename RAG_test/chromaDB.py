from ragModel import get_embedded_function, load_documents, doc_splitter
#from langchain_community.vectorstores import Chroma 
import os
from langchain_chroma import Chroma

CHROMA_PATH = "chroma_db"


def add_to_chroma(chunks):
    db = Chroma(
        persist_directory = CHROMA_PATH, 
        embedding_function = get_embedded_function()
    )
    new_chunks = [chunk for chunk in chunks]
    new_chunk_ids = [chunk.metadata["id"] for chunk in chunks]

    db.add_documents(new_chunks, ids=new_chunk_ids)
   # db.persist()


documents = load_documents()
chunks = doc_splitter(documents)

for i, chunk in enumerate(chunks):
    source = os.path.basename(chunk.metadata.get("source", "unknown"))
    page = chunk.metadata.get("page", 0)
    chunk_id = f"{source}_page{page}_chunk{i}"

    chunk.metadata["id"] = chunk_id

add_to_chroma(chunks)