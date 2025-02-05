import streamlit as st
import numpy as np
import tempfile
import random
import base64
import wave
from audio_processing import transcribe_audio
import requests
import os

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
    "How about adding a custom paint job to give your car a fresh new look?",
    "Consider upgrading your wheels for better performance and style.",
    "Installing a new set of lights could really enhance the car’s appearance.",
    "You might want to check out custom seat covers that suit your style.",
    "How about adding a sunroof for a more luxurious feel?",
    "Consider a custom spoiler for added performance and aesthetics.",
    "A new sound system could make your car feel like a concert hall!"
]

# --- RECORD AUDIO FEATURE ---
st.markdown("### 🎙️ Record Your Own Voice")

# Initialize state to track recording status
if "is_recording" not in st.session_state:
    st.session_state.is_recording = False

# Button to start recording
def start_recording():
    st.session_state.is_recording = True

# Button to stop recording
def stop_recording():
    st.session_state.is_recording = False

# Initialize audio parameters
samplerate = 16000  # Sample rate in Hz
duration = 5  # Duration of the recording in seconds
channels = 1  # Mono audio

# Create an empty numpy array to store the audio
audio_data = np.zeros((duration * samplerate,), dtype=np.int16)

# Initialize wavfile variable
wavfile = None

# --- BUTTONS FOR START AND STOP RECORDING ---
if not st.session_state.is_recording:
    start_button = st.button("Start Recording", on_click=start_recording, key="start_button", help="Start recording your voice.", use_container_width=True)
else:
    stop_button = st.button("Stop Recording", on_click=stop_recording, key="stop_button", help="Stop recording.", use_container_width=True)

# --- VISUAL INDICATOR FOR AMPLITUDE ---
if st.session_state.is_recording:
    st.markdown("<div class='amplitude-plot'></div>", unsafe_allow_html=True)
    # Placeholder for live recording amplitude (will just show a background to show that recording is in progress)
    st.markdown("Recording... 🎙️ Speak now!")

    # Record audio
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
    sd.wait()

    # Save the recorded audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio_file:
        wavfile = temp_audio_file.name
        with wave.open(wavfile, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)  # 2 bytes per sample (16-bit)
            wf.setframerate(samplerate)
            wf.writeframes(audio_data.tobytes())

    # --- AUDIO PLAYBACK FOR RECORDED FILE ---
    st.audio(wavfile, format="audio/wav")

    # --- TRANSCRIPTION ---
    transcription = transcribe_audio(wavfile)
    st.markdown("<div class='custom-card'><h3>📝 Transcription</h3></div>", unsafe_allow_html=True)
    st.markdown(f"<div id='transcription'>{transcription}</div>", unsafe_allow_html=True)

    # --- CUSTOMIZATION SUGGESTIONS ---
    st.markdown("<div class='custom-card'><h3>🚘 Customization Suggestions</h3></div>", unsafe_allow_html=True)
    
    # Fetch a random subset of suggestions
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
        # Save the audio to a file
        suggestions_audio_path = "suggestions_audio_output.wav"
        tts.save(suggestions_audio_path)
        
        # Provide download link
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
    # Save uploaded audio file to a temporary file
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

# --- SOCIAL LINKS ---
st.markdown("""
    <div class="social-buttons">
        <a href="https://github.com/your-username" target="_blank">
            <img id="github-logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/GitHub_Invertocat_Logo.svg/1200px-GitHub_Invertocat_Logo.svg.png" alt="GitHub">
        </a>
        <a href="https://www.linkedin.com/in/your-linkedin" target="_blank">
            <img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" alt="LinkedIn">
        </a>
    </div>
""", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<div class='footer'>Developed by shaiiikh</div>", unsafe_allow_html=True)
