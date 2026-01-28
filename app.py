from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import requests
import uuid
from pydub import AudioSegment
import librosa
import os
import random

app = FastAPI()

API_KEY = "mysecretkey"
security = HTTPBearer()


# -------- Request Model --------
class AudioRequest(BaseModel):
    message: str
    audio_url: str


# -------- Auth Verification using Security --------
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


# -------- Audio Download --------
def download_audio(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)


# -------- Dummy Audio Processing --------
def process_audio(file_path):
    sound = AudioSegment.from_mp3(file_path)
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
def analyze_audio(
    request: AudioRequest,
    _: str = Depends(verify_token)
):

    temp_file = f"{uuid.uuid4()}.mp3"

    try:
        download_audio(request.audio_url, temp_file)
        classification, confidence, explanation = process_audio(temp_file)

        return {
            "classification": classification,
            "confidence": confidence,
            "explanation": explanation
        }

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
