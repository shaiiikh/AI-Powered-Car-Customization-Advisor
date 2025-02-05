import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Test if the API key is loaded correctly
def test_openai_api():
    try:
        # Using the updated API for GPT-3.5
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the appropriate model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, can you help me?"}
            ]
        )
        print("API is working! Response: ", response)
        return True
    except Exception as e:
        print("Error: ", e)
        return False

# Test the API
if __name__ == "__main__":
    if test_openai_api():
        print("API Test Successful!")
    else:
        print("API Test Failed!")
