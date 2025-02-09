import streamlit as st
import whisper
import tempfile
import os
from dotenv import load_dotenv
from pydub import AudioSegment
from PIL import Image
import requests
from openai import OpenAI
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder

load_dotenv()
client = OpenAI()

# Streamlit Page Configuration
st.set_page_config(page_title="AI Car Customization", page_icon="🚗", layout="wide")
os.environ["STREAMLIT_WATCH_USE_POLLING"] = "true"

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
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="header">
        <h1>🚗🚨 AI-Powered Car Customization Advisor</h1>
    </div>
""", unsafe_allow_html=True)

# Load Whisper model
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

model = load_whisper_model()

# Transcribe audio function
def transcribe_audio(audio_file_path):
    audio = AudioSegment.from_file(audio_file_path)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        audio.export(tmp_file, format="wav")
        tmp_file_path = tmp_file.name
    audio_array = whisper.load_audio(tmp_file_path)
    result = model.transcribe(audio_array)
    os.remove(tmp_file_path)
    return result['text']

# Get customization suggestions using OpenAI GPT
def get_customization_suggestions(transcription):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant providing car customization suggestions."},
            {"role": "user", "content": f"Suggest car modifications for the following request: {transcription}"}
        ]
    )
    return completion.choices[0].message.content

# Generate car image using DALL-E
def generate_car_image(prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    image_response = requests.get(image_url)
    with open("car_customization.jpg", "wb") as f:
        f.write(image_response.content)
    return "car_customization.jpg"

# --- RECORD AUDIO FEATURE ---
st.markdown("### 🎧 Record Your Own Voice")

audio_bytes = audio_recorder(pause_threshold=10.0, text="Click to Record")

if audio_bytes:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio_file:
        temp_audio_file.write(audio_bytes)
        temp_audio_file_path = temp_audio_file.name

    st.audio(audio_bytes, format="audio/mp3")

    transcription = transcribe_audio(temp_audio_file_path).strip()
    st.markdown(f"<div class='custom-card'><h3>📝 Transcription</h3><p>{transcription}</p></div>", unsafe_allow_html=True)

    suggestions = get_customization_suggestions(transcription)
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

    suggestions = get_customization_suggestions(transcription)
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
        Developed by Junaid Hossain Mridul 👨‍💻
    </div>
""", unsafe_allow_html=True)
