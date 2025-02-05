import openai
from pydub import AudioSegment
from io import BytesIO
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to convert audio file to text using Whisper (new API)
def process_audio(audio_file):
    # Load the audio file using pydub
    audio = AudioSegment.from_mp3(audio_file)
    
    # Convert the audio to a format suitable for Whisper (mono, 16kHz)
    audio = audio.set_channels(1).set_frame_rate(16000)
    
    # Save the audio to a temporary buffer
    buffer = BytesIO()
    audio.export(buffer, format="wav")
    buffer.seek(0)
    
    # Send the audio to Whisper API for transcription using the new method
    response = openai.Audio.transcribe("whisper-1", file=buffer)
    
    return response["text"]
