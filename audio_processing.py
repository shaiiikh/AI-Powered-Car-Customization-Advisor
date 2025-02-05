# audio_processing.py
from pydub import AudioSegment
import whisper

# Load the Whisper model
model = whisper.load_model("base")

# Function to transcribe audio
def transcribe_audio(audio_path):
    # Convert the audio to WAV format if necessary
    audio = AudioSegment.from_file(audio_path)
    audio.export("temp.wav", format="wav")
    
    # Use Whisper for transcription
    result = model.transcribe("temp.wav")
    return result["text"]
