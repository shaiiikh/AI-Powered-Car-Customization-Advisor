from gtts import gTTS

# Define a sample car customization description
customization_description = """
I want to customize my car with a sleek metallic blue paint, add sport rims, and install a leather interior. 
The car should have a modern and elegant look with a sunroof and tinted windows. 
Also, I'd like to include a premium sound system and a navigation system.
"""

# Use gTTS to generate speech from the description
tts = gTTS(text=customization_description, lang='en')

# Save the generated audio to an MP3 file
audio_filename = "test_customization_audio.mp3"
tts.save(audio_filename)

print(f"Test audio saved as {audio_filename}")
