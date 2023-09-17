from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, List, Optional
from pathlib import Path
import glob
import os

from helpers.detect_people import detect_people
from helpers.service_time import service_time

UPLOAD_DIR = Path() / 'uploads'
VIDEO_DIR = Path() / 'videos'
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
    
    cleanupUploadDirectories(UPLOAD_DIR)

    return {
        "total_people": total_people
    }
    
@app.post("/detect-people-video")
async def post_service_time_video(files: UploadFile):
    # Code to receive video from front-end and execute
    data = await files.read()
    save_to = VIDEO_DIR / files.filename
    
    with open(save_to, 'wb') as f:
            f.write(data)

    average_service_time = await service_time('./videos/' + files.filename)

    cleanupUploadDirectories(VIDEO_DIR)

    return {
        "average_service_time": average_service_time
    }

def cleanupUploadDirectories(dirToClean):
    filelist = glob.glob(os.path.join(dirToClean, "*"))
    for f in filelist:
        os.remove(f)
 