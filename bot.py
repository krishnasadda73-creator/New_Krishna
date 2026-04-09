import os
import requests
from google import genai

# API Key setup
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_content():
    try:
        # 1. Gemini se Prompt aur Quote lena
        print("Fetching prompt from Gemini...")
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents="Write a 1-sentence English prompt for an AI image of Lord Krishna. Also, a 10-word Hindi quote."
        )
        
        full_text = response.text
        # Safety split: Agar Gemini galti se point na de toh poora text prompt ban jaye
        image_prompt = full_text.split('\n')[0].strip()
        quote = full_text.strip()
        
        print(f"Generated Prompt: {image_prompt}")

        # 2. Image Generation (Direct Pollinations for stability)
        print("Generating image via Pollinations...")
        # URL ko clean karna zaroori hai
        clean_prompt = "".join(x for x in image_prompt if x.isalnum() or x in " -_")
        image_url = f"https://pollinations.ai/p/{clean_prompt.replace(' ', '%20')}?width=720&height=1280&seed=42&model=flux"
        
        img_data = requests.get(image_url).content
        
        # Check karna ki data mila ya nahi
        if len(img_data) > 1000: # Minimum size check (1kb)
            with open('krishna_image.jpg', 'wb') as handler:
                handler.write(img_data)
            print("Successfully saved krishna_image.jpg")
        else:
            print("Error: Image data too small, might be a failed request.")

        # 3. Save Quote
        with open('quote.txt', 'w', encoding='utf-8') as f:
            f.write(quote)
            
    except Exception as e:
        print(f"Bhai error aaya hai: {e}")

if __name__ == "__main__":
    generate_content()
