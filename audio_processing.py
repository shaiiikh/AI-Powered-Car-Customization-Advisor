from pydub import AudioSegment
import whisper
import os
import streamlit as st

# Manually set ffmpeg path for deployment environments
AudioSegment.ffmpeg = "/usr/bin/ffmpeg"
AudioSegment.ffprobe = "/usr/bin/ffprobe"

@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

def transcribe_audio(audio_path):
    try:
        audio = AudioSegment.from_file(audio_path)
        temp_wav_path = "temp.wav"
        audio.export(temp_wav_path, format="wav")

        if os.path.exists(temp_wav_path):
            result = model.transcribe(temp_wav_path)
            return result["text"]
        else:
            return "Error: Audio file conversion failed."
    except Exception as e:
        return f"Transcription error: {e}"
