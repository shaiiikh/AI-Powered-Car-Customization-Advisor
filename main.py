import streamlit as st
import sounddevice as sd
import numpy as np
import wave
import tempfile
import random
import time
import matplotlib.pyplot as plt
import base64
from gtts import gTTS
from audio_processing import transcribe_audio

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
            width: 30px;
            height: 30px;
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
        }
        .amplitude-plot {
            height: 200px;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="header">
        <h1>🚗💨 AI-Powered Car Customization Advisor</h1>
    </div>
""", unsafe_allow_html=True)

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

# If recording is in progress, perform recording
if st.session_state.is_recording:
    st.button("Stop Recording", on_click=stop_recording)

    # Record audio
    st.markdown("Recording... 🎙️ Speak now!")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
    sd.wait()

    # Display the waveform (amplitude) of the recording
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(np.linspace(0, duration, len(audio_data)), audio_data)
    ax.set_title("Recording Amplitude")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Amplitude")
    st.pyplot(fig)

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

    suggestions_pool = [
        "How about adding a custom paint job to give your car a fresh new look?",
        "Consider upgrading your wheels for better performance and style.",
        "Installing a new set of lights could really enhance the car’s appearance.",
        "You might want to check out custom seat covers that suit your style.",
        "How about adding a sunroof for a more luxurious feel?",
        "Consider a custom spoiler for added performance and aesthetics.",
        "A new sound system could make your car feel like a concert hall!"
    ]
    suggestions = random.sample(suggestions_pool, 3)  # Pick 3 random suggestions
    for suggestion in suggestions:
        st.markdown(f"- {suggestion}")

    # --- TEXT-TO-SPEECH (TTS) ---
    tts = gTTS(text=" ".join(suggestions), lang="en")
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

else:
    st.button("Start Recording", on_click=start_recording)

# --- FOOTER ---
st.markdown("<div class='footer'>Developed by Shaiiikh</div>", unsafe_allow_html=True)
