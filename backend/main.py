from fileinput import filename
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from scan_AI import scan_file
import uuid

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
id = 1
file_id = "file" + str(id)

@app.get("/")
def root():
    return {"message": "Backend is running successfully!"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Save uploaded file to the uploads/ folder"""
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

        file_id = str(uuid.uuid4())
        files[file_id] = file.filename

    scan_file(file.filename)
    
    return {"filename": file.filename, "message": "File uploaded successfully and scanned!"}


@app.get("/files/{name}")
async def get_file(name: str):
    file_path = os.path.join(UPLOAD_FOLDER, name)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")
    
@app.get('/responses/{name}')
async def get_responses(name: str):
    resName = name + "_response.json"
    filePath = os.path.join(RESPONSE_FOLDER, resName)
    if os.path.exists(filePath):
        return FileResponse(filePath)
    else:
        raise HTTPException(status_code=404, detail="File not found")


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