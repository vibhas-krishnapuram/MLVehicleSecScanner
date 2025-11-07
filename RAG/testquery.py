from langchain_aws import ChatBedrock
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from ragModel import get_embedded_function
import os
from dotenv import load_dotenv

load_dotenv()


CHROMA_PATH = "chroma_db"
embedding = get_embedded_function()

db = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embedding
)

retriever = db.as_retriever(search_kwargs={"k": 3})

llm = ChatBedrock(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="us-east-2"
)


prompt = ChatPromptTemplate.from_template("""
You are a helpful AI assistant.
Use the provided context to answer the user's question.

Context:
{context}

Question: {question}

Answer clearly and concisely:
""")

rag_chain = (
    {"context": retriever | (lambda docs: "\n\n".join(d.page_content for d in docs)),
     "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- Query the RAG ---
query = "Summarize the key points in Assignment4.pdf."
response = rag_chain.invoke(query)

print("\n Question:", query)
print("\n Answer:", response)
