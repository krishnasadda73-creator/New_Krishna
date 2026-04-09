import os
import requests
import time
from google import genai

# API Key setup
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_content():
    try:
        # 1. Gemini se Text lena (Iska quota kabhi khatam nahi hota)
        print("Step 1: Fetching Script from Gemini...")
        response = client.models.generate_content(
            model="gemini-1.5-flash", # Stable model use kar rahe hain
            contents="Write a 1-sentence hyper-realistic English prompt for an AI to create a cinematic 9:16 portrait of Lord Krishna with divine lighting. Then on a new line, write a 10-word Hindi quote."
        )
        
        full_text = response.text
        lines = full_text.strip().split('\n')
        image_prompt = lines[0].strip()
        quote = lines[-1].strip() if len(lines) > 1 else "Jai Shree Krishna"
        
        print(f"Prompt: {image_prompt}")

        # 2. Image Generation via Pollinations (FLUX Model - Best Quality)
        print("Step 2: Generating High Quality Image...")
        encoded_prompt = requests.utils.quote(image_prompt)
        seed = int(time.time())
        # 'model=flux' use karne se Gemini jaisi quality milti hai
        image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1080&height=1920&seed={seed}&model=flux"
        
        img_data = requests.get(image_url).content
        
        if len(img_data) > 5000:
            with open('krishna_image.jpg', 'wb') as f:
                f.write(img_data)
            print("SUCCESS: Image saved!")
        else:
            print("ERROR: Image download failed.")
            exit(1)

        with open('quote.txt', 'w', encoding='utf-8') as f:
            f.write(quote)

    except Exception as e:
        print(f"Bhai, Gemini ne block kiya hai, wait 24 hours for Gemini 2.0: {e}")
        exit(1)

if __name__ == "__main__":
    generate_content()
