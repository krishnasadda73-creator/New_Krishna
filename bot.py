import os
import requests
import time
import urllib.parse

def generate_content():
    try:
        # 1. Pollinations se Text (Prompt + Quote) mangwana
        print("Step 1: Fetching Script from AI...")
        
        system_prompt = "You are a creative assistant. Write a 1-sentence image prompt for Lord Krishna and a 10-word Hindi quote. Separate them with a pipe symbol |"
        user_input = "Create a new Krishna post"
        
        # Pollinations Text API (Free & No Key)
        text_url = f"https://text.pollinations.ai/{urllib.parse.quote(system_prompt + ' ' + user_input)}"
        
        response = requests.get(text_url)
        full_text = response.text
        print(f"AI Response: {full_text}")
        
        if "|" in full_text:
            image_prompt = full_text.split('|')[0].strip()
            quote = full_text.split('|')[1].strip()
        else:
            image_prompt = "Cinematic 9:16 portrait of Lord Krishna in divine light"
            quote = "Karmanye vadhikaraste ma phaleshu kadachana"

        # 2. Image Generation (Pollinations Flux)
        print(f"Step 2: Generating Image for: {image_prompt}")
        
        encoded_prompt = requests.utils.quote(image_prompt)
        seed = int(time.time())
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
        print(f"Bhai ab toh ye chalna hi chahiye: {e}")
        exit(1)

if __name__ == "__main__":
    generate_content()
