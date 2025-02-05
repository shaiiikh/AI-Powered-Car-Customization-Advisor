import streamlit as st
from audio_processing import process_audio
from car_customization import get_customization_suggestions, generate_car_image

# Streamlit App
def app():
    st.title("AI-Powered Car Customization Advisor")
    
    # Upload an audio file (e.g., 'test_audio.mp3')
    audio_file = st.file_uploader("Upload your audio file", type=["mp3", "wav"])
    
    if audio_file is not None:
        st.audio(audio_file, format='audio/mp3')
        
        # Process audio file and get transcription
        transcription = process_audio(audio_file)
        st.write(f"You said: {transcription}")
        
        # Get AI customization suggestions
        suggestions = get_customization_suggestions(transcription)
        st.write(f"AI Suggestions: {suggestions}")
        
        # Generate and display car image preview
        car_image_url = generate_car_image(suggestions)
        st.image(car_image_url, caption="Your Customized Car")

if __name__ == "__main__":
    app()
