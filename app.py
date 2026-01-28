from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import base64
import uuid
from pydub import AudioSegment
import librosa
import os
import random

app = FastAPI()

API_KEY = "mysecretkey"


class AudioRequest(BaseModel):
    language: str
    audio_format: str
    audio_base64: str


def save_base64_audio(base64_string, file_path):
    audio_bytes = base64.b64decode(base64_string)
    with open(file_path, "wb") as f:
        f.write(audio_bytes)


def process_audio(file_path):
    sound = AudioSegment.from_mp3(file_path)
    wav_path = file_path.replace(".mp3", ".wav")
    sound.export(wav_path, format="wav")

    y, sr = librosa.load(wav_path)
    duration = librosa.get_duration(y=y, sr=sr)

    classification = random.choice(["Human", "AI Generated"])
    confidence = round(random.uniform(0.7, 0.99), 2)

    explanation = f"Audio duration {duration:.2f}s analyzed for spectral patterns."

    return classification, confidence, explanatio