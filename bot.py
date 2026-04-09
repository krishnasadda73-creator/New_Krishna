import os
import requests
import time
import urllib.parse
import random
from PIL import Image, ImageDraw
import subprocess

# API Config
HF_TOKEN = os.getenv("HF_TOKEN")
# Stable Diffusion XL - One of the best free models
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_hf(prompt):
    # Retry logic kyunki kabhi kabhi model 'Wake up' hone mein time leta hai
    for i in range(3):
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        if response.status_code == 200:
            return response.content
        elif response.status_code == 503:
            print("Model is sleeping, waiting 20s...")
            time.sleep(20)
        else:
            print(f"HF Error: {response.status_code}")
    return None

def generate_content():
    try:
        # 1. Text Script (Pollinations Text is fine for this)
        print("Step 1: Fetching Quote...")
        quote = "Jai Shree Krishna"
        try:
            text_url = f"https://text.pollinations.ai/{urllib.parse.quote('Write a beautiful 10-word Hindi quote of Lord Krishna')}"
            quote = requests.get(text_url, timeout=10).text.strip()
        except: pass
        print(f"Quote: {quote}")

        # 2. Image Generation via Hugging Face
        print("Step 2: Generating Image via Hugging Face...")
        prompt = "Hyper-realistic cinematic portrait of Lord Krishna, divine lighting, 8k, highly detailed"
        img_data = query_hf(prompt)
        
        if img_data:
            with open('raw_image.jpg', 'wb') as f:
                f.write(img_data)
            print("Image downloaded from Hugging Face!")
        else:
            print("HF Failed. Using fallback.jpg...")
            if os.path.exists('fallback.jpg'):
                Image.open('fallback.jpg').convert("RGB").save('raw_image.jpg')
            else:
                Image.new('RGB', (1080, 1920), color=(30, 30, 30)).save('raw_image.jpg')

        # 3. Drawing Text
        img = Image.open("raw_image.jpg").convert("RGB")
        # HF images 1024x1024 hoti hain, hum ise reel size mein resize karenge
        img = img.resize((1080, 1920), Image.LANCZOS)
        w, h = img.size
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, h-450, w, h-50], fill=(0, 0, 0, 160))
        draw.text((w/2, h-250), quote, fill="white", anchor="mm")
        img.save("processed_image.jpg")

        # 4. Rendering Video
        bgm_folder = "BGM"
        selected_bgm = ""
        if os.path.exists(bgm_folder):
            files = [f for f in os.listdir(bgm_folder) if f.endswith('.mp3')]
            if files:
                selected_bgm = os.path.join(bgm_folder, random.choice(files))

        print("Step 4: FFmpeg Rendering...")
        cmd = f'ffmpeg -loop 1 -i processed_image.jpg '
        if selected_bgm:
            cmd += f'-i "{selected_bgm}" -c:v libx264 -t 10 -pix_fmt yuv420p -c:a aac -shortest '
        else:
            cmd += f'-c:v libx264 -t 10 -pix_fmt yuv420p '
        cmd += '-y final_reel.mp4'
        
        subprocess.run(cmd, shell=True, check=True)
        print("REEL GENERATED SUCCESSFULLY!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_content()
