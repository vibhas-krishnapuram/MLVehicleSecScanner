from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_aws import BedrockEmbeddings
from dotenv import load_dotenv
import os


DATA_PATH = "Vulnerabilities.pdf"

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")


class PrepareFile:
    def __init__(self, file):
        self.data_path = file

    def load_documents(self):
        document_loader = PyPDFLoader(self.data_path)
        return document_loader.load()


    def doc_splitter(self, documents: list[Document]):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=30,
            length_function=len,
            is_separator_regex=False
        )
        return text_splitter.split_documents(documents)

    def get_embedded_function(self):
        embedding = BedrockEmbeddings(
            model_id="amazon.titan-embed-text-v2:0",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-2")
        )
        return embedding
    
    def id_chunks(self, chunks):
        for i, chunk in enumerate(chunks):
            source = os.path.basename(chunk.metadata.get("source", "unknown"))
            page = chunk.metadata.get("page", 0)
            chunk_id = f"{source}_page{page}_chunk{i}"

            chunk.metadata["id"] = chunk_id

        return chunks



# pf = PrepareFile(DATA_PATH)

# document = pf.load_documents()
# chunks = pf.doc_splitter(document)
# chunks = pf.id_chunks(chunks)

# print(chunks[5].metadata['id'])


