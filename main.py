import streamlit as st
import tempfile
import os
from dotenv import load_dotenv
from pydub import AudioSegment
import openai
from PIL import Image
import requests
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app layout
st.set_page_config(page_title="AI Car Customization Advisor", page_icon="🚗", layout="wide")

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
        audio {
            width: 100%;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="header">
        <h1>🚗🚨 AI-Powered Car Customization Advisor</h1>
    </div>
""", unsafe_allow_html=True)

# Function to transcribe speech to text using OpenAI Whisper API
def transcribe_audio(audio_file):
    audio = AudioSegment.from_file(audio_file)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        audio.export(tmp_file, format="wav")
        tmp_file_path = tmp_file.name
    
    with open(tmp_file_path, "rb") as audio_file:
        transcription_result = openai.Audio.transcribe("whisper-1", audio_file)
    
    os.remove(tmp_file_path)
    return transcription_result['text']

# Function to generate car customization suggestions using OpenAI GPT
def generate_customization_suggestions(transcription):
    prompt = f"Based on the following car customization request, suggest detailed modifications including paint, rims, body kits, and interior changes:\n\n{transcription}\n\nSuggestions:" 
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Function to generate car image using DALL-E
def generate_car_image(prompt):
    response = openai.Image.create(
        model="dall-e-3",
        prompt=prompt,
        quality="standard",
        n=1,
    )
    image_url = response['data'][0]['url']
    image_response = requests.get(image_url)
    with open("car_customization.jpg", "wb") as f:
        f.write(image_response.content)
    return "car_customization.jpg"

# --- RECORD AUDIO FEATURE ---
st.markdown("### 🎧 Record Your Own Voice")

audio_bytes = audio_recorder(pause_threshold=60.0, text="Click to Record")

if audio_bytes:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio_file:
        temp_audio_file.write(audio_bytes)
        temp_audio_file_path = temp_audio_file.name

    st.audio(audio_bytes, format="audio/mp3")

    transcription = transcribe_audio(temp_audio_file_path).strip()
    st.markdown(f"<div class='custom-card'><h3>📝 Transcription</h3><p>{transcription}</p></div>", unsafe_allow_html=True)

    if st.button("Generate Suggestions and Image"):
        suggestions = generate_customization_suggestions(transcription)
        st.markdown("<div class='custom-card'><h3>🚗 Customization Suggestions</h3>", unsafe_allow_html=True)
        for suggestion in suggestions.split("\n"):
            st.markdown(f"- {suggestion}")
        st.markdown("</div>", unsafe_allow_html=True)

        image_prompt = f"A car customized with the following features: {transcription}"
        st.markdown("<div class='custom-card'><h3>🖼 Customized Car Visualization</h3>", unsafe_allow_html=True)
        with st.spinner('Generating car image...'):
            car_image_path = generate_car_image(image_prompt)
        car_image = Image.open(car_image_path)
        st.image(car_image, caption="Your Customized Car", use_container_width=True)

        tts = gTTS(text=suggestions, lang="en")
        tts.save("suggestions_audio.mp3")

        with open("suggestions_audio.mp3", "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")
else:
    st.warning("Click the record button to start recording your voice.")

# --- UPLOAD AUDIO FILE FEATURE ---
st.markdown("### 📂 Browse and Upload Your Audio File")
audio_file = st.file_uploader("Choose an audio file...", type=["wav", "mp3", "flac"])

if audio_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
        temp_file.write(audio_file.read())
        audio_file_path = temp_file.name

    st.audio(audio_file, format="audio/wav")

    transcription = transcribe_audio(audio_file_path).strip()
    st.markdown(f"<div class='custom-card'><h3>📝 Transcription</h3><p>{transcription}</p></div>", unsafe_allow_html=True)

    if st.button("Generate Suggestions and Image", key='upload_btn'):
        suggestions = generate_customization_suggestions(transcription)
        st.markdown("<div class='custom-card'><h3>🚗 Customization Suggestions</h3>", unsafe_allow_html=True)
        for suggestion in suggestions.split("\n"):
            st.markdown(f"- {suggestion}")
        st.markdown("</div>", unsafe_allow_html=True)

        image_prompt = f"A car customized with the following features: {transcription}"
        st.markdown("<div class='custom-card'><h3>🖼 Customized Car Visualization</h3>", unsafe_allow_html=True)
        with st.spinner('Generating car image...'):
            car_image_path = generate_car_image(image_prompt)
        car_image = Image.open(car_image_path)
        st.image(car_image, caption="Your Customized Car", use_container_width=True)

        tts = gTTS(text=suggestions, lang="en")
        tts.save("suggestions_audio.mp3")

        with open("suggestions_audio.mp3", "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")

# --- FOOTER ---
st.markdown("""
    <div class='footer'>
        Developed by shaiiikh 👨‍💻
    </div>
""", unsafe_allow_html=True)