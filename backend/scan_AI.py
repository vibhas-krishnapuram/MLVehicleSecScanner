from openai import OpenAI
import json
from dotenv import load_dotenv
import os
from io import BytesIO
import boto3
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


load_dotenv()

def scan_file(s3, bucket_name, file_ref):
    folder = "uploads"
    
    obj = s3.get_object(Bucket=bucket_name, Key=file_ref)
    file_bytes = obj["Body"].read()
    code_text = file_bytes.decode("utf-8")

    prompt = f"""   
                    You are a security auditor for automotive systems.
                    Given vehicle-related code, configs, or logs, identify vulnerabilities and risky patterns,
                    especially those relevant to CAN, diagnostics, and ECU software.
                    For each finding, return: type, severity (Low/Medium/High),
                    a real-world specific example of this vulnerability on where it might or did happen to a specific car or year, and a recommended fix, and the actual code to fix from the code file as well as line number.
                    Return ONLY valid JSON that matches the provided schema in the user message.
                    Be concise and specific.
                    Here is the code: {code_text}
                    Return ONLY raw JSON. No explanations, no surrounding backticks.
            """

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    chat_completion = client.chat.completions.create(
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o-mini"
    )

    jsonResponse = chat_completion.choices[0].message.content

    try:
        parsed = json.loads(jsonResponse)
    except json.JSONDecodeError:
        parsed = [{"error": "Invalid JSON from OpenAI"}]
    

    file_name = os.path.basename(file_ref) + "_response.json"
    folder_path = "response"
    upload_key = f"{folder_path}/{file_name}"

    json_bytes = BytesIO(json.dumps(parsed, indent=4).encode("utf-8"))

    try:
        s3.upload_fileobj(json_bytes, bucket_name, upload_key)

    except FileExistsError:
        return "ERROR"

    return upload_key

def scan_file_with_rag(s3, bucket_name, file_ref, debug=False):
    """
    This function:
      1. Downloads a file from S3.
      2. Queries your local RAG (Chroma DB) for context.
      3. Sends a single combined prompt to OpenAI (RAG context + code).
      4. Uploads the final JSON vulnerability analysis back to S3.
    """
    if debug:
        print("Starting scan for:", file_ref)

    obj = s3.get_object(Bucket=bucket_name, Key=file_ref)
    file_bytes = obj["Body"].read()
    code_text = file_bytes.decode("utf-8")

    if debug:
        print(f"File loaded from S3 ({len(code_text)} chars)")

    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        chroma_db = Chroma(
            persist_directory="./chroma_db",
            embedding_function=embeddings
        )

        query_text = "C++ vulnerabilities and best practices for secure automotive software."
        results = chroma_db.similarity_search(query_text, k=4)
        rag_context = "\n\n".join([doc.page_content for doc in results])

        if debug:
            print(f"Retrieved {len(results)} context docs from RAG DB")
    except Exception as e:
        rag_context = ""
        if debug:
            print("RAG query failed:", e)

    

    prompt = f"""
    You are a security auditor for automotive systems.
    Given vehicle-related code, configs, or logs, identify vulnerabilities and risky patterns,
    especially those relevant to CAN, diagnostics, and ECU software.

    Use the following context from your knowledge base:
    {rag_context}

    Now, analyze this code:
    {code_text}

    For each finding, return:
    - type: "type"
    - severity (Low/Medium/High): "severity"
    - a real-world example (car model/year if possible): "example"
    - the vulnerable code section: "code"
    - line number: "line_number"
    - the recommended fix (with secure code snippet): "recommended_fix"

    Here is a sample:
    
    "type": "Hardcoded Credentials",
    "severity": "High",
    "example": "The use of hardcoded API keys can lead to unauthorized access, as was seen in the 2019 Jeep and Chrysler recall due to similar issues.",
    "recommended_fix": "Remove hardcoded API keys and use a secure method to store and retrieve sensitive information.",
    "code": "const std::string DEVICE_API_KEY = \"CAR_HARDCODED_API_KEY_98765\";",
    "line_number": 5
    
    Return ONLY valid JSON valid with provided schema.
    Return ONLY raw JSON. No explanations, no surrounding backticks.
        """


    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert automotive cybersecurity auditor."},
                {"role": "user", "content": prompt}
            ]
        )
        jsonResponse = chat_completion.choices[0].message.content

        if debug:
            print("Model returned response (first 400 chars):")
            print(jsonResponse[:400])

    except Exception as e:
        print("Error from OpenAI:", e)
        return [{"error": str(e)}]


    try:
        parsed = json.loads(jsonResponse)
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        print("Raw output from model:\n", jsonResponse)
        parsed = [{"error": "Invalid JSON from OpenAI"}]


    file_name = os.path.basename(file_ref) + "_response.json"
    upload_key = f"response/{file_name}"
    json_bytes = BytesIO(json.dumps(parsed, indent=4).encode("utf-8"))

    try:
        s3.upload_fileobj(json_bytes, bucket_name, upload_key)
        if debug:
            print("☁️ Uploaded analysis to S3:", upload_key)
    except Exception as e:
        print("Upload failed:", e)
        return "ERROR"

    if debug:
        print("Scan completed successfully!")

    return upload_key
