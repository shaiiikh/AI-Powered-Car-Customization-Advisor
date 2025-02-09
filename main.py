import streamlit as st
st.set_page_config(page_title="AI Car Customization", page_icon="🚗", layout="wide")
import numpy as np
import tempfile
import random
import base64
from gtts import gTTS
from pydub import AudioSegment
import wave
from audio_processing import transcribe_audio
from car_customization import get_customization_suggestions
import requests
import os
import time
from audio_recorder_streamlit import audio_recorder
from pydub import AudioSegment
from pydub.utils import which

# Explicitly set ffmpeg and ffprobe paths for Streamlit Cloud
AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")


# --- PAGE CONFIGURATION ---


# --- EMBEDDED CSS STYLING ---
st.markdown("""
    <style>
        body {
            background-color: #f9f9f9;
            color: black;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        [data-theme="dark"] body {
            background-color: #1e1e1e;
            color: #f9f9f9;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #135387;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .header h1 {
            color: white;
            font-size: 40px;
            margin: 0;
        }
        .footer {
            text-align: center;
            font-size: 14px;
            margin-top: 40px;
            color: #888;
        }
        .custom-card {
            background-color: #E8F4F8;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            color: black;
            margin-top: 20px;
        }
        [data-theme="dark"] .custom-card {
            background-color: #2b2b2b;
            color: #f9f9f9;
        }
        .custom-card h3 {
            color: #135387;
            font-size: 24px;
        }
        .custom-card p {
            font-size: 16px;
            line-height: 1.6;
            color: #333;
        }
        [data-theme="dark"] .custom-card p {
            color: #ccc;
        }
        .audio-control {
            margin-top: 20px;
            width: 100%;
        }
        .social-buttons {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 20px;
        }
        .social-buttons img {
            width: 32px;
            height: 32px;
            transition: filter 0.3s ease;
        }
        [data-theme="dark"] .social-buttons img {
            filter: invert(1);
        }
        button {
            background-color: #135387;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #0f4369;
        }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="header">
        <h1>🚗🚨 AI-Powered Car Customization Advisor</h1>
    </div>
""", unsafe_allow_html=True)

# --- RECORD AUDIO FEATURE ---
st.markdown("### 🎧 Record Your Own Voice")

audio_bytes = audio_recorder(pause_threshold=10.0, text="Click to Record")

if audio_bytes:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio_file:
        temp_audio_file.write(audio_bytes)
        temp_audio_file_path = temp_audio_file.name

    audio = AudioSegment.from_file(temp_audio_file_path)
    wav_audio_path = temp_audio_file_path.replace('.mp3', '.wav')
    audio.export(wav_audio_path, format="wav")

    st.audio(audio_bytes, format="audio/wav")

    transcription = transcribe_audio(wav_audio_path).strip()
    st.markdown("<div class='custom-card'><h3>📝 Transcription</h3><p>{}</p></div>".format(transcription), unsafe_allow_html=True)

    suggestions = get_customization_suggestions(transcription)
    if not suggestions or "No specific customizations detected." in suggestions:
        if any(word in transcription.lower() for word in ["car", "vehicle", "jeep", "automobile"]):
            suggestions = "Consider upgrading your car's interior with luxury leather seats, add custom alloy wheels, or install a premium sound system for an immersive experience."
        else:
            suggestions = "No relevant car customizations detected from your audio."

    st.markdown("<div class='custom-card'><h3>🚗 Customization Suggestions</h3>", unsafe_allow_html=True)

    for suggestion in suggestions.split("\n"):
        st.markdown(f"- {suggestion}")

    st.markdown("</div>", unsafe_allow_html=True)

    tts = gTTS(text=suggestions, lang="en")
    tts.save("suggestions_audio.mp3")

    with open("suggestions_audio.mp3", "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()

    st.markdown(f"""
        <audio controls class="audio-control">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
    """, unsafe_allow_html=True)
else:
    st.warning("Click the record button to start recording your voice.")

# --- UPLOAD AUDIO FILE FEATURE ---
st.markdown("### 📂 Browse and Upload Your Audio File")
audio_file = st.file_uploader("Choose an audio file...", type=["wav", "mp3", "flac"])

if audio_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
        temp_file.write(audio_file.read())
        audio_file_path = temp_file.name

    st.audio(audio_file_path, format="audio/wav")

    transcription = transcribe_audio(audio_file_path).strip()
    st.markdown("<div class='custom-card'><h3>📝 Transcription</h3><p>{}</p></div>".format(transcription), unsafe_allow_html=True)

    suggestions = get_customization_suggestions(transcription)
    if not suggestions or "No specific customizations detected." in suggestions:
        if any(word in transcription.lower() for word in ["car", "vehicle", "jeep", "automobile"]):
            suggestions = "Consider upgrading your car's interior with luxury leather seats, add custom alloy wheels, or install a premium sound system for an immersive experience."
        else:
            suggestions = "No relevant car customizations detected from your audio."

    st.markdown("<div class='custom-card'><h3>🚗 Customization Suggestions</h3>", unsafe_allow_html=True)

    for suggestion in suggestions.split("\n"):
        st.markdown(f"- {suggestion}")

    st.markdown("</div>", unsafe_allow_html=True)

    tts = gTTS(text=suggestions, lang="en")
    tts.save("suggestions_audio.mp3")

    with open("suggestions_audio.mp3", "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()

    st.markdown(f"""
        <audio controls class="audio-control">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
    """, unsafe_allow_html=True)

# --- SOCIAL LINKS ---
st.markdown("""
    <div class="social-buttons">
        <a href="https://github.com/shaiiikh" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub">
        </a>
        <a href="https://www.linkedin.com/in/ali-shaiiikh" target="_blank">
            <img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" alt="LinkedIn">
        </a>
    </div>
""", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
    <div class='footer'>
        Developed by shaiiikh 👨‍💻
    </div>
""", unsafe_allow_html=True)
