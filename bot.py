import os
import google.generativeai as genai

# API Key ko GitHub Secrets se uthana
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Model setup
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_content():
    # 1. Image Prompt Banana
    prompt_response = model.generate_content("Generate a detailed prompt for an AI image generator to create a cinematic, 9:16 vertical image of Lord Krishna in a divine forest with ethereal lighting.")
    print("Image Prompt Generated:", prompt_response.text)

    # 2. Quote Banana
    quote_response = model.generate_content("Write a deep spiritual Hindi quote by Lord Krishna about life, in 10-15 words.")
    print("Quote Generated:", quote_response.text)

if __name__ == "__main__":
    generate_content()
