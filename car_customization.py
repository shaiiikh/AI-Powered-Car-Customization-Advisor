import openai
import os
from dotenv import load_dotenv

# Load API key from .env file (optional, but recommended for security)
load_dotenv()

# Set OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to get car customization suggestions from GPT-4
def get_customization_suggestions(user_input):
    try:
        prompt = f"User wants to customize a car: {user_input}. Suggest possible customization options including color, accessories, and style."
        
        response = openai.Completion.create(
            model="gpt-4", 
            prompt=prompt, 
            max_tokens=100
        )
        
        # Get the suggestion from GPT-4 response
        customization_suggestions = response.choices[0].text.strip()
        return customization_suggestions

    except Exception as e:
        return f"Error occurred while getting customization suggestions: {str(e)}"

# Function to generate a car image using DALL-E
def generate_car_image(customizations):
    try:
        prompt = f"Generate an image of a {customizations} car."
        
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        
        # Extract the image URL from the response
        image_url = response['data'][0]['url']
        return image_url
    
    except Exception as e:
        return f"Error occurred while generating the car image: {str(e)}"
