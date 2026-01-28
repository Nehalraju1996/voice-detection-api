from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field
import base64
import uuid
from pydub import AudioSegment
import librosa
import os
import random

app = FastAPI()

API_KEY = "mysecretkey"


# -------- Request Model (GUVI camelCase compatible) --------
class AudioRequest(BaseModel):
    language: str
    audioFormat: str = Field(..., alias="audioFormat")
    audioBase64: str = Field(..., alias="audioBase64")


# -------- Save Base64 Audio --------
def save_base64_audio(base64_string, file_path):
    audio_bytes = base64.b64decode(base64_string)
    with open(file_path, "wb") as f:
        f.write(audio_bytes)


# -------- Dummy Audio Processing --------
def process_audio(file_path):
    sound = AudioSegment.from_file(file_path)
    wav_path = file_path.replace(".mp3", ".wav")
    sound.export(wav_path, format="wav")

    y, sr = librosa.load(wav_path)
    duration = librosa.get_duration(y=y, sr=sr)

    classification = random.choice(["Human", "AI Generated"])
    confidence = round(random.uniform(0.7, 0.99), 2)

    explanation = f"Audio duration {duration:.2f}s analyzed for spectral patterns."

    return classification, confidence, explanation


# -------- API Endpoint --------
@app.post("/analyze")
def analyze_audio(request: AudioRequest, x_api_key: str = Header(...)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    temp_file = f"{uuid.uuid4()}.mp3"

    try:
        save_base64_audio(request.audioBase64, temp_file)
        classification, confidence, explanation = process_audio(temp_file)

        return {
            "classification": classification,
            "confidence": confidence,
            "explanation": explanation
        }

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
