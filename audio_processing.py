# audio_processing.py
import whisper

# Load the Whisper model
model = whisper.load_model("base")

# Function to transcribe audio
def transcribe_audio(audio_path):
    result = model.transcribe(audio_path)
    return result["text"]
