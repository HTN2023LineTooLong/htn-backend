from fastapi import FastAPI
from helpers.detect_people import detect_people

app = FastAPI()

@app.get("/")
async def root():
    total_people = detect_people()
    return {
        "message": "Hello, world!",
        "total_people": total_people
    }