from openai import OpenAI
import json
from dotenv import load_dotenv
import os
from io import BytesIO
import boto3

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






