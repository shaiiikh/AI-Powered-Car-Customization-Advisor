import streamlit as st
import os
from audio_processing import transcribe_audio
from car_customization import get_customization_suggestions
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def app():
    st.title("AI-Powered Car Customization Advisor")
    
    # Add a short description
    st.markdown("""
    Welcome to the AI-Powered Car Customization Advisor! 🚗✨  
    Upload an audio file describing your car customization preferences, and our AI will generate suggestions for you.  
    Let's get started!
    """)

    # Display GitHub handle for reference
    st.markdown("""
    Developed by: [Muhammad Ali Shaikh](https://github.com/shaiiikh)
    """)

    # File upload section
    st.subheader("Upload Your Audio File")
    audio_file = st.file_uploader("Choose an Audio file (mp3, wav, m4a)", type=["mp3", "wav", "m4a"])
    
    if audio_file is not None:
        # Save the uploaded audio file
        with open("uploaded_audio.wav", "wb") as f:
            f.write(audio_file.getbuffer())
        
        # Transcribe the audio
        transcription = transcribe_audio("uploaded_audio.wav")
        
        # Display transcription
        st.subheader("Transcription:")
        st.write(transcription)

        # Provide suggestions
        st.subheader("AI Customization Suggestions")
        suggestions = get_customization_suggestions(transcription)
        st.write(suggestions)
        
        # Option to save suggestions
        if st.button("Save Customization"):
            save_user_customization({
                "transcription": transcription,
                "suggestions": suggestions
            })
            st.success("Customization saved successfully!")

    # Error handling for empty file upload
    else:
        st.warning("Please upload an audio file to get started.")

def save_user_customization(customization_data):
    """
    This function will save the user's customization data (e.g., transcription and suggestions) locally.
    You can also extend this to save the data to a database if needed.
    """
    if not os.path.exists('user_data.json'):
        with open('user_data.json', 'w') as f:
            json.dump([], f)

    # Load existing data
    with open('user_data.json', 'r') as f:
        data = json.load(f)

    # Append new customization data
    data.append(customization_data)

    # Save back to the file
    with open('user_data.json', 'w') as f:
        json.dump(data, f, indent=4)

# Run the Streamlit app
if __name__ == "__main__":
    app()
