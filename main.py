# main.py
import streamlit as st
import os
from audio_processing import transcribe_audio
from car_customization import get_customization_suggestions
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def app():
    st.title("AI-Powered Car Customization Advisor")
    
    # File upload section
    audio_file = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a"])
    
    if audio_file is not None:
        # Save the uploaded audio file
        with open("uploaded_audio.wav", "wb") as f:
            f.write(audio_file.getbuffer())
        
        # Transcribe the audio
        transcription = transcribe_audio("uploaded_audio.wav")
        st.write("Transcription: ", transcription)
        
        # Get car customization suggestions
        suggestions = get_customization_suggestions(transcription)
        st.write("Customization Suggestions: ", suggestions)
        
        # Optionally, generate car image (if you have this functionality)
        # car_image = generate_car_image(suggestions)
        # st.image(car_image)

# Run the Streamlit app
if __name__ == "__main__":
    app()
