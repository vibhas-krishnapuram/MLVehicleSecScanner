from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
#from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_aws import BedrockEmbeddings
import os



DATA_PATH = "Assignment4.pdf"

def load_documents():
    document_loader = PyPDFLoader(DATA_PATH)
    return document_loader.load()

def doc_splitter(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=30,
        length_function=len,
        is_separator_regex=False
    )
    return text_splitter.split_documents(documents)

def get_embedded_function():
    embedding = BedrockEmbeddings(
        model_id="amazon.titan-embed-text-v2:0",       
        region_name="us-east-2"
    )
    return embedding

document = load_documents()
chunks = doc_splitter(document)

for i, chunk in enumerate(chunks):
    source = os.path.basename(chunk.metadata.get("source", "unknown"))
    page = chunk.metadata.get("page", 0)
    chunk_id = f"{source}_page{page}_chunk{i}"

    chunk.metadata["id"] = chunk_id

print(chunks[5].metadata['id'])