import os
import requests
import time
import urllib.parse
import random
from PIL import Image, ImageDraw
import subprocess

def generate_content():
    try:
        # 1. Generate Text (AI Script)
        print("Step 1: Fetching Script...")
        text_url = f"https://text.pollinations.ai/{urllib.parse.quote('Write 1-sentence prompt for Lord Krishna portrait | 10-word Hindi quote')}"
        full_text = requests.get(text_url).text
        image_prompt = full_text.split('|')[0].strip() if "|" in full_text else "Lord Krishna divine portrait"
        quote = full_text.split('|')[1].strip() if "|" in full_text else "Jai Shree Krishna"
        print(f"Quote: {quote}")

        # 2. Image Generation (Prodia API via Pollinations - Stable Route)
        # Hum Prodia ka model specify karenge jo hamesha up rehta hai
        print("Step 2: Generating Image via Prodia Engine...")
        encoded_prompt = urllib.parse.quote(image_prompt)
        # Seed change karne se har baar unique image aayegi
        seed = random.randint(1, 99999)
        
        # Is baar hum model specify kar rahe hain: 'v1.5-pruned-emaonly' (Very Stable)
        img_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&model=v1.5-pruned-emaonly&seed={seed}&nologo=true"
        
        # Retry with a bit of delay
        response = requests.get(img_url, timeout=30)
        
        if response.status_code == 200 and len(response.content) > 20000:
            with open('raw_image.jpg', 'wb') as f:
                f.write(response.content)
            print("Image downloaded successfully!")
        else:
            print("Stable API also busy. Using fallback.jpg...")
            if os.path.exists('fallback.jpg'):
                img = Image.open('fallback.jpg')
                img.save('raw_image.jpg')
            else:
                raise Exception("No image source available!")

        # 3. Processing (Pillow)
        print("Step 3: Drawing Text...")
        img = Image.open("raw_image.jpg").convert("RGB")
        w, h = img.size
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, h-450, w, h-50], fill=(0, 0, 0, 160))
        draw.text((w/2, h-250), quote, fill="white", anchor="mm")
        img.save("processed_image.jpg")

        # 4. BGM & FFmpeg
        bgm_folder = "BGM"
        selected_bgm = ""
        if os.path.exists(bgm_folder):
            files = [f for f in os.listdir(bgm_folder) if f.endswith('.mp3')]
            if files:
                selected_bgm = os.path.join(bgm_folder, random.choice(files))

        print("Step 4: FFmpeg Rendering...")
        cmd = f'ffmpeg -loop 1 -i processed_image.jpg '
        if selected_bgm:
            cmd += f'-i "{selected_bgm}" -c:v libx264 -t 10 -pix_fmt yuv420p -vf "scale=1080:1920" -c:a aac -shortest '
        else:
            cmd += f'-c:v libx264 -t 10 -pix_fmt yuv420p -vf "scale=1080:1920" '
        cmd += '-y final_reel.mp4'
        
        subprocess.run(cmd, shell=True, check=True)
        print("REEL GENERATED SUCCESSFULLY!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_content()
