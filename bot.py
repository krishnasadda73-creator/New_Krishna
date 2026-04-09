import os
from google import genai

# API Key setup
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_content():
    try:
        # 1. Image Prompt Banana (Model name changed to gemini-2.0-flash)
        prompt_response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents="Generate a detailed prompt for an AI image generator to create a cinematic, 9:16 vertical image of Lord Krishna in a divine forest."
        )
        print("Image Prompt Generated:", prompt_response.text)

        # 2. Quote Banana
        quote_response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents="Write a deep spiritual Hindi quote by Lord Krishna about life, in 10-15 words."
        )
        print("Quote Generated:", quote_response.text)
        
    except Exception as e:
        print(f"Error aagaya bhai: {e}")

if __name__ == "__main__":
    generate_content()
