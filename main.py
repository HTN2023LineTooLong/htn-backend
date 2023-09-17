from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, List, Optional
from pathlib import Path
import glob

from helpers.detect_people import detect_people

UPLOAD_DIR = Path() / 'uploads'
app = FastAPI()

origins = ["http://localhost:3000", "localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/detect-people-photo")
async def detect_people_photo():
    total_people = detect_people()
    return {
        "message": "Hello, world!",
        "total_people": total_people
    }
    
@app.post("/detect-people-photo")
async def post_detect_people_photo(files: list[UploadFile]):
    image_list = []
    for file in files:
        data = await file.read()
        save_to = UPLOAD_DIR / file.filename
        image_list.append(data)
        with open(save_to, 'wb') as f:
            f.write(data)
    total_people = await detect_people(glob.glob('./uploads/*.jpg'))
    print(total_people)
    return {
        "total_people": total_people
    }
    
@app.post("/detect-people-video")
async def detect_people_video():
    # Code to receive video from front-end and execute
    return 1