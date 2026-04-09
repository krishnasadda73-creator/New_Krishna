import os
import requests
import time
import urllib.parse
import random
from PIL import Image, ImageDraw
import subprocess

# API Config
HF_TOKEN = os.getenv("HF_TOKEN")
# Stable Diffusion 1.5 - Extremely reliable
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_hf(prompt):
    for i in range(3):
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=60)
            if response.status_code == 200:
                return response.content
            elif response.status_code == 503:
                print("Model is loading, waiting 20s...")
                time.sleep(20)
            else:
                print(f"HF Error: {response.status_code}")
        except Exception as e:
            print(f"Request Error: {e}")
    return None

def generate_content():
    try:
        # 1. Text Script
        print("Step 1: Fetching Quote...")
        quote = "Jai Shree Krishna"
        try:
            text_url = f"https://text.pollinations.ai/{urllib.parse.quote('Write a beautiful 10-word Hindi quote of Lord Krishna')}"
            res = requests.get(text_url, timeout=10)
            if res.status_code == 200:
                quote = res.text.strip()
        except: pass
        print(f"Quote: {quote}")

        # 2. Image Generation
        print("Step 2: Generating Image via HF...")
        prompt = "Portrait of Lord Krishna, divine smile, peacock feather, cinematic lighting, 4k"
        img_data = query_hf(prompt)
        
        if img_data and len(img_data) > 5000:
            with open('raw_image.jpg', 'wb') as f:
                f.write(img_data)
            print("Image saved from HF!")
        else:
            print("HF Failed. Checking for fallback...")
            if os.path.exists('fallback.jpg'):
                Image.open('fallback.jpg').convert("RGB").save('raw_image.jpg')
            else:
                Image.new('RGB', (1080, 1920), color=(20, 20, 20)).save('raw_image.jpg')

        # 3. Processing
        img = Image.open("raw_image.jpg").convert("RGB")
        img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
        w, h = img.size
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, h-450, w, h-50], fill=(0, 0, 0, 160))
        # Default font
        draw.text((w/2, h-250), quote, fill="white", anchor="mm")
        img.save("processed_image.jpg")

        # 4. BGM & FFmpeg
        bgm_folder = "BGM"
        selected_bgm = ""
        if os.path.exists(bgm_folder):
            files = [f for f in os.listdir(bgm_folder) if f.endswith('.mp3')]
            if files:
                selected_bgm = os.path.join(bgm_folder, random.choice(files))

        print("Step 4: Rendering...")
        if selected_bgm:
            cmd = f'ffmpeg -loop 1 -i processed_image.jpg -i "{selected_bgm}" -c:v libx264 -t 10 -pix_fmt yuv420p -vf "scale=1080:1920" -c:a aac -shortest -y final_reel.mp4'
        else:
            cmd = f'ffmpeg -loop 1 -i processed_image.jpg -c:v libx264 -t 10 -pix_fmt yuv420p -vf "scale=1080:1920" -y final_reel.mp4'
        
        subprocess.run(cmd, shell=True, check=True)
        print("SUCCESS!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_content()
