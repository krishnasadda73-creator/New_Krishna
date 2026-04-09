import os
import requests
import time
from google import genai

# API Key setup
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_content():
    try:
        # 1. Gemini se Text lena
        print("Step 1: Fetching Script from Gemini...")
        
        # Model ka naam sirf 'gemini-1.5-flash' rakho (No prefix)
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents="Generate a 1-sentence hyper-realistic English prompt for an AI to create a cinematic 9:16 portrait of Lord Krishna. Then on a new line, write a 10-word Hindi quote about life."
        )
        
        full_text = response.text
        print(f"Gemini Response: {full_text}")
        
        # Line splitting logic
        lines = [line.strip() for line in full_text.strip().split('\n') if line.strip()]
        image_prompt = lines[0] if lines else "Lord Krishna divine portrait cinematic 9:16"
        quote = lines[-1] if len(lines) > 1 else "Jai Shree Krishna"

        # 2. Image Generation (Pollinations - Flux Model)
        print(f"Step 2: Generating Image...")
        
        encoded_prompt = requests.utils.quote(image_prompt)
        seed = int(time.time())
        # Flux model provides 100% accuracy for cinematic prompts
        image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1080&height=1920&seed={seed}&model=flux"
        
        img_data = requests.get(image_url).content
        
        if len(img_data) > 5000:
            with open('krishna_image.jpg', 'wb') as f:
                f.write(img_data)
            print(f"SUCCESS: Image saved! Size: {len(img_data)} bytes")
        else:
            print("ERROR: Image download failed.")
            exit(1)

        # 3. Save Quote
        with open('quote.txt', 'w', encoding='utf-8') as f:
            f.write(quote)

    except Exception as e:
        print(f"Abhi bhi issue hai bhai: {e}")
        exit(1)

if __name__ == "__main__":
    generate_content()
