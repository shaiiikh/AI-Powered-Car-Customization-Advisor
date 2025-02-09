from pydub import AudioSegment
import whisper
import os
import streamlit as st

# Load the Whisper model (use a smaller one like 'small' for deployment)
@st.cache_resource
def load_model():
    try:
        model = whisper.load_model("small")  # Using a smaller model for faster loading
        return model
    except Exception as e:
        st.error(f"Error loading Whisper model: {e}")
        return None

model = load_model()

def transcribe_audio(audio_path):
    try:
        # Directly use Whisper's ability to process .mp3 and .wav files
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        return f"Transcription error: {e}"
