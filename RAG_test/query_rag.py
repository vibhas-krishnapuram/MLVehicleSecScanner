from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_aws import ChatBedrock

import os
from ragModel import get_embedded_function

CHROMA_PATH = "chroma_db"

def load_db():
    embedding = get_embedded_function()
    db = Chroma(
        persist_directory = CHROMA_PATH, 
        embedding_function = get_embedded_function()
    )
    return db

def get_llm():

    llm = ChatBedrock(
        model_id="anthropic.claude-3-haiku-20240307-v1:0",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-2"
    )
    return llm

def query_rag(question):
    db = load_db()
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    llm = get_llm()

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    result = qa.invoke({"query": question})
    print("Answer:", result["result"])

    print("Sources:")
    for doc in result["source_documents"]:
        print(" -", doc.metadata.get("source", "Unknown"), "|", doc.page_content[:200])


query_rag("Summarize the main topic of this PDF")

