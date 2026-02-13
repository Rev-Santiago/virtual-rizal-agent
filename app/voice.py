import os
import edge_tts
from faster_whisper import WhisperModel
import asyncio

# Initialize Whisper for Speech-to-Text (STT)
# device="cpu" ensures it runs on any laptop/edge device without a GPU
# compute_type="int8" makes it faster and lighter
stt_model = WhisperModel("tiny", device="cpu", compute_type="int8")

def transcribe_audio(file_path: str) -> str:
    """Converts audio file to text using local Whisper model."""
    segments, _ = stt_model.transcribe(file_path, beam_size=5)
    text = " ".join([segment.text for segment in segments])
    return text.strip()

async def text_to_speech(text: str, output_file: str):
    """Converts text to audio file using Edge TTS (Offline-capable)."""
    # Voices: 
    # 'en-US-ChristopherNeural' (Male, Formal - Good for Rizal)
    # 'en-US-AriaNeural' (Female, Professional - Good for Real Estate)
    voice = "en-US-ChristopherNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)