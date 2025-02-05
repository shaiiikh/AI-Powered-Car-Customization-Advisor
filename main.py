import streamlit as st
import sounddevice as sd
import numpy as np
import tempfile
import random
import base64
from gtts import gTTS
import wave
from audio_processing import transcribe_audio
import requests
import os
import pyaudio
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Car Customization", page_icon="🚗", layout="wide")

# --- CUSTOM CSS STYLING ---
st.markdown("""
    <style>
        body {
            background-color: #f9f9f9;
            color: black;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #333;
            padding: 15px;
            border-radius: 10px;
        }
        .header h1 {
            color: white;
            margin: 0;
        }
        .social-buttons {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            margin-top: 10px;
        }
        .social-buttons a {
            text-decoration: none;
            font-weight: bold;
            font-size: 18px;
        }
        .social-buttons img {
            width: 24px;
            height: 24px;
        }
        .footer {
            text-align: center;
            font-size: 14px;
            margin-top: 20px;
            color: #888888;
        }
        .custom-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            color: black;
            margin-bottom: 10px;
        }
        .highlight {
            color: black;
            font-weight: bold;
        }
        .button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            padding: 10px 20px;
            border-radius: 5px;
        }
        .button:hover {
            background-color: #45a049;
        }
        #transcription {
            font-size: 18px;
            line-height: 1.8;
        }
        .audio-control {
            margin-top: 20px;
            width: 100%;
        }
        .amplitude-plot {
            height: 100px;
            width: 100%;
            background-color: #ddd;
            margin-top: 20px;
        }
        .button-row {
            display: flex;
            justify-content: space-between;
            gap: 10px;
        }
        .green-button {
            background-color: green;
            color: white;
        }
        .red-button {
            background-color: red;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="header">
        <h1>🚗💨 AI-Powered Car Customization Advisor</h1>
    </div>
""", unsafe_allow_html=True)

# --- CAR CUSTOMIZATION SUGGESTIONS ---
suggestions = [
    "Upgrade to LED or neon underglow lighting for a futuristic look.",
    "Try a matte or metallic wrap to give your car a unique aesthetic.",
    "Consider installing carbon fiber accents for a sportier appeal.",
    "How about adding custom racing stripes for a bold statement?",
    "Upgrade your exhaust system for a more powerful sound and performance.",
    "Tint your windows for privacy and a sleek, modern touch.",
    "Personalize your license plate with a custom frame or LED lights.",
    "Swap out your stock grille for a custom-designed one that stands out.",
    "Install a roof rack for added storage and a rugged look.",
    "Upgrade your car's interior lighting with ambient LED strips.",
    "Enhance your dashboard with a digital display or heads-up display (HUD).",
    "Get a custom steering wheel cover to match your personality.",
    "Install heated or ventilated seats for ultimate driving comfort.",
    "Try a body kit to give your car an aggressive, performance-oriented look.",
    "Upgrade your brake calipers with a custom color for a sportier feel.",
    "Install retractable side steps for easier entry and exit.",
    "Opt for smart keyless entry for convenience and security.",
    "Add a high-performance air intake system for better fuel efficiency.",
    "Customize your rims with a unique design or color finish.",
    "Install a rear diffuser for improved aerodynamics and style."
]

# --- RECORD AUDIO FEATURE ---
st.markdown("### 🎙️ Record Your Own Voice")

# Initialize state variables
if "is_recording" not in st.session_state:
    st.session_state.is_recording = False
if "recording_complete" not in st.session_state:
    st.session_state.recording_complete = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "wavfile" not in st.session_state:
    st.session_state.wavfile = None

# Initialize audio parameters
samplerate = 16000  # Sample rate in Hz
duration = 10  # Duration of the recording in seconds
channels = 1  # Mono audio

def start_recording():
    st.session_state.is_recording = True
    st.session_state.start_time = time.time()
    st.session_state.recording_complete = False
    st.rerun()

def reset_recording():
    st.session_state.is_recording = False
    st.session_state.recording_complete = False
    st.session_state.start_time = None
    st.session_state.wavfile = None
    st.rerun()

# --- BUTTON FOR START RECORDING ---
if not st.session_state.is_recording and not st.session_state.recording_complete:
    col1, col2 = st.columns([3, 1])
    with col1:
        start_button = st.button("Start Recording (10 secs)", 
                                key="start_button", 
                                help="Start recording your voice for 10 seconds.", 
                                on_click=start_recording,
                                use_container_width=True)
    with col2:
        if st.button("Reset", on_click=reset_recording):
            st.rerun()

# --- RECORDING PROCESS AND STATUS ---
if st.session_state.is_recording:
    # Show recording status
    st.markdown("<div class='amplitude-plot'></div>", unsafe_allow_html=True)
    status_placeholder = st.empty()
    
    # Record audio
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
    
    # Show countdown
    for remaining in range(duration, 0, -1):
        status_placeholder.markdown(f"Recording... 🎙️ {remaining} seconds remaining")
        time.sleep(1)
    
    sd.wait()
    
    # After recording is complete
    st.session_state.is_recording = False
    st.session_state.recording_complete = True
    
    # Save the recorded audio
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio_file:
        st.session_state.wavfile = temp_audio_file.name
        with wave.open(st.session_state.wavfile, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            wf.writeframes(audio_data.tobytes())
    
    st.rerun()

# --- DISPLAY RECORDING COMPLETE AND RESULTS ---
if st.session_state.recording_complete and st.session_state.wavfile:
    st.success("Recording Complete! 🎉")
    
    # --- AUDIO PLAYBACK FOR RECORDED FILE ---
    st.audio(st.session_state.wavfile, format="audio/wav")
    
    # --- TRANSCRIPTION ---
    transcription = transcribe_audio(st.session_state.wavfile)
    st.markdown("<div class='custom-card'><h3>📝 Transcription</h3></div>", unsafe_allow_html=True)
    st.markdown(f"<div id='transcription'>{transcription}</div>", unsafe_allow_html=True)

    # --- CUSTOMIZATION SUGGESTIONS ---
    st.markdown("<div class='custom-card'><h3>🚘 Customization Suggestions</h3></div>", unsafe_allow_html=True)
    
    # Fetch random suggestions
    random_suggestions = random.sample(suggestions, 3)
    
    for suggestion in random_suggestions:
        st.markdown(f"- {suggestion}")

    # --- TEXT-TO-SPEECH (TTS) ---
    tts = gTTS(text=" ".join(random_suggestions), lang="en")
    tts.save("suggestions_audio.mp3")

    # Encode audio to play in Streamlit
    with open("suggestions_audio.mp3", "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()

    # Display Play Button for AI Voice
    st.markdown(f"""
        <audio controls class="audio-control">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
    """, unsafe_allow_html=True)

    # --- SAVE SUGGESTION AUDIO FILE ---
    save_button = st.button("Save Suggestions Audio", key="save_button")
    if save_button:
        suggestions_audio_path = "suggestions_audio_output.wav"
        tts.save(suggestions_audio_path)
        
        with open(suggestions_audio_path, "rb") as file:
            st.download_button(
                label="Download Suggestions Audio",
                data=file,
                file_name=suggestions_audio_path,
                mime="audio/wav"
            )

# --- BROWSE AUDIO FILE FEATURE ---
st.markdown("### 📂 Browse and Upload Your Audio File")
audio_file = st.file_uploader("Choose an audio file...", type=["wav", "mp3", "flac"])

if audio_file is not None:
    # Save uploaded audio file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
        temp_file.write(audio_file.read())
        audio_file_path = temp_file.name

    # --- AUDIO PLAYBACK FOR UPLOADED FILE ---
    st.audio(audio_file_path, format="audio/wav")

    # --- TRANSCRIPTION FOR UPLOADED FILE ---
    transcription = transcribe_audio(audio_file_path)
    st.markdown("<div class='custom-card'><h3>📝 Transcription</h3></div>", unsafe_allow_html=True)
    st.markdown(f"<div id='transcription'>{transcription}</div>", unsafe_allow_html=True)

    # --- CUSTOMIZATION SUGGESTIONS ---
    st.markdown("<div class='custom-card'><h3>🚘 Customization Suggestions</h3></div>", unsafe_allow_html=True)
    
    random_suggestions = random.sample(suggestions, 3)
    for suggestion in random_suggestions:
        st.markdown(f"- {suggestion}")

    # --- TEXT-TO-SPEECH (TTS) ---
    tts = gTTS(text=" ".join(random_suggestions), lang="en")
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
            <img id="github-logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/GitHub_Invertocat_Logo.svg/1200px-GitHub_Invertocat_Logo.svg.png" alt="GitHub">
        </a>
        <a href="https://www.linkedin.com/in/ali-shaiiikh" target="_blank">
            <img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" alt="LinkedIn">
        </a>
    </div>
""", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<div class='footer'>Developed by shaiiikh</div>", unsafe_allow_html=True)