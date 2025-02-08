# audio_processing.py
from pydub import AudioSegment
import whisper  # Try using the OpenAI Whisper if available
import os
import streamlit as st

# Load the Whisper model only once using Streamlit's cache
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

# Function to transcribe audio
def transcribe_audio(audio_path):
    try:
        # Convert audio to WAV if necessary
        audio = AudioSegment.from_file(audio_path)
        temp_wav_path = "temp.wav"
        audio.export(temp_wav_path, format="wav")

        # Ensure the file exists before transcription
        if os.path.exists(temp_wav_path):
            result = model.transcribe(temp_wav_path)
            return result["text"]
        else:
            return "Error: Audio file conversion failed."
    except Exception as e:
        return f"Transcription error: {e}"
