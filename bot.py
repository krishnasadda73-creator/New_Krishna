import os
import requests
import time
import urllib.parse
import random
from PIL import Image, ImageDraw, ImageFont
import subprocess

def generate_content():
    try:
        # 1. Assets Generation
        print("Step 1: Generating Text & Image...")
        system_prompt = "Write a 1-sentence prompt for Lord Krishna image and a 10-word Hindi quote. Separate with |"
        text_url = f"https://text.pollinations.ai/{urllib.parse.quote(system_prompt)}"
        full_text = requests.get(text_url).text
        
        image_prompt = full_text.split('|')[0].strip() if "|" in full_text else "Lord Krishna divine"
        quote = full_text.split('|')[1].strip() if "|" in full_text else "Jai Shree Krishna"

        img_url = f"https://pollinations.ai/p/{urllib.parse.quote(image_prompt)}?width=1080&height=1920&model=flux"
        with open('raw_image.jpg', 'wb') as f:
            f.write(requests.get(img_url).content)

        # 2. Image pe Text (Pillow)
        print("Step 2: Drawing Text...")
        img = Image.open("raw_image.jpg")
        draw = ImageDraw.Draw(img)
        w, h = img.size
        # Bottom overlay for quote
        draw.rectangle([0, h-450, w, h-50], fill=(0, 0, 0, 160))
        draw.text((w/2, h-250), quote, fill="white", anchor="mm")
        img.save("processed_image.jpg")

        # 3. Random BGM Selection
        bgm_folder = "BGM"
        selected_bgm = ""
        
        if os.path.exists(bgm_folder):
            files = [f for f in os.listdir(bgm_folder) if f.endswith('.mp3')]
            if files:
                selected_bgm = os.path.join(bgm_folder, random.choice(files))
                print(f"Selected BGM: {selected_bgm}")

        # 4. FFmpeg Video Creation
        print("Step 4: Rendering Video...")
        if selected_bgm:
            cmd = (
                f'ffmpeg -loop 1 -i processed_image.jpg -i "{selected_bgm}" '
                f'-c:v libx264 -t 10 -pix_fmt yuv420p -vf "scale=1080:1920" '
                f'-c:a aac -shortest -y final_reel.mp4'
            )
        else:
            cmd = (
                f'ffmpeg -loop 1 -i processed_image.jpg '
                f'-c:v libx264 -t 10 -pix_fmt yuv420p -vf "scale=1080:1920" '
                f'-y final_reel.mp4'
            )
        
        subprocess.run(cmd, shell=True, check=True)
        print("SUCCESS: final_reel.mp4 generated!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_content()
