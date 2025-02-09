
# AI-Powered Car Customization Advisor

## Overview

AI-Powered Car Customization Advisor is a cutting-edge application that allows users to personalize their vehicles using voice or text descriptions. Powered by Generative AI, Whisper AI, and DALL-E, this tool provides customized suggestions and visual previews, all within a user-friendly Streamlit interface.

## Features

- **Voice and Text Input**: Describe car customizations using natural language.
- **Real-time Transcription**: Whisper AI converts voice inputs into text.
- **Personalized Suggestions**: AI generates tailored customization ideas.
- **Visual Previews**: DALL-E creates images based on descriptions.
- **Interactive UI**: Streamlit ensures an intuitive, smooth user experience.

## Tech Stack

- **Generative AI**: Provides smart customization suggestions.
- **Whisper AI**: Converts voice inputs to text.
- **DALL-E**: Generates real-time visual previews.
- **Streamlit**: Offers an easy-to-use interface.

## Installation

1. **Clone the Repository**

```bash
git clone https://github.com/shaiiikh/AI-Powered-Car-Customization-Advisor.git
cd AI-Powered-Car-Customization-Advisor
```

2. **Install Dependencies**

Ensure you have Python installed, then run:

```bash
pip install -r requirements.txt
```

3. **Set Up Environment Variables**

Create a `.env` file in the root directory and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

4. **Run the Application**

```bash
streamlit run main.py
```

## Requirements

The project dependencies are listed in `requirements.txt`:

```
openai-whisper
language-tool-python
openai>=1.0.0
pydub
gTTS
python-dotenv
ffmpeg-python
torch
streamlit
requests
Pillow
audio-recorder-streamlit
```

Ensure `ffmpeg` is installed on your system for audio processing.

## Usage

1. **Record Voice**: Use the built-in recorder to describe your customization.
2. **Upload Audio**: Alternatively, upload a pre-recorded audio file.
3. **Get Suggestions**: The AI will provide tailored customization ideas.
4. **View Visual Preview**: See your car's customization in real-time.

## Acknowledgments

Special thanks to Muhammad Usama for his guidance and support throughout this project.

## Connect with Me

- **GitHub**: [AI-Powered Car Customization Advisor](https://github.com/shaiiikh/AI-Powered-Car-Customization-Advisor)
- **LinkedIn**: [Ali Shaiiikh](https://www.linkedin.com/in/ali-shaiiikh)

## License

This project is licensed under the MIT License.

---

For any questions or suggestions, feel free to reach out or open an issue on the GitHub repository!
