from fileinput import filename
from urllib import response
from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import boto3
from scan_AI import scan_file, scan_file_with_rag
import uuid
import time
from botocore.exceptions import ClientError
import botocore.exceptions
import json

import os

# Create a FastAPI instance
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Folder to store uploaded files
UPLOAD_FOLDER = "uploads"
RESPONSE_FOLDER = "response"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

items = []
files = {}

### AWS BUCKET
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
REGION = os.getenv("AWS_REGION")

s3 = boto3.resource(
                    's3',
                    aws_access_key_id = os.getenv("AWS_ACCESS_KEY"),
                    aws_secret_access_key=  os.getenv("AWS_SECRET_ACCESS_KEY"),
                    region_name= REGION
                        )

                        
s3_client = boto3.client(
                        's3',
                        aws_access_key_id = os.getenv("AWS_ACCESS_KEY"),
                        aws_secret_access_key=  os.getenv("AWS_SECRET_ACCESS_KEY"),
                        region_name='us-east-2'
                        )

@app.get("/")
def root():
    return {"message": "Backend is running successfully!"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):

    filename = file.filename
    file_id = str(uuid.uuid4())
    files[file_id] = filename
    
    upload_location = f"{UPLOAD_FOLDER}/{filename}"


    s3_client.upload_fileobj(file.file, S3_BUCKET, upload_location)
  ##  response_location = scan_file(s3_client, S3_BUCKET, upload_location)
    response_location = scan_file_with_rag(s3_client, S3_BUCKET, upload_location) 

    for _ in range(15):
        try:
            s3_client.head_object(Bucket=S3_BUCKET, Key=response_location)
            break
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                time.sleep(1)
            else:
                raise
            

    return {
        "filename": filename,
        "upload_url": f"https://{S3_BUCKET}.s3.{REGION}.amazonaws.com/{upload_location}",
        "response_url": f"https://{S3_BUCKET}.s3.{REGION}.amazonaws.com/{response_location}",
        "message": "File scanned and results stored in S3!"
    }

@app.get("/files/{name}")
async def get_file(name: str):
    get_key = f"{UPLOAD_FOLDER}/{name}"

    try:
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=get_key)
        file_bytes = response["Body"].read()

        
        try:
            file_content = file_bytes.decode("utf-8")
            return Response(content=file_content, media_type="text/plain")
        except UnicodeDecodeError:
            return Response(content=file_bytes, media_type="application/octet-stream")

    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            raise HTTPException(status_code=404, detail="File not found in S3.")
        else:
            raise HTTPException(status_code=500, detail=f"S3 error: {str(e)}")

    
@app.get('/responses/{name}')
async def get_responses(name: str):
    res_key = f"{RESPONSE_FOLDER}/{name}_response.json"

    try:
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=res_key)
        content = response["Body"].read().decode("utf-8")

        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Invalid JSON in response file.")
        return data

    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            raise HTTPException(status_code=404, detail="Response file not found in S3.")
        else:
            raise HTTPException(status_code=500, detail=f"S3 error: {str(e)}")

@app.post("/items")
def create_item(item: str):
    items.append(item)
    return items


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if -1 < item_id < len(items):
        item = items[item_id]
        return {"item": item}
    else:
        raise HTTPException(status_code=404, detail="Item not found")