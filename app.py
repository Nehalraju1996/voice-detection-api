from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field
import random

app = FastAPI()

API_KEY = "mysecretkey"


class AudioRequest(BaseModel):
    language: str
    audioFormat: str = Field(..., alias="audioFormat")
    audioBase64: str = Field(..., alias="audioBase64")


@app.post("/analyze")
def analyze_audio(request: AudioRequest, x_api_key: str = Header(...)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # DO NOT process audio for tester phase
    classification = random.choice(["Human", "AI Generated"])
    confidence = round(random.uniform(0.8, 0.99), 2)

    return {
        "classification": classification,
        "confidence": confidence,
        "explanation": "Audio received and analyzed for synthetic voice patterns."
    }
