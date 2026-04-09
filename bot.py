import os
import requests
import time
from google import genai

# API Key setup
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_content():
    try:
        # 1. Gemini se Prompt aur Quote lena
        print("Step 1: Fetching prompt from Gemini...")
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents="Write a 1-sentence English prompt for an AI to create a cinematic vertical 9:16 portrait of Lord Krishna. Also, write a 10-word Hindi quote about life."
        )
        
        full_text = response.text
        # Safety split: Pehli line prompt, baaki quote
        lines = full_text.strip().split('\n')
        image_prompt = lines[0].strip()
        quote = " ".join(lines[1:]).strip() if len(lines) > 1 else "Jai Shree Krishna"
        
        print(f"Prompt: {image_prompt}")

        # 2. Save Quote first (Safety)
        with open('quote.txt', 'w', encoding='utf-8') as f:
            f.write(quote)
        print("Step 2: Quote saved.")

        # 3. Image Generation with Pollinations (Retry Logic)
        print("Step 3: Generating image via Pollinations...")
        
        # URL Cleaning: Sirf zaroori characters rakhenge
        clean_prompt = "".join(x for x in image_prompt if x.isalnum() or x in " ")
        encoded_prompt = clean_prompt.replace(' ', '%20')
        
        # Seed change karne se har baar nayi image milti hai
        seed = int(time.time()) 
        image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=720&height=1280&seed={seed}&model=flux"
        
        print(f"Requesting URL: {image_url}")
        
        response = requests.get(image_url, timeout=30)
        
        if response.status_code == 200 and len(response.content) > 5000:
            with open('krishna_image.jpg', 'wb') as handler:
                handler.write(response.content)
            print("SUCCESS: krishna_image.jpg saved successfully!")
        else:
            print(f"FAILED: Status {response.status_code}, Size {len(response.content)}")
            # Agar fail ho jaye toh ek blank file bana do taaki Git error na de
            open('krishna_image.jpg', 'a').close() 

    except Exception as e:
        print(f"SYSTEM ERROR: {e}")
        # Error aane par bhi empty files banao taaki workflow na tute
        open('krishna_image.jpg', 'a').close()
        open('quote.txt', 'a').close()

if __name__ == "__main__":
    generate_content()
