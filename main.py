from fastapi import FastAPI
from helpers.detect_people import detect_people

app = FastAPI()

@app.get("/detect-people-photo")
async def detect_people_photo():
    total_people = detect_people()
    return {
        "message": "Hello, world!",
        "total_people": total_people
    }
    
@app.get("/detect-people-video")
async def detect_people_video():
    total_people = 1
    return 1