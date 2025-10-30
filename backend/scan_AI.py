from openai import OpenAI
import json
from dotenv import load_dotenv
import os


load_dotenv()

def scan_file(file):
    folder = "uploads"
    with open(os.path.join(folder, file), "rb") as f:
        workingFile = f.read()

    prompt = f"""   
                    You are a security auditor for automotive systems.
                    Given vehicle-related code, configs, or logs, identify vulnerabilities and risky patterns,
                    especially those relevant to CAN, diagnostics, and ECU software.
                    For each finding, return: type, severity (Low/Medium/High),
                    a real-world example of this vulnerability on where it might or did happen, and a recommended fix.
                    Return ONLY valid JSON that matches the provided schema in the user message.
                    Be concise and specific.
                    Here is the code: {workingFile}
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
    file_name = file + "_response.json"
    folder_path = "response"
    full_file_path = os.path.join(folder_path, file_name)

    os.makedirs(folder_path, exist_ok=True)

    try:
        with open(full_file_path, "w") as file:
            file.write(jsonResponse)

    except FileExistsError:
        return "ERROR"

    return None

#scan_file("ifelse.cpp")





